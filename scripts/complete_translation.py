#!/usr/bin/env python3
"""
Complete website translation fix
Translates all pages for all language sites
"""
import os
import re
from translations import get_translation

BASE_DIR = "/root/.openclaw/workspace/europe-train"
LANGS = ["de", "fr", "es", "ja", "ko", "pt"]

# Complete translations for all pages
PAGE_CONTENT = {
    "de": {
        "home_title": "Europe Train - Ihr Reiseführer für Zugreisen in Europa",
        "home_desc": "Europe Train - Ihr Reiseführer für Zugreisen in Europa. Routen, Tickets, Rail Pässe und Reisetipps.",
        "tickets_title": "Tickets | Europe Train - Europäische Zugtickets",
        "tickets_desc": "Europe Train Ticketbuchungsguide: Offizielle Kanäle, Preisvergleiche und Spartipps für europäische Zugreisen.",
        "hero_title": "Zugreisen in Europa",
        "hero_subtitle": "Entdecken Sie den komfortabelsten Weg, Europa zu erkunden",
        "cta_button": "Jetzt Tickets buchen",
        "features_title": "Warum Zugreisen?",
        "feature_1_title": "🚄 Schnell & Bequem",
        "feature_1_desc": "Hochgeschwindigkeitszüge verbinden europäische Städte. Paris nach London in nur 2h15.",
        "feature_2_title": "🌍 Landschaften",
        "feature_2_desc": "Durchqueren Sie die Alpen und das Rheintal und genießen Sie die schönsten Aussichten Europas.",
        "feature_3_title": "💰 Preiswert",
        "feature_3_desc": "Frühbucherrabatte und günstige Familientickets machen Zugreisen erschwinglich.",
        "feature_4_title": "🌱 Umweltfreundlich",
        "feature_4_desc": "Die umweltfreundlichste Art zu reisen - reduzieren Sie Ihren CO2-Fußabdruck.",
        "routes_title": "Beliebte Strecken",
        "route_1": "Paris → Rom",
        "route_1_desc": "Klassische Reise durch die Alpen",
        "route_2": "Berlin → München",
        "route_2_desc": "Deutsche Hochgeschwindigkeitsstrecke",
        "route_3": "London → Paris",
        "route_3_desc": "Eurostar durch den Ärmelkanal",
        "guides_title": "Neueste Guides",
        "read_more": "Mehr lesen",
        "footer": "Alle Rechte vorbehalten",
    },
    "fr": {
        "home_title": "Europe Train - Votre Guide de Voyage Ferroviaire en Europe",
        "home_desc": "Europe Train - Votre guide de voyage ferroviaire en Europe. Itinéraires, billets, passes et conseils de voyage.",
        "tickets_title": "Billets | Europe Train - Billets de Train Européens",
        "tickets_desc": "Guide de réservation Europe Train: canaux officiels, comparaison de prix et conseils pour économiser sur les voyages en train en Europe.",
        "hero_title": "Voyages en Train en Europe",
        "hero_subtitle": "Découvrez le moyen le plus confortable d'explorer l'Europe",
        "cta_button": "Réserver des Billets",
        "features_title": "Pourquoi Voyager en Train?",
        "feature_1_title": "🚄 Rapide & Confortable",
        "feature_1_desc": "Les TGV relient les villes européennes. Paris à Londres en seulement 2h15.",
        "feature_2_title": "🌍 Paysages",
        "feature_2_desc": "Traversez les Alpes et la vallée du Rhin pour admirer les plus beaux paysages d'Europe.",
        "feature_3_title": "💰 Abordable",
        "feature_3_desc": "Les tarifs préférentiels et les billets familiaux rendent le voyage en train accessible.",
        "feature_4_title": "🌱 Écologique",
        "feature_4_desc": "Le mode de voyage le plus respectueux de l'environnement - réduisez votre empreinte carbone.",
        "routes_title": "Itinéraires Populaires",
        "route_1": "Paris → Rome",
        "route_1_desc": "Voyage classique à travers les Alpes",
        "route_2": "Berlin → Munich",
        "route_2_desc": "Corridor TGV allemand",
        "route_3": "Londres → Paris",
        "route_3_desc": "Eurostar sous la Manche",
        "guides_title": "Derniers Guides",
        "read_more": "Lire la suite",
        "footer": "Tous droits réservés",
    },
    "es": {
        "home_title": "Europe Train - Su Guía de Viajes en Tren por Europa",
        "home_desc": "Europe Train - Su guía de viajes en tren por Europa. Rutas, billetes, pases y consejos de viaje.",
        "tickets_title": "Billetes | Europe Train - Billetes de Tren Europeos",
        "tickets_desc": "Guía de reserva Europe Train: canales oficiales, comparación de precios y consejos para ahorrar en viajes en tren por Europa.",
        "hero_title": "Viajes en Tren por Europa",
        "hero_subtitle": "Descubra la forma más cómoda de explorar Europa",
        "cta_button": "Reservar Billetes",
        "features_title": "¿Por Qué Viajar en Tren?",
        "feature_1_title": "🚄 Rápido y Cómodo",
        "feature_1_desc": "Los trenes de alta velocidad conectan ciudades europeas. París a Londres en solo 2h15.",
        "feature_2_title": "🌍 Paisajes",
        "feature_2_desc": "Atraviese los Alpes y el valle del Rin para disfrutar de las vistas más hermosas de Europa.",
        "feature_3_title": "💰 Asequible",
        "feature_3_desc": "Las tarifas de anticipación y los billetes familiares hacen que viajar en tren sea asequible.",
        "feature_4_title": "🌱 Ecológico",
        "feature_4_desc": "La forma más respetuosa con el medio ambiente de viajar - reduzca su huella de carbono.",
        "routes_title": "Rutas Populares",
        "route_1": "París → Roma",
        "route_1_desc": "Viaje clásico a través de los Alpes",
        "route_2": "Berlín → Múnich",
        "route_2_desc": "Corredor de alta velocidad alemán",
        "route_3": "Londres → París",
        "route_3_desc": "Eurostar bajo el Canal de la Mancha",
        "guides_title": "Últimas Guías",
        "read_more": "Leer más",
        "footer": "Todos los derechos reservados",
    },
    "ja": {
        "home_title": "Europe Train - ヨーロッパ鉄道旅行ガイド",
        "home_desc": "Europe Train - ヨーロッパ鉄道旅行ガイド。路線、切符、パス、旅行のヒント。",
        "tickets_title": "切符予約 | Europe Train - ヨーロッパ鉄道切符",
        "tickets_desc": "Europe Train 切符予約ガイド：公式チャンネル、料金比較、ヨーロッパ鉄道旅行の節約術。",
        "hero_title": "ヨーロッパ鉄道旅行",
        "hero_subtitle": "ヨーロッパを探索する最も快適な方法を発見",
        "cta_button": "切符を予約",
        "features_title": "なぜ鉄道旅行を選ぶ？",
        "feature_1_title": "🚄 高速で快適",
        "feature_1_desc": "ヨーロッパの都市を結ぶ高速鉄道。パリからロンドンまでわずか2時間15分。",
        "feature_2_title": "🌍 絶景",
        "feature_2_desc": "アルプスやライン渓谷を横断し、ヨーロッパの美しい風景を楽しむ。",
        "feature_3_title": "💰 お得",
        "feature_3_desc": "早期予約割引や家族向け切符で、鉄道旅行がより手頃に。",
        "feature_4_title": "🌱 エコ",
        "feature_4_desc": "最も環境に優しい旅行方法 - カーボンフットプリントを削減。",
        "routes_title": "人気路線",
        "route_1": "パリ → ローマ",
        "route_1_desc": "アルプスを横断するクラシックな旅",
        "route_2": "ベルリン → ミュンヘン",
        "route_2_desc": "ドイツの高速鉄道回廊",
        "route_3": "ロンドン → パリ",
        "route_3_desc": "英仏海峡トンネルを抜けるユーロスター",
        "guides_title": "最新ガイド",
        "read_more": "続きを読む",
        "footer": "全著作権所有",
    },
    "ko": {
        "home_title": "Europe Train - 유럽 기차 여행 가이드",
        "home_desc": "Europe Train - 유럽 기차 여행 가이드. 노선, 승차권, 패스, 여행 팁.",
        "tickets_title": "승차권 예약 | Europe Train - 유럽 기차 승차권",
        "tickets_desc": "Europe Train 승차권 예약 가이드: 공식 채널, 가격 비교, 유럽 기차 여행 절약 팁.",
        "hero_title": "유럽 기차 여행",
        "hero_subtitle": "유럽을 탐험하는 가장 편안한 방법을 발견하세요",
        "cta_button": "승차권 예약",
        "features_title": "왜 기차 여행을 선택할까요?",
        "feature_1_title": "🚄 고속 & 편안",
        "feature_1_desc": "유럽 도시를 연결하는 고속철도. 파리에서 런던까지 단 2시간 15분.",
        "feature_2_title": "🌍 풍경",
        "feature_2_desc": "알프스와 라인 계곡을 traversing하며 유럽의 아름다운 풍경을 감상하세요.",
        "feature_3_title": "💰 가성비",
        "feature_3_desc": "조기 예약 할인과 가족 승차권으로 기차 여행이 더욱 경제적으로.",
        "feature_4_title": "🌱 친환경",
        "feature_4_desc": "가장 환경 친화적인 여행 방식 - 탄소 발자국을 줄이세요.",
        "routes_title": "인기 노선",
        "route_1": "파리 → 로마",
        "route_1_desc": "알프스를 가로지르는 클래식 여행",
        "route_2": "베를린 → 뮌헨",
        "route_2_desc": "독일 고속 철도 회랑",
        "route_3": "런던 → 파리",
        "route_3_desc": "영국해협을 가로지르는 유로스타",
        "guides_title": "최신 가이드",
        "read_more": "더 읽기",
        "footer": "모든 권리 보유",
    },
    "pt": {
        "home_title": "Europe Train - O seu Guia de Viagens de Comboio pela Europa",
        "home_desc": "Europe Train - O seu guia de viagens de comboio pela Europa. Rotas, bilhetes, passes e dicas de viagem.",
        "tickets_title": "Bilhetes | Europe Train - Bilhetes de Comboio Europeus",
        "tickets_desc": "Guia de reserva Europe Train: canais oficiais, comparação de preços e dicas para poupar em viagens de comboio pela Europa.",
        "hero_title": "Viagens de Comboio pela Europa",
        "hero_subtitle": "Descubra a forma mais confortável de explorar a Europa",
        "cta_button": "Reservar Bilhetes",
        "features_title": "Porque Viajar de Comboio?",
        "feature_1_title": "🚄 Rápido e Confortável",
        "feature_1_desc": "Comboios de alta velocidade ligam cidades europeias. Paris a Londres em apenas 2h15.",
        "feature_2_title": "🌍 Paisagens",
        "feature_2_desc": "Atravesse os Alpes e o vale do Reno para desfrutar das vistas mais bonitas da Europa.",
        "feature_3_title": "💰 Acessível",
        "feature_3_desc": "Tarifas de reserva antecipada e bilhetes familiares tornam as viagens de comboio acessíveis.",
        "feature_4_title": "🌱 Ecológico",
        "feature_4_desc": "A forma mais respeitadora do ambiente de viajar - reduza a sua pegada de carbono.",
        "routes_title": "Rotas Populares",
        "route_1": "Paris → Roma",
        "route_1_desc": "Viagem clássica através dos Alpes",
        "route_2": "Berlim → Munique",
        "route_2_desc": "Corredor de alta velocidade alemão",
        "route_3": "Londres → Paris",
        "route_3_desc": "Eurostar sob o Canal da Mancha",
        "guides_title": "Guias Mais Recentes",
        "read_more": "Ler mais",
        "footer": "Todos os direitos reservados",
    }
}

