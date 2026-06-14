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

# 读取模板
with open("/root/.openclaw/workspace/europe-train/templates/disruption-detail.html", "r") as f:
    template = f.read()

# 获取 disruption 数据
import subprocess
result = subprocess.run(
    ["curl", "-s", "https://traini.ainchina.com/api/disruptions?limit=100"],
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
        
        # 替换模板变量
        html = template
        html = html.replace("{{id}}", str(d.get("id", "")))
        html = html.replace("{{title}}", title)
        html = html.replace("{{description}}", desc)
        html = html.replace("{{description_short}}", description_short)
        html = html.replace("{{operator_name}}", d.get("operatorName", ""))
        html = html.replace("{{country}}", d.get("country", ""))
        html = html.replace("{{status}}", status)
        html = html.replace("{{status_color}}", status_color)
        html = html.replace("{{disruption_type}}", d.get("disruptionType", ""))
        html = html.replace("{{severity}}", d.get("severity", ""))
        html = html.replace("{{start_time_formatted}}", start_time_formatted)
        html = html.replace("{{published_at}}", d.get("publishedAt", ""))
        html = html.replace("{{published_at_formatted}}", published_at_formatted)
        html = html.replace("{{source_url}}", d.get("sourceUrl", ""))
        html = html.replace("{{affected_stations}}", affected_stations_str)
        
        # 处理 affectedStations 列表
        if affected_stations:
            stations_html = "\n".join([
                f'                    <span style="background: #e3f2fd; color: #1976d2; padding: 6px 12px; border-radius: 20px; font-size: 14px;">{s}</span>'
                for s in affected_stations
            ])
            html = html.replace("{{#each affected_stations}}\n                    <span style=\"background: #e3f2fd; color: #1976d2; padding: 6px 12px; border-radius: 20px; font-size: 14px;\">{{this}}</span>\n                    {{/each}}", stations_html)
        else:
            html = html.replace("{{#if affected_stations}}", "<!-- ")
            html = html.replace("{{/if}}", " -->")
        
        # 写入文件
        filename = f"{d.get('id', generated)}.html"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        generated += 1
        if generated % 10 == 0:
            print(f"Generated {generated} pages...")
            
    except Exception as e:
        print(f"Error generating page for disruption {d.get('id', 'unknown')}: {e}")

print(f"\n✅ Generated {generated} disruption detail pages in {output_dir}/")
print(f"Sample: https://europe-train.com/disruption/{disruptions[0].get('id', '1')}.html")
