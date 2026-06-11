#!/usr/bin/env python3
"""
Translate Chinese HTML articles to Portuguese.
Preserves HTML structure, CSS classes, and styling.
Updates lang to "pt", navigation to /pt/ paths, adds hreflang alternates.
"""

import os
import re
import glob

# Translation dictionaries for common terms
NAV_TRANSLATIONS = {
    '旅行指南': 'Guias de Viagem',
    '热门路线': 'Rotas Populares',
    '车票预订': 'Bilhetes',
    '通票': 'Passes',
    '首页': 'Início',
    'Articles': 'Artigos',
    'Article': 'Artigo',
}

META_TRANSLATIONS = {
    '更新于 2026年6月': 'Atualizado em junho de 2026',
    '阅读时间：': 'Tempo de leitura: ',
    '分钟': ' minutos',
    '核心要点': 'Pontos Principais',
    '费用对比': 'Comparação de Custos',
    '列车体验': 'Experiência de Trem',
    '景观列车': 'Trem Panorâmico',
    '国家指南': 'Guias por País',
    '实用攻略': 'Guias Práticos',
    '硬核科普': 'Guias de Especialistas',
    '预订指南': 'Guia de Reserva',
    '权益保障': 'Compensação',
    'APP对比': 'Comparação de Apps',
    '车站指南': 'Guia de Estações',
    '省钱 checklist': 'Checklist de Economia',
    '重要提示': 'Dicas Importantes',
    '相关指南': 'Guias Relacionados',
    '快速结论': 'Conclusão Rápida',
    '项目': 'Item',
    '详情': 'Detalhes',
    '路线': 'Rota',
    '起点': 'Origem',
    '终点': 'Destino',
    '时间': 'Tempo',
    '距离': 'Distância',
    '运营商': 'Operadora',
    '票价': 'Preço',
    '亮点': 'Destaques',
    '最佳座位': 'Melhores Assentos',
    '座位选择建议': 'Dicas de Seleção de Assentos',
    '季节': 'Estação',
    '优点': 'Prós',
    '缺点': 'Contras',
    '推荐度': 'Recomendação',
    '预订 checklist': 'Checklist de Reserva',
    '票种': 'Tipo de Bilhete',
    '价格区间': 'Faixa de Preço',
    '退改规则': 'Regras de Reembolso',
    '适合人群': 'Público-alvo',
    '等级': 'Classe',
    '包含服务': 'Serviços Incluídos',
    '下载与注册': 'Download e Registro',
    '核心功能': 'Funções Principais',
    '车站': 'Estação',
    '主要目的地': 'Principais Destinos',
    '地铁连接': 'Conexão de Metrô',
    '特色设施': 'Instalações Especiais',
    '周边交通': 'Transporte Local',
    '常见设施': 'Instalações Comuns',
    '行李寄存': 'Depósito de Bagagem',
    '换乘技巧': 'Dicas de Transferência',
    '换乘时间建议': 'Recomendação de Tempo de Transferência',
    '同站换乘': 'Transferência na Mesma Estação',
    '同城不同站': 'Entre Estações da Mesma Cidade',
    '国际换乘': 'Transferência Internacional',
    '主要城市车站间交通': 'Transporte Entre Estações Principais',
    '城市': 'Cidade',
    '车站间交通': 'Transporte Entre Estações',
    '费用': 'Custo',
    '安全提示': 'Dicas de Segurança',
    '安全 checklist': 'Checklist de Segurança',
    '延误时间': 'Tempo de Atraso',
    '赔偿比例': 'Percentual de Indenização',
    '申请方式': 'Forma de Solicitação',
    '必备材料': 'Documentos Necessários',
    '申请步骤': 'Passos para Solicitação',
    '通用流程': 'Processo Geral',
    '全额退款条件': 'Condições para Reembolso Total',
    '部分退款条件': 'Condições para Reembolso Parcial',
    '免费改签': 'Alteração Gratuita',
    '付费改签': 'Alteração Paga',
    '不可抗力': 'Força Maior',
    '铁路公司罢工': 'Greve da Companhia Ferroviária',
    '罢工赔偿': 'Indenização por Greve',
    '实用建议': 'Dicas Práticas',
    '延误 checklist': 'Checklist de Atraso',
    '功能': 'Função',
    '优点': 'Prós',
    '缺点': 'Contras',
    '特色': 'Destaques',
    '下载': 'Download',
    '覆盖': 'Cobertura',
    '适合': 'Ideal para',
    '最佳组合': 'Melhor Combinação',
    '省钱组合': 'Combinação Econômica',
    '便捷组合': 'Combinação Conveniente',
    'APP选择 checklist': 'Checklist de Escolha de APP',
    '线路网络': 'Rede de Linhas',
    '主要线路': 'Principais Linhas',
    '票价体系': 'Sistema de Preços',
    '票种对比': 'Comparação de Tipos de Bilhete',
    '购票技巧': 'Dicas de Compra',
    '座位选择': 'Seleção de Assentos',
    '座位类型': 'Tipos de Assento',
    '选座建议': 'Dicas de Seleção de Assento',
    '座位编号规则': 'Regras de Numeração de Assentos',
    '使用指南': 'Guia de Uso',
    '巴黎火车站指南': 'Guia de Estações de Trem de Paris',
    '其他景观列车': 'Outros Trens Panorâmicos',
    '齿轨登山列车': 'Trens de Cremalheira',
    '票价与通票': 'Preços e Passes',
    '包含': 'Inclui',
    '单独购票': 'Compra Individual',
    '最佳季节': 'Melhor Época',
    '季节对比': 'Comparação de Estações',
    '预订技巧': 'Dicas de Reserva',
    '出入境流程': 'Processo de Imigração',
    '安检流程': 'Processo de Segurança',
    '购票技巧': 'Dicas de Compra',
    '车站指南': 'Guia de Estações',
    '省钱': 'Economia',
    '赔偿申请流程': 'Processo de Solicitação de Indenização',
    '退款规则': 'Regras de Reembolso',
    '改签政策': 'Política de Alteração',
    '特殊情况': 'Situações Especiais',
    '跨国购票APP': 'APPs de Compra Internacional',
    '使用建议': 'Dicas de Uso',
}

