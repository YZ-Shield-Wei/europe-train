#!/usr/bin/env python3
"""
修复 guides/ 页面的混合语言问题
"""

from pathlib import Path

BASE_DIR = Path("/root/.openclaw/workspace/europe-train")

# zh guides 标题翻译
ZH_GUIDES_TITLES = {
    'ticket-buying-guide.html': '欧洲火车票购买指南',
    'rail-pass-guide.html': '欧洲铁路通票指南',
    'popular-routes.html': '欧洲热门火车路线',
    'train-experience-guide.html': '欧洲火车旅行体验指南',
}

def fix_zh_guides():
    """修复中文 guides 页面"""
    print("🚀 修复中文 guides 页面...")
    
    guides_dir = BASE_DIR / 'zh' / 'guides'
    if not guides_dir.exists():
        print("  ✗ guides 目录不存在")
        return
    
    for filename, title in ZH_GUIDES_TITLES.items():
        filepath = guides_dir / filename
        if not filepath.exists():
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找并替换 h1 标题
        import re
        h1_match = re.search(r'<h1>(.*?)</h1>', content)
        if h1_match:
            old_title = h1_match.group(1)
            if old_title != title:
                content = content.replace(f'<h1>{old_title}</h1>', f'<h1>{title}</h1>', 1)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✓ {filename}: '{old_title}' → '{title}'")
    
    print("✅ 中文 guides 页面修复完成")

if __name__ == '__main__':
    fix_zh_guides()
