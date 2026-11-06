"""Windows integration tests: reconstruct the original installation, then run both wrappers.
Requires a Git checkout containing the supported original commit, PowerShell and Git Bash.
Never changes HOME or the real global Codex installation; CODEX_HOME targets temporary folders.
"""
import ctypes
from ctypes import wintypes
from functools import cache
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = "eb4ff29cafa8cceba238b9d8f81ebaf660a5b904"

@cache
def originals():
    baseline = json.loads((ROOT / "config/legacy-install-manifest.json").read_text(encoding="utf8"))
    result = {}
    for name, expected in baseline["files"].items():
        data = subprocess.check_output(["git", "show", f"{BASE}:{name}"], cwd=ROOT)
        if hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest() != expected:
            raise AssertionError("Legacy baseline mismatch: " + name)
        result[name] = data
    return result


def fixture(target, crlf=False):
    # Reproduce precisely the original installers' AGENTS + six-directory copy layout.
    # Executing the old installers would target real HOME, so we reconstruct their outputs.
    for name, data in originals().items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if crlf:
            data = data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        path.write_bytes(data)
    for name, data in {"config.toml": b"# user config", "skills/personal/SKILL.md": b"personal rules",
                       "docs/user-notes.md": b"user additions"}.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def snapshot(target):
    return {p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob("*")
            if p.is_file() and "vibe-frame-kit-backups" not in p.relative_to(target).parts}


class LegacyWrappers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.name != "nt":
            raise unittest.SkipTest("PowerShell/Git Bash integration requires Windows")
        cls.powershell = shutil.which("powershell")
        cls.bash = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Git/bin/bash.exe"
        if not cls.powershell or not cls.bash.is_file():
            raise unittest.SkipTest("PowerShell and Git Bash required")
        originals()

    def run_wrapper(self, wrapper, target, migrate=True, dry=False):
        if wrapper == "powershell":
            command = [self.powershell, "-NoProfile", "-File", str(ROOT / "scripts/install.ps1"), "-Scope", "global"]
            if migrate:
                command.append("-MigrateLegacy")
            if dry:
                command.append("-DryRun")
        else:
            command = [str(self.bash), str(ROOT / "scripts/install.sh"), "--scope", "global"]
            if migrate:
                command.append("--migrate-legacy")
            if dry:
                command.append("--dry-run")
        env = dict(os.environ, CODEX_HOME=str(target), PYTHONIOENCODING="utf-8")
        return subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf8", timeout=60)

    def test_original_upgrade_dry_run_backups_and_repeat(self):
        for wrapper in ("powershell", "git-bash"):
            for crlf in (False, True):
                with self.subTest(wrapper=wrapper, crlf=crlf), tempfile.TemporaryDirectory() as directory:
                    target = Path(directory)
                    fixture(target, crlf)
                    before = snapshot(target)
                    blocked = self.run_wrapper(wrapper, target, migrate=False)
                    self.assertNotEqual(blocked.returncode, 0)
                    self.assertEqual(snapshot(target), before)
                    dry = self.run_wrapper(wrapper, target, dry=True)
                    self.assertEqual(dry.returncode, 0, dry.stderr)
                    self.assertEqual(snapshot(target), before)
                    applied = self.run_wrapper(wrapper, target)
                    self.assertEqual(applied.returncode, 0, applied.stderr)
                    self.assertEqual((target / "AGENTS.md").read_bytes(), (ROOT / "AGENTS.md").read_bytes())
                    self.assertEqual((target / "skills/requirements-definition/SKILL.md").read_bytes(),
                                     (ROOT / "skills/requirements-definition/SKILL.md").read_bytes())
                    self.assertEqual((target / "templates/mvp-plan-template.md").read_bytes(),
                                     (ROOT / "templates/mvp-plan-template.md").read_bytes())
                    manifest = json.loads((target / ".vibe-frame-kit-install.json").read_text())
                    self.assertTrue(manifest["legacy_aliases"])
                    for name, data in before.items():
                        if name not in manifest["files"]:
                            self.assertEqual((target / name).read_bytes(), data)
                        elif (target / name).read_bytes() != data:
                            copies = list((target / "vibe-frame-kit-backups").glob("install-*/" + name))
                            self.assertEqual(len(copies), 1, name)
                            self.assertEqual(copies[0].read_bytes(), data)
                    after = snapshot(target)
                    repeat = self.run_wrapper(wrapper, target, migrate=False)
                    self.assertEqual(repeat.returncode, 0, repeat.stderr)
                    self.assertIn("Installed: 0 file changes", repeat.stdout)
                    self.assertEqual(snapshot(target), after)
                    checker = subprocess.run([shutil.which("python"), "scripts/check-environment.py"],
                                             cwd=target / "vibe-frame-kit", capture_output=True, timeout=20)
                    self.assertEqual(checker.returncode, 0, checker.stderr)

    def test_modified_files_and_new_path_collisions_preserved(self):
        for wrapper in ("powershell", "git-bash"):
            for name in ("skills/requirements-definition/SKILL.md", "AGENTS.md", "docs/course-workflow.md"):
                with self.subTest(wrapper=wrapper, conflict=name), tempfile.TemporaryDirectory() as directory:
                    target = Path(directory)
                    fixture(target)
                    (target / name).write_bytes(b"user edited or added content")
                    before = snapshot(target)
                    result = self.run_wrapper(wrapper, target)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("Conflict; existing file preserved", result.stderr)
                    self.assertEqual(snapshot(target), before)
                    self.assertFalse((target / "vibe-frame-kit-backups").exists())

    def test_modified_managed_file_after_migration_preserved(self):
        for wrapper in ("powershell", "git-bash"):
            with self.subTest(wrapper=wrapper), tempfile.TemporaryDirectory() as directory:
                target = Path(directory)
                fixture(target)
                self.assertEqual(self.run_wrapper(wrapper, target).returncode, 0)
                (target / "templates/mvp-plan-template.md").write_bytes(b"later user edit")
                before = snapshot(target)
                result = self.run_wrapper(wrapper, target, migrate=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(snapshot(target), before)

    def test_failure_rolls_back_and_can_retry(self):
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.CreateFileW.argtypes = (wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
                                     wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE)
        kernel.CreateFileW.restype = wintypes.HANDLE
        kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
        kernel.CloseHandle.restype = wintypes.BOOL
        for wrapper in ("powershell", "git-bash"):
            with self.subTest(wrapper=wrapper), tempfile.TemporaryDirectory() as directory:
                target = Path(directory)
                fixture(target)
                before = snapshot(target)
                # Read sharing permits preflight and backups, but prevents replacement late in the transaction.
                handle = kernel.CreateFileW(str(target / "AGENTS.md"), 0x80000000, 1, None, 3, 0x80, None)
                self.assertNotEqual(handle, ctypes.c_void_p(-1).value)
                try:
                    failed = self.run_wrapper(wrapper, target)
                    self.assertNotEqual(failed.returncode, 0)
                    self.assertIn("files rolled back", failed.stderr)
                    self.assertEqual(snapshot(target), before)
                    self.assertFalse((target / ".vibe-frame-kit-install.json").exists())
                    self.assertTrue(list((target / "vibe-frame-kit-backups").glob("install-*/recovery.json")))
                finally:
                    kernel.CloseHandle(handle)
                retried = self.run_wrapper(wrapper, target)
                self.assertEqual(retried.returncode, 0, retried.stderr)
                self.assertTrue((target / ".vibe-frame-kit-install.json").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
