import os
import requests

GITHUB_API = "https://api.github.com"


def fetch_issues(repo: str):
    if '/' not in repo:
        raise ValueError('repo must be in owner/name format')
    owner, name = repo.split('/', 1)

    token = os.getenv('GITHUB_TOKEN')
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'

    issues = []
    page = 1
    per_page = 100
    while True:
        url = f"{GITHUB_API}/repos/{owner}/{name}/issues"
        params = {"state": "open", "per_page": per_page, "page": page}
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        if resp.status_code == 404:
            raise ValueError('Repository not found')
        resp.raise_for_status()
        page_items = resp.json()
        if not page_items:
            break

        # Filter out pull requests (they have a `pull_request` key)
        for it in page_items:
            if 'pull_request' in it:
                continue
            issues.append({
                'id': it.get('id'),
                'title': it.get('title') or '',
                'body': it.get('body') or '',
                'html_url': it.get('html_url'),
                'created_at': it.get('created_at'),
            })

        if len(page_items) < per_page:
            break
        page += 1

    return issues
