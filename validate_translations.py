#!/usr/bin/env python3
"""
Validate translation completeness for all language versions.
"""

import os
import re
from pathlib import Path

LANGUAGES = ['de', 'fr', 'es', 'ja', 'ko', 'pt', 'zh']
REQUIRED_ELEMENTS = [
    'lang="',
    'hreflang=',
    'class="active"',
    '<title>',
    '<meta name="description"',
]

def validate_file(filepath):
    """Validate a single HTML file"""
    issues = []
    
    if not os.path.exists(filepath):
        return [f"File not found: {filepath}"]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check required elements
    for element in REQUIRED_ELEMENTS:
        if element not in content:
            issues.append(f"Missing: {element}")
    
    # Check for untranslated English text (basic check)
    # Look for common English phrases that should be translated
    english_patterns = [
        r'Book via',
        r'Buy \d+ months',
        r'Money-Saving Tips',
        r'Local Information',
    ]
    
    for pattern in english_patterns:
        if re.search(pattern, content):
            issues.append(f"Possible untranslated text: {pattern}")
    
    return issues

def validate_all():
    """Validate all language versions"""
    base_path = '/root/.openclaw/workspace/europe-train'
    
    print("Translation Validation Report")
    print("=" * 50)
    
    total_issues = 0
    
    for lang in LANGUAGES:
        tickets_path = f'{base_path}/{lang}/tickets.html'
        issues = validate_file(tickets_path)
        
        print(f"\n{lang.upper()}: ", end="")
        if issues:
            print(f"❌ {len(issues)} issues")
            for issue in issues:
                print(f"  - {issue}")
            total_issues += len(issues)
        else:
            print("✅ OK")
    
    print(f"\n{'=' * 50}")
    print(f"Total issues: {total_issues}")
    
    return total_issues == 0

if __name__ == '__main__':
    success = validate_all()
    exit(0 if success else 1)
