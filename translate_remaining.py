#!/usr/bin/env python3
"""
批量翻译所有语言文章中剩余的英文段落
使用简单但有效的字符串替换
"""

import re
from pathlib import Path

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

# 定义各语言需要翻译的常见英文段落
TRANSLATIONS = {
    'de': {
        'Travel from Berlin to Munich by train from €17.90. ICE high-speed route, booking tips, and money-saving strategies for 2026.': 'Reisen Sie mit dem Zug von Berlin nach München ab €17,90. ICE-Hochgeschwindigkeitsstrecke, Buchungstipps und Spartipps für 2026.',
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': 'Die Strecke Berlin-München ist Deutschlands belebteste Hochgeschwindigkeitsstrecke, die 623 km in nur 4 Stunden zurücklegt.',
        'Complete 2026 Guide | From €17.90': 'Kompletter Guide 2026 | Ab €17,90',
        'Yes, ICE trains run every hour with no changes required.': 'Ja, ICE-Züge fahren stündlich ohne Umstieg.',
        'Sparpreis fares from €17.90 with advance booking.': 'Sparpreis-Tarife ab €17,90 bei frühzeitiger Buchung.',
        'Book early for the best prices.': 'Buchen Sie früh für die besten Preise.',
        'Prices vary by season and demand.': 'Preise variieren je nach Saison und Nachfrage.',
    },
    'fr': {
        'Travel from Berlin to Munich by train from €17.90. ICE high-speed route, booking tips, and money-saving strategies for 2026.': 'Voyagez de Berlin à Munich en train à partir de €17,90. Route ICE à grande vitesse, conseils de réservation et astuces pour économiser pour 2026.',
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': 'La route Berlin-Munich est le corridor ferroviaire à grande vitesse le plus fréquenté d\'Allemagne, couvrant 623 km en seulement 4 heures.',
        'Complete 2026 Guide | From €17.90': 'Guide Complet 2026 | À partir de €17,90',
        'Yes, ICE trains run every hour with no changes required.': 'Oui, les trains ICE circulent toutes les heures sans correspondance.',
        'Sparpreis fares from €17.90 with advance booking.': 'Tarifs Sparpreis à partir de €17,90 avec réservation anticipée.',
        'Book early for the best prices.': 'Réservez tôt pour les meilleurs prix.',
        'Prices vary by season and demand.': 'Les prix varient selon la saison et la demande.',
    },
    'es': {
        'Travel from Berlin to Munich by train from €17.90. ICE high-speed route, booking tips, and money-saving strategies for 2026.': 'Viaje de Berlín a Múnich en tren desde €17,90. Ruta ICE de alta velocidad, consejos de reserva y estrategias de ahorro para 2026.',
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': 'La ruta Berlín-Múnich es el corredor ferroviario de alta velocidad más concurrido de Alemania, cubriendo 623 km en solo 4 horas.',
        'Complete 2026 Guide | From €17.90': 'Guía Completa 2026 | Desde €17,90',
        'Yes, ICE trains run every hour with no changes required.': 'Sí, los trenes ICE circulan cada hora sin transbordos.',
        'Sparpreis fares from €17.90 with advance booking.': 'Tarifas Sparpreis desde €17,90 con reserva anticipada.',
        'Book early for the best prices.': 'Reserve con anticipación para obtener los mejores precios.',
        'Prices vary by season and demand.': 'Los precios varían según la temporada y la demanda.',
    },
    'ja': {
        'Travel from Berlin to Munich by train from €17.90. ICE high-speed route, booking tips, and money-saving strategies for 2026.': 'ベルリンからミュンヘンまで電車で€17.90から。ICE高速ルート、予約のコツ、節約術2026。',
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': 'ベルリンからミュンヘンまでの路線は、ドイツで最も混雑する高速鉄道で、623kmをわずか4時間で結びます。',
        'Complete 2026 Guide | From €17.90': '完全ガイド 2026 | €17.90〜',
        'Yes, ICE trains run every hour with no changes required.': 'はい、ICE列車は毎時運行され、乗り換えは不要です。',
        'Sparpreis fares from €17.90 with advance booking.': '事前予約でSparpreis運賃が€17.90から。',
        'Book early for the best prices.': '早めに予約して最安値をゲット。',
        'Prices vary by season and demand.': '価格は季節と需要によって変動します。',
    },
    'ko': {
        'Travel from Berlin to Munich by train from €17.90. ICE high-speed route, booking tips, and money-saving strategies for 2026.': '베를린에서 뮌헨까지 기차로 €17.90부터. ICE 고속 노선, 예약 팁, 절약 전략 2026.',
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': '베를린에서 뮌헨까지의 노선은 독일에서 가장 분주한 고속철도로, 623km를 단 4시간에 주행합니다.',
        'Complete 2026 Guide | From €17.90': '완벽 가이드 2026 | €17.90부터',
        'Yes, ICE trains run every hour with no changes required.': '네, ICE 열차는 매시간 운행되며 환승이 필요 없습니다.',
        'Sparpreis fares from €17.90 with advance booking.': '사전 예약 시 Sparpreis 요금은 €17.90부터 시작합니다.',
        'Book early for the best prices.': '최저가를 위해 미리 예약하세요.',
        'Prices vary by season and demand.': '가격은 계절과 수요에 따라 변동됩니다.',
    },
    'pt': {
        'Travel from Berlin to Munich by train from €17.90. ICE high-speed route, booking tips, and money-saving strategies for 2026.': 'Viaje de Berlim a Munique de trem a partir de €17,90. Rota ICE de alta velocidade, dicas de reserva e estratégias de economia para 2026.',
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': 'A rota Berlim-Munique é o corredor ferroviário de alta velocidade mais movimentado da Alemanha, cobrindo 623 km em apenas 4 horas.',
        'Complete 2026 Guide | From €17.90': 'Guia Completo 2026 | A partir de €17,90',
        'Yes, ICE trains run every hour with no changes required.': 'Sim, os trens ICE circulam a cada hora sem transbordos.',
        'Sparpreis fares from €17.90 with advance booking.': 'Tarifas Sparpreis a partir de €17,90 com reserva antecipada.',
        'Book early for the best prices.': 'Reserve cedo para os melhores preços.',
        'Prices vary by season and demand.': 'Os preços variam conforme a temporada e a demanda.',
    },
    'it': {
        'Travel from Berlin to Munich by train from €17.90. ICE high-speed route, booking tips, and money-saving strategies for 2026.': 'Viaggiare da Berlino a Monaco in treno a partire da €17,90. Percorso ICE ad alta velocità, consigli di prenotazione e strategie di risparmio per il 2026.',
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': 'La tratta Berlino-Monaco è il corridoio ferroviario ad alta velocità più trafficato della Germania, coprendo 623 km in sole 4 ore.',
        'Complete 2026 Guide | From €17.90': 'Guida Completa 2026 | Da €17,90',
        'Yes, ICE trains run every hour with no changes required.': 'Sì, i treni ICE circolano ogni ora senza cambi.',
        'Sparpreis fares from €17.90 with advance booking.': 'Tariffe Sparpreis da €17,90 con prenotazione anticipata.',
        'Book early for the best prices.': 'Prenotate in anticipo per i migliori prezzi.',
        'Prices vary by season and demand.': 'I prezzi variano in base alla stagione e alla domanda.',
    },
    'zh': {
        'Travel from Berlin to Munich by train from €17.90. ICE high-speed route, booking tips, and money-saving strategies for 2026.': '乘坐火车从柏林到慕尼黑，起价€17.90。ICE高速路线、预订技巧和省钱攻略2026。',
        'The Berlin to Munich route is Germany\'s busiest high-speed rail corridor, covering 623km in just 4 hours.': '柏林到慕尼黑的路线是德国最繁忙的高速铁路走廊，仅4小时即可覆盖623公里。',
        'Complete 2026 Guide | From €17.90': '完整指南 2026 | 起价 €17.90',
        'Yes, ICE trains run every hour with no changes required.': '是的，ICE列车每小时一班，无需换乘。',
        'Sparpreis fares from €17.90 with advance booking.': '提前预订Sparpreis票价从€17.90起。',
        'Book early for the best prices.': '提前预订以获取最佳价格。',
        'Prices vary by season and demand.': '价格因季节和需求而异。',
    }
}

def translate_remaining_paragraphs():
    """翻译所有语言中剩余的英文段落"""
    print("🚀 开始批量翻译剩余英文段落...")
    
    total_fixed = 0
    
    for lang, translations in TRANSLATIONS.items():
        lang_dir = BASE_DIR / lang / 'articles'
        if not lang_dir.exists():
            continue
        
        print(f"\n📁 翻译 {lang}...")
        lang_fixed = 0
        
        for article_file in lang_dir.glob('*.html'):
            with open(article_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            for en_text, translated in translations.items():
                content = content.replace(en_text, translated)
            
            if content != original:
                with open(article_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                lang_fixed += 1
        
        print(f"  ✅ {lang}: {lang_fixed} 个文件")
        total_fixed += lang_fixed
    
    print(f"\n✅ 总计: {total_fixed} 个文件已翻译")

if __name__ == '__main__':
    translate_remaining_paragraphs()
