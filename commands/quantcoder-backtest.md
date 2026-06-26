---
description: Run a QuantConnect backtest for a generated algorithm
argument-hint: "<file_path> --start YYYY-MM-DD --end YYYY-MM-DD [--name NAME]"
allowed-tools: Bash(cd:*), Bash(uv run quantcoder:*)
---

Run a QuantConnect backtest through QuantCoder.

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && uv run quantcoder backtest $ARGUMENTS
```

Report the metrics as research evidence only. Explicitly call out remaining
checks: out-of-sample validation, transaction costs, slippage, data leakage,
portfolio constraints, and robustness across regimes.
