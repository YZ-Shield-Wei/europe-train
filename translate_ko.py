#!/usr/bin/env python3
"""
翻译 europe-train.com 韩语文章中的英文段落
使用 Kimi API 进行翻译
"""
import os
import re
import glob
import json
import time
from pathlib import Path

# 专有名词列表 - 不翻译
PROPER_NOUNS = [
    'TGV', 'ICE', 'DB', 'SNCF', 'AVE', 'Frecciarossa', 'Eurostar',
    'Lyria', 'Glacier Express', 'Bernina Express', 'GoldenPass Line',
    'Trainline', 'Omio', 'Rail Planner', 'Paris', 'Rome', 'Berlin',
    'Munich', 'Zurich', 'Lausanne', 'London', 'Milan', 'Madrid',
    'Barcelona', 'Frankfurt', 'Gare du Nord', 'St Pancras', 'Hauptbahnhof',
    'Duplex', 'Red Arrow', 'Ferrari', 'Alps', 'English Channel',
    'City of Light', 'Eternal City', 'Iberian', 'EU Regulation 1371/2007',
    'Europe Train', 'ET', 'TGV Lyria', 'Swiss', 'France', 'Germany',
    'Italy', 'Spain', 'Europe', 'European', 'Route Guide', 'Cost Comparison',
    'Train Experience', 'Scenic Trains', 'Booking Guide', 'Station Guide',
    'Ticket Rules', 'Compensation', 'App Comparison', 'France', 'Germany',
    'Italy', 'Spain', 'EN', '中文', 'DE', 'FR', 'ES', 'JP', 'KR', 'PT', 'IT',
    'Eurail', 'Interrail', 'BahnCard', 'Sparpreis', 'PREM\'S', 'Super Economy',
    'Swiss Travel Pass', 'Mont Cenis', 'Mont d\'Ambin', 'Duomo', 'Galleria Vittorio',
    'Île-de-France', 'Jura Mountains', 'Lake Neuchâtel', 'Burgundy', 'Le Marais',
    'Gare de Lyon', 'Milano Centrale', 'Roma Termini', 'Torino Porta Susa',
    'Zermatt', 'St. Moritz', 'Chur', 'Tirano', 'Lucerne', 'Montreux', 'Interlaken',
    'Pontarlier', 'Lake Geneva', 'Orly', 'Dijon', 'Besançon', 'Bahnhofstrasse',
    'SNCF Connect', 'DB Navigator'
]

def is_english_text(text):
    """判断文本是否为英文（包含足够比例的ASCII字符）"""
    if not text or not text.strip():
        return False
    
    # 去除HTML标签
    clean = re.sub(r'<[^>]+>', '', text).strip()
    if not clean:
        return False
    
    # 如果包含韩文字符，认为是韩语
    korean_chars = re.findall(r'[\uac00-\ud7af\u1100-\u11ff\u3130-\u318f]', clean)
    if korean_chars and len(korean_chars) > len(clean) * 0.1:
        return False
    
    # 检查是否主要是英文
    ascii_chars = [c for c in clean if c.isascii() and c.isalpha()]
    if len(ascii_chars) > len(clean) * 0.5:
        return True
    
    return False

