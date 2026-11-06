"""Offline regression checks. Optional API dependencies and real Codex discovery are explicit."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import install

class KitChecks(unittest.TestCase):
    def test_metadata_and_contracts(self):
        skills = list((ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 10)
        for p in skills:
            text = p.read_text(encoding="utf8")
            header = text.split("---", 2)[1]
            self.assertIn("name: " + p.parent.name, header)
            self.assertRegex(header, r"description: .+")
            self.assertRegex(p.parent.name, r"^[a-z0-9-]{1,64}$")
            refs = re.findall(r"templates/([a-z-]+\.md)", text)
            self.assertTrue(refs)
            for ref in refs:
                self.assertTrue((ROOT / "templates" / ref).is_file(), ref)
        self.assertNotIn("google-generativeai", (ROOT / "skills/project-structure-builder/SKILL.md").read_text(encoding="utf8"))

    def test_local_markdown_links(self):
        for p in ROOT.rglob("*.md"):
            if ".git" in p.parts:
                continue
            for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", p.read_text(encoding="utf8")):
                if "://" in link or link.startswith("#"):
                    continue
                self.assertTrue((p.parent / link.split("#")[0]).exists(), f"{p}: {link}")

    def test_project_install_repeat_conflict_and_dry_run(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "project"
            install.install(target, "project", dry_run=True)
            self.assertFalse(target.exists())
            install.install(target, "project")
            self.assertEqual(len(list((target / ".agents/skills").glob("*/SKILL.md"))), 10)
            before = {p.relative_to(target): p.read_bytes() for p in target.rglob("*") if p.is_file()}
            install.install(target, "project")
            after = {p.relative_to(target): p.read_bytes() for p in target.rglob("*") if p.is_file()}
            self.assertEqual(before, after)
            (target / "AGENTS.md").write_text("user rules", encoding="utf8")
            with self.assertRaisesRegex(ValueError, "Conflict"):
                install.install(target, "project")
            self.assertEqual((target / "AGENTS.md").read_text(), "user rules")

    def test_existing_configuration_and_other_skills_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "AGENTS.md").write_text("existing rules")
            (target / "config.toml").write_text("# existing settings")
            other = target / "skills/other/SKILL.md"
            other.parent.mkdir(parents=True)
            other.write_text("other skill")
            install.install(target, "global")
            self.assertEqual((target / "AGENTS.md").read_text(), "existing rules")
            self.assertEqual((target / "config.toml").read_text(), "# existing settings")
            self.assertEqual(other.read_text(), "other skill")

    def test_installed_environment_checker_runs_without_source(self):
        for scope in ("project", "global"):
            with self.subTest(scope=scope), tempfile.TemporaryDirectory() as directory:
                target = Path(directory)
                install.install(target, scope)
                package_root = target if scope == "project" else target / "vibe-frame-kit"
                checker = package_root / "scripts/check-environment.py"
                manifest = json.loads((target / ".vibe-frame-kit-install.json").read_text())
                self.assertIn(checker.relative_to(target).as_posix(), manifest["files"])
                process = subprocess.run([sys.executable, "scripts/check-environment.py"],
                                         cwd=package_root, capture_output=True, text=True, timeout=20)
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertIn("Python:", process.stdout)
                self.assertIn("instructor decision required", process.stdout)

    def test_codex_home_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            env = dict(os.environ, CODEX_HOME=directory)
            process = subprocess.run([sys.executable, str(ROOT / "scripts/install.py"), "--scope", "global"], env=env, capture_output=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertTrue((Path(directory) / "skills/requirements-definition/SKILL.md").is_file())

    def test_late_conflict_prevents_all_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            conflict = target / "templates/test-scenario-template.md"
            conflict.parent.mkdir()
            conflict.write_text("user-owned template")
            with self.assertRaisesRegex(ValueError, "Conflict"):
                install.install(target, "project")
            self.assertEqual(conflict.read_text(), "user-owned template")
            self.assertFalse((target / "AGENTS.md").exists())
            self.assertFalse((target / ".agents").exists())
            self.assertFalse((target / ".vibe-frame-kit-install.json").exists())

    def test_successful_managed_upgrade(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            install.install(target, "project")
            path = target / "AGENTS.md"
            path.write_bytes(b"old managed version")
            manifest_path = target / ".vibe-frame-kit-install.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["files"]["AGENTS.md"] = install.digest(path.read_bytes())
            manifest_path.write_text(json.dumps(manifest))
            install.install(target, "project")
            self.assertEqual(path.read_bytes(), (ROOT / "AGENTS.md").read_bytes())
            backups = list((target / ".vibe-frame-kit-backups").glob("install-*/AGENTS.md"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), b"old managed version")

    def test_failure_rolls_back(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            install.install(target, "project")
            # A valid prior version may be updated; inject a mid-write failure.
            manifest_path = target / ".vibe-frame-kit-install.json"
            manifest = json.loads(manifest_path.read_text())
            for name in ("AGENTS.md", "templates/mvp-plan-template.md"):
                (target / name).write_bytes(b"previous version")
                manifest["files"][name] = install.digest(b"previous version")
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaises(OSError):
                install.install(target, "project", fail_after=1)
            self.assertEqual((target / "AGENTS.md").read_bytes(), b"previous version")
            self.assertEqual((target / "templates/mvp-plan-template.md").read_bytes(), b"previous version")
            self.assertEqual(json.loads(manifest_path.read_text()), manifest)

    def test_missing_source_no_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            original = install.SOURCE
            try:
                install.SOURCE = Path(directory) / "missing"
                target = Path(directory) / "target"
                with self.assertRaises(ValueError):
                    install.install(target, "project")
                self.assertFalse(target.exists())
            finally:
                install.SOURCE = original


def load_example(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "examples/meeting-summary" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class ApiChecks(unittest.TestCase):
    def test_api_contract(self):
        from fastapi.testclient import TestClient
        api = load_example("api")
        with TestClient(api.create_app()) as client:
            response = client.post("/api/summarize", json={"text": "  sample  "})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["summary"], "sample")
            self.assertEqual(set(response.json()), {"summary", "action_items", "message"})
            for data in ({}, {"text": ""}, {"text": " \t\n"}, {"text": 3}, {"text": None}):
                response = client.post("/api/summarize", json=data)
                self.assertEqual(response.status_code, 422)
                self.assertIsInstance(response.json()["detail"], list)

    def test_provider_failures_are_502(self):
        from fastapi.testclient import TestClient
        api = load_example("api")
        for error_type in (TimeoutError, ConnectionError, api.ProviderError):
            with self.subTest(error=error_type.__name__):
                def failing(text):
                    raise error_type("private provider data")
                with TestClient(api.create_app(failing)) as client:
                    response = client.post("/api/summarize", json={"text": "sample"})
                    self.assertEqual(response.status_code, 502)
                    self.assertEqual(response.json(), {"detail": "Summary provider unavailable"})
                    self.assertNotIn("private", response.text)

        with self.subTest(error="malformed provider response"):
            with TestClient(api.create_app(lambda text: {"unexpected": "private response data"})) as client:
                response = client.post("/api/summarize", json={"text": "sample"})
                self.assertEqual(response.status_code, 502)
                self.assertEqual(response.json(), {"detail": "Summary provider unavailable"})
                self.assertNotIn("private", response.text)

    def test_internal_bug_remains_500(self):
        from fastapi.testclient import TestClient
        api = load_example("api")
        def broken(text):
            raise RuntimeError("private internal data")
        with TestClient(api.create_app(broken), raise_server_exceptions=False) as client:
            response = client.post("/api/summarize", json={"text": "sample"})
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.text, "Internal Server Error")
            self.assertNotIn("private", response.text)

    def test_documented_schema_matches_executable(self):
        api = load_example("api")
        text = (ROOT / "skills/api-service-builder/SKILL.md").read_text(encoding="utf8")
        blocks = re.findall(r"```python\n(.*?)```", text, re.S)
        self.assertEqual(len(blocks), 2)
        for block in blocks:
            namespace = {}
            exec(block, namespace)
            self.assertEqual(namespace["SummarizeRequest"].model_json_schema(), api.SummarizeRequest.model_json_schema())

    def test_retry_limit_and_action_ledger(self):
        workflow = load_example("workflow")
        calls = []
        def generate():
            calls.append(1)
            return "bad"
        self.assertEqual(workflow.generate_with_limit(generate, lambda value: False)["status"], "failed")
        self.assertEqual(len(calls), 2)
        self.assertEqual(workflow.generate_with_limit(lambda: "ok", lambda value: True)["attempt"], 1)
        ledger = {}
        def action():
            calls.append(1)
            return "mock-id"
        for _ in range(2):
            self.assertEqual(workflow.run_action_once(ledger, "same", action)["status"], "succeeded")
        self.assertEqual(len(calls), 3)
        def uncertain():
            raise TimeoutError()
        self.assertEqual(workflow.run_action_once(ledger, "unknown", uncertain)["status"], "unknown")
        self.assertEqual(workflow.run_action_once(ledger, "unknown", action)["status"], "unknown")
        self.assertEqual(len(calls), 3)


def codex_discovery():
    """Use the installed client's skills/list RPC, without creating a thread or model turn."""
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "project"
        codex_home = Path(directory) / "codex-home"
        codex_home.mkdir()
        install.install(project, "project")
        env = dict(os.environ, CODEX_HOME=str(codex_home))
        process = subprocess.Popen([shutil.which("codex"), "app-server", "--stdio"],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                   text=True, encoding="utf8", env=env, cwd=project)
        messages = queue.Queue()
        def read():
            for line in process.stdout:
                try:
                    messages.put(json.loads(line))
                except ValueError:
                    pass
        threading.Thread(target=read, daemon=True).start()
        def send(value):
            process.stdin.write(json.dumps(value) + "\n")
            process.stdin.flush()
        def receive(identifier):
            import time
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                value = messages.get(timeout=max(0.1, deadline-time.monotonic()))
                if value.get("id") == identifier:
                    if "error" in value:
                        raise RuntimeError(str(value["error"]))
                    return value["result"]
            raise TimeoutError("Codex app-server response")
        try:
            send({"id": 1, "method": "initialize", "params": {"clientInfo": {"name": "vibe-frame-kit-check", "version": "1.0"}}})
            receive(1)
            send({"method": "initialized"})
            send({"id": 2, "method": "skills/list", "params": {"cwds": [str(project)], "forceReload": True}})
            result = receive(2)
            entries = result["data"]
            expected = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
            found = {skill["name"] for entry in entries for skill in entry["skills"] if skill["name"] in expected and skill.get("enabled", True) and Path(skill["path"]).is_relative_to(project)}
            all_errors = [error for entry in entries for error in entry.get("errors", [])]
            errors = [error for error in all_errors if Path(error["path"]).is_relative_to(project)]
            if len(all_errors) > len(errors):
                print("WARNING unrelated existing skill errors:", len(all_errors)-len(errors))
            if found != expected or errors:
                raise AssertionError({"missing": sorted(expected-found), "errors": errors})
            print("PASS actual Codex skills/list:", ", ".join(sorted(found)))
        finally:
            process.terminate()
            process.wait(timeout=10)
            process.stdin.close()
            process.stdout.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api", action="store_true", help="Requires FastAPI, Pydantic v2 and httpx")
    parser.add_argument("--codex-discovery", action="store_true", help="Requires installed Codex CLI; no model calls")
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(KitChecks)
    if args.api:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ApiChecks))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
    if args.codex_discovery:
        codex_discovery()
