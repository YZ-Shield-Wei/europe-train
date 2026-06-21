#!/usr/bin/env python3
"""
修复所有页面的语言切换器，添加 it 链接
"""

import re
from pathlib import Path

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")
LANGUAGES = ['en', 'zh', 'de', 'fr', 'es', 'ja', 'ko', 'pt', 'it']

def fix_lang_switcher():
    """修复语言切换器"""
    print("🚀 修复语言切换器...")
    
    fixed_count = 0
    
    for lang in LANGUAGES:
        lang_dir = BASE_DIR / lang
        if not lang_dir.exists():
            continue
        
        for html_file in lang_dir.rglob('*.html'):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 查找语言切换器部分
            # 匹配格式：<div class="lang-switcher">...</div>
            pattern = r'(<div class="lang-switcher">)(.*?)(</div>)'
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                # 生成新的语言切换器
                lang_links = []
                for l in LANGUAGES:
                    href = f"/{l}/" if l != "en" else "/"
                    active = ' class="active"' if l == lang else ""
                    
                    # 语言显示名称
                    names = {
                        'en': 'EN', 'zh': '中文', 'de': 'DE', 'fr': 'FR',
                        'es': 'ES', 'ja': 'JP', 'ko': 'KR', 'pt': 'PT', 'it': 'IT'
                    }
                    name = names.get(l, l.upper())
                    
                    lang_links.append(f'                <a href="{href}"{active}>{name}</a>')
                
                new_switcher = f'<div class="lang-switcher">\n' + '\n'.join(lang_links) + '\n            </div>'
                
                # 替换旧的语言切换器
                content = content[:match.start()] + new_switcher + content[match.end():]
            
            if content != original:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
    
    print(f"✅ 修复完成: {fixed_count} 个文件")

if __name__ == '__main__':
    fix_lang_switcher()
