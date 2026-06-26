---
description: Lint or compile-check a QuantConnect Python algorithm through QuantCoder
argument-hint: "<file_path> [--local-only]"
allowed-tools: Bash(cd:*), Bash(uv run quantcoder:*)
---

Validate a QuantConnect Python algorithm.

For local static linting only, run the supplied file path with `--local-only`
if the user did not already include it:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && uv run quantcoder validate <file_path> --local-only
```

For QuantConnect compile validation, omit `--local-only` and ensure
`QUANTCONNECT_API_KEY` and `QUANTCONNECT_USER_ID` are set:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && uv run quantcoder validate <file_path>
```

Report compile errors separately from strategy/research concerns.
