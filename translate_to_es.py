#!/usr/bin/env python3
"""Translate English articles to Spanish, preserving HTML structure."""

import os
import re
import shutil

# Translation dictionaries for common UI elements and navigation
UI_TRANSLATIONS = {
    # Navigation
    "Travel Guides": "Guías de Viaje",
    "Popular Routes": "Rutas Populares",
    "Book Tickets": "Reservar Billetes",
    "Ticket Booking": "Reservar Billetes",
    "Rail Passes": "Pases Ferroviarios",
    "Passes": "Pases",
    
    # Language switcher
    "EN": "EN",
    "中文": "中文",
    "DE": "DE",
    "FR": "FR",
    "ES": "ES",
    "JP": "JP",
    "KR": "KR",
    "PT": "PT",
    
    # Breadcrumb / Common
    "Home": "Inicio",
    "Articles": "Artículos",
    "Article": "Artículo",
    
    # Footer
    "All rights reserved": "Todos los derechos reservados",
    
    # Article meta
    "Updated": "Actualizado",
    "Reading time": "Tiempo de lectura",
    "minutes": "minutos",
    "min": "min",
    "Category": "Categoría",
    "Cost Comparison": "Comparación de Costos",
    "Train Experience": "Experiencia en Tren",
    "Scenic Trains": "Trenes Panorámicos",
    "France": "Francia",
    "Germany": "Alemania",
    "Italy": "Italia",
    "Spain": "España",
    "Booking Guide": "Guía de Reservas",
    "Passenger Rights": "Derechos de Pasajeros",
    "App Comparison": "Comparación de Apps",
    "Station Guide": "Guía de Estaciones",
    "Expert Guide": "Guía Experta",
    "Deep Dive": "Análisis Profundo",
    
    # Common article sections
    "Key Takeaways": "Puntos Clave",
    "Key Highlights": "Puntos Destacados",
    "Quick Verdict": "Veredicto Rápido",
    
    # Related articles
    "Related Guides": "Guías Relacionadas",
    "Related": "Relacionado",
    
    # Article footer
    "Written by": "Escrito por",
    "based on": "basado en",
    "real-world test": "prueba en el mundo real",
    "Fares and schedules are subject to change": "Las tarifas y horarios están sujetos a cambios",
    "please check current information before booking": "verifique la información actual antes de reservar",
    "Rules may change": "Las reglas pueden cambiar",
    "always check the latest regulations": "consulte siempre las últimas regulaciones",
    "of each railway company": "de cada compañía ferroviaria",
    
    # Tags
    "Ticket Rules": "Reglas de Billetes",
    "Guide": "Guía",
    "Dining Car": "Coche Restaurante",
    
    # Common table headers
    "Feature": "Característica",
    "Details": "Detalles",
    "Item": "Elemento",
    "Price": "Precio",
    "What's Included": "Qué Incluye",
    "Class": "Clase",
    "Route": "Ruta",
    "Origin": "Origen",
    "Destination": "Destino",
    "Duration": "Duración",
    "Distance": "Distancia",
    "Time": "Tiempo",
    "Fare": "Tarifa",
    "Highlights": "Puntos Destacados",
    "Operator": "Operador",
    "Fares": "Tarifas",
    "Top Speed": "Velocidad Máxima",
    "Ticket Type": "Tipo de Billete",
    "Price Range": "Rango de Precio",
    "Refund/Change Rules": "Reglas de Reembolso/Cambio",
    "Best For": "Mejor Para",
    "Card": "Tarjeta",
    "Annual Fee": "Cuota Anual",
    "Discount": "Descuento",
    "Break-even": "Punto de Equilibrio",
    "Season": "Temporada",
    "Pros": "Ventajas",
    "Cons": "Desventajas",
    "Rating": "Valoración",
    "Train": "Tren",
    "Second Class": "Segunda Clase",
    "First Class": "Primera Clase",
    "Reservation Fee": "Tarifa de Reserva",
    "Country": "País",
    "Validation Required": "Validación Requerida",
    "Check Frequency": "Frecuencia de Control",
    "Fine for No Ticket": "Multa Sin Billete",
    "Child Policy": "Política Infantil",
    "Transport": "Transporte",
    "City Center to City Center": "Centro a Centro",
    
    # Common UI labels
    "Tag": "Etiqueta",
    "Date": "Fecha",
    
    # Month names (for dates)
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre",
}


