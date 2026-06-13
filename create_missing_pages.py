#!/usr/bin/env python3
"""
批量创建 europe-train.com 各语言站缺失的子页面
P0 - 子页面404修复：为每个语言站创建 routes.html, tickets.html, passes.html, live-status.html
"""

import os
import shutil
import re

# 配置
LANGUAGES = ['de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']
PAGES = ['routes.html', 'tickets.html', 'passes.html', 'live-status.html']
SOURCE_LANG = 'en'  # 使用英文站作为模板
BASE_DIR = '/root/.openclaw/workspace/europe-train'

# 各语言的语言代码映射（用于 <html lang="">）
LANG_CODES = {
    'de': 'de',
    'fr': 'fr',
    'es': 'es',
    'ja': 'ja',
    'ko': 'ko',
    'pt': 'pt',
    'zh': 'zh-CN'
}

# 各语言的基础路径前缀
LANG_PREFIXES = {
    'de': '/de/',
    'fr': '/fr/',
    'es': '/es/',
    'ja': '/ja/',
    'ko': '/ko/',
    'pt': '/pt/',
    'zh': '/'
}

# 各语言的导航标题映射
NAV_TITLES = {
    'de': {
        'routes': 'Beliebte Strecken',
        'tickets': 'Tickets buchen',
        'passes': 'Pässe',
        'live-status': 'Live-Status',
        'articles': 'Artikel',
        'home': 'Startseite'
    },
    'fr': {
        'routes': 'Routes populaires',
        'tickets': 'Réserver des billets',
        'passes': 'Pass',
        'live-status': 'Statut en direct',
        'articles': 'Articles',
        'home': 'Accueil'
    },
    'es': {
        'routes': 'Rutas populares',
        'tickets': 'Reservar billetes',
        'passes': 'Pases',
        'live-status': 'Estado en vivo',
        'articles': 'Artículos',
        'home': 'Inicio'
    },
    'ja': {
        'routes': '人気ルート',
        'tickets': '切符予約',
        'passes': 'パス',
        'live-status': 'リアルタイム状況',
        'articles': '記事',
        'home': 'ホーム'
    },
    'ko': {
        'routes': '인기 노선',
        'tickets': '승차권 예약',
        'passes': '패스',
        'live-status': '실시간 상태',
        'articles': '기사',
        'home': '홈'
    },
    'pt': {
        'routes': 'Rotas populares',
        'tickets': 'Reservar bilhetes',
        'passes': 'Passes',
        'live-status': 'Status ao vivo',
        'articles': 'Artigos',
        'home': 'Início'
    },
    'zh': {
        'routes': '热门路线',
        'tickets': '车票预订',
        'passes': '通票',
        'live-status': '实时状态',
        'articles': '文章',
        'home': '首页'
    }
}

# 页面标题映射
PAGE_TITLES = {
    'de': {
        'routes': 'Beliebte Zugstrecken in Europa | Europe-Train.com',
        'tickets': 'Europäische Zugtickets buchen | Europe-Train.com',
        'passes': 'Eurail & Interrail Pässe | Europe-Train.com',
        'live-status': 'Live-Zugstatus | Europe-Train.com'
    },
    'fr': {
        'routes': 'Routes de train populaires en Europe | Europe-Train.com',
        'tickets': 'Réserver des billets de train européens | Europe-Train.com',
        'passes': 'Passe Eurail & Interrail | Europe-Train.com',
        'live-status': 'Statut de train en direct | Europe-Train.com'
    },
    'es': {
        'routes': 'Rutas de tren populares en Europa | Europe-Train.com',
        'tickets': 'Reservar billetes de tren europeos | Europe-Train.com',
        'passes': 'Pase Eurail & Interrail | Europe-Train.com',
        'live-status': 'Estado de tren en vivo | Europe-Train.com'
    },
    'ja': {
        'routes': 'ヨーロッパ人気鉄道路線 | Europe-Train.com',
        'tickets': 'ヨーロッパ鉄道切符予約 | Europe-Train.com',
        'passes': 'Eurail & Interrail パス | Europe-Train.com',
        'live-status': '鉄道リアルタイム状況 | Europe-Train.com'
    },
    'ko': {
        'routes': '유럽 인기 기차 노선 | Europe-Train.com',
        'tickets': '유럽 기차 승차권 예약 | Europe-Train.com',
        'passes': 'Eurail & Interrail 패스 | Europe-Train.com',
        'live-status': '기차 실시간 상태 | Europe-Train.com'
    },
    'pt': {
        'routes': 'Rotas de trem populares na Europa | Europe-Train.com',
        'tickets': 'Reservar bilhetes de trem europeus | Europe-Train.com',
        'passes': 'Passe Eurail & Interrail | Europe-Train.com',
        'live-status': 'Status de trem ao vivo | Europe-Train.com'
    },
    'zh': {
        'routes': '欧洲热门火车路线 | Europe-Train.com',
        'tickets': '预订欧洲火车票 | Europe-Train.com',
        'passes': 'Eurail & Interrail 通票 | Europe-Train.com',
        'live-status': '火车实时状态 | Europe-Train.com'
    }
}


