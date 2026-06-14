#!/usr/bin/env python3
"""
批量生成 disruption 详情页
为每个 disruption 创建独立的 SEO 友好页面
"""

import json
import os
import re
from datetime import datetime

# 创建输出目录
output_dir = "/root/.openclaw/workspace/europe-train/disruption"
os.makedirs(output_dir, exist_ok=True)

# 获取 disruption 数据
import subprocess
result = subprocess.run(
    ["curl", "-s", "https://traini.ainchina.com/api/disruptions?limit=1000"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
disruptions = data.get("data", [])

print(f"Total disruptions: {len(disruptions)}")

# 生成页面
generated = 0
for d in disruptions:
    try:
        # 准备替换数据
        status = d.get("status", "unknown")
        status_color = "#4caf50" if status == "resolved" else "#ff9800" if status == "active" else "#f44336"
        
        affected_stations = d.get("affectedStations", [])
        affected_stations_str = ", ".join(affected_stations) if affected_stations else "Not specified"
        
        # 格式化时间
        start_time = d.get("startTime", "")
        try:
            dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            start_time_formatted = dt.strftime("%Y-%m-%d %H:%M UTC")
        except:
            start_time_formatted = start_time
        
        try:
            published_dt = datetime.fromisoformat(d.get("publishedAt", "").replace("Z", "+00:00"))
            published_at_formatted = published_dt.strftime("%B %d, %Y at %H:%M UTC")
        except:
            published_at_formatted = d.get("publishedAt", "")
        
        # 简短描述（前200字符）
        desc = d.get("descriptionTranslated") or d.get("description", "")
        description_short = desc[:200] + "..." if len(desc) > 200 else desc
        
        # 清理标题中的特殊字符
        title = d.get("titleTranslated") or d.get("title", "")
        title = re.sub(r'[^\w\s\-\(\)]', ' ', title).strip()
        
        # 生成 affected stations HTML
        if affected_stations:
            stations_html = "\n".join([
                f'                    <span style="background: #e3f2fd; color: #1976d2; padding: 6px 12px; border-radius: 20px; font-size: 14px;">{s}</span>'
                for s in affected_stations
            ])
            affected_stations_section = f'''
            <div style="background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h2>Affected Stations</h2>
                <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px;">
{stations_html}
                </div>
            </div>'''
        else:
            affected_stations_section = ""
        
        # 生成 source_url 按钮
        source_url = d.get("sourceUrl", "")
        if source_url:
            source_button = f'''
                <a href="{source_url}" target="_blank" rel="noopener noreferrer" style="display: inline-block; margin-top: 12px; padding: 10px 20px; background: #e91e63; color: white; text-decoration: none; border-radius: 6px; font-weight: 600;">
                    View Official Announcement →
                </a>'''
        else:
            source_button = ""
        
        # 构建完整 HTML
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Europe Train Disruption Details</title>
    <meta name="description" content="{description_short}. Affected stations: {affected_stations_str}. Status: {status}.">
    <link rel="canonical" href="https://www.europe-train.com/disruption/{d.get('id', '')}.html">
    <link rel="stylesheet" href="../css/global.css">
    
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {{
                "@type": "Question",
                "name": "What is the current status of {d.get('operatorName', '')} service disruption?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "The disruption is currently {status}. {description_short}"
                }}
            }},
            {{
                "@type": "Question",
                "name": "Which stations are affected by this disruption?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "Affected stations: {affected_stations_str}."
                }}
            }},
            {{
                "@type": "Question",
                "name": "What type of disruption is this?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "This is a {d.get('disruptionType', '')} disruption with {d.get('severity', '')} severity."
                }}
            }}
        ]
    }}
    </script>
    
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": "{title}",
        "description": "{description_short}",
        "datePublished": "{d.get('publishedAt', '')}",
        "dateModified": "{d.get('publishedAt', '')}",
        "author": {{
            "@type": "Organization",
            "name": "Europe Train"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "Europe Train",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://www.europe-train.com/images/logo.png"
            }}
        }}
    }}
    </script>
</head>
<body>
    <header class="header">
        <div class="header-inner">
            <a href="/" class="logo">
                <div class="logo-icon">ET</div>
                Europe Train
            </a>
            <nav class="nav">
                <a href="/">Home</a>
                <a href="/live-status.html">Live Status</a>
            </nav>
        </div>
    </header>

    <article class="article">
        <div class="article-header">
            <div style="display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 16px; background: {status_color}; color: white;">
                {status}
            </div>
            <h1>{title}</h1>
            <p class="subtitle">{d.get('operatorName', '')} | {d.get('country', '')}</p>
            <div class="article-meta-header">
                <span>Published: {published_at_formatted}</span>
                <span>Type: {d.get('disruptionType', '')}</span>
                <span>Severity: {d.get('severity', '')}</span>
            </div>
        </div>

        <div class="article-content">
            <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
                <h2>Overview</h2>
                <p>{desc}</p>
            </div>

{affected_stations_section}

            <div style="background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h2>Impact Details</h2>
                <table style="width: 100%; margin-top: 12px;">
                    <tr>
                        <td style="padding: 8px 0; color: #666;">Disruption Type</td>
                        <td style="padding: 8px 0; font-weight: 600;">{d.get('disruptionType', '')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666;">Severity</td>
                        <td style="padding: 8px 0; font-weight: 600;">{d.get('severity', '')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666;">Start Time</td>
                        <td style="padding: 8px 0; font-weight: 600;">{start_time_formatted}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666;">Status</td>
                        <td style="padding: 8px 0; font-weight: 600;">{status}</td>
                    </tr>
                </table>
            </div>

            <div style="background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h2>Official Source</h2>
                <p>This information is sourced from {d.get('operatorName', '')} official channels.</p>
{source_button}
            </div>

            <div style="background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h2>Frequently Asked Questions</h2>
                
                <div style="margin-top: 16px;">
                    <h3 style="font-size: 16px; margin-bottom: 8px;">What is the current status of this disruption?</h3>
                    <p style="color: #666;">This disruption is currently {status}. {description_short}</p>
                </div>
                
                <div style="margin-top: 16px;">
                    <h3 style="font-size: 16px; margin-bottom: 8px;">Which stations are affected?</h3>
                    <p style="color: #666;">Affected stations: {affected_stations_str}.</p>
                </div>
                
                <div style="margin-top: 16px;">
                    <h3 style="font-size: 16px; margin-bottom: 8px;">How long will this disruption last?</h3>
                    <p style="color: #666;">The disruption started on {start_time_formatted}. Please check the official source for the latest updates on expected resolution time.</p>
                </div>
            </div>
        </div>
    </article>

    <footer class="footer">
        <p>© 2026 Europe Train Travel Guide. All rights reserved.</p>
    </footer>
</body>
</html>'''
        
        # 写入文件
        filename = f"{d.get('id', generated)}.html"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        generated += 1
        if generated % 100 == 0:
            print(f"Generated {generated} pages...")
            
    except Exception as e:
        print(f"Error generating page for disruption {d.get('id', 'unknown')}: {e}")

print(f"\n✅ Generated {generated} disruption detail pages in {output_dir}/")
print(f"Sample: https://europe-train.com/disruption/{disruptions[0].get('id', '1')}.html")