CATEGORY_TAGS = {
    '费用对比': 'Comparação de Custos',
    '列车体验': 'Experiência de Trem',
    '景观列车': 'Trem Panorâmico',
    '法国': 'França',
    '德国': 'Alemanha',
    '意大利': 'Itália',
    '西班牙': 'Espanha',
    '预订指南': 'Guia de Reserva',
    '权益保障': 'Compensação',
    'APP对比': 'Comparação de Apps',
    '车站指南': 'Guia de Estações',
    '硬核科普': 'Guia de Especialistas',
    'Comparação': 'Comparação',
    'Experiência': 'Experiência',
    'Panorâmico': 'Panorâmico',
    'França': 'França',
    'Alemanha': 'Alemanha',
    'Itália': 'Itália',
    'Espanha': 'Espanha',
    'Reserva': 'Reserva',
    'Compensação': 'Compensação',
    'Apps': 'Apps',
    'Estações': 'Estações',
    'Especialista': 'Especialista',
}

MONTHS = {
    '1月': 'janeiro',
    '2月': 'fevereiro',
    '3月': 'março',
    '4月': 'abril',
    '5月': 'maio',
    '6月': 'junho',
    '7月': 'julho',
    '8月': 'agosto',
    '9月': 'setembro',
    '10月': 'outubro',
    '11月': 'novembro',
    '12月': 'dezembro',
}

