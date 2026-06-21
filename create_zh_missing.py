#!/usr/bin/env python3
"""
批量创建 zh 站点缺失的文件
基于 en 版本，添加中文翻译
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

# 需要创建的文件列表
GUIDES_FILES = [
    'popular-routes.html',
    'rail-pass-guide.html', 
    'ticket-buying-guide.html',
    'train-experience-guide.html'
]

ARTICLES_FILES = [
    'delay-compensation-guide.html',
    'europe-train-ticket-rules.html',
    'france-tgv-guide.html',
    'germany-ice-guide.html',
    'london-paris-eurostar-guide.html',
    'paris-zurich-train-vs-flight.html',
    'spain-ave-guide.html',
    'swiss-scenic-trains.html',
    'tgv-lyria-experience.html',
    'train-station-guide.html'
]

# 简单的中文翻译映射
ZH_TRANSLATIONS = {
    'Travel Guides': '旅行指南',
    'Popular Routes': '热门路线',
    'Tickets': '火车票',
    'Passes': '通票',
    'Live Status': '实时状态',
    'How to Buy European Train Tickets': '如何购买欧洲火车票',
    'Complete Guide': '完整指南',
    'Related Guides': '相关指南',
    'Read more': '阅读更多',
    'Updated': '更新',
    'All rights reserved': '版权所有',
    'Home': '首页',
    'Guides': '指南',
    'Articles': '文章',
}

def create_zh_file(src_path, dst_path, is_guide=False):
    """基于英文文件创建中文版本"""
    if not src_path.exists():
        print(f"  ✗ 源文件不存在: {src_path}")
        return False
    
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 基础替换
    content = content.replace('lang="en"', 'lang="zh-CN"')
    content = content.replace('href="/"', 'href="/zh/"')
    content = content.replace('href="/guides/', 'href="/zh/guides/')
    content = content.replace('href="/articles/', 'href="/zh/articles/')
    content = content.replace('href="/routes.html"', 'href="/zh/routes.html"')
    content = content.replace('href="/tickets.html"', 'href="/zh/tickets.html"')
    content = content.replace('href="/passes.html"', 'href="/zh/passes.html"')
    content = content.replace('href="/live-status.html"', 'href="/zh/live-status.html"')
    content = content.replace('href="/faq.html"', 'href="/zh/faq.html"')
    
    # 翻译导航
    for en, zh in ZH_TRANSLATIONS.items():
        content = content.replace(en, zh)
    
    # 修复 hreflang（移除旧的，稍后统一修复）
    import re
    content = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', content)
    
    # 确保目录存在
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ {dst_path}")
    return True

def main():
    print("🚀 创建 zh 站点缺失文件...")
    
    # 创建 guides
    print("\n📁 创建 zh/guides/...")
    for filename in GUIDES_FILES:
        src = BASE_DIR / 'en' / 'guides' / filename
        dst = BASE_DIR / 'zh' / 'guides' / filename
        create_zh_file(src, dst, is_guide=True)
    
    # 创建 articles
    print("\n📁 创建 zh/articles/...")
    for filename in ARTICLES_FILES:
        src = BASE_DIR / 'en' / 'articles' / filename
        dst = BASE_DIR / 'zh' / 'articles' / filename
        create_zh_file(src, dst)
    
    print("\n✅ zh 站点缺失文件创建完成")

if __name__ == '__main__':
    main()
