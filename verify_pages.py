#!/usr/bin/env python3
"""
验证各语言站点的子页面是否正确创建
"""

import os

LANGUAGES = ['de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']
PAGES = ['routes.html', 'tickets.html', 'passes.html', 'live-status.html']
BASE_DIR = '/root/.openclaw/workspace/europe-train'

def verify_pages():
    print("=" * 60)
    print("验证子页面创建结果")
    print("=" * 60)
    
    all_ok = True
    for lang in LANGUAGES:
        print(f"\n🌍 {lang.upper()} 站点:")
        for page in PAGES:
            path = os.path.join(BASE_DIR, lang, page)
            if os.path.exists(path):
                size = os.path.getsize(path)
                # 检查 html lang 属性
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read(500)
                    lang_match = f'lang="{lang}"' in content or (lang == 'zh' and 'lang="zh-CN"' in content)
                
                status = "✅" if lang_match else "⚠️"
                print(f"  {status} {page} ({size} bytes, lang属性正确: {lang_match})")
            else:
                print(f"  ❌ {page} - 不存在!")
                all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ 所有页面验证通过!")
    else:
        print("❌ 部分页面缺失!")
    print("=" * 60)
    
    return all_ok

if __name__ == '__main__':
    success = verify_pages()
    exit(0 if success else 1)
