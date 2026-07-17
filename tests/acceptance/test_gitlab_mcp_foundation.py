from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MCP_ROOT = ROOT.parent / "gitlab-mcp"
PROTOCOL_VERSION = "2025-11-25"


class GitLabMcpFoundationAcceptanceTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.mcp_root = Path(os.environ.get("GITLAB_MCP_ROOT", DEFAULT_MCP_ROOT)).resolve()
        cls.server = cls.mcp_root / "server.py"
        if not cls.server.is_file():
            raise AssertionError(
                f"RED: GitLab MCP server is not implemented at {cls.server}; "
                "set GITLAB_MCP_ROOT for an alternate checkout"
            )
        cls.responses, cls.stderr = cls._run_conversation()

    @classmethod
    def _run_conversation(cls) -> tuple[dict[int, dict], str]:
        requests = [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {},
                    "clientInfo": {"name": "maestro-acceptance", "version": "1.0.0"},
                },
            },
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "gitlab.capabilities", "arguments": {}},
            },
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "gitlab.projects.list",
                    "arguments": {"per_page": 2, "page": 1},
                },
            },
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "gitlab.projects.delete",
                    "arguments": {"project_id": 123},
                },
            },
        ]
        payload = "".join(json.dumps(message) + "\n" for message in requests)
        env = os.environ.copy()
        env.update(
            {
                "GITLAB_MCP_TEST_MODE": "1",
                "GITLAB_TOKEN": "",
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )
        completed = subprocess.run(
            [sys.executable, str(cls.server), "--stdio"],
            cwd=cls.mcp_root,
            input=payload,
            text=True,
            capture_output=True,
            timeout=20,
            env=env,
            check=False,
        )
        if completed.returncode != 0:
            raise AssertionError(completed.stderr or completed.stdout)
        responses: dict[int, dict] = {}
        for raw_line in completed.stdout.splitlines():
            if not raw_line.strip():
                continue
            try:
                message = json.loads(raw_line)
            except json.JSONDecodeError as error:
                raise AssertionError(f"stdout must contain only JSON-RPC messages: {raw_line!r}") from error
            if "id" in message:
                responses[message["id"]] = message
        return responses, completed.stderr

    def _result(self, request_id: int) -> dict:
        response = self.responses[request_id]
        self.assertEqual(response["jsonrpc"], "2.0")
        self.assertEqual(response["id"], request_id)
        self.assertNotIn("error", response)
        result = response["result"]
        self.assertRegex(result["_meta"]["trace_id"], r"^[A-Za-z0-9._:-]{8,}$")
        return result

    def test_initialize_negotiates_current_protocol(self) -> None:
        result = self._result(1)
        self.assertEqual(result["protocolVersion"], PROTOCOL_VERSION)
        self.assertIn("tools", result["capabilities"])
        self.assertTrue(result["serverInfo"]["name"])
        self.assertTrue(result["serverInfo"]["version"])

    def test_tools_list_exposes_minimum_catalog_with_policy_annotations(self) -> None:
        result = self._result(2)
        tools = {tool["name"]: tool for tool in result["tools"]}
        self.assertTrue(
            {"gitlab.capabilities", "gitlab.projects.list", "gitlab.projects.delete"}.issubset(tools)
        )
        self.assertTrue(tools["gitlab.capabilities"]["annotations"]["readOnlyHint"])
        self.assertTrue(tools["gitlab.projects.list"]["annotations"]["readOnlyHint"])
        self.assertTrue(tools["gitlab.projects.delete"]["annotations"]["destructiveHint"])
        for tool in tools.values():
            self.assertEqual(tool["inputSchema"]["type"], "object")
            self.assertIn("operationClass", tool)

    def test_capabilities_and_project_listing_are_structured_and_paginated(self) -> None:
        capabilities = self._result(3)["structuredContent"]
        self.assertIn("domains", capabilities)
        self.assertIn("protocol_version", capabilities)
        self.assertEqual(capabilities["protocol_version"], PROTOCOL_VERSION)

        projects = self._result(4)["structuredContent"]
        self.assertEqual(len(projects["items"]), 2)
        self.assertEqual(projects["page"], 1)
        self.assertIn("next_page", projects)
        self.assertLessEqual(projects["per_page"], 100)

    def test_destructive_call_without_confirmation_fails_before_transport(self) -> None:
        response = self.responses[5]
        self.assertEqual(response["jsonrpc"], "2.0")
        self.assertEqual(response["id"], 5)
        self.assertNotIn("result", response)
        error = response["error"]
        self.assertEqual(error["data"]["stable_code"], "CONFIRMATION_REQUIRED")
        self.assertRegex(error["data"]["trace_id"], r"^[A-Za-z0-9._:-]{8,}$")
        self.assertFalse(error["data"]["transport_called"])

    def test_protocol_output_and_logs_do_not_leak_credentials(self) -> None:
        serialized = json.dumps(self.responses) + self.stderr
        self.assertNotIn("PRIVATE-TOKEN", serialized)
        self.assertNotIn("Authorization: Bearer", serialized)
        self.assertNotIn("Traceback", self.stderr)


if __name__ == "__main__":
    unittest.main()
