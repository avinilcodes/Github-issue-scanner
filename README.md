# GitHub Issue Scanner and Analyzer

This small service provides two endpoints:

- `POST /scan` — fetches open issues for a GitHub repository and caches them locally (SQLite).
- `POST /analyze` — retrieves cached issues and sends them, together with a user prompt, to an LLM for natural-language analysis.

Why SQLite

- Durable across restarts and easy to set up without external services.
- Simple SQL storage makes inspecting cached issues straightforward (`issues.db`).

Requirements

- Python 3.10+
- Set `OPENAI_API_KEY` in your environment. Optionally set `OPENAI_MODEL`.
- Optionally set `GITHUB_TOKEN` to increase GitHub API rate limits.

Install

```powershell
python -m pip install -r requirements.txt
```

Run

```powershell
uvicorn main:app --reload
```

Endpoints

- POST /scan

  Request body:

  ```json
  { "repo": "owner/repo" }
  ```

  Response example:

  ```json
  { "repo": "owner/repo", "issues_fetched": 42, "cached_successfully": true }
  ```

- POST /analyze

  Request body:

  ```json
  { "repo": "owner/repo", "prompt": "Find themes across recent issues and recommend what to fix first" }
  ```

  Response example:

  ```json
  { "analysis": "<LLM-generated text>" }
  ```

Prompts used

- Prompts sent to AI coding tools while building:
  - Create a FASTAPI/python boilerplate code to create to endpoints Endpoint: POST /scan
    request
    ```json
    { "repo": "owner/repository-name"}
    ```
    respose
    ```json
    {"repo": "owner/repository-name", "issues_fetched": 42, "cached_successfully": true }
    ```
   Endpoint: POST /analyze
    request 
    ```json
    {  "repo": "owner/repository-name",
      "prompt": "Find themes across recent issues and recommend what the maintainers should fix first"}
```
response
```json
{
  "analysis": "<LLM-generated text here>"
}.
```

  - Create DB for caching issue those will be used in analyze endpoint while answering their questions
  - Write a README for above endpoints.


Notes

- This is intentionally minimal and focused on the backend. The server uses SQLite so cached data persists across restarts.
- The analyzer truncates long issue bodies and limits the number of issues sent to the LLM to keep requests within model context limits.