def translate_common_ui(text):
    """Translate common UI elements in HTML text."""
    for en, es in UI_TRANSLATIONS.items():
        # Be careful to only match whole words/phrases in text content, not URLs or attributes
        # Use word boundaries for short words, phrase matching for longer ones
        if len(en) <= 3:
            continue  # Skip very short ones to avoid breaking URLs
        # Replace in text content (between tags)
        pattern = re.compile(r'>([^<]*\b' + re.escape(en) + r'\b[^<]*)<')
        text = pattern.sub(lambda m: '>' + m.group(1).replace(en, es) + '<', text)
    return text


def translate_article_index(html_content):
    """Translate the articles index page."""
    # Replace lang
    html_content = html_content.replace('lang="en"', 'lang="es"')
    
    # Replace canonical and hreflang
    html_content = html_content.replace('https://www.europe-train.com/en/articles/', 'https://www.europe-train.com/es/articles/')
    html_content = html_content.replace('hreflang="en"', 'hreflang="es"')
    
    # Add Spanish hreflang alternate (remove old zh-CN if present, add proper alternates)
    # Replace the alternate tags section
    old_alternates = '''<link rel="alternate" hreflang="en" href="https://www.europe-train.com/en/articles/">
    <link rel="alternate" hreflang="zh-CN" href="https://www.europe-train.com/articles/">'''
    new_alternates = '''<link rel="alternate" hreflang="es" href="https://www.europe-train.com/es/articles/">
    <link rel="alternate" hreflang="en" href="https://www.europe-train.com/en/articles/">
    <link rel="alternate" hreflang="zh-CN" href="https://www.europe-train.com/articles/">'''
    html_content = html_content.replace(old_alternates, new_alternates)
    
    # Update title
    html_content = html_content.replace(
        '<title>Travel Guides | Europe Train - European Train Travel Tips</title>',
        '<title>Guías de Viaje | Europe Train - Consejos para Viajar en Tren por Europa</title>'
    )
    
    # Update meta description
    html_content = html_content.replace(
        'content="Europe Train Travel Guides: cost comparisons, train experiences, in-depth guides to help you plan the perfect European train journey."',
        'content="Guías de Viaje en Tren por Europa: comparaciones de costos, experiencias en tren, guías detalladas para ayudarte a planificar el viaje perfecto en tren por Europa."'
    )
    
    # Update navigation paths
    html_content = html_content.replace('href="/en/', 'href="/es/')
    html_content = html_content.replace('href="/zh/', 'href="/zh/')  # Keep Chinese link
    
    # Update active language
    html_content = html_content.replace('<a href="/es/" class="active">EN</a>', '<a href="/es/" class="active">ES</a>')
    html_content = html_content.replace('<a href="/en/" class="active">EN</a>', '<a href="/en/">EN</a>')
    
    # Update hero text
    html_content = html_content.replace(
        '<div class="hero-image">\n            Travel Guides\n        </div>',
        '<div class="hero-image">\n            Guías de Viaje\n        </div>'
    )
    
    # Update intro paragraph
    html_content = html_content.replace(
        'In-depth comparisons, train experiences, and expert guides to help you plan the perfect European train journey',
        'Comparaciones detalladas, experiencias en tren y guías expertas para ayudarte a planificar el viaje perfecto en tren por Europa'
    )
    
    # Update category titles
    html_content = html_content.replace('>Cost Comparisons<', '>Comparaciones de Costos<')
    html_content = html_content.replace('>Train Experiences<', '>Experiencias en Tren<')
    html_content = html_content.replace('>Country Guides<', '>Guías por País<')
    html_content = html_content.replace('>Practical Guides<', '>Guías Prácticas<')
    html_content = html_content.replace('>Expert Guides<', '>Guías Expertas<')
    
    # Replace article titles and descriptions manually
    replacements = [
        ("Paris to Zurich: Train vs Flight vs Car", "París a Zúrich: Tren vs Avión vs Coche"),
        ("487km journey, three transport modes fully compared. TGV Lyria from €49, 4 hours direct to city center...", 
         "Viaje de 487 km, tres modos de transporte comparados en profundidad. TGV Lyria desde €49, 4 horas directo al centro de la ciudad..."),
        ("Cost Comparison", "Comparación de Costos"),
        
        ("TGV Lyria Experience: Paris to Lausanne", "Experiencia TGV Lyria: París a Lausana"),
        ("Wake up naturally, walk to the station, enjoy dining car coffee, three hours strolling by Swiss lakeside...",
         "Despierta naturalmente, camina hasta la estación, disfruta del café en el coche restaurante, tres horas paseando por la orilla del lago suizo..."),
        ("Train Experience", "Experiencia en Tren"),
        
        ("London-Paris Eurostar Complete Guide", "Guía Completa del Eurostar Londres-París"),
        ("The ultimate rail experience crossing the English Channel, from booking to boarding...",
         "La experiencia ferroviaria definitiva cruzando el Canal de la Mancha, desde la reserva hasta el embarque..."),
        
        ("Swiss Scenic Trains Ultimate Guide", "Guía Definitiva de los Trenes Panorámicos Suizos"),
        ("Glacier Express, Bernina Express, GoldenPass Line - a visual feast through the Alps...",
         "Glacier Express, Bernina Express, GoldenPass Line - un festín visual a través de los Alpes..."),
        ("Scenic Trains", "Trenes Panorámicos"),
        
        ("France TGV High-Speed Train Complete Guide", "Guía Completa del TGV de Alta Velocidad de Francia"),
        ("French high-speed rail network explained, from booking tips to seat selection, TGV Duplex double-decker experience...",
         "Red ferroviaria de alta velocidad francesa explicada, desde consejos de reserva hasta selección de asientos, experiencia en el TGV Duplex de dos pisos..."),
        ("France", "Francia"),
        
        ("Germany ICE High-Speed Train Complete Guide", "Guía Completa del ICE de Alta Velocidad de Alemania"),
        ("Germany's flagship rail service, 300km/h, connecting Berlin, Munich, Frankfurt...",
         "El servicio ferroviario insignia de Alemania, 300 km/h, conectando Berlín, Múnich, Frankfurt..."),
        ("Germany", "Alemania"),
        
        ("Italy Frecciarossa Complete Guide", "Guía Completa del Frecciarossa de Italia"),
        ("Italy's high-speed Red Arrow train, Rome to Milan in 3 hours, Ferrari-designed 360km/h...",
         "El tren Flecha Roja de alta velocidad de Italia, Roma a Milán en 3 horas, diseñado por Ferrari a 360 km/h..."),
        ("Italy", "Italia"),
        
        ("Spain AVE High-Speed Train Complete Guide", "Guía Completa del AVE de Alta Velocidad de España"),
        ("Spain's high-speed rail network, Madrid-Barcelona in 2.5 hours, the Iberian railway revolution...",
         "Red ferroviaria de alta velocidad de España, Madrid-Barcelona en 2.5 horas, la revolución ferroviaria ibérica..."),
        ("Spain", "España"),
        
        ("Complete Guide to European Train Seat Reservations", "Guía Completa de Reservas de Asientos en Trenes Europeos"),
        ("Which trains need reservations? How to book? How much does it cost? 5-country comparison at a glance...",
         "¿Qué trenes necesitan reserva? ¿Cómo reservar? ¿Cuánto cuesta? Comparación de 5 países de un vistazo..."),
        ("Booking Guide", "Guía de Reservas"),
        
        ("Complete Guide to European Train Delay Compensation", "Guía Completa de Compensación por Retrasos en Trenes Europeos"),
        ("EU261 regulation explained, compensation from 15-minute delays, up to 100% ticket price refund...",
         "Regulación EU261 explicada, compensación desde retrasos de 15 minutos, hasta reembolso del 100% del precio del billete..."),
        ("Passenger Rights", "Derechos de Pasajeros"),
        
        ("European Train Apps Comparison", "Comparación de Apps de Tren Europeas"),
        ("Trainline, Omio, Rail Planner, national railway apps - which is the best?...",
         "Trainline, Omio, Rail Planner, apps ferroviarias nacionales - ¿cuál es la mejor?..."),
        ("App Comparison", "Comparación de Apps"),
        
        ("Major European Train Stations Guide", "Guía de las Principales Estaciones de Tren Europeas"),
        ("Paris Gare du Nord, London St Pancras, Berlin Hauptbahnhof - facilities, transfers, and local tips...",
         "Gare du Nord de París, St Pancras de Londres, Hauptbahnhof de Berlín - instalaciones, transbordos y consejos locales..."),
        ("Station Guide", "Guía de Estaciones"),
        
        ("Complete Guide to European Train Ticket Rules", "Guía Completa de las Reglas de Billetes de Tren por País en Europa"),
        ("Understand every code and symbol on your ticket, avoid fines and embarrassment. 5-country comparison...",
         "Comprende cada código y símbolo en tu billete para evitar multas y momentos incómodos. Comparación de 5 países..."),
        ("Expert Guide", "Guía Experta"),
    ]
    
    for old, new in replacements:
        html_content = html_content.replace(old, new)
    
    # Update footer
    html_content = html_content.replace(
        "© 2026 Europe Train Travel Guide. All rights reserved.",
        "© 2026 Guía de Viaje en Tren por Europa. Todos los derechos reservados."
    )
    
    return html_content


