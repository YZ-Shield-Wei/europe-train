#!/usr/bin/env python3
"""
Translate articles directory to 6 languages.
"""

import os
import re

# Translation dictionaries for each language
TRANSLATIONS = {
    'de': {
        'European Train Travel Guides': 'Europäische Zug-Reiseführer',
        'Expert guides for European train travel': 'Experten-Guides für europäische Zugreisen',
        'How to Buy Tickets': 'Wie man Tickets kauft',
        'Popular Routes': 'Beliebte Strecken',
        'Rail Passes': 'Rail Pässe',
        'Train Experience': 'Zug-Erlebnis',
        'Updated': 'Aktualisiert',
        'Read more': 'Mehr lesen',
        'Related Guides': 'Verwandte Guides',
        'All rights reserved': 'Alle Rechte vorbehalten',
        'Home': 'Startseite',
        'Guides': 'Guides',
        'Articles': 'Artikel',
        'Live Status': 'Live-Status',
    },
    'fr': {
        'European Train Travel Guides': 'Guides de Voyage en Train Européen',
        'Expert guides for European train travel': 'Guides experts pour les voyages en train en Europe',
        'How to Buy Tickets': 'Comment Acheter des Billets',
        'Popular Routes': 'Routes Populaires',
        'Rail Passes': 'Pass Ferroviaires',
        'Train Experience': 'Expérience Train',
        'Updated': 'Mis à jour',
        'Read more': 'Lire la suite',
        'Related Guides': 'Guides Connexes',
        'All rights reserved': 'Tous droits réservés',
        'Home': 'Accueil',
        'Guides': 'Guides',
        'Articles': 'Articles',
        'Live Status': 'Statut en Direct',
    },
    'es': {
        'European Train Travel Guides': 'Guías de Viaje en Tren Europeo',
        'Expert guides for European train travel': 'Guías expertas para viajes en tren por Europa',
        'How to Buy Tickets': 'Cómo Comprar Billetes',
        'Popular Routes': 'Rutas Populares',
        'Rail Passes': 'Pases Ferroviarios',
        'Train Experience': 'Experiencia de Tren',
        'Updated': 'Actualizado',
        'Read more': 'Leer más',
        'Related Guides': 'Guías Relacionadas',
        'All rights reserved': 'Todos los derechos reservados',
        'Home': 'Inicio',
        'Guides': 'Guías',
        'Articles': 'Artículos',
        'Live Status': 'Estado en Vivo',
    },
    'ja': {
        'European Train Travel Guides': '欧州鉄道旅行ガイド',
        'Expert guides for European train travel': '欧州鉄道旅行の専門ガイド',
        'How to Buy Tickets': '切符の購入方法',
        'Popular Routes': '人気ルート',
        'Rail Passes': '鉄道パス',
        'Train Experience': '鉄道体験',
        'Updated': '更新',
        'Read more': '続きを読む',
        'Related Guides': '関連ガイド',
        'All rights reserved': 'All rights reserved',
        'Home': 'ホーム',
        'Guides': 'ガイド',
        'Articles': '記事',
        'Live Status': 'ライブ状況',
    },
    'ko': {
        'European Train Travel Guides': '유럽 기차 여행 가이드',
        'Expert guides for European train travel': '유럽 기차 여행 전문 가이드',
        'How to Buy Tickets': '티켓 구매 방법',
        'Popular Routes': '인기 경로',
        'Rail Passes': '철도 패스',
        'Train Experience': '기차 여행 경험',
        'Updated': '업데이트',
        'Read more': '더 읽기',
        'Related Guides': '관련 가이드',
        'All rights reserved': 'All rights reserved',
        'Home': '홈',
        'Guides': '가이드',
        'Articles': '기사',
        'Live Status': '실시간 상태',
    },
    'pt': {
        'European Train Travel Guides': 'Guias de Viagem de Trem Europeu',
        'Expert guides for European train travel': 'Guias especializados para viagens de trem na Europa',
        'How to Buy Tickets': 'Como Comprar Bilhetes',
        'Popular Routes': 'Rotas Populares',
        'Rail Passes': 'Passes Ferroviários',
        'Train Experience': 'Experiência de Trem',
        'Updated': 'Atualizado',
        'Read more': 'Ler mais',
        'Related Guides': 'Guias Relacionados',
        'All rights reserved': 'Todos os direitos reservados',
        'Home': 'Início',
        'Guides': 'Guias',
        'Articles': 'Artigos',
        'Live Status': 'Status ao Vivo',
    }
}

# Articles to translate (excluding index.html)
ARTICLES_FILES = [
    'delay-compensation-guide.html',
    'europe-train-ticket-rules.html',
    'france-tgv-guide.html',
    'germany-ice-guide.html',
    'italy-frecciarossa-guide.html',
    'london-paris-eurostar-guide.html',
    'paris-zurich-train-vs-flight.html',
    'seat-reservation-guide.html',
    'spain-ave-guide.html',
    'swiss-scenic-trains.html',
    'tgv-lyria-experience.html',
    'train-apps-comparison.html',
    'train-station-guide.html'
]

def translate_file(lang, filename):
    """Translate a single article file"""
    src_path = f'/root/.openclaw/workspace/europe-train/en/articles/{filename}'
    
    if not os.path.exists(src_path):
        print(f'  ✗ Source file not found: {src_path}')
        return False
    
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get translations for this language
    trans = TRANSLATIONS.get(lang, {})
    
    # Replace all occurrences
    for en_text, translated in trans.items():
        content = content.replace(en_text, translated)
    
    # Update lang attribute
    content = content.replace('lang="en"', f'lang="{lang}"')
    
    # Update hreflang links
    content = content.replace('hreflang="en"', f'hreflang="{lang}"')
    
    # Update navigation links
    content = content.replace('href="/"', f'href="/{lang}/"')
    content = content.replace('href="/guides/"', f'href="/{lang}/guides/"')
    content = content.replace('href="/articles/"', f'href="/{lang}/articles/"')
    content = content.replace('href="/live-status.html"', f'href="/{lang}/live-status.html"')
    
    # Update article links
    content = content.replace('href="/articles/', f'href="/{lang}/articles/')
    content = content.replace('href="/guides/', f'href="/{lang}/guides/')
    
    # Write translated file
    output_dir = f'/root/.openclaw/workspace/europe-train/{lang}/articles'
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = f'{output_dir}/{filename}'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'  ✓ {lang}/articles/{filename}')
    return True

def main():
    print('Starting articles translation...')
    print(f'Target languages: {list(TRANSLATIONS.keys())}')
    print(f'Files: {ARTICLES_FILES}')
    print()
    
    total_files = 0
    for lang in TRANSLATIONS.keys():
        print(f'Translating to {lang}...')
        for filename in ARTICLES_FILES:
            if translate_file(lang, filename):
                total_files += 1
        print()
    
    print(f'✅ Complete! Translated {total_files} files.')
    print(f'Output: /root/.openclaw/workspace/europe-train/{{lang}}/articles/')

if __name__ == '__main__':
    main()