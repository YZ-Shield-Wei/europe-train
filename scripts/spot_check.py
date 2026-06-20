#!/usr/bin/env python3
"""
Spot Check Verification System
Randomly verifies pages to ensure quality
"""
import random
import requests
import os
import re

BASE_URL = "https://europe-train.com"
LANGS = ["en", "zh", "de", "fr", "es", "ja", "ko", "pt"]

# All pages to check
PAGES = {
    "home": "",
    "articles_index": "articles/",
    "tickets": "tickets.html",
    "routes": "routes.html",
    "passes": "passes.html",
    "live_status": "live-status.html"
}

# Sample articles to check (random selection)
ARTICLES = [
    "paris-to-rome-train-guide.html",
    "berlin-to-munich-train-guide.html",
    "paris-zurich-train-vs-flight.html",
    "tgv-lyria-experience.html",
    "london-paris-eurostar-guide.html",
    "swiss-scenic-trains.html",
    "france-tgv-guide.html",
    "germany-ice-guide.html",
    "italy-frecciarossa-guide.html",
    "spain-ave-guide.html",
    "seat-reservation-guide.html",
    "train-station-guide.html",
    "europe-train-ticket-rules.html",
    "delay-compensation-guide.html",
    "train-apps-comparison.html"
]

def check_page(url, expected_lang):
    """Check a single page for issues"""
    issues = []
    
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code != 200:
            return [f"HTTP {resp.status_code}"]
        
        html = resp.text
        
        # Check 1: Language attribute
    if f'lang="{expected_lang}"' not in html and f'lang="{expected_lang}-CN"' not in html:
            issues.append(f"Wrong lang attribute")
        
        # Check 2: Navigation links point to correct language
        if expected_lang != "en":
            # Should have language prefix in main nav links
            if f'href="/{expected_lang}/' not in html:
                issues.append("Missing language prefix in navigation")
        
        # Check 3: Title should not be pure English for non-EN pages
        if expected_lang != "en":
            title_match = re.search(r'<title>([^<]*)</title>', html)
            if title_match:
                title = title_match.group(1)
                # Check if title contains common English phrases
                english_indicators = ["Complete Guide", "Travel Tips", "Train Travel"]
                for indicator in english_indicators:
                    if indicator in title and not any(x in title for x in ["指南", "Reiseführer", "Guide", "Guía", "ガイド", "가이드"]):
                        issues.append(f"English title: {title[:50]}")
                        break
        
        # Check 4: Hreflang tags
        if expected_lang != "en":
            if f'hreflang="{expected_lang}"' not in html:
                issues.append("Missing hreflang tag")
        
        return issues
    except Exception as e:
        return [f"Error: {str(e)}"]

def spot_check():
    """Perform random spot checks"""
    print("=" * 60)
    print("SPOT CHECK VERIFICATION")
    print("=" * 60)
    print()
    
    # Randomly select 3 languages
    check_langs = random.sample(LANGS, 3)
    print(f"Checking languages: {', '.join(check_langs)}")
    print()
    
    total_issues = 0
    
    for lang in check_langs:
        print(f"\n--- {lang.upper()} ---")
        
        # Check 2 random main pages
        check_pages = random.sample(list(PAGES.keys()), 2)
        for page_key in check_pages:
            page_path = PAGES[page_key]
            if lang == "en":
                url = f"{BASE_URL}/{page_path}"
            else:
                url = f"{BASE_URL}/{lang}/{page_path}"
            
            issues = check_page(url, lang)
            if issues:
                print(f"  ❌ {page_key}: {', '.join(issues)}")
                total_issues += len(issues)
            else:
                print(f"  ✅ {page_key}")
        
        # Check 2 random articles
        check_articles = random.sample(ARTICLES, 2)
        for article in check_articles:
            if lang == "en":
                url = f"{BASE_URL}/articles/{article}"
            else:
                url = f"{BASE_URL}/{lang}/articles/{article}"
            
            issues = check_page(url, lang)
            if issues:
                print(f"  ❌ {article}: {', '.join(issues)}")
                total_issues += len(issues)
            else:
                print(f"  ✅ {article[:40]}")
    
    print()
    print("=" * 60)
    if total_issues == 0:
        print("✅ SPOT CHECK PASSED - No issues found!")
    else:
        print(f"❌ SPOT CHECK FAILED - {total_issues} issues found")
    print("=" * 60)
    
    return total_issues

if __name__ == "__main__":
    spot_check()
