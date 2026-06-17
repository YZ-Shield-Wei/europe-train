#!/usr/bin/env python3
"""
Update hreflang links for all translated pages.
"""

import os
import re

# Languages
LANGUAGES = ['en', 'de', 'fr', 'es', 'ja', 'ko', 'pt']

# Base URL
BASE_URL = 'https://www.europe-train.com'

def update_hreflang_in_file(filepath, lang):
    """Update hreflang links in a single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove existing hreflang links
    content = re.sub(r'<link rel="alternate"[^>]*>\n?', '', content)
    
    # Generate new hreflang links
    hreflang_links = []
    
    # Get relative path from language root
    rel_path = filepath.replace(f'/root/.openclaw/workspace/europe-train/{lang}/', '')
    
    for l in LANGUAGES:
        if l == 'en':
            url = f'{BASE_URL}/{rel_path}'
        else:
            url = f'{BASE_URL}/{l}/{rel_path}'
        
        hreflang_links.append(f'<link rel="alternate" hreflang="{l}" href="{url}">')
    
    # Add x-default
    hreflang_links.append(f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}/{rel_path}">')
    
    # Insert hreflang links after canonical link
    hreflang_block = '\n'.join(hreflang_links)
    content = re.sub(
        r'(<link rel="canonical"[^>]*>)',
        r'\1\n' + hreflang_block,
        content
    )
    
    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'  ✓ Updated hreflang: {lang}/{rel_path}')
    return True

def process_directory(directory, lang):
    """Process all HTML files in a directory"""
    updated = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if update_hreflang_in_file(filepath, lang):
                    updated += 1
    return updated

def main():
    print('Updating hreflang links for all translated pages...')
    print()
    
    total_updated = 0
    
    for lang in LANGUAGES:
        directory = f'/root/.openclaw/workspace/europe-train/{lang}'
        if os.path.exists(directory):
            print(f'Processing {lang}...')
            updated = process_directory(directory, lang)
            total_updated += updated
            print(f'  Updated {updated} files')
            print()
    
    print(f'✅ Complete! Updated hreflang in {total_updated} files.')

if __name__ == '__main__':
    main()
