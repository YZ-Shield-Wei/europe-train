#!/usr/bin/env python3
"""
Europe Train - 全站一致性修复脚本
修复导航栏、hreflang、语言属性等结构性问题
"""

import os
import re
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
        "articles": "Reiseführer", "routes": "Beliebte Strecken",
        "tickets": "Tickets", "passes": "Rail Passes", "live_status": "Live-Status"
    }},
    "fr": {"name": "FR", "nav": {
        "articles": "Guides de Voyage", "routes": "Itinéraires Populaires",
        "tickets": "Billets", "passes": "Pass", "live_status": "Statut en Direct"
    }},
    "es": {"name": "ES", "nav": {
        "articles": "Guías de Viaje", "routes": "Rutas Populaires",
        "tickets": "Billetes", "passes": "Pases", "live_status": "Estado en Vivo"
    }},
    "ja": {"name": "JP", "nav": {
        "articles": "旅行ガイド", "routes": "人気路線",
        "tickets": "切符予約", "passes": "レールパス", "live_status": "ライブ状況"
    }},
    "ko": {"name": "KR", "nav": {
        "articles": "여행 가이드", "routes": "인기 노선",
        "tickets": "티켓", "passes": "철도 패스", "live_status": "실시간 상태"
    }},
    "pt": {"name": "PT", "nav": {
        "articles": "Guias de Viagem", "routes": "Rotas Populares",
        "tickets": "Bilhetes", "passes": "Passes", "live_status": "Status ao Vivo"
    }},
    "it": {"name": "IT", "nav": {
        "articles": "Guide di Viaggio", "routes": "Percorsi Popolari",
        "tickets": "Biglietti", "passes": "Pass", "live_status": "Stato in Tempo Reale"
    }}
}

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

def fix_hardcoded_links(filepath, lang):
    """修复硬编码的 /en/ 链接"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    base_path = f"/{lang}/"
    
    # 修复硬编码的 /en/ 路径（但保留外部链接和特定路径）
    # 只修复内部链接：href="/en/xxx" → href="/lang/xxx"
    content = re.sub(r'href="/en/([^"]*?)"', f'href="{base_path}\\1"', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def check_duplicate_hreflang(filepath):
    """检查并修复重复的 hreflang"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有 hreflang 标签
    hreflang_pattern = r'<link rel="alternate" hreflang="([^"]*)" href="([^"]*)"'
    matches = re.findall(hreflang_pattern, content)
    
    if not matches:
        return False
    
    # 检查重复
    seen = set()
    duplicates = []
    for lang_code, url in matches:
        if lang_code in seen:
            duplicates.append(lang_code)
        seen.add(lang_code)
    
    if duplicates:
        print(f"  ⚠️  {filepath} 发现重复 hreflang: {duplicates}")
        # 移除所有 hreflang
        content = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', content)
        
        # 获取文件相对于语言目录的路径
        # 例如: de/tickets.html → tickets.html
        rel_parts = filepath.relative_to(BASE_DIR).parts
        if len(rel_parts) > 1:
            # 去掉语言前缀
            rel_path = '/'.join(rel_parts[1:])
        else:
            rel_path = str(filepath.relative_to(BASE_DIR))
        
        # 生成新的 hreflang
        hreflang_tags = []
        for l in LANGUAGES.keys():
            prefix = f"/{l}" if l != "en" else ""
            hreflang_code = f"zh-CN" if l == "zh" else l
            hreflang_tags.append(f'    <link rel="alternate" hreflang="{hreflang_code}" href="https://www.europe-train.com{prefix}/{rel_path}">')
        
        hreflang_block = "\n".join(hreflang_tags)
        
        # 插入到 </head> 之前
        content = content.replace('</head>', f'{hreflang_block}\n</head>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def process_all_pages():
    """处理所有页面"""
    total = 0
    fixed_links = 0
    fixed_hreflang = 0
    
    for lang in LANGUAGES.keys():
        lang_dir = BASE_DIR / lang
        if not lang_dir.exists():
            print(f"⚠️  {lang} 目录不存在，跳过")
            continue
        
        for html_file in lang_dir.rglob("*.html"):
            total += 1
            if fix_hardcoded_links(html_file, lang):
                fixed_links += 1
            if check_duplicate_hreflang(html_file):
                fixed_hreflang += 1
    
    print(f"✅ 处理完成: {total} 个文件")
    print(f"   修复硬编码链接: {fixed_links}")
    print(f"   修复重复hreflang: {fixed_hreflang}")

if __name__ == "__main__":
    print("🚀 开始修复全站一致性...")
    process_all_pages()
    print("✅ 修复完成")
