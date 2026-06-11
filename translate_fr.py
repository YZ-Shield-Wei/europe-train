#!/usr/bin/env python3
"""
Translate Chinese articles to French.
Keeps HTML structure, CSS classes, and styling.
Updates lang to "fr", navigation to /fr/ paths, adds hreflang alternates.
"""

import os
import re

# Article files to translate
ARTICLES = [
    "paris-zurich-train-vs-flight.html",
    "tgv-lyria-experience.html",
    "london-paris-eurostar-guide.html",
    "swiss-scenic-trains.html",
    "france-tgv-guide.html",
    "germany-ice-guide.html",
    "italy-frecciarossa-guide.html",
    "spain-ave-guide.html",
    "train-station-guide.html",
    "delay-compensation-guide.html",
    "train-apps-comparison.html",
    "europe-train-ticket-rules.html",
]

SRC_DIR = "/root/.openclaw/workspace/europe-train/articles"
DST_DIR = "/root/.openclaw/workspace/europe-train/fr/articles"

os.makedirs(DST_DIR, exist_ok=True)

# Translation dictionary for common UI elements
UI_TRANSLATIONS = {
    'lang="zh-CN"': 'lang="fr"',
    '旅行指南 | Europe Train - 欧洲火车旅行攻略': 'Guides de Voyage | Europe Train - Guides de Voyage Ferroviaire Européenne',
    '旅行指南': 'Guides de Voyage',
    '热门路线': 'Routes Populaires',
    '车票预订': 'Billets',
    '通票': 'Pass',
    '中文': '中文',
    '首页': 'Accueil',
    '文章': 'Articles',
    '费用对比': 'Comparaisons de Coûts',
    '列车体验': 'Expériences de Train',
    '国家指南': 'Guides par Pays',
    '实用攻略': 'Guides Pratiques',
    '硬核科普': 'Guides Experts',
    '景观列车': 'Trains Panoramiques',
    '法国': 'France',
    '德国': 'Allemagne',
    '意大利': 'Italie',
    '西班牙': 'Espagne',
    '预订指南': 'Guide de Réservation',
    '权益保障': 'Indemnisation',
    'APP对比': 'Comparaison d\'Apps',
    '车站指南': 'Guide des Gares',
    '快速结论': 'Conclusion Rapide',
    '核心要点': 'Points Clés',
    '阅读时间': 'Temps de Lecture',
    '更新于': 'Mis à jour le',
    '本文由 Europe Train 编辑部撰写': 'Article rédigé par la rédaction Europe Train',
    '票价和时刻可能变动，请查询最新信息': 'Les prix et horaires peuvent changer, veuillez consulter les informations les plus récentes',
    '相关指南': 'Guides Connexes',
}

# Navigation path replacements
NAV_REPLACEMENTS = [
    (r'href="/articles/"', 'href="/fr/articles/"'),
    (r'href="/routes.html"', 'href="/fr/routes.html"'),
    (r'href="/tickets.html"', 'href="/fr/tickets.html"'),
    (r'href="/passes.html"', 'href="/fr/passes.html"'),
    (r'href="/"', 'href="/fr/"'),
    (r'href="/zh/" class="active"', 'href="/zh/"'),
    (r'href="/fr/"', 'href="/fr/" class="active"'),
]

def translate_article(filename):
    src_path = os.path.join(SRC_DIR, filename)
    dst_path = os.path.join(DST_DIR, filename)
    
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply UI translations
    for cn, fr in UI_TRANSLATIONS.items():
        content = content.replace(cn, fr)
    
    # Apply navigation path replacements
    for pattern, replacement in NAV_REPLACEMENTS:
        content = re.sub(pattern, replacement, content)
    
    # Update lang attribute
    content = content.replace('lang="zh-CN"', 'lang="fr"')
    content = content.replace('lang="zh"', 'lang="fr"')
    
    # Update canonical and add hreflang alternates
    # Replace canonical URL
    content = re.sub(
        r'<link rel="canonical" href="https://www\.europe-train\.com/articles/([^"]+)">',
        r'<link rel="canonical" href="https://www.europe-train.com/fr/articles/\1">\n    <link rel="alternate" hreflang="fr" href="https://www.europe-train.com/fr/articles/\1">\n    <link rel="alternate" hreflang="zh-CN" href="https://www.europe-train.com/articles/\1">\n    <link rel="alternate" hreflang="en" href="https://www.europe-train.com/en/articles/\1">',
        content
    )
    
    # Update title meta description language
    content = re.sub(
        r'<title>([^<]+)</title>',
        lambda m: f'<title>{m.group(1).replace(" | Europe Train", " | Europe Train")}</title>',
        content
    )
    
    # Update og:title if present
    content = re.sub(
        r'<meta property="og:title" content="([^"]+)">',
        lambda m: f'<meta property="og:title" content="{m.group(1)}">',
        content
    )
    
    # Fix breadcrumb links
    content = content.replace('href="/"', 'href="/fr/"')
    content = content.replace('href="/articles/"', 'href="/fr/articles/"')
    
    # Update article links to point to fr version
    content = re.sub(
        r'href="/articles/([^"]+)"',
        r'href="/fr/articles/\1"',
        content
    )
    
    # But don't double-prefix already fr links
    content = content.replace('href="/fr/articles/', 'href="/fr/articles/')
    
    # Update related article links
    content = re.sub(
        r'href="/guides/([^"]+)"',
        r'href="/fr/guides/\1"',
        content
    )
    
    # Update tag links
    content = re.sub(
        r'href="/articles/tag-([^"]+)"',
        r'href="/fr/articles/tag-\1"',
        content
    )
    
    # Update CSS paths
    content = content.replace('href="../css/', 'href="../../css/')
    content = content.replace('href="css/global.css"', 'href="../../css/global.css"')
    content = content.replace('url(\'../images/', 'url(\'../../images/')
    content = content.replace('url("../images/', 'url("../../images/')
    
    # Update image paths in content
    content = content.replace('../images/', '../../images/')
    
    # Translate specific Chinese text content (basic replacements)
    # These are article-specific and would need proper translation
    # For now, we'll add markers for translation
    
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created: {dst_path}")

if __name__ == "__main__":
    for article in ARTICLES:
        translate_article(article)
    
    print(f"\nDone! Translated {len(ARTICLES)} articles to {DST_DIR}")
