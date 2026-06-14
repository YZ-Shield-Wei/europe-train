#!/usr/bin/env python3
"""
Europe Train - 多语言静态网站构建系统

使用方法: python build.py
"""

import re
import shutil
from pathlib import Path

# 语言配置
LANGUAGES = {
    "en": {"name": "EN", "nav": {
        "articles": "Travel Guides", "routes": "Popular Routes", 
        "tickets": "Tickets", "passes": "Passes", "live_status": "Live Status"
    }},
    "zh": {"name": "中文", "nav": {
        "articles": "旅行指南", "routes": "热门路线",
        "tickets": "火车票", "passes": "通票", "live_status": "实时状态"
    }},
    "de": {"name": "DE", "nav": {
        "articles": "Reiseführer", "routes": "Beliebte Routen",
        "tickets": "Tickets", "passes": "Pässe", "live_status": "Live-Status"
    }},
    "fr": {"name": "FR", "nav": {
        "articles": "Guides", "routes": "Routes",
        "tickets": "Billets", "passes": "Pass", "live_status": "Statut en Direct"
    }},
    "es": {"name": "ES", "nav": {
        "articles": "Guías", "routes": "Rutas",
        "tickets": "Billetes", "passes": "Pases", "live_status": "Estado en Vivo"
    }},
    "ja": {"name": "JP", "nav": {
        "articles": "ガイド", "routes": "人気ルート",
        "tickets": "切符", "passes": "レールパス", "live_status": "ライブ状況"
    }},
    "ko": {"name": "KR", "nav": {
        "articles": "가이드", "routes": "인기 경로",
        "tickets": "티켓", "passes": "레일 패스", "live_status": "실시간 상태"
    }},
    "pt": {"name": "PT", "nav": {
        "articles": "Guias", "routes": "Rotas",
        "tickets": "Bilhetes", "passes": "Passe", "live_status": "Status ao Vivo"
    }}
}

COMPONENTS_DIR = Path("components")
CONTENT_DIR = Path("content")
BUILD_DIR = Path("build")

def generate_nav(lang: str) -> str:
    """生成导航组件"""
    config = LANGUAGES[lang]
    nav_config = config["nav"]
    base_path = f"/{lang}/" if lang != "en" else "/"
    
    nav_links = "\n".join([
        f'            <a href="{base_path}{key.replace("_", "-")}.html">{value}</a>'
        for key, value in nav_config.items()
    ])
    
    lang_links = "\n".join([
        f'            <a href="/{l}/"{" class=\"active\"" if l == lang else ""}>{LANGUAGES[l]["name"]}</a>'
        for l in LANGUAGES.keys()
    ])
    
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

def generate_footer() -> str:
    """生成页脚组件"""
    return '<footer class="footer"><p>© 2026 Europe Train Travel Guide. All rights reserved.</p></footer>'

def generate_hreflang(path: str, current_lang: str) -> str:
    """生成 hreflang 链接"""
    links = []
    for lang in LANGUAGES.keys():
        prefix = f"/{lang}" if lang != "en" else ""
        hreflang = f"zh-CN" if lang == "zh" else lang
        # 清理路径中的语言前缀
        clean_path = path
        if clean_path.startswith(f"{current_lang}/"):
            clean_path = clean_path[len(current_lang)+1:]
        links.append(f'    <link rel="alternate" hreflang="{hreflang}" href="https://www.europe-train.com{prefix}/{clean_path}">')
    return "\n".join(links)

def extract_meta(html: str) -> dict:
    """提取页面元数据"""
    meta = {"title": "Europe Train", "description": "European Train Travel Guide"}
    
    match = re.search(r'<title>(.*?)</title>', html)
    if match:
        meta["title"] = match.group(1)
    
    match = re.search(r'<meta name="description" content="(.*?)">', html)
    if match:
        meta["description"] = match.group(1)
    
    return meta

def extract_body(html: str) -> str:
    """提取 body 内容"""
    for tag in ['article', 'main']:
        match = re.search(rf'<{tag}.*?</{tag}>', html, re.DOTALL)
        if match:
            return match.group(0)
    
    match = re.search(r'<body>(.*?)</body>', html, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return html

def build_page(content_html: str, lang: str, path: str) -> str:
    """构建完整页面"""
    meta = extract_meta(content_html)
    body_content = extract_body(content_html)
    hreflang = generate_hreflang(path, lang)
    base_path = f"/{lang}/" if lang != "en" else "/"
    
    return f"""<!DOCTYPE html>
<html lang="{lang if lang != 'zh' else 'zh-CN'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta['title']}</title>
    <meta name="description" content="{meta['description']}">
    <link rel="canonical" href="https://www.europe-train.com{base_path}{path}">
    <link rel="stylesheet" href="/css/global.css">
{hreflang}
    <meta property="og:title" content="{meta['title']}">
    <meta property="og:description" content="{meta['description']}">
    <meta property="og:image" content="https://www.europe-train.com/images/og-image.jpg">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JWY9K5ZRSF"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-JWY9K5ZRSF');</script>
</head>
<body>
{generate_nav(lang)}
{body_content}
{generate_footer()}
</body>
</html>"""

def build_all():
    """构建整个站点"""
    print("🚀 开始构建站点...")
    
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir()
    
    # 复制静态资源
    for dir_name in ['css', 'js', 'images', 'fonts']:
        src = Path(dir_name)
        if src.exists():
            dst = BUILD_DIR / dir_name
            shutil.copytree(src, dst)
            print(f"📁 复制: {dir_name}")
    
    # 构建每种语言
    for lang in LANGUAGES.keys():
        content_dir = CONTENT_DIR / lang if lang != "en" else CONTENT_DIR
        if not content_dir.exists():
            continue
        
        output_dir = BUILD_DIR / lang if lang != "en" else BUILD_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n🌐 构建语言: {lang.upper()}")
        
        for content_file in content_dir.rglob("*.html"):
            with open(content_file, 'r', encoding='utf-8') as f:
                content_html = f.read()
            
            rel_path = content_file.relative_to(content_dir)
            path = str(rel_path).replace("\\", "/")
            
            page_html = build_page(content_html, lang, path)
            
            output_path = output_dir / rel_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(page_html)
            
            print(f"  ✅ {path}")
    
    print(f"\n✅ 构建完成: {BUILD_DIR}")

if __name__ == "__main__":
    build_all()
