#!/usr/bin/env python3
"""
批量推送 europe-train 文章到 GitHub API
避免 git push SIGKILL 问题
"""

import requests
import base64
import os
import sys

TOKEN = "TOKEN_REDACTED"
REPO = "YZ-Shield-Wei/europe-train"
BRANCH = "main"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_sha(path):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}?ref={BRANCH}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json().get("sha")
    return None

def push_file(local_path, repo_path, message):
    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    
    sha = get_sha(repo_path)
    data = {
        "message": message,
        "content": content,
        "branch": BRANCH
    }
    if sha:
        data["sha"] = sha
    
    url = f"https://api.github.com/repos/{REPO}/contents/{repo_path}"
    resp = requests.put(url, headers=headers, json=data)
    
    if resp.status_code in (200, 201):
        print(f"✅ {repo_path}")
        return True
    else:
        print(f"❌ {repo_path}: {resp.status_code}")
        return False

def main():
    files = [
        # 新文章 - 所有语言
        ("en/articles/how-to-buy-european-train-tickets.html", "en/articles/how-to-buy-european-train-tickets.html", "feat: add how to buy European train tickets guide (EN)"),
        ("de/articles/how-to-buy-european-train-tickets.html", "de/articles/how-to-buy-european-train-tickets.html", "feat: add how to buy European train tickets guide (DE)"),
        ("fr/articles/how-to-buy-european-train-tickets.html", "fr/articles/how-to-buy-european-train-tickets.html", "feat: add how to buy European train tickets guide (FR)"),
        ("es/articles/how-to-buy-european-train-tickets.html", "es/articles/how-to-buy-european-train-tickets.html", "feat: add how to buy European train tickets guide (ES)"),
        ("ja/articles/how-to-buy-european-train-tickets.html", "ja/articles/how-to-buy-european-train-tickets.html", "feat: add how to buy European train tickets guide (JA)"),
        ("ko/articles/how-to-buy-european-train-tickets.html", "ko/articles/how-to-buy-european-train-tickets.html", "feat: add how to buy European train tickets guide (KO)"),
        ("pt/articles/how-to-buy-european-train-tickets.html", "pt/articles/how-to-buy-european-train-tickets.html", "feat: add how to buy European train tickets guide (PT)"),
        ("zh/articles/how-to-buy-european-train-tickets.html", "zh/articles/how-to-buy-european-train-tickets.html", "feat: add how to buy European train tickets guide (ZH)"),
        # 更新索引
        ("en/articles/index.html", "en/articles/index.html", "update: add new article to index"),
    ]
    
    success = 0
    for local, repo, msg in files:
        if os.path.exists(local):
            if push_file(local, repo, msg):
                success += 1
        else:
            print(f"⚠️ Missing: {local}")
    
    print(f"\n✅ Pushed {success}/{len(files)} files")

if __name__ == "__main__":
    main()
