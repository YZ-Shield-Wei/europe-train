#!/usr/bin/env python3
"""Create missing article files for all language sites"""
import os
import shutil

# Articles that exist in EN but may be missing in other languages
articles = [
    'paris-to-rome-train-guide.html',
    'berlin-to-munich-train-guide.html'
]

langs = ['de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']

for article in articles:
    en_path = f'/root/.openclaw/workspace/europe-train/articles/{article}'
    
    if not os.path.exists(en_path):
        print(f"⚠️ EN version not found: {article}")
        continue
    
    for lang in langs:
        lang_path = f'/root/.openclaw/workspace/europe-train/{lang}/articles/{article}'
        
        if not os.path.exists(lang_path):
            # Copy EN version as base
            shutil.copy2(en_path, lang_path)
            print(f"✅ Created: {lang}/{article}")
        else:
            print(f"✓ Already exists: {lang}/{article}")

print("\nDone! Now you need to translate each file.")
