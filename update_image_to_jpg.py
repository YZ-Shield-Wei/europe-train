#!/usr/bin/env python3
"""
更新 HTML 中的图片引用，将 .svg 占位图替换为 .jpg
"""

import os
import re
import glob

# 需要替换的图片映射
IMAGE_MAP = {
    'delay-compensation.svg': 'delay-compensation.jpg',
    'france-tgv.svg': 'france-tgv.jpg',
    'germany-ice.svg': 'germany-ice.jpg',
    'italy-frecciarossa.svg': 'italy-frecciarossa.jpg',
    'london-paris.svg': 'london-paris.jpg',
    'seat-reservation.svg': 'seat-reservation.jpg',
    'spain-ave.svg': 'spain-ave.jpg',
    'swiss-scenic.svg': 'swiss-scenic.jpg',
    'train-apps.svg': 'train-apps.jpg',
    'train-station.svg': 'train-station.jpg',
}

def update_image_refs(filepath):
    """更新单个文件的图片引用"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 替换图片引用
    for old_img, new_img in IMAGE_MAP.items():
        content = content.replace(old_img, new_img)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """主函数"""
    print("🚀 开始更新图片引用...")
    
    # 查找所有 HTML 文件
    html_files = []
    for pattern in ['*.html', '*/*.html', '*/*/*.html']:
        html_files.extend(glob.glob(pattern))
    
    # 排除不需要更新的文件
    exclude_patterns = ['.git', 'disruption/', 'components/']
    html_files = [f for f in html_files if not any(ex in f for ex in exclude_patterns)]
    
    updated = 0
    for filepath in sorted(html_files):
        if update_image_refs(filepath):
            updated += 1
            print(f"✅ 已更新: {filepath}")
    
    print(f"\n📊 更新统计: {updated} 个文件")

if __name__ == "__main__":
    main()
