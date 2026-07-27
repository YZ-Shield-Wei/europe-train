#!/usr/bin/env python3
"""
批量修复 Search Console 问题
优先级：Canonical > 404 > 重复页面 > 内容过短
"""

import os
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

def fix_canonical_tags():
    """修复所有页面的 canonical 标签"""
    fixed = 0
    languages = ['en', 'de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']
    
    for lang in languages:
        articles_dir = BASE_DIR / lang / 'articles'
        if not articles_dir.exists():
            continue
        
        for html_file in articles_dir.glob("*.html"):
            if html_file.name == 'index.html':
                continue
            
            content = html_file.read_text()
            original = content
            
            # 计算正确的 canonical URL
            correct_url = f"https://www.europe-train.com/{lang}/articles/{html_file.name}"
            
            # 替换错误的 canonical
            # 匹配各种格式的 canonical
            content = re.sub(
                r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'][^"\']+["\'][^>]*/?>',
                f'<link rel="canonical" href="{correct_url}" />',
                content
            )
            
            # 也尝试匹配 href 在 rel 前面的格式
            content = re.sub(
                r'<link[^>]*href=["\'][^"\']+["\'][^>]*rel=["\']canonical["\'][^>]*/?>',
                f'<link rel="canonical" href="{correct_url}" />',
                content
            )
            
            if content != original:
                html_file.write_text(content)
                fixed += 1
    
    # 也修复根目录 articles 下的 canonical
    root_articles = BASE_DIR / 'articles'
    if root_articles.exists():
        for html_file in root_articles.glob("*.html"):
            content = html_file.read_text()
            original = content
            
            correct_url = f"https://www.europe-train.com/articles/{html_file.name}"
            
            content = re.sub(
                r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'][^"\']+["\'][^>]*/?>',
                f'<link rel="canonical" href="{correct_url}" />',
                content
            )
            content = re.sub(
                r'<link[^>]*href=["\'][^"\']+["\'][^>]*rel=["\']canonical["\'][^>]*/?>',
                f'<link rel="canonical" href="{correct_url}" />',
                content
            )
            
            if content != original:
                html_file.write_text(content)
                fixed += 1
    
    return fixed

def fix_live_status_links():
    """修复 live-status.html 中的模板变量链接"""
    fixed = 0
    languages = ['', 'en', 'de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']
    
    for lang in languages:
        if lang:
            live_status = BASE_DIR / lang / 'live-status.html'
        else:
            live_status = BASE_DIR / 'live-status.html'
        
        if not live_status.exists():
            continue
        
        content = live_status.read_text()
        original = content
        
        # 修复模板变量链接
        # 将 /disruption/${d.id}.html 改为 /disruption/placeholder.html
        # 或者删除这些链接（因为它们是动态生成的）
        content = content.replace('/disruption/${d.id}.html', '/live-status.html')
        content = content.replace('/disruption/${disruption.id}.html', '/live-status.html')
        
        if content != original:
            live_status.write_text(content)
            fixed += 1
    
    return fixed

def fix_homepage_links():
    """修复首页中不存在的文章链接"""
    fixed = 0
    
    # 获取所有存在的文章
    existing_articles = set()
    for lang in ['en', 'de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']:
        articles_dir = BASE_DIR / lang / 'articles'
        if articles_dir.exists():
            for f in articles_dir.glob('*.html'):
                existing_articles.add(f.name)
    
    # 也检查根目录 articles
    root_articles = BASE_DIR / 'articles'
    if root_articles.exists():
        for f in root_articles.glob('*.html'):
            existing_articles.add(f.name)
    
    # 修复首页
    homepage = BASE_DIR / 'index.html'
    if homepage.exists():
        content = homepage.read_text()
        original = content
        
        # 查找所有 /articles/xxx.html 链接
        links = re.findall(r'href=["\'](/articles/([^"\']+\.html))["\']', content)
        
        for full_link, filename in links:
            if filename not in existing_articles:
                # 替换为存在的文章链接或删除
                # 先尝试找到同名文件
                content = content.replace(f'href="{full_link}"', 'href="/en/articles/how-to-buy-european-train-tickets.html"')
        
        if content != original:
            homepage.write_text(content)
            fixed += 1
    
    return fixed

