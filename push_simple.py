#!/usr/bin/env python3
"""
使用GitHub API推送commit - 简化版
"""

import requests
import subprocess

GITHUB_TOKEN = open('/root/.openclaw/workspace/.github_token_europe_train').read().strip()
REPO = "YZ-Shield-Wei/europe-train"

def get_local_commit_sha():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()

def get_remote_commit_sha():
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(f'https://api.github.com/repos/{REPO}/git/ref/heads/main', headers=headers)
    return response.json()['object']['sha']

def create_blob(content):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {'content': content, 'encoding': 'utf-8'}
    response = requests.post(f'https://api.github.com/repos/{REPO}/git/blobs', headers=headers, json=data)
    result = response.json()
    if 'sha' not in result:
        print(f"  ✗ Blob创建失败: {result.get('message', 'Unknown error')}")
        return None
    return result['sha']

def create_tree(base_tree_sha, files_to_update):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    tree = []
    for filepath, content in files_to_update.items():
        blob_sha = create_blob(content)
        if blob_sha:
            tree.append({
                "path": filepath,
                "mode": "100644",
                "type": "blob",
                "sha": blob_sha
            })
    
    data = {
        "base_tree": base_tree_sha,
        "tree": tree
    }
    response = requests.post(f'https://api.github.com/repos/{REPO}/git/trees', headers=headers, json=data)
    result = response.json()
    if 'sha' not in result:
        print(f"  ✗ Tree创建失败: {result.get('message', 'Unknown error')}")
        return None
    return result['sha']

def create_commit(tree_sha, parent_sha, message):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        "message": message,
        "tree": tree_sha,
        "parents": [parent_sha]
    }
    response = requests.post(f'https://api.github.com/repos/{REPO}/git/commits', headers=headers, json=data)
    result = response.json()
    if 'sha' not in result:
        print(f"  ✗ Commit创建失败: {result.get('message', 'Unknown error')}")
        return None
    return result['sha']

def update_ref(commit_sha):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {'sha': commit_sha, 'force': True}
    response = requests.patch(f'https://api.github.com/repos/{REPO}/git/refs/heads/main', headers=headers, json=data)
    return response.status_code == 200

def main():
    print("🚀 使用GitHub API推送...")
    
    local_sha = get_local_commit_sha()
    remote_sha = get_remote_commit_sha()
    
    print(f"Local: {local_sha}")
    print(f"Remote: {remote_sha}")
    
    if local_sha == remote_sha:
        print("Already up to date")
        return
    
    # 获取本地commit信息
    commit_info = subprocess.check_output(['git', 'cat-file', '-p', local_sha]).decode()
    lines = commit_info.split('\n')
    message = lines[4] if len(lines) > 4 else "Update"
    
    # 获取tree SHA
    tree_sha = subprocess.check_output(['git', 'rev-parse', f'{local_sha}^{{tree}}']).decode().strip()
    print(f"Tree SHA: {tree_sha}")
    
    # 获取修改的文件列表（使用git status）
    result = subprocess.check_output(['git', 'status', '--short']).decode().strip()
    files_changed = []
    for line in result.split('\n'):
        if line:
            # 解析 git status 输出
            filepath = line[3:].strip()
            if filepath:
                files_changed.append(filepath)
    
    print(f"Files changed: {len(files_changed)}")
    
    # 读取修改的文件内容
    files_to_update = {}
    for filepath in files_changed:
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                files_to_update[filepath] = content
                print(f"  ✓ {filepath} ({len(content)} chars)")
            except Exception as e:
                print(f"  ✗ 读取 {filepath} 失败: {e}")
    
    print(f"\nFiles to update: {len(files_to_update)}")
    
    # 创建新tree
    new_tree_sha = create_tree(remote_sha, files_to_update)
    if not new_tree_sha:
        print("✗ Tree创建失败，退出")
        return
    print(f"New tree SHA: {new_tree_sha}")
    
    # 创建commit
    new_commit_sha = create_commit(new_tree_sha, remote_sha, message)
    if not new_commit_sha:
        print("✗ Commit创建失败，退出")
        return
    print(f"New commit SHA: {new_commit_sha}")
    
    # 更新引用
    if update_ref(new_commit_sha):
        print("✅ 推送成功")
    else:
        print("✗ 推送失败")

if __name__ == '__main__':
    main()
