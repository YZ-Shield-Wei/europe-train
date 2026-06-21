#!/usr/bin/env python3
"""
修复核心页面（routes.html等）的混合语言问题
"""

from pathlib import Path

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

# routes.html 段落翻译
ROUTES_TRANSLATIONS = {
    'de': {
        "Germany's flagship high-speed train at 300km/h across the heart of Germany.": "Deutschlands Flaggschiff-Hochgeschwindigkeitszug mit 300 km/h quer durch das Herz Deutschlands.",
        "90 minutes through Tuscany, Italy's most popular high-speed route.": "90 Minuten durch die Toskana, Italiens beliebteste Hochgeschwindigkeitsstrecke.",
        "Spain's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "Spaniens Hochgeschwindigkeitszug durchquert die Iberische Halbinsel in 2,5 Stunden.",
    },
    'fr': {
        "Germany's flagship high-speed train at 300km/h across the heart of Germany.": "Le train à grande vitesse phare de l'Allemagne à 300 km/h à travers le cœur de l'Allemagne.",
        "90 minutes through Tuscany, Italy's most popular high-speed route.": "90 minutes à travers la Toscane, l'itinéraire à grande vitesse le plus populaire d'Italie.",
        "Spain's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "Le train à grande vitesse espagnol traverse la péninsule ibérique en 2,5 heures.",
    },
    'es': {
        "Germany's flagship high-speed train at 300km/h across the heart of Germany.": "El tren de alta velocidad insignia de Alemania a 300 km/h a través del corazón de Alemania.",
        "90 minutes through Tuscany, Italy's most popular high-speed route.": "90 minutos a través de la Toscana, la ruta de alta velocidad más popular de Italia.",
        "Spain's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "El tren de alta velocidad español cruza la península ibérica en 2,5 horas.",
    },
    'ja': {
        "Germany's flagship high-speed train at 300km/h across the heart of Germany.": "ドイツの旗艦高速列車、時速300kmでドイツの中心部を横断。",
        "90 minutes through Tuscany, Italy's most popular high-speed route.": "トスカーナを90分で横断、イタリアで最も人気のある高速ルート。",
        "Spain's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "スペインの高速列車が2.5時間でイベリア半島を横断。",
    },
    'ko': {
        "Germany's flagship high-speed train at 300km/h across the heart of Germany.": "독일의 플래그십 고속열차, 시속 300km로 독일의 중심을 가로지르다.",
        "90 minutes through Tuscany, Italy's most popular high-speed route.": "토스카나를 90분 만에, 이탈리아에서 가장 인기 있는 고속 노선.",
        "Spain's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "스페인의 고속열차가 2.5시간 만에 이베리아 반도를 횡단하다.",
    },
    'pt': {
        "Germany's flagship high-speed train at 300km/h across the heart of Germany.": "O trem de alta velocidade emblemático da Alemanha a 300 km/h através do coração da Alemanha.",
        "90 minutes through Tuscany, Italy's most popular high-speed route.": "90 minutos através da Toscana, a rota de alta velocidade mais popular da Itália.",
        "Spain's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "O trem de alta velocidade espanhol cruza a Península Ibérica em 2,5 horas.",
    },
    'it': {
        "Germany's flagship high-speed train at 300km/h across the heart of Germany.": "Il treno ad alta velocità di punta della Germania a 300 km/h attraverso il cuore della Germania.",
        "90 minutes through Tuscany, Italy's most popular high-speed route.": "90 minuti attraverso la Toscana, l'itinerario ad alta velocità più popolare d'Italia.",
        "Spain's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "Il treno ad alta velocità spagnolo attraversa la penisola iberica in 2,5 ore.",
    },
    'zh': {
        "Germany's flagship high-speed train at 300km/h across the heart of Germany.": "德国旗舰高速列车，以300公里/小时穿越德国心脏地带。",
        "90 minutes through Tuscany, Italy's most popular high-speed route.": "90分钟穿越托斯卡纳，意大利最受欢迎的高速路线。",
        "Spain's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "西班牙高速列车2.5小时穿越伊比利亚半岛。",
    }
}

def fix_routes_mixed_language():
    """修复 routes.html 的混合语言"""
    print("🚀 修复 routes.html 混合语言...")
    
    fixed_count = 0
    
    for lang, translations in ROUTES_TRANSLATIONS.items():
        filepath = BASE_DIR / lang / 'routes.html'
        if not filepath.exists():
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        for en_text, translated in translations.items():
            content = content.replace(en_text, translated)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_count += 1
            print(f"  ✓ {lang}/routes.html")
    
    print(f"✅ 修复完成: {fixed_count} 个文件")

if __name__ == '__main__':
    fix_routes_mixed_language()
