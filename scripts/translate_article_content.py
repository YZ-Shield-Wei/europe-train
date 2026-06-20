#!/usr/bin/env python3
"""
Translate article content for all languages
Translates headings, paragraphs, and common phrases
"""
import os
import re

BASE_DIR = "/root/.openclaw/workspace/europe-train"
LANGS = ["de", "fr", "es", "ja", "ko", "pt"]

# Common content translations
CONTENT_TRANSLATIONS = {
    "de": {
        "Quick Facts": "Wichtige Informationen",
        "Route Options": "Streckenoptionen",
        "Booking Tips & Money-Saving Strategies": "Buchungstipps & Spartipps",
        "Onboard Experience": "Erlebnis an Bord",
        "What to See Along the Way": "Sehenswertes unterwegs",
        "Station Information": "Bahnhofsinformationen",
        "Sample Timetable & Prices": "Beispiel-Fahrplan & Preise",
        "FAQ": "Häufige Fragen",
        "Fastest journey": "Schnellste Reisezeit",
        "Average journey": "Durchschnittliche Reisezeit",
        "Direct trains": "Direktzüge",
        "Main operators": "Hauptbetreiber",
        "Price range": "Preisspanne",
        "Best booking window": "Beste Buchungszeit",
        "Book Early for Best Prices": "Früh buchen für beste Preise",
        "Split Your Booking": "Buchung aufteilen",
        "Consider Rail Passes": "Rail Pässe in Betracht ziehen",
        "Travel Mid-Week": "Unter der Woche reisen",
        "Is there a direct train": "Gibt es einen Direktzug",
        "What's the cheapest way": "Was ist der günstigste Weg",
        "Can I use a Eurail Pass": "Kann ich einen Eurail Pass verwenden",
        "Note": "Hinweis",
        "Departure": "Abfahrt",
        "Arrival": "Ankunft",
        "Duration": "Dauer",
        "Changes": "Umstiege",
        "Price From": "Preis ab",
    },
    "fr": {
        "Quick Facts": "Points Clés",
        "Route Options": "Options d'Itinéraire",
        "Booking Tips & Money-Saving Strategies": "Conseils de Réservation & Économies",
        "Onboard Experience": "Expérience à Bord",
        "What to See Along the Way": "Que Voir en Route",
        "Station Information": "Informations sur les Gares",
        "Sample Timetable & Prices": "Horaire Exemple & Prix",
        "FAQ": "FAQ",
        "Fastest journey": "Trajet le plus rapide",
        "Average journey": "Trajet moyen",
        "Direct trains": "Trains directs",
        "Main operators": "Opérateurs principaux",
        "Price range": "Gamme de prix",
        "Best booking window": "Meilleure période de réservation",
        "Book Early for Best Prices": "Réserver tôt pour les meilleurs prix",
        "Split Your Booking": "Diviser votre réservation",
        "Consider Rail Passes": "Envisager les Pass Rail",
        "Travel Mid-Week": "Voyager en milieu de semaine",
        "Is there a direct train": "Y a-t-il un train direct",
        "What's the cheapest way": "Quel est le moyen le moins cher",
        "Can I use a Eurail Pass": "Puis-je utiliser un Pass Eurail",
        "Note": "Note",
        "Departure": "Départ",
        "Arrival": "Arrivée",
        "Duration": "Durée",
        "Changes": "Correspondances",
        "Price From": "Prix à partir de",
    },
    "es": {
        "Quick Facts": "Datos Clave",
        "Route Options": "Opciones de Ruta",
        "Booking Tips & Money-Saving Strategies": "Consejos de Reserva & Ahorro",
        "Onboard Experience": "Experiencia a Bordo",
        "What to See Along the Way": "Qué Ver en el Camino",
        "Station Information": "Información de Estaciones",
        "Sample Timetable & Prices": "Horario Ejemplo & Precios",
        "FAQ": "Preguntas Frecuentes",
        "Fastest journey": "Viaje más rápido",
        "Average journey": "Viaje promedio",
        "Direct trains": "Trenes directos",
        "Main operators": "Operadores principales",
        "Price range": "Rango de precios",
        "Best booking window": "Mejor ventana de reserva",
        "Book Early for Best Prices": "Reservar temprano para mejores precios",
        "Split Your Booking": "Dividir su reserva",
        "Consider Rail Passes": "Considerar pases rail",
        "Travel Mid-Week": "Viajar entre semana",
        "Is there a direct train": "¿Hay un tren directo",
        "What's the cheapest way": "¿Cuál es la forma más barata",
        "Can I use a Eurail Pass": "¿Puedo usar un pase Eurail",
        "Note": "Nota",
        "Departure": "Salida",
        "Arrival": "Llegada",
        "Duration": "Duración",
        "Changes": "Transbordos",
        "Price From": "Precio desde",
    },
    "ja": {
        "Quick Facts": "主な情報",
        "Route Options": "ルートオプション",
        "Booking Tips & Money-Saving Strategies": "予約のコツと節約術",
        "Onboard Experience": "車内体験",
        "What to See Along the Way": "途中の見どころ",
        "Station Information": "駅情報",
        "Sample Timetable & Prices": "時刻表例と料金",
        "FAQ": "よくある質問",
        "Fastest journey": "最速所要時間",
        "Average journey": "平均所要時間",
        "Direct trains": "直通列車",
        "Main operators": "主要運行会社",
        "Price range": "価格帯",
        "Best booking window": "最適な予約時期",
        "Book Early for Best Prices": "早期予約でお得に",
        "Split Your Booking": "予約を分割する",
        "Consider Rail Passes": "レールパスを検討",
        "Travel Mid-Week": "平日の旅行",
        "Is there a direct train": "直通列車はありますか",
        "What's the cheapest way": "最も安い方法は",
        "Can I use a Eurail Pass": "Eurailパスは使えますか",
        "Note": "注",
        "Departure": "出発",
        "Arrival": "到着",
        "Duration": "所要時間",
        "Changes": "乗り換え",
        "Price From": "料金（から）",
    },
    "ko": {
        "Quick Facts": "주요 정보",
        "Route Options": "노선 옵션",
        "Booking Tips & Money-Saving Strategies": "예약 팁과 절약 전략",
        "Onboard Experience": "차내 체험",
        "What to See Along the Way": "도중 볼거리",
        "Station Information": "역 정보",
        "Sample Timetable & Prices": "시간표 예시와 가격",
        "FAQ": "자주 묻는 질문",
        "Fastest journey": "최소 소요 시간",
        "Average journey": "평균 소요 시간",
        "Direct trains": "직통 열차",
        "Main operators": "주요 운영사",
        "Price range": "가격 범위",
        "Best booking window": "최적 예약 시기",
        "Book Early for Best Prices": "조기 예약으로 최저가",
        "Split Your Booking": "예약 분할하기",
        "Consider Rail Passes": "레일 패스 고려",
        "Travel Mid-Week": "주중 여행",
        "Is there a direct train": "직통 열차가 있나요",
        "What's the cheapest way": "가장 저렴한 방법은",
        "Can I use a Eurail Pass": "Eurail 패스를 사용할 수 있나요",
        "Note": "참고",
        "Departure": "출발",
        "Arrival": "도착",
        "Duration": "소요 시간",
        "Changes": "환승",
        "Price From": "가격（부터）",
    },
    "pt": {
        "Quick Facts": "Informações Principais",
        "Route Options": "Opções de Rota",
        "Booking Tips & Money-Saving Strategies": "Dicas de Reserva & Poupança",
        "Onboard Experience": "Experiência a Bordo",
        "What to See Along the Way": "O que Ver pelo Caminho",
        "Station Information": "Informações das Estações",
        "Sample Timetable & Prices": "Horário Exemplo & Preços",
        "FAQ": "Perguntas Frequentes",
        "Fastest journey": "Viagem mais rápida",
        "Average journey": "Viagem média",
        "Direct trains": "Comboios diretos",
        "Main operators": "Operadores principais",
        "Price range": "Faixa de preços",
        "Best booking window": "Melhor período de reserva",
        "Book Early for Best Prices": "Reservar cedo para melhores preços",
        "Split Your Booking": "Dividir a sua reserva",
        "Consider Rail Passes": "Considerar passes rail",
        "Travel Mid-Week": "Viajar em meio de semana",
        "Is there a direct train": "Há um comboio direto",
        "What's the cheapest way": "Qual é a forma mais barata",
        "Can I use a Eurail Pass": "Posso usar um passe Eurail",
        "Note": "Nota",
        "Departure": "Partida",
        "Arrival": "Chegada",
        "Duration": "Duração",
        "Changes": "Mudanças",
        "Price From": "Preço desde",
    }
}

