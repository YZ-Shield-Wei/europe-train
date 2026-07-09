#!/usr/bin/env python3
"""
使用 GitHub API 推送 europe-train 文章文件
避免 git push 被 SIGKILL 的问题
"""

import requests
import json
import base64
import os
from datetime import datetime

# 配置 - 从环境变量或本地文件读取 Token
TOKEN = os.environ.get("GITHUB_TOKEN_EUROPE_TRAIN", "")

# 如果环境变量未设置，尝试读取本地文件
if not TOKEN:
    try:
        with open(".github_token", "r") as f:
            TOKEN = f.read().strip()
    except:
        pass

REPO = "YZ-Shield-Wei/europe-train"
BRANCH = "main"
API_BASE = f"https://api.github.com/repos/{REPO}"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_file_sha(path):
    """获取文件当前 SHA（如果不存在返回 None）"""
    url = f"{API_BASE}/contents/{path}?ref={BRANCH}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json().get("sha")
    return None

def push_file(local_path, repo_path, message):
    """推送单个文件到 GitHub"""
    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    
    sha = get_file_sha(repo_path)
    
    data = {
        "message": message,
        "content": content,
        "branch": BRANCH
    }
    if sha:
        data["sha"] = sha
    
    url = f"{API_BASE}/contents/{repo_path}"
    resp = requests.put(url, headers=headers, json=data)
    
    if resp.status_code in (200, 201):
        print(f"✅ 已推送: {repo_path}")
        return True
    else:
        print(f"❌ 推送失败 {repo_path}: {resp.status_code} - {resp.text[:200]}")
        return False

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 检查 Token 是否配置
    if not TOKEN:
        print("❌ GITHUB_TOKEN_EUROPE_TRAIN 环境变量未设置，且 .github_token 文件不存在")
        return False
    
    # 只推送手动写的完整文章
    files_to_push = [
        ("en/articles/how-to-buy-european-train-tickets.html", "en/articles/how-to-buy-european-train-tickets.html", f"feat: add complete guide to buying European train tickets {today}"),
    ]
    
    success = True
    for local_path, repo_path, message in files_to_push:
        if os.path.exists(local_path):
            if not push_file(local_path, repo_path, message):
                success = False
        else:
            print(f"⚠️ 文件不存在: {local_path}")
            success = False
    
    return success

if __name__ == "__main__":
    if main():
        print("✅ 文章已同步到 GitHub")
    else:
        print("❌ 部分文件同步失败")
        exit(1)
