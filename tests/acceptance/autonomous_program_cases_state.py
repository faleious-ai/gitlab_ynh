from __future__ import annotations

from tests.acceptance.autonomous_program_fixture import *


class AutonomousProgramExecutionStateTests(AutonomousProgramFixture):
    def test_parallelism_requires_distinct_workers_workspaces_overlap_and_hashed_outputs(self) -> None:
        plan = {
            "parallelism_required": True,
            "lanes": [
                {"lane_id": "LANE-A", "task_ids": ["T-A"], "paths": ["src/a/"], "baseline_heads": {"coordinator": "abc"}},
                {"lane_id": "LANE-B", "task_ids": ["T-B"], "paths": ["src/b/"], "baseline_heads": {"coordinator": "abc"}},
            ],
        }
        plan_path = self.work / "plan.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        journal = self.work / "lanes.jsonl"
        workspace_a = self.work / "worker-a"
        workspace_b = self.work / "worker-b"
        workspace_a.mkdir()
        workspace_b.mkdir()
        self._run("lane-start", "--journal", str(journal), "--task-id", "T-A", "--lane-id", "LANE-A", "--worker-id", "worker-a", "--workspace", str(workspace_a), "--baseline", "abc", "--path", "src/a/")
        self._run("lane-start", "--journal", str(journal), "--task-id", "T-B", "--lane-id", "LANE-B", "--worker-id", "worker-b", "--workspace", str(workspace_b), "--baseline", "abc", "--path", "src/b/")
        artifact_a = workspace_a / "a.patch"
        artifact_b = workspace_b / "b.patch"
        log_a = workspace_a / "a.log"
        log_b = workspace_b / "b.log"
        artifact_a.write_text("patch-a", encoding="utf-8")
        artifact_b.write_text("patch-b", encoding="utf-8")
        log_a.write_text("command-a", encoding="utf-8")
        log_b.write_text("command-b", encoding="utf-8")
        time.sleep(0.02)
        self._run("lane-finish", "--journal", str(journal), "--lane-id", "LANE-A", "--worker-id", "worker-a", "--artifact", str(artifact_a), "--log", str(log_a), "--result", "ready")
        self._run("lane-finish", "--journal", str(journal), "--lane-id", "LANE-B", "--worker-id", "worker-b", "--artifact", str(artifact_b), "--log", str(log_b), "--result", "ready")
        valid = self._run("validate-wave", "--plan", str(plan_path), "--journal", str(journal))
        self.assertTrue(valid["parallelism_demonstrated"])
        artifact_b.write_text("tampered", encoding="utf-8")
        invalid = self._run("validate-wave", "--plan", str(plan_path), "--journal", str(journal), expected=2)
        self.assertIn("LANE_ARTIFACT_HASH_INVALID:LANE-B", invalid["reasons"])

    def test_lane_finish_requires_artifact_inside_isolated_workspace(self) -> None:
        journal = self.work / "lanes.jsonl"
        workspace = self.work / "worker"
        workspace.mkdir()
        log = workspace / "commands.log"
        log.write_text("command", encoding="utf-8")
        outside = self.work / "outside.patch"
        outside.write_text("patch", encoding="utf-8")
        self._run("lane-start", "--journal", str(journal), "--task-id", "T-A", "--lane-id", "LANE-A", "--worker-id", "worker-a", "--workspace", str(workspace), "--baseline", "abc", "--path", "src/a/")
        missing = self._run("lane-finish", "--journal", str(journal), "--lane-id", "LANE-A", "--worker-id", "worker-a", "--log", str(log), "--result", "ready", expected=2)
        self.assertIn("LANE_ARTIFACT_REQUIRED", missing["reasons"])
        outside_result = self._run("lane-finish", "--journal", str(journal), "--lane-id", "LANE-A", "--worker-id", "worker-a", "--artifact", str(outside), "--log", str(log), "--result", "ready", expected=2)
        self.assertTrue(any(reason.startswith("LANE_ARTIFACT_OUTSIDE_WORKSPACE") for reason in outside_result["reasons"]))

    def test_wave_rejects_task_and_baseline_mismatch(self) -> None:
        plan = {"parallelism_required": False, "lanes": [{"lane_id": "LANE-A", "task_ids": ["T-EXPECTED"], "paths": ["src/a/"], "baseline_heads": {"coordinator": "expected"}}]}
        plan_path = self.work / "plan.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        journal = self.work / "lanes.jsonl"
        workspace = self.work / "worker"
        workspace.mkdir()
        artifact = workspace / "a.patch"
        log = workspace / "a.log"
        artifact.write_text("patch", encoding="utf-8")
        log.write_text("command", encoding="utf-8")
        self._run("lane-start", "--journal", str(journal), "--task-id", "T-WRONG", "--lane-id", "LANE-A", "--worker-id", "worker-a", "--workspace", str(workspace), "--baseline", "wrong", "--path", "src/a/")
        self._run("lane-finish", "--journal", str(journal), "--lane-id", "LANE-A", "--worker-id", "worker-a", "--artifact", str(artifact), "--log", str(log), "--result", "ready")
        result = self._run("validate-wave", "--plan", str(plan_path), "--journal", str(journal), expected=2)
        self.assertIn("LANE_TASK_ID_MISMATCH:LANE-A", result["reasons"])
        self.assertIn("LANE_BASELINE_MISMATCH:LANE-A", result["reasons"])

    def test_task_completion_is_derived_only_from_published_self_bound_receipt(self) -> None:
        self.state["task_overrides"] = {}
        self._write_program()
        self._commit_and_push(self.coordinator, "program baseline")
        evidence = self.coordinator / "evidence" / "base" / "result.json"
        evidence.parent.mkdir(parents=True)
        evidence.write_text('{"result":"pass"}\n', encoding="utf-8")
        (self.coordinator / "src" / "base.py").write_text("BASE = 2\n", encoding="utf-8")
        self._run("prepare-receipt", *self._program_args(), "--task-id", "T-BASE", "--repo-id", "coordinator", "--repo-root", str(self.coordinator), "--acceptance-command", "python -m unittest test_base", "--evidence", "evidence/base/result.json", "--gate", "unit-tests")
        self._git(self.coordinator, "add", "-A")
        self._git(self.coordinator, "commit", "-m", "RND-TEST T-BASE: implement base")
        before_push = self._run("plan", *self._program_args())
        self.assertNotEqual(before_push["effective_states"]["T-BASE"], "task_remote_verified")
        self.assertNotIn("T-NEXT", before_push["eligible_tasks"])
        self._git(self.coordinator, "push", "origin", "master")
        after_push = self._run("plan", *self._program_args())
        self.assertEqual(after_push["effective_states"]["T-BASE"], "task_remote_verified")
        self.assertIn("T-NEXT", after_push["eligible_tasks"])
        self.assertFalse(after_push["stop_allowed"])

    def test_remote_verified_tasks_create_review_checkpoint_not_program_completion(self) -> None:
        self.state["task_overrides"] = {
            "T-BASE": {"state": "accepted", "review": "ORCHESTRATOR", "commit": self._git(self.coordinator, "rev-parse", "HEAD").stdout.strip()},
            "T-NEXT": {"state": "accepted", "review": "ORCHESTRATOR", "commit": self._git(self.runner, "rev-parse", "HEAD").stdout.strip()},
        }
        self._write_program()
        complete = self._run("plan", *self._program_args())
        self.assertTrue(complete["program_complete"])
        self.assertTrue(complete["stop_allowed"])
        self.assertEqual(complete["stop_reason"], "PROGRAM_COMPLETE")
        self.state["task_overrides"]["T-NEXT"] = {"state": "blocked_environment"}
        self.state["environment_blocks"] = [{"task_id": "T-NEXT", "state": "open", "condition": "external Linux host unavailable", "evidence": ["probe failed"], "fallbacks_attempted": ["local", "CI"], "safe_state": "no mutation", "resume": "rerun on Linux"}]
        self._write_program()
        checkpoint = self._run("plan", *self._program_args())
        self.assertFalse(checkpoint["stop_allowed"])
        self.assertTrue(checkpoint["checkpoint_allowed"])
        self.assertEqual(checkpoint["stop_reason"], "ORCHESTRATOR_OR_ENVIRONMENT_CHECKPOINT")

    def test_register_finding_creates_canonical_corrective_task(self) -> None:
        payload = {"id": "F-DYNAMIC-001", "severity": "P1", "summary": "a deterministic test is failing", "source_task_id": "T-NEXT", "evidence": ["tests/output.txt"], "correction_task": {"id": "T-CORR-DYNAMIC-001", "work_package": "WP-01", "repositories": ["runner"], "dependencies": [], "reversible": True, "operation_class": "correction", "paths": ["tests/", "evidence/corrections/"], "priority": 250, "auto_activate": True}}
        payload_path = self.work / "finding.json"
        payload_path.write_text(json.dumps(payload), encoding="utf-8")
        result = self._run("register-finding", *self._program_args(), "--payload", str(payload_path))
        self.assertEqual(result["correction_task_id"], "T-CORR-DYNAMIC-001")
        plan = self._run("plan", *self._program_args())
        self.assertIn("T-CORR-DYNAMIC-001", plan["eligible_tasks"])
        self.assertIn("F-DYNAMIC-001", plan["open_actionable_findings"])
        self.assertFalse(plan["stop_allowed"])

    def test_doctor_rejects_protected_hash_drift_and_incomplete_objective_coverage(self) -> None:
        self.backlog["objectives"].pop("T2")
        self._write_program()
        oracle = self.coordinator / "tests" / "acceptance" / "oracle.py"
        oracle.write_text("ORACLE = 9\n", encoding="utf-8")
        result = self._run("doctor", *self._program_args(), expected=2)
        self.assertIn("REQUIRED_OBJECTIVE_MISSING", result["reasons"])
        self.assertTrue(any(reason.startswith("PROTECTED_FILE_DRIFT") for reason in result["reasons"]))
