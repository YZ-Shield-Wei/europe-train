#!/usr/bin/env python3
"""
Daily Article Generator for europe-train.com
Generates one article per day with multi-language support
"""

import os
import json
import random
from datetime import datetime

# Article topics pool
ARTICLE_TOPICS = [
    {
        "en": "Berlin to Munich by Train: Complete Guide",
        "de": "Zug von Berlin nach München: Kompletter Reiseführer",
        "fr": "Train de Berlin à Munich: Guide Complet",
        "es": "Tren de Berlín a Múnich: Guía Completa",
        "zh": "柏林到慕尼黑火车完全指南"
    },
    {
        "en": "London to Amsterdam by Train: Eurostar + Thalys",
        "de": "Zug von London nach Amsterdam: Eurostar + Thalys",
        "fr": "Train de Londres à Amsterdam: Eurostar + Thalys",
        "es": "Tren de Londres a Ámsterdam: Eurostar + Thalys",
        "zh": "伦敦到阿姆斯特丹火车：欧洲之星+大力士"
    },
    {
        "en": "Swiss Travel Pass vs Half Fare Card: Which is Better?",
        "de": "Swiss Travel Pass vs Halbtax: Was ist besser?",
        "fr": "Swiss Travel Pass vs Carte Demi-Tarif: Lequel Choisir?",
        "es": "Swiss Travel Pass vs Tarjeta Media Tarifa: ¿Cuál es Mejor?",
        "zh": "瑞士通票 vs 半价卡：哪个更划算？"
    },
    {
        "en": "How to Book Cheap Train Tickets in Europe: 10 Tips",
        "de": "So Buchen Sie Günstige Zugtickets in Europa: 10 Tipps",
        "fr": "Comment Réserver des Billets de Train Pas Chers en Europe: 10 Conseils",
        "es": "Cómo Reservar Billetes de Tren Baratos en Europa: 10 Consejos",
        "zh": "如何预订欧洲便宜火车票：10个技巧"
    },
    {
        "en": "Night Trains in Europe: Routes, Cabins & Booking Tips",
        "de": "Nachtzüge in Europa: Routen, Kabinen & Buchungstipps",
        "fr": "Trains de Nuit en Europe: Routes, Cabines & Conseils",
        "es": "Trenes Nocturnos en Europa: Rutas, Cabinas & Consejos",
        "zh": "欧洲夜火车：路线、卧铺和预订技巧"
    },
    {
        "en": "Amsterdam to Berlin by Train: The Perfect Route",
        "de": "Amsterdam nach Berlin mit dem Zug: Die Perfekte Route",
        "fr": "Amsterdam à Berlin en Train: L'Itinéraire Parfait",
        "es": "Ámsterdam a Berlín en Tren: La Ruta Perfecta",
        "zh": "阿姆斯特丹到柏林火车：完美路线"
    },
    {
        "en": "Barcelona to Madrid by AVE: Spain's High-Speed Experience",
        "de": "Barcelona nach Madrid mit AVE: Spanisches Hochgeschwindigkeitserlebnis",
        "fr": "Barcelone à Madrid par AVE: L'Expérience Grande Vitesse Espagnole",
        "es": "Barcelona a Madrid en AVE: La Experiencia de Alta Velocidad Española",
        "zh": "巴塞罗那到马德里AVE：西班牙高铁体验"
    },
    {
        "en": "Interrail vs Eurail: Which Rail Pass is Right for You?",
        "de": "Interrail vs Eurail: Welcher Rail Pass ist der Richtige?",
        "fr": "Interrail vs Eurail: Quel Pass Ferroviaire Choisir?",
        "es": "Interrail vs Eurail: ¿Qué Pase Ferroviario es Mejor?",
        "zh": "Interrail vs Eurail：哪个铁路通票适合你？"
    },
    {
        "en": "Vienna to Prague by Train: A Scenic Central European Journey",
        "de": "Wien nach Prag mit dem Zug: Eine Malerische Mitteleuropäische Reise",
        "fr": "Vienne à Prague en Train: Un Voyage Pittoresque en Europe Centrale",
        "es": "Viena a Praga en Tren: Un Viaje Escénico por Europa Central",
        "zh": "维也纳到布拉格火车：中欧风景之旅"
    },
    {
        "en": "European Train Food Guide: What to Eat on Your Journey",
        "de": "Europäischer Zug-Essen-Guide: Was Sie auf Ihrer Reise Essen",
        "fr": "Guide Culinaire des Trains Européens: Quoi Manger Pendant Votre Voyage",
        "es": "Guía de Comida en Trenes Europeos: Qué Comer en Tu Viaje",
        "zh": "欧洲火车美食指南：旅途中吃什么"
    }
]

def get_today_topic():
    """Get topic based on day of year"""
    day_of_year = datetime.now().timetuple().tm_yday
    index = day_of_year % len(ARTICLE_TOPICS)
    return ARTICLE_TOPICS[index]

def generate_article_html(topic, lang):
    """Generate article HTML for specific language"""
    # This is a simplified version - full implementation would include complete article content
    title = topic[lang]
    
    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Europe Train</title>
    <meta name="description" content="{title}: Complete guide with route options, booking tips, and money-saving strategies.">
    <link rel="canonical" href="https://www.europe-train.com/{lang}/articles/{topic['en'].lower().replace(' ', '-').replace(':', '')}.html">
    <link rel="stylesheet" href="/css/article.css">
    <link rel="stylesheet" href="/css/global.css">
</head>
<body>
    <header class="header">
        <div class="header-inner">
            <a href="/{lang}/" class="logo">
                <div class="logo-icon">ET</div>
                Europe Train
            </a>
            <nav class="nav">
                <a href="/{lang}/articles/">Travel Guides</a>
                <a href="/{lang}/routes.html">Popular Routes</a>
                <a href="/{lang}/tickets.html">Tickets</a>
                <a href="/{lang}/passes.html">Rail Passes</a>
                <a href="/{lang}/live-status.html">Live Status</a>
            </nav>
        </div>
    </header>
    <article class="article">
        <div class="hero-image" style="background: linear-gradient(135deg, #e65100 0%, #bf360c 100%);">
            <h1>{title}</h1>
        </div>
        <div class="article-content">
            <p class="lead">Article content coming soon...</p>
        </div>
    </article>
</body>
</html>"""
    return html

def main():
    """Main function to generate daily article"""
    topic = get_today_topic()
    
    # Generate for all languages
    languages = ['en', 'de', 'fr', 'es', 'zh']
    
    for lang in languages:
        # Create directory if not exists
        article_dir = f'/root/.openclaw/workspace/europe-train/{lang}/articles'
        os.makedirs(article_dir, exist_ok=True)
        
        # Generate filename from English title
        filename = topic['en'].lower().replace(' ', '-').replace(':', '') + '.html'
        filepath = os.path.join(article_dir, filename)
        
        # Generate HTML
        html = generate_article_html(topic, lang)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Generated: {filepath}")
    
    print(f"\n✅ Daily article generated: {topic['en']}")
    print(f"Languages: {', '.join(languages)}")

if __name__ == '__main__':
    main()