def translate_with_kimi(text):
    """使用 Kimi API 翻译文本"""
    import requests
    
    api_key = os.environ.get('KIMI_API_KEY', '')
    if not api_key:
        print("警告: 未设置 KIMI_API_KEY 环境变量")
        return None
    
    # 保护专有名词
    protected_text = text
    placeholders = {}
    placeholder_idx = 0
    
    for noun in sorted(PROPER_NOUNS, key=len, reverse=True):
        if noun in protected_text:
            placeholder = f"__PLACEHOLDER_{placeholder_idx}__"
            placeholders[placeholder] = noun
            protected_text = protected_text.replace(noun, placeholder)
            placeholder_idx += 1
    
    prompt = f"""请将以下英文翻译成自然流畅的韩语。保持原有的HTML标签不变。只翻译文本内容，不要添加额外解释。

原文：{protected_text}

韩语翻译："""
    
    try:
        response = requests.post(
            'https://api.moonshot.cn/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'moonshot-v1-8k',
                'messages': [
                    {'role': 'system', 'content': 'You are a professional translator. Translate English to Korean naturally and accurately. Preserve HTML tags and proper nouns. Do not add explanations.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.3
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            translated = result['choices'][0]['message']['content'].strip()
            
            # 恢复专有名词
            for placeholder, noun in placeholders.items():
                translated = translated.replace(placeholder, noun)
            
            return translated
        else:
            print(f"API 错误: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"翻译错误: {e}")
        return None

def translate_paragraph(text):
    """翻译段落，使用本地规则或API"""
    # 先尝试使用简单的本地翻译规则（常见短语）
    local_translations = {
        'Route Guide': '노선 가이드',
        'Cost Comparison': '비용 비교',
        'Train Experience': '열차 체험',
        'Scenic Trains': '경관 열차',
        'Booking Guide': '예약 가이드',
        'Station Guide': '역 가이드',
        'Ticket Rules': '승차권 규정',
        'Compensation': '보상',
        'App Comparison': '앱 비교',
        'France': '프랑스',
        'Germany': '독일',
        'Italy': '이탈리아',
        'Spain': '스페인',
        'National railway websites, early bird tickets, money-saving tips': '국철 웹사이트, 얼리버드 티켓, 비용 절약 팁',
        'Reservation rules, fees, and tips': '예약 규칙, 수수료 및 팁',
        'Seats, dining car, luggage, WiFi': '좌석, 다이닝카, 수하물, WiFi',
        '20 classic European train routes': '20개 클래식 유럽 열차 노선',
        'Scenic train booking tips': '경관 열차 예약 팁',
        'Eurail vs Swiss Travel Pass comparison': 'Eurail vs Swiss Travel Pass 비교',
        'TGV seat selection and booking': 'TGV 좌석 선택 및 예약',
        'Eurail Pass reservation rules explained': 'Eurail Pass 예약 규칙 설명',
        'German Rail Pass explained': 'German Rail Pass 설명',
        'France high-speed rail comparison': '프랑스 고속철 비교',
        'Germany high-speed rail experience': '독일 고속철 체험',
        'Italy high-speed rail comparison': '이탈리아 고속철 비교',
        'France high-speed rail experience': '프랑스 고속철 체험',
        'SNCF Connect user guide': 'SNCF Connect 사용 가이드',
        'DB Navigator user guide': 'DB Navigator 사용 가이드',
        'Swiss Travel Pass explained': 'Swiss Travel Pass 설명',
        'Station facilities, navigation, transfers': '역 시설, 안내, 환승',
        'Compensation standards and application process': '보상 기준 및 신청 절차',
        'National rail websites, early-bird tickets, savings tips': '국철 웹사이트, 얼리버드 티켓, 절약 팁',
    }
    
    # 检查是否是纯专有名词或已知短语
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    if clean_text in local_translations:
        # 替换文本内容但保留HTML标签
        for key, value in local_translations.items():
            if key in text:
                text = text.replace(key, value)
        return text
    
    # 使用API翻译
    return translate_with_kimi(text)

def process_html_file(filepath):
    """处理单个HTML文件，翻译英文段落"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 找到所有<p>标签内容
    p_pattern = re.compile(r'<p>(.*?)</p>', re.DOTALL)
    
    translated_count = 0
    
    for match in p_pattern.finditer(content):
        p_content = match.group(1)
        if is_english_text(p_content):
            translated = translate_paragraph(p_content)
            if translated and translated != p_content:
                # 替换原文
                old_p = match.group(0)
                new_p = f'<p>{translated}</p>'
                content = content.replace(old_p, new_p, 1)
                translated_count += 1
                print(f"  翻译: {p_content[:60]}...")
                print(f"  → {translated[:60]}...")
                time.sleep(0.5)  # 避免API速率限制
    
    # 保存文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ 已保存: {os.path.basename(filepath)}")
    
    return translated_count

def main():
    articles_dir = '/root/.openclaw/workspace/europe-train/ko/articles/'
    html_files = sorted(glob.glob(os.path.join(articles_dir, '*.html')))
    
    print(f"找到 {len(html_files)} 个HTML文件\n")
    
    total_files = 0
    total_paragraphs = 0
    file_stats = {}
    
    for filepath in html_files:
        filename = os.path.basename(filepath)
        print(f"\n=== 处理: {filename} ===")
        
        count = process_html_file(filepath)
        
        if count > 0:
            total_files += 1
            total_paragraphs += count
            file_stats[filename] = count
    
    print(f"\n\n{'='*50}")
    print(f"翻译完成总结:")
    print(f"{'='*50}")
    print(f"- 翻译文件数: {total_files}")
    print(f"- 翻译段落总数: {total_paragraphs}")
    print(f"\n各文件翻译详情:")
    for filename, count in file_stats.items():
        print(f"  - {filename}: {count} 个段落")

if __name__ == '__main__':
    main()
