#!/usr/bin/env python3
"""
彻底修复 europe-train 多语言站点所有中文内容
"""
import os
import re

BASE_DIR = "/root/.openclaw/workspace/europe-train"

# 各语言需要替换的中文内容映射
REPLACEMENTS = {
    'de': {
        '欧洲火车旅行指南': 'Europäische Bahn-Reiseguides',
        '路线、车票、通票': 'Routen, Tickets, Pässe',
        '巴黎到洛桑': 'Paris → Lausanne',
        '欧洲各国火': 'Europäische Bahn',
        '使用规则完全指南': 'Regeln Vollständiger Guide',
        '看懂': 'Verstehen',
        '上的每一个代码和符号，避免罚款和尴尬': 'jeden Code und Symbol, Strafen vermeiden',
        '国对比': 'Länder-Vergleich',
        '红线': 'Rote Linie',
    },
    'fr': {
        '欧洲火车旅行指南': 'Guides de voyage en train en Europe',
        '路线、车票、通票': 'Itinéraires, billets, passes',
        '巴黎到洛桑': 'Paris → Lausanne',
        '欧洲各国火': 'Règles européennes',
        '使用规则完全指南': 'Guide complet des règles',
        '看懂': 'Comprendre',
        '上的每一个代码和符号，避免罚款和尴尬': 'chaque code et symbole, éviter les amendes',
        '国对比': 'Comparaison pays',
        '红线': 'Ligne Rouge',
    },
    'es': {
        '欧洲火车旅行指南': 'Guías de viaje en tren por Europa',
        '路线、车票、通票': 'Rutas, billetes, pases',
        '巴黎到洛桑': 'París → Lausana',
        '欧洲各国火': 'Reglas europeas',
        '使用规则完全指南': 'Guía completa de reglas',
        '看懂': 'Entender',
        '上的每一个代码和符号，避免罚款和尴尬': 'cada código y símbolo, evitar multas',
        '国对比': 'Comparación países',
        '红线': 'Línea Roja',
    },
    'ja': {
        '欧洲火车旅行指南': 'ヨーロッパ鉄道旅行ガイド',
        '路线、车票、通票': 'ルート、切符、パス',
        '巴黎到洛桑': 'パリ → ローザンヌ',
        '欧洲各国火': 'ヨーロッパ各国',
        '使用规则完全指南': '使用規則完全ガイド',
        '看懂': '理解する',
        '上的每一个代码和符号，避免罚款和尴尬': '上のコードと記号、罰金を回避',
        '国对比': 'カ国比較',
        '红线': 'レッドライン',
    },
    'ko': {
        '欧洲火车旅行指南': '유럽 기차 여행 가이드',
        '路线、车票、通票': '노선, 티켓, 패스',
        '巴黎到洛桑': '파리 → 로잔',
        '欧洲各国火': '유럽 각국',
        '使用规则完全指南': '사용 규칙 완벽 가이드',
        '看懂': '이해하기',
        '上的每一个代码和符号，避免罚款和尴尬': '위의 코드와 기호, 벌금 회피',
        '国对比': '개국 비교',
        '红线': '레드라인',
    },
    'pt': {
        '欧洲火车旅行指南': 'Guias de viagem de trem na Europa',
        '路线、车票、通票': 'Rotas, bilhetes, passes',
        '巴黎到洛桑': 'Paris → Lausanne',
        '欧洲各国火': 'Regras europeias',
        '使用规则完全指南': 'Guia completo das regras',
        '看懂': 'Entender',
        '上的每一个代码和符号，避免罚款和尴尬': 'cada código e símbolo, evitar multas',
        '国对比': 'Comparação países',
        '红线': 'Linha Vermelha',
    }
}

def fix_all_chinese(lang):
    """修复指定语言的所有中文内容"""
    index_file = os.path.join(BASE_DIR, lang, 'index.html')
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    replacements = REPLACEMENTS.get(lang, {})
    for cn, translated in replacements.items():
        content = content.replace(cn, translated)
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ {lang} 修复完成")

def main():
    print("=" * 60)
    print("彻底修复所有语言站点的中文内容")
    print("=" * 60)
    
    for lang in REPLACEMENTS:
        fix_all_chinese(lang)
    
    print("\n" + "=" * 60)
    print("修复完成，重新检查...")
    
    # 重新检查
    for lang in REPLACEMENTS:
        index_file = os.path.join(BASE_DIR, lang, 'index.html')
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        chinese_chars = re.findall(r'[\u4e00-\u9fff]+', content)
        if chinese_chars:
            print(f'{lang}: 仍有 {len(chinese_chars)} 处中文: {chinese_chars[:5]}')
        else:
            print(f'{lang}: 无中文内容 ✅')
    
    print("=" * 60)

if __name__ == "__main__":
    main()
