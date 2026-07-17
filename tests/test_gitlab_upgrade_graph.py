from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "evidence" / "gitlab" / "upgrade-graph" / "RND-20260717-017-required-stop-graph.json"
VALIDATOR = ROOT / "evidence" / "gitlab" / "upgrade-graph" / "validate_gitlab_upgrade_graph.py"
sys.path.insert(0, str(ROOT / "scripts"))
import gitlab_autoupdate  # noqa: E402


class GitLabUpgradeGraphTests(unittest.TestCase):
    def test_official_graph_validates_and_records_positive_negative_paths(self) -> None:
        payload = json.loads(GRAPH.read_text(encoding="utf-8"))
        self.assertEqual(payload["result"], "policy_graph_recorded")
        positive = [item for item in payload["examples"] if item["kind"] == "positive"]
        self.assertEqual(positive[0]["required_stop_minors"][-1], "19.11")
        negative = [item for item in payload["examples"] if item["kind"] == "negative"][0]
        self.assertEqual(negative["expected_error"], "DOWNGRADE_NOT_SUPPORTED")
        result = subprocess.run([sys.executable, str(VALIDATOR), str(GRAPH)], text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(json.loads(result.stdout)["valid"], True)

    def test_graph_rejects_duplicate_or_malformed_stops(self) -> None:
        payload = json.loads(GRAPH.read_text(encoding="utf-8"))
        payload["required_stops"]["18"].append(copy.deepcopy(payload["required_stops"]["18"][0]))
        with tempfile.TemporaryDirectory() as directory:
            invalid = Path(directory) / "invalid.json"
            invalid.write_text(json.dumps(payload), encoding="utf-8")
            result = subprocess.run([sys.executable, str(VALIDATOR), str(invalid)], text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("DUPLICATE_STOP", result.stdout)

    def test_graph_drives_positive_and_negative_resolver_paths(self) -> None:
        versions = [
            "17.11.7",
            "18.2.9",
            "18.5.8",
            "18.8.11",
            "18.11.7",
            "19.2.4",
            "19.5.6",
            "19.8.3",
            "19.11.1",
            "19.12.0",
        ]
        catalog = {
            "required_stops": {
                "17": ["17.11"],
                "18": ["18.2", "18.5", "18.8", "18.11"],
                "19": ["19.2", "19.5", "19.8", "19.11"],
            },
            "releases": [{"version": version} for version in versions],
        }
        self.assertEqual(
            gitlab_autoupdate.upgrade_path(catalog, "17.8.7", "19.12.0"),
            ["17.11.7", "18.2.9", "18.5.8", "18.8.11", "18.11.7", "19.2.4", "19.5.6", "19.8.3", "19.11.1", "19.12.0"],
        )
        with self.assertRaisesRegex(gitlab_autoupdate.ContractError, "DOWNGRADE_NOT_SUPPORTED"):
            gitlab_autoupdate.upgrade_path(catalog, "19.2.0", "18.11.7")


if __name__ == "__main__":
    unittest.main()
