#!/usr/bin/env python3
"""
Translate tickets.html to 6 languages.
Keeps HTML structure, translates content text.
"""

import os
import re

# Translation dictionaries for tickets page
TRANSLATIONS = {
    'fr': {
        'Tickets': 'Billets',
        'European train ticket booking guide and money-saving tips': 'Guide d\'achat de billets de train européens et conseils pour économiser',
        'France SNCF': 'France SNCF',
        'Book via SNCF Connect website or App. Buy 2-3 months in advance for PREM\'S fares from €19.': 'Réservez via le site ou l\'application SNCF Connect. Achetez 2-3 mois à l\'avance pour les tarifs PREM\'S dès 19 €.',
        'Germany DB': 'Allemagne DB',
        'DB Navigator App booking. Sparpreis offers 50% discount for advance purchase, BahnCard holders get extra 25% off.': 'Réservation via l\'application DB Navigator. Sparpreis offre 50% de réduction pour l\'achat anticipé, les détenteurs de BahnCard bénéficient de 25% de réduction supplémentaire.',
        'Italy Trenitalia': 'Italie Trenitalia',
        'Super Economy from €9.9 when booked early. Note: non-refundable, confirm your itinerary before booking.': 'Super Economy dès 9,90 € en cas de réservation anticipée. Remarque : non remboursable, confirmez votre itinéraire avant la réservation.',
        'Switzerland SBB': 'Suisse CFF',
        'Supersaver up to 70% off for early booking. Consider Halbtax half-fare card (annual fee CHF 185).': 'Supersaver jusqu\'à 70% de réduction pour les réservations anticipées. Envisagez la carte demi-tarif Halbtax (cotisation annuelle 185 CHF).',
        'Spain Renfe': 'Espagne Renfe',
        'Promo fares from €15 when booked early. AVE high-speed trains require 30-minute advance arrival for security check.': 'Tarifs Promo dès 15 € en cas de réservation anticipée. Les trains à grande vitesse AVE nécessitent une arrivée 30 minutes à l\'avance pour le contrôle de sécurité.',
        'Eurail Pass': 'Pass Eurail',
        'Multi-country continuous or flexible pass. Best for travelers visiting 3+ countries, 15 days from €400.': 'Pass continu ou flexible multi-pays. Idéal pour les voyageurs visitant 3+ pays, 15 jours dès 400 €.',
        'Money-Saving Tips': 'Conseils pour Économiser',
        'Book 2-3 months in advance for early bird discounts': 'Réservez 2-3 mois à l\'avance pour les remises de pré-réservation',
        'Choose off-peak times (Tuesday to Thursday)': 'Choisissez les heures creuses (mardi à jeudi)',
        'Consider rail company membership cards (BahnCard, Halbtax)': 'Envisagez les cartes d\'abonnement des compagnies ferroviaires (BahnCard, Halbtax)',
        'Compare single tickets vs. passes based on your itinerary': 'Comparez les billets simples vs. les passes en fonction de votre itinéraire',
        'Subscribe to rail company promotional emails': 'Abonnez-vous aux e-mails promotionnels des compagnies ferroviaires',
        'Use price alert features for fare drop notifications': 'Utilisez les alertes de prix pour les notifications de baisse de tarifs',
        'Local Information': 'Informations Locales',
        'Currency:': 'Devise :',
        'Price Examples:': 'Exemples de Prix :',
        'Official Booking:': 'Réservation Officielle :',
        'Payment Methods:': 'Modes de Paiement :',
        'Customer Support:': 'Service Client :',
        'Note:': 'Remarque :',
    },
    'es': {
        'Tickets': 'Billetes',
        'European train ticket booking guide and money-saving tips': 'Guía de compra de billetes de tren europeos y consejos para ahorrar',
        'France SNCF': 'Francia SNCF',
        'Book via SNCF Connect website or App. Buy 2-3 months in advance for PREM\'S fares from €19.': 'Reserve a través del sitio web o la aplicación SNCF Connect. Compre con 2-3 meses de antelación para tarifas PREM\'S desde 19 €.',
        'Germany DB': 'Alemania DB',
        'DB Navigator App booking. Sparpreis offers 50% discount for advance purchase, BahnCard holders get extra 25% off.': 'Reserva a través de la aplicación DB Navigator. Sparpreis ofrece 50% de descuento por compra anticipada, los titulares de BahnCard obtienen un 25% adicional de descuento.',
        'Italy Trenitalia': 'Italia Trenitalia',
        'Super Economy from €9.9 when booked early. Note: non-refundable, confirm your itinerary before booking.': 'Super Economy desde 9,90 € al reservar con antelación. Nota: no reembolsable, confirme su itinerario antes de reservar.',
        'Switzerland SBB': 'Suiza SBB',
        'Supersaver up to 70% off for early booking. Consider Halbtax half-fare card (annual fee CHF 185).': 'Supersaver hasta 70% de descuento por reserva anticipada. Considere la tarjeta de media tarifa Halbtax (cuota anual 185 CHF).',
        'Spain Renfe': 'España Renfe',
        'Promo fares from €15 when booked early. AVE high-speed trains require 30-minute advance arrival for security check.': 'Tarifas Promo desde 15 € al reservar con antelación. Los trenes de alta velocidad AVE requieren llegar 30 minutos antes para el control de seguridad.',
        'Eurail Pass': 'Pase Eurail',
        'Multi-country continuous or flexible pass. Best for travelers visiting 3+ countries, 15 days from €400.': 'Pase continuo o flexible multi-país. Ideal para viajeros que visitan 3+ países, 15 días desde 400 €.',
        'Money-Saving Tips': 'Consejos para Ahorrar',
        'Book 2-3 months in advance for early bird discounts': 'Reserve con 2-3 meses de antelación para descuentos por compra anticipada',
        'Choose off-peak times (Tuesday to Thursday)': 'Elija horas de menor demanda (martes a jueves)',
        'Consider rail company membership cards (BahnCard, Halbtax)': 'Considere tarjetas de membresía de compañías ferroviarias (BahnCard, Halbtax)',
        'Compare single tickets vs. passes based on your itinerary': 'Compare billetes sencillos vs. pases según su itinerario',
        'Subscribe to rail company promotional emails': 'Suscríbase a correos promocionales de compañías ferroviarias',
        'Use price alert features for fare drop notifications': 'Use alertas de precio para notificaciones de bajada de tarifas',
        'Local Information': 'Información Local',
        'Currency:': 'Moneda:',
        'Price Examples:': 'Ejemplos de Precios:',
        'Official Booking:': 'Reserva Oficial:',
        'Payment Methods:': 'Métodos de Pago:',
        'Customer Support:': 'Atención al Cliente:',
        'Note:': 'Nota:',
    },
    'ja': {
        'Tickets': '切符',
        'European train ticket booking guide and money-saving tips': 'ヨーロッパ鉄道切符予約ガイドと節約のコツ',
        'France SNCF': 'フランス SNCF',
        'Book via SNCF Connect website or App. Buy 2-3 months in advance for PREM\'S fares from €19.': 'SNCF Connectのウェブサイトまたはアプリで予約。2〜3か月前に購入すると、PREM\'S運賃が19€から。',
        'Germany DB': 'ドイツ DB',
        'DB Navigator App booking. Sparpreis offers 50% discount for advance purchase, BahnCard holders get extra 25% off.': 'DB Navigatorアプリで予約。Sparpreisは事前購入で50%割引、BahnCard保有者はさらに25%割引。',
        'Italy Trenitalia': 'イタリア Trenitalia',
        'Super Economy from €9.9 when booked early. Note: non-refundable, confirm your itinerary before booking.': '早めの予約でSuper Economyが9.9€から。注意：返金不可、予約前に旅程を確認してください。',
        'Switzerland SBB': 'スイス SBB',
        'Supersaver up to 70% off for early booking. Consider Halbtax half-fare card (annual fee CHF 185).': '早割でSupersaverが最大70%割引。Halbtax半額カード（年間料金185CHF）も検討してください。',
        'Spain Renfe': 'スペイン Renfe',
        'Promo fares from €15 when booked early. AVE high-speed trains require 30-minute advance arrival for security check.': '早割でPromo運賃が15€から。AVE高速列車はセキュリティチェックのため30分前の到着が必要。',
        'Eurail Pass': 'ユーレイルパス',
        'Multi-country continuous or flexible pass. Best for travelers visiting 3+ countries, 15 days from €400.': '多国間連続またはフレキシブルパス。3カ国以上を訪れる旅行者に最適、15日間で400€から。',
        'Money-Saving Tips': '節約のコツ',
        'Book 2-3 months in advance for early bird discounts': '早割で2〜3か月前に予約',
        'Choose off-peak times (Tuesday to Thursday)': '閑散期を選ぶ（火曜〜木曜）',
        'Consider rail company membership cards (BahnCard, Halbtax)': '鉄道会社の会員カードを検討（BahnCard、Halbtax）',
        'Compare single tickets vs. passes based on your itinerary': '旅程に応じて片道切符とパスを比較',
        'Subscribe to rail company promotional emails': '鉄道会社のプロモーションメールを購読',
        'Use price alert features for fare drop notifications': '運賃下落通知のための価格アラート機能を使用',
        'Local Information': '現地情報',
        'Currency:': '通貨：',
        'Price Examples:': '価格例：',
        'Official Booking:': '公式予約：',
        'Payment Methods:': '支払方法：',
        'Customer Support:': 'カスタマーサポート：',
        'Note:': '注意：',
    },
    'ko': {
        'Tickets': '승차권',
        'European train ticket booking guide and money-saving tips': '유럽 기차 티켓 예약 가이드와 절약 팁',
        'France SNCF': '프랑스 SNCF',
        'Book via SNCF Connect website or App. Buy 2-3 months in advance for PREM\'S fares from €19.': 'SNCF Connect 웹사이트 또는 앱으로 예약. 2-3개월 전에 구매하면 PREM\'S 요금이 19€부터.',
        'Germany DB': '독일 DB',
        'DB Navigator App booking. Sparpreis offers 50% discount for advance purchase, BahnCard holders get extra 25% off.': 'DB Navigator 앱으로 예약. Sparpreis는 사전 구매 시 50% 할인, BahnCard 소지자는 추가 25% 할인.',
        'Italy Trenitalia': '이탈리아 Trenitalia',
        'Super Economy from €9.9 when booked early. Note: non-refundable, confirm your itinerary before booking.': '미리 예약하면 Super Economy가 9.9€부터. 참고: 환불 불가, 예약 전 여정을 확인하세요.',
        'Switzerland SBB': '스위스 SBB',
        'Supersaver up to 70% off for early booking. Consider Halbtax half-fare card (annual fee CHF 185).': '조기 예약 시 Supersaver가 최대 70% 할인. Halbtax 반액 카드(연회비 185CHF)를 고려해보세요.',
        'Spain Renfe': '스페인 Renfe',
        'Promo fares from €15 when booked early. AVE high-speed trains require 30-minute advance arrival for security check.': '조기 예약 시 Promo 요금이 15€부터. AVE 고속열차는 보안 검색을 위해 30분 전 도착 필요.',
        'Eurail Pass': '유레일 패스',
        'Multi-country continuous or flexible pass. Best for travelers visiting 3+ countries, 15 days from €400.': '다국가 연속 또는 유연한 패스. 3개국 이상 방문하는 여행자에게 최적, 15일간 400€부터.',
        'Money-Saving Tips': '절약 팁',
        'Book 2-3 months in advance for early bird discounts': '얼리버드 할인을 위해 2-3개월 전 예약',
        'Choose off-peak times (Tuesday to Thursday)': '비성수기 시간 선택 (화요일~목요일)',
        'Consider rail company membership cards (BahnCard, Halbtax)': '철도 회사 멤버십 카드 고려 (BahnCard, Halbtax)',
        'Compare single tickets vs. passes based on your itinerary': '여정에 따라 편도 티켓과 패스 비교',
        'Subscribe to rail company promotional emails': '철도 회사 프로모션 이메일 구독',
        'Use price alert features for fare drop notifications': '요금 인하 알림을 위한 가격 알림 기능 사용',
        'Local Information': '현지 정보',
        'Currency:': '통화:',
        'Price Examples:': '가격 예시:',
        'Official Booking:': '공식 예약:',
        'Payment Methods:': '결제 수단:',
        'Customer Support:': '고객 지원:',
        'Note:': '참고:',
    },
    'pt': {
        'Tickets': 'Bilhetes',
        'European train ticket booking guide and money-saving tips': 'Guia de compra de bilhetes de trem europeus e dicas para economizar',
        'France SNCF': 'França SNCF',
        'Book via SNCF Connect website or App. Buy 2-3 months in advance for PREM\'S fares from €19.': 'Reserve pelo site ou aplicativo SNCF Connect. Compre com 2-3 meses de antecedência para tarifas PREM\'S a partir de 19 €.',
        'Germany DB': 'Alemanha DB',
        'DB Navigator App booking. Sparpreis offers 50% discount for advance purchase, BahnCard holders get extra 25% off.': 'Reserva pelo aplicativo DB Navigator. Sparpreis oferece 50% de desconto para compra antecipada, titulares de BahnCard ganham 25% extra de desconto.',
        'Italy Trenitalia': 'Itália Trenitalia',
        'Super Economy from €9.9 when booked early. Note: non-refundable, confirm your itinerary before booking.': 'Super Economy a partir de 9,90 € ao reservar com antecedência. Nota: não reembolsável, confirme seu itinerário antes de reservar.',
        'Switzerland SBB': 'Suíça SBB',
        'Supersaver up to 70% off for early booking. Consider Halbtax half-fare card (annual fee CHF 185).': 'Supersaver com até 70% de desconto para reserva antecipada. Considere o cartão de meia-tarifa Halbtax (taxa anual 185 CHF).',
        'Spain Renfe': 'Espanha Renfe',
        'Promo fares from €15 when booked early. AVE high-speed trains require 30-minute advance arrival for security check.': 'Tarifas Promo a partir de 15 € ao reservar com antecedência. Trens de alta velocidade AVE exigem chegada com 30 minutos de antecedência para verificação de segurança.',
        'Eurail Pass': 'Passe Eurail',
        'Multi-country continuous or flexible pass. Best for travelers visiting 3+ countries, 15 days from €400.': 'Passe contínuo ou flexível multi-país. Melhor para viajantes visitando 3+ países, 15 dias a partir de 400 €.',
        'Money-Saving Tips': 'Dicas para Economizar',
        'Book 2-3 months in advance for early bird discounts': 'Reserve com 2-3 meses de antecedência para descontos de compra antecipada',
        'Choose off-peak times (Tuesday to Thursday)': 'Escolha horários de menor movimento (terça a quinta)',
        'Consider rail company membership cards (BahnCard, Halbtax)': 'Considere cartões de associação de companhias ferroviárias (BahnCard, Halbtax)',
        'Compare single tickets vs. passes based on your itinerary': 'Compare bilhetes simples vs. passes com base no seu itinerário',
        'Subscribe to rail company promotional emails': 'Assine e-mails promocionais de companhias ferroviárias',
        'Use price alert features for fare drop notifications': 'Use recursos de alerta de preço para notificações de queda de tarifas',
        'Local Information': 'Informações Locais',
        'Currency:': 'Moeda:',
        'Price Examples:': 'Exemplos de Preços:',
        'Official Booking:': 'Reserva Oficial:',
        'Payment Methods:': 'Métodos de Pagamento:',
        'Customer Support:': 'Suporte ao Cliente:',
        'Note:': 'Nota:',
    },
    'zh': {
        'Tickets': '车票预订',
        'European train ticket booking guide and money-saving tips': '欧洲火车票预订指南与省钱攻略',
        'France SNCF': '法国 SNCF',
        'Book via SNCF Connect website or App. Buy 2-3 months in advance for PREM\'S fares from €19.': '通过SNCF Connect官网或App预订。提前2-3个月购买可享受PREM\'S优惠票价，低至€19起。',
        'Germany DB': '德国 DB',
        'DB Navigator App booking. Sparpreis offers 50% discount for advance purchase, BahnCard holders get extra 25% off.': '通过DB Navigator App预订。Sparpreis提前购票可享5折优惠，BahnCard持卡人额外再享75折。',
        'Italy Trenitalia': '意大利 Trenitalia',
        'Super Economy from €9.9 when booked early. Note: non-refundable, confirm your itinerary before booking.': '提前预订可享受Super Economy票价€9.9起。注意：不可退款，预订前请确认行程。',
        'Switzerland SBB': '瑞士 SBB',
        'Supersaver up to 70% off for early booking. Consider Halbtax half-fare card (annual fee CHF 185).': '提前预订Supersaver可享高达7折优惠。可考虑办理Halbtax半价卡（年费CHF 185）。',
        'Spain Renfe': '西班牙 Renfe',
        'Promo fares from €15 when booked early. AVE high-speed trains require 30-minute advance arrival for security check.': '提前预订可享受Promo票价€15起。AVE高速列车需提前30分钟到达进行安检。',
        'Eurail Pass': 'Eurail通票',
        'Multi-country continuous or flexible pass. Best for travelers visiting 3+ countries, 15 days from €400.': '多国连续或灵活通票。适合游览3个以上国家的旅客，15天起€400。',
        'Money-Saving Tips': '省钱攻略',
        'Book 2-3 months in advance for early bird discounts': '提前2-3个月预订享受早鸟优惠',
        'Choose off-peak times (Tuesday to Thursday)': '选择非高峰时段（周二至周四）',
        'Consider rail company membership cards (BahnCard, Halbtax)': '考虑办理铁路公司会员卡（BahnCard、Halbtax）',
        'Compare single tickets vs. passes based on your itinerary': '根据行程比较单程票与通票',
        'Subscribe to rail company promotional emails': '订阅铁路公司促销邮件',
        'Use price alert features for fare drop notifications': '使用降价提醒功能获取票价下跌通知',
        'Local Information': '当地信息',
        'Currency:': '货币：',
        'Price Examples:': '价格示例：',
        'Official Booking:': '官方预订：',
        'Payment Methods:': '支付方式：',
        'Customer Support:': '客服支持：',
        'Note:': '注意：',
    }
}

