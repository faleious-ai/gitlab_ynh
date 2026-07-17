from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "gitlab_autoupdate.py"
CATALOG = ROOT / "evidence" / "gitlab" / "catalog" / "RND-20260717-017-live-package-catalog.json"
EXPECTED = {
    (edition, distribution, architecture)
    for edition in ("ce", "ee")
    for distribution in ("bullseye", "bookworm", "trixie")
    for architecture in ("amd64", "arm64")
}


class GitLabLiveCatalogTests(unittest.TestCase):
    def test_complete_fixed_official_matrix_is_consumable(self) -> None:
        payload = json.loads(CATALOG.read_text(encoding="utf-8"))
        self.assertEqual(payload["result"], "complete_fixed_matrix")
        self.assertEqual(payload["releases"][0]["version"], "18.11.7")
        packages = payload["releases"][0]["packages"]
        self.assertEqual(
            {(row["edition"], row["distribution"], row["architecture"]) for row in packages},
            EXPECTED,
        )
        for row in packages:
            self.assertTrue(row["url"].startswith("https://packages.gitlab.com/gitlab/"))
            self.assertIn("/debian/", row["url"])
            self.assertTrue(row["url"].endswith("/download.deb"))
            self.assertNotIn("latest", row["url"].lower())
            self.assertRegex(row["sha256"], re.compile(r"^[0-9a-f]{64}$"))
            self.assertTrue(row["metadata_url"].startswith("https://packages.gitlab.com/gitlab/"))

        completed = subprocess.run(
            [
                sys.executable,
                str(CLI),
                "resolve",
                "--catalog",
                str(CATALOG),
                "--current",
                "18.11.7",
                "--target",
                "18.11.7",
                "--edition",
                "ee",
                "--distribution",
                "bookworm",
                "--architecture",
                "arm64",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        result = json.loads(completed.stdout)
        self.assertTrue(result["valid"])
        selected = result["target_package"]
        self.assertEqual(selected["edition"], "ee")
        self.assertEqual(selected["distribution"], "bookworm")
        self.assertEqual(selected["architecture"], "arm64")
        self.assertEqual(selected["sha256"], "2e2213917100bafc06256e292a70000b38fdf639c35e19e373b5000c5a73350e")


if __name__ == "__main__":
    unittest.main()

