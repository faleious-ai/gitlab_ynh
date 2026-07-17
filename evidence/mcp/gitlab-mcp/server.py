#!/usr/bin/env python3
"""Fixture-only GitLab MCP foundation for contract testing and publication."""

from __future__ import annotations

import json
import sys
from typing import Any


PROTOCOL_VERSION = "2025-11-25"
PROJECTS = [
    {"id": 101, "path": "gitlab", "namespace": "faleious-ai"},
    {"id": 102, "path": "gitlab-runner", "namespace": "faleious-ai"},
    {"id": 103, "path": "gitlab-mcp", "namespace": "faleious-ai"},
]


class ProtocolError(Exception):
    def __init__(self, code: int, stable_code: str, message: str) -> None:
        self.code = code
        self.stable_code = stable_code
        self.message = message
        super().__init__(message)


class Server:
    def __init__(self) -> None:
        self.initialized = False
        self.trace_counter = 0

    def trace_id(self) -> str:
        self.trace_counter += 1
        return f"trace-{self.trace_counter:08d}"

    def result(self, request_id: Any, payload: dict[str, Any]) -> dict[str, Any]:
        payload.setdefault("_meta", {"trace_id": self.trace_id()})
        return {"jsonrpc": "2.0", "id": request_id, "result": payload}

    def error(self, request_id: Any, error: ProtocolError) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": error.code,
                "message": error.message,
                "data": {
                    "stable_code": error.stable_code,
                    "trace_id": self.trace_id(),
                    "transport_called": False,
                },
            },
        }

    @staticmethod
    def tools() -> list[dict[str, Any]]:
        return [
            {
                "name": "gitlab.capabilities",
                "description": "Describe the GitLab MCP capability surface.",
                "operationClass": "read",
                "annotations": {"readOnlyHint": True, "destructiveHint": False},
                "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
            },
            {
                "name": "gitlab.projects.list",
                "description": "List GitLab projects with bounded pagination.",
                "operationClass": "read",
                "annotations": {"readOnlyHint": True, "destructiveHint": False},
                "inputSchema": {
                    "type": "object",
                    "properties": {"page": {"type": "integer"}, "per_page": {"type": "integer"}},
                    "additionalProperties": False,
                },
            },
            {
                "name": "gitlab.projects.delete",
                "description": "Delete a project only after explicit authorization and confirmation.",
                "operationClass": "destructive",
                "annotations": {"readOnlyHint": False, "destructiveHint": True},
                "inputSchema": {
                    "type": "object",
                    "properties": {"project_id": {"type": "integer"}, "confirmation": {"type": "string"}},
                    "required": ["project_id"],
                    "additionalProperties": False,
                },
            },
        ]

    def call_tool(self, request_id: Any, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "gitlab.capabilities":
            return self.result(
                request_id,
                {
                    "structuredContent": {
                        "protocol_version": PROTOCOL_VERSION,
                        "server_version": "0.1.0-test-mode",
                        "edition": "ce-ee-aware",
                        "domains": ["projects", "repositories", "pipelines", "groups"],
                    }
                },
            )
        if name == "gitlab.projects.list":
            page = arguments.get("page", 1)
            per_page = arguments.get("per_page", 20)
            if not isinstance(page, int) or not isinstance(per_page, int) or page < 1 or per_page < 1 or per_page > 100:
                raise ProtocolError(-32602, "INVALID_PAGINATION", "invalid pagination")
            start = (page - 1) * per_page
            items = PROJECTS[start : start + per_page]
            next_page = page + 1 if start + per_page < len(PROJECTS) else None
            return self.result(
                request_id,
                {"structuredContent": {"items": items, "page": page, "per_page": per_page, "next_page": next_page}},
            )
        if name == "gitlab.projects.delete":
            raise ProtocolError(-32001, "CONFIRMATION_REQUIRED", "confirmation required")
        raise ProtocolError(-32601, "TOOL_NOT_FOUND", "tool not found")

    def handle(self, message: dict[str, Any]) -> dict[str, Any] | None:
        request_id = message.get("id")
        method = message.get("method")
        if method == "notifications/initialized":
            return None
        if not self.initialized and method != "initialize":
            raise ProtocolError(-32000, "INITIALIZATION_REQUIRED", "initialize must be first")
        if method == "initialize":
            self.initialized = True
            return self.result(
                request_id,
                {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "gitlab-mcp-foundation", "version": "0.1.0"},
                },
            )
        if method == "tools/list":
            return self.result(request_id, {"tools": self.tools()})
        if method == "tools/call":
            params = message.get("params")
            if not isinstance(params, dict) or not isinstance(params.get("name"), str):
                raise ProtocolError(-32602, "INVALID_TOOL_CALL", "tool name required")
            arguments = params.get("arguments", {})
            if not isinstance(arguments, dict):
                raise ProtocolError(-32602, "INVALID_TOOL_ARGUMENTS", "arguments object required")
            return self.call_tool(request_id, params["name"], arguments)
        raise ProtocolError(-32601, "METHOD_NOT_FOUND", "method not found")


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] != "--stdio":
        return 2
    server = Server()
    for raw_line in sys.stdin:
        if not raw_line.strip():
            continue
        request_id: Any = None
        try:
            message = json.loads(raw_line)
            if not isinstance(message, dict):
                raise ProtocolError(-32600, "INVALID_REQUEST", "request object required")
            request_id = message.get("id")
            response = server.handle(message)
        except json.JSONDecodeError:
            response = server.error(request_id, ProtocolError(-32700, "PARSE_ERROR", "invalid JSON"))
        except ProtocolError as error:
            response = server.error(request_id, error)
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=True, separators=(",", ":")) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
