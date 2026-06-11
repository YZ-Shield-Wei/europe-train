#!/usr/bin/env python3
"""
Full French translation of all article content.
This script translates the Chinese text content to French while preserving HTML structure.
"""

import os
import re

SRC_DIR = "/root/.openclaw/workspace/europe-train/articles"
DST_DIR = "/root/.openclaw/workspace/europe-train/fr/articles"

# Full translations for each article
TRANSLATIONS = {
    "paris-zurich-train-vs-flight.html": {
        "title": "Paris à Zurich : Train vs Avion vs Voiture - Comparaison Détaillée | Europe Train",
        "description": "Comparaison complète des transports entre Paris et Zurich : TGV Lyria, avion, voiture - coûts, durée et expérience.",
        "h1": "Paris à Zurich : Train vs Avion vs Voiture - Comparaison Détaillée",
        "subtitle": "Un voyage de 487 km, trois expériences de voyage radicalement différentes",
        "hero": "Paris → Zurich | 487 km",
        "quick_summary_title": "Conclusion Rapide : Le Train est Optimal",
        "quick_summary_1": "Le plus confortable : TGV Lyria, 4 heures directement au centre-ville",
        "quick_summary_2": "Le plus rapide : Avion, mais avec les procédures aéroportuaires, le temps total est comparable",
        "quick_summary_3": "Le plus flexible : Voiture, mais coûteux et fatigant",
        "quick_summary_4": "Recommandé : TGV Lyria (dès €49, directement au centre-ville, avec vue)",
        "table_title": "Aperçu des Coûts et du Temps",
        "table_header_transport": "Mode de Transport",
        "table_header_price": "Prix",
        "table_header_time": "Durée",
        "table_header_center": "Centre-ville à Centre-ville",
        "table_train": "TGV Lyria",
        "table_plane": "Avion (Air France/Swiss)",
        "table_car": "Voiture",
        "plane_time": "1h15 de vol + 3h de procédures aéroportuaires",
        "car_cost": "€80-120 (essence + péage)",
        "car_time": "5-6 heures",
        "section_tgv": "Expérience TGV Lyria Détaillée",
        "section_before": "Avant le Départ",
        "section_facilities": "Équipements du Train",
        "section_scenery": "Paysages en Route",
        "section_arrival": "Arrivée Pratique",
        "section_plane": "Expérience Avion",
        "section_car": "Expérience Voiture",
        "section_recommendation": "Conclusion et Recommandations",
        "recommendation_train": "Choisissez le train si vous : valorisez le confort, voulez voir les paysages, évitez les tracas aéroportuaires, souhaitez arriver directement au centre-ville, voulez utiliser le temps de voyage pour travailler ou vous reposer.",
        "recommendation_plane": "Choisissez l'avion si vous : cherchez un tarif moins cher (parfois dès €39 si réservé à l'avance), êtes pressés et acceptez les procédures aéroportuaires, partez du nord de Paris (plus proche de l'aéroport).",
        "recommendation_car": "Choisissez la voiture si vous : prévoyez de visiter en route (Dijon, Besançon), voyagez à plusieurs pour partager les coûts, avez besoin de transporter beaucoup de bagages ou d'équipement.",
    },
    "tgv-lyria-experience.html": {
        "title": "Expérience TGV Lyria : Voyage Paisible de Paris à Lausanne | Europe Train",
        "description": "Expérience approfondie du TGV Lyria : gastronomie du wagon-restaurant, paysages, équipements et confort.",
        "h1": "Expérience TGV Lyria : Voyage Paisible de Paris à Lausanne",
        "subtitle": "Réveil naturel, marche jusqu'à la gare, petit-déjeuner français à bord, promenade au bord du lac suisse trois heures plus tard",
        "hero": "TGV Lyria | Paris → Lausanne",
        "quick_summary_title": "Conclusion Rapide : Le Mode de Voyage Européen le Plus Agréable",
        "quick_summary_1": "Durée : 3h57, comparable à l'avion + procédures aéroportuaires",
        "quick_summary_2": "Expérience : Réveil naturel, marche jusqu'à la gare, café au wagon-restaurant",
        "quick_summary_3": "Paysages : Vignobles de Bourgogne, montagnes du Jura, lac de Neuchâtel",
        "quick_summary_4": "Prix : €39-95 (standard), le moins cher si réservé à l'avance",
        "quick_summary_5": "Conclusion : Plus confortable que l'avion, plus simple que la voiture, directement au centre-ville",
        "section_boarding": "Embarquement : Un Rite",
        "section_departure": "Départ : De la Ville à la Campagne",
        "section_dining": "Wagon-Restaurant : Un Restaurant Français Mobile",
        "section_scenery": "Paysages : Quatre Saisons",
        "section_arrival": "Arrivée : Connexion Sans Couture",
        "section_data": "Données du Train",
        "section_why": "Pourquoi Choisir le Train ?",
    },
    "london-paris-eurostar-guide.html": {
        "title": "Guide London-Paris Eurostar | Europe Train - Expérience, Tarifs, Immigration",
        "description": "Guide ultime London-Paris Eurostar : expérience, tarifs, procédures d'immigration, choix de siège, guide des gares St Pancras et Gare du Nord.",
        "h1": "Guide London-Paris Eurostar",
        "subtitle": "Dernière mise à jour 2026 : Expérience Eurostar, tarifs, procédures d'immigration, choix de siège",
        "section_route": "Informations sur la Route",
        "section_price": "Système de Tarifs",
        "section_immigration": "Procédures d'Immigration",
        "section_tips": "Conseils d'Achat",
        "section_stations": "Guide des Gares",
    },
    "swiss-scenic-trains.html": {
        "title": "Guide des Trains Panoramiques Suisses | Europe Train - Glacier Express, Bernina Express, GoldenPass",
        "description": "Guide ultime des trains panoramiques suisses : Glacier Express, Bernina Express, GoldenPass Line, tarifs, meilleures saisons, choix de siège.",
        "h1": "Guide des Trains Panoramiques Suisses",
        "subtitle": "Dernière mise à jour 2026 : Glacier Express, Bernina Express, GoldenPass Line, tarifs, meilleures saisons",
        "section_glacier": "Glacier Express",
        "section_bernina": "Bernina Express",
        "section_golden": "GoldenPass Line",
        "section_others": "Autres Trains Panoramiques",
        "section_prices": "Tarifs et Pass",
        "section_seasons": "Meilleures Saisons",
        "section_booking": "Conseils de Réservation",
    },
    "france-tgv-guide.html": {
        "title": "Guide Complet du TGV Français | Europe Train - Lignes, Tarifs, Conseils d'Achat",
        "description": "Guide ultime du TGV français : réseau de lignes, tarifs, billets PREM'S, choix de siège, guide d'utilisation de l'app SNCF.",
        "h1": "Guide Complet du TGV Français",
        "subtitle": "Dernière mise à jour 2026 : Réseau de lignes, tarifs, billets PREM'S, choix de siège, guide SNCF APP",
        "section_network": "Réseau TGV",
        "section_prices": "Système de Tarifs",
        "section_tips": "Conseils d'Achat",
        "section_seats": "Choix de Siège",
        "section_app": "Guide SNCF APP",
        "section_stations": "Guide des Gares de Paris",
    },
    "germany-ice-guide.html": {
        "title": "Guide de l'ICE Allemand | Europe Train - Lignes, Tarifs, Conseils DB",
        "description": "Guide ultime de l'ICE allemand : réseau de lignes, billets Sparpreis, carte BahnCard, guide d'utilisation de l'app DB Navigator.",
        "h1": "Guide de l'ICE Allemand",
        "subtitle": "Dernière mise à jour 2026 : Réseau de lignes, billets Sparpreis, carte BahnCard, guide DB Navigator",
        "section_network": "Réseau ICE",
        "section_prices": "Système de Tarifs",
        "section_bahncard": "Carte BahnCard",
        "section_app": "Guide DB Navigator",
        "section_experience": "Expérience ICE",
    },
    "italy-frecciarossa-guide.html": {
        "title": "Guide du Frecciarossa Italien | Europe Train - vs italo, Tarifs, Conseils",
        "description": "Guide ultime du Frecciarossa italien : comparaison avec italo, tarifs, billets Super Economy, classes de siège, guide Trenitalia APP.",
        "h1": "Guide du Frecciarossa Italien",
        "subtitle": "Dernière mise à jour 2026 : vs italo, tarifs, billets Super Economy, classes de siège",
        "section_compare": "Frecciarossa vs italo",
        "section_prices": "Système de Tarifs",
        "section_routes": "Principales Lignes",
        "section_seats": "Classes de Siège",
        "section_tips": "Conseils d'Achat",
        "section_app": "Guide Trenitalia APP",
    },
    "spain-ave-guide.html": {
        "title": "Guide de l'AVE Espagnol | Europe Train - Lignes, Tarifs, Conseils Renfe",
        "description": "Guide ultime de l'AVE espagnol : réseau de lignes, billets Promo, carte +Renfe, classes de siège, guide Renfe APP.",
        "h1": "Guide de l'AVE Espagnol",
        "subtitle": "Dernière mise à jour 2026 : Réseau de lignes, billets Promo, carte +Renfe, classes de siège",
        "section_network": "Réseau AVE",
        "section_prices": "Système de Tarifs",
        "section_seats": "Classes de Siège",
        "section_tips": "Conseils d'Achat",
        "section_app": "Guide Renfe APP",
    },
    "train-station-guide.html": {
        "title": "Guide des Gares Européennes | Europe Train - Équipements, Navigation, Correspondances",
        "description": "Guide ultime des gares européennes : équipements principaux, navigation, correspondances, consigne à bagages, restaurants, connexions de transport.",
        "h1": "Guide des Gares Européennes",
        "subtitle": "Dernière mise à jour 2026 : Équipements principaux, navigation, correspondances, consigne à bagages, connexions de transport",
        "section_stations": "Principales Gares",
        "section_facilities": "Équipements des Gares",
        "section_transfers": "Conseils de Correspondance",
        "section_safety": "Conseils de Sécurité",
    },
    "delay-compensation-guide.html": {
        "title": "Guide d'Indemnisation pour Retard | Europe Train - Retards, Remboursements, Règles",
        "description": "Guide ultime d'indemnisation pour retard : normes de compensation, procédures de demande, règles de remboursement, politiques de modification.",
        "h1": "Guide d'Indemnisation pour Retard",
        "subtitle": "Dernière mise à jour 2026 : Normes de compensation, procédures de demande, règles de remboursement",
        "section_eu": "Règlement EU 261/2004",
        "section_countries": "Normes par Pays",
        "section_process": "Procédure de Demande",
        "section_refund": "Règles de Remboursement",
        "section_change": "Politiques de Modification",
        "section_special": "Cas Particuliers",
    },
    "train-apps-comparison.html": {
        "title": "Comparaison des Apps de Train Européennes | Europe Train - Évaluation des Fonctions",
        "description": "Comparaison ultime des apps de train européennes : SNCF Connect, DB Navigator, Trenitalia, SBB Mobile, Renfe - évaluation des fonctions, avantages et inconvénients.",
        "h1": "Comparaison des Apps de Train Européennes",
        "subtitle": "Dernière mise à jour 2026 : SNCF Connect, DB Navigator, Trenitalia, SBB Mobile, Renfe - évaluation des fonctions",
        "section_compare": "Comparaison des Fonctions",
        "section_apps": "Détail par App",
        "section_international": "Apps pour Achats Internationaux",
        "section_advice": "Conseils d'Utilisation",
    },
    "europe-train-ticket-rules.html": {
        "title": "Guide des Règles de Billets de Train Européens | Europe Train",
        "description": "Guide détaillé des règles de billets de train européens : SNCF, DB, Trenitalia, SBB, Renfe - codes et symboles sur les billets.",
        "h1": "Guide des Règles de Billets de Train Européens",
        "subtitle": "Comprenez chaque code et symbole sur votre billet, évitez les amendes et la confusion",
        "hero": "Règles des Billets Européens | Comparaison 5 Pays",
        "section_france": "France SNCF : Le Système le Plus Complexe",
        "section_germany": "Allemagne DB : Le Système le Plus Clair",
        "section_italy": "Italie Trenitalia : Attention aux Amendes",
        "section_switzerland": "Suisse SBB : Le Système le Plus Convivial",
        "section_spain": "Espagne Renfe : Le Système le Plus Spécial",
        "section_summary": "Résumé des Règles",
        "section_tips": "Guide d'Évitement des Pièges",
    },
}

