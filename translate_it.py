#!/usr/bin/env python3
"""
翻译 europe-train.com 意大利语文章中的英文段落。
保持HTML结构不变，只替换<p>标签内的英文文本。
"""

import os
import re
import glob
from pathlib import Path

# 专有名词列表（不翻译）
PROPER_NOUNS = [
    'TGV', 'ICE', 'DB', 'SNCF', 'SBB', 'AVE', 'Frecciarossa', 'italo',
    'Eurail', 'Interrail', 'BahnCard', 'Renfe', 'Eurostar', 'Lyria',
    'Glacier Express', 'Bernina Express', 'GoldenPass Line',
    'Paris', 'Rome', 'Milan', 'Berlin', 'Munich', 'Zurich', 'Lyon',
    'Gare de Lyon', 'Milano Centrale', 'Roma Termini', 'Torino Porta Susa',
    'Chur', 'St. Moritz', 'Tirano', 'Lucerne', 'Montreux', 'Interlaken',
    'Neuchâtel', 'Bern', 'Solothurn', 'Dijon', 'Burgundy', 'Jura',
    'Le Marais', 'Île-de-France', 'Swiss Plateau', 'Swiss Travel Pass',
    'German Rail Pass', 'France', 'Germany', 'Italy', 'Spain', 'Switzerland',
    'Europe', 'European', 'EU', 'EC 261/2004',
    'SNCF Connect', 'DB Navigator', 'Trenitalia', 'SBB Mobile',
    'Atocha', 'Hauptbahnhof', 'Termini', 'Centrale',
    'QR', 'WiFi', 'X-ray',
]

# 意大利语常见词（用于检测是否已经是意大利语）
ITALIAN_WORDS = [
    'il', 'la', 'lo', 'i', 'le', 'gli',     # 冠词
    'di', 'a', 'da', 'in', 'con', 'su', 'per', 'tra', 'fra',  # 介词
    'e', 'o', 'ma', 'che', 'come', 'quando',  # 连词
    'è', 'sono', 'ha', 'ho', 'hai', 'hanno',  # 动词
    'questo', 'questa', 'quello', 'quella',   # 指示代词
    'mio', 'tuo', 'suo', 'nostro', 'vostro',  # 物主代词
    'non', 'più', 'meno', 'molto', 'tutto',   # 副词
    'bene', 'male', 'qui', 'là', 'ora', 'poi',
    'guida', 'treno', 'biglietto', 'viaggio', 'stazione',  # 常见名词
    'prezzo', 'tariffa', 'prenotazione', 'posto', 'treno',
    'alta', 'velocità', 'ferrovia', 'nazionale',
]


def is_italian(text: str) -> bool:
    """检测文本是否已经是意大利语。"""
    text_lower = text.lower()
    # 如果包含明显的意大利语单词，认为是意大利语
    italian_score = sum(1 for w in ITALIAN_WORDS if w in text_lower)
    # 如果包含大量意大利语特征（如重音符号）
    if any(c in text for c in 'àèéìòù'):
        italian_score += 2
    # 简单启发式：如果得分>=3，认为是意大利语
    return italian_score >= 3


def is_mostly_english(text: str) -> bool:
    """检测文本是否主要是英文。"""
    # 去除HTML标签
    clean = re.sub(r'<[^>]+>', '', text)
    clean = clean.strip()
    if not clean:
        return False
    # 如果已经是意大利语，跳过
    if is_italian(clean):
        return False
    # 如果包含大量英文常见词
    english_words = ['the', 'and', 'for', 'with', 'you', 'your', 'from', 'to', 'of', 'in', 'on', 'at', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'a', 'an', 'as', 'if', 'when', 'where', 'why', 'how', 'what', 'who', 'which', 'while', 'during', 'before', 'after', 'above', 'below', 'between', 'through', 'into', 'onto', 'upon', 'about', 'against', 'among', 'around', 'behind', 'beyond', 'despite', 'except', 'inside', 'outside', 'until', 'via', 'within', 'without']
    text_lower = clean.lower()
    english_score = sum(1 for w in english_words if f' {w} ' in f' {text_lower} ' or text_lower.startswith(w + ' ') or text_lower.endswith(' ' + w))
    # 如果英文词得分>=3，认为是英文
    return english_score >= 3


def translate_text(text: str) -> str:
    """
    将英文文本翻译成意大利语。
    这是一个简化版本，实际应该调用翻译API。
    这里使用规则-based翻译常见短语。
    """
    # 这是一个占位符函数。由于我们无法调用外部翻译API，
    # 我们将使用一个简单的方法：标记需要翻译的段落，
    # 然后让主agent使用翻译工具处理。
    return f"[TRANSLATE_TO_IT]{text}[/TRANSLATE_TO_IT]"


def process_html_file(filepath: str) -> tuple[int, list[str]]:
    """
    处理单个HTML文件，找出英文段落。
    返回：(英文段落数量, 英文段落列表)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    english_paragraphs = []
    
    # 查找所有<p>标签
    pattern = re.compile(r'(<p[^>]*>)(.*?)(</p>)', re.DOTALL)
    
    for match in pattern.finditer(content):
        open_tag = match.group(1)
        inner = match.group(2)
        close_tag = match.group(3)
        
        # 检查是否主要是英文
        if is_mostly_english(inner):
            english_paragraphs.append({
                'full': match.group(0),
                'open_tag': open_tag,
                'inner': inner,
                'close_tag': close_tag,
            })
    
    return len(english_paragraphs), english_paragraphs


def main():
    articles_dir = Path('/root/.openclaw/workspace/europe-train/it/articles')
    html_files = sorted(articles_dir.glob('*.html'))
    
    total_files = 0
    total_paragraphs = 0
    all_results = []
    
    for filepath in html_files:
        count, paragraphs = process_html_file(str(filepath))
        if count > 0:
            total_files += 1
            total_paragraphs += count
            all_results.append({
                'file': filepath.name,
                'count': count,
                'paragraphs': paragraphs,
            })
    
    # 输出结果
    print(f"总计: {total_files} 个文件包含英文段落")
    print(f"总计: {total_paragraphs} 个英文段落需要翻译")
    print()
    
    for result in all_results:
        print(f"\n=== {result['file']} ({result['count']} 段) ===")
        for i, p in enumerate(result['paragraphs'], 1):
            # 只显示前200字符
            inner_preview = p['inner'][:200].replace('\n', ' ')
            print(f"  [{i}] {inner_preview}...")


if __name__ == '__main__':
    main()
