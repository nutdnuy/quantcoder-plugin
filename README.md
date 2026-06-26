# QuantCoder Agent Plugin

Claude Code and Codex plugin wrapper around
[SL-Mar/quantcoder](https://github.com/SL-Mar/quantcoder): a research workflow
for turning quantitative research papers into draft QuantConnect LEAN
algorithms with Claude Code / Codex agents.

> Upstream status: the original QuantCoder project says it is no longer
> maintained and explicitly warns that automated code generation may fail to implement
> non-trivial paper mathematics faithfully. This plugin preserves that caveat:
> use it for research scaffolding, linting, and validation workflows, not as a
> promise of trading performance.

[![Version](https://img.shields.io/badge/version-2.0.0-green)](https://github.com/nutdnuy/quantcoder-plugin)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

## Install as a Codex plugin

```bash
codex plugin marketplace add nutdnuy/quantcoder-plugin
```

Then enable/install `quantcoder` from the Codex plugin UI. The repo includes
`.agents/plugins/marketplace.json` for Codex marketplace discovery and
`.codex-plugin/plugin.json` for the plugin manifest.

## Install as a Claude Code plugin

Add this GitHub repository as a Claude Code marketplace:

```text
/plugin marketplace add https://github.com/nutdnuy/quantcoder-plugin
/plugin install quantcoder
```

The Claude marketplace manifest lives at `.claude-plugin/marketplace.json`, and
the plugin manifest lives at `.claude-plugin/plugin.json`.

## What the plugin adds

- `skills/quantcoder-research/SKILL.md` for agent workflow behavior.
- Claude slash commands:
  - `/quantcoder-setup`
  - `/quantcoder-search`
  - `/quantcoder-generate`
  - `/quantcoder-validate`
  - `/quantcoder-backtest`
- MCP tools through `.mcp.json`:
  - `quantcoder_lint_qc_code`
  - `quantcoder_get_api_docs`
  - `quantcoder_validate_code`
  - `quantcoder_backtest`

The plugin flow is agent-native: Claude Code or Codex reads the paper/summary,
extracts the strategy specification, writes the LEAN draft, then uses the
bundled linter/MCP tools for verification. The plugin intentionally does not
expose live deployment as an MCP tool.

## Local setup

QuantCoder plugin transforms academic quant research into draft QuantConnect
LEAN algorithms using the active Claude Code / Codex agent. No separate local
model server is required for the plugin workflow.

> **Status (Feb 2026):** v2.0.0 introduced a significant refactoring of the code generation pipeline — two-stage generation (framework stubs then mathematical core), two-pass summarization, cross-model fidelity assessment, MinerU PDF extraction, and a static QC API linter (11 rules). This plugin uses Claude Code / Codex Agent for reasoning and code drafting, while preserving the warning that generated implementations of novel mathematical models must be checked manually against the paper.

---

## Installation

### Prerequisites

- Python 3.10+
- Claude Code or Codex with this plugin installed

### Package setup

```bash
git clone https://github.com/nutdnuy/quantcoder-plugin.git
cd quantcoder-plugin

python -m venv .venv
source .venv/bin/activate

pip install -e ".[mcp]"
python -m spacy download en_core_web_sm
```

### Verify

```bash
# Check CLI utilities and plugin package
quantcoder --help
quantcoder-mcp --help
```

---

## Usage

### Interactive Mode

```bash
quantcoder        # or: qc
```

### CLI Commands

```bash
# Search for papers
quantcoder search "momentum trading" --num 5

# Download a paper PDF for the agent to read
quantcoder download 1

# Generate QuantConnect algorithm
# Ask Claude Code / Codex to read the paper or extracted summary and draft LEAN code.

# Validate and backtest (requires QC credentials)
quantcoder validate generated_code/algorithm_1.py
quantcoder backtest generated_code/algorithm_1.py --start 2022-01-01 --end 2024-01-01
```

### Backtest with Detailed Metrics

```bash
# Shows Sharpe, Total Return, CAGR, Max Drawdown, Win Rate, Total Trades
quantcoder backtest generated_code/algorithm_1.py --start 2022-01-01 --end 2024-01-01
```

### Library Builder

```bash
quantcoder library build --comprehensive --max-hours 24
quantcoder library status
```

---

## Configuration

QuantConnect credentials can be set in `~/.quantcoder/.env` or the environment:

```bash
QUANTCONNECT_API_KEY=your_key
QUANTCONNECT_USER_ID=your_id
```

### QuantConnect Integration

For backtesting and deployment, set credentials in `~/.quantcoder/.env`:

```
QUANTCONNECT_API_KEY=your_key
QUANTCONNECT_USER_ID=your_id
```

---

## Architecture

```
quantcoder/
├── cli.py           # CLI entry point
├── config.py        # Configuration management
├── chat.py          # Interactive chat
├── llm/             # Upstream local-model provider layer
├── core/            # LLM handler, processor, NLP
├── agents/          # Multi-agent system (Coordinator, Alpha, Risk, Universe)
├── evolver/         # AlphaEvolve-inspired evolution engine
├── autonomous/      # Self-improving pipeline
├── library/         # Batch strategy library builder
├── tools/           # Pluggable tool system
└── mcp/             # QuantConnect MCP integration
```

---

## Background

QuantCoder was initiated in November 2023 based on ["Dual Agent Chatbots and Expert Systems Design"](https://towardsdev.com/dual-agent-chatbots-and-expert-systems-design-25e2cba434e9). The initial version coded a blended momentum/mean-reversion strategy from ["Outperforming the Market (1000% in 10 years)"](https://medium.com/coinmonks/how-to-outperform-the-market-fe151b944c77?sk=7066045abe12d5cf88c7edc80ec2679c), which received over 10,000 impressions on LinkedIn.

v2.0.0 is a complete rewrite with multi-agent architecture, evolution engine,
autonomous learning, two-stage code generation, two-pass summarization,
cross-model fidelity assessment, MinerU PDF extraction with LaTeX equation
preservation, and a static QC API linter with 11 auto-fix rules. This plugin
uses Claude Code / Codex agents as the default reasoning and coding layer, then
keeps QuantCoder's CLI, linter, and QuantConnect integration as verification
utilities.

---

## License

Apache License 2.0. See [LICENSE](LICENSE).
