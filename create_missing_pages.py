#!/usr/bin/env python3
"""
批量创建 europe-train.com 各语言站缺失的子页面
P0 - 子页面404修复：为每个语言站创建 routes.html, tickets.html, passes.html, live-status.html
"""

import os
import re

BASE_DIR = "/root/.openclaw/workspace/europe-train"

# 语言配置（简化版，只包含关键翻译）
LANG_CONFIG = {
    "de": {
        "lang": "de",
        "title_suffix": "Europe Train - Europäische Bahn-Reise",
        "nav": {"articles": "Reiseguides", "routes": "Beliebte Strecken", "tickets": "Tickets buchen", "passes": "Pässe", "live_status": "Live Status"},
        "routes": {"title": "Beliebte Strecken", "subtitle": "Kuratierte europäische Bahnstrecken, von Hochgeschwindigkeitszügen bis Panoramafahrten"},
        "tickets": {"title": "Tickets", "subtitle": "Europäischer Bahn-Ticket-Buchungsleitfaden und Spartipps"},
        "passes": {"title": "Pässe", "subtitle": "Vollständiger europäischer Bahnpass-Leitfaden"},
        "live_status": {"title": "Europäischer Bahn Live-Status", "subtitle": "Echtzeit-Verspätungen und Ausfälle für DB, SNCF, Trenitalia, SBB, ÖBB und Renfe"},
    },
    "fr": {
        "lang": "fr",
        "title_suffix": "Europe Train - Voyage en train en Europe",
        "nav": {"articles": "Guides", "routes": "Routes", "tickets": "Billets", "passes": "Pass", "live_status": "Live Status"},
        "routes": {"title": "Routes Populaires", "subtitle": "Itinéraires ferroviaires européens sélectionnés, des trains à grande vitesse aux voyages panoramiques"},
        "tickets": {"title": "Billets", "subtitle": "Guide de réservation de billets de train européens et astuces pour économiser"},
        "passes": {"title": "Pass", "subtitle": "Guide complet des passes ferroviaires européens"},
        "live_status": {"title": "Statut en Direct des Trains Européens", "subtitle": "Retards et annulations en temps réel pour DB, SNCF, Trenitalia, SBB, ÖBB et Renfe"},
    },
    "es": {
        "lang": "es",
        "title_suffix": "Europe Train - Viaje en tren por Europa",
        "nav": {"articles": "Guías", "routes": "Rutas", "tickets": "Billetes", "passes": "Pases", "live_status": "Estado en Vivo"},
        "routes": {"title": "Rutas Populares", "subtitle": "Rutas ferroviarias europeas seleccionadas, desde trenes de alta velocidad hasta viajes panorámicos"},
        "tickets": {"title": "Billetes", "subtitle": "Guía de reserva de billetes de tren europeos y consejos para ahorrar"},
        "passes": {"title": "Pases", "subtitle": "Guía completa de pases ferroviarios europeos"},
        "live_status": {"title": "Estado en Vivo de Trenes Europeos", "subtitle": "Retrasos y cancelaciones en tiempo real para DB, SNCF, Trenitalia, SBB, ÖBB y Renfe"},
    },
    "ja": {
        "lang": "ja",
        "title_suffix": "Europe Train - ヨーロッパ鉄道旅行",
        "nav": {"articles": "ガイド", "routes": "人気ルート", "tickets": "切符予約", "passes": "パス", "live_status": "運行状況"},
        "routes": {"title": "人気ルート", "subtitle": "高速鉄道から景観路線まで、厳選されたヨーロッパ鉄道路線"},
        "tickets": {"title": "切符", "subtitle": "ヨーロッパ鉄道切符予約ガイドと節約のコツ"},
        "passes": {"title": "パス", "subtitle": "ヨーロッパ鉄道パス完全ガイド"},
        "live_status": {"title": "ヨーロッパ鉄道リアルタイム運行状況", "subtitle": "DB、SNCF、Trenitalia、SBB、ÖBB、Renfeの遅延と運休情報"},
    },
    "ko": {
        "lang": "ko",
        "title_suffix": "Europe Train - 유럽 기차 여행",
        "nav": {"articles": "가이드", "routes": "인기 노선", "tickets": "티켓 예약", "passes": "패스", "live_status": "실시간 상태"},
        "routes": {"title": "인기 노선", "subtitle": "고속열차부터 경관열차까지, 엄선된 유럽 기차 노선"},
        "tickets": {"title": "티켓", "subtitle": "유럽 기차 티켓 예약 가이드와 절약 팁"},
        "passes": {"title": "패스", "subtitle": "유럽 기차 패스 완벽 가이드"},
        "live_status": {"title": "유럽 기차 실시간 운행 상태", "subtitle": "DB, SNCF, Trenitalia, SBB, ÖBB, Renfe 지연 및 운행 중단 정보"},
    },
    "pt": {
        "lang": "pt",
        "title_suffix": "Europe Train - Viagem de Trem na Europa",
        "nav": {"articles": "Guias", "routes": "Rotas", "tickets": "Bilhetes", "passes": "Passes", "live_status": "Status ao Vivo"},
        "routes": {"title": "Rotas Populares", "subtitle": "Rotas ferroviárias europeas selecionadas, de trens de alta velocidade a viagens panorâmicas"},
        "tickets": {"title": "Bilhetes", "subtitle": "Guia de reserva de bilhetes de trem europeus e dicas para economizar"},
        "passes": {"title": "Passes", "subtitle": "Guia completo de passes ferroviários europeus"},
        "live_status": {"title": "Status ao Vivo dos Trens Europeus", "subtitle": "Atrasos e cancelamentos em tempo real para DB, SNCF, Trenitalia, SBB, ÖBB e Renfe"},
    },
    "zh": {
        "lang": "zh-CN",
        "title_suffix": "Europe Train - 欧洲火车旅行",
        "nav": {"articles": "旅行指南", "routes": "热门路线", "tickets": "车票预订", "passes": "通票", "live_status": "实时状态"},
        "routes": {"title": "热门路线", "subtitle": "精选欧洲火车路线，从高速列车到风景之旅"},
        "tickets": {"title": "车票", "subtitle": "欧洲火车票预订指南与省钱技巧"},
        "passes": {"title": "通票", "subtitle": "欧洲铁路通票完整指南"},
        "live_status": {"title": "欧洲火车实时状态", "subtitle": "DB、SNCF、Trenitalia、SBB、ÖBB、Renfe 延误与取消信息"},
    },
}


