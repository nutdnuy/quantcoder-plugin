# QuantCoder Agent Plugin

Claude Code and Codex plugin wrapper around
[SL-Mar/quantcoder](https://github.com/SL-Mar/quantcoder): a local-first CLI
for turning quantitative research papers into draft QuantConnect LEAN
algorithms with Ollama.

> Upstream status: the original QuantCoder project says it is no longer
> maintained and explicitly warns that local LLMs may fail to implement
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

The plugin intentionally does not expose live deployment as an MCP tool.

## Local setup

QuantCoder transforms academic quant research into compilable QuantConnect LEAN algorithms using local LLMs. No cloud API keys required.

**Models (defaults):**
- **qwen2.5-coder:14b** — code generation, refinement, error fixing
- **mistral** — reasoning, summarization, chat

> **Status (Feb 2026):** v2.0.0 introduced a significant refactoring of the code generation pipeline — two-stage generation (framework stubs then mathematical core), two-pass summarization, cross-model fidelity assessment, MinerU PDF extraction, and a static QC API linter (11 rules). This refactoring is **not complete**. Testing on papers with novel mathematical models (HMM, directional changes, regime-switching) has produced disappointing results: local LLMs (14-32B) consistently fail to implement non-trivial math faithfully, substituting simple indicator proxies instead. The linter catches API-level mistakes but cannot compensate for algorithmic logic gaps. Work is ongoing. Any Ollama-compatible model can be configured via `~/.quantcoder/config.toml`.

---

## Installation

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) running locally

```bash
# Pull the required models
ollama pull qwen2.5-coder:14b
ollama pull mistral
```

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
# Check Ollama is running
curl http://localhost:11434/api/tags

# Launch QuantCoder
quantcoder
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

# Download and summarize
quantcoder download 1
quantcoder summarize 1

# Generate QuantConnect algorithm
quantcoder generate 1
quantcoder generate 1 --open-in-editor

# Validate and backtest (requires QC credentials)
quantcoder validate generated_code/algorithm_1.py
quantcoder backtest generated_code/algorithm_1.py --start 2022-01-01 --end 2024-01-01
```

### Programmatic Mode

```bash
quantcoder --prompt "Find articles about mean reversion"
```

### Autonomous Mode

```bash
quantcoder auto start --query "momentum trading" --max-iterations 50
quantcoder auto status
```

### Evolution Mode (AlphaEvolve-inspired)

```bash
quantcoder evolve start 1 --gens 3 --variants 5
quantcoder evolve start 1 --gens 3 --push-to-qc   # Push best to QC
quantcoder evolve list
quantcoder evolve export abc123
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

Configuration is stored in `~/.quantcoder/config.toml`:

```toml
[model]
provider = "ollama"
model = "qwen2.5-coder:14b"
code_model = "qwen2.5-coder:14b"
reasoning_model = "mistral"
ollama_base_url = "http://localhost:11434"
ollama_timeout = 600
temperature = 0.5
max_tokens = 3000

[ui]
theme = "monokai"
editor = "zed"
```

### QuantConnect Integration

For backtesting and deployment, set credentials in `~/.quantcoder/.env`:

```
QUANTCONNECT_API_KEY=your_key
QUANTCONNECT_USER_ID=your_id
```

### Remote Ollama

To use a remote Ollama instance:

```toml
[model]
ollama_base_url = "http://your-server:11434"
```

---

## Architecture

```
quantcoder/
├── cli.py           # CLI entry point
├── config.py        # Configuration management
├── chat.py          # Interactive chat
├── llm/             # Ollama provider layer
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

v2.0.0 is a complete rewrite — local-only inference, multi-agent architecture, evolution engine, and autonomous learning. Recent additions include a two-stage code generation pipeline (framework stubs then mathematical core), two-pass summarization, cross-model fidelity assessment, MinerU-based PDF extraction with LaTeX equation preservation, and a static QC API linter with 11 auto-fix rules. Despite these improvements, generation quality for papers with novel mathematical models remains limited by local LLM capabilities at the 14-32B parameter range.

---

## License

Apache License 2.0. See [LICENSE](LICENSE).
