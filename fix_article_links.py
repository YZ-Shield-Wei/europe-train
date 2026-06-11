#!/usr/bin/env python3
"""
修复 europe-train 多语言站点首页文章链接
将 /articles/ 改为 /{lang}/articles/
"""

import os
import re

BASE_DIR = "/root/.openclaw/workspace/europe-train"

# 语言目录和对应的文章链接前缀
LANGS = {
    'de': '/de/articles/',
    'fr': '/fr/articles/',
    'es': '/es/articles/',
    'ja': '/ja/articles/',
    'ko': '/ko/articles/',
    'pt': '/pt/articles/'
}

def fix_index_html(lang_dir, lang_code):
    """修复指定语言的首页文件"""
    index_file = os.path.join(BASE_DIR, lang_code, 'index.html')
    
    if not os.path.exists(index_file):
        print(f"✗ 文件不存在: {index_file}")
        return False
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复文章链接 /articles/ -> /{lang}/articles/
    # 修复图片路径 images/ -> ../images/
    
    original = content
    
    # 修复文章链接
    content = re.sub(r'href="/articles/"', f'href="/{lang_code}/articles/"', content)
    
    # 修复图片路径（如果当前是相对路径）
    # 注意：只修复不在 ../images/ 中的路径
    content = re.sub(r'url\(\'images/', "url('../images/", content)
    content = re.sub(r'url\("images/', 'url("../images/', content)
    
    if content != original:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 已修复: {index_file}")
        return True
    else:
        print(f"- 无需修改: {index_file}")
        return False

def main():
    print("=" * 60)
    print("修复 europe-train 多语言站点首页文章链接")
    print("=" * 60)
    
    fixed_count = 0
    
    for lang_code in LANGS:
        print(f"\n处理语言: {lang_code}")
        if fix_index_html(LANGS[lang_code], lang_code):
            fixed_count += 1
    
    print(f"\n{'=' * 60}")
    print(f"修复完成: {fixed_count} 个文件已修改")
    print("=" * 60)

if __name__ == "__main__":
    main()
