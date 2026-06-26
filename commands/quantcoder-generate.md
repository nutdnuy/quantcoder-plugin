---
description: Generate a QuantConnect LEAN draft from a QuantCoder summary ID
argument-hint: "<summary_id> [--backtest] [--max-attempts N]"
allowed-tools: Bash(cd:*), Bash(uv run quantcoder:*)
---

Generate QuantConnect code from a QuantCoder summary ID.

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && uv run quantcoder generate $ARGUMENTS
```

After generation, inspect the output file, summarize the strategy logic, and
flag any places where the generated code may not faithfully implement the paper
or may contain data leakage.
