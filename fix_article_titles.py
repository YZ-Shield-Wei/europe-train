#!/usr/bin/env python3
"""
批量修复文章标题翻译
为每种语言的文章页面添加翻译后的标题
"""

import re
from pathlib import Path

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

# 文章标题翻译映射
ARTICLE_TITLES = {
    'berlin-to-munich-train-guide.html': {
        'de': 'Berlin nach München mit dem Zug',
        'fr': 'Berlin à Munich en Train',
        'es': 'Berlín a Múnich en Tren',
        'ja': 'ベルリンからミュンヘンまで電車で',
        'ko': '베를린에서 뮌헨까지 기차로',
        'pt': 'Berlim a Munique de Trem',
        'it': 'Berlino a Monaco in Treno',
        'zh': '柏林到慕尼黑火车指南',
    },
    'delay-compensation-guide.html': {
        'de': 'Leitfaden zur Zugverspätungsentschädigung',
        'fr': 'Guide d\'Indemnisation pour Retards de Train',
        'es': 'Guía de Compensación por Retrasos de Tren',
        'ja': '列車遅延補償ガイド',
        'ko': '열차 지연 보상 가이드',
        'pt': 'Guia de Compensação por Atraso de Trem',
        'it': 'Guida al Rimborso per Ritardi dei Treni',
        'zh': '火车延误赔偿指南',
    },
    'europe-train-ticket-rules.html': {
        'de': 'Vollständiger Leitfaden zu europäischen Zugticketregeln',
        'fr': 'Guide Complet des Règles de Billets de Train Européens',
        'es': 'Guía Completa de Reglas de Billetes de Tren Europeos',
        'ja': '欧州鉄道切符規則完全ガイド',
        'ko': '유럽 기차 티켓 규칙 완벽 가이드',
        'pt': 'Guia Completo das Regras de Bilhetes de Trem Europeus',
        'it': 'Guida Completa alle Regole dei Biglietti del Treno Europeo',
        'zh': '欧洲火车票规则完整指南',
    },
    'france-tgv-guide.html': {
        'de': 'Vollständiger Leitfaden zum französischen TGV',
        'fr': 'Guide Complet du TGV Français',
        'es': 'Guía Completa del TGV Francés',
        'ja': 'フランスTGV完全ガイド',
        'ko': '프랑스 TGV 완벽 가이드',
        'pt': 'Guia Completo do TGV Francês',
        'it': 'Guida Completa al TGV Francese',
        'zh': '法国TGV高铁完整指南',
    },
    'germany-ice-guide.html': {
        'de': 'Leitfaden zum deutschen ICE-Hochgeschwindigkeitszug',
        'fr': 'Guide du Train à Grande Vitesse ICE Allemand',
        'es': 'Guía del Tren de Alta Velocidad ICE Alemán',
        'ja': 'ドイツICE高速列車ガイド',
        'ko': '독일 ICE 고속열차 가이드',
        'pt': 'Guia do Trem de Alta Velocidade ICE Alemão',
        'it': 'Guida al Treno ad Alta Velocità ICE Tedesco',
        'zh': '德国ICE高速列车指南',
    },
    'italy-frecciarossa-guide.html': {
        'de': 'Leitfaden zum italienischen Frecciarossa',
        'fr': 'Guide du Frecciarossa Italien',
        'es': 'Guía del Frecciarossa Italiano',
        'ja': 'イタリアフレッチャロッサガイド',
        'ko': '이탈리아 프레차로사 가이드',
        'pt': 'Guia do Frecciarossa Italiano',
        'it': 'Guida al Frecciarossa Italiano',
        'zh': '意大利Frecciarossa指南',
    },
    'london-paris-eurostar-guide.html': {
        'de': 'London nach Paris mit dem Eurostar',
        'fr': 'Londres à Paris en Eurostar',
        'es': 'Londres a París en Eurostar',
        'ja': 'ロンドンからパリまでユーロスターで',
        'ko': '런던에서 파리까지 유로스타로',
        'pt': 'Londres a Paris de Eurostar',
        'it': 'Londra a Parigi con Eurostar',
        'zh': '伦敦到巴黎欧洲之星指南',
    },
    'paris-to-rome-train-guide.html': {
        'de': 'Paris nach Rom mit dem Zug',
        'fr': 'Paris à Rome en Train',
        'es': 'París a Roma en Tren',
        'ja': 'パリからローマまで電車で',
        'ko': '파리에서 로마까지 기차로',
        'pt': 'Paris a Roma de Trem',
        'it': 'Parigi a Roma in Treno',
        'zh': '巴黎到罗马火车指南',
    },
    'paris-zurich-train-vs-flight.html': {
        'de': 'Paris nach Zürich: Zug vs Flug vs Auto',
        'fr': 'Paris à Zurich : Train vs Avion vs Voiture',
        'es': 'París a Zúrich: Tren vs Vuelo vs Coche',
        'ja': 'パリからチューリッヒ：電車 vs 飛行機 vs 車',
        'ko': '파리에서 취리히까지: 기차 vs 비행기 vs 자동차',
        'pt': 'Paris a Zurique: Trem vs Voo vs Carro',
        'it': 'Parigi a Zurigo: Treno vs Aereo vs Auto',
        'zh': '巴黎到苏黎世：火车 vs 飞机 vs 汽车',
    },
    'seat-reservation-guide.html': {
        'de': 'Vollständiger Leitfaden zu Sitzplatzreservierungen',
        'fr': 'Guide Complet des Réservations de Sièges',
        'es': 'Guía Completa de Reservas de Asientos',
        'ja': '座席予約完全ガイド',
        'ko': '좌석 예약 완벽 가이드',
        'pt': 'Guia Completo de Reservas de Assentos',
        'it': 'Guida Completa alle Prenotazioni dei Posti',
        'zh': '座位预订完整指南',
    },
    'spain-ave-guide.html': {
        'de': 'Leitfaden zum spanischen AVE-Hochgeschwindigkeitszug',
        'fr': 'Guide du Train à Grande Vitesse AVE Espagnol',
        'es': 'Guía del Tren de Alta Velocidad AVE Español',
        'ja': 'スペインAVE高速列車ガイド',
        'ko': '스페인 AVE 고속열차 가이드',
        'pt': 'Guia do Trem de Alta Velocidade AVE Espanhol',
        'it': 'Guida al Treno ad Alta Velocità AVE Spagnolo',
        'zh': '西班牙AVE高速列车指南',
    },
    'swiss-scenic-trains.html': {
        'de': 'Leitfaden zu den Schweizer Panoramazügen',
        'fr': 'Guide des Trains Panoramiques Suisses',
        'es': 'Guía de los Trenes Panorámicos Suizos',
        'ja': 'スイス観光列車ガイド',
        'ko': '스위스 관광열차 가이드',
        'pt': 'Guia dos Trens Panorâmicos Suíços',
        'it': 'Guida ai Treni Panoramici Svizzera',
        'zh': '瑞士景观列车指南',
    },
    'tgv-lyria-experience.html': {
        'de': 'TGV Lyria Erlebnis: Eine entspannende Reise von Paris nach Lausanne',
        'fr': 'Expérience TGV Lyria : Un Voyage Relaxant de Paris à Lausanne',
        'es': 'Experiencia TGV Lyria: Un Viaje Relajante de París a Lausana',
        'ja': 'TGVリリア体験：パリからローザンヌへのリラックスした旅',
        'ko': 'TGV 리리아 경험: 파리에서 로잔까지의 여유로운 여행',
        'pt': 'Experiência TGV Lyria: Uma Viagem Relaxante de Paris a Lausanne',
        'it': 'Esperienza TGV Lyria: Un Viaggio Rilassante da Parigi a Losanna',
        'zh': 'TGV Lyria体验：从巴黎到洛桑的轻松之旅',
    },
    'train-apps-comparison.html': {
        'de': 'Vergleich europäischer Zug-Apps',
        'fr': 'Comparaison des Applications de Train Européennes',
        'es': 'Comparación de Aplicaciones de Tren Europeas',
        'ja': '欧州鉄道アプリ比較',
        'ko': '유럽 기차 앱 비교',
        'pt': 'Comparação de Aplicativos de Trem Europeus',
        'it': 'Confronto delle App per Treni Europee',
        'zh': '欧洲火车APP比较',
    },
    'train-station-guide.html': {
        'de': 'Vollständiger Leitfaden zu europäischen Bahnhöfen',
        'fr': 'Guide Complet des Gares Européennes',
        'es': 'Guía Completa de las Estaciones de Tren Europeas',
        'ja': '欧州鉄道駅完全ガイド',
        'ko': '유럽 기차역 완벽 가이드',
        'pt': 'Guia Completo das Estações de Trem Europeias',
        'it': 'Guida Completa alle Stazioni Ferroviarie Europee',
        'zh': '欧洲火车站完整指南',
    },
}

def fix_article_titles():
    """修复所有文章标题"""
    print("🚀 开始修复文章标题翻译...")
    
    fixed_count = 0
    
    for filename, translations in ARTICLE_TITLES.items():
        for lang, title in translations.items():
            filepath = BASE_DIR / lang / 'articles' / filename
            if not filepath.exists():
                continue
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找并替换 h1 标题
            h1_pattern = r'<h1>(.*?)</h1>'
            match = re.search(h1_pattern, content)
            if match:
                old_title = match.group(1)
                if old_title != title:
                    content = content.replace(f'<h1>{old_title}</h1>', f'<h1>{title}</h1>', 1)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    fixed_count += 1
                    print(f"  ✓ {lang}/articles/{filename}: '{old_title}' → '{title}'")
    
    print(f"\n✅ 修复完成: {fixed_count} 个标题")

if __name__ == '__main__':
    fix_article_titles()