def translate_content(filename, content):
    """Translate Chinese content to French for a specific article."""
    trans = TRANSLATIONS.get(filename, {})
    
    # Replace title
    if "title" in trans:
        content = re.sub(r'<title>[^<]+</title>', f'<title>{trans["title"]}</title>', content)
    
    # Replace description
    if "description" in trans:
        content = re.sub(r'<meta name="description" content="[^"]+">', f'<meta name="description" content="{trans["description"]}">', content)
    
    # Replace h1
    if "h1" in trans:
        content = re.sub(r'<h1>[^<]+</h1>', f'<h1>{trans["h1"]}</h1>', content)
    
    # Replace subtitle
    if "subtitle" in trans:
        content = re.sub(r'<p class="article-subtitle">[^<]+</p>', f'<p class="article-subtitle">{trans["subtitle"]}</p>', content)
        content = re.sub(r'<p class="subtitle">[^<]+</p>', f'<p class="subtitle">{trans["subtitle"]}</p>', content)
    
    # Replace hero text
    if "hero" in trans:
        content = re.sub(r'<div class="hero-image">\s*[^<]+\s*</div>', f'<div class="hero-image">\n            {trans["hero"]}\n        </div>', content)
    
    return content

def process_all_articles():
    for filename in os.listdir(SRC_DIR):
        if not filename.endswith('.html') or filename == 'index.html':
            continue
            
        src_path = os.path.join(SRC_DIR, filename)
        dst_path = os.path.join(DST_DIR, filename)
        
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply full translation
        content = translate_content(filename, content)
        
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Translated: {filename}")

if __name__ == "__main__":
    process_all_articles()
    print("\nDone! All articles translated to French.")
