#!/usr/bin/env python3
"""
Batch fix all language sites
Updates all pages with proper translations
"""
import os
import shutil
from translations import get_translation

BASE_DIR = "/root/.openclaw/workspace/europe-train"
LANGS = ["de", "fr", "es", "ja", "ko", "pt"]

def create_translated_index(lang):
    """Create translated index.html for a language"""
    
    # Read English template
    en_path = os.path.join(BASE_DIR, "articles", "index.html")
    with open(en_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Basic replacements
    content = content.replace('lang="en"', f'lang="{lang}"')
    
    # Update navigation links
    content = content.replace('href="/"', f'href="/{lang}/"')
    content = content.replace('href="/articles/"', f'href="/{lang}/articles/"')
    content = content.replace('href="/routes.html"', f'href="/{lang}/routes.html"')
    content = content.replace('href="/tickets.html"', f'href="/{lang}/tickets.html"')
    content = content.replace('href="/passes.html"', f'href="/{lang}/passes.html"')
    content = content.replace('href="/live-status.html"', f'href="/{lang}/live-status.html"')
    
    # Update lang switcher
    content = content.replace('href="/" class="active"', 'href="/"')
    content = content.replace(f'href="/{lang}/"', f'href="/{lang}/" class="active"')
    
    # Translate navigation text
    content = content.replace('>Travel Guides<', f'>{get_translation(lang, "nav_guides")}<')
    content = content.replace('>Popular Routes<', f'>{get_translation(lang, "nav_routes")}<')
    content = content.replace('>Tickets<', f'>{get_translation(lang, "nav_tickets")}<')
    content = content.replace('>Passes<', f'>{get_translation(lang, "nav_passes")}<')
    content = content.replace('>Live Status<', f'>{get_translation(lang, "nav_status")}<')
    
    # Translate footer
    content = content.replace('All rights reserved', get_translation(lang, 'footer'))
    
    # Write translated file
    lang_dir = os.path.join(BASE_DIR, lang, "articles")
    os.makedirs(lang_dir, exist_ok=True)
    
    output_path = os.path.join(lang_dir, "index.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {lang}/articles/index.html created")

def main():
    print("Starting batch translation...")
    print()
    
    for lang in LANGS:
        create_translated_index(lang)
    
    print()
    print("Batch translation complete!")
    print("Note: Article content still needs manual translation.")

if __name__ == "__main__":
    main()