# Language-specific local info
LOCAL_INFO = {
    'fr': {
        'currency': 'EUR',
        'price_examples': 'TGV PREM\'S dès 17€, Carte SNCF Jeune 25-30% de réduction',
        'official_booking': '<a href="https://sncf-connect.com" target="_blank" rel="nofollow">sncf-connect.com</a>',
        'payment_methods': 'Carte bancaire, PayPal, Apple Pay, Google Pay',
        'customer_support': 'Service client francophone, chat en ligne disponible',
        'note': 'SNCF est le principal opérateur ferroviaire en France. Les TGV desservent les grandes villes, les TER les régions.',
    },
    'es': {
        'currency': 'EUR',
        'price_examples': 'AVE Promo desde 15€, Tarjeta +Renfe 25% de descuento',
        'official_booking': '<a href="https://renfe.com" target="_blank" rel="nofollow">renfe.com</a>',
        'payment_methods': 'Tarjeta de crédito, PayPal, transferencia bancaria',
        'customer_support': 'Atención al cliente en español, chat en línea disponible',
        'note': 'Renfe es el operador principal en España. AVE conecta Madrid, Barcelona, Sevilla y otras ciudades principales.',
    },
    'ja': {
        'currency': 'EUR/JPY',
        'price_examples': 'ユーレイルパス 15日間 約64,000円、JRパス連携割引あり',
        'official_booking': '<a href="https://eurail.com" target="_blank" rel="nofollow">eurail.com</a>',
        'payment_methods': 'クレジットカード、PayPal、銀行振込',
        'customer_support': '日本語カスタマーサポート（メール/チャット）',
        'note': '日本からの予約はEurail公式サイトまたは国内旅行会社が便利。JRパスとの併用も検討。',
    },
    'ko': {
        'currency': 'EUR/KRW',
        'price_examples': '유레일 패스 15일 약 58만원, 코레일 회원 연계 할인',
        'official_booking': '<a href="https://eurail.com" target="_blank" rel="nofollow">eurail.com</a>',
        'payment_methods': '신용카드, PayPal, 계좌이체',
        'customer_support': '한국어 고객 지원(이메일/채팅)',
        'note': '한국에서 예약하려면 Eurail 공식 사이트 또는 국내 여행사 이용. 코레일 회원 카드 연동 시 추가 할인 가능.',
    },
    'pt': {
        'currency': 'EUR',
        'price_examples': 'TAP Rail & Fly a partir de 25€, Comboios de Portugal Promoções sazonais',
        'official_booking': '<a href="https://cp.pt" target="_blank" rel="nofollow">cp.pt</a>',
        'payment_methods': 'Cartão de crédito, PayPal, MB WAY, Multibanco',
        'customer_support': 'Suporte ao cliente em português, chat online disponível',
        'note': 'Comboios de Portugal (CP) opera serviços nacionais. Alfa Pendular liga Lisboa, Porto e Faro.',
    },
    'zh': {
        'currency': 'EUR/CNY',
        'price_examples': '欧洲之星提前预订¥350起，Eurail通票15天约¥3,200',
        'official_booking': '<a href="https://raileurope.cn" target="_blank" rel="nofollow">raileurope.cn</a>、<a href="https://eurail.com" target="_blank" rel="nofollow">eurail.com</a>',
        'payment_methods': '信用卡、PayPal、微信支付、支付宝',
        'customer_support': '中文客服支持，微信/邮件咨询',
        'note': '中国旅客可通过Rail Europe中文官网或微信小程序预订，支持微信支付和中文客服。',
    }
}

