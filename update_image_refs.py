#!/usr/bin/env python3
"""
更新 HTML 中的图片引用，将缺失的 .jpg 替换为 .svg 占位图
"""

import os
import re
import glob

# 需要替换的图片映射
IMAGE_MAP = {
    'delay-compensation.jpg': 'delay-compensation.svg',
    'france-tgv.jpg': 'france-tgv.svg',
    'germany-ice.jpg': 'germany-ice.svg',
    'italy-frecciarossa.jpg': 'italy-frecciarossa.svg',
    'london-paris.jpg': 'london-paris.svg',
    'seat-reservation.jpg': 'seat-reservation.svg',
    'spain-ave.jpg': 'spain-ave.svg',
    'swiss-scenic.jpg': 'swiss-scenic.svg',
    'train-apps.jpg': 'train-apps.svg',
    'train-station.jpg': 'train-station.svg',
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
