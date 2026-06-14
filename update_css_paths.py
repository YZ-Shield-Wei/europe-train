#!/usr/bin/env python3
"""
统一所有 HTML 文件的 CSS 路径为绝对路径 /css/
"""

import os
import re
import glob

def update_css_paths(filepath):
    """更新单个文件的 CSS 路径"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 记录原始内容是否有变化
    original = content
    
    # 替换各种 CSS 路径为绝对路径
    # ../../css/ -> /css/
    content = re.sub(r'\.\./\.\./css/', '/css/', content)
    # ../css/ -> /css/
    content = re.sub(r'\.\./css/', '/css/', content)
    # css/ (相对根目录) -> /css/
    content = re.sub(r'href="css/', 'href="/css/', content)
    # ../../../../css/ -> /css/
    content = re.sub(r'\.\./\.\./\.\./\.\./css/', '/css/', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """主函数"""
    print("🚀 开始统一 CSS 路径...")
    
    # 查找所有 HTML 文件
    html_files = []
    for pattern in ['*.html', '*/*.html', '*/*/*.html']:
        html_files.extend(glob.glob(pattern))
    
    # 排除不需要更新的文件
    exclude_patterns = ['.git', 'disruption/', 'components/']
    html_files = [f for f in html_files if not any(ex in f for ex in exclude_patterns)]
    
    updated = 0
    for filepath in sorted(html_files):
        if update_css_paths(filepath):
            updated += 1
            print(f"✅ 已更新: {filepath}")
    
    print(f"\n📊 更新统计: {updated} 个文件")

if __name__ == "__main__":
    main()