def translate_tickets(lang):
    """Translate tickets.html for a specific language"""
    src_path = '/root/.openclaw/workspace/europe-train/en/tickets.html'
    
    if not os.path.exists(src_path):
        print(f'  ✗ Source file not found: {src_path}')
        return False
    
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get translations for this language
    trans = TRANSLATIONS.get(lang, {})
    
    # Replace all occurrences
    for en_text, translated in trans.items():
        content = content.replace(en_text, translated)
    
    # Update lang attribute
    content = content.replace('lang="en"', f'lang="{lang}"')
    
    # Update hreflang links
    content = content.replace('hreflang="en"', f'hreflang="{lang}"')
    
    # Update navigation links
    content = content.replace('href="/"', f'href="/{lang}/"')
    content = content.replace('href="/guides/"', f'href="/{lang}/guides/"')
    content = content.replace('href="/articles/"', f'href="/{lang}/articles/"')
    content = content.replace('href="/live-status.html"', f'href="/{lang}/live-status.html"')
    content = content.replace('href="/tickets.html"', f'href="/{lang}/tickets.html"')
    content = content.replace('href="/passes.html"', f'href="/{lang}/passes.html"')
    content = content.replace('href="/routes.html"', f'href="/{lang}/routes.html"')
    
    # Update article links
    content = content.replace('href="/articles/', f'href="/{lang}/articles/')
    content = content.replace('href="/guides/', f'href="/{lang}/guides/')
    
    # Update language switcher active state
    content = content.replace(f'href="/{lang}/" class="active"', f'href="/{lang}/"')
    content = content.replace(f'href="/{lang}/"', f'href="/{lang}/" class="active"')
    
    # Update local info
    local = LOCAL_INFO.get(lang, {})
    if local:
        content = content.replace('GBP/EUR', local.get('currency', 'EUR'))
        content = content.replace('Eurostar Advance from £39, BritRail Pass from £169', local.get('price_examples', ''))
        content = content.replace('<a href="https://thetrainline.com, eurostar.com" target="_blank" rel="nofollow">thetrainline.com, eurostar.com</a>', local.get('official_booking', ''))
        content = content.replace('Credit card, PayPal, Apple Pay, Google Pay', local.get('payment_methods', ''))
        content = content.replace('English customer support, live chat available', local.get('customer_support', ''))
        content = content.replace('National Rail operates UK services. Eurostar connects London with Paris, Brussels, Amsterdam.', local.get('note', ''))
    
    # Write translated file
    output_dir = f'/root/.openclaw/workspace/europe-train/{lang}'
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = f'{output_dir}/tickets.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'  ✓ {lang}/tickets.html')
    return True

def main():
    print('Starting tickets.html translation...')
    print(f'Target languages: {list(TRANSLATIONS.keys())}')
    print()
    
    total_files = 0
    for lang in TRANSLATIONS.keys():
        print(f'Translating to {lang}...')
        if translate_tickets(lang):
            total_files += 1
        print()
    
    print(f'✅ Complete! Translated {total_files} files.')
    print(f'Output: /root/.openclaw/workspace/europe-train/{{lang}}/tickets.html')

if __name__ == '__main__':
    main()
