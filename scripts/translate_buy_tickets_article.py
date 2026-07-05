#!/usr/bin/env python3
"""
翻译 how-to-buy-european-train-tickets.html 到多语言版本
"""

import os
import re

# 语言配置
LANGUAGES = {
    'de': {
        'lang_code': 'de',
        'title': 'Wie man Europäische Zugtickets kauft: Vollständiger Leitfaden 2026',
        'subtitle': 'Von der Online-Buchung bis zum Bahnhofsschalter – alles, was Sie wissen müssen, um die besten Tarife zu sichern',
        'quick_title': 'Schnelle Tipps',
        'book_early': 'Früh buchen',
        'use_apps': 'Offizielle Apps nutzen',
        'rail_passes': 'Rail Pässe in Betracht ziehen',
        'check_discounts': 'Nach Rabatten suchen',
        'reserve_seats': 'Sitzplätze reservieren',
        'where_buy': 'Wo man europäische Zugtickets kauft',
        'official_apps': '1. Offizielle Bahn-Websites \u0026 Apps',
        'multi_platforms': '2. Multi-Länder Buchungsplattformen',
        'at_station': '3. Am Bahnhof',
        'step_by_step': 'Schritt-für-Schritt Buchungsprozess',
        'step1': 'Schritt 1: Route planen',
        'step2': 'Schritt 2: Preise vergleichen',
        'step3': 'Schritt 3: Tickettyp wählen',
        'step4': 'Schritt 4: Kauf abschließen',
        'money_tips': 'Spartipps',
        'book_early_tip': '1. Früh buchen',
        'railcards': '2. Railcards und Rabattkarten nutzen',
        'alt_routes': '3. Alternative Routen in Betracht ziehen',
        'group_discounts': '4. Gruppenrabatte',
        'mistakes': 'Häufige Buchungsfehler vermeiden',
        'special': 'Besondere Hinweise',
        'cross_border': 'Grenzüberschreitende Reisen',
        'night_trains': 'Nachtzüge',
        'scenic': 'Panoramastrecken',
        'platform_compare': 'Plattform-Vergleich: Wo buchen',
        'faq': 'FAQ',
        'footer': 'Zuletzt aktualisiert: 2. Juli 2026. Preise und Richtlinien können sich ändern; bitte vor der Buchung beim Betreiber verifizieren.',
        'category': 'Leitfaden',
        'date': '2. Juli 2026',
        'hero_text': 'Leitfaden zum Kauf europäischer Zugtickets 2026'
    },
    'fr': {
        'lang_code': 'fr',
        'title': 'Comment Acheter des Billets de Train en Europe: Guide Complet 2026',
        'subtitle': 'De la réservation en ligne aux guichets de gare – tout ce que vous devez savoir pour obtenir les meilleurs tarifs',
        'quick_title': 'Conseils Rapides',
        'book_early': 'Réserver tôt',
        'use_apps': 'Utiliser les applications officielles',
        'rail_passes': 'Envisager les passes ferroviaires',
        'check_discounts': 'Vérifier les réductions',
        'reserve_seats': 'Réserver les sièges',
        'where_buy': 'Où Acheter des Billets de Train en Europe',
        'official_apps': '1. Sites Web \u0026 Applications Officiels',
        'multi_platforms': '2. Plateformes Multi-Pays',
        'at_station': '3. À la Gare',
        'step_by_step': 'Processus de Réservation Étape par Étape',
        'step1': 'Étape 1: Planifier votre itinéraire',
        'step2': 'Étape 2: Comparer les prix',
        'step3': 'Étape 3: Choisir le type de billet',
        'step4': 'Étape 4: Finaliser l\'achat',
        'money_tips': 'Conseils pour Économiser',
        'book_early_tip': '1. Réserver tôt',
        'railcards': '2. Utiliser les cartes de réduction',
        'alt_routes': '3. Envisager des itinéraires alternatifs',
        'group_discounts': '4. Réductions de groupe',
        'mistakes': 'Erreurs de Réservation Courantes à Éviter',
        'special': 'Considérations Spéciales',
        'cross_border': 'Voyages Transfrontaliers',
        'night_trains': 'Trains de Nuit',
        'scenic': 'Routes Panoramiques',
        'platform_compare': 'Comparaison des Plateformes: Où Réserver',
        'faq': 'FAQ',
        'footer': 'Dernière mise à jour: 2 juillet 2026. Les prix et politiques sont sujets à changement; veuillez vérifier auprès de l\'opérateur avant de réserver.',
        'category': 'Guide',
        'date': '2 juillet 2026',
        'hero_text': 'Guide d\'achat de billets de train européens 2026'
    },
    'es': {
        'lang_code': 'es',
        'title': 'Cómo Comprar Billetes de Tren en Europa: Guía Completa 2026',
        'subtitle': 'Desde la reserva online hasta las taquillas de la estación – todo lo que necesita saber para conseguir las mejores tarifas',
        'quick_title': 'Consejos Rápidos',
        'book_early': 'Reservar con antelación',
        'use_apps': 'Usar aplicaciones oficiales',
        'rail_passes': 'Considerar pases ferroviarios',
        'check_discounts': 'Buscar descuentos',
        'reserve_seats': 'Reservar asientos',
        'where_buy': 'Dónde Comprar Billetes de Tren en Europa',
        'official_apps': '1. Webs \u0026 Apps Oficiales',
        'multi_platforms': '2. Plataformas Multi-País',
        'at_station': '3. En la Estación',
        'step_by_step': 'Proceso de Reserva Paso a Paso',
        'step1': 'Paso 1: Planificar su ruta',
        'step2': 'Paso 2: Comparar precios',
        'step3': 'Paso 3: Elegir el tipo de billete',
        'step4': 'Paso 4: Completar la compra',
        'money_tips': 'Consejos para Ahorrar',
        'book_early_tip': '1. Reservar con antelación',
        'railcards': '2. Usar tarjetas de descuento',
        'alt_routes': '3. Considerar rutas alternativas',
        'group_discounts': '4. Descuentos de grupo',
        'mistakes': 'Errores Comunes de Reserva a Evitar',
        'special': 'Consideraciones Especiales',
        'cross_border': 'Viajes Transfronterizos',
        'night_trains': 'Trenes Nocturnos',
        'scenic': 'Rutas Panorámicas',
        'platform_compare': 'Comparación de Plataformas: Dónde Reservar',
        'faq': 'Preguntas Frecuentes',
        'footer': 'Última actualización: 2 de julio de 2026. Los precios y políticas están sujetos a cambios; verifique con el operador antes de reservar.',
        'category': 'Guía',
        'date': '2 de julio de 2026',
        'hero_text': 'Guía de compra de billetes de tren europeos 2026'
    },
    'ja': {
        'lang_code': 'ja',
        'title': 'ヨーロッパの鉄道チケット購入完全ガイド2026',
        'subtitle': 'オンライン予約から駅の窓口まで、最安値でチケットを入手するためのすべて',
        'quick_title': 'クイックヒント',
        'book_early': '早期予約',
        'use_apps': '公式アプリを使用',
        'rail_passes': 'レールパスを検討',
        'check_discounts': '割引を確認',
        'reserve_seats': '座席予約',
        'where_buy': 'ヨーロッパの鉄道チケット購入先',
        'official_apps': '1. 公式鉄道ウェブサイト\u0026アプリ',
        'multi_platforms': '2. 多言語予約プラットフォーム',
        'at_station': '3. 駅で',
        'step_by_step': 'ステップバイステップ予約プロセス',
        'step1': 'ステップ1: ルートを計画',
        'step2': 'ステップ2: 価格を比較',
        'step3': 'ステップ3: チケットタイプを選択',
        'step4': 'ステップ4: 購入を完了',
        'money_tips': '節約のヒント',
        'book_early_tip': '1. 早期予約',
        'railcards': '2. レールカードと割引カードを使用',
        'alt_routes': '3. 代替ルートを検討',
        'group_discounts': '4. グループ割引',
        'mistakes': '避けるべき一般的な予約ミス',
        'special': '特別な考慮事項',
        'cross_border': '国境越えの旅',
        'night_trains': '夜行列車',
        'scenic': '景観ルート',
        'platform_compare': 'プラットフォーム比較: どこで予約するか',
        'faq': 'よくある質問',
        'footer': '最終更新: 2026年7月2日。価格とポリシーは変更される場合があります。予約前に運営者に確認してください。',
        'category': 'ガイド',
        'date': '2026年7月2日',
        'hero_text': 'ヨーロッパ鉄道チケット購入ガイド2026'
    },
    'ko': {
        'lang_code': 'ko',
        'title': '유럽 기차 티켓 구매 방법: 완벽 가이드 2026',
        'subtitle': '온라인 예약부터 역 창구까지 최저가로 티켓을 구매하는 모든 방법',
        'quick_title': '빠른 팁',
        'book_early': '조기 예약',
        'use_apps': '공식 앱 사용',
        'rail_passes': '레일 패스 고려',
        'check_discounts': '할인 확인',
        'reserve_seats': '좌석 예약',
        'where_buy': '유럽 기차 티켓 구매처',
        'official_apps': '1. 공식 철도 웹사이트 \u0026 앱',
        'multi_platforms': '2. 다국어 예약 플랫폼',
        'at_station': '3. 역에서',
        'step_by_step': '단계별 예약 프로세스',
        'step1': '1단계: 경로 계획',
        'step2': '2단계: 가격 비교',
        'step3': '3단계: 티켓 유형 선택',
        'step4': '4단계: 구매 완료',
        'money_tips': '비절약 팁',
        'book_early_tip': '1. 조기 예약',
        'railcards': '2. 레일카드 및 할인 카드 사용',
        'alt_routes': '3. 대체 경로 고려',
        'group_discounts': '4. 단체 할인',
        'mistakes': '피해야 할 일반적인 예약 실수',
        'special': '특별 고려사항',
        'cross_border': '국경 간 여행',
        'night_trains': '야간 열차',
        'scenic': '경관 노선',
        'platform_compare': '플랫폼 비교: 어디에서 예약할까',
        'faq': '자주 묻는 질문',
        'footer': '마지막 업데이트: 2026년 7월 2일. 가격과 정책은 변경될 수 있습니다. 예약 전 운영자에게 확인하세요.',
        'category': '가이드',
        'date': '2026년 7월 2일',
        'hero_text': '유럽 기차 티켓 구매 가이드 2026'
    },
    'pt': {
        'lang_code': 'pt',
        'title': 'Como Comprar Bilhetes de Trem na Europa: Guia Completo 2026',
        'subtitle': 'Da reserva online aos guichês da estação – tudo o que precisa saber para garantir os melhores preços',
        'quick_title': 'Dicas Rápidas',
        'book_early': 'Reservar com antecedência',
        'use_apps': 'Usar apps oficiais',
        'rail_passes': 'Considerar passes ferroviários',
        'check_discounts': 'Verificar descontos',
        'reserve_seats': 'Reservar assentos',
        'where_buy': 'Onde Comprar Bilhetes de Trem na Europa',
        'official_apps': '1. Sites \u0026 Apps Oficiais',
        'multi_platforms': '2. Plataformas Multi-País',
        'at_station': '3. Na Estação',
        'step_by_step': 'Processo de Reserva Passo a Passo',
        'step1': 'Passo 1: Planejar sua rota',
        'step2': 'Passo 2: Comparar preços',
        'step3': 'Passo 3: Escolher o tipo de bilhete',
        'step4': 'Passo 4: Concluir a compra',
        'money_tips': 'Dicas para Economizar',
        'book_early_tip': '1. Reservar com antecedência',
        'railcards': '2. Usar cartões de desconto',
        'alt_routes': '3. Considerar rotas alternativas',
        'group_discounts': '4. Descontos de grupo',
        'mistakes': 'Erros Comuns de Reserva a Evitar',
        'special': 'Considerações Especiais',
        'cross_border': 'Viagens Transfronteiriças',
        'night_trains': 'Trens Noturnos',
        'scenic': 'Rotas Cênicas',
        'platform_compare': 'Comparação de Plataformas: Onde Reservar',
        'faq': 'Perguntas Frequentes',
        'footer': 'Última atualização: 2 de julho de 2026. Preços e políticas estão sujeitos a alterações; verifique com a operadora antes de reservar.',
        'category': 'Guia',
        'date': '2 de julho de 2026',
        'hero_text': 'Guia de compra de bilhetes de trem europeus 2026'
    },
    'zh': {
        'lang_code': 'zh',
        'title': '如何购买欧洲火车票：完整指南2026',
        'subtitle': '从在线预订到车站柜台——获取最优惠票价所需了解的一切',
        'quick_title': '快速要点',
        'book_early': '提前预订',
        'use_apps': '使用官方应用',
        'rail_passes': '考虑铁路通票',
        'check_discounts': '查看折扣',
        'reserve_seats': '预订座位',
        'where_buy': '在哪里购买欧洲火车票',
        'official_apps': '1. 官方铁路网站和应用',
        'multi_platforms': '2. 多国预订平台',
        'at_station': '3. 在车站',
        'step_by_step': '分步预订流程',
        'step1': '第一步：规划路线',
        'step2': '第二步：比较价格',
        'step3': '第三步：选择票种',
        'step4': '第四步：完成购买',
        'money_tips': '省钱技巧',
        'book_early_tip': '1. 提前预订',
        'railcards': '2. 使用铁路卡和折扣卡',
        'alt_routes': '3. 考虑替代路线',
        'group_discounts': '4. 团体折扣',
        'mistakes': '避免常见预订错误',
        'special': '特别注意事项',
        'cross_border': '跨境旅行',
        'night_trains': '夜火车',
        'scenic': '景观路线',
        'platform_compare': '平台对比：在哪里预订',
        'faq': '常见问题',
        'footer': '最后更新：2026年7月2日。价格和政策可能变更；预订前请向运营商确认。',
        'category': '指南',
        'date': '2026年7月2日',
        'hero_text': '欧洲火车票购买指南2026'
    }
}