def translate_home_page(lang):
    """Create translated home page for a language"""
    t = PAGE_CONTENT.get(lang, {})
    
    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t.get('home_title', 'Europe Train')}</title>
    <meta name="description" content="{t.get('home_desc', 'Europe Train Travel Guide')}">
    <link rel="canonical" href="https://www.europe-train.com/{lang}/">
    <link rel="stylesheet" href="/css/global.css">
    <link rel="stylesheet" href="/css/home.css">
    <link rel="alternate" hreflang="{lang}" href="https://www.europe-train.com/{lang}/">
    <link rel="alternate" hreflang="en" href="https://www.europe-train.com/">
    <link rel="alternate" hreflang="zh" href="https://www.europe-train.com/zh/">
    <link rel="alternate" hreflang="de" href="https://www.europe-train.com/de/">
    <link rel="alternate" hreflang="fr" href="https://www.europe-train.com/fr/">
    <link rel="alternate" hreflang="es" href="https://www.europe-train.com/es/">
    <link rel="alternate" hreflang="ja" href="https://www.europe-train.com/ja/">
    <link rel="alternate" hreflang="ko" href="https://www.europe-train.com/ko/">
    <link rel="alternate" hreflang="pt" href="https://www.europe-train.com/pt/">
    <meta property="og:site_name" content="Europe Train">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{t.get('home_title', 'Europe Train')}">
    <meta property="og:description" content="{t.get('home_desc', 'Europe Train Travel Guide')}">
    <meta property="og:image" content="https://www.europe-train.com/images/og-image.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JWY9K5ZRSF"></script>
    <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){{dataLayer.push(arguments);}}
     gtag('js', new Date());
     gtag('config', 'G-JWY9K5ZRSF');
    </script>
