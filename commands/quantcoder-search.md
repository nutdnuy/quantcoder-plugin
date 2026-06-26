---
description: Search for quantitative research papers with QuantCoder
argument-hint: "<query> [--deep] [--num N]"
allowed-tools: Bash(cd:*), Bash(uv run quantcoder:*)
---

Search for research papers using QuantCoder.

Use `$ARGUMENTS` as the search query and options. Prefer arXiv search unless the
user explicitly asks for semantic/deep search and has `TAVILY_API_KEY` set.

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && uv run quantcoder search $ARGUMENTS
```

Return the paper IDs, titles, and any important caveats about source quality.
