#!/usr/bin/env python3
"""
完善所有页面的 alternate hreflang 标签
为每个页面添加所有 8 种语言的替代版本链接
"""

import os
import re
import glob

# 语言配置
LANG_CONFIG = {
    'en': {'hreflang': 'en', 'path': '/en/'},
    'zh': {'hreflang': 'zh-CN', 'path': '/zh/'},
    'de': {'hreflang': 'de', 'path': '/de/'},
    'fr': {'hreflang': 'fr', 'path': '/fr/'},
    'es': {'hreflang': 'es', 'path': '/es/'},
    'ja': {'hreflang': 'ja', 'path': '/ja/'},
    'ko': {'hreflang': 'ko', 'path': '/ko/'},
    'pt': {'hreflang': 'pt', 'path': '/pt/'},
}

def get_page_path(filepath):
    """获取页面相对路径"""
    # 移除 .html 后缀
    path = filepath.replace('.html', '')
    # 移除开头的 ./
    path = path.lstrip('./')
    return path

def get_alternate_urls(filepath):
    """生成所有语言的替代 URL"""
    # 获取当前文件的路径部分
    # 例如: articles/index.html -> articles/index
    # 或: en/articles/index.html -> articles/index
    
    path = get_page_path(filepath)
    
    # 检测当前语言
    current_lang = 'en'  # 默认英文
    for lang in ['zh', 'de', 'fr', 'es', 'ja', 'ko', 'pt']:
        if path.startswith(f'{lang}/'):
            current_lang = lang
            # 移除语言前缀获取内容路径
            content_path = path[len(lang)+1:]
            break
    else:
        # 根目录英文页面
        content_path = path
    
    # 生成所有语言的 URL
    alternates = []
    
    # 英文版本
    if content_path:
        en_url = f"https://www.europe-train.com/en/{content_path}"
    else:
        en_url = "https://www.europe-train.com/"
    alternates.append(('en', en_url))
    
    # 中文版本
    if content_path:
        zh_url = f"https://www.europe-train.com/zh/{content_path}"
    else:
        zh_url = "https://www.europe-train.com/zh/"
    alternates.append(('zh-CN', zh_url))
    
    # 其他语言
    for lang in ['de', 'fr', 'es', 'ja', 'ko', 'pt']:
        if content_path:
            url = f"https://www.europe-train.com/{lang}/{content_path}"
        else:
            url = f"https://www.europe-train.com/{lang}/"
        alternates.append((LANG_CONFIG[lang]['hreflang'], url))
    
    return alternates

def generate_alternate_tags(alternates):
    """生成 alternate hreflang HTML 标签"""
    tags = []
    for hreflang, url in alternates:
        tags.append(f'    <link rel="alternate" hreflang="{hreflang}" href="{url}">')
    return '\n'.join(tags)

def update_alternate_tags(filepath):
    """更新单个文件的 alternate 标签"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有 alternate 标签
    if 'rel="alternate"' not in content:
        return False  # 没有现有标签，跳过
    
    # 获取所有语言的替代 URL
    alternates = get_alternate_urls(filepath)
    
    # 生成新的标签
    new_tags = generate_alternate_tags(alternates)
    
    # 替换现有的 alternate 标签块
    # 匹配所有 alternate 标签行
    pattern = r'\s*<link rel="alternate"[^>]*>\s*'
    
    # 找到所有匹配并替换
    existing_tags = re.findall(pattern, content)
    if existing_tags:
        # 替换第一个出现的标签块
        first_tag = existing_tags[0]
        content = content.replace(first_tag, '\n' + new_tags + '\n', 1)
        
        # 移除其他现有的 alternate 标签
        for tag in existing_tags[1:]:
            content = content.replace(tag, '\n')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函数"""
    print("🚀 开始完善 alternate hreflang 标签...")
    
    # 查找所有 HTML 文件
    html_files = []
    for pattern in ['*.html', '*/*.html', '*/*/*.html']:
        html_files.extend(glob.glob(pattern))
    
    # 排除不需要更新的文件
    exclude_patterns = ['.git', 'disruption/', 'components/', 'templates/']
    html_files = [f for f in html_files if not any(ex in f for ex in exclude_patterns)]
    
    updated = 0
    skipped = 0
    
    for filepath in sorted(html_files):
        if update_alternate_tags(filepath):
            updated += 1
            print(f"✅ 已更新: {filepath}")
        else:
            skipped += 1
    
    print(f"\n📊 更新统计: {updated} 个文件更新, {skipped} 个文件跳过")

if __name__ == "__main__":
    main()
