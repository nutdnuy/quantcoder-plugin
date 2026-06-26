# Agent Instructions - QuantCoder Plugin

This repository is the shared source of truth for the QuantCoder Claude Code
and Codex plugin wrapper around `SL-Mar/quantcoder`.

## Goal

Provide an installable agent plugin that helps users run QuantCoder workflows:

- search quantitative papers
- download and summarize papers
- generate QuantConnect LEAN Python drafts
- locally lint common QuantConnect API mistakes
- optionally validate and backtest through QuantConnect
- run evolution/autonomous/library-builder modes when appropriate

## Plugin Surfaces

- Codex plugin manifest: `.codex-plugin/plugin.json`
- Codex marketplace manifest: `.agents/plugins/marketplace.json`
- Claude plugin manifest: `.claude-plugin/plugin.json`
- Claude marketplace manifest: `.claude-plugin/marketplace.json`
- Shared skill: `skills/quantcoder-research/SKILL.md`
- Claude slash commands: `commands/*.md`
- MCP configuration: `.mcp.json`
- MCP stdio wrapper: `quantcoder/mcp_stdio.py` and `scripts/quantcoder-mcp`

When behavior changes, update all relevant surfaces.

## Development

Use `uv` when available:

```bash
uv run quantcoder --help
uv run --extra mcp python -c "import quantcoder.mcp_stdio; print('ok')"
uv run --extra mcp pytest tests/test_qc_linter.py tests/test_mcp.py -q
```

Validate the Codex plugin manifest before handoff:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

## Safety

QuantCoder output is research scaffolding. Never present generated strategies
or backtests as guaranteed profitable. Always distinguish implementation facts,
assumptions, interpretations, and recommendations. Check for data leakage,
look-ahead bias, survivorship bias, overfitting, unrealistic costs, and
mathematical fidelity to the source paper.

Do not commit secrets. QuantConnect and optional API keys must come from user
environment variables or `~/.quantcoder/.env`.
