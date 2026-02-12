# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the main pipeline
uv run src/main.py

# Run tests
uv run pytest tests/

# Run a single test file
uv run pytest tests/test_notifier.py

# Run classifier evaluation (requires OpenAI key)
uv run tests/eval_classifier.py
```

## Architecture

Single-pipeline script that runs on a schedule (GitHub Actions, hourly) to monitor news and send push notifications.

**Data flow:** `config.json` + env vars → `config.py` → `main.py` orchestrates: `rss.py` fetches/filters articles → `classifier.py` classifies each with LLM → `notifier.py` sends Pushover notification if triggered.

**Modules:**
- `src/config.py` — Loads `config.json` for static settings; secrets (`OPENAI_API_KEY`, `PUSHOVER_API_TOKEN`, `PUSHOVER_USER_KEYS`) come from env vars / `.env`
- `src/rss.py` — Fetches RSS feed, filters by `lookback_minutes` and `keyword_filter`. Returns `List[NewsEvent]`
- `src/classifier.py` — Uses `gpt-4.1-mini` via LangChain to classify whether `triggering_event` occurred. Returns `bool`
- `src/notifier.py` — Sends Pushover notifications; handles Pushover's 512-char URL and 1024-char message limits by following redirects and falling back to embedding the URL in the message body

**Config (`config.json`):**
- `rss_feed_url` — supports `{keyword}` interpolation
- `keyword_filter` — pre-filters RSS entries by title substring match
- `triggering_event` — natural-language description passed to LLM for classification
- `lookback_minutes` — how far back to look in the feed (default: 60)

## Environment

Requires a `.env` file (gitignored):
```
OPENAI_API_KEY=sk-...
PUSHOVER_API_TOKEN=...
PUSHOVER_USER_KEYS=key1,key2
```

## File paths

Always use paths starting from the project root (e.g. `config.json`, not `./config.json` or relative paths). The `pytest` pythonpath is set to `src/` in `pyproject.toml`, so tests import modules directly (e.g. `from notifier import ...`).
