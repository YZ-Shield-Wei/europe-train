import os
import re

BASE_DIR = "/root/.openclaw/workspace/europe-train"

# Google Analytics 代码块
ga_code = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-JWY9K5ZRSF"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-JWY9K5ZRSF');</script>'''

def get_lang_switcher(current_lang, article_name):
    """生成语言切换器HTML"""
    langs = [
        ('en', 'EN'), ('de', 'DE'), ('fr', 'FR'), ('es', 'ES'),
        ('it', 'IT'), ('ja', 'JP'), ('ko', 'KR'), ('pt', 'PT'), ('zh', '中文')
    ]
    
    html = '<div class="lang-switcher">\n'
    for lang_code, label in langs:
        if lang_code == current_lang:
            html += f'                <a href="/{lang_code}/articles/{article_name}" class="active">{label}</a>\n'
        else:
            html += f'                <a href="/{lang_code}/articles/{article_name}">{label}</a>\n'
    html += '            </div>'
    return html

def get_hreflangs(current_lang, article_name):
    """生成 hreflang 链接"""
    langs = ['en', 'zh-CN', 'de', 'fr', 'es', 'ja', 'ko', 'pt', 'it']
    html = ''
    for lang in langs:
        if lang == 'zh-CN':
            path = '/zh/'
        elif lang == 'it':
            path = '/it/'
        else:
            path = f'/{lang}/'
        html += f'    <link rel="alternate" hreflang="{lang}" href="https://www.europe-train.com{path}articles/{article_name}">\n'
    return html

def fix_file(filepath, lang):
    """修复单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    article_name = os.path.basename(filepath)
    
    # 1. 添加 Google Analytics（如果缺少）
    if 'G-JWY9K5ZRSF' not in html:
        html = html.replace('</head>', f'{ga_code}\n</head>')
    
    # 2. 添加 canonical（如果缺少）
    if 'rel="canonical"' not in html:
        canonical = f'<link rel="canonical" href="https://www.europe-train.com/{lang}/articles/{article_name}">'
        html = html.replace('</head>', f'{canonical}\n</head>')
    
    # 3. 添加 hreflang（如果缺少）- 检查是否有任何 hreflang
    has_hreflang = 'hreflang="en"' in html or 'hreflang="zh"' in html or 'hreflang="zh-CN"' in html
    if not has_hreflang:
        hreflangs = get_hreflangs(lang, article_name)
        html = html.replace('</head>', f'{hreflangs}</head>')
    
    # 4. 添加 lang-switcher（如果缺少）
    if 'lang-switcher' not in html:
        lang_switcher = get_lang_switcher(lang, filepath)
        html = html.replace('</header>', f'{lang_switcher}\n    </header>')
    
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

# 修复所有文件
fixed_count = 0
for lang in ['en', 'de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']:
    articles_dir = f"{BASE_DIR}/{lang}/articles"
    if not os.path.exists(articles_dir):
        continue
    
    for filename in os.listdir(articles_dir):
        if not filename.endswith('.html'):
            continue
        filepath = os.path.join(articles_dir, filename)
        if fix_file(filepath, lang):
            fixed_count += 1
            print(f"✅ 修复: {lang}/articles/{filename}")

print(f"\n✅ 共修复 {fixed_count} 个文件")
