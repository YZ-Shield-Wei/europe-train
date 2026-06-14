#!/usr/bin/env python3
"""
Generate disruption detail pages from API data
Uses Python string formatting instead of Handlebars templates to avoid syntax leakage
"""

import requests
import json
import os
from datetime import datetime

# API endpoint
API_URL = "https://traini.ainchina.com/api/disruptions?limit=1000"

# Output directory
OUTPUT_DIR = "/root/.openclaw/workspace/europe-train/disruption"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Operator mapping
OPERATOR_MAP = {
    'DB': {'name': 'Deutsche Bahn', 'country': 'Germany'},
    'SNCF': {'name': 'SNCF', 'country': 'France'},
    'Trenitalia': {'name': 'Trenitalia', 'country': 'Italy'},
    'SBB': {'name': 'Swiss Federal Railways', 'country': 'Switzerland'},
    'Renfe': {'name': 'Renfe', 'country': 'Spain'},
    'NS': {'name': 'Nederlandse Spoorwegen', 'country': 'Netherlands'},
    'NationalRail': {'name': 'National Rail', 'country': 'United Kingdom'},
    'ÖBB': {'name': 'ÖBB', 'country': 'Austria'}
}

def get_status_color(status):
    """Get color for status badge"""
    status = status.lower() if status else 'unknown'
    if status == 'active':
        return '#e91e63'  # Pink/red for active
    elif status == 'resolved':
        return '#4caf50'  # Green for resolved
    else:
        return '#ff9800'  # Orange for unknown

def format_datetime(dt_string):
    """Format datetime string for display"""
    if not dt_string:
        return 'N/A'
    try:
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M UTC')
    except:
        return dt_string

def generate_disruption_page(disruption):
    """Generate HTML page for a single disruption"""
    
    # Extract data
    disruption_id = disruption.get('id', 'unknown')
    operator_code = disruption.get('operatorCode', 'Unknown')
    operator_info = OPERATOR_MAP.get(operator_code, {'name': operator_code, 'country': 'Unknown'})
    operator_name = operator_info['name']
    country = operator_info['country']
    
    title = disruption.get('title', f'{operator_name} Service Disruption')
    description = disruption.get('description', 'No description available.')
    description_short = description[:150] + '...' if len(description) > 150 else description
    
    status = disruption.get('status', 'unknown')
    status_color = get_status_color(status)
    
    disruption_type = disruption.get('type', 'unknown')
    severity = disruption.get('severity', 'unknown')
    
    start_time = disruption.get('startTime', '')
    start_time_formatted = format_datetime(start_time)
    published_at = disruption.get('createdAt', start_time)
    published_at_formatted = format_datetime(published_at)
    
    source_url = disruption.get('sourceUrl', '')
    
    # Handle affected stations
    affected_stations = disruption.get('affectedStations', [])
    if isinstance(affected_stations, str):
        affected_stations = [s.strip() for s in affected_stations.split(',') if s.strip()]
    elif not isinstance(affected_stations, list):
        affected_stations = []
    
    # Build affected stations HTML
    if affected_stations:
        stations_html = '<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px;">'
        for station in affected_stations:
            stations_html += f'<span style="background: #e3f2fd; color: #1976d2; padding: 6px 12px; border-radius: 20px; font-size: 14px;">{station}</span>'
        stations_html += '</div>'
        affected_stations_section = f'''
            <div style="background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h2>Affected Stations</h2>
                {stations_html}
            </div>
        '''
        affected_stations_text = ', '.join(affected_stations)
    else:
        affected_stations_section = ''
        affected_stations_text = 'No specific stations reported'
    
    # Build source URL section
    if source_url:
        source_section = f'''
            <a href="{source_url}" target="_blank" rel="noopener noreferrer" style="display: inline-block; margin-top: 12px; padding: 10px 20px; background: #e91e63; color: white; text-decoration: none; border-radius: 6px; font-weight: 600;">
                View Official Announcement →
            </a>
        '''
    else:
        source_section = ''
    
    # Build HTML page
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Europe Train Disruption Details</title>
    <meta name="description" content="{description_short}. Affected stations: {affected_stations_text}. Status: {status}.">
    <link rel="canonical" href="https://www.europe-train.com/disruption/{disruption_id}.html">
    <link rel="stylesheet" href="../css/global.css">
    
    <!-- FAQ Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {{
                "@type": "Question",
                "name": "What is the current status of {operator_name} service disruption?",
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
                    "text": "Affected stations: {affected_stations_text}."
                }}
            }},
            {{
                "@type": "Question",
                "name": "What type of disruption is this?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "This is a {disruption_type} disruption with {severity} severity."
                }}
            }}
        ]
    }}
    </script>
    
    <!-- Article Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": "{title}",
        "description": "{description_short}",
        "datePublished": "{published_at}",
        "dateModified": "{published_at}",
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
            <p class="subtitle">{operator_name} | {country}</p>
            <div class="article-meta-header">
                <span>Published: {published_at_formatted}</span>
                <span>Type: {disruption_type}</span>
                <span>Severity: {severity}</span>
            </div>
        </div>

        <div class="article-content">
            <!-- Overview Card -->
            <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
                <h2>Overview</h2>
                <p>{description}</p>
            </div>

            <!-- Affected Stations -->
            {affected_stations_section}

            <!-- Impact Details -->
            <div style="background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h2>Impact Details</h2>
                <table style="width: 100%; margin-top: 12px;">
                    <tr>
                        <td style="padding: 8px 0; color: #666;">Disruption Type</td>
                        <td style="padding: 8px 0; font-weight: 600;">{disruption_type}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666;">Severity</td>
                        <td style="padding: 8px 0; font-weight: 600;">{severity}</td>
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

            <!-- Source -->
            <div style="background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h2>Official Source</h2>
                <p>This information is sourced from {operator_name} official channels.</p>
                {source_section}
            </div>

            <!-- FAQ Section for SEO -->
            <div style="background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h2>Frequently Asked Questions</h2>
                
                <div style="margin-top: 16px;">
                    <h3 style="font-size: 16px; margin-bottom: 8px;">What is the current status of this disruption?</h3>
                    <p style="color: #666;">This disruption is currently {status}. {description_short}</p>
                </div>
                
                <div style="margin-top: 16px;">
                    <h3 style="font-size: 16px; margin-bottom: 8px;">Which stations are affected?</h3>
                    <p style="color: #666;">Affected stations: {affected_stations_text}.</p>
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
    
    return html

def main():
    """Main function to generate all disruption pages"""
    
    # Fetch disruptions from API
    print(f"Fetching disruptions from {API_URL}...")
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, dict):
            disruptions = data.get('disruptions', data.get('data', []))
        else:
            disruptions = data
            
        print(f"Total disruptions: {len(disruptions)}")
    except Exception as e:
        print(f"Error fetching disruptions: {e}")
        return
    
    # Generate pages
    generated = 0
    for i, disruption in enumerate(disruptions):
        try:
            html = generate_disruption_page(disruption)
            
            # Write to file
            filename = f"{disruption.get('id', i+1)}.html"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            
            generated += 1
            if generated % 100 == 0:
                print(f"Generated {generated} pages...")
                
        except Exception as e:
            print(f"Error generating page for disruption {disruption.get('id', i+1)}: {e}")
            continue
    
    print(f"\n✅ Generated {generated} disruption detail pages in {OUTPUT_DIR}/")
    print(f"Sample: https://europe-train.com/disruption/1.html")

if __name__ == "__main__":
    main()
