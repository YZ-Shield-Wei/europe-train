#!/usr/bin/env python3
"""
深度排查 Search Console 问题
检查 redirect、canonical、404 的具体原因
"""

import os
import re
from pathlib import Path
import json

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

def find_redirect_issues():
    """查找可能导致 redirect 的问题"""
    issues = []
    
    # 1. 检查根目录下的旧文章是否有重定向
    root_articles = BASE_DIR / "articles"
    if root_articles.exists():
        for html_file in root_articles.glob("*.html"):
            content = html_file.read_text()
            # 检查是否有重定向代码
            if 'http-equiv="refresh"' in content or 'window.location' in content or 'window.location.href' in content:
                issues.append(f"articles/{html_file.name}: 包含重定向代码")
    
    # 2. 检查是否有重复的页面（多语言冲突）
    # 例如 /en/articles/xxx.html 和 /articles/xxx.html 同时存在
    en_articles = BASE_DIR / "en" / "articles"
    root_articles = BASE_DIR / "articles"
    
    if en_articles.exists() and root_articles.exists():
        for root_file in root_articles.glob("*.html"):
            en_file = en_articles / root_file.name
            if en_file.exists():
                issues.append(f"重复页面: articles/{root_file.name} 和 en/articles/{root_file.name}")
    
    # 3. 检查链接是否指向旧路径
    for html_file in BASE_DIR.rglob("*.html"):
        if 'build' in str(html_file) or 'content' in str(html_file):
            continue
        
        content = html_file.read_text()
        # 检查是否有指向 /articles/ 但不带语言前缀的链接（在语言子站点中）
        rel_path = html_file.relative_to(BASE_DIR)
        
        # 如果在语言子站点中，检查是否链接到 /articles/ 而非 /en/articles/
        if str(rel_path).startswith(('de/', 'fr/', 'es/', 'ja/', 'ko/', 'pt/', 'zh/')):
            bad_links = re.findall(r'href=["\'](/articles/[^"\']+)["\']', content)
            if bad_links:
                issues.append(f"{rel_path}: 链接到旧路径 {bad_links}")
    
    return issues

def find_canonical_issues():
    """查找 canonical 标签问题"""
    issues = []
    
    # 检查所有页面的 canonical 标签
    languages = ['en', 'de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']
    
    for lang in languages:
        articles_dir = BASE_DIR / lang / 'articles'
        if not articles_dir.exists():
            continue
        
        for html_file in articles_dir.glob("*.html"):
            if html_file.name == 'index.html':
                continue
            
            content = html_file.read_text()
            
            # 检查是否有 canonical
            canonical_match = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*>', content)
            if not canonical_match:
                issues.append(f"{lang}/articles/{html_file.name}: 缺少 canonical 标签")
                continue
            
            # 检查 canonical 是否指向正确的 URL
            canonical_url = re.search(r'href=["\']([^"\']+)["\']', canonical_match.group())
            if canonical_url:
                url = canonical_url.group(1)
                expected = f"https://www.europe-train.com/{lang}/articles/{html_file.name}"
                if url != expected:
                    issues.append(f"{lang}/articles/{html_file.name}: canonical 指向错误 URL\n  当前: {url}\n  应为: {expected}")
    
    return issues

