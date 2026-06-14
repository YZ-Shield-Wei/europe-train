#!/usr/bin/env python3
"""
为缺失的图片创建占位符 SVG 文件
并更新 HTML 中的图片引用
"""

import os

# 缺失的图片列表
MISSING_IMAGES = [
    'delay-compensation.jpg',
    'france-tgv.jpg',
    'germany-ice.jpg',
    'italy-frecciarossa.jpg',
    'london-paris.jpg',
    'seat-reservation.jpg',
    'spain-ave.jpg',
    'swiss-scenic.jpg',
    'train-apps.jpg',
    'train-station.jpg',
]

# 创建占位 SVG
SVG_TEMPLATE = '''<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="400" fill="#f0f0f0"/>
  <text x="400" y="200" font-family="Arial" font-size="24" fill="#999" text-anchor="middle">
    {title}
  </text>
  <text x="400" y="240" font-family="Arial" font-size="16" fill="#bbb" text-anchor="middle">
    Image Placeholder
  </text>
</svg>'''

def create_placeholder_svg(filename, title):
    """创建占位 SVG 文件"""
    svg_content = SVG_TEMPLATE.format(title=title)
    filepath = f'images/{filename.replace(".jpg", ".svg")}'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"✅ 创建占位图: {filepath}")

def main():
    """主函数"""
    print("🚀 开始创建占位图片...")
    
    # 确保 images 目录存在
    os.makedirs('images', exist_ok=True)
    
    # 图片标题映射
    titles = {
        'delay-compensation.jpg': 'Delay Compensation Guide',
        'france-tgv.jpg': 'France TGV Guide',
        'germany-ice.jpg': 'Germany ICE Guide',
        'italy-frecciarossa.jpg': 'Italy Frecciarossa Guide',
        'london-paris.jpg': 'London to Paris Eurostar',
        'seat-reservation.jpg': 'Seat Reservation Guide',
        'spain-ave.jpg': 'Spain AVE Guide',
        'swiss-scenic.jpg': 'Swiss Scenic Trains',
        'train-apps.jpg': 'Train Apps Comparison',
        'train-station.jpg': 'Train Station Guide',
    }
    
    for img in MISSING_IMAGES:
        title = titles.get(img, 'Guide')
        create_placeholder_svg(img, title)
    
    print(f"\n📊 已创建 {len(MISSING_IMAGES)} 个占位图片")
    print("💡 请替换为实际图片文件")

if __name__ == "__main__":
    main()