def translate_content(content, lang):
    """Translate common content elements"""
    translations = CONTENT_TRANSLATIONS.get(lang, {})
    
    for en_text, translated in translations.items():
        # Replace in headings and text
        content = content.replace(en_text, translated)
    
    return content

def translate_article_content(lang, article_file):
    """Translate article content for a language"""
    
    # Read the already-translated file (with navigation)
    lang_path = os.path.join(BASE_DIR, lang, "articles", article_file)
    
    if not os.path.exists(lang_path):
        print(f"⚠️  File not found: {lang_path}")
        return False
    
    with open(lang_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Translate content elements
    content = translate_content(content, lang)
    
    # Write back
    with open(lang_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("Starting article content translation...")
    print()
    
    # Get list of all article files
    articles_dir = os.path.join(BASE_DIR, "articles")
    article_files = [f for f in os.listdir(articles_dir) if f.endswith('.html') and f != 'index.html']
    
    for lang in LANGS:
        print(f"\n=== {lang.upper()} ===")
        success = 0
        
        for article_file in article_files:
            if translate_article_content(lang, article_file):
                success += 1
                print(f"  ✅ {article_file}")
            else:
                print(f"  ❌ {article_file}")
        
        print(f"  {success}/{len(article_files)} articles translated")
    
    print()
    print("=" * 50)
    print("Content translation complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()
