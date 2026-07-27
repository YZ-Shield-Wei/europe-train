#!/usr/bin/env python3
"""
修复 Search Console 问题的脚本
1. 更新 sitemap.xml，包含所有语言子站点的文章
2. 修复缺少 hreflang 的页面
3. 修复 guides 目录中的错误链接
"""

import os
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

def generate_sitemap():
    """生成完整的 sitemap.xml"""
    
    # 基础 URL 列表
    urls = []
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 首页
    urls.append({
        'loc': 'https://www.europe-train.com/',
        'lastmod': today,
        'changefreq': 'daily',
        'priority': '1.0',
        'alternates': [
            ('en', 'https://www.europe-train.com/'),
            ('de', 'https://www.europe-train.com/de/'),
            ('fr', 'https://www.europe-train.com/fr/'),
            ('es', 'https://www.europe-train.com/es/'),
            ('ja', 'https://www.europe-train.com/ja/'),
            ('ko', 'https://www.europe-train.com/ko/'),
            ('pt', 'https://www.europe-train.com/pt/'),
            ('zh', 'https://www.europe-train.com/zh/'),
        ]
    })
    
    # 关键页面
    key_pages = ['tickets.html', 'passes.html', 'routes.html', 'live-status.html']
    for page in key_pages:
        urls.append({
            'loc': f'https://www.europe-train.com/{page}',
            'lastmod': today,
            'changefreq': 'weekly',
            'priority': '0.8'
        })
    
    # 各语言首页
    languages = ['de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']
    for lang in languages:
        urls.append({
            'loc': f'https://www.europe-train.com/{lang}/',
            'lastmod': today,
            'changefreq': 'daily',
            'priority': '0.9'
        })
    
    # 收集所有文章页面
    article_dirs = {
        'en': BASE_DIR / 'en' / 'articles',
        'de': BASE_DIR / 'de' / 'articles',
        'fr': BASE_DIR / 'fr' / 'articles',
        'es': BASE_DIR / 'es' / 'articles',
        'ja': BASE_DIR / 'ja' / 'articles',
        'ko': BASE_DIR / 'ko' / 'articles',
        'pt': BASE_DIR / 'pt' / 'articles',
        'zh': BASE_DIR / 'zh' / 'articles',
    }
    
    # 英文文章（根路径）
    en_articles = BASE_DIR / 'en' / 'articles'
    if en_articles.exists():
        for html_file in sorted(en_articles.glob("*.html")):
            if html_file.name == 'index.html':
                continue
            urls.append({
                'loc': f'https://www.europe-train.com/en/articles/{html_file.name}',
                'lastmod': today,
                'changefreq': 'weekly',
                'priority': '0.7'
            })
    
    # 其他语言文章
    for lang, articles_dir in article_dirs.items():
        if not articles_dir.exists():
            continue
        for html_file in sorted(articles_dir.glob("*.html")):
            if html_file.name == 'index.html':
                continue
            urls.append({
                'loc': f'https://www.europe-train.com/{lang}/articles/{html_file.name}',
                'lastmod': today,
                'changefreq': 'weekly',
                'priority': '0.7'
            })
    
    # 生成 XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    
    for url in urls:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{url["loc"]}</loc>')
        xml_lines.append(f'    <lastmod>{url["lastmod"]}</lastmod>')
        xml_lines.append(f'    <changefreq>{url["changefreq"]}</changefreq>')
        xml_lines.append(f'    <priority>{url["priority"]}</priority>')
        
        # 添加 alternate 链接
        if 'alternates' in url:
            for lang, href in url['alternates']:
                xml_lines.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{href}"/>')
        
        xml_lines.append('  </url>')
    
    xml_lines.append('</urlset>')
    
    # 写入文件
    sitemap_content = '\n'.join(xml_lines)
    sitemap_file = BASE_DIR / 'sitemap.xml'
    sitemap_file.write_text(sitemap_content)
    
    return len(urls)

def fix_guides_links():
    """修复 guides 目录中的错误链接"""
    guides_dir = BASE_DIR / 'guides'
    if not guides_dir.exists():
        return 0
    
    fixed_count = 0
    
    for html_file in guides_dir.glob("*.html"):
        content = html_file.read_text()
        original = content
        
        # 修复缺少语言前缀的 /articles/ 链接
        # 将 href="/articles/xxx" 改为 href="/en/articles/xxx"
        content = re.sub(
            r'href=["\'](/articles/[^"\']+)["\']',
            r'href="/en\1"',
            content
        )
        
        if content != original:
            html_file.write_text(content)
            fixed_count += 1
            print(f"   修复: {html_file.name}")
    
    return fixed_count

def add_hreflang_to_articles():
    """为文章页面添加 hreflang 标签"""
    languages = ['en', 'de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']
    fixed_count = 0
    
    for lang in languages:
        articles_dir = BASE_DIR / lang / 'articles'
        if not articles_dir.exists():
            continue
        
        for html_file in articles_dir.glob("*.html"):
            if html_file.name == 'index.html':
                continue
            
            content = html_file.read_text()
            
            # 检查是否已有 hreflang
            if 'hreflang' in content:
                continue
            
            # 检查是否有 <head> 标签
            if '<head>' not in content:
                continue
            
            # 构建 hreflang 标签
            hreflang_tags = []
            page_name = html_file.name
            
            for alt_lang in languages:
                alt_path = BASE_DIR / alt_lang / 'articles' / page_name
                if alt_path.exists():
                    hreflang_tags.append(
                        f'<link rel="alternate" hreflang="{alt_lang}" href="https://www.europe-train.com/{alt_lang}/articles/{page_name}" />'
                    )
            
            if hreflang_tags:
                # 在 </head> 前插入 hreflang 标签
                hreflang_block = '\n'.join(['    ' + tag for tag in hreflang_tags])
                content = content.replace(
                    '</head>',
                    f'    <!-- Hreflang -->\n{hreflang_block}\n</head>'
                )
                
                html_file.write_text(content)
                fixed_count += 1
    
    return fixed_count

def main():
    print("=" * 60)
    print("🔧 修复 Search Console 问题")
    print("=" * 60)
    
    # 1. 更新 sitemap
    print("\n🗺️  1. 更新 sitemap.xml")
    url_count = generate_sitemap()
    print(f"   ✅ 已生成新 sitemap，包含 {url_count} 个 URL")
    
    # 2. 修复 guides 链接
    print("\n🔗 2. 修复 guides 目录链接")
    fixed_guides = fix_guides_links()
    print(f"   ✅ 已修复 {fixed_guides} 个 guides 文件")
    
    # 3. 添加 hreflang
    print("\n🌐 3. 为文章添加 hreflang 标签")
    fixed_hreflang = add_hreflang_to_articles()
    print(f"   ✅ 已为 {fixed_hreflang} 个文章添加 hreflang")
    
    print("\n" + "=" * 60)
    print("✅ 修复完成，请推送更新到服务器")
    print("=" * 60)

if __name__ == "__main__":
    main()
