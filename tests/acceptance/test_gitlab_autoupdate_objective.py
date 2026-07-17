from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts" / "gitlab_autoupdate.py"
EDITIONS = ("ce", "ee")
DISTRIBUTIONS = ("bullseye", "bookworm", "trixie")
ARCHITECTURES = ("amd64", "arm64")


class GitLabAutoupdateAcceptanceTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.work = Path(self.tempdir.name)
        self.catalog = self.work / "catalog.json"
        self.catalog.write_text(json.dumps(self._catalog(), indent=2), encoding="utf-8")
        self.manifest = self.work / "manifest.toml"
        self.manifest.write_text(self._manifest(), encoding="utf-8")

    def _packages(self, version: str) -> list[dict]:
        packages = []
        for edition in EDITIONS:
            for distribution in DISTRIBUTIONS:
                for architecture in ARCHITECTURES:
                    package = f"gitlab-{edition}"
                    url = (
                        f"https://packages.gitlab.com/gitlab/{package}/packages/debian/{distribution}/"
                        f"{package}_{version}-{edition}.0_{architecture}.deb/download.deb"
                    )
                    packages.append(
                        {
                            "edition": edition,
                            "distribution": distribution,
                            "architecture": architecture,
                            "url": url,
                            "sha256": hashlib.sha256(
                                f"{version}:{edition}:{distribution}:{architecture}".encode()
                            ).hexdigest(),
                        }
                    )
        return packages

    def _catalog(self) -> dict:
        return {
            "artifact_kind": "gitlab-package-catalog-fixture",
            "source": "https://packages.gitlab.com/gitlab/",
            "observed_at": "2026-07-17",
            "required_stops": {
                "18": ["18.2", "18.5", "18.8", "18.11"],
                "19": ["19.2", "19.5", "19.8", "19.11"],
            },
            "releases": [
                {"version": version, "packages": self._packages(version)}
                for version in ("18.8.10", "18.11.2", "18.11.5", "19.1.0", "19.2.4")
            ],
        }

    def _manifest(self) -> str:
        lines = ['packaging_format = 2', 'id = "gitlab"', 'version = "18.8.10~ynh1"', '', '[resources.sources]']
        for edition in EDITIONS:
            for distribution in DISTRIBUTIONS:
                name = f"latest_{edition}_{distribution}"
                lines.extend(
                    [
                        f"[resources.sources.{name}]",
                        f'rename = "gitlab-{edition}.deb"',
                        'amd64.url = "https://example.invalid/old-amd64.deb"',
                        f'amd64.sha256 = "{"0" * 64}"',
                        'arm64.url = "https://example.invalid/old-arm64.deb"',
                        f'arm64.sha256 = "{"1" * 64}"',
                        "",
                    ]
                )
        return "\n".join(lines)

    def _run(self, *args: str, expected: int = 0) -> dict:
        self.assertTrue(CLI.is_file(), "RED: scripts/gitlab_autoupdate.py is not implemented")
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

    def test_resolver_includes_required_stops_and_latest_patch(self) -> None:
        result = self._run(
            "resolve",
            "--catalog",
            str(self.catalog),
            "--current",
            "18.8.10",
            "--target",
            "19.2.4",
            "--edition",
            "ce",
            "--distribution",
            "bookworm",
            "--architecture",
            "amd64",
        )
        self.assertEqual(result["upgrade_path"], ["18.11.5", "19.2.4"])
        selected = result["target_package"]
        self.assertEqual(selected["edition"], "ce")
        self.assertEqual(selected["distribution"], "bookworm")
        self.assertEqual(selected["architecture"], "amd64")
        self.assertIn("gitlab-ce_19.2.4-ce.0_amd64.deb", selected["url"])
        self.assertEqual(len(selected["sha256"]), 64)

    def test_generate_produces_complete_atomic_candidate_without_mutating_input(self) -> None:
        before = self.manifest.read_bytes()
        candidate = self.work / "candidate.toml"
        result = self._run(
            "generate",
            "--catalog",
            str(self.catalog),
            "--manifest",
            str(self.manifest),
            "--target",
            "19.2.4",
            "--output",
            str(candidate),
        )
        self.assertEqual(self.manifest.read_bytes(), before)
        self.assertFalse(result["promoted"])
        self.assertEqual(result["target_version"], "19.2.4")
        parsed = tomllib.loads(candidate.read_text(encoding="utf-8"))
        self.assertEqual(parsed["version"], "19.2.4~ynh1")
        sources = parsed["resources"]["sources"]
        for edition in EDITIONS:
            for distribution in DISTRIBUTIONS:
                source = sources[f"latest_{edition}_{distribution}"]
                for architecture in ARCHITECTURES:
                    asset = source[architecture]
                    self.assertIn(f"gitlab-{edition}_19.2.4-{edition}.0_{architecture}.deb", asset["url"])
                    self.assertEqual(len(asset["sha256"]), 64)
                    self.assertNotIn("latest", asset["url"].lower())

    def test_missing_matrix_entry_and_mutable_target_fail_closed(self) -> None:
        payload = json.loads(self.catalog.read_text(encoding="utf-8"))
        target = next(item for item in payload["releases"] if item["version"] == "19.2.4")
        target["packages"] = [
            item
            for item in target["packages"]
            if not (
                item["edition"] == "ee"
                and item["distribution"] == "trixie"
                and item["architecture"] == "arm64"
            )
        ]
        incomplete = self.work / "incomplete.json"
        incomplete.write_text(json.dumps(payload), encoding="utf-8")
        rejected = self._run(
            "generate",
            "--catalog",
            str(incomplete),
            "--manifest",
            str(self.manifest),
            "--target",
            "19.2.4",
            "--output",
            str(self.work / "rejected.toml"),
            expected=2,
        )
        self.assertFalse(rejected["valid"])
        self.assertIn("INCOMPLETE_PACKAGE_MATRIX", rejected["reasons"])

        mutable = self._run(
            "resolve",
            "--catalog",
            str(self.catalog),
            "--current",
            "18.8.10",
            "--target",
            "latest",
            "--edition",
            "ce",
            "--distribution",
            "bookworm",
            "--architecture",
            "amd64",
            expected=2,
        )
        self.assertFalse(mutable["valid"])
        self.assertIn("MUTABLE_TARGET_FORBIDDEN", mutable["reasons"])


if __name__ == "__main__":
    unittest.main()
