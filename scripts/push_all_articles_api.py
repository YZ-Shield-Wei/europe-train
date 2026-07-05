#!/usr/bin/env python3
"""
使用 GitHub API 批量推送 europe-train 所有文章文件
避免 git push 被 SIGKILL 的问题
"""

import requests
import json
import base64
import os
import hashlib
from datetime import datetime

# 配置
TOKEN = "TOKEN_REDACTED"
REPO = "raileurope/website-raileurope-cn"
BRANCH = "main"
API_BASE = f"https://api.github.com/repos/{REPO}"

# 远程路径前缀（仓库中的实际路径）
REMOTE_PREFIX = "www/europe-train"

# 缓存文件：记录已推送文件的哈希
HASH_CACHE_FILE = ".push_cache.json"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def load_hash_cache():
    """加载已推送文件的哈希缓存"""
    if os.path.exists(HASH_CACHE_FILE):
        try:
            with open(HASH_CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_hash_cache(cache):
    """保存哈希缓存"""
    with open(HASH_CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def compute_file_hash(filepath):
    """计算文件 MD5 哈希"""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

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
    
    # 加载哈希缓存
    hash_cache = load_hash_cache()
    new_cache = {}
    
    # 所有语言的文章目录
    languages = ['en', 'de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']
    
    success = True
    total = 0
    skipped = 0
    
    for lang in languages:
        articles_dir = f"{lang}/articles"
        if not os.path.exists(articles_dir):
            continue
            
        for filename in os.listdir(articles_dir):
            if not filename.endswith('.html'):
                continue
                
            local_path = os.path.join(articles_dir, filename)
            
            # 计算当前文件哈希
            current_hash = compute_file_hash(local_path)
            cache_key = f"{lang}/{filename}"
            new_cache[cache_key] = current_hash
            
            # 检查是否与缓存相同（未变更）
            if cache_key in hash_cache and hash_cache[cache_key] == current_hash:
                skipped += 1
                continue
            
            # 构建远程路径（加 www/europe-train 前缀）
            repo_path = f"{REMOTE_PREFIX}/{articles_dir}/{filename}"
            message = f"Daily update: {filename} {today}"
            
            if push_file(local_path, repo_path, message):
                total += 1
            else:
                success = False
    
    # 保存新的哈希缓存
    save_hash_cache(new_cache)
    
    print(f"\n📊 推送统计:")
    print(f"  ✅ 新推送: {total} 个文件")
    print(f"  ⏭️  跳过（未变更）: {skipped} 个文件")
    return success

if __name__ == "__main__":
    if main():
        print("✅ 所有文章已同步到 GitHub")
    else:
        print("❌ 部分文件同步失败")
        exit(1)