def translate_article(lang, translations):
    """为指定语言生成翻译后的文章"""
    
    # 读取英文原文
    with open('en/articles/how-to-buy-european-train-tickets.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换语言代码和链接
    content = content.replace('lang="en"', f'lang="{translations["lang_code"]}"')
    content = content.replace('/en/', f'/{lang}/')
    content = content.replace('/en/articles/', f'/{lang}/articles/')
    content = content.replace('href="/en/', f'href="/{lang}/')
    
    # 替换标题和元数据
    content = content.replace('How to Buy European Train Tickets: Complete Guide 2026 | Europe Train', 
                              f'{translations["title"]} | Europe Train')
    content = content.replace('Step-by-step guide to buying European train tickets: online platforms, station counters, mobile apps, and money-saving tips for your rail journey.',
                              f'{translations["subtitle"]}')
    
    # 替换导航
    content = content.replace('Travel Guides', '旅行指南' if lang == 'zh' else 'Guides' if lang == 'fr' else 'Guías' if lang == 'es' else 'Leitfäden' if lang == 'de' else 'ガイド' if lang == 'ja' else '가이드' if lang == 'ko' else 'Guias')
    content = content.replace('Popular Routes', '热门路线' if lang == 'zh' else 'Routes Populaires' if lang == 'fr' else 'Rutas Populares' if lang == 'es' else 'Beliebte Routen' if lang == 'de' else '人気ルート' if lang == 'ja' else '인기 경로' if lang == 'ko' else 'Rotas Populares')
    content = content.replace('Tickets', '车票' if lang == 'zh' else 'Billets' if lang == 'fr' else 'Billetes' if lang == 'es' else 'Tickets' if lang == 'de' else 'チケット' if lang == 'ja' else '티켓' if lang == 'ko' else 'Bilhetes')
    content = content.replace('Passes', '通票' if lang == 'zh' else 'Passes' if lang == 'fr' else 'Pases' if lang == 'es' else 'Pässe' if lang == 'de' else 'パス' if lang == 'ja' else '패스' if lang == 'ko' else 'Passes')
    content = content.replace('Live Status', '实时状态' if lang == 'zh' else 'Statut en Direct' if lang == 'fr' else 'Estado en Vivo' if lang == 'es' else 'Live Status' if lang == 'de' else 'リアルタイム状況' if lang == 'ja' else '실시간 상태' if lang == 'ko' else 'Status ao Vivo')
    
    # 替换文章头部
    content = content.replace('How to Buy European Train Tickets: Complete Guide 2026', translations['title'])
    content = content.replace('From online booking to station counters—everything you need to know to secure the best fares', translations['subtitle'])
    content = content.replace('Guide', translations['category'])
    content = content.replace('July 2, 2026', translations['date'])
    content = content.replace('European Train Ticket Buying Guide 2026', translations['hero_text'])
    
    # 替换快速摘要
    content = content.replace('Quick Takeaways', translations['quick_title'])
    content = content.replace('Book early:', translations['book_early'] + ':')
    content = content.replace('Use official apps:', translations['use_apps'] + ':')
    content = content.replace('Consider rail passes:', translations['rail_passes'] + ':')
    content = content.replace('Check for discounts:', translations['check_discounts'] + ':')
    content = content.replace('Reserve seats:', translations['reserve_seats'] + ':')
    
    # 替换主要章节标题
    content = content.replace('Where to Buy European Train Tickets', translations['where_buy'])
    content = content.replace('1. Official Railway Websites \u0026 Apps', translations['official_apps'])
    content = content.replace('2. Multi-Country Booking Platforms', translations['multi_platforms'])
    content = content.replace('3. At the Station', translations['at_station'])
    content = content.replace('Step-by-Step Booking Process', translations['step_by_step'])
    content = content.replace('Step 1: Plan Your Route', translations['step1'])
    content = content.replace('Step 2: Compare Prices', translations['step2'])
    content = content.replace('Step 3: Choose Your Ticket Type', translations['step3'])
    content = content.replace('Step 4: Complete Your Purchase', translations['step4'])
    content = content.replace('Money-Saving Tips', translations['money_tips'])
    content = content.replace('1. Book Early', translations['book_early_tip'])
    content = content.replace('2. Use Railcards and Discount Cards', translations['railcards'])
    content = content.replace('3. Consider Alternative Routes', translations['alt_routes'])
    content = content.replace('4. Group Travel Discounts', translations['group_discounts'])
    content = content.replace('Common Booking Mistakes to Avoid', translations['mistakes'])
    content = content.replace('Special Considerations', translations['special'])
    content = content.replace('Cross-Border Journeys', translations['cross_border'])
    content = content.replace('Night Trains', translations['night_trains'])
    content = content.replace('Scenic Routes', translations['scenic'])
    content = content.replace('Platform Comparison: Where to Book', translations['platform_compare'])
    content = content.replace('FAQ', translations['faq'])
    
    # 替换页脚
    content = content.replace('Last updated: July 2, 2026. Prices and policies subject to change; always verify with the operator before booking.', translations['footer'])
    
    # 保存翻译后的文件
    output_dir = f'{lang}/articles'
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = f'{output_dir}/how-to-buy-european-train-tickets.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已生成: {output_path}")
    return output_path

def main():
    """主函数：生成所有语言版本"""
    print("🌐 开始翻译文章到多语言版本...")
    
    for lang, translations in LANGUAGES.items():
        if lang == 'en':
            continue  # 英文原文已存在
        
        try:
            translate_article(lang, translations)
        except Exception as e:
            print(f"❌ 翻译 {lang} 失败: {e}")
    
    print("\n✅ 多语言翻译完成！")

if __name__ == "__main__":
    main()
