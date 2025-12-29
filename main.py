from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from github_client import fetch_issues
from db import init_db, save_issues, get_issues
from analyzer import analyze_issues
import uvicorn

app = FastAPI()

init_db()


class ScanRequest(BaseModel):
    repo: str


class AnalyzeRequest(BaseModel):
    repo: str
    prompt: str


@app.post('/scan')
def scan(req: ScanRequest):
    repo = req.repo.strip()
    try:
        issues = fetch_issues(repo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    saved = save_issues(repo, issues)
    return {
        "repo": repo,
        "issues_fetched": len(issues),
        "cached_successfully": saved,
    }


@app.post('/analyze')
def analyze(req: AnalyzeRequest):
    repo = req.repo.strip()
    issues = get_issues(repo)
    if issues is None:
        raise HTTPException(status_code=404, detail="Repository not scanned yet. Run /scan first.")
    if len(issues) == 0:
        raise HTTPException(status_code=400, detail="No issues cached for this repository.")

    try:
        result = analyze_issues(repo, req.prompt, issues)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {e}")

    return {"analysis": result}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
