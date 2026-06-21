#!/usr/bin/env python3
"""
创建 it（意大利语）站点
基于 en 版本，添加意大利语翻译
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

# 意大利语翻译映射
IT_TRANSLATIONS = {
    'Travel Guides': 'Guide di Viaggio',
    'Popular Routes': 'Percorsi Popolari',
    'Tickets': 'Biglietti',
    'Passes': 'Pass',
    'Live Status': 'Stato in Tempo Reale',
    'Related Guides': 'Guide Correlati',
    'Read more': 'Leggi di più',
    'Updated': 'Aggiornato',
    'All rights reserved': 'Tutti i diritti riservati',
    'Home': 'Home',
    'Guides': 'Guide',
    'Articles': 'Articoli',
    'How to Buy European Train Tickets': 'Come Acquistare Biglietti del Treno Europei',
    'Complete Guide': 'Guida Completa',
    'Europe Train': 'Europe Train',
}

def create_it_site():
    """创建意大利语站点"""
    print("🚀 创建 it 站点...")
    
    src_dir = BASE_DIR / 'en'
    dst_dir = BASE_DIR / 'it'
    
    if dst_dir.exists():
        print("⚠️  it 目录已存在，跳过")
        return
    
    # 复制 en 目录到 it
    shutil.copytree(src_dir, dst_dir)
    print(f"📁 复制 {src_dir} → {dst_dir}")
    
    # 翻译所有 HTML 文件
    for html_file in dst_dir.rglob('*.html'):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 基础替换
        content = content.replace('lang="en"', 'lang="it"')
        content = content.replace('href="/"', 'href="/it/"')
        content = content.replace('href="/guides/', 'href="/it/guides/')
        content = content.replace('href="/articles/', 'href="/it/articles/')
        content = content.replace('href="/routes.html"', 'href="/it/routes.html"')
        content = content.replace('href="/tickets.html"', 'href="/it/tickets.html"')
        content = content.replace('href="/passes.html"', 'href="/it/passes.html"')
        content = content.replace('href="/live-status.html"', 'href="/it/live-status.html"')
        content = content.replace('href="/faq.html"', 'href="/it/faq.html"')
        
        # 翻译导航和常见文本
        for en, it in IT_TRANSLATIONS.items():
            content = content.replace(en, it)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("✅ it 站点创建完成")

if __name__ == '__main__':
    create_it_site()