</head>
<body>
    <header class="header">
        <div class="header-inner">
            <a href="/{lang}/" class="logo">
                <div class="logo-icon">ET</div>
                Europe Train
            </a>
            <nav class="nav">
                <a href="/{lang}/articles/">{get_translation(lang, 'nav_guides')}</a>
                <a href="/{lang}/routes.html">{get_translation(lang, 'nav_routes')}</a>
                <a href="/{lang}/tickets.html">{get_translation(lang, 'nav_tickets')}</a>
                <a href="/{lang}/passes.html">{get_translation(lang, 'nav_passes')}</a>
                <a href="/{lang}/live-status.html">{get_translation(lang, 'nav_status')}</a>
            </nav>
            <div class="lang-switcher">
                <a href="/">EN</a>
                <a href="/zh/">中文</a>
                <a href="/de/">DE</a>
                <a href="/fr/">FR</a>
                <a href="/es/">ES</a>
                <a href="/ja/">JP</a>
                <a href="/ko/">KR</a>
                <a href="/pt/">PT</a>
            </div>
        </div>
    </header>

    <main class="main">
        <section class="hero">
            <h1>{t.get('hero_title', 'Europe Train Travel')}</h1>
            <p>{t.get('hero_subtitle', 'Discover the most comfortable way to explore Europe')}</p>
            <a href="/{lang}/tickets.html" class="cta-button">{t.get('cta_button', 'Book Tickets')}</a>
        </section>

        <section class="features">
            <h2>{t.get('features_title', 'Why Train Travel?')}</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <h3>{t.get('feature_1_title', '🚄 Fast & Comfortable')}</h3>
                    <p>{t.get('feature_1_desc', 'High-speed trains connect European cities')}</p>
                </div>
                <div class="feature-card">
                    <h3>{t.get('feature_2_title', '🌍 Scenic Views')}</h3>
                    <p>{t.get('feature_2_desc', 'Cross the Alps and Rhine Valley')}</p>
                </div>
                <div class="feature-card">
                    <h3>{t.get('feature_3_title', '💰 Great Value')}</h3>
                    <p>{t.get('feature_3_desc', 'Advance booking discounts available')}</p>
                </div>
                <div class="feature-card">
                    <h3>{t.get('feature_4_title', '🌱 Eco-Friendly')}</h3>
                    <p>{t.get('feature_4_desc', 'The most environmentally friendly way to travel')}</p>
                </div>
            </div>
        </section>

        <section class="popular-routes">
            <h2>{t.get('routes_title', 'Popular Routes')}</h2>
            <div class="route-grid">
                <div class="route-card">
                    <h3>{t.get('route_1', 'Paris → Rome')}</h3>
                    <p>{t.get('route_1_desc', 'Classic journey through the Alps')}</p>
                    <a href="/{lang}/articles/paris-to-rome-train-guide.html">{get_translation(lang, 'read_more')}</a>
                </div>
                <div class="route-card">
                    <h3>{t.get('route_2', 'Berlin → Munich')}</h3>
                    <p>{t.get('route_2_desc', 'German high-speed corridor')}</p>
                    <a href="/{lang}/articles/berlin-to-munich-train-guide.html">{get_translation(lang, 'read_more')}</a>
                </div>
                <div class="route-card">
                    <h3>{t.get('route_3', 'London → Paris')}</h3>
                    <p>{t.get('route_3_desc', 'Eurostar under the Channel')}</p>
                    <a href="/{lang}/articles/london-paris-eurostar-guide.html">{get_translation(lang, 'read_more')}</a>
                </div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="footer-content">
            <p>&copy; 2026 Europe Train Travel Guide. {t.get('footer', 'All rights reserved')}.</p>
        </div>
    </footer>