def build_header(lang, active_nav):
    """构建通用header"""
    cfg = LANG_CONFIG[lang]
    nav = cfg["nav"]
    
    # 语言切换器
    lang_links = []
    for l in ["en", "zh", "de", "fr", "es", "ja", "ko", "pt"]:
        if l == lang:
            lang_links.append(f'<a href="/{l}/" class="active">{l.upper() if l != "zh" else "中文"}</a>')
        else:
            label = {"en": "EN", "zh": "中文", "de": "DE", "fr": "FR", "es": "ES", "ja": "JP", "ko": "KR", "pt": "PT"}[l]
            lang_links.append(f'<a href="/{l}/">{label}</a>')
    
    nav_html = ""
    for key, href in [("articles", f"/{lang}/articles/"), ("routes", f"/{lang}/routes.html"), 
                      ("tickets", f"/{lang}/tickets.html"), ("passes", f"/{lang}/passes.html"),
                      ("live_status", f"/{lang}/live-status.html")]:
        cls = ' class="active"' if active_nav == key else ""
        nav_html += f'<a href="{href}"{cls}>{nav[key]}</a>'
    
    return f'''<header class="header">
    <div class="header-inner">
        <a href="/" class="logo">
            <div class="logo-icon">ET</div>
            Europe Train
        </a>
        <nav class="nav">
            {nav_html}
        </nav>
        <div class="lang-switcher">
            {' '.join(lang_links)}
        </div>
    </div>
</header>'''


def build_routes_page(lang):
    """构建 routes.html"""
    cfg = LANG_CONFIG[lang]
    header = build_header(lang, "routes")
    
    # 读取英文模板作为基础结构
    en_path = os.path.join(BASE_DIR, "en", "routes.html")
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()
    
    # 替换关键内容
    html = en_html.replace('<html lang="en">', f'<html lang="{cfg["lang"]}">')
    html = html.replace('Popular Routes | Europe Train - European Rail Travel Routes', 
                        f'{cfg["routes"]["title"]} | {cfg["title_suffix"]}')
    html = html.replace('href="https://www.europe-train.com/en/routes.html"', 
                        f'href="https://www.europe-train.com/{lang}/routes.html"')
    html = html.replace('Curated European train routes, from high-speed trains to scenic journeys', 
                        cfg["routes"]["subtitle"])
    
    # 替换header
    header_pattern = r'<header class="header">.*?</header>'
    html = re.sub(header_pattern, header, html, flags=re.DOTALL)
    
    return html


