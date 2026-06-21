#!/usr/bin/env python3
"""
修复核心页面（routes.html等）的混合语言问题 v2
处理国家名已翻译但描述仍是英文的情况
"""

from pathlib import Path

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

# 各语言特定的混合段落修复
MIXED_PARAGRAPHS = {
    'de': {
        "Deutschland's flagship high-speed train at 300km/h across the heart of Deutschland.": "Deutschlands Flaggschiff-Hochgeschwindigkeitszug mit 300 km/h quer durch das Herz Deutschlands.",
        "90 minutes through Tuscany, Italien's most popular high-speed route.": "90 Minuten durch die Toskana, Italiens beliebteste Hochgeschwindigkeitsstrecke.",
        "Spanien's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "Spaniens Hochgeschwindigkeitszug durchquert die Iberische Halbinsel in 2,5 Stunden.",
    },
    'fr': {
        "Allemagne's flagship high-speed train at 300km/h across the heart of Allemagne.": "Le train à grande vitesse phare de l'Allemagne à 300 km/h à travers le cœur de l'Allemagne.",
        "90 minutes through Tuscany, Italie's most popular high-speed route.": "90 minutes à travers la Toscane, l'itinéraire à grande vitesse le plus populaire d'Italie.",
        "Espagne's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "Le train à grande vitesse espagnol traverse la péninsule ibérique en 2,5 heures.",
    },
    'es': {
        "Alemania's flagship high-speed train at 300km/h across the heart of Alemania.": "El tren de alta velocidad insignia de Alemania a 300 km/h a través del corazón de Alemania.",
        "90 minutes through Tuscany, Italia's most popular high-speed route.": "90 minutos a través de la Toscana, la ruta de alta velocidad más popular de Italia.",
        "España's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "El tren de alta velocidad español cruza la península ibérica en 2,5 horas.",
    },
    'ja': {
        "ドイツ's flagship high-speed train at 300km/h across the heart of ドイツ.": "ドイツの旗艦高速列車、時速300kmでドイツの中心部を横断。",
        "90 minutes through Tuscany, イタリア's most popular high-speed route.": "トスカーナを90分で横断、イタリアで最も人気のある高速ルート。",
        "スペイン's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "スペインの高速列車が2.5時間でイベリア半島を横断。",
    },
    'ko': {
        "독일's flagship high-speed train at 300km/h across the heart of 독일.": "독일의 플래그십 고속열차, 시속 300km로 독일의 중심을 가로지르다.",
        "90 minutes through Tuscany, 이탈리아's most popular high-speed route.": "토스카나를 90분 만에, 이탈리아에서 가장 인기 있는 고속 노선.",
        "스페인's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "스페인의 고속열차가 2.5시간 만에 이베리아 반도를 횡단하다.",
    },
    'pt': {
        "Alemanha's flagship high-speed train at 300km/h across the heart of Alemanha.": "O trem de alta velocidade emblemático da Alemanha a 300 km/h através do coração da Alemanha.",
        "90 minutes through Tuscany, Itália's most popular high-speed route.": "90 minutos através da Toscana, a rota de alta velocidade mais popular da Itália.",
        "Espanha's high-speed train crossing the Iberian Peninsula in 2.5 hours.": "O trem de alta velocidade espanhol cruza a Península Ibérica em 2,5 horas.",
    },
}

def fix_mixed_language():
    """修复混合语言"""
    print("🚀 修复 routes.html 混合语言...")
    
    fixed_count = 0
    
    for lang, translations in MIXED_PARAGRAPHS.items():
        filepath = BASE_DIR / lang / 'routes.html'
        if not filepath.exists():
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        for mixed_text, translated in translations.items():
            content = content.replace(mixed_text, translated)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_count += 1
            print(f"  ✓ {lang}/routes.html")
    
    print(f"✅ 修复完成: {fixed_count} 个文件")

if __name__ == '__main__':
    fix_mixed_language()
