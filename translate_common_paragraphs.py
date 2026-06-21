#!/usr/bin/env python3
"""
Europe Train - 通用段落翻译脚本
覆盖最常见的描述性段落
"""

from pathlib import Path

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

# 通用段落翻译（适用于多篇文章）
COMMON_PARAGRAPHS = {
    'de': {
        'Book Sparpreis fares 2-3 months in advance for prices from €17.90. Use BahnCard 25 for additional 25% savings.': 'Buchen Sie Sparpreis-Tarife 2-3 Monate im Voraus für Preise ab €17,90. Nutzen Sie die BahnCard 25 für zusätzliche 25% Ersparnis.',
        'Yes, ICE trains run every hour with no changes required.': 'Ja, ICE-Züge fahren stündlich ohne Umstieg.',
        'Sparpreis fares from €17.90 with advance booking.': 'Sparpreis-Tarife ab €17,90 bei frühzeitiger Buchung.',
        'Book early for the best prices.': 'Buchen Sie früh für die besten Preise.',
        'Prices vary by season and demand.': 'Preise variieren je nach Saison und Nachfrage.',
    },
    'fr': {
        'Book Sparpreis fares 2-3 months in advance for prices from €17.90. Use BahnCard 25 for additional 25% savings.': 'Réservez les tarifs Sparpreis 2-3 mois à l\'avance pour des prix à partir de €17,90. Utilisez la BahnCard 25 pour 25% d\'économies supplémentaires.',
        'Yes, ICE trains run every hour with no changes required.': 'Oui, les trains ICE circulent toutes les heures sans correspondance.',
        'Sparpreis fares from €17.90 with advance booking.': 'Tarifs Sparpreis à partir de €17,90 avec réservation anticipée.',
        'Book early for the best prices.': 'Réservez tôt pour les meilleurs prix.',
        'Prices vary by season and demand.': 'Les prix varient selon la saison et la demande.',
    },
    'es': {
        'Book Sparpreis fares 2-3 months in advance for prices from €17.90. Use BahnCard 25 for additional 25% savings.': 'Reserve tarifas Sparpreis con 2-3 meses de anticipación para precios desde €17,90. Use la BahnCard 25 para un ahorro adicional del 25%.',
        'Yes, ICE trains run every hour with no changes required.': 'Sí, los trenes ICE circulan cada hora sin transbordos.',
        'Sparpreis fares from €17.90 with advance booking.': 'Tarifas Sparpreis desde €17,90 con reserva anticipada.',
        'Book early for the best prices.': 'Reserve con anticipación para obtener los mejores precios.',
        'Prices vary by season and demand.': 'Los precios varían según la temporada y la demanda.',
    },
    'ja': {
        'Book Sparpreis fares 2-3 months in advance for prices from €17.90. Use BahnCard 25 for additional 25% savings.': 'Sparpreis運賃を2〜3か月前に予約すると、€17.90からの価格が適用されます。BahnCard 25を利用すると、さらに25%割引になります。',
        'Yes, ICE trains run every hour with no changes required.': 'はい、ICE列車は毎時運行され、乗り換えは不要です。',
        'Sparpreis fares from €17.90 with advance booking.': '事前予約でSparpreis運賃が€17.90から。',
        'Book early for the best prices.': '早めに予約して最安値をゲット。',
        'Prices vary by season and demand.': '価格は季節と需要によって変動します。',
    },
    'ko': {
        'Book Sparpreis fares 2-3 months in advance for prices from €17.90. Use BahnCard 25 for additional 25% savings.': 'Sparpreis 요금을 2-3개월 전에 예약하면 €17.90부터 이용 가능합니다. BahnCard 25를 사용하면 추가 25% 할인이 적용됩니다.',
        'Yes, ICE trains run every hour with no changes required.': '네, ICE 열차는 매시간 운행되며 환승이 필요 없습니다.',
        'Sparpreis fares from €17.90 with advance booking.': '사전 예약 시 Sparpreis 요금은 €17.90부터 시작합니다.',
        'Book early for the best prices.': '최저가를 위해 미리 예약하세요.',
        'Prices vary by season and demand.': '가격은 계절과 수요에 따라 변동됩니다.',
    },
    'pt': {
        'Book Sparpreis fares 2-3 months in advance for prices from €17.90. Use BahnCard 25 for additional 25% savings.': 'Reserve tarifas Sparpreis com 2-3 meses de antecedência para preços a partir de €17,90. Use o BahnCard 25 para economia adicional de 25%.',
        'Yes, ICE trains run every hour with no changes required.': 'Sim, os trens ICE circulam a cada hora sem transbordos.',
        'Sparpreis fares from €17.90 with advance booking.': 'Tarifas Sparpreis a partir de €17,90 com reserva antecipada.',
        'Book early for the best prices.': 'Reserve cedo para os melhores preços.',
        'Prices vary by season and demand.': 'Os preços variam conforme a temporada e a demanda.',
    },
    'it': {
        'Book Sparpreis fares 2-3 months in advance for prices from €17.90. Use BahnCard 25 for additional 25% savings.': 'Prenotate le tariffe Sparpreis con 2-3 mesi di anticipo per prezzi a partire da €17,90. Utilizzate la BahnCard 25 per un risparmio aggiuntivo del 25%.',
        'Yes, ICE trains run every hour with no changes required.': 'Sì, i treni ICE circolano ogni ora senza cambi.',
        'Sparpreis fares from €17.90 with advance booking.': 'Tariffe Sparpreis da €17,90 con prenotazione anticipata.',
        'Book early for the best prices.': 'Prenotate in anticipo per i migliori prezzi.',
        'Prices vary by season and demand.': 'I prezzi variano in base alla stagione e alla domanda.',
    },
    'zh': {
        'Book Sparpreis fares 2-3 months in advance for prices from €17.90. Use BahnCard 25 for additional 25% savings.': '提前2-3个月预订Sparpreis票价，起价€17.90。使用BahnCard 25可额外节省25%。',
        'Yes, ICE trains run every hour with no changes required.': '是的，ICE列车每小时一班，无需换乘。',
        'Sparpreis fares from €17.90 with advance booking.': '提前预订Sparpreis票价从€17.90起。',
        'Book early for the best prices.': '提前预订以获取最佳价格。',
        'Prices vary by season and demand.': '价格因季节和需求而异。',
    }
}

def translate_common_paragraphs():
    """翻译通用段落"""
    print("🚀 开始翻译通用段落...")
    
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
            translations = COMMON_PARAGRAPHS.get(lang, {})
            
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
    translate_common_paragraphs()
