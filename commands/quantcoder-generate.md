---
description: Generate a QuantConnect LEAN draft with Claude Code or Codex Agent
argument-hint: "<paper_or_summary_path> [output_path]"
allowed-tools: Bash(cd:*), Bash(uv run quantcoder:*), Bash(uv run python:*)
---

Generate QuantConnect code with the active Claude Code / Codex agent.

Use `$ARGUMENTS` as the source paper/summary path and optional output path.

Agent workflow:

1. Read the paper or summary.
2. Extract the strategy hypothesis, universe, signal formula, rebalance cadence,
   risk controls, data assumptions, and paper equations.
3. Write a QuantConnect LEAN Python draft directly.
4. Run local validation/linting with:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && uv run quantcoder validate <output_path> --local-only
```

5. Summarize the strategy logic and flag paper-to-code assumptions, possible
   data leakage, transaction-cost omissions, and math-fidelity risks.