# Article-specific title and description translations
ARTICLE_META = {
    'paris-zurich-train-vs-flight.html': {
        'title': 'Paris a Zurique: Trem vs Avião vs Carro | Europe Train',
        'description': 'Comparação completa de transporte Paris-Zurique: TGV Lyria, avião e carro. Análise detalhada de custos, tempo e experiência.',
        'canonical': 'https://www.europe-train.com/pt/articles/paris-zurich-train-vs-flight.html',
        'h1': 'Paris a Zurique: Trem vs Avião vs Carro',
        'subtitle': 'Uma jornada de 487 km, três experiências de viagem completamente diferentes',
        'category': 'Comparação de Custos',
        'date': '15 de janeiro de 2025',
        'hero': 'Paris → Zurique | 487 km',
    },
    'tgv-lyria-experience.html': {
        'title': 'Experiência TGV Lyria: Viagem Agradável de Paris a Lausanne | Europe Train',
        'description': 'Experiência aprofundada no TGV Lyria: café da manhã no vagão-restaurante, paisagens ao longo do percurso e avaliação completa das instalações.',
        'canonical': 'https://www.europe-train.com/pt/articles/tgv-lyria-experience.html',
        'h1': 'Experiência TGV Lyria: Viagem Agradável de Paris a Lausanne',
        'subtitle': 'Acorde naturalmente, caminhe até a estação, desfrute de um café da manhã francês no trem, e três horas depois passeie à beira do lago suíço',
        'category': 'Experiência de Trem',
        'date': '20 de janeiro de 2025',
        'hero': 'TGV Lyria | Paris → Lausanne',
    },
    'london-paris-eurostar-guide.html': {
        'title': 'Guia Eurostar Londres-Paris | Europe Train - Experiência, Preços, Imigração',
        'description': 'Guia definitivo Eurostar Londres-Paris: experiência, sistema de preços, processo de imigração, seleção de assentos, guia das estações St Pancras e Gare du Nord.',
        'canonical': 'https://www.europe-train.com/pt/articles/london-paris-eurostar-guide.html',
        'h1': 'Guia Eurostar Londres-Paris',
        'subtitle': 'Atualizado 2026: experiência Eurostar, sistema de preços, processo de imigração, seleção de assentos',
        'category': 'Experiência de Trem',
        'date': '10 de junho de 2026',
        'hero': None,
    },
    'swiss-scenic-trains.html': {
        'title': 'Guia de Trens Panorâmicos Suíços | Europe Train - Glacier Express, Bernina Express, GoldenPass',
        'description': 'Guia definitivo de trens panorâmicos suíços: rotas Glacier Express, Bernina Express, GoldenPass, preços, melhor época, seleção de assentos.',
        'canonical': 'https://www.europe-train.com/pt/articles/swiss-scenic-trains.html',
        'h1': 'Guia de Trens Panorâmicos Suíços',
        'subtitle': 'Atualizado 2026: rotas Glacier Express, Bernina Express, GoldenPass, preços, melhor época',
        'category': 'Trem Panorâmico',
        'date': '10 de junho de 2026',
        'hero': None,
    },
    'france-tgv-guide.html': {
        'title': 'Guia Completo do TGV Francês | Europe Train - Rede, Preços, Dicas de Compra',
        'description': 'Guia definitivo do TGV francês: rede de linhas, sistema de preços, dicas de bilhetes antecipados, seleção de assentos, guia do APP SNCF Connect.',
        'canonical': 'https://www.europe-train.com/pt/articles/france-tgv-guide.html',
        'h1': 'Guia Completo do TGV Francês',
        'subtitle': 'Atualizado 2026: rede de linhas, sistema de preços, dicas de bilhetes antecipados, seleção de assentos, guia do APP SNCF Connect',
        'category': 'França',
        'date': '10 de junho de 2026',
        'hero': None,
    },
    'germany-ice-guide.html': {
        'title': 'Guia de Experiência do ICE Alemão | Europe Train - Rede, Preços, Dicas de Economia DB',
        'description': 'Guia definitivo do ICE alemão: rede de linhas, bilhetes antecipados Sparpreis, cartão BahnCard, guia do APP DB Navigator.',
        'canonical': 'https://www.europe-train.com/pt/articles/germany-ice-guide.html',
        'h1': 'Guia de Experiência do ICE Alemão',
        'subtitle': 'Atualizado 2026: rede de linhas, bilhetes antecipados Sparpreis, cartão BahnCard, guia do APP DB Navigator',
        'category': 'Alemanha',
        'date': '10 de junho de 2026',
        'hero': None,
    },
    'italy-frecciarossa-guide.html': {
        'title': 'Guia do Frecciarossa Italiano | Europe Train - Comparação com italo, Preços, Dicas de Economia',
        'description': 'Guia definitivo do Frecciarossa italiano: comparação com italo, sistema de preços, bilhetes antecipados Super Economy, classes de assentos.',
        'canonical': 'https://www.europe-train.com/pt/articles/italy-frecciarossa-guide.html',
        'h1': 'Guia do Frecciarossa Italiano',
        'subtitle': 'Atualizado 2026: comparação com italo, sistema de preços, bilhetes antecipados Super Economy, classes de assentos',
        'category': 'Itália',
        'date': '10 de junho de 2026',
        'hero': None,
    },
    'spain-ave-guide.html': {
        'title': 'Guia do AVE Espanhol | Europe Train - Rede, Preços, Dicas de Economia Renfe',
        'description': 'Guia definitivo do AVE espanhol: rede de linhas, bilhetes promocionais, cartão +Renfe, classes de assentos, guia do APP Renfe.',
        'canonical': 'https://www.europe-train.com/pt/articles/spain-ave-guide.html',
        'h1': 'Guia do AVE Espanhol',
        'subtitle': 'Atualizado 2026: rede de linhas, bilhetes promocionais, cartão +Renfe, classes de assentos',
        'category': 'Espanha',
        'date': '10 de junho de 2026',
        'hero': None,
    },
    'delay-compensation-guide.html': {
        'title': 'Guia de Indenização por Atraso de Trem Europeu | Europe Train - Reembolso, Regras de Alteração',
        'description': 'Guia definitivo de indenização por atraso de trem europeu: padrões de indenização por país, processo de solicitação, regras de reembolso.',
        'canonical': 'https://www.europe-train.com/pt/articles/delay-compensation-guide.html',
        'h1': 'Guia de Indenização por Atraso de Trem Europeu',
        'subtitle': 'Atualizado 2026: padrões de indenização por país, processo de solicitação, regras de reembolso',
        'category': 'Compensação',
        'date': '10 de junho de 2026',
        'hero': None,
    },
    'europe-train-ticket-rules.html': {
        'title': 'Guia Completo de Regras de Bilhetes de Trem Europeus | Europe Train',
        'description': 'Guia detalhado de regras de bilhetes de trem europeus: SNCF, DB, Trenitalia, SBB, Renfe - códigos e símbolos, evite multas.',
        'canonical': 'https://www.europe-train.com/pt/articles/europe-train-ticket-rules.html',
        'h1': 'Guia Completo de Regras de Bilhetes de Trem Europeus',
        'subtitle': 'Entenda cada código e símbolo no seu bilhete, evite multas e constrangimentos',
        'category': 'Guia de Especialistas',
        'date': '25 de janeiro de 2025',
        'hero': 'Regras de Bilhetes de Trem Europeus | Comparação de 5 Países',
    },
    'train-apps-comparison.html': {
        'title': 'Comparação de APPs de Trem Europeus | Europe Train - Avaliação de Funções',
        'description': 'Comparação definitiva de APPs de trem europeus: SNCF Connect, DB Navigator, Trenitalia, SBB Mobile, Renfe - avaliação de funções, análise de prós e contras.',
        'canonical': 'https://www.europe-train.com/pt/articles/train-apps-comparison.html',
        'h1': 'Comparação de APPs de Trem Europeus',
        'subtitle': 'Atualizado 2026: avaliação de funções SNCF Connect, DB Navigator, Trenitalia, SBB Mobile, Renfe',
        'category': 'Comparação de Apps',
        'date': '10 de junho de 2026',
        'hero': None,
    },
    'train-station-guide.html': {
        'title': 'Guia Completo de Estações de Trem Europeias | Europe Train - Instalações, Navegação, Transferência',
        'description': 'Guia definitivo de estações de trem europeias: instalações principais, dicas de navegação, regras de transferência, depósito de bagagem, refeições e compras.',
        'canonical': 'https://www.europe-train.com/pt/articles/train-station-guide.html',
        'h1': 'Guia Completo de Estações de Trem Europeias',
        'subtitle': 'Atualizado 2026: instalações principais, dicas de navegação, regras de transferência, depósito de bagagem, transporte local',
        'category': 'Guia de Estações',
        'date': '10 de junho de 2026',
        'hero': None,
    },
}