def find_404_issues():
    """查找可能导致 404 的问题"""
    issues = []
    
    # 1. 检查 sitemap 中的 URL 是否都存在
    sitemap_file = BASE_DIR / "sitemap.xml"
    if sitemap_file.exists():
        content = sitemap_file.read_text()
        urls = re.findall(r'<loc>https://www\.europe-train\.com/([^<]+)</loc>', content)
        
        missing = []
        for url_path in urls:
            # 转换为文件路径
            file_path = BASE_DIR / url_path
            index_path = file_path / "index.html"
            
            if not file_path.exists() and not index_path.exists():
                # 检查是否是语言子站点
                parts = url_path.strip('/').split('/')
                if len(parts) >= 2 and parts[0] in ['de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']:
                    missing.append(url_path)
                elif len(parts) == 1 and parts[0].endswith('.html'):
                    missing.append(url_path)
        
        if missing:
            issues.append(f"Sitemap 中有 {len(missing)} 个 URL 缺少对应文件:")
            for m in missing[:10]:
                issues.append(f"  - {m}")
    
    # 2. 检查内部链接是否指向不存在的页面
    all_files = set()
    for html_file in BASE_DIR.rglob("*.html"):
        if 'build' in str(html_file) or 'content' in str(html_file):
            continue
        rel = str(html_file.relative_to(BASE_DIR))
        all_files.add(rel)
    
    # 检查各页面的链接
    for html_file in BASE_DIR.rglob("*.html"):
        if 'build' in str(html_file) or 'content' in str(html_file):
            continue
        
        content = html_file.read_text()
        links = re.findall(r'href=["\'](/[^"\']+\.html)["\']', content)
        
        for link in links:
            # 去掉开头的 /
            link_path = link.lstrip('/')
            # 检查是否存在
            if link_path not in all_files and link_path + '/index.html' not in all_files:
                # 可能是外部链接或语言子站点
                if not link.startswith('http') and not link.startswith('//'):
                    issues.append(f"{html_file.relative_to(BASE_DIR)}: 链接到不存在的页面 {link}")
    
    return issues

def find_indexing_issues():
    """查找可能导致不被索引的问题"""
    issues = []
    
    # 检查是否有 noindex 标签
    for html_file in BASE_DIR.rglob("*.html"):
        if 'build' in str(html_file) or 'content' in str(html_file):
            continue
        
        content = html_file.read_text()
        if 'noindex' in content:
            issues.append(f"{html_file.relative_to(BASE_DIR)}: 包含 noindex 标签")
    
    # 检查页面质量（内容长度）
    short_pages = []
    for html_file in BASE_DIR.rglob("*.html"):
        if 'build' in str(html_file) or 'content' in str(html_file):
            continue
        
        content = html_file.read_text()
        # 提取 body 内容
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
        if body_match:
            body_text = re.sub(r'<[^>]+>', '', body_match.group(1))
            body_text = re.sub(r'\s+', ' ', body_text).strip()
            
            if len(body_text) < 200:  # 内容少于200字符
                short_pages.append(f"{html_file.relative_to(BASE_DIR)}: 内容仅 {len(body_text)} 字符")
    
    if short_pages:
        issues.append(f"发现 {len(short_pages)} 个内容过短的页面:")
        issues.extend(short_pages[:10])
    
    return issues

def main():
    print("=" * 60)
    print("🔍 Search Console 深度问题排查")
    print("=" * 60)
    
    # 1. Redirect 问题
    print("\n🔄 1. Redirect 问题排查")
    redirect_issues = find_redirect_issues()
    if redirect_issues:
        print(f"   发现 {len(redirect_issues)} 个问题:")
        for issue in redirect_issues[:20]:
            print(f"   ⚠️  {issue}")
    else:
        print("   ✅ 未发现 redirect 问题")
    
    # 2. Canonical 问题
    print("\n🔗 2. Canonical 标签排查")
    canonical_issues = find_canonical_issues()
    if canonical_issues:
        print(f"   发现 {len(canonical_issues)} 个问题:")
        for issue in canonical_issues[:20]:
            print(f"   ⚠️  {issue}")
    else:
        print("   ✅ 未发现 canonical 问题")
    
    # 3. 404 问题
    print("\n❌ 3. 404 问题排查")
    notfound_issues = find_404_issues()
    if notfound_issues:
        print(f"   发现 {len(notfound_issues)} 个问题:")
        for issue in notfound_issues[:20]:
            print(f"   ⚠️  {issue}")
    else:
        print("   ✅ 未发现 404 问题")
    
    # 4. 索引问题
    print("\n📄 4. 索引问题排查")
    indexing_issues = find_indexing_issues()
    if indexing_issues:
        print(f"   发现 {len(indexing_issues)} 个问题:")
        for issue in indexing_issues[:20]:
            print(f"   ⚠️  {issue}")
    else:
        print("   ✅ 未发现索引问题")
    
    print("\n" + "=" * 60)
    print("✅ 排查完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
