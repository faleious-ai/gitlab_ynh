from __future__ import annotations

from tests.acceptance.autonomous_program_fixture import *


class AutonomousProgramExecutionCoreTests(AutonomousProgramFixture):
    def test_backlog_not_derived_queue_is_authoritative_and_prevents_false_stop(self) -> None:
        stale_queue = {
            "schema_version": 2,
            "program_id": "test-program",
            "derived": True,
            "source_hashes": {},
            "eligible_tasks": [],
            "stop_allowed": True,
        }
        self._write("continuity/PROGRAM_QUEUE.json", stale_queue)
        result = self._run("plan", *self._program_args(), expected=2)
        self.assertFalse(result["valid"])
        self.assertFalse(result["stop_allowed"])
        self.assertIn("DERIVED_QUEUE_STALE", result["validation_reasons"])
        self.assertIn("T-NEXT", result["eligible_tasks"])

        refreshed = self._run("refresh-queue", *self._program_args())
        self.assertEqual(refreshed["eligible_tasks"], ["T-NEXT"])
        self.assertFalse(refreshed["stop_allowed"])
        doctor = self._run("doctor", *self._program_args())
        self.assertTrue(doctor["valid"])

    def test_open_finding_without_finished_correction_never_allows_stop(self) -> None:
        self.backlog["tasks"].append(
            {
                "id": "T-CORRECTION",
                "work_package": "WP-01",
                "repositories": ["coordinator"],
                "dependencies": [],
                "reversible": True,
                "operation_class": "correction",
                "paths": ["src/correction.py", "evidence/correction/"],
                "priority": 200,
                "auto_activate": False,
            }
        )
        self.state["task_overrides"].update(
            {
                "T-NEXT": {
                    "state": "accepted",
                    "review": "ORCHESTRATOR",
                    "commit": self._git(self.runner, "rev-parse", "HEAD").stdout.strip(),
                },
                "T-CORRECTION": {"state": "blocked_environment"},
            }
        )
        self.state["environment_blocks"] = [
            {
                "task_id": "T-CORRECTION",
                "state": "open",
                "condition": "controlled environment unavailable",
                "evidence": ["environment probe"],
                "fallbacks_attempted": ["local fixture", "remote CI"],
                "safe_state": "no mutation",
                "resume": "run in controlled environment",
            }
        ]
        self.findings["findings"] = [
            {
                "id": "F-001",
                "severity": "P1",
                "state": "open",
                "actionable": True,
                "summary": "known failing contract",
                "correction_task_id": "T-CORRECTION",
            }
        ]
        self._write_program()
        result = self._run("plan", *self._program_args())
        self.assertFalse(result["stop_allowed"])
        self.assertFalse(result["checkpoint_allowed"])
        self.assertEqual(result["stop_reason"], "OPEN_ACTIONABLE_FINDINGS")

    def test_actual_git_diff_protects_oracles_without_caller_supplied_paths(self) -> None:
        base = self._git(self.coordinator, "rev-parse", "HEAD").stdout.strip()
        oracle = self.coordinator / "tests" / "acceptance" / "oracle.py"
        oracle.write_text("ORACLE = 2\n", encoding="utf-8")
        result = self._run(
            "validate-change",
            "--root",
            str(self.coordinator),
            "--repo-root",
            str(self.coordinator),
            "--base",
            base,
            expected=2,
        )
        self.assertFalse(result["valid"])
        self.assertIn("tests/acceptance/oracle.py", {item["path"] for item in result["protected_violations"]})

    def test_protected_prefix_detects_rename_and_untracked_addition(self) -> None:
        base = self._git(self.coordinator, "rev-parse", "HEAD").stdout.strip()
        source = self.coordinator / "tests" / "acceptance" / "oracle.py"
        renamed = self.coordinator / "tests" / "acceptance" / "renamed.py"
        source.rename(renamed)
        (self.coordinator / "tests" / "acceptance" / "new_oracle.py").write_text("NEW = 1\n", encoding="utf-8")
        result = self._run(
            "validate-change",
            "--root",
            str(self.coordinator),
            "--repo-root",
            str(self.coordinator),
            "--base",
            base,
            expected=2,
        )
        violated = {item["path"] for item in result["protected_violations"]}
        self.assertIn("tests/acceptance/oracle.py", violated)
        self.assertIn("tests/acceptance/renamed.py", violated)
        self.assertIn("tests/acceptance/new_oracle.py", violated)

    def test_prefix_aware_ownership_prevents_fake_parallelism(self) -> None:
        self.backlog["tasks"] = [
            {
                "id": "T-LEFT",
                "work_package": "WP-00",
                "repositories": ["coordinator"],
                "dependencies": [],
                "reversible": True,
                "operation_class": "research",
                "paths": ["evidence/"],
                "priority": 10,
                "auto_activate": True,
            },
            {
                "id": "T-RIGHT",
                "work_package": "WP-01",
                "repositories": ["coordinator"],
                "dependencies": [],
                "reversible": True,
                "operation_class": "research",
                "paths": ["evidence/mcp/"],
                "priority": 9,
                "auto_activate": True,
            },
        ]
        self.state["task_overrides"] = {}
        self._write_program()
        result = self._run("plan", *self._program_args())
        self.assertEqual(set(result["eligible_tasks"]), {"T-LEFT", "T-RIGHT"})
        self.assertFalse(result["parallelism_required"])
