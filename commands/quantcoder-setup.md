---
description: Check local QuantCoder plugin utilities and optional QuantConnect setup
argument-hint: ""
allowed-tools: Bash(cd:*), Bash(uv:*), Bash(quantcoder:*), Bash(curl:*)
---

Check the plugin-local QuantCoder utility setup.

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && uv run quantcoder --help
cd "${CLAUDE_PLUGIN_ROOT}" && uv run --extra mcp python -c "import quantcoder.mcp_stdio; print('mcp ok')"
```

Then report whether the CLI and MCP wrapper are available, and whether the user
still needs to set
`QUANTCONNECT_API_KEY` and `QUANTCONNECT_USER_ID` for validation/backtesting.
