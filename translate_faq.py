#!/usr/bin/env python3
"""
Translate FAQ page to 6 languages.
"""

import os

TRANSLATIONS = {
    'de': {
        'FAQ': 'FAQ',
        'Frequently Asked Questions': 'Häufig Gestellte Fragen',
        'How do I book European train tickets?': 'Wie buche ich europäische Zugtickets?',
        'You can book through official railway websites...': 'Sie können über offizielle Bahnwebsites (SNCF Connect, DB Navigator, Trenitalia), Drittanbieter-Plattformen (Trainline, Omio) oder an Bahnhöfen buchen. Online-Buchung wird für Frühbucherrabatte empfohlen.',
        'How far in advance should I book?': 'Wie weit im Voraus sollte ich buchen?',
        'For high-speed trains...': 'Für Hochgeschwindigkeitszüge (TGV, ICE, AVE) 2-3 Monate im Voraus buchen für die besten Preise. Regionalzüge erfordern normalerweise keine Vorausbuchung. Eurail-Pässe können jederzeit vor der Reise gekauft werden.',
        'What is a Eurail Pass?': 'Was ist ein Eurail-Pass?',
        'A Eurail Pass is...': 'Ein Eurail-Pass ist ein Multi-Länder-Zugpass, der in 33 europäischen Ländern gültig ist. Optionen umfassen Global Pass (alle Länder), Select Pass (2-4 Länder) und One Country Pass. Am besten für Reisende, die 3+ Länder besuchen.',
        'How do seat reservations work?': 'Wie funktionieren Sitzplatzreservierungen?',
        'High-speed and international trains...': 'Hochgeschwindigkeits- und internationale Züge erfordern Sitzplatzreservierungen (€10-30). Regionalzüge benötigen normalerweise keine Reservierungen. Reservierungen können online oder an Bahnhöfen vorgenommen werden.',
        'What is the refund policy?': 'Wie ist die Rückerstattungspolitik?',
        'Flexible fares...': 'Flexible Tarife: Volle Rückerstattung vor Abfahrt. Semi-flexibel: Teilweise Rückerstattung mit Gebühr. Nicht flexibel (Super Economy, PREM\'S): Keine Rückerstattung. Reiseversicherung empfohlen.',
        'How do children tickets work?': 'Wie funktionieren Kindertickets?',
        'Children under 4...': 'Kinder unter 4 Jahren reisen kostenlos (ohne Sitzplatz). Alter 4-11 typischerweise 50% Rabatt. Familienrabatte in Deutschland, Schweiz und Frankreich verfügbar. Spezifische Betreiberpolitiken prüfen.',
        'What are the luggage rules?': 'Was sind die Gepäckregeln?',
        'Most European trains...': 'Die meisten europäischen Züge erlauben 2 große Koffer + 1 Handgepäck pro Person. Keine Gewichtsbeschränkungen, müssen aber in Gepäckregalen passen. Übergroße Gegenstände erfordern möglicherweise spezielle Buchung.',
        'Am I entitled to compensation for delays?': 'Habe ich Anspruch auf Entschädigung bei Verspätungen?',
        'EU regulation...': 'EU-Verordnung EG 261/2007: 50% Rückerstattung für Verspätungen 60-119 Minuten, 100% für 120+ Minuten. Anträge über die Website des Betreibers innerhalb von 3 Monaten einreichen.',
        'How do I collect my tickets?': 'Wie hole ich meine Tickets ab?',
        'Options: mobile tickets...': 'Optionen: Mobile Tickets (QR-Code), Zuhause ausdrucken, Abholung an Bahnhöfen an Automaten oder Schaltern. Mobile Tickets sind am bequemsten und umweltfreundlich.',
        'What payment methods are accepted?': 'Welche Zahlungsmethoden werden akzeptiert?',
        'Credit/debit cards...': 'Kredit-/Debitkarten (Visa, Mastercard), PayPal, Apple Pay, Google Pay. Einige Betreiber akzeptieren lokale Methoden (Sofort in Deutschland, iDEAL in den Niederlanden).',
    },
    'fr': {
        'FAQ': 'FAQ',
        'Frequently Asked Questions': 'Questions Fréquemment Posées',
        'How do I book European train tickets?': 'Comment réserver des billets de train européens ?',
        'You can book through official railway websites...': 'Vous pouvez réserver via les sites web officiels des chemins de fer (SNCF Connect, DB Navigator, Trenitalia), les plateformes tierces (Trainline, Omio) ou en gare. La réservation en ligne est recommandée pour les remises de pré-réservation.',
        'How far in advance should I book?': 'Combien de temps à l\'avance dois-je réserver ?',
        'For high-speed trains...': 'Pour les trains à grande vitesse (TGV, ICE, AVE), réservez 2-3 mois à l\'avance pour les meilleurs prix. Les trains régionaux ne nécessitent généralement pas de réservation anticipée. Les passes Eurail peuvent être achetés à tout moment avant le voyage.',
        'What is a Eurail Pass?': 'Qu\'est-ce qu\'un pass Eurail ?',
        'A Eurail Pass is...': 'Un pass Eurail est un pass train multi-pays valable dans 33 pays européens. Les options incluent le Global Pass (tous les pays), le Select Pass (2-4 pays) et le One Country Pass. Idéal pour les voyageurs visitant 3+ pays.',
        'How do seat reservations work?': 'Comment fonctionnent les réservations de sièges ?',
        'High-speed and international trains...': 'Les trains à grande vitesse et internationaux nécessitent des réservations de sièges (€10-30). Les trains régionaux ne nécessitent généralement pas de réservation. Les réservations peuvent être faites en ligne ou en gare.',
        'What is the refund policy?': 'Quelle est la politique de remboursement ?',
        'Flexible fares...': 'Tarifs flexibles : remboursement intégral avant le départ. Semi-flexible : remboursement partiel avec frais. Non flexible (Super Economy, PREM\'S) : aucun remboursement. Assurance voyage recommandée.',
        'How do children tickets work?': 'Comment fonctionnent les billets enfants ?',
        'Children under 4...': 'Les enfants de moins de 4 ans voyagent gratuitement (sans siège). Âge 4-11 typiquement 50% de réduction. Réductions familiales disponibles en Allemagne, Suisse et France. Vérifiez les politiques spécifiques des opérateurs.',
        'What are the luggage rules?': 'Quelles sont les règles de bagages ?',
        'Most European trains...': 'La plupart des trains européens autorisent 2 grandes valises + 1 bagage à main par personne. Pas de limites de poids, mais doivent tenir dans les porte-bagages. Les articles surdimensionnés peuvent nécessiter une réservation spéciale.',
        'Am I entitled to compensation for delays?': 'Ai-je droit à une indemnisation pour les retards ?',
        'EU regulation...': 'Règlement UE CE 261/2007 : 50% de remboursement pour les retards de 60-119 minutes, 100% pour 120+ minutes. Soumettez les réclamations via le site web de l\'opérateur dans les 3 mois.',
        'How do I collect my tickets?': 'Comment récupérer mes billets ?',
        'Options: mobile tickets...': 'Options : billets mobiles (QR code), imprimer à domicile, retrait en gare aux distributeurs ou guichets. Les billets mobiles sont les plus pratiques et écologiques.',
        'What payment methods are accepted?': 'Quels modes de paiement sont acceptés ?',
        'Credit/debit cards...': 'Cartes de crédit/débit (Visa, Mastercard), PayPal, Apple Pay, Google Pay. Certains opérateurs acceptent des méthodes locales (Sofort en Allemagne, iDEAL aux Pays-Bas).',
    },
    'es': {
        'FAQ': 'FAQ',
        'Frequently Asked Questions': 'Preguntas Frecuentes',
        'How do I book European train tickets?': '¿Cómo reservo billetes de tren europeos?',
        'You can book through official railway websites...': 'Puede reservar a través de sitios web oficiales de ferrocarriles (SNCF Connect, DB Navigator, Trenitalia), plataformas de terceros (Trainline, Omio) o en estaciones. Se recomienda la reserva en línea para descuentos por compra anticipada.',
        'How far in advance should I book?': '¿Con cuánta antelación debo reservar?',
        'For high-speed trains...': 'Para trenes de alta velocidad (TGV, ICE, AVE), reserve 2-3 meses antes para los mejores precios. Los trenes regionales generalmente no requieren reserva anticipada. Los pases Eurail se pueden comprar en cualquier momento antes del viaje.',
        'What is a Eurail Pass?': '¿Qué es un pase Eurail?',
        'A Eurail Pass is...': 'Un pase Eurail es un pase de tren multi-país válido en 33 países europeos. Las opciones incluyen Global Pass (todos los países), Select Pass (2-4 países) y One Country Pass. Mejor para viajeros que visitan 3+ países.',
        'How do seat reservations work?': '¿Cómo funcionan las reservas de asientos?',
        'High-speed and international trains...': 'Los trenes de alta velocidad e internacionales requieren reservas de asientos (€10-30). Los trenes regionales típicamente no requieren reservas. Las reservas se pueden hacer en línea o en estaciones.',
        'What is the refund policy?': '¿Cuál es la política de reembolso?',
        'Flexible fares...': 'Tarifas flexibles: reembolso completo antes de la salida. Semi-flexible: reembolso parcial con tarifa. No flexible (Super Economy, PREM\'S): sin reembolso. Se recomienda seguro de viaje.',
        'How do children tickets work?': '¿Cómo funcionan los billetes para niños?',
        'Children under 4...': 'Niños menores de 4 años viajan gratis (sin asiento). Edades 4-11 típicamente 50% de descuento. Descuentos familiares disponibles en Alemania, Suiza y Francia. Verifique políticas específicas de operadores.',
        'What are the luggage rules?': '¿Cuáles son las reglas de equipaje?',
        'Most European trains...': 'La mayoría de los trenes europeos permiten 2 maletas grandes + 1 equipaje de mano por persona. Sin límites de peso, pero deben caber en los portaequipajes. Los artículos grandes pueden requerir reserva especial.',
        'Am I entitled to compensation for delays?': '¿Tengo derecho a compensación por retrasos?',
        'EU regulation...': 'Reglamento UE CE 261/2007: 50% de reembolso por retrasos de 60-119 minutos, 100% para 120+ minutos. Presente reclamaciones a través del sitio web del operador dentro de 3 meses.',
        'How do I collect my tickets?': '¿Cómo recojo mis billetes?',
        'Options: mobile tickets...': 'Opciones: billetes móviles (código QR), imprimir en casa, recogida en estación en máquinas o mostradores. Los billetes móviles son los más convenientes y ecológicos.',
        'What payment methods are accepted?': '¿Qué métodos de pago se aceptan?',
        'Credit/debit cards...': 'Tarjetas de crédito/débito (Visa, Mastercard), PayPal, Apple Pay, Google Pay. Algunos operadores aceptan métodos locales (Sofort en Alemania, iDEAL en Países Bajos).',
    },
    'ja': {
        'FAQ': 'よくある質問',
        'Frequently Asked Questions': 'よくある質問',
        'How do I book European train tickets?': 'ヨーロッパの鉄道切符はどうやって予約しますか？',
        'You can book through official railway websites...': '鉄道会社の公式ウェブサイト（SNCF Connect、DB Navigator、Trenitalia）、第三者プラットフォーム（Trainline、Omio）、または駅で予約できます。早割を受けるにはオンライン予約がおすすめです。',
        'How far in advance should I book?': 'どのくらい前に予約すべきですか？',
        'For high-speed trains...': '高速列車（TGV、ICE、AVE）は2〜3か月前に予約すると最安値で購入できます。地域列車は通常事前予約不要です。ユーレイルパスは出発前にいつでも購入可能です。',
        'What is a Eurail Pass?': 'ユーレイルパスとは何ですか？',
        'A Eurail Pass is...': 'ユーレイルパスは33ヶ国で有効な多国間鉄道パスです。グローバルパス（全対象国）、セレクトパス（2〜4カ国）、ワンカントリーパスがあります。3カ国以上を訪れる旅行者に最適です。',
        'How do seat reservations work?': '座席予約はどうやりますか？',
        'High-speed and international trains...': '高速列車・国際列車は座席予約が必要です（€10〜30）。地域列車は通常予約不要です。オンラインまたは駅で予約できます。',
        'What is the refund policy?': '払い戻しポリシーはどうなっていますか？',
        'Flexible fares...': 'フレキシブル運賃：出発前に全額払い戻し。セミフレキシブル：手数料ありで一部払い戻し。ノンフレキシブル（スーパーエコノミー、PREM\'S）：払い戻し不可。旅行保険の加入をおすすめします。',
        'How do children tickets work?': '子供料金はどうなっていますか？',
        'Children under 4...': '4歳未満は無料（座席なし）。4〜11歳は通常50%割引。ドイツ、スイス、フランスではファミリー割引あり。各鉄道会社の規定をご確認ください。',
        'What are the luggage rules?': '手荷物規定はどうなっていますか？',
        'Most European trains...': 'ヨーロッパの列車の多くは、大きなスーツケース2個＋機内持ち込み1個までOK。重量制限はありませんが、荷物置き場に収まるサイズが条件。特大荷物は別途予約が必要な場合があります。',
        'Am I entitled to compensation for delays?': '遅延時の補償はありますか？',
        'EU regulation...': 'EU規則EC261/2007：60〜119分遅延で50%払い戻し、120分以上で全額払い戻し。請求は運行会社のウェブサイトから3か月以内に行ってください。',
        'How do I collect my tickets?': '切符はどうやって受け取りますか？',
        'Options: mobile tickets...': 'モバイル切符（QRコード）、自宅印刷、駅の券売機・窓口での受け取りが選べます。モバイル切符が最も便利でエコです。',
        'What payment methods are accepted?': 'どの支払い方法が使えますか？',
        'Credit/debit cards...': 'クレジット/デビットカード（Visa、Mastercard）、PayPal、Apple Pay、Google Payが使用可能です。一部の鉄道会社では現地の支払い方法（ドイツのSofort、オランダのiDEAL）も受け付けています。',
    },
    'ko': {
        'FAQ': '자주 묻는 질문',
        'Frequently Asked Questions': '자주 묻는 질문',
        'How do I book European train tickets?': '유럽 기차 티켓은 어떻게 예약하나요?',
        'You can book through official railway websites...': '철도 회사 공식 웹사이트(SNCF Connect, DB Navigator, Trenitalia), 제3자 플랫폼(Trainline, Omio) 또는 역에서 예약할 수 있습니다. 얼리버드 할인을 받으려면 온라인 예약을 권장합니다.',
        'How far in advance should I book?': '얼마나 미리 예약해야 하나요?',
        'For high-speed trains...': '고속열차(TGV, ICE, AVE)는 최저가를 원하면 2~3개월 전에 예약하세요. 지역열차는 보통 사전 예약이 필요 없습니다. 유레일 패스는 출발 전 언제든 구매 가능합니다.',
        'What is a Eurail Pass?': '유레일 패스란 무엇인가요?',
        'A Eurail Pass is...': '유레일 패스는 33개 유럽 국가에서 유효한 다국간 기차 패스입니다. 글로벌 패스(전체 국가), 셀렉트 패스(2~4개국), 원 컨트리 패스가 있습니다. 3개국 이상 여행자에게 가장 적합합니다.',
        'How do seat reservations work?': '좌석 예약은 어떻게 하나요?',
        'High-speed and international trains...': '고속열차 및 국제열차는 좌석 예약이 필수입니다(€10~30). 지역열차는 보통 예약이 필요 없습니다. 온라인 또는 역에서 예약할 수 있습니다.',
        'What is the refund policy?': '환불 정책은 어떻게 되나요?',
        'Flexible fares...': '플렉시블 요금: 출발 전 전액 환불. 세미플렉시블: 수수료 공제 후 부분 환불. 논플렉시블(슈퍼 이코노미, PREM\'S): 환불 불가. 여행자 보험 가입을 권장합니다.',
        'How do children tickets work?': '아동 티켓은 어떻게 되나요?',
        'Children under 4...': '4세 미만은 무료(좌석 없음). 4~11세는 일반적으로 50% 할인. 독일, 스위스, 프랑스에서 가족 할인 가능. 특정 운영사 정책을 확인하세요.',
        'What are the luggage rules?': '수하물 규정은 어떻게 되나요?',
        'Most European trains...': '대부분의 유럽 열차는 1인당 대형 수하물 2개 + 기내용 1개 허용. 중량 제한은 없으나 수하물 보관함에 들어가는 크기여야 함. 초대형 물품은 별도 예약 필요할 수 있음.',
        'Am I entitled to compensation for delays?': '지연 시 보상을 받을 수 있나요?',
        'EU regulation...': 'EU 규정 EC 261/2007: 60~119분 지연 시 50% 환불, 120분 이상 시 100% 환불. 청구는 운영사 웹사이트를 통해 3개월 이내에 제출하세요.',
        'How do I collect my tickets?': '티켓은 어떻게 수령하나요?',
        'Options: mobile tickets...': '모바일 티켓(QR 코드), 홈프린트, 역 기계 또는 창구에서 수령. 모바일 티켓이 가장 편리하고 친환경적입니다.',
        'What payment methods are accepted?': '어떤 결제 수단을 사용할 수 있나요?',
        'Credit/debit cards...': '신용/직불카드(Visa, Mastercard), PayPal, Apple Pay, Google Pay. 일부 운영사는 현지 결제 수단(독일 Sofort, 네덜란드 iDEAL)도 수락합니다.',
    },
    'pt': {
        'FAQ': 'FAQ',
        'Frequently Asked Questions': 'Perguntas Frequentes',
        'How do I book European train tickets?': 'Como reservo bilhetes de trem europeus?',
        'You can book through official railway websites...': 'Pode reservar através de sites oficiais de ferrovias (SNCF Connect, DB Navigator, Trenitalia), plataformas de terceiros (Trainline, Omio) ou nas estações. A reserva online é recomendada para descontos de compra antecipada.',
        'How far in advance should I book?': 'Com quanta antecedência devo reservar?',
        'For high-speed trains...': 'Para trens de alta velocidade (TGV, ICE, AVE), reserve 2-3 meses antes para os melhores preços. Trens regionais geralmente não requerem reserva antecipada. Pases Eurail podem ser comprados a qualquer momento antes da viagem.',
        'What is a Eurail Pass?': 'O que é um Passe Eurail?',
        'A Eurail Pass is...': 'Um Passe Eurail é um passe de trem multi-país válido em 33 países europeus. As opções incluem Global Pass (todos os países), Select Pass (2-4 países) e One Country Pass. Melhor para viajantes visitando 3+ países.',
        'How do seat reservations work?': 'Como funcionam as reservas de assentos?',
        'High-speed and international trains...': 'Trens de alta velocidade e internacionais requerem reservas de assentos (€10-30). Trens regionais tipicamente não requerem reservas. Reservas podem ser feitas online ou nas estações.',
        'What is the refund policy?': 'Qual é a política de reembolso?',
        'Flexible fares...': 'Tarifas flexíveis: reembolso integral antes da partida. Semi-flexível: reembolso parcial com taxa. Não flexível (Super Economy, PREM\'S): sem reembolso. Seguro de viagem recomendado.',
        'How do children tickets work?': 'Como funcionam os bilhetes para crianças?',
        'Children under 4...': 'Crianças menores de 4 anos viajam grátis (sem assento). Idades 4-11 tipicamente 50% de desconto. Descontos familiares disponíveis na Alemanha, Suíça e França. Verifique políticas específicas dos operadores.',
        'What are the luggage rules?': 'Quais são as regras de bagagem?',
        'Most European trains...': 'A maioria dos trens europeus permite 2 malas grandes + 1 bagagem de mão por pessoa. Sem limites de peso, mas devem caber nos porta-bagagens. Itens grandes podem requerer reserva especial.',
        'Am I entitled to compensation for delays?': 'Tenho direito a compensação por atrasos?',
        'EU regulation...': 'Regulamento UE CE 261/2007: 50% de reembolso por atrasos de 60-119 minutos, 100% para 120+ minutos. Submeta reclamações através do site do operador dentro de 3 meses.',
        'How do I collect my tickets?': 'Como recolho os meus bilhetes?',
        'Options: mobile tickets...': 'Opções: bilhetes móveis (código QR), imprimir em casa, levantamento na estação em máquinas ou balcões. Bilhetes móveis são os mais convenientes e ecológicos.',
        'What payment methods are accepted?': 'Quais métodos de pagamento são aceites?',
        'Credit/debit cards...': 'Cartões de crédito/débito (Visa, Mastercard), PayPal, Apple Pay, Google Pay. Alguns operadores aceitam métodos locais (Sofort na Alemanha, iDEAL nos Países Baixos).',
    },
    'zh': {
        'FAQ': '常见问题',
        'Frequently Asked Questions': '常见问题解答',
        'How do I book European train tickets?': '如何预订欧洲火车票？',
        'You can book through official railway websites...': '您可以通过官方铁路网站（SNCF Connect、DB Navigator、Trenitalia）、第三方平台（Trainline、Omio）或在车站预订。建议在线预订以享受早鸟优惠。',
        'How far in advance should I book?': '应该提前多久预订？',
        'For high-speed trains...': '高速列车（TGV、ICE、AVE）建议提前2-3个月预订以获得最优价格。地区列车通常无需提前预订。Eurail通票可在出发前随时购买。',
        'What is a Eurail Pass?': '什么是Eurail通票？',
        'A Eurail Pass is...': 'Eurail通票是在33个欧洲国家有效的多国铁路通票。选项包括全球通票（所有国家）、自选通票（2-4个国家）和单国通票。适合游览3个以上国家的旅客。',
        'How do seat reservations work?': '如何预订座位？',
        'High-speed and international trains...': '高速列车和国际列车需要预订座位（€10-30）。地区列车通常无需预订。可在线或在车站预订。',
        'What is the refund policy?': '退票政策是什么？',
        'Flexible fares...': '灵活票价：出发前可全额退款。半灵活：扣除手续费后部分退款。非灵活（Super Economy、PREM\'S）：不可退款。建议购买旅行保险。',
        'How do children tickets work?': '儿童票怎么买？',
        'Children under 4...': '4岁以下儿童免费（无座）。4-11岁通常可享5折优惠。德国、瑞士、法国提供家庭优惠。请查看各运营商具体政策。',
        'What are the luggage rules?': '行李规定是什么？',
        'Most European trains...': '大多数欧洲列车允许每人携带2件大行李+1件随身行李。无重量限制，但须能放入行李架。超大行李可能需要特殊预订。',
        'Am I entitled to compensation for delays?': '列车晚点有赔偿吗？',
        'EU regulation...': '欧盟法规EC 261/2007：晚点60-119分钟可获50%退款，120分钟以上可获全额退款。请在运营商网站提交索赔，期限为3个月内。',
        'How do I collect my tickets?': '如何取票？',
        'Options: mobile tickets...': '可选方式：手机电子票（二维码）、在家打印、车站自动售票机或柜台取票。手机电子票最方便且环保。',
        'What payment methods are accepted?': '支持哪些支付方式？',
        'Credit/debit cards...': '支持信用卡/借记卡（Visa、Mastercard）、PayPal、Apple Pay、Google Pay。部分运营商接受本地支付方式（德国Sofort、荷兰iDEAL）。',
    }
}

def translate_faq(lang):
    """Translate FAQ page for a specific language"""
    src_path = '/root/.openclaw/workspace/europe-train/en/faq.html'
    
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
    
    # Update navigation links
    content = content.replace('href="/en/', f'href="/{lang}/')
    
    # Write translated file
    output_dir = f'/root/.openclaw/workspace/europe-train/{lang}'
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = f'{output_dir}/faq.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'  ✓ {lang}/faq.html')
    return True

def main():
    print('Starting FAQ translation...')
    print(f'Target languages: {list(TRANSLATIONS.keys())}')
    print()
    
    total_files = 0
    for lang in TRANSLATIONS.keys():
        print(f'Translating to {lang}...')
        if translate_faq(lang):
            total_files += 1
        print()
    
    print(f'✅ Complete! Translated {total_files} files.')
    print(f'Output: /root/.openclaw/workspace/europe-train/{{lang}}/faq.html')

if __name__ == '__main__':
    main()
