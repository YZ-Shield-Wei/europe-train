#!/usr/bin/env python3
"""
Europe Train - 文章正文批量翻译脚本 v3
使用更全面的翻译字典
"""

import re
from pathlib import Path

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

# 扩展翻译映射 - 包含更多常见的标题和短语
ADDITIONAL_TRANSLATIONS = {
    'de': {
        'Seat Selection Recommendations': 'Sitzplatz-Empfehlungen',
        'Eurail Pass Reservation Guide': 'Eurail Pass Reservierungsguide',
        'Trains That Require Reservations': 'Züge mit Reservierungspflicht',
        'Trains That Do Not Require Reservations': 'Züge ohne Reservierungspflicht',
        'TGV Network': 'TGV-Netzwerk',
        'SNCF App Guide': 'SNCF App-Guide',
        'ICE Route Network': 'ICE-Streckennetz',
        'DB Navigator App Guide': 'DB Navigator App-Guide',
        'Frecciarossa vs italo Comparison': 'Frecciarossa vs italo Vergleich',
        'AVE Route Network': 'AVE-Streckennetz',
        'Glacier Express': 'Glacier Express',
        'Bernina Express': 'Bernina Express',
        'GoldenPass Line': 'GoldenPass Line',
        'Other Scenic Trains': 'Weitere Panoramazüge',
        'Route Information': 'Streckeninformation',
        'Immigration Process': 'Einwanderungsprozess',
        'Cost & Time Overview': 'Kosten- & Zeitübersicht',
        'TGV Lyria Experience in Detail': 'TGV Lyria Erlebnis im Detail',
        'Boarding: A Sense of Occasion': 'Einsteigen: Ein besonderer Moment',
        'Departure: From City to Countryside': 'Abfahrt: Von der Stadt ins Land',
        'Dining Car: A Moving French Bistro': 'Speisewagen: Ein französisches Bistro auf Schienen',
        'Scenery: Four Seasons in One Journey': 'Landschaft: Vier Jahreszeiten auf einer Reise',
        'Arrival: Seamless Connection': 'Ankunft: Nahtlose Verbindung',
        'Paris to Zurich: Train vs Flight vs Car – In-Depth Comparison': 'Paris nach Zürich: Zug vs Flug vs Auto – Detaillierter Vergleich',
        'Quick Verdict: Train Wins': 'Schnelles Urteil: Zug gewinnt',
        'Quick Verdict: The Most Pleasant Way to Travel Europe': 'Schnelles Urteil: Die angenehmste Art, Europa zu bereisen',
        'Pre-Boarding Ease': 'Komfort vor dem Einsteigen',
        'Onboard Amenities': 'Ausstattung an Bord',
        'Scenery Along the Way': 'Landschaft unterwegs',
        '1. EU Regulation EC 261/2004': '1. EU-Verordnung EG 261/2004',
        '2. Delay Compensation Standards by Country': '2. Verspätungsentschädigung nach Land',
        'Germany Deutsche Bahn': 'Deutschland Deutsche Bahn',
        'France SNCF': 'Frankreich SNCF',
        'Italy Trenitalia': 'Italien Trenitalia',
        'Switzerland SBB': 'Schweiz SBB',
        'Austria ÖBB': 'Österreich ÖBB',
        'Spain Renfe': 'Spanien Renfe',
        'UK National Rail': 'UK National Rail',
        'Netherlands NS': 'Niederlande NS',
        'Belgium NMBS/SNCB': 'Belgien NMBS/SNCB',
        'Quick Verdict: Rules Vary Widely': 'Schnelles Urteil: Regeln variieren stark',
        'France SNCF: The Most Complex System': 'Frankreich SNCF: Das komplexeste System',
        'Germany DB: Simple and Flexible': 'Deutschland DB: Einfach und flexibel',
        'Italy Trenitalia: Validation Required': 'Italien Trenitalia: Validierung erforderlich',
        'Switzerland SBB: Honor System': 'Schweiz SBB: Vertrauenssystem',
        'Spain Renfe: Security Check Required': 'Spanien Renfe: Sicherheitskontrolle erforderlich',
        'Austria ÖBB: Similar to Germany': 'Österreich ÖBB: Ähnlich wie Deutschland',
        'UK: No Validation, But Penalty Fares': 'UK: Keine Validierung, aber Strafgebühren',
        'Netherlands NS: Check-in/Check-out': 'Niederlande NS: Check-in/Check-out',
        'Belgium NMBS/SNCB: Simple System': 'Belgien NMBS/SNCB: Einfaches System',
        'General Tips': 'Allgemeine Tipps',
        'Paris, France': 'Paris, Frankreich',
        'Berlin, Germany': 'Berlin, Deutschland',
        'Rome, Italy': 'Rom, Italien',
        'Madrid, Spain': 'Madrid, Spanien',
        'Zurich, Switzerland': 'Zürich, Schweiz',
        'London, UK': 'London, UK',
        'Amsterdam, Netherlands': 'Amsterdam, Niederlande',
        'Vienna, Austria': 'Wien, Österreich',
        'Brussels, Belgium': 'Brüssel, Belgien',
        'Inter-station Transport in Major Cities': 'Bahnhofstransport in Großstädten',
        'Same-station transfer': 'Umstieg im selben Bahnhof',
        'Different-station transfer': 'Umstieg in verschiedenen Bahnhöfen',
    },
    'ja': {
        'Seat Selection Recommendations': '座席選択のおすすめ',
        'Eurail Pass Reservation Guide': 'Eurailパス予約ガイド',
        'Trains That Require Reservations': '予約が必要な列車',
        'Trains That Do Not Require Reservations': '予約不要の列車',
        'TGV Network': 'TGVネットワーク',
        'SNCF App Guide': 'SNCFアプリガイド',
        'ICE Route Network': 'ICE路線網',
        'DB Navigator App Guide': 'DB Navigatorアプリガイド',
        'Frecciarossa vs italo Comparison': 'Frecciarossa vs italo比較',
        'AVE Route Network': 'AVE路線網',
        'Glacier Express': 'グレイシャーエクスプレス',
        'Bernina Express': 'ベルニナエクスプレス',
        'GoldenPass Line': 'ゴールデンパスライン',
        'Other Scenic Trains': 'その他の観光列車',
        'Route Information': '路線情報',
        'Immigration Process': '出入境手続き',
        'Cost & Time Overview': '費用と時間の概要',
        'TGV Lyria Experience in Detail': 'TGVリリア体験詳細',
        'Boarding: A Sense of Occasion': '乗車：特別な瞬間',
        'Departure: From City to Countryside': '出発：都市から田舎へ',
        'Dining Car: A Moving French Bistro': '食堂車：走るフランスのビストロ',
        'Scenery: Four Seasons in One Journey': '景色：一度の旅で四季',
        'Arrival: Seamless Connection': '到着：シームレスな接続',
        'Paris to Zurich: Train vs Flight vs Car – In-Depth Comparison': 'パリからチューリッヒ：電車 vs 飛行機 vs 車 – 詳細比較',
        'Quick Verdict: Train Wins': '結論：電車の勝利',
        'Quick Verdict: The Most Pleasant Way to Travel Europe': '結論：ヨーロッパ旅行最適な方法',
        'Pre-Boarding Ease': '乗車前の便利さ',
        'Onboard Amenities': '車内設備',
        'Scenery Along the Way': '沿線の景色',
        '1. EU Regulation EC 261/2004': '1. EU規則EC 261/2004',
        '2. Delay Compensation Standards by Country': '2. 国別遅延補償基準',
        'Germany Deutsche Bahn': 'ドイツ Deutsche Bahn',
        'France SNCF': 'フランス SNCF',
        'Italy Trenitalia': 'イタリア Trenitalia',
        'Switzerland SBB': 'スイス SBB',
        'Austria ÖBB': 'オーストリア ÖBB',
        'Spain Renfe': 'スペイン Renfe',
        'UK National Rail': 'イギリス National Rail',
        'Netherlands NS': 'オランダ NS',
        'Belgium NMBS/SNCB': 'ベルギー NMBS/SNCB',
        'Quick Verdict: Rules Vary Widely': '結論：規則は国によって大きく異なる',
        'France SNCF: The Most Complex System': 'フランスSNCF：最も複雑なシステム',
        'Germany DB: Simple and Flexible': 'ドイツDB：シンプルで柔軟',
        'Italy Trenitalia: Validation Required': 'イタリアTrenitalia：確認が必要',
        'Switzerland SBB: Honor System': 'スイスSBB：信頼システム',
        'Spain Renfe: Security Check Required': 'スペインRenfe：セキュリティチェックが必要',
        'Austria ÖBB: Similar to Germany': 'オーストリアÖBB：ドイツと類似',
        'UK: No Validation, But Penalty Fares': 'イギリス：確認不要だが罰金あり',
        'Netherlands NS: Check-in/Check-out': 'オランダNS：チェックイン/アウト',
        'Belgium NMBS/SNCB: Simple System': 'ベルギーNMBS/SNCB：シンプルなシステム',
        'General Tips': '一般的なヒント',
        'Paris, France': 'フランス パリ',
        'Berlin, Germany': 'ドイツ ベルリン',
        'Rome, Italy': 'イタリア ローマ',
        'Madrid, Spain': 'スペイン マドリード',
        'Zurich, Switzerland': 'スイス チューリッヒ',
        'London, UK': 'イギリス ロンドン',
        'Amsterdam, Netherlands': 'オランダ アムステルダム',
        'Vienna, Austria': 'オーストリア ウィーン',
        'Brussels, Belgium': 'ベルギー ブリュッセル',
        'Inter-station Transport in Major Cities': '主要都市の駅間交通',
        'Same-station transfer': '同一駅乗り換え',
        'Different-station transfer': '別駅乗り換え',
    },
    'zh': {
        'Seat Selection Recommendations': '选座推荐',
        'Eurail Pass Reservation Guide': 'Eurail通票预订指南',
        'Trains That Require Reservations': '需要预订的列车',
        'Trains That Do Not Require Reservations': '无需预订的列车',
        'TGV Network': 'TGV网络',
        'SNCF App Guide': 'SNCF应用指南',
        'ICE Route Network': 'ICE线路网络',
        'DB Navigator App Guide': 'DB Navigator应用指南',
        'Frecciarossa vs italo Comparison': 'Frecciarossa与italo对比',
        'AVE Route Network': 'AVE线路网络',
        'Glacier Express': '冰川快车',
        'Bernina Express': '伯尔尼纳快车',
        'GoldenPass Line': '黄金列车线',
        'Other Scenic Trains': '其他景观列车',
        'Route Information': '线路信息',
        'Immigration Process': '出入境流程',
        'Cost & Time Overview': '费用与时间概览',
        'TGV Lyria Experience in Detail': 'TGV Lyria体验详情',
        'Boarding: A Sense of Occasion': '登车：仪式感',
        'Departure: From City to Countryside': '出发：从城市到乡村',
        'Dining Car: A Moving French Bistro': '餐车：移动的法式小酒馆',
        'Scenery: Four Seasons in One Journey': '风景：一趟旅程四季变换',
        'Arrival: Seamless Connection': '到达：无缝衔接',
        'Paris to Zurich: Train vs Flight vs Car – In-Depth Comparison': '巴黎到苏黎世：火车 vs 飞机 vs 汽车 – 深度对比',
        'Quick Verdict: Train Wins': '快速结论：火车胜出',
        'Quick Verdict: The Most Pleasant Way to Travel Europe': '快速结论：欧洲最舒适的旅行方式',
        'Pre-Boarding Ease': '登车前便利',
        'Onboard Amenities': '车上设施',
        'Scenery Along the Way': '沿途风景',
        '1. EU Regulation EC 261/2004': '1. 欧盟法规EC 261/2004',
        '2. Delay Compensation Standards by Country': '2. 各国延误赔偿标准',
        'Germany Deutsche Bahn': '德国 Deutsche Bahn',
        'France SNCF': '法国 SNCF',
        'Italy Trenitalia': '意大利 Trenitalia',
        'Switzerland SBB': '瑞士 SBB',
        'Austria ÖBB': '奥地利 ÖBB',
        'Spain Renfe': '西班牙 Renfe',
        'UK National Rail': '英国 National Rail',
        'Netherlands NS': '荷兰 NS',
        'Belgium NMBS/SNCB': '比利时 NMBS/SNCB',
        'Quick Verdict: Rules Vary Widely': '快速结论：规则差异很大',
        'France SNCF: The Most Complex System': '法国SNCF：最复杂的系统',
        'Germany DB: Simple and Flexible': '德国DB：简单灵活',
        'Italy Trenitalia: Validation Required': '意大利Trenitalia：需要验证',
        'Switzerland SBB: Honor System': '瑞士SBB：诚信制度',
        'Spain Renfe: Security Check Required': '西班牙Renfe：需要安检',
        'Austria ÖBB: Similar to Germany': '奥地利ÖBB：与德国类似',
        'UK: No Validation, But Penalty Fares': '英国：无需验证，但有罚款',
        'Netherlands NS: Check-in/Check-out': '荷兰NS：刷卡进出',
        'Belgium NMBS/SNCB: Simple System': '比利时NMBS/SNCB：简单系统',
        'General Tips': '通用提示',
        'Paris, France': '法国巴黎',
        'Berlin, Germany': '德国柏林',
        'Rome, Italy': '意大利罗马',
        'Madrid, Spain': '西班牙马德里',
        'Zurich, Switzerland': '瑞士苏黎世',
        'London, UK': '英国伦敦',
        'Amsterdam, Netherlands': '荷兰阿姆斯特丹',
        'Vienna, Austria': '奥地利维也纳',
        'Brussels, Belgium': '比利时布鲁塞尔',
        'Inter-station Transport in Major Cities': '主要城市车站间交通',
        'Same-station transfer': '同站换乘',
        'Different-station transfer': '异站换乘',
    }
}

