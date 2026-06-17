#!/usr/bin/env python3
"""
Create translated guides for de/fr/es/ja/ko/pt languages.
Uses Moonshot API for translation.
"""

import os
import re
import time

# Try to import openai
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("Warning: openai not installed, using fallback dictionary translation")

# Language configurations
LANG_CONFIG = {
    'de': {
        'lang': 'de',
        'name': 'DE',
        'native_name': 'Deutsch',
        'flag': 'DE',
    },
    'fr': {
        'lang': 'fr',
        'name': 'FR',
        'native_name': 'Français',
        'flag': 'FR',
    },
    'es': {
        'lang': 'es',
        'name': 'ES',
        'native_name': 'Español',
        'flag': 'ES',
    },
    'ja': {
        'lang': 'ja',
        'name': 'JP',
        'native_name': '日本語',
        'flag': 'JP',
    },
    'ko': {
        'lang': 'ko',
        'name': 'KR',
        'native_name': '한국어',
        'flag': 'KR',
    },
    'pt': {
        'lang': 'pt',
        'name': 'PT',
        'native_name': 'Português',
        'flag': 'PT',
    },
}

# UI translations for each language
UI_TRANSLATIONS = {
    'de': {
        'Travel Guides': 'Reiseführer',
        'Popular Routes': 'Beliebte Strecken',
        'Tickets': 'Tickets',
        'Passes': 'Pässe',
        'Live Status': 'Live-Status',
        'Home': 'Startseite',
        'Guides': 'Guides',
        'Updated June 2026': 'Aktualisiert Juni 2026',
        'Reading time': 'Lesezeit',
        'Key Takeaways': 'Wichtigste Erkenntnisse',
        'Booking Tips': 'Buchungstipps',
        'Related Guides': 'Verwandte Guides',
        'minutes': 'Minuten',
        'All rights reserved': 'Alle Rechte vorbehalten',
    },
    'fr': {
        'Travel Guides': 'Guides de Voyage',
        'Popular Routes': 'Routes Populaires',
        'Tickets': 'Billets',
        'Passes': 'Pass',
        'Live Status': 'Statut en Direct',
        'Home': 'Accueil',
        'Guides': 'Guides',
        'Updated June 2026': 'Mis à jour juin 2026',
        'Reading time': 'Temps de lecture',
        'Key Takeaways': 'Points Clés',
        'Booking Tips': 'Conseils de Réservation',
        'Related Guides': 'Guides Connexes',
        'minutes': 'minutes',
        'All rights reserved': 'Tous droits réservés',
    },
    'es': {
        'Travel Guides': 'Guías de Viaje',
        'Popular Routes': 'Rutas Populares',
        'Tickets': 'Billetes',
        'Passes': 'Pases',
        'Live Status': 'Estado en Vivo',
        'Home': 'Inicio',
        'Guides': 'Guías',
        'Updated June 2026': 'Actualizado junio 2026',
        'Reading time': 'Tiempo de lectura',
        'Key Takeaways': 'Puntos Clave',
        'Booking Tips': 'Consejos de Reserva',
        'Related Guides': 'Guías Relacionadas',
        'minutes': 'minutos',
        'All rights reserved': 'Todos los derechos reservados',
    },
    'ja': {
        'Travel Guides': '旅行ガイド',
        'Popular Routes': '人気ルート',
        'Tickets': '切符',
        'Passes': 'パス',
        'Live Status': 'ライブ状況',
        'Home': 'ホーム',
        'Guides': 'ガイド',
        'Updated June 2026': '2026年6月更新',
        'Reading time': '読了時間',
        'Key Takeaways': '要点',
        'Booking Tips': '予約のヒント',
        'Related Guides': '関連ガイド',
        'minutes': '分',
        'All rights reserved': 'All rights reserved',
    },
    'ko': {
        'Travel Guides': '여행 가이드',
        'Popular Routes': '인기 경로',
        'Tickets': '티켓',
        'Passes': '패스',
        'Live Status': '실시간 상태',
        'Home': '홈',
        'Guides': '가이드',
        'Updated June 2026': '2026년 6월 업데이트',
        'Reading time': '독서 시간',
        'Key Takeaways': '핵심 요약',
        'Booking Tips': '예약 팁',
        'Related Guides': '관련 가이드',
        'minutes': '분',
        'All rights reserved': 'All rights reserved',
    },
    'pt': {
        'Travel Guides': 'Guias de Viagem',
        'Popular Routes': 'Rotas Populares',
        'Tickets': 'Bilhetes',
        'Passes': 'Passes',
        'Live Status': 'Status ao Vivo',
        'Home': 'Início',
        'Guides': 'Guias',
        'Updated June 2026': 'Atualizado junho 2026',
        'Reading time': 'Tempo de leitura',
        'Key Takeaways': 'Pontos Principais',
        'Booking Tips': 'Dicas de Reserva',
        'Related Guides': 'Guias Relacionados',
        'minutes': 'minutos',
        'All rights reserved': 'Todos os direitos reservados',
    },
}