def build_tickets_page(lang):
    """构建 tickets.html"""
    cfg = LANG_CONFIG[lang]
    header = build_header(lang, "tickets")
    
    en_path = os.path.join(BASE_DIR, "en", "tickets.html")
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()
    
    html = en_html.replace('<html lang="en">', f'<html lang="{cfg["lang"]}">')
    html = html.replace('Tickets | Europe Train - European Train Ticket Booking Guide', 
                        f'{cfg["tickets"]["title"]} | {cfg["title_suffix"]}')
    html = html.replace('href="https://www.europe-train.com/en/tickets.html"', 
                        f'href="https://www.europe-train.com/{lang}/tickets.html"')
    html = html.replace('European train ticket booking guide and money-saving tips', 
                        cfg["tickets"]["subtitle"])
    
    header_pattern = r'<header class="header">.*?</header>'
    html = re.sub(header_pattern, header, html, flags=re.DOTALL)
    
    return html


def build_passes_page(lang):
    """构建 passes.html"""
    cfg = LANG_CONFIG[lang]
    header = build_header(lang, "passes")
    
    en_path = os.path.join(BASE_DIR, "en", "passes.html")
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()
    
    html = en_html.replace('<html lang="en">', f'<html lang="{cfg["lang"]}">')
    html = html.replace('Passes | Europe Train - Eurail & National Pass Guide', 
                        f'{cfg["passes"]["title"]} | {cfg["title_suffix"]}')
    html = html.replace('href="https://www.europe-train.com/en/passes.html"', 
                        f'href="https://www.europe-train.com/{lang}/passes.html"')
    html = html.replace('Complete European rail pass guide to find your best option', 
                        cfg["passes"]["subtitle"])
    
    header_pattern = r'<header class="header">.*?</header>'
    html = re.sub(header_pattern, header, html, flags=re.DOTALL)
    
    return html


def build_live_status_page(lang):
    """构建 live-status.html"""
    cfg = LANG_CONFIG[lang]
    header = build_header(lang, "live_status")
    
    en_path = os.path.join(BASE_DIR, "en", "live-status.html")
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()
    
    html = en_html.replace('<html lang="en">', f'<html lang="{cfg["lang"]}">')
    html = html.replace('European Train Live Status | Europe Train - Delays, Cancellations, Disruptions', 
                        f'{cfg["live_status"]["title"]} | {cfg["title_suffix"]}')
    html = html.replace('href="https://www.europe-train.com/en/live-status.html"', 
                        f'href="https://www.europe-train.com/{lang}/live-status.html"')
    html = html.replace('Real-time delays and cancellations for DB, SNCF, Trenitalia, SBB, ÖBB, and Renfe', 
                        cfg["live_status"]["subtitle"])
    
    # 替换header（live-status的header格式略有不同，是单行）
    header_pattern = r'<header class="header">.*?</header>'
    html = re.sub(header_pattern, header.replace('\n', ''), html, flags=re.DOTALL)
    
    return html


def main():
    langs = ["de", "fr", "es", "ja", "ko", "pt", "zh"]
    pages = ["routes.html", "tickets.html", "passes.html", "live-status.html"]
    
    builders = {
        "routes.html": build_routes_page,
        "tickets.html": build_tickets_page,
        "passes.html": build_passes_page,
        "live-status.html": build_live_status_page,
    }
    
    created = []
    skipped = []
    
    for lang in langs:
        lang_dir = os.path.join(BASE_DIR, lang)
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)
        
        for page in pages:
            page_path = os.path.join(lang_dir, page)
            
            # 检查是否已存在（zh站可能有部分页面）
            if os.path.exists(page_path):
                skipped.append(f"{lang}/{page} (exists)")
                continue
            
            html = builders[page](lang)
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(html)
            created.append(f"{lang}/{page}")
    
    print(f"Created {len(created)} files:")
    for f in created:
        print(f"  + {f}")
    
    if skipped:
        print(f"\nSkipped {len(skipped)} files:")
        for f in skipped:
            print(f"  = {f}")


if __name__ == "__main__":
    main()
