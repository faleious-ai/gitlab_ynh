from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts" / "maestro_program.py"


class AutonomousProgramFixture(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.work = Path(self.tempdir.name)
        self.coordinator = self.work / "coordinator"
        self.runner = self.work / "runner"
        self._init_repo(self.coordinator)
        self._init_repo(self.runner)
        (self.coordinator / "tests" / "acceptance").mkdir(parents=True)
        (self.coordinator / "tests" / "acceptance" / "oracle.py").write_text("ORACLE = 1\n", encoding="utf-8")
        (self.coordinator / "src").mkdir()
        (self.coordinator / "src" / "base.py").write_text("BASE = 1\n", encoding="utf-8")
        (self.runner / "src").mkdir()
        (self.runner / "src" / "runner.py").write_text("RUNNER = 1\n", encoding="utf-8")
        self._commit_and_push(self.coordinator, "baseline coordinator")
        self._commit_and_push(self.runner, "baseline runner")
        self.mandate = self._mandate()
        self.backlog = self._backlog()
        self.state = self._state()
        self.findings = {"schema_version": 2, "program_id": "test-program", "findings": []}
        self._write_program()

    def _git(self, repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True, check=False)
        if check and completed.returncode != 0:
            self.fail(completed.stderr or completed.stdout)
        return completed

    def _init_repo(self, repo: Path) -> None:
        repo.mkdir(parents=True)
        remote = repo.with_name(repo.name + "-remote.git")
        subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
        self._git(repo, "init", "-b", "master")
        self._git(repo, "config", "user.email", "acceptance@example.invalid")
        self._git(repo, "config", "user.name", "Acceptance")
        self._git(repo, "remote", "add", "origin", str(remote))

    def _commit_and_push(self, repo: Path, subject: str) -> str:
        self._git(repo, "add", "-A")
        self._git(repo, "commit", "--allow-empty", "-m", subject)
        self._git(repo, "push", "-u", "origin", "master")
        return self._git(repo, "rev-parse", "HEAD").stdout.strip()

    def _mandate(self) -> dict:
        protected = self.coordinator / "tests" / "acceptance" / "oracle.py"
        return {
            "schema_version": 2,
            "program_id": "test-program",
            "mission": "finish all authorized technical work",
            "required_objectives": ["T1", "T2"],
            "required_work_packages": ["WP-00", "WP-01"],
            "repositories": [
                {"id": "coordinator", "relative_path": ".", "remote_ref": "origin/master"},
                {"id": "runner", "relative_path": "../runner", "remote_ref": "origin/master"},
            ],
            "protected_paths": {
                "exact": ["continuity/PROGRAM_MANDATE.json"],
                "prefixes": ["tests/acceptance"],
                "inventory": {
                    "tests/acceptance/oracle.py": hashlib.sha256(protected.read_bytes()).hexdigest(),
                },
            },
            "human_gate_classes": [
                "credential_required",
                "external_authorization",
                "financial_cost",
                "legal_or_ethical_decision",
                "product_consequence",
                "irreversible_operation",
                "destructive_production_action",
            ],
            "unsafe_operation_classes": ["release", "deploy", "promotion", "destructive", "irreversible"],
        }

    def _backlog(self) -> dict:
        return {
            "schema_version": 2,
            "program_id": "test-program",
            "objectives": {"T1": ["WP-00"], "T2": ["WP-01"]},
            "work_packages": [
                {"id": "WP-00", "title": "Foundation"},
                {"id": "WP-01", "title": "Delivery"},
            ],
            "tasks": [
                {
                    "id": "T-BASE",
                    "work_package": "WP-00",
                    "repositories": ["coordinator"],
                    "dependencies": [],
                    "reversible": True,
                    "operation_class": "implementation",
                    "paths": ["src/base.py", "evidence/base/"],
                    "priority": 100,
                    "auto_activate": False,
                },
                {
                    "id": "T-NEXT",
                    "work_package": "WP-01",
                    "repositories": ["runner"],
                    "dependencies": ["T-BASE"],
                    "reversible": True,
                    "operation_class": "implementation",
                    "paths": ["src/runner.py", "evidence/next/"],
                    "priority": 90,
                    "auto_activate": True,
                },
            ],
        }

    def _state(self) -> dict:
        return {
            "schema_version": 2,
            "program_id": "test-program",
            "round_id": "RND-TEST-001",
            "baseline_heads": {
                "coordinator": self._git(self.coordinator, "rev-parse", "HEAD").stdout.strip(),
                "runner": self._git(self.runner, "rev-parse", "HEAD").stdout.strip(),
            },
            "task_overrides": {
                "T-BASE": {
                    "state": "accepted",
                    "review": "ORCHESTRATOR",
                    "commit": self._git(self.coordinator, "rev-parse", "HEAD").stdout.strip(),
                }
            },
            "human_gates": [],
            "environment_blocks": [],
            "history": [],
        }

    def _write(self, relative: str, payload: dict) -> Path:
        path = self.coordinator / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def _write_program(self) -> None:
        self._write("continuity/PROGRAM_MANDATE.json", self.mandate)
        self._write("continuity/PROGRAM_BACKLOG.json", self.backlog)
        self._write("continuity/PROGRAM_STATE.json", self.state)
        self._write("continuity/PROGRAM_FINDINGS.json", self.findings)

    def _run(self, *args: str, expected: int = 0) -> dict:
        completed = subprocess.run(
            [sys.executable, str(CLI), *args], cwd=ROOT, text=True, capture_output=True, check=False
        )
        self.assertEqual(completed.returncode, expected, completed.stderr or completed.stdout)
        try:
            return json.loads(completed.stdout)
        except json.JSONDecodeError as error:
            self.fail(f"CLI did not emit JSON: {error}: {completed.stdout!r}")

    def _program_args(self) -> list[str]:
        return [
            "--root",
            str(self.coordinator),
            "--repo",
            f"coordinator={self.coordinator}",
            "--repo",
            f"runner={self.runner}",
        ]
