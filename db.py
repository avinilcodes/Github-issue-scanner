import sqlite3
import os
from typing import List, Dict

DB_PATH = os.path.join(os.path.dirname(__file__), 'issues.db')


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            repo TEXT,
            issue_id INTEGER,
            title TEXT,
            body TEXT,
            html_url TEXT,
            created_at TEXT,
            PRIMARY KEY (repo, issue_id)
        )
    ''')
    conn.commit()
    conn.close()


def save_issues(repo: str, issues: List[Dict]) -> bool:
    conn = get_conn()
    c = conn.cursor()
    try:
        for it in issues:
            c.execute(
                'REPLACE INTO issues (repo, issue_id, title, body, html_url, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                (repo, it.get('id'), it.get('title'), it.get('body'), it.get('html_url'), it.get('created_at'))
            )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()


def get_issues(repo: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT issue_id as id, title, body, html_url, created_at FROM issues WHERE repo = ? ORDER BY created_at DESC', (repo,))
    rows = c.fetchall()
    conn.close()
    if rows is None:
        return None
    return [dict(r) for r in rows]
