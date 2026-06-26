---
description: Check local QuantCoder, Ollama, and optional QuantConnect setup
argument-hint: ""
allowed-tools: Bash(cd:*), Bash(uv:*), Bash(quantcoder:*), Bash(curl:*)
---

Check the plugin-local QuantCoder setup.

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && uv run quantcoder --help
curl http://localhost:11434/api/tags
```

Then report whether Ollama is reachable, whether `qwen2.5-coder:14b` and
`mistral` are available, and whether the user still needs to set
`QUANTCONNECT_API_KEY` and `QUANTCONNECT_USER_ID` for validation/backtesting.
