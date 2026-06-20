#!/usr/bin/env python3
"""
Batch fix all language sites - Complete translation
Updates all pages with proper translations including titles and content
"""
import os
import re
from translations import get_translation

BASE_DIR = "/root/.openclaw/workspace/europe-train"
LANGS = ["de", "fr", "es", "ja", "ko", "pt"]

# Translations for titles and descriptions
PAGE_TITLES = {
    "de": {
        "articles_title": "Reiseführer | Europe Train - Europäische Zugreisetipps",
        "articles_desc": "Europe Train Reiseführer: Kostenvergleiche, Zugerlebnisse, ausführliche Guides für Ihre perfekte europäische Zugreise.",
    },
    "fr": {
        "articles_title": "Guides de Voyage | Europe Train - Conseils de Voyage Ferroviaire",
        "articles_desc": "Guides Europe Train: comparaisons de coûts, expériences de train, guides approfondis pour planifier votre voyage ferroviaire européen.",
    },
    "es": {
        "articles_title": "Guías de Viaje | Europe Train - Consejos de Viaje en Tren",
        "articles_desc": "Guías Europe Train: comparaciones de costos, experiencias de tren, guías detalladas para planificar su viaje en tren por Europa.",
    },
    "ja": {
        "articles_title": "旅行ガイド | Europe Train - ヨーロッパ鉄道旅行のヒント",
        "articles_desc": "Europe Train 旅行ガイド：費用比較、列車体験、ヨーロッパ鉄道旅行を計画するための詳細ガイド。",
    },
    "ko": {
        "articles_title": "여행 가이드 | Europe Train - 유럽 기차 여행 팁",
        "articles_desc": "Europe Train 여행 가이드: 비용 비교, 열차 체험, 완벽한 유럽 기차 여행을 위한 심층 가이드.",
    },
    "pt": {
        "articles_title": "Guias de Viagem | Europe Train - Dicas de Viagem de Comboio",
        "articles_desc": "Guias Europe Train: comparações de custos, experiências de comboio, guias detalhados para planear a sua viagem de comboio pela Europa.",
    }
}

def translate_articles_index(lang):
    """Create fully translated articles/index.html for a language"""
    
    # Read English template
    en_path = os.path.join(BASE_DIR, "articles", "index.html")
    with open(en_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get translations for this language
    titles = PAGE_TITLES.get(lang, {})
    
    # Replace title
    content = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{titles.get("articles_title", "Travel Guides | Europe Train")}</title>',
        content
    )
    
    # Replace meta description
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{titles.get("articles_desc", "Europe Train Travel Guides")}">',
        content
    )
    
    # Replace OG title
    content = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{titles.get("articles_title", "Travel Guides | Europe Train")}">',
        content
    )
    
    # Replace OG description
    content = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{titles.get("articles_desc", "Europe Train Travel Guides")}">',
        content
    )
    
    # Basic replacements
    content = content.replace('lang="en"', f'lang="{lang}"')
    
    # Update navigation links
    content = content.replace('href="/"', f'href="/{lang}/"')
    content = content.replace('href="/articles/"', f'href="/{lang}/articles/"')
    content = content.replace('href="/routes.html"', f'href="/{lang}/routes.html"')
    content = content.replace('href="/tickets.html"', f'href="/{lang}/tickets.html"')
    content = content.replace('href="/passes.html"', f'href="/{lang}/passes.html"')
    content = content.replace('href="/live-status.html"', f'href="/{lang}/live-status.html"')
    
    # Update lang switcher
    content = content.replace('href="/" class="active"', 'href="/"')
    content = content.replace(f'href="/{lang}/"', f'href="/{lang}/" class="active"')
    
    # Translate navigation text
    content = content.replace('>Travel Guides<', f'>{get_translation(lang, "nav_guides")}<')
    content = content.replace('>Popular Routes<', f'>{get_translation(lang, "nav_routes")}<')
    content = content.replace('>Tickets<', f'>{get_translation(lang, "nav_tickets")}<')
    content = content.replace('>Passes<', f'>{get_translation(lang, "nav_passes")}<')
    content = content.replace('>Live Status<', f'>{get_translation(lang, "nav_status")}<')
    
    # Translate page heading
    content = content.replace('>Travel Guides<', f'>{get_translation(lang, "nav_guides")}<', 1)
    
    # Translate footer
    content = content.replace('All rights reserved', get_translation(lang, 'footer'))
    
    # Write translated file
    lang_dir = os.path.join(BASE_DIR, lang, "articles")
    os.makedirs(lang_dir, exist_ok=True)
    
    output_path = os.path.join(lang_dir, "index.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {lang}/articles/index.html translated")

def main():
    print("Starting complete translation...")
    print()
    
    for lang in LANGS:
        translate_articles_index(lang)
    
    print()
    print("Translation complete!")
    print("Note: Article detail pages still need manual translation.")

if __name__ == "__main__":
    main()
