#!/usr/bin/env python3
"""
gh_repo_metadata.py — JSON minimalista para LLMs.
"""

import json
import os
import sys
import time

import httpx
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    sys.exit("❌ Falta GITHUB_TOKEN")

client = httpx.Client(
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
    },
    timeout=30,
)


def fetch_all_repos() -> list[dict]:
    """Brings all repos for the authenticated user, paginated."""
    repos = []
    page = 1

    while True:
        resp = client.get(
            "https://api.github.com/user/repos",
            params={
                "per_page": 100,
                "page": page,
                "affiliation": "owner,collaborator,organization_member",
            },
        )

        if resp.status_code == 403 and resp.headers.get("X-RateLimit-Remaining") == "0":
            reset = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            time.sleep(max(reset - int(time.time()), 1))
            continue

        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break

        repos.extend(batch)
        print(f"📦 {len(repos)} repos...", file=sys.stderr)
        page += 1

    client.close()
    return repos


def slim(repo: dict) -> dict:
    """stuff the LLM cares about, and nothing else."""
    return {
        "name": repo["full_name"],
        "private": repo["private"],
        "desc": repo["description"],
        "lang": repo["language"],
        "stars": repo["stargazers_count"],
        "updated": repo["updated_at"][:10],
        "archived": repo["archived"],
        "tags": repo.get("topics", []),
    }


if __name__ == "__main__":
    repos = [slim(r) for r in fetch_all_repos()]
    with open("repos.json", "w", encoding="utf-8") as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)
