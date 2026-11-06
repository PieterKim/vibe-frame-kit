#!/usr/bin/env python3
"""Install a checked, recoverable snapshot; never modify Codex config or credentials."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import sys
import tempfile

SOURCE = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inside(base, relative):
    path = base / relative
    if path.is_symlink() or not path.resolve().is_relative_to(base.resolve()):
        raise ValueError(f"Unsafe target: {relative}")
    # Reject linked parents too, including links pointing within the target.
    for parent in path.parents:
        if parent == base.parent:
            break
        if parent.is_symlink():
            raise ValueError(f"Linked target parent: {relative}")
    return path


def payload(scope, legacy_aliases=False):
    result = {}
    skills = sorted((SOURCE / "skills").glob("*/SKILL.md"))
    if len(skills) != 10:
        raise ValueError("Expected 10 source skills")
    for entry in skills:
        text = entry.read_text(encoding="utf-8")
        if not text.startswith("---\nname: " + entry.parent.name + "\ndescription: "):
            raise ValueError(f"Invalid skill metadata: {entry.parent.name}")
        for template in re.findall(r"templates/([a-z-]+\.md)", text):
            if not (SOURCE / "templates" / template).is_file():
                raise ValueError(f"Missing template: {template}")
    for required in ("agents/routing.md", "docs/course-workflow.md"):
        if not (SOURCE / required).is_file():
            raise ValueError(f"Missing source: {required}")
    for folder in ("agents", "templates", "prompts", "docs", "config", "skills"):
        directory = SOURCE / folder
        if not directory.is_dir():
            raise ValueError(f"Missing source: {folder}")
        for entry in sorted(directory.rglob("*")):
            if entry.is_symlink():
                raise ValueError(f"Linked source: {entry}")
            if not entry.is_file():
                continue
            if folder == "skills":
                prefix = Path(".agents/skills") if scope == "project" else Path("skills")
                relative = prefix / entry.relative_to(directory)
            else:
                prefix = Path() if scope == "project" else Path("vibe-frame-kit")
                relative = prefix / entry.relative_to(SOURCE)
            result[relative.as_posix()] = entry.read_bytes()
    # Only the standalone, credential-free checker is installed, not installer/test engines.
    checker = SOURCE / "scripts/check-environment.py"
    if not checker.is_file() or checker.is_symlink() or checker.parent.is_symlink():
        raise ValueError("Missing or linked source: scripts/check-environment.py")
    prefix = Path() if scope == "project" else Path("vibe-frame-kit")
    result[(prefix / "scripts/check-environment.py").as_posix()] = checker.read_bytes()
    agents = SOURCE / "AGENTS.md"
    if not agents.is_file():
        raise ValueError("Missing source: AGENTS.md")
    relative = "AGENTS.md" if scope == "project" else "vibe-frame-kit/AGENTS.md"
    result[relative] = agents.read_bytes()
    if legacy_aliases:
        # Keep the original global paths current as well as the new resource package.
        # This preserves old AGENTS/routing links and existing classroom references.
        for name, data in list(result.items()):
            if name.startswith("vibe-frame-kit/"):
                result[name.removeprefix("vibe-frame-kit/")] = data
    return result


def install(target, scope, dry_run=False, fail_after=None, migrate_legacy=False):
    target = target.absolute()
    if target.is_symlink():
        raise ValueError("Target cannot be a symlink")
    manifest_name = ".vibe-frame-kit-install.json"
    manifest_path = inside(target, manifest_name)
    old = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    if old and old.get("scope") != scope:
        raise ValueError("Installation scope conflicts with previous installation")
    old_files = old.get("files", {})
    legacy_aliases = bool(old.get("legacy_aliases", False))
    legacy_files = {}
    if migrate_legacy and not old:
        if scope != "global":
            raise ValueError("Legacy migration is for the original global installation only")
        baseline = json.loads((SOURCE / "config/legacy-install-manifest.json").read_text(encoding="utf-8"))
        legacy_files = baseline["files"]
        def matches_legacy(name):
            path = inside(target, name)
            return path.is_file() and digest(path.read_bytes().replace(b"\r\n", b"\n")) == legacy_files[name]
        if not any(matches_legacy(name) for name in legacy_files if name.startswith("skills/")):
            raise ValueError("No recognized original installation found; use a clean project or review manually")
        legacy_aliases = True
    files = payload(scope, legacy_aliases)  # Validate sources before touching target.
    if set(old_files) - set(files):
        raise ValueError("Old managed paths were removed upstream; review before migration")
    for name, content in files.items():
        path = inside(target, name)
        if path.exists():
            if not path.is_file():
                raise ValueError(f"Target is not a file: {name}")
            current = digest(path.read_bytes())
            expected = old_files.get(name)
            recognized_legacy = name in legacy_files and digest(path.read_bytes().replace(b"\r\n", b"\n")) == legacy_files[name]
            if current != digest(content) and current != expected and not recognized_legacy:
                raise ValueError(f"Conflict; existing file preserved: {name}")
    manifest = {"scope": scope, "legacy_aliases": legacy_aliases,
                "files": {k: digest(v) for k, v in files.items()}}
    files[manifest_name] = (json.dumps(manifest, indent=2) + "\n").encode()
    changes = [(name, data) for name, data in files.items()
               if not (target / name).exists() or (target / name).read_bytes() != data]
    if dry_run:
        print(f"Preflight passed: {len(changes)} file changes; scope={scope}")
        return
    # Persist recovery data before any mutation; keep backup on failure as well.
    target.mkdir(parents=True, exist_ok=True)
    backup = target / (".vibe-frame-kit-backups" if scope == "project" else "vibe-frame-kit-backups")
    inside(target, backup.relative_to(target))
    backup.mkdir(exist_ok=True)
    journal = Path(tempfile.mkdtemp(prefix="install-", dir=backup)) if changes else None
    original = {}
    changed = []
    try:
        for index, (name, data) in enumerate(changes):
            path = inside(target, name)
            original[name] = path.read_bytes() if path.exists() else None
            if original[name] is not None:
                saved = journal / name
                saved.parent.mkdir(parents=True, exist_ok=True)
                saved.write_bytes(original[name])
        if journal:
            (journal / "recovery.json").write_text(json.dumps({
                "target": str(target), "existing": [n for n,v in original.items() if v is not None],
                "created": [n for n,v in original.items() if v is None]}), encoding="utf-8")
        for index, (name, data) in enumerate(changes):
            if fail_after is not None and index == fail_after:
                raise OSError("Injected installation failure")
            path = inside(target, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            # Write to sibling staging file then atomically replace one file.
            fd, staged = tempfile.mkstemp(prefix=".vfk-", dir=path.parent)
            try:
                with os.fdopen(fd, "wb") as stream:
                    stream.write(data)
                os.replace(staged, path)
                changed.append(name)
            finally:
                if os.path.exists(staged):
                    os.unlink(staged)
    except BaseException:
        for name in reversed(changed):
            path = inside(target, name)
            if original[name] is None:
                path.unlink()
            else:
                path.write_bytes(original[name])
        print(f"Installation failed; files rolled back. Recovery journal: {journal}", file=sys.stderr)
        raise
    print(f"Installed: {len(changes)} file changes; scope={scope}; target={target}")
    if scope == "global":
        if legacy_aliases:
            print("Recognized legacy Kit paths updated with backups; unrelated files and config.toml preserved.")
        else:
            print("Global AGENTS.md/config.toml preserved. Load vibe-frame-kit/AGENTS.md explicitly in course projects.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=("project", "global"), default="project")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--migrate-legacy", action="store_true",
                        help="Back up and update unchanged original global Kit files; user edits still conflict")
    args = parser.parse_args()
    target = args.project if args.scope == "project" else Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    try:
        install(target, args.scope, args.dry_run, migrate_legacy=args.migrate_legacy)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
