---
name: quantcoder-research
description: Use QuantCoder for quantitative research-paper to QuantConnect LEAN algorithm workflows, including arXiv/deep search, PDF download, summarization, code generation, local QC linting, QuantConnect validation, backtesting, evolution, autonomous mode, and library building. Use when the user mentions QuantCoder, QuantConnect code generation, LEAN algorithms from papers, local Ollama quant research, alpha evolution, or asks to lint/validate/backtest QuantConnect Python code.
---

# QuantCoder Research

QuantCoder is a local-first research assistant for turning quantitative papers
into draft QuantConnect LEAN algorithms. Treat it as a research scaffold, not a
source of guaranteed trading performance.

## Preconditions

- Python 3.10+.
- Install the package from this plugin root:

```bash
cd "${CLAUDE_PLUGIN_ROOT:-.}"
uv run quantcoder --help
```

- Ollama must be running for search/summarize/generate workflows:

```bash
ollama pull qwen2.5-coder:14b
ollama pull mistral
curl http://localhost:11434/api/tags
```

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

2. Download and summarize:

```bash
quantcoder download 1
quantcoder summarize 1
quantcoder summaries
```

3. Generate a QuantConnect draft:

```bash
quantcoder generate 1 --max-attempts 6
quantcoder generate 1 --open-in-editor
```

4. Verify before interpreting results:

```bash
quantcoder validate generated_code/algorithm_1.py --local-only
quantcoder validate generated_code/algorithm_1.py
quantcoder backtest generated_code/algorithm_1.py --start 2020-01-01 --end 2024-01-01
```

5. Use evolution/autonomous modes only after the base logic is manually reviewed:

```bash
quantcoder evolve start 1 --gens 3 --variants 5
quantcoder auto start --query "momentum trading" --max-iterations 50
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
  generated implementation. Upstream QuantCoder notes that local LLMs may
  substitute simpler indicator proxies for non-trivial math.

## Common Failure Modes

- Ollama is not running or the configured models are missing.
- `~/.quantcoder/config.toml` has a stale `ollama_base_url`.
- QuantConnect credentials are absent or have insufficient permissions.
- Generated code compiles but does not faithfully implement the paper.
- Backtest results omit realistic fees, slippage, borrow constraints, or
  execution limits.
