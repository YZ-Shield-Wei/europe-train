#!/usr/bin/env python3
"""
多语言网站组件化系统

核心原则：
1. 导航栏、页脚、语言切换等通用组件集中管理
2. 页面只包含内容和结构，不包含通用组件
3. 构建时自动注入组件
4. 支持多语言自动切换

使用方法：
1. 在 components/ 目录维护组件
2. 运行此脚本构建所有页面
3. 推送构建结果到 GitHub
"""

import os
import json
import re
from pathlib import Path

# 组件目录
COMPONENTS_DIR = Path("components")
PAGES_DIR = Path(".")
BUILD_DIR = Path("build")

# 语言配置
LANGUAGES = {
    "en": {"name": "EN", "label": "English"},
    "zh": {"name": "中文", "label": "中文"},
    "de": {"name": "DE", "label": "Deutsch"},
    "fr": {"name": "FR", "label": "Français"},
    "es": {"name": "ES", "label": "Español"},
    "ja": {"name": "JP", "label": "日本語"},
    "ko": {"name": "KR", "label": "한국어"},
    "pt": {"name": "PT", "label": "Português"}
}

# 导航配置（每种语言）
NAV_CONFIG = {
    "en": {
        "articles": "Travel Guides",
        "routes": "Popular Routes",
        "tickets": "Tickets",
        "passes": "Passes",
        "live_status": "Live Status"
    },
    "zh": {
        "articles": "旅行指南",
        "routes": "热门路线",
        "tickets": "火车票",
        "passes": "通票",
        "live_status": "实时状态"
    },
    "de": {
        "articles": "Reiseführer",
        "routes": "Beliebte Routen",
        "tickets": "Tickets",
        "passes": "Pässe",
        "live_status": "Live-Status"
    },
    "fr": {
        "articles": "Guides",
        "routes": "Routes",
        "tickets": "Billets",
        "passes": "Pass",
        "live_status": "Statut en Direct"
    },
    "es": {
        "articles": "Guías",
        "routes": "Rutas",
        "tickets": "Billetes",
        "passes": "Pases",
        "live_status": "Estado en Vivo"
    },
    "ja": {
        "articles": "ガイド",
        "routes": "人気ルート",
        "tickets": "切符",
        "passes": "レールパス",
        "live_status": "ライブ状況"
    },
    "ko": {
        "articles": "가이드",
        "routes": "인기 경로",
        "tickets": "티켓",
        "passes": "레일 패스",
        "live_status": "실시간 상태"
    },
    "pt": {
        "articles": "Guias",
        "routes": "Rotas",
        "tickets": "Bilhetes",
        "passes": "Passe",
        "live_status": "Status ao Vivo"
    }
}

def generate_nav_component(lang: str) -> str:
    """生成导航组件"""
    config = NAV_CONFIG[lang]
    base_path = f"/{lang}/" if lang != "en" else "/"
    
    nav_links = f"""
        <a href="{base_path}articles/">{config['articles']}</a>
        <a href="{base_path}routes.html">{config['routes']}</a>
        <a href="{base_path}tickets.html">{config['tickets']}</a>
        <a href="{base_path}passes.html">{config['passes']}</a>
        <a href="{base_path}live-status.html">{config['live_status']}</a>
    """
    
    lang_links = ""
    for code, info in LANGUAGES.items():
        active = ' class="active"' if code == lang else ''
        href = f"/{code}/" if code != "en" else "/"
        lang_links += f'<a href="{href}"{active}>{info["name"]}</a>\n'
    
    return f"""<!-- Universal Navigation Component -->
<!-- Language: {lang.upper()} -->
<header class="header">
    <div class="header-inner">
        <a href="{base_path}" class="logo">
            <div class="logo-icon">ET</div>
            Europe Train
        </a>
        <nav class="nav">
            {nav_links}
        </nav>
        <div class="lang-switcher">
            {lang_links}
        </div>
    </div>
</header>"""

def generate_footer_component(lang: str) -> str:
    """生成页脚组件"""
    return """<footer class="footer"><p>© 2026 Europe Train Travel Guide. All rights reserved.</p></footer>"""

def generate_hreflang_links(filepath: str, lang: str) -> str:
    """生成 hreflang 链接"""
    # 从文件路径提取相对路径
    rel_path = filepath.replace(f"{lang}/", "") if lang != "en" else filepath
    
    links = ""
    for code in LANGUAGES.keys():
        prefix = f"/{code}" if code != "en" else ""
        links += f'<link rel="alternate" hreflang="{code if code != "zh" else "zh-CN"}" href="https://www.europe-train.com{prefix}/{rel_path}">\n'
    
    return links

def build_page(source_path: Path, lang: str) -> str:
    """构建单个页面"""
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取页面内容（去掉旧的导航和页脚）
    # 保留 <article> 到 </article> 之间的内容
    article_match = re.search(r'<article.*?</article>', content, re.DOTALL)
    if not article_match:
        article_match = re.search(r'<main.*?</main>', content, re.DOTALL)
    
    if article_match:
        page_content = article_match.group(0)
    else:
        # 如果没有 article/main，保留 body 内容
        body_match = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
        page_content = body_match.group(1) if body_match else content
    
    # 生成页面
    base_path = f"/{lang}/" if lang != "en" else "/"
    
    html = f"""<!DOCTYPE html>
<html lang="{lang if lang != 'zh' else 'zh-CN'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{extract_title(content)}</title>
    <meta name="description" content="{extract_description(content)}">
    <link rel="canonical" href="https://www.europe-train.com/{lang}/{source_path}">
    <link rel="stylesheet" href="/css/global.css">
    {generate_hreflang_links(str(source_path), lang)}
</head>
<body>
    {generate_nav_component(lang)}
    {page_content}
    {generate_footer_component(lang)}
</body>
</html>"""
    
    return html

def extract_title(content: str) -> str:
    """提取页面标题"""
    match = re.search(r'<title>(.*?)</title>', content)
    return match.group(1) if match else "Europe Train"

def extract_description(content: str) -> str:
    """提取页面描述"""
    match = re.search(r'<meta name="description" content="(.*?)">', content)
    return match.group(1) if match else "European Train Travel Guide"

def build_all():
    """构建所有页面"""
    # 清理构建目录
    if BUILD_DIR.exists():
        import shutil
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir()
    
    # 构建每种语言的页面
    for lang in LANGUAGES.keys():
        lang_dir = BUILD_DIR / lang if lang != "en" else BUILD_DIR
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        # 查找源文件
        source_dir = PAGES_DIR / lang if lang != "en" else PAGES_DIR
        if not source_dir.exists():
            continue
        
        for html_file in source_dir.rglob("*.html"):
            # 构建页面
            built_html = build_page(html_file, lang)
            
            # 保存到构建目录
            rel_path = html_file.relative_to(source_dir)
            target_path = lang_dir / rel_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(built_html)
            
            print(f"Built: {target_path}")
    
    print(f"\n✅ Build complete: {BUILD_DIR}")

if __name__ == "__main__":
    build_all()