def translate_common_text(content):
    """Translate common navigation and UI text."""
    # Language switcher
    content = content.replace('href="/zh/" class="active"', 'href="/pt/" class="active"')
    content = content.replace('href="/zh/"', 'href="/zh/"')
    
    # Navigation links
    content = content.replace('href="/articles/"', 'href="/pt/articles/"')
    content = content.replace('href="/routes.html"', 'href="/pt/routes.html"')
    content = content.replace('href="/tickets.html"', 'href="/pt/tickets.html"')
    content = content.replace('href="/passes.html"', 'href="/pt/passes.html"')
    content = content.replace('href="/"', 'href="/pt/"')
    
    # Breadcrumb
    content = content.replace('href="/">首页', 'href="/pt/">Início')
    content = content.replace('href="/">Home', 'href="/pt/">Início')
    content = content.replace('href="/articles/">旅行指南', 'href="/pt/articles/">Guias de Viagem')
    content = content.replace('href="/articles/">Articles', 'href="/pt/articles/">Artigos')
    
    # Nav items
    for cn, pt in NAV_TRANSLATIONS.items():
        content = content.replace(f'>{cn}<', f'>{pt}<')
    
    # Meta translations
    for cn, pt in META_TRANSLATIONS.items():
        content = content.replace(cn, pt)
    
    # Category tags in articles
    for cn, pt in CATEGORY_TAGS.items():
        content = content.replace(f'>{cn}<', f'>{pt}<')
        content = content.replace(f'class="tag">{cn}', f'class="tag">{pt}')
    
    # Month translations in dates
    for cn, pt in MONTHS.items():
        content = content.replace(cn, pt)
    
    # Date format translations
    content = content.replace('年', ' de ')
    content = content.replace('月', ' ')
    content = content.replace('日', ' de ')
    
    # Footer
    content = content.replace('© 2026 Europe Train Travel Guide. All rights reserved.', '© 2026 Europe Train Travel Guide. Todos os direitos reservados.')
    
    # Article footer text
    content = content.replace('本文由 Europe Train 编辑部撰写，基于', 'Artigo escrito pela redação Europe Train, baseado em ')
    content = content.replace('实际体验。票价和时刻可能变动，请查询最新信息。', 'experiência real. Preços e horários podem variar, consulte as informações mais recentes.')
    content = content.replace('实际体验。规则可能变动，请以各铁路公司最新规定为准。', 'experiência real. As regras podem mudar, consulte as regulamentações mais recentes de cada companhia ferroviária.')
    
    return content

