#!/usr/bin/env python3
"""
翻译文章中的描述性段落（lead 和 subtitle）
"""

from pathlib import Path

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

# 描述性段落翻译
LEAD_TRANSLATIONS = {
    'de': {
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': 'Die Strecke Berlin nach München ist Deutschlands belebteste Hochgeschwindigkeitsstrecke, die 623 km in nur 4 Stunden zurücklegt.',
        'Complete 2026 Guide | From €17.90': 'Kompletter Guide 2026 | Ab €17,90',
    },
    'fr': {
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': 'La route Berlin-Munich est le corridor ferroviaire à grande vitesse le plus fréquenté d\'Allemagne, couvrant 623 km en seulement 4 heures.',
        'Complete 2026 Guide | From €17.90': 'Guide Complet 2026 | À partir de €17,90',
    },
    'es': {
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': 'La ruta Berlín-Múnich es el corredor ferroviario de alta velocidad más concurrido de Alemania, cubriendo 623 km en solo 4 horas.',
        'Complete 2026 Guide | From €17.90': 'Guía Completa 2026 | Desde €17,90',
    },
    'ja': {
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': 'ベルリンからミュンヘンまでの路線は、ドイツで最も混雑する高速鉄道で、623kmをわずか4時間で結びます。',
        'Complete 2026 Guide | From €17.90': '完全ガイド 2026 | €17.90〜',
    },
    'ko': {
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': '베를린에서 뮌헨까지의 노선은 독일에서 가장 분주한 고속철도로, 623km를 단 4시간에 주행합니다.',
        'Complete 2026 Guide | From €17.90': '완벽 가이드 2026 | €17.90부터',
    },
    'pt': {
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': 'A rota Berlim-Munique é o corredor ferroviário de alta velocidade mais movimentado da Alemanha, cobrindo 623 km em apenas 4 horas.',
        'Complete 2026 Guide | From €17.90': 'Guia Completo 2026 | A partir de €17,90',
    },
    'it': {
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': 'La tratta Berlino-Monaco è il corridoio ferroviario ad alta velocità più trafficato della Germania, coprendo 623 km in sole 4 ore.',
        'Complete 2026 Guide | From €17.90': 'Guida Completa 2026 | Da €17,90',
    },
    'zh': {
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': '柏林到慕尼黑的路线是德国最繁忙的高速铁路走廊，仅4小时即可覆盖623公里。',
        'Complete 2026 Guide | From €17.90': '完整指南 2026 | 起价 €17.90',
    }
}

# subtitle 翻译
SUBTITLE_TRANSLATIONS = {
    'de': {
        '2026 latest: network, fare system, early-bird tips, seat selection, and SNCF app guide': '2026 Aktuell: Netzwerk, Tarifsystem, Frühbucher-Tipps, Sitzplatzwahl und SNCF-App-Guide',
        '2026 Latest: Which trains require reservations, fees, how to choose seats, and booking tips': '2026 Aktuell: Welche Züge erfordern Reservierungen, Gebühren, Sitzplatzwahl und Buchungstipps',
    },
    'fr': {
        '2026 latest: network, fare system, early-bird tips, seat selection, and SNCF app guide': '2026 Dernières infos: réseau, système tarifaire, conseils early-bird, sélection de sièges et guide app SNCF',
        '2026 Latest: Which trains require reservations, fees, how to choose seats, and booking tips': '2026 Dernières infos: quels trains nécessitent une réservation, frais, comment choisir ses sièges et conseils de réservation',
    },
    'es': {
        '2026 latest: network, fare system, early-bird tips, seat selection, and SNCF app guide': '2026 Última info: red, sistema tarifario, consejos early-bird, selección de asientos y guía de app SNCF',
        '2026 Latest: Which trains require reservations, fees, how to choose seats, and booking tips': '2026 Última info: qué trenes requieren reserva, tarifas, cómo elegir asientos y consejos de reserva',
    },
    'ja': {
        '2026 latest: network, fare system, early-bird tips, seat selection, and SNCF app guide': '2026最新：ネットワーク、料金システム、早割りのコツ、座席選択、SNCFアプリガイド',
        '2026 Latest: Which trains require reservations, fees, how to choose seats, and booking tips': '2026最新：予約が必要な列車、料金、座席の選び方、予約のコツ',
    },
    'ko': {
        '2026 latest: network, fare system, early-bird tips, seat selection, and SNCF app guide': '2026 최신: 네트워크, 요금 시스템, 얼리버드 팁, 좌석 선택, SNCF 앱 가이드',
        '2026 Latest: Which trains require reservations, fees, how to choose seats, and booking tips': '2026 최신: 예약이 필요한 열차, 수수료, 좌석 선택 방법, 예약 팁',
    },
    'pt': {
        '2026 latest: network, fare system, early-bird tips, seat selection, and SNCF app guide': '2026 Últimas: rede, sistema tarifário, dicas early-bird, seleção de assentos e guia do app SNCF',
        '2026 Latest: Which trains require reservations, fees, how to choose seats, and booking tips': '2026 Últimas: quais trens exigem reserva, taxas, como escolher assentos e dicas de reserva',
    },
    'it': {
        '2026 latest: network, fare system, early-bird tips, seat selection, and SNCF app guide': '2026 Ultimo: rete, sistema tariffario, consigli early-bird, selezione posti e guida app SNCF',
        '2026 Latest: Which trains require reservations, fees, how to choose seats, and booking tips': '2026 Ultimo: quali treni richiedono prenotazione, tariffe, come scegliere i posti e consigli di prenotazione',
    },
    'zh': {
        '2026 latest: network, fare system, early-bird tips, seat selection, and SNCF app guide': '2026最新：网络、票价系统、早鸟技巧、座位选择、SNCF应用指南',
        '2026 Latest: Which trains require reservations, fees, how to choose seats, and booking tips': '2026最新：哪些列车需要预订、费用、如何选座、预订技巧',
    }
}

def translate_leads_and_subtitles():
    """翻译 lead 和 subtitle 段落"""
    print("🚀 开始翻译 lead 和 subtitle 段落...")
    
    total_fixed = 0
    languages = ['de', 'fr', 'es', 'ja', 'ko', 'pt', 'it', 'zh']
    
    for lang in languages:
        lang_dir = BASE_DIR / lang / 'articles'
        if not lang_dir.exists():
            continue
        
        print(f"\n📁 翻译 {lang}...")
        lang_fixed = 0
        
        for article_file in lang_dir.glob('*.html'):
            with open(article_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 翻译 lead 段落
            lead_trans = LEAD_TRANSLATIONS.get(lang, {})
            for en_text, translated in lead_trans.items():
                content = content.replace(en_text, translated)
            
            # 翻译 subtitle 段落
            subtitle_trans = SUBTITLE_TRANSLATIONS.get(lang, {})
            for en_text, translated in subtitle_trans.items():
                content = content.replace(en_text, translated)
            
            if content != original:
                with open(article_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                lang_fixed += 1
        
        print(f"  ✅ {lang}: {lang_fixed} 个文件")
        total_fixed += lang_fixed
    
    print(f"\n✅ 总计: {total_fixed} 个文件已翻译")

if __name__ == '__main__':
    translate_leads_and_subtitles()
