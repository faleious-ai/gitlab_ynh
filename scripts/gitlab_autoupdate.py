#!/usr/bin/env python3
"""Resolve fixed GitLab package paths and generate non-promoting candidates."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import tomllib
from pathlib import Path
from typing import Any


EDITIONS = ("ce", "ee")
DISTRIBUTIONS = ("bullseye", "bookworm", "trixie")
ARCHITECTURES = ("amd64", "arm64")
VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ContractError(Exception):
    def __init__(self, *reasons: str) -> None:
        self.reasons = list(reasons)
        super().__init__(", ".join(self.reasons))


def read_json(path: str) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContractError("INVALID_CATALOG_JSON") from error
    if not isinstance(payload, dict):
        raise ContractError("CATALOG_OBJECT_REQUIRED")
    return payload


def version_key(version: str) -> tuple[int, int, int]:
    match = VERSION_RE.fullmatch(version)
    if not match:
        raise ContractError("EXACT_VERSION_REQUIRED")
    return tuple(int(part) for part in match.groups())


def releases(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    entries = catalog.get("releases")
    if not isinstance(entries, list):
        raise ContractError("RELEASE_LIST_REQUIRED")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for release in entries:
        if not isinstance(release, dict) or not isinstance(release.get("version"), str):
            raise ContractError("RELEASE_VERSION_REQUIRED")
        version = release["version"]
        version_key(version)
        if version in seen:
            raise ContractError("DUPLICATE_RELEASE_VERSION")
        seen.add(version)
        result.append(release)
    return sorted(result, key=lambda item: version_key(item["version"]))


def release_for(catalog: dict[str, Any], version: str) -> dict[str, Any]:
    for release in releases(catalog):
        if release["version"] == version:
            return release
    raise ContractError("RELEASE_NOT_FOUND")


def package_matrix(release: dict[str, Any]) -> dict[tuple[str, str, str], dict[str, Any]]:
    packages = release.get("packages")
    if not isinstance(packages, list):
        raise ContractError("INCOMPLETE_PACKAGE_MATRIX")
    matrix: dict[tuple[str, str, str], dict[str, Any]] = {}
    for package in packages:
        if not isinstance(package, dict):
            raise ContractError("INVALID_PACKAGE_ENTRY")
        key = tuple(package.get(field) for field in ("edition", "distribution", "architecture"))
        if key in matrix or any(not isinstance(value, str) for value in key):
            raise ContractError("INVALID_PACKAGE_MATRIX_KEY")
        url = package.get("url")
        checksum = package.get("sha256")
        if not isinstance(url, str) or not url or "latest" in url.lower():
            raise ContractError("MUTABLE_PACKAGE_URL_FORBIDDEN")
        if not isinstance(checksum, str) or not SHA256_RE.fullmatch(checksum.lower()):
            raise ContractError("INVALID_PACKAGE_SHA256")
        matrix[key] = package
    expected = {
        (edition, distribution, architecture)
        for edition in EDITIONS
        for distribution in DISTRIBUTIONS
        for architecture in ARCHITECTURES
    }
    if set(matrix) != expected:
        raise ContractError("INCOMPLETE_PACKAGE_MATRIX")
    return matrix


def package_for(catalog: dict[str, Any], version: str, edition: str, distribution: str, architecture: str) -> dict[str, Any]:
    if edition not in EDITIONS or distribution not in DISTRIBUTIONS or architecture not in ARCHITECTURES:
        raise ContractError("UNSUPPORTED_PACKAGE_COORDINATE")
    matrix = package_matrix(release_for(catalog, version))
    package = matrix[(edition, distribution, architecture)]
    return {
        "edition": package["edition"],
        "distribution": package["distribution"],
        "architecture": package["architecture"],
        "url": package["url"],
        "sha256": package["sha256"].lower(),
    }


def latest_patch_for(release_entries: list[dict[str, Any]], major: int, minor: int, limit: tuple[int, int, int]) -> str:
    candidates = [
        release["version"]
        for release in release_entries
        if version_key(release["version"])[0:2] == (major, minor)
        and version_key(release["version"]) <= limit
    ]
    if not candidates:
        raise ContractError("REQUIRED_STOP_NOT_AVAILABLE")
    return max(candidates, key=version_key)


def upgrade_path(catalog: dict[str, Any], current: str, target: str) -> list[str]:
    current_key = version_key(current)
    target_key = version_key(target)
    if target_key < current_key:
        raise ContractError("DOWNGRADE_NOT_SUPPORTED")
    entries = releases(catalog)
    required_stops = catalog.get("required_stops", {})
    if not isinstance(required_stops, dict):
        raise ContractError("REQUIRED_STOPS_REQUIRED")
    path: list[str] = []
    current_major, current_minor, _ = current_key
    target_major, target_minor, _ = target_key
    for major in range(current_major, target_major + 1):
        configured = required_stops.get(str(major), [])
        if not isinstance(configured, list):
            raise ContractError("INVALID_REQUIRED_STOPS")
        for stop in configured:
            if not isinstance(stop, str) or "." not in stop:
                raise ContractError("INVALID_REQUIRED_STOP")
            stop_major, stop_minor = (int(part) for part in stop.split(".", 1))
            if stop_major != major:
                raise ContractError("INVALID_REQUIRED_STOP")
            if (major, stop_minor) <= (current_major, current_minor):
                continue
            if (major, stop_minor) >= (target_major, target_minor):
                continue
            path.append(latest_patch_for(entries, stop_major, stop_minor, target_key))
    path = sorted(set(path), key=version_key)
    if target != current:
        path.append(target)
    return path


def resolve(catalog: dict[str, Any], current: str, target: str, edition: str, distribution: str, architecture: str) -> dict[str, Any]:
    if target.lower() in {"latest", "edge", "stable"}:
        raise ContractError("MUTABLE_TARGET_FORBIDDEN")
    path = upgrade_path(catalog, current, target)
    selected = package_for(catalog, target, edition, distribution, architecture)
    return {
        "valid": True,
        "current_version": current,
        "target_version": target,
        "upgrade_path": path,
        "target_package": selected,
    }


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def source_block(name: str, edition: str, matrix: dict[tuple[str, str, str], dict[str, Any]]) -> str:
    lines = [f"[resources.sources.{name}]", f"rename = {toml_string(f'gitlab-{edition}.deb')}"]
    for architecture in ARCHITECTURES:
        package = matrix[(edition, name.rsplit("_", 1)[-1], architecture)]
        lines.append(f"{architecture}.url = {toml_string(package['url'])}")
        lines.append(f"{architecture}.sha256 = {toml_string(package['sha256'].lower())}")
    return "\n".join(lines) + "\n"


def build_candidate(manifest_text: str, manifest: dict[str, Any], catalog: dict[str, Any], target: str) -> str:
    target_release = release_for(catalog, target)
    matrix = package_matrix(target_release)
    version_line = re.compile(r"(?m)^version\s*=\s*\"[^\"]*\"\s*$")
    candidate = version_line.sub(f"version = {toml_string(target + '~ynh1')}", manifest_text, count=1)
    if candidate == manifest_text:
        raise ContractError("MANIFEST_VERSION_FIELD_REQUIRED")
    for edition in EDITIONS:
        for distribution in DISTRIBUTIONS:
            name = f"latest_{edition}_{distribution}"
            pattern = re.compile(
                rf"(?ms)^[ \t]*\[resources\.sources\.{re.escape(name)}\]\r?\n.*?(?=^[ \t]*\[|\Z)"
            )
            replacement = source_block(name, edition, matrix)
            candidate, count = pattern.subn(replacement, candidate, count=1)
            if count != 1:
                raise ContractError("MANIFEST_SOURCE_REQUIRED")
    try:
        parsed = tomllib.loads(candidate)
    except tomllib.TOMLDecodeError as error:
        raise ContractError("GENERATED_MANIFEST_INVALID") from error
    if parsed.get("version") != target + "~ynh1":
        raise ContractError("GENERATED_VERSION_MISMATCH")
    return candidate


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as handle:
            temporary = handle.name
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def generate(catalog: dict[str, Any], manifest_path: str, target: str, output: str) -> dict[str, Any]:
    if target.lower() in {"latest", "edge", "stable"}:
        raise ContractError("MUTABLE_TARGET_FORBIDDEN")
    path = Path(manifest_path)
    try:
        manifest_text = path.read_text(encoding="utf-8")
        manifest = tomllib.loads(manifest_text)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ContractError("INVALID_MANIFEST") from error
    candidate = build_candidate(manifest_text, manifest, catalog, target)
    output_path = Path(output)
    atomic_write(output_path, candidate)
    return {
        "valid": True,
        "promoted": False,
        "target_version": target,
        "candidate": str(output_path),
        "manifest_unchanged": True,
        "package_matrix": len(EDITIONS) * len(DISTRIBUTIONS) * len(ARCHITECTURES),
    }


def emit(payload: dict[str, Any], exit_code: int = 0) -> int:
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
    return exit_code


def build_parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    resolve_parser = commands.add_parser("resolve")
    resolve_parser.add_argument("--catalog", required=True)
    resolve_parser.add_argument("--current", required=True)
    resolve_parser.add_argument("--target", required=True)
    resolve_parser.add_argument("--edition", required=True)
    resolve_parser.add_argument("--distribution", required=True)
    resolve_parser.add_argument("--architecture", required=True)

    generate_parser = commands.add_parser("generate")
    generate_parser.add_argument("--catalog", required=True)
    generate_parser.add_argument("--manifest", required=True)
    generate_parser.add_argument("--target", required=True)
    generate_parser.add_argument("--output", required=True)
    return root


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        catalog = read_json(args.catalog)
        if args.command == "resolve":
            return emit(
                resolve(catalog, args.current, args.target, args.edition, args.distribution, args.architecture)
            )
        if args.command == "generate":
            return emit(generate(catalog, args.manifest, args.target, args.output))
        raise ContractError("UNKNOWN_COMMAND")
    except ContractError as error:
        return emit({"valid": False, "reasons": error.reasons}, 2)


if __name__ == "__main__":
    sys.exit(main())