def translate_article(html_content, article_name):
    """Translate a single article to Spanish."""
    # Replace lang
    html_content = html_content.replace('lang="en"', 'lang="es"')
    
    # Update canonical URLs
    html_content = html_content.replace('/en/articles/', '/es/articles/')
    
    # Update hreflang alternates - add es, keep en and zh-CN
    # Find and replace alternate tags
    if 'hreflang="en"' in html_content and 'hreflang="zh-CN"' in html_content:
        # Replace the pattern: en first, then zh-CN
        old_pattern = re.compile(
            r'<link rel="alternate" hreflang="en" href="https://www\.europe-train\.com/en/articles/([^"]+)">\s*\n\s*<link rel="alternate" hreflang="zh-CN" href="https://www\.europe-train\.com/articles/([^"]+)">'
        )
        new_alternates = '<link rel="alternate" hreflang="es" href="https://www.europe-train.com/es/articles/\\1">\n    <link rel="alternate" hreflang="en" href="https://www.europe-train.com/en/articles/\\1">\n    <link rel="alternate" hreflang="zh-CN" href="https://www.europe-train.com/articles/\\2">'
        html_content = old_pattern.sub(new_alternates, html_content)
    
    # Update navigation paths
    html_content = html_content.replace('href="/en/', 'href="/es/')
    
    # Update active language in lang switcher
    html_content = html_content.replace('<a href="/es/" class="active">EN</a>', '<a href="/es/" class="active">ES</a>')
    html_content = html_content.replace('<a href="/en/" class="active">EN</a>', '<a href="/en/">EN</a>')
    
    # Update breadcrumb
    html_content = html_content.replace('>Home<', '>Inicio<')
    html_content = html_content.replace('>Travel Guides<', '>Guías de Viaje<')
    html_content = html_content.replace('>Articles<', '>Artículos<')
    html_content = html_content.replace('>Article<', '>Artículo<')
    
    # Update footer
    html_content = html_content.replace(
        "© 2026 Europe Train Travel Guide. All rights reserved.",
        "© 2026 Guía de Viaje en Tren por Europa. Todos los derechos reservados."
    )
    
    # Update common article meta
    html_content = html_content.replace('Updated June 2026', 'Actualizado Junio 2026')
    html_content = html_content.replace('Reading time: 10 minutes', 'Tiempo de lectura: 10 minutos')
    html_content = html_content.replace('Reading time: 12 min', 'Tiempo de lectura: 12 min')
    html_content = html_content.replace('Reading time: 12 minutes', 'Tiempo de lectura: 12 minutos')
    
    # Update "Key Takeaways" / "Key Highlights" / "Quick Verdict"
    html_content = html_content.replace('>Key Takeaways<', '>Puntos Clave<')
    html_content = html_content.replace('>Key Highlights<', '>Puntos Destacados<')
    html_content = html_content.replace('>Quick Verdict<', '>Veredicto Rápido<')
    html_content = html_content.replace('>Quick Verdict: The Most Pleasant Way to Travel Europe<', '>Veredicto Rápido: La Forma Más Agradable de Viajar por Europa<')
    html_content = html_content.replace('>Quick Verdict: Train Wins<', '>Veredicto Rápido: El Tren Gana<')
    html_content = html_content.replace('>Quick Verdict: Rules Vary Widely<', '>Veredicto Rápido: Las Reglas Varían Mucho<')
    
    # Update "Related Guides"
    html_content = html_content.replace('>Related Guides<', '>Guías Relacionadas<')
    
    # Update common section headers
    html_content = html_content.replace('>Cost & Time Overview<', '>Resumen de Costos y Tiempo<')
    html_content = html_content.replace('>Summary & Recommendations<', '>Resumen y Recomendaciones<')
    
    # Update footer article text
    html_content = html_content.replace(
        'Written by the Europe Train editorial team, based on a January 2025 real-world test.',
        'Escrito por el equipo editorial de Europe Train, basado en una prueba en el mundo real de enero de 2025.'
    )
    html_content = html_content.replace(
        'Fares and schedules are subject to change; please check current information before booking.',
        'Las tarifas y horarios están sujetos a cambios; verifique la información actual antes de reservar.'
    )
    html_content = html_content.replace(
        'Rules may change; always check the latest regulations of each railway company.',
        'Las reglas pueden cambiar; consulte siempre las últimas regulaciones de cada compañía ferroviaria.'
    )
    
    return html_content


