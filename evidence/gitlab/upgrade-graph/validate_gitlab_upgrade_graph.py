#!/usr/bin/env python3
"""Validate the bounded GitLab required-upgrade-stop graph artifact."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MINOR_RE = re.compile(r"^(\d+)\.(\d+)$")
VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


class GraphError(ValueError):
    pass


def load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise GraphError("GRAPH_OBJECT_REQUIRED")
    if not str(payload.get("source", {}).get("url", "")).startswith("https://docs.gitlab.com/"):
        raise GraphError("OFFICIAL_SOURCE_REQUIRED")
    stops = payload.get("required_stops")
    if not isinstance(stops, dict) or not stops:
        raise GraphError("REQUIRED_STOPS_REQUIRED")
    for major, entries in stops.items():
        if not str(major).isdigit() or not isinstance(entries, list):
            raise GraphError("INVALID_MAJOR_STOP_LIST")
        seen: set[str] = set()
        previous: tuple[int, int, int] | None = None
        for entry in entries:
            if not isinstance(entry, dict):
                raise GraphError("INVALID_STOP_ENTRY")
            raw = entry.get("version") or entry.get("minor")
            if not isinstance(raw, str):
                raise GraphError("STOP_VERSION_REQUIRED")
            match = VERSION_RE.fullmatch(raw) or MINOR_RE.fullmatch(raw)
            if not match or int(match.group(1)) != int(major):
                raise GraphError("STOP_VERSION_MAJOR_MISMATCH")
            key = raw
            if key in seen:
                raise GraphError("DUPLICATE_STOP")
            seen.add(key)
            value = tuple(int(part) for part in match.groups())
            if len(value) == 2:
                value = (*value, -1)
            if previous is not None and value <= previous:
                raise GraphError("STOPS_MUST_BE_ASCENDING")
            previous = value
    examples = payload.get("examples")
    if not isinstance(examples, list) or not examples:
        raise GraphError("EXAMPLES_REQUIRED")
    for example in examples:
        if not isinstance(example, dict):
            raise GraphError("INVALID_EXAMPLE")
        current = example.get("current")
        target = example.get("target")
        if not isinstance(current, str) or not VERSION_RE.fullmatch(current):
            raise GraphError("EXAMPLE_CURRENT_VERSION_REQUIRED")
        if not isinstance(target, str) or not VERSION_RE.fullmatch(target):
            raise GraphError("EXAMPLE_TARGET_VERSION_REQUIRED")
        if example.get("kind") == "positive":
            path = example.get("required_stop_minors")
            if not isinstance(path, list) or any(not isinstance(item, str) or not MINOR_RE.fullmatch(item) for item in path):
                raise GraphError("POSITIVE_PATH_REQUIRED")
        elif example.get("kind") == "negative":
            if not isinstance(example.get("expected_error"), str):
                raise GraphError("NEGATIVE_ERROR_REQUIRED")
        else:
            raise GraphError("UNKNOWN_EXAMPLE_KIND")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    args = parser.parse_args(argv)
    try:
        payload = load(args.graph)
    except (OSError, json.JSONDecodeError, GraphError) as error:
        print(json.dumps({"valid": False, "reasons": [str(error)]}, sort_keys=True))
        return 2
    print(json.dumps({"valid": True, "required_stops": sum(len(items) for items in payload["required_stops"].values())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


