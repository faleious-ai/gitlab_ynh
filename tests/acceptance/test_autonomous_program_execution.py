from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts" / "maestro_program.py"
PROTECTED = [
    "docs/specifications/AUTONOMOUS_PROGRAM_EXECUTION_SPEC.md",
    "tests/acceptance/test_autonomous_program_execution.py",
]


class AutonomousProgramExecutionAcceptanceTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.work = Path(self.tempdir.name)
        self.mandate = self._write(
            "mandate.json",
            {
                "mission": "complete all authorized technical work until a real human dependency",
                "protected_paths": PROTECTED,
                "human_gate_classes": [
                    "credential_required",
                    "external_authorization",
                    "financial_cost",
                    "legal_or_ethical_decision",
                    "product_consequence",
                    "irreversible_operation",
                    "destructive_production_action",
                ],
                "review": {
                    "machine_green_allows_reversible_dependents": True,
                    "orchestrator_acceptance_required_for": [
                        "release",
                        "deploy",
                        "promotion",
                        "destructive",
                        "irreversible",
                        "production_credential",
                    ],
                },
                "parallelism": {
                    "minimum_lanes_when_independent": 2,
                    "preparation": "parallel_isolated",
                    "integration": "serial",
                    "overlap_evidence_required": True,
                },
            },
        )
        self.queue = self._write(
            "queue.json",
            {
                "tasks": [
                    {
                        "id": "T-BASE-GREEN",
                        "work_package": "WP-BASE",
                        "status": "machine_green_awaiting_review",
                        "dependencies": [],
                        "reversible": True,
                        "operation_class": "implementation",
                        "paths": ["src/base.py"],
                        "priority": 20,
                    },
                    {
                        "id": "T-CORRECT-ALPINE",
                        "work_package": "WP-RUNNER",
                        "status": "ready",
                        "dependencies": [],
                        "reversible": True,
                        "operation_class": "correction",
                        "paths": ["manifest.toml", "config_panel.toml"],
                        "priority": 100,
                    },
                    {
                        "id": "T-GITLAB-RESEARCH",
                        "work_package": "WP-GITLAB",
                        "status": "ready",
                        "dependencies": ["T-BASE-GREEN"],
                        "reversible": True,
                        "operation_class": "research",
                        "paths": ["docs/research/gitlab.md"],
                        "priority": 40,
                    },
                    {
                        "id": "T-MCP-HARNESS",
                        "work_package": "WP-MCP",
                        "status": "ready",
                        "dependencies": [],
                        "reversible": True,
                        "operation_class": "test_harness",
                        "paths": ["tests/acceptance/mcp.py"],
                        "priority": 30,
                    },
                    {
                        "id": "T-LIVE-TRUST",
                        "work_package": "WP-RUNNER",
                        "status": "blocked_environment",
                        "dependencies": [],
                        "reversible": True,
                        "operation_class": "observation",
                        "paths": ["evidence/live.json"],
                        "priority": 90,
                    },
                    {
                        "id": "T-RELEASE",
                        "work_package": "WP-RUNNER",
                        "status": "ready",
                        "dependencies": ["T-BASE-GREEN"],
                        "reversible": False,
                        "operation_class": "release",
                        "requires_orchestrator_acceptance": True,
                        "paths": ["manifest.toml"],
                        "priority": 10,
                    },
                ]
            },
        )
        self.state = self._write(
            "state.json",
            {
                "reviews": [{"task_id": "T-BASE-GREEN", "state": "awaiting_orchestrator"}],
                "blocks": [{"task_id": "T-LIVE-TRUST", "class": "network_unavailable"}],
            },
        )

    def _write(self, name: str, payload: dict) -> Path:
        path = self.work / name
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    def _run(self, *args: str, expected: int = 0) -> dict:
        self.assertTrue(CLI.is_file(), "RED: scripts/maestro_program.py is not implemented")
        completed = subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, expected, completed.stderr or completed.stdout)
        try:
            return json.loads(completed.stdout)
        except json.JSONDecodeError as error:
            self.fail(f"CLI must emit JSON: {error}: {completed.stdout!r}")

    def _plan(self) -> dict:
        return self._run(
            "plan",
            "--mandate",
            str(self.mandate),
            "--queue",
            str(self.queue),
            "--state",
            str(self.state),
        )

    def test_continues_across_work_packages_without_waiting_for_review(self) -> None:
        plan = self._plan()
        eligible = set(plan["eligible_tasks"])
        self.assertEqual(
            eligible,
            {"T-CORRECT-ALPINE", "T-GITLAB-RESEARCH", "T-MCP-HARNESS"},
        )
        self.assertNotIn("T-RELEASE", eligible)
        self.assertFalse(plan["stop_allowed"])
        self.assertEqual(plan["integration_order"][0], "T-CORRECT-ALPINE")

    def test_environment_block_does_not_stop_independent_work(self) -> None:
        plan = self._plan()
        blocked = {item["task_id"]: item["reason"] for item in plan["blocked_tasks"]}
        self.assertIn("T-LIVE-TRUST", blocked)
        self.assertGreaterEqual(len(plan["eligible_tasks"]), 2)
        self.assertFalse(plan["stop_allowed"])

    def test_parallel_preparation_is_required_but_commits_remain_serial(self) -> None:
        plan = self._plan()
        self.assertTrue(plan["parallelism_required"])
        self.assertGreaterEqual(len(plan["lanes"]), 2)
        self.assertEqual(plan["commit_mode"], "serial")
        assigned = {task for lane in plan["lanes"] for task in lane["task_ids"]}
        self.assertEqual(assigned, set(plan["eligible_tasks"]))

    def test_parallel_wave_requires_overlap_evidence(self) -> None:
        plan = self._plan()
        plan_path = self._write("plan.json", plan)
        lane_ids = [lane["lane_id"] for lane in plan["lanes"][:2]]
        sequential = self._write(
            "sequential.json",
            {
                "lanes": [
                    {"lane_id": lane_ids[0], "started_at": "2026-07-17T10:00:00Z", "finished_at": "2026-07-17T10:10:00Z"},
                    {"lane_id": lane_ids[1], "started_at": "2026-07-17T10:11:00Z", "finished_at": "2026-07-17T10:20:00Z"},
                ]
            },
        )
        rejected = self._run(
            "validate-wave",
            "--plan",
            str(plan_path),
            "--evidence",
            str(sequential),
            expected=2,
        )
        self.assertFalse(rejected["valid"])
        self.assertIn("PARALLELISM_NOT_DEMONSTRATED", rejected["reasons"])

        overlapping = self._write(
            "overlapping.json",
            {
                "lanes": [
                    {"lane_id": lane_ids[0], "started_at": "2026-07-17T10:00:00Z", "finished_at": "2026-07-17T10:12:00Z"},
                    {"lane_id": lane_ids[1], "started_at": "2026-07-17T10:02:00Z", "finished_at": "2026-07-17T10:20:00Z"},
                ]
            },
        )
        accepted = self._run(
            "validate-wave",
            "--plan",
            str(plan_path),
            "--evidence",
            str(overlapping),
        )
        self.assertTrue(accepted["valid"])

    def test_rejects_fake_human_gate_while_independent_work_exists(self) -> None:
        gate = self._write(
            "invalid-gate.json",
            {
                "reason_class": "tool_unavailable",
                "blocked_task": "T-LIVE-TRUST",
                "requested_human_action": "choose another technical tool",
                "fallbacks_attempted": ["preferred endpoint"],
            },
        )
        result = self._run(
            "validate-gate",
            "--mandate",
            str(self.mandate),
            "--queue",
            str(self.queue),
            "--state",
            str(self.state),
            "--gate",
            str(gate),
            expected=2,
        )
        self.assertFalse(result["valid"])
        self.assertIn("INVALID_HUMAN_GATE_CLASS", result["reasons"])
        self.assertIn("INDEPENDENT_WORK_REMAINS", result["reasons"])

    def test_accepts_real_human_gate_only_after_all_independent_work_is_exhausted(self) -> None:
        queue = self._write(
            "human-only-queue.json",
            {
                "tasks": [
                    {
                        "id": "T-PROD-CREDENTIAL",
                        "status": "blocked_human",
                        "dependencies": [],
                        "reversible": False,
                        "operation_class": "production_credential",
                        "paths": [],
                    }
                ]
            },
        )
        state = self._write("human-only-state.json", {"reviews": [], "blocks": []})
        gate = self._write(
            "valid-gate.json",
            {
                "reason_class": "credential_required",
                "blocked_task": "T-PROD-CREDENTIAL",
                "external_authority": True,
                "condition": "production credential is not available to the executor",
                "evidence": ["credential store contains no authorized value"],
                "fallbacks_attempted": ["completed all work that does not require the credential"],
                "requested_human_action": "provide or decline the credential",
                "safe_state": "no production mutation performed",
                "resume": "validate credential and continue the blocked task",
            },
        )
        result = self._run(
            "validate-gate",
            "--mandate",
            str(self.mandate),
            "--queue",
            str(queue),
            "--state",
            str(state),
            "--gate",
            str(gate),
        )
        self.assertTrue(result["valid"])
        self.assertTrue(result["stop_allowed"])

    def test_executor_cannot_modify_orchestrator_owned_oracles(self) -> None:
        result = self._run(
            "validate-change",
            "--mandate",
            str(self.mandate),
            "--actor",
            "executor",
            "--paths",
            *PROTECTED,
            expected=2,
        )
        self.assertFalse(result["valid"])
        self.assertEqual(set(result["protected_paths"]), set(PROTECTED))


if __name__ == "__main__":
    unittest.main()
