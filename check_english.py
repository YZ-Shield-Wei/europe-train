#!/usr/bin/env python3
"""
翻译 europe-train.com 韩语文章中的英文段落
"""
import os
import re
import glob
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
    'Italy', 'Spain', 'EN', '中文', 'DE', 'FR', 'ES', 'JP', 'KR', 'PT', 'IT'
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

def translate_text(text):
    """简单的翻译映射（常见短语）"""
    # 这里我们使用一个简化的翻译字典，实际应该用翻译API
    # 但由于没有API，我们会标记需要翻译的文本
    return f"[TRANSLATE: {text}]"

def process_html_file(filepath):
    """处理单个HTML文件，找出英文段落"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到所有<p>标签内容
    p_pattern = re.compile(r'<p>(.*?)</p>', re.DOTALL)
    
    english_paragraphs = []
    
    for match in p_pattern.finditer(content):
        p_content = match.group(1)
        if is_english_text(p_content):
            english_paragraphs.append({
                'original': match.group(0),
                'content': p_content
            })
    
    return english_paragraphs

def main():
    articles_dir = '/root/.openclaw/workspace/europe-train/ko/articles/'
    html_files = sorted(glob.glob(os.path.join(articles_dir, '*.html')))
    
    print(f"找到 {len(html_files)} 个HTML文件\n")
    
    total_files = 0
    total_paragraphs = 0
    
    for filepath in html_files:
        filename = os.path.basename(filepath)
        paragraphs = process_html_file(filepath)
        
        if paragraphs:
            total_files += 1
            total_paragraphs += len(paragraphs)
            print(f"\n=== {filename} ===")
            for i, p in enumerate(paragraphs, 1):
                print(f"  [{i}] {p['content'][:100]}...")
    
    print(f"\n\n总结:")
    print(f"- 涉及文件数: {total_files}")
    print(f"- 英文段落总数: {total_paragraphs}")

if __name__ == '__main__':
    main()