def translate_additional_content(filepath, lang):
    """翻译额外的内容"""
    if lang == 'en':
        return 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    translations = ADDITIONAL_TRANSLATIONS.get(lang, {})
    
    for en_text, translated in translations.items():
        content = content.replace(f'<h2>{en_text}</h2>', f'<h2>{translated}</h2>')
        content = content.replace(f'<h3>{en_text}</h3>', f'<h3>{translated}</h3>')
        content = content.replace(f'<strong>{en_text}:</strong>', f'<strong>{translated}:</strong>')
        content = content.replace(f'<p>{en_text}</p>', f'<p>{translated}</p>')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1
    return 0

def translate_all_additional():
    """批量翻译额外内容"""
    print("🚀 开始批量翻译额外内容...")
    
    total_fixed = 0
    languages = ['de', 'fr', 'es', 'ja', 'ko', 'pt', 'it', 'zh']
    
    for lang in languages:
        lang_dir = BASE_DIR / lang / 'articles'
        if not lang_dir.exists():
            continue
        
        print(f"\n📁 翻译 {lang} 额外内容...")
        lang_fixed = 0
        
        for article_file in lang_dir.glob('*.html'):
            if article_file.name == 'index.html':
                continue
            if translate_additional_content(article_file, lang):
                lang_fixed += 1
                print(f"  ✓ {article_file.name}")
        
        print(f"  ✅ {lang}: {lang_fixed} 篇文章已更新")
        total_fixed += lang_fixed
    
    print(f"\n✅ 总计: {total_fixed} 篇文章已更新")

if __name__ == '__main__':
    translate_all_additional()