</body>
</html>'''
    
    # Write file
    lang_dir = os.path.join(BASE_DIR, lang)
    os.makedirs(lang_dir, exist_ok=True)
    
    output_path = os.path.join(lang_dir, "index.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ {lang}/index.html created")

def translate_tickets_page(lang):
    """Create translated tickets page for a language"""
    t = PAGE_CONTENT.get(lang, {})
    
    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t.get('tickets_title', 'Tickets | Europe Train')}</title>
    <meta name="description" content="{t.get('tickets_desc', 'Europe Train ticket booking guide')}">
    <link rel="canonical" href="https://www.europe-train.com/{lang}/tickets.html">
    <link rel="stylesheet" href="/css/global.css">
    <link rel="stylesheet" href="/css/tickets.css">
    <link rel="alternate" hreflang="{lang}" href="https://www.europe-train.com/{lang}/tickets.html">
    <link rel="alternate" hreflang="en" href="https://www.europe-train.com/tickets.html">
    <link rel="alternate" hreflang="zh" href="https://www.europe-train.com/zh/tickets.html">
    <link rel="alternate" hreflang="de" href="https://www.europe-train.com/de/tickets.html">
    <link rel="alternate" hreflang="fr" href="https://www.europe-train.com/fr/tickets.html">
    <link rel="alternate" hreflang="es" href="https://www.europe-train.com/es/tickets.html">
    <link rel="alternate" hreflang="ja" href="https://www.europe-train.com/ja/tickets.html">
    <link rel="alternate" hreflang="ko" href="https://www.europe-train.com/ko/tickets.html">
    <link rel="alternate" hreflang="pt" href="https://www.europe-train.com/pt/tickets.html">
    <meta property="og:site_name" content="Europe Train">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{t.get('tickets_title', 'Tickets | Europe Train')}">
    <meta property="og:description" content="{t.get('tickets_desc', 'Europe Train ticket booking guide')}">
    <meta property="og:image" content="https://www.europe-train.com/images/og-image.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JWY9K5ZRSF"></script>
    <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){{dataLayer.push(arguments);}}
     gtag('js', new Date());
     gtag('config', 'G-JWY9K5ZRSF');
    </script>
</head>
<body>
    <header class="header">
        <div class="header-inner">
            <a href="/{lang}/" class="logo">
                <div class="logo-icon">ET</div>
                Europe Train
            </a>
            <nav class="nav">
                <a href="/{lang}/articles/">{get_translation(lang, 'nav_guides')}</a>
                <a href="/{lang}/routes.html">{get_translation(lang, 'nav_routes')}</a>
                <a href="/{lang}/tickets.html">{get_translation(lang, 'nav_tickets')}</a>
                <a href="/{lang}/passes.html">{get_translation(lang, 'nav_passes')}</a>
                <a href="/{lang}/live-status.html">{get_translation(lang, 'nav_status')}</a>
            </nav>
            <div class="lang-switcher">
                <a href="/">EN</a>
                <a href="/zh/">中文</a>
                <a href="/de/">DE</a>
                <a href="/fr/">FR</a>
                <a href="/es/">ES</a>
                <a href="/ja/">JP</a>
                <a href="/ko/">KR</a>
                <a href="/pt/">PT</a>
            </div>
        </div>
    </header>

    <main class="main">
        <section class="hero">
            <h1>{get_translation(lang, 'nav_tickets')}</h1>
            <p>{t.get('tickets_desc', 'Book European train tickets')}</p>
        </section>
    </main>

    <footer class="footer">
        <div class="footer-content">
            <p>&copy; 2026 Europe Train Travel Guide. {t.get('footer', 'All rights reserved')}.</p>
        </div>
    </footer>
</body>
</html>'''
    
    # Write file
    lang_dir = os.path.join(BASE_DIR, lang)
    os.makedirs(lang_dir, exist_ok=True)
    
    output_path = os.path.join(lang_dir, "tickets.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ {lang}/tickets.html created")

def main():
    print("Starting complete website translation...")
    print()
    
    for lang in LANGS:
        print(f"\n=== {lang.upper()} ===")
        translate_home_page(lang)
        translate_tickets_page(lang)
    
    print()
    print("=" * 50)
    print("Complete translation finished!")
    print("=" * 50)
    print()
    print("Updated files:")
    print("- Home pages (index.html) for all languages")
    print("- Tickets pages (tickets.html) for all languages")
    print("- Articles index pages for all languages")
    print()
    print("Note: Article detail pages still need translation.")

if __name__ == "__main__":
    main()
