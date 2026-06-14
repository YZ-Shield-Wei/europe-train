#!/usr/bin/env python3
"""
批量更新所有页面的导航栏 - 使用模块化组件
替换所有页面中的硬编码导航为统一组件
"""

import os
import re
import glob

# 导航组件映射（语言 -> 组件文件）
NAV_COMPONENTS = {
    'en': 'components/nav-en.html',
    'zh': 'components/nav-zh.html',
    'de': 'components/nav-de.html',
    'fr': 'components/nav-fr.html',
    'es': 'components/nav-es.html',
    'ja': 'components/nav-ja.html',
    'ko': 'components/nav-ko.html',
    'pt': 'components/nav-pt.html',
}

# 默认导航（根目录英文页面）
DEFAULT_NAV = 'components/nav-en.html'

def read_nav_component(path):
    """读取导航组件内容"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def detect_language(filepath):
    """根据文件路径检测语言"""
    if '/zh/' in filepath or filepath.startswith('zh/'):
        return 'zh'
    elif '/de/' in filepath or filepath.startswith('de/'):
        return 'de'
    elif '/fr/' in filepath or filepath.startswith('fr/'):
        return 'fr'
    elif '/es/' in filepath or filepath.startswith('es/'):
        return 'es'
    elif '/ja/' in filepath or filepath.startswith('ja/'):
        return 'ja'
    elif '/ko/' in filepath or filepath.startswith('ko/'):
        return 'ko'
    elif '/pt/' in filepath or filepath.startswith('pt/'):
        return 'pt'
    else:
        return 'en'  # 根目录默认为英文

def update_navigation(filepath, nav_content):
    """更新单个文件的导航栏"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 <header class="header"> 到 </header> 之间的内容
    pattern = r'<header class="header">.*?</header>'
    
    if re.search(pattern, content, re.DOTALL):
        # 替换导航
        new_content = re.sub(pattern, nav_content, content, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    else:
        print(f"  ⚠️  未找到导航栏: {filepath}")
        return False

def main():
    """主函数"""
    print("🚀 开始批量更新导航栏...")
    print("=" * 60)
    
    # 读取所有导航组件
    nav_components = {}
    for lang, path in NAV_COMPONENTS.items():
        if os.path.exists(path):
            nav_components[lang] = read_nav_component(path)
            print(f"✅ 加载导航组件: {path}")
        else:
            print(f"⚠️  导航组件不存在: {path}")
    
    # 查找所有 HTML 文件
    html_files = []
    for pattern in ['*.html', '*/*.html', '*/*/*.html']:
        html_files.extend(glob.glob(pattern))
    
    # 排除不需要更新的文件
    exclude_patterns = [
        '.git',
        'disruption/',
        'components/',
    ]
    
    html_files = [f for f in html_files if not any(ex in f for ex in exclude_patterns)]
    
    print(f"\n📄 找到 {len(html_files)} 个 HTML 文件")
    print("=" * 60)
    
    # 更新统计
    updated = 0
    skipped = 0
    failed = 0
    
    for filepath in sorted(html_files):
        # 检测语言
        lang = detect_language(filepath)
        
        # 获取对应语言的导航组件
        if lang in nav_components:
            nav_content = nav_components[lang]
        else:
            nav_content = nav_components.get('en', '')
        
        # 更新文件
        if update_navigation(filepath, nav_content):
            updated += 1
            print(f"✅ 已更新: {filepath} ({lang})")
        else:
            failed += 1
    
    print("=" * 60)
    print(f"\n📊 更新统计:")
    print(f"   ✅ 成功: {updated}")
    print(f"   ⚠️  失败: {failed}")
    print(f"   📄 总计: {len(html_files)}")
    
    if updated > 0:
        print(f"\n💡 请执行 git add 和 git commit 提交更改")

if __name__ == "__main__":
    main()
