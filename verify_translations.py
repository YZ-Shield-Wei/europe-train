#!/usr/bin/env python3
"""
Verify translation quality by sampling key elements.
"""

import os
import re

# Languages to verify
LANGUAGES = ['de', 'fr', 'es', 'ja', 'ko', 'pt']

# Key elements to check
CHECK_ELEMENTS = {
    'de': {
        'title': 'Beliebte',
        'nav': 'Startseite',
        'footer': 'Alle Rechte',
    },
    'fr': {
        'title': 'Populaires',
        'nav': 'Accueil',
        'footer': 'Tous droits',
    },
    'es': {
        'title': 'Populares',
        'nav': 'Inicio',
        'footer': 'Todos los derechos',
    },
    'ja': {
        'title': '人気',
        'nav': 'ホーム',
        'footer': 'All rights',
    },
    'ko': {
        'title': '인기',
        'nav': '홈',
        'footer': 'All rights',
    },
    'pt': {
        'title': 'Populares',
        'nav': 'Início',
        'footer': 'Todos os direitos',
    }
}

def verify_file(filepath, lang):
    """Verify a single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = CHECK_ELEMENTS.get(lang, {})
    results = {}
    
    for key, expected in checks.items():
        found = expected in content
        results[key] = '✓' if found else '✗'
    
    return results

def main():
    print('Translation Quality Verification')
    print('=' * 50)
    print()
    
    # Sample files to check
    sample_files = [
        'guides/popular-routes.html',
        'guides/ticket-buying-guide.html',
        'articles/france-tgv-guide.html',
        'index.html'
    ]
    
    for lang in LANGUAGES:
        print(f'{lang.upper()}:')
        for sample in sample_files:
            filepath = f'/root/.openclaw/workspace/europe-train/{lang}/{sample}'
            if os.path.exists(filepath):
                results = verify_file(filepath, lang)
                status = ' '.join([f'{k}:{v}' for k, v in results.items()])
                print(f'  {sample}: {status}')
        print()
    
    print('✅ Verification complete!')

if __name__ == '__main__':
    main()