def add_hreflang(content, filename):
    """Add hreflang alternate links to head."""
    # Find the canonical link and add hreflang after it
    canonical_pattern = r'<link rel="canonical" href="([^"]+)">'
    canonical_match = re.search(canonical_pattern, content)
    
    if canonical_match:
        canonical_url = canonical_match.group(1)
        # Extract the path part after /articles/
        if '/pt/articles/' in canonical_url:
            base_path = canonical_url.replace('https://www.europe-train.com/pt/articles/', '')
            hreflang_block = f'''    <link rel="canonical" href="{canonical_url}">
    <link rel="alternate" hreflang="en" href="https://www.europe-train.com/en/articles/{base_path}">
    <link rel="alternate" hreflang="zh-CN" href="https://www.europe-train.com/articles/{base_path}">
    <link rel="alternate" hreflang="pt" href="{canonical_url}">'''
            content = content.replace(canonical_match.group(0), hreflang_block)
    
    return content

def update_css_paths(content):
    """Update CSS paths for pt/articles/ directory."""
    # Change ../css/ to ../../css/ since we're in pt/articles/
    content = content.replace('href="../css/', 'href="../../css/')
    content = content.replace('href="css/global.css"', 'href="../../css/global.css"')
    content = content.replace('url(\'../images/', 'url(\'../../images/')
    content = content.replace('url("../images/', 'url("../../images/')
    return content

