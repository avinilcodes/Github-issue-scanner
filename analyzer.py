import os
import openai
from typing import List, Dict

openai.api_key = os.getenv('OPENAI_API_KEY')

MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')


def _prepare_issues_text(issues: List[Dict], max_issues=30, per_body_limit=2000):
    # take most recent issues up to max_issues
    selected = issues[:max_issues]
    parts = []
    for it in selected:
        body = (it.get('body') or '')
        if len(body) > per_body_limit:
            body = body[:per_body_limit] + '(...truncated)'
        parts.append(f"- Title: {it.get('title')}\n  URL: {it.get('html_url')}\n  Created: {it.get('created_at')}\n  Body:\n{body}\n")
    return '\n'.join(parts)


def analyze_issues(repo: str, prompt: str, issues: List[Dict]) -> str:
    if openai.api_key is None:
        raise RuntimeError('OPENAI_API_KEY environment variable not set')

    issues_text = _prepare_issues_text(issues)

    system_msg = {
        'role': 'system',
        'content': 'You are an assistant that analyzes GitHub issues and provides actionable recommendations.'
    }

    user_msg = {
        'role': 'user',
        'content': f"Repo: {repo}\nUser prompt: {prompt}\n\nHere are the recent issues (most recent first):\n{issues_text}\n\nPlease provide a clear, human-readable analysis and recommendations. Be concise but thorough."
    }

    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[system_msg, user_msg],
        temperature=0.2,
        max_tokens=1500,
    )

    choices = resp.get('choices')
    if not choices:
        raise RuntimeError('No response from LLM')

    return choices[0]['message']['content'].strip()
