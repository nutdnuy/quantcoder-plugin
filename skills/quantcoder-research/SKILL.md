---
name: quantcoder-research
description: Use Claude Code or Codex Agent with QuantCoder utilities for quantitative research-paper to QuantConnect LEAN algorithm workflows, including arXiv/deep search, PDF download, agent-native summarization, agent-native code generation, local QC linting, QuantConnect validation, and backtesting. Use when the user mentions QuantCoder, QuantConnect code generation, LEAN algorithms from papers, Claude/Codex agent quant research, alpha research, or asks to lint/validate/backtest QuantConnect Python code.
---

# QuantCoder Research

QuantCoder plugin is an agent-native research workflow for turning quantitative
papers into draft QuantConnect LEAN algorithms. Claude Code or Codex Agent does
the summarization, reasoning, and code drafting; QuantCoder utilities provide
paper search/download, local QC linting, and optional QuantConnect
validation/backtesting. Treat it as a research scaffold, not a source of
guaranteed trading performance.

## Preconditions

- Python 3.10+.
- Install the package from this plugin root when CLI utilities are needed:

```bash
cd "${CLAUDE_PLUGIN_ROOT:-.}"
uv run quantcoder --help
```

- Claude Code or Codex is the LLM layer. Do not require a separate local model
  server for the default plugin workflow.

- QuantConnect validation/backtesting needs environment variables or
  `~/.quantcoder/.env`:

```bash
QUANTCONNECT_API_KEY=...
QUANTCONNECT_USER_ID=...
```

- Optional deep search and publishing:
  `TAVILY_API_KEY`, `NOTION_API_KEY`, `NOTION_DATABASE_ID`.

## Core Workflow

1. Search for papers:

```bash
quantcoder search "momentum trading" --num 5
quantcoder search "mean reversion" --deep --num 10
```

2. Download source material:

```bash
quantcoder download 1
```

3. Summarize with the active agent:

- Read the PDF/text or user-provided paper summary.
- Extract: strategy hypothesis, asset universe, signal formula, rebalance rule,
  risk controls, data needs, lookback windows, portfolio construction, and
  expected failure modes.
- Separate facts from assumptions and interpretations.

4. Generate a QuantConnect draft with the active agent:

- Write LEAN Python code directly in the workspace.
- Prefer simple, auditable implementation over clever abstraction.
- Add only comments that clarify non-obvious paper-to-code translation choices.

5. Verify before interpreting results:

```bash
quantcoder validate generated_code/algorithm_1.py --local-only
quantcoder validate generated_code/algorithm_1.py
quantcoder backtest generated_code/algorithm_1.py --start 2020-01-01 --end 2024-01-01
```

## MCP Tools

When MCP is available, prefer tools for focused verification:

- `quantcoder_lint_qc_code`: local static fixes and warnings, no credentials.
- `quantcoder_get_api_docs`: QuantConnect documentation lookup.
- `quantcoder_validate_code`: uploads to QuantConnect and compiles.
- `quantcoder_backtest`: compiles and runs a QuantConnect backtest.

Do not use MCP for live deployment. This plugin intentionally does not expose a
live-trading deployment tool.

## Quality Rules

- Separate facts, assumptions, interpretations, and recommendations.
- Never imply price or return certainty.
- Inspect generated code before backtesting.
- Check for data leakage, look-ahead bias, survivorship bias, transaction
  costs, universe construction assumptions, and overfitting.
- Treat high Sharpe or strong backtest output as a hypothesis requiring
  out-of-sample validation and risk review.
- For novel mathematical models, manually compare the paper equations to the
  generated implementation. Do not substitute simpler indicator proxies unless
  the user explicitly accepts that approximation.

## Common Failure Modes

- QuantConnect credentials are absent or have insufficient permissions.
- Generated code compiles but does not faithfully implement the paper.
- Backtest results omit realistic fees, slippage, borrow constraints, or
  execution limits.