def update_article_links(content):
    """Update internal article links to pt/ paths."""
    # Links to other articles in /articles/ should go to /pt/articles/
    content = content.replace('href="/articles/', 'href="/pt/articles/')
    content = content.replace('href="/guides/', 'href="/pt/guides/')
    
    # But don't double-convert already pt links
    content = content.replace('href="/pt/pt/', 'href="/pt/')
    
    return content

def translate_article(filename, source_dir, target_dir):
    """Translate a single article."""
    source_path = os.path.join(source_dir, filename)
    target_path = os.path.join(target_dir, filename)
    
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update lang attribute
    content = content.replace('<html lang="zh-CN">', '<html lang="pt">')
    content = content.replace('<html lang="zh">', '<html lang="pt">')
    
    # Apply common translations
    content = translate_common_text(content)
    
    # Update CSS paths
    content = update_css_paths(content)
    
    # Update article links
    content = update_article_links(content)
    
    # Apply article-specific meta translations
    meta = ARTICLE_META.get(filename, {})
    if meta:
        # Update title
        if 'title' in meta:
            content = re.sub(r'<title>[^<]+</title>', f'<title>{meta["title"]}</title>', content)
        
        # Update description
        if 'description' in meta:
            content = re.sub(r'<meta name="description" content="[^"]+">', 
                           f'<meta name="description" content="{meta["description"]}">', content)
        
        # Update canonical
        if 'canonical' in meta:
            # This will be handled by add_hreflang
            pass
        
        # Update h1
        if 'h1' in meta:
            content = re.sub(r'<h1>[^<]+</h1>', f'<h1>{meta["h1"]}</h1>', content, count=1)
        
        # Update subtitle
        if 'subtitle' in meta:
            content = re.sub(r'<p class="article-subtitle">[^<]+</p>', 
                           f'<p class="article-subtitle">{meta["subtitle"]}</p>', content)
            content = re.sub(r'<p class="subtitle">[^<]+</p>', 
                           f'<p class="subtitle">{meta["subtitle"]}</p>', content, count=1)
        
        # Update category
        if 'category' in meta:
            content = re.sub(r'<span class="category">[^<]+</span>', 
                           f'<span class="category">{meta["category"]}</span>', content, count=1)
        
        # Update date
        if 'date' in meta:
            content = re.sub(r'<span class="date">[^<]+</span>', 
                           f'<span class="date">{meta["date"]}</span>', content, count=1)
        
        # Update hero image text
        if 'hero' in meta and meta['hero']:
            content = re.sub(r'<div class="hero-image">\s*[^<]+\s*</div>', 
                           f'<div class="hero-image">\n            {meta["hero"]}\n        </div>', content, count=1)
    
    # Add hreflang alternates
    content = add_hreflang(content, filename)
    
    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Translated: {filename}")
    return True

def main():
    source_dir = '/root/.openclaw/workspace/europe-train/articles'
    target_dir = '/root/.openclaw/workspace/europe-train/pt/articles'
    
    # Get all HTML files except index.html
    files = [f for f in os.listdir(source_dir) if f.endswith('.html') and f != 'index.html']
    files.sort()
    
    print(f"Found {len(files)} articles to translate")
    
    for filename in files:
        translate_article(filename, source_dir, target_dir)
    
    print(f"\n✅ All {len(files)} articles translated to {target_dir}")

if __name__ == '__main__':
    main()