def translate_seat_reservation_guide(html_content):
    """Special translation for seat reservation guide."""
    html_content = translate_article(html_content, "seat-reservation-guide")
    
    # Title and meta
    html_content = html_content.replace(
        '<title>Complete Guide to European Train Seat Reservations | Europe Train - Rules, Fees & Tips</title>',
        '<title>Guía Completa de Reservas de Asientos en Trenes Europeos | Europe Train - Reglas, Tarifas y Consejos</title>'
    )
    html_content = html_content.replace(
        'content="Ultimate guide to European train seat reservations: which trains require booking, reservation fees, how to choose seats, booking tips, and avoiding standing-only journeys."',
        'content="Guía definitiva de reservas de asientos en trenes europeos: qué trenes requieren reserva, tarifas de reserva, cómo elegir asientos, consejos de reserva y evitar viajes de pie."'
    )
    html_content = html_content.replace(
        '<meta property="og:title" content="Complete Guide to European Train Seat Reservations | Europe Train">',
        '<meta property="og:title" content="Guía Completa de Reservas de Asientos en Trenes Europeos | Europe Train">'
    )
    html_content = html_content.replace(
        '<meta property="og:description" content="European train reservation rules, fees, and tips explained">',
        '<meta property="og:description" content="Reglas, tarifas y consejos de reserva de trenes europeos explicados">'
    )
    
    # Breadcrumb current
    html_content = html_content.replace('>Seat Reservation Guide<', '>Guía de Reserva de Asientos<')
    
    # Article header
    html_content = html_content.replace(
        '<h1>Complete Guide to European Train Seat Reservations</h1>',
        '<h1>Guía Completa de Reservas de Asientos en Trenes Europeos</h1>'
    )
    html_content = html_content.replace(
        '<p class="subtitle">2026 Latest: Which trains require reservations, fees, how to choose seats, and booking tips</p>',
        '<p class="subtitle">2026 Actualizado: Qué trenes requieren reservas, tarifas, cómo elegir asientos y consejos de reserva</p>'
    )
    
    # Content sections
    html_content = html_content.replace('>1. Which Trains Require Reservations?<', '>1. ¿Qué Trenes Requieren Reserva?<')
    html_content = html_content.replace('>2. Reservation Fee Comparison<', '>2. Comparación de Tarifas de Reserva<')
    html_content = html_content.replace('>3. How to Book Seats<', '>3. Cómo Reservar Asientos<')
    html_content = html_content.replace('>4. Seat Selection Tips<', '>4. Consejos para Seleccionar Asientos<')
    html_content = html_content.replace('>5. Eurail Pass Reservation Guide<', '>5. Guía de Reserva con Pase Eurail<')
    html_content = html_content.replace('>6. Frequently Asked Questions<', '>6. Preguntas Frecuentes<')
    
    # Table headers
    html_content = html_content.replace('>Train Type<', '>Tipo de Tren<')
    html_content = html_content.replace('>Reservation Required<', '>Reserva Requerida<')
    html_content = html_content.replace('>Fee<', '>Tarifa<')
    html_content = html_content.replace('>Notes<', '>Notas<')
    html_content = html_content.replace('>Railway Company<', '>Compañía Ferroviaria<')
    html_content = html_content.replace('>1st Class<', '>Primera Clase<')
    html_content = html_content.replace('>2nd Class<', '>Segunda Clase<')
    html_content = html_content.replace('>Scenic Train<', '>Tren Panorámico<')
    html_content = html_content.replace('>Night Train<', '>Tren Nocturno<')
    
    # Table content
    html_content = html_content.replace('>Mandatory<', '>Obligatoria<')
    html_content = html_content.replace('>Recommended<', '>Recomendada<')
    html_content = html_content.replace('>Not required<', '>No requerida<')
    html_content = html_content.replace('>Free<', '>Gratis<')
    html_content = html_content.replace('>All TGV trains<', '>Todos los trenes TGV<')
    html_content = html_content.replace('>Not mandatory, but advised in peak season<', '>No obligatoria, pero recomendada en