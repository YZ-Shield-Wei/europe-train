#!/usr/bin/env python3
"""
Translate index.html for all languages.
"""

import os

# Translation dictionaries for index.html
INDEX_TRANSLATIONS = {
    'de': {
        'Explore Europe by Train': 'Europa mit dem Zug erkunden',
        'Your complete guide to European rail travel': 'Ihr kompletter Guide für europäische Zugreisen',
        'Search destinations, routes, or train types...': 'Ziele, Routen oder Zugtypen suchen...',
        'Search': 'Suchen',
        'Why Travel by Train?': 'Warum mit dem Zug reisen?',
        'Eco-Friendly': 'Umweltfreundlich',
        'Comfortable': 'Komfortabel',
        'City Center to City Center': 'Stadtzentrum zu Stadtzentrum',
        'Cost Effective': 'Kostengünstig',
        'European Rail Travel Data': 'Europäische Zugreisedaten',
        'Countries Covered': 'Länder abgedeckt',
        'Kilometers of Rail Network': 'Kilometer Schienennetz',
        'Daily Train Services': 'Tägliche Zugdienste',
        'Less Carbon vs Flights': 'Weniger CO₂ als Flüge',
        'Popular Routes': 'Beliebte Strecken',
        'Travel Guides': 'Reiseführer',
        'All rights reserved': 'Alle Rechte vorbehalten',
    },
    'fr': {
        'Explore Europe by Train': 'Explorer l\'Europe en Train',
        'Your complete guide to European rail travel': 'Votre guide complet des voyages en train en Europe',
        'Search destinations, routes, or train types...': 'Rechercher des destinations, itinéraires...',
        'Search': 'Rechercher',
        'Why Travel by Train?': 'Pourquoi voyager en train ?',
        'Eco-Friendly': 'Écologique',
        'Comfortable': 'Confortable',
        'City Center to City Center': 'Centre-ville à centre-ville',
        'Cost Effective': 'Économique',
        'European Rail Travel Data': 'Données sur les voyages en train en Europe',
        'Countries Covered': 'Pays couverts',
        'Kilometers of Rail Network': 'Kilomètres de réseau ferroviaire',
        'Daily Train Services': 'Services de train quotidiens',
        'Less Carbon vs Flights': 'Moins de CO₂ que les vols',
        'Popular Routes': 'Routes Populaires',
        'Travel Guides': 'Guides de Voyage',
        'All rights reserved': 'Tous droits réservés',
    },
    'es': {
        'Explore Europe by Train': 'Explora Europa en Tren',
        'Your complete guide to European rail travel': 'Tu guía completa para viajar en tren por Europa',
        'Search destinations, routes, or train types...': 'Buscar destinos, rutas o tipos de tren...',
        'Search': 'Buscar',
        'Why Travel by Train?': '¿Por qué viajar en tren?',
        'Eco-Friendly': 'Ecológico',
        'Comfortable': 'Cómodo',
        'City Center to City Center': 'Centro a centro',
        'Cost Effective': 'Económico',
        'European Rail Travel Data': 'Datos de viajes en tren por Europa',
        'Countries Covered': 'Países cubiertos',
        'Kilometers of Rail Network': 'Kilómetros de red ferroviaria',
        'Daily Train Services': 'Servicios diarios de tren',
        'Less Carbon vs Flights': 'Menos CO₂ que los vuelos',
        'Popular Routes': 'Rutas Populares',
        'Travel Guides': 'Guías de Viaje',
        'All rights reserved': 'Todos los derechos reservados',
    },
    'ja': {
        'Explore Europe by Train': '鉄道で欧州を探索',
        'Your complete guide to European rail travel': '欧州鉄道旅行の完全ガイド',
        'Search destinations, routes, or train types...': '目的地、ルート、列車タイプを検索...',
        'Search': '検索',
        'Why Travel by Train?': 'なぜ鉄道で旅行するのか？',
        'Eco-Friendly': 'エコフレンドリー',
        'Comfortable': '快適',
        'City Center to City Center': '中心部から中心部へ',
        'Cost Effective': 'コスト効率',
        'European Rail Travel Data': '欧州鉄道旅行データ',
        'Countries Covered': '対象国',
        'Kilometers of Rail Network': '鉄道ネットワーク距離',
        'Daily Train Services': '毎日の列車サービス',
        'Less Carbon vs Flights': '飛行機より90%少ないCO₂',
        'Popular Routes': '人気ルート',
        'Travel Guides': '旅行ガイド',
        'All rights reserved': 'All rights reserved',
    },
    'ko': {
        'Explore Europe by Train': '기차로 유럽 탐험',
        'Your complete guide to European rail travel': '유럽 기차 여행 완벽 가이드',
        'Search destinations, routes, or train types...': '목적지, 경로, 기차 유형 검색...',
        'Search': '검색',
        'Why Travel by Train?': '왜 기차로 여행할까요?',
        'Eco-Friendly': '친환경',
        'Comfortable': '편안함',
        'City Center to City Center': '도심에서 도심으로',
        'Cost Effective': '비용 효율',
        'European Rail Travel Data': '유럽 기차 여행 데이터',
        'Countries Covered': '포함 국가',
        'Kilometers of Rail Network': '철도 네트워크 거리',
        'Daily Train Services': '일일 기차 서비스',
        'Less Carbon vs Flights': '비행기보다 90% 적은 CO₂',
        'Popular Routes': '인기 경로',
        'Travel Guides': '여행 가이드',
        'All rights reserved': 'All rights reserved',
    },
    'pt': {
        'Explore Europe by Train': 'Explore a Europa de Trem',
        'Your complete guide to European rail travel': 'Seu guia completo para viagens de trem na Europa',
        'Search destinations, routes, or train types...': 'Pesquisar destinos, rotas ou tipos de trem...',
        'Search': 'Pesquisar',
        'Why Travel by Train?': 'Por que viajar de trem?',
        'Eco-Friendly': 'Ecológico',
        'Comfortable': 'Confortável',
        'City Center to City Center': 'Centro a centro',
        'Cost Effective': 'Econômico',
        'European Rail Travel Data': 'Dados de viagens de trem na Europa',
        'Countries Covered': 'Países cobertos',
        'Kilometers of Rail Network': 'Quilômetros de rede ferroviária',
        'Daily Train Services': 'Serviços diários de trem',
        'Less Carbon vs Flights': 'Menos CO₂ que voos',
        'Popular Routes': 'Rotas Populares',
        'Travel Guides': 'Guias de Viagem',
        'All rights reserved': 'Todos os direitos reservados',
    }
}

def translate_index(lang):
    """Translate index.html for a specific language"""
    src_path = '/root/.openclaw/workspace/europe-train/en/index.html'
    dst_path = f'/root/.openclaw/workspace/europe-train/{lang}/index.html'
    
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get translations
    trans = INDEX_TRANSLATIONS.get(lang, {})
    
    # Replace translations
    for en_text, translated in trans.items():
        content = content.replace(en_text, translated)
    
    # Update lang attribute
    content = content.replace('lang="en"', f'lang="{lang}"')
    
    # Write translated file
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'  ✓ Translated {lang}/index.html')
    return True

def main():
    print('Translating index.html for all languages...')
    print()
    
    for lang in ['de', 'fr', 'es', 'ja', 'ko', 'pt']:
        translate_index(lang)
    
    print()
    print('✅ Complete! Translated index.html for all languages.')

if __name__ == '__main__':
    main()