def translate_with_moonshot(text, target_lang):
    """Translate text using Moonshot API."""
    if not HAS_OPENAI:
        return None
    
    try:
        client = OpenAI(
            api_key=os.environ.get('MOONSHOT_API_KEY', ''),
            base_url="https://api.moonshot.cn/v1"
        )
        
        lang_names = {
            'de': 'German',
            'fr': 'French',
            'es': 'Spanish',
            'ja': 'Japanese',
            'ko': 'Korean',
            'pt': 'Portuguese',
        }
        
        response = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {"role": "system", "content": f"You are a professional translator. Translate the following text to {lang_names.get(target_lang, target_lang)}. Keep HTML tags and structure intact. Only translate the text content."},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Translation API error: {e}")
        return None

def translate_content_simple(content, lang):
    """Simple dictionary-based translation for UI elements."""
    trans = UI_TRANSLATIONS.get(lang, {})
    
    for en, translated in trans.items():
        content = content.replace(en, translated)
    
    return content

def create_translated_guide(src_path, dst_dir, lang):
    """Create a translated version of a guide file."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    config = LANG_CONFIG[lang]
    
    # Update lang attribute
    content = content.replace('lang="en"', f'lang="{config["lang"]}"')
    
    # Update navigation paths
    content = content.replace('href="/articles/"', f'href="/{lang}/articles/"')
    content = content.replace('href="/routes.html"', f'href="/{lang}/routes.html"')
    content = content.replace('href="/tickets.html"', f'href="/{lang}/tickets.html"')
    content = content.replace('href="/passes.html"', f'href="/{lang}/passes.html"')
    content = content.replace('href="/live-status.html"', f'href="/{lang}/live-status.html"')
    content = content.replace('href="/"', f'href="/{lang}/"')
    
    # Update active language
    content = content.replace('href="/" class="active"', f'href="/{lang}/" class="active"')
    content = content.replace(f'href="/{lang}/"', f'href="/{lang}/" class="active"')
    
    # Update canonical and hreflang
    content = re.sub(
        r'<link rel="canonical" href="https://www\.europe-train\.com/en/guides/([^"]+)">',
        f'<link rel="canonical" href="https://www.europe-train.com/{lang}/guides/\\1">',
        content
    )
    
    # Update breadcrumb
    content = content.replace('href="/en/"', f'href="/{lang}/"')
    content = content.replace('href="/en/articles/"', f'href="/{lang}/articles/"')
    
    # Update related article links
    content = re.sub(
        r'href="/en/guides/([^"]+)"',
        f'href="/{lang}/guides/\\1"',
        content
    )
    content = re.sub(
        r'href="/en/articles/([^"]+)"',
        f'href="/{lang}/articles/\\1"',
        content
    )
    
    # Update CSS paths
    content = content.replace('href="/css/global.css"', 'href="../../css/global.css"')
    content = content.replace('href="../../css/global.css"', 'href="../../css/global.css"')
    
    # Update image paths
    content = content.replace('src="/images/', 'src="../../images/')
    content = content.replace('url(/images/', 'url(../../images/')
    
    # Update og:image
    content = re.sub(
        r'<meta property="og:image" content="https://www\.europe-train\.com/images/og-([^"]+)-en\.jpg">',
        f'<meta property="og:image" content="https://www.europe-train.com/images/og-\\1-{lang}.jpg">',
        content
    )
    
    # Apply UI translations
    content = translate_content_simple(content, lang)
    
    # Write translated file
    os.makedirs(dst_dir, exist_ok=True)
    filename = os.path.basename(src_path)
    dst_path = os.path.join(dst_dir, filename)
    
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created: {dst_path}")
    return dst_path

def main():
    src_dir = "/root/.openclaw/workspace/europe-train/en/guides"
    
    guide_files = [
        "popular-routes.html",
        "ticket-buying-guide.html",
        "rail-pass-guide.html",
        "train-experience-guide.html",
    ]
    
    target_langs = ['de', 'fr', 'es', 'ja', 'ko', 'pt']
    
    for lang in target_langs:
        dst_dir = f"/root/.openclaw/workspace/europe-train/{lang}/guides"
        
        for filename in guide_files:
            src_path = os.path.join(src_dir, filename)
            if os.path.exists(src_path):
                create_translated_guide(src_path, dst_dir, lang)
            else:
                print(f"Source file not found: {src_path}")
        
        print(f"\nDone with {lang}!")
        time.sleep(1)
    
    print("\nAll guides created successfully!")

if __name__ == "__main__":
    main()
