#!/usr/bin/env python3
"""
Batch translate article detail pages
Translates navigation and common elements for all articles in all languages
"""
import os
import re
from translations import get_translation

BASE_DIR = "/root/.openclaw/workspace/europe-train"
LANGS = ["de", "fr", "es", "ja", "ko", "pt"]

# Article translations for titles
ARTICLE_TITLES = {
    "paris-to-rome-train-guide.html": {
        "de": "Paris nach Rom mit dem Zug: Kompletter Guide",
        "fr": "Paris à Rome en Train: Guide Complet",
        "es": "París a Roma en Tren: Guía Completa",
        "ja": "パリからローマへの鉄道旅行：完全ガイド",
        "ko": "파리에서 로마 기차 여행: 완벽 가이드",
        "pt": "Paris a Roma de Comboio: Guia Completo",
    },
    "berlin-to-munich-train-guide.html": {
        "de": "Berlin nach München mit dem Zug: Kompletter Guide",
        "fr": "Berlin à Munich en Train: Guide Complet",
        "es": "Berlín a Múnich en Tren: Guía Completa",
        "ja": "ベルリンからミュンヘンへの鉄道旅行：完全ガイド",
        "ko": "베를린에서 뮌헨 기차 여행: 완벽 가이드",
        "pt": "Berlim a Munique de Comboio: Guia Completo",
    },
    "paris-zurich-train-vs-flight.html": {
        "de": "Paris nach Zürich: Zug vs Flug vs Auto",
        "fr": "Paris à Zurich: Train vs Avion vs Voiture",
        "es": "París a Zúrich: Tren vs Vuelo vs Coche",
        "ja": "パリからチューリッヒ：鉄道 vs 飛行機 vs 車",
        "ko": "파리에서 취리히: 기차 vs 비행기 vs 자동차",
        "pt": "Paris a Zurique: Comboio vs Voo vs Carro",
    },
    "london-paris-eurostar-guide.html": {
        "de": "London-Paris Eurostar: Kompletter Guide",
        "fr": "Londres-Paris Eurostar: Guide Complet",
        "es": "Londres-París Eurostar: Guía Completa",
        "ja": "ロンドン-パリ ユーロスター：完全ガイド",
        "ko": "런던-파리 유로스타: 완벽 가이드",
        "pt": "Londres-Paris Eurostar: Guia Completo",
    },
    "tgv-lyria-experience.html": {
        "de": "TGV Lyria Erlebnis: Paris nach Lausanne",
        "fr": "Expérience TGV Lyria: Paris à Lausanne",
        "es": "Experiencia TGV Lyria: París a Lausana",
        "ja": "TGVリリア体験：パリからローザンヌ",
        "ko": "TGV 리리아 체험: 파리에서 로잔",
        "pt": "Experiência TGV Lyria: Paris a Lausanne",
    },
    "swiss-scenic-trains.html": {
        "de": "Schweizer Panoramazüge: Ultimativer Guide",
        "fr": "Trains Panoramiques Suisses: Guide Ultime",
        "es": "Trenes Panorámicos Suizos: Guía Definitiva",
        "ja": "スイス観光列車：究極ガイド",
        "ko": "스위스 관광 열차: 궁극 가이드",
        "pt": "Comboios Panorâmicos Suíços: Guia Definitivo",
    },
    "france-tgv-guide.html": {
        "de": "Frankreich TGV Hochgeschwindigkeitszug: Kompletter Guide",
        "fr": "France TGV Grande Vitesse: Guide Complet",
        "es": "Francia TGV Alta Velocidad: Guía Completa",
        "ja": "フランスTGV高速鉄道：完全ガイド",
        "ko": "프랑스 TGV 고속철도: 완벽 가이드",
        "pt": "França TGV Alta Velocidade: Guia Completo",
    },
    "germany-ice-guide.html": {
        "de": "Deutschland ICE Hochgeschwindigkeitszug: Kompletter Guide",
        "fr": "Allemagne ICE Grande Vitesse: Guide Complet",
        "es": "Alemania ICE Alta Velocidad: Guía Completa",
        "ja": "ドイツICE高速鉄道：完全ガイド",
        "ko": "독일 ICE 고속철도: 완벽 가이드",
        "pt": "Alemanha ICE Alta Velocidade: Guia Completo",
    },
    "italy-frecciarossa-guide.html": {
        "de": "Italien Frecciarossa: Kompletter Guide",
        "fr": "Italie Frecciarossa: Guide Complet",
        "es": "Italia Frecciarossa: Guía Completa",
        "ja": "イタリアフレッチャロッサ：完全ガイド",
        "ko": "이탈리아 프레차로사: 완벽 가이드",
        "pt": "Itália Frecciarossa: Guia Completo",
    },
    "spain-ave-guide.html": {
        "de": "Spanien AVE Hochgeschwindigkeitszug: Kompletter Guide",
        "fr": "Espagne AVE Grande Vitesse: Guide Complet",
        "es": "España AVE Alta Velocidad: Guía Completa",
        "ja": "スペインAVE高速鉄道：完全ガイド",
        "ko": "스페인 AVE 고속철도: 완벽 가이드",
        "pt": "Espanha AVE Alta Velocidade: Guia Completo",
    },
    "seat-reservation-guide.html": {
        "de": "Sitzplatzreservierung in Europa: Kompletter Guide",
        "fr": "Réservation de Sièges en Europe: Guide Complet",
        "es": "Reserva de Asientos en Europa: Guía Completa",
        "ja": "ヨーロッパ座席予約：完全ガイド",
        "ko": "유럽 좌석 예약: 완벽 가이드",
        "pt": "Reserva de Lugares na Europa: Guia Completo",
    },
    "train-station-guide.html": {
        "de": "Europäische Hauptbahnhöfe: Kompletter Guide",
        "fr": "Gares Européennes Principales: Guide Complet",
        "es": "Estaciones de Tren Europeas: Guía Completa",
        "ja": "ヨーロッパ主要駅：完全ガイド",
        "ko": "유럽 주요 역: 완벽 가이드",
        "pt": "Estações Ferroviárias Europeias: Guia Completo",
    },
    "europe-train-ticket-rules.html": {
        "de": "Europäische Zugticketregeln: Rückgabe & Änderung",
        "fr": "Règles des Billets de Train Européens: Remboursement & Modification",
        "es": "Reglas de Billetes de Tren Europeos: Reembolso y Cambio",
        "ja": "ヨーロッパ鉄道切符規則：払い戻しと変更",
        "ko": "유럽 기차 승차권 규정: 환불 및 변경",
        "pt": "Regras de Bilhetes de Comboio Europeus: Reembolso e Alteração",
    },
    "delay-compensation-guide.html": {
        "de": "Verspätungsentschädigung: Ihre Rechte in Europa",
        "fr": "Indemnisation pour Retard: Vos Droits en Europe",
        "es": "Compensación por Retraso: Sus Derechos en Europa",
        "ja": "遅延賠償：ヨーロッパでの権利",
        "ko": "지연 배상: 유럽에서의 권리",
        "pt": "Compensação por Atraso: Os Seus Direitos na Europa",
    },
    "train-apps-comparison.html": {
        "de": "Europäische Zug-Apps: Vergleichstest",
        "fr": "Applications de Train Européennes: Comparaison",
        "es": "Apps de Tren Europeas: Comparativa",
        "ja": "ヨーロッパ鉄道アプリ：比較レビュー",
        "ko": "유럽 기차 앱: 비교 평가",
        "pt": "Apps de Comboio Europeus: Comparação",
    },
}

