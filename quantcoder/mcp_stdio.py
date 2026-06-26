"""Stdio MCP wrapper for QuantCoder's QuantConnect helpers."""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from quantcoder.config import Config
from quantcoder.core.qc_linter import lint_qc_code
from quantcoder.mcp.quantconnect_mcp import QuantConnectMCPClient

mcp = FastMCP("quantcoder_mcp")


def _json(data: Any) -> str:
    """Return stable JSON for MCP clients."""
    return json.dumps(data, indent=2, sort_keys=True, default=str)


def _credentialed_client() -> QuantConnectMCPClient:
    config = Config.load()
    api_key, user_id = config.load_quantconnect_credentials()
    return QuantConnectMCPClient(api_key=api_key, user_id=user_id)


@mcp.tool(
    name="quantcoder_lint_qc_code",
    annotations={
        "title": "Lint QuantConnect Python Code",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def quantcoder_lint_qc_code(code: str) -> str:
    """Run QuantCoder's local static linter for common QuantConnect Python API mistakes."""
    result = lint_qc_code(code)
    return _json({
        "fixed_code": result.code,
        "had_fixes": result.had_fixes,
        "unfixable_count": result.unfixable_count,
        "issues": [
            {
                "rule_id": issue.rule_id,
                "line": issue.line,
                "message": issue.message,
                "severity": issue.severity,
                "fixed": issue.fixed,
                "original": issue.original,
                "replacement": issue.replacement,
            }
            for issue in result.issues
        ],
    })


@mcp.tool(
    name="quantcoder_validate_code",
    annotations={
        "title": "Validate QuantConnect Code",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def quantcoder_validate_code(
    code: str,
    files: dict[str, str] | None = None,
) -> str:
    """Create a temporary QuantConnect project, upload code, and compile it."""
    try:
        client = _credentialed_client()
        result = await client.validate_code(code=code, files=files or {})
        return _json(result)
    except Exception as exc:
        return _json({"valid": False, "errors": [str(exc)], "warnings": []})


@mcp.tool(
    name="quantcoder_backtest",
    annotations={
        "title": "Run QuantConnect Backtest",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def quantcoder_backtest(
    code: str,
    start_date: str,
    end_date: str,
    files: dict[str, str] | None = None,
    name: str | None = None,
) -> str:
    """Compile and run a QuantConnect backtest for the provided LEAN algorithm code."""
    try:
        client = _credentialed_client()
        result = await client.backtest(
            code=code,
            start_date=start_date,
            end_date=end_date,
            files=files or {},
            name=name,
        )
        return _json(result)
    except Exception as exc:
        return _json({"success": False, "error": str(exc)})


@mcp.tool(
    name="quantcoder_get_api_docs",
    annotations={
        "title": "Get QuantConnect Documentation Link",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def quantcoder_get_api_docs(topic: str) -> str:
    """Return the best QuantConnect documentation URL for a topic."""
    client = QuantConnectMCPClient(api_key="", user_id="")
    return await client.get_api_docs(topic)


def run() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