def get_page_key(filename):
    """从文件名获取页面key"""
    return filename.replace('.html', '')


def localize_content(content, lang, page_file):
    """将英文内容本地化为目标语言"""
    page_key = get_page_key(page_file)
    prefix = LANG_PREFIXES[lang]
    
    # 1. 修复 html lang 属性
    content = re.sub(
        r'<html lang="[^"]*">',
        f'<html lang="{LANG_CODES[lang]}">',
        content
    )
    
    # 2. 修复页面标题
    if page_key in PAGE_TITLES[lang]:
        title = PAGE_TITLES[lang][page_key]
        content = re.sub(
            r'<title>.*?</title>',
            f'<title>{title}</title>',
            content
        )
    
    # 3. 修复导航链接 - 将 /en/xxx 改为 /{lang}/xxx 或 /xxx
    # 先处理语言切换器中的链接
    content = re.sub(
        r'href="/en/',
        f'href="{prefix}',
        content
    )
    
    # 4. 修复导航菜单标题
    nav = NAV_TITLES[lang]
    
    # 修复导航链接文本和href
    # 首页链接
    content = re.sub(
        r'<a href="/en/"[^>]*>.*?</a>',
        f'<a href="{prefix}">{nav["home"]}</a>',
        content
    )
    
    # 各页面导航链接 - 使用更精确的模式
    for page in ['routes', 'tickets', 'passes', 'live-status']:
        page_file_name = f'{page}.html'
        # 匹配导航中的链接
        pattern = rf'<a href="/en/{page_file_name}"[^>]*>.*?</a>'
        replacement = f'<a href="{prefix}{page_file_name}">{nav[page]}</a>'
        content = re.sub(pattern, replacement, content)
    
    # 修复文章链接
    content = re.sub(
        r'<a href="/en/articles/"[^>]*>.*?</a>',
        f'<a href="{prefix}articles/">{nav["articles"]}</a>',
        content
    )
    
    # 5. 修复语言切换器 - 当前语言高亮
    # 将当前语言的链接改为 span
    for other_lang in LANGUAGES:
        other_prefix = LANG_PREFIXES[other_lang]
        other_code = LANG_CODES[other_lang]
        if other_lang == lang:
            # 当前语言改为 span
            content = re.sub(
                rf'<a href="{other_prefix}{page_file}"[^>]*>(.*?)</a>',
                rf'<span class="lang-active">\1</span>',
                content
            )
        else:
            # 其他语言保持链接
            pass
    
    # 6. 修复 canonical 和 og:url
    content = re.sub(
        r'<link rel="canonical" href="https://www\.europe-train\.com/en/[^"]*"',
        f'<link rel="canonical" href="https://www.europe-train.com{prefix}{page_file}"',
        content
    )
    content = re.sub(
        r'<meta property="og:url" content="https://www\.europe-train\.com/en/[^"]*"',
        f'<meta property="og:url" content="https://www.europe-train.com{prefix}{page_file}"',
        content
    )
    
    return content


def create_page_for_language(lang, page_file):
    """为指定语言创建页面"""
    source_path = os.path.join(BASE_DIR, SOURCE_LANG, page_file)
    target_dir = os.path.join(BASE_DIR, lang)
    target_path = os.path.join(target_dir, page_file)
    
    # 检查源文件是否存在
    if not os.path.exists(source_path):
        print(f"❌ 源文件不存在: {source_path}")
        return False
    
    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)
    
    # 读取源文件
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 本地化处理
    content = localize_content(content, lang, page_file)
    
    # 写入目标文件
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 创建: {target_path}")
    return True


def main():
    """主函数：批量创建所有缺失页面"""
    print("=" * 60)
    print("开始批量创建缺失子页面 (P0)")
    print("=" * 60)
    
    total_created = 0
    total_failed = 0
    
    for lang in LANGUAGES:
        print(f"\n🌍 处理语言站: {lang.upper()}")
        print("-" * 40)
        
        for page in PAGES:
            # 中文站特殊处理：检查是否已存在
            if lang == 'zh':
                target_path = os.path.join(BASE_DIR, lang, page)
                if os.path.exists(target_path):
                    print(f"  ⏭️  已存在，跳过: {lang}/{page}")
                    continue
            
            if create_page_for_language(lang, page):
                total_created += 1
            else:
                total_failed += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 完成! 成功创建: {total_created} 个页面")
    if total_failed > 0:
        print(f"❌ 失败: {total_failed} 个页面")
    print("=" * 60)
    
    return total_failed == 0


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
