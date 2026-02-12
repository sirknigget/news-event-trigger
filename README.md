# News Event Trigger

A scheduled Python script that monitors news via RSS, filters by keyword, classifies using an LLM (gpt-4o-mini), and notifies via Pushover.

## Setup

1.  **Install uv** (if not already installed):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Environment Variables**:
    Create a `.env` file in the root directory:
    ```
    OPENAI_API_KEY=sk-...
    PUSHOVER_API_TOKEN=...
    ```

3.  **Configuration**:
    Edit `config.json` to set your RSS feed, keywords, and Pushover user keys.

## Running Locally

Run the main script:
```bash
uv run src/main.py
```

Run the classifier evaluation (requires OpenAI key):
```bash
uv run tests/eval_classifier.py
```

## GitHub Actions

The workflow is defined in `.github/workflows/main.yml`.
You must set the following **Repository Secrets** in GitHub:
- `OPENAI_API_KEY`
- `PUSHOVER_API_TOKEN`

The script is scheduled to run every hour.