def translate_article_file(lang, article_file):
    """Translate a single article file for a language"""
    
    # Read English version
    en_path = os.path.join(BASE_DIR, "articles", article_file)
    if not os.path.exists(en_path):
        print(f"⚠️  EN version not found: {article_file}")
        return False
    
    with open(en_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get translated title
    titles = ARTICLE_TITLES.get(article_file, {})
    translated_title = titles.get(lang, "")
    
    if not translated_title:
        print(f"⚠️  No translation for {article_file} in {lang}")
        return False
    
    # Replace language attribute
    content = content.replace('lang="en"', f'lang="{lang}"')
    
    # Replace title
    # Extract current title
    title_match = re.search(r'<title>([^<]*)</title>', content)
    if title_match:
        current_title = title_match.group(1)
        # Create new title with translated main title but keep site name
        new_title = f"{translated_title} | Europe Train"
        content = content.replace(f'<title>{current_title}</title>', f'<title>{new_title}</title>')
    
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
    
    # Translate footer
    content = content.replace('All rights reserved', get_translation(lang, 'footer'))
    
    # Write translated file
    lang_dir = os.path.join(BASE_DIR, lang, "articles")
    os.makedirs(lang_dir, exist_ok=True)
    
    output_path = os.path.join(lang_dir, article_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("Starting article translation...")
    print()
    
    # Get list of all article files
    articles_dir = os.path.join(BASE_DIR, "articles")
    article_files = [f for f in os.listdir(articles_dir) if f.endswith('.html') and f != 'index.html']
    
    total_files = 0
    success_count = 0
    
    for lang in LANGS:
        print(f"\n=== {lang.upper()} ===")
        lang_success = 0
        
        for article_file in article_files:
            total_files += 1
            if translate_article_file(lang, article_file):
                success_count += 1
                lang_success += 1
                print(f"  ✅ {article_file}")
            else:
                print(f"  ❌ {article_file}")
        
        print(f"  {lang_success}/{len(article_files)} articles translated")
    
    print()
    print("=" * 50)
    print(f"Translation complete: {success_count}/{total_files} files")
    print("=" * 50)

if __name__ == "__main__":
    main()
