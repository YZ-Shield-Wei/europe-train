#!/usr/bin/env python3
"""
为 europe-train 多语言站点添加 "View all articles" 链接
"""
import os
import re

BASE_DIR = "/root/.openclaw/workspace/europe-train"

# 各语言的 "View all articles" 翻译
VIEW_ALL_LINKS = {
    'de': '<a href="/de/articles/" style="display: inline-block; background: var(--primary); color: white; padding: 12px 32px; border-radius: 50px; text-decoration: none; font-weight: 600; transition: background 0.2s;">Alle Artikel anzeigen →</a>',
    'fr': '<a href="/fr/articles/" style="display: inline-block; background: var(--primary); color: white; padding: 12px 32px; border-radius: 50px; text-decoration: none; font-weight: 600; transition: background 0.2s;">Voir tous les articles →</a>',
    'es': '<a href="/es/articles/" style="display: inline-block; background: var(--primary); color: white; padding: 12px 32px; border-radius: 50px; text-decoration: none; font-weight: 600; transition: background 0.2s;">Ver todos los artículos →</a>',
    'ja': '<a href="/ja/articles/" style="display: inline-block; background: var(--primary); color: white; padding: 12px 32px; border-radius: 50px; text-decoration: none; font-weight: 600; transition: background 0.2s;">すべての記事を見る →</a>',
    'ko': '<a href="/ko/articles/" style="display: inline-block; background: var(--primary); color: white; padding: 12px 32px; border-radius: 50px; text-decoration: none; font-weight: 600; transition: background 0.2s;">모든 기사 보기 →</a>',
    'pt': '<a href="/pt/articles/" style="display: inline-block; background: var(--primary); color: white; padding: 12px 32px; border-radius: 50px; text-decoration: none; font-weight: 600; transition: background 0.2s;">Ver todos os artigos →</a>',
}

def add_view_all_link(lang):
    """为指定语言站点添加 View all articles 链接"""
    index_file = os.path.join(BASE_DIR, lang, 'index.html')
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有链接
    if 'articles/' in content and '→' in content:
        # 查找是否已有 View all 链接
        if re.search(r'href="/' + lang + r'/articles/".*→', content):
            print(f"  {lang}: 已有 View all 链接")
            return True
    
    # 在文章区域结束后添加链接
    # 查找 </div>\n        </div>\n    </section> 后面跟着 <section class="routes"
    pattern = r'(</div>\s*</div>\s*</section>\s*<section class="routes" id="routes">)'
    replacement = r'</div>\n        </div>\n        <div style="text-align: center; margin-top: 32px;">\n            ' + VIEW_ALL_LINKS[lang] + r'\n        </div>\n    </section>\n    <section class="routes" id="routes">'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content == content:
        # 尝试另一种模式
        pattern2 = r'(</div>\s*</div>\s*</section>\s*\n\s*<section class="routes")'
        replacement2 = r'</div>\n        </div>\n        <div style="text-align: center; margin-top: 32px;">\n            ' + VIEW_ALL_LINKS[lang] + r'\n        </div>\n    </section>\n\n    <section class="routes"'
        
        new_content = re.sub(pattern2, replacement2, content)
    
    if new_content != content:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ {lang}: 已添加 View all 链接")
        return True
    else:
        print(f"  ✗ {lang}: 未找到插入位置")
        return False

def main():
    print("=" * 60)
    print("为各语言站点添加 View all articles 链接")
    print("=" * 60)
    
    for lang in VIEW_ALL_LINKS:
        print(f"\n处理: {lang}")
        add_view_all_link(lang)
    
    print("\n" + "=" * 60)
    print("完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