def remove_duplicate_root_articles():
    """删除根目录 articles/ 下与 en/articles/ 重复的文件"""
    removed = 0
    
    root_articles = BASE_DIR / 'articles'
    en_articles = BASE_DIR / 'en' / 'articles'
    
    if not root_articles.exists() or not en_articles.exists():
        return removed
    
    for root_file in root_articles.glob('*.html'):
        en_file = en_articles / root_file.name
        if en_file.exists():
            # 检查根目录文件是否是重定向页面
            content = root_file.read_text()
            
            # 如果是重定向页面，删除它
            if 'http-equiv="refresh"' in content or 'window.location' in content:
                root_file.unlink()
                removed += 1
                print(f"   删除重定向页面: articles/{root_file.name}")
            else:
                # 如果不是重定向，也删除（因为内容重复）
                root_file.unlink()
                removed += 1
                print(f"   删除重复页面: articles/{root_file.name}")
    
    return removed

def fix_old_articles_links():
    """修复旧 articles 页面中的链接"""
    fixed = 0
    
    root_articles = BASE_DIR / 'articles'
    if not root_articles.exists():
        return fixed
    
    for html_file in root_articles.glob('*.html'):
        content = html_file.read_text()
        original = content
        
        # 修复指向 /en/articles/tag-xxx.html 的链接
        # 这些 tag 页面不存在，改为指向 /en/articles/
        content = re.sub(
            r'href=["\'](/en/articles/tag-[^"\']+)["\']',
            'href="/en/articles/"',
            content
        )
        
        if content != original:
            html_file.write_text(content)
            fixed += 1
    
    return fixed

def fix_language_article_links():
    """修复语言子站点文章中的旧路径链接"""
    fixed = 0
    languages = ['de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']
    
    for lang in languages:
        articles_dir = BASE_DIR / lang / 'articles'
        if not articles_dir.exists():
            continue
        
        for html_file in articles_dir.glob("*.html"):
            if html_file.name == 'index.html':
                continue
            
            content = html_file.read_text()
            original = content
            
            # 修复指向 /articles/xxx.html 的链接（应改为 /{lang}/articles/xxx.html）
            content = re.sub(
                r'href=["\'](/articles/([^"\']+\.html))["\']',
                f'href="/{lang}/articles/\\2"',
                content
            )
            
            if content != original:
                html_file.write_text(content)
                fixed += 1
    
    return fixed

def main():
    print("=" * 60)
    print("🔧 批量修复 Search Console 问题")
    print("=" * 60)
    
    # P0: 修复 canonical 标签
    print("\n🔗 P0: 修复 Canonical 标签")
    canonical_fixed = fix_canonical_tags()
    print(f"   ✅ 已修复 {canonical_fixed} 个页面的 canonical")
    
    # P1: 修复 live-status 模板变量
    print("\n🌐 P1: 修复 Live Status 链接")
    livestatus_fixed = fix_live_status_links()
    print(f"   ✅ 已修复 {livestatus_fixed} 个 live-status 页面")
    
    # P1: 修复首页链接
    print("\n🏠 P1: 修复首页链接")
    homepage_fixed = fix_homepage_links()
    print(f"   ✅ 已修复首页链接")
    
    # P1: 修复旧 articles 链接
    print("\n📄 P1: 修复旧 Articles 链接")
    old_fixed = fix_old_articles_links()
    print(f"   ✅ 已修复 {old_fixed} 个旧 articles 页面")
    
    # P1: 修复语言子站点链接
    print("\n🌍 P1: 修复语言子站点链接")
    lang_fixed = fix_language_article_links()
    print(f"   ✅ 已修复 {lang_fixed} 个语言子站点页面")
    
    # P2: 删除重复页面
    print("\n🗑️  P2: 删除重复页面")
    removed = remove_duplicate_root_articles()
    print(f"   ✅ 已删除 {removed} 个重复页面")
    
    print("\n" + "=" * 60)
    print("✅ 修复完成")
    print("=" * 60)
    print(f"\n📊 修复统计:")
    print(f"   Canonical 修复: {canonical_fixed}")
    print(f"   Live Status 修复: {livestatus_fixed}")
    print(f"   首页链接修复: {homepage_fixed}")
    print(f"   旧 Articles 修复: {old_fixed}")
    print(f"   语言子站点修复: {lang_fixed}")
    print(f"   重复页面删除: {removed}")

if __name__ == "__main__":
    main()
