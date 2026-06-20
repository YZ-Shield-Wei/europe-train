#!/usr/bin/env python3
"""
Website Quality Audit Tool
Checks all language versions for consistency
"""
import requests
import json
from urllib.parse import urljoin

BASE_URL = "https://europe-train.com"
LANGS = ["en", "zh", "de", "fr", "es", "ja", "ko", "pt"]

# Pages to check
PAGES = ["", "articles/", "tickets.html", "routes.html", "passes.html", "live-status.html"]

# Articles to check (from articles/index.html)
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
    """Check a single page for language consistency"""
    try:
        resp = requests.get(url, timeout=30)
        status = resp.status_code
        
        if status != 200:
            return {"status": status, "error": f"HTTP {status}"}
        
        html = resp.text
        
        # Check lang attribute
        lang_match = html.find(f'lang="{expected_lang}"')
        lang_correct = lang_match > -1
        
        # Check navigation links point to correct language
        nav_issues = []
        if expected_lang != "en":
            # Check that navigation links include language prefix
            if f'href="/{expected_lang}/' not in html and f'href="/{expected_lang}/' not in html:
                nav_issues.append("Missing language prefix in navigation")
        
        # Check content language (basic check - look for common English words in non-EN pages)
        content_issues = []
        if expected_lang != "en":
            # Check if page title is English
            if "<title>" in html:
                title_start = html.find("<title>") + 7
                title_end = html.find("</title>")
                title = html[title_start:title_end]
                # Simple heuristic: if title contains mostly ASCII and common English words
                english_words = ["Travel", "Guide", "Train", "Complete", "Tips", "European"]
                for word in english_words:
                    if word in title:
                        content_issues.append(f"English title detected: '{title}'")
                        break
        
        return {
            "status": status,
            "lang_correct": lang_correct,
            "nav_issues": nav_issues,
            "content_issues": content_issues
        }
    except Exception as e:
        return {"status": 0, "error": str(e)}

def main():
    results = {}
    
    print("=" * 80)
    print("EUROPE-TRAIN.COM FULL WEBSITE AUDIT")
    print("=" * 80)
    print()
    
    # Check main pages
    for lang in LANGS:
        print(f"\n{'='*40}")
        print(f"Language: {lang.upper()}")
        print(f"{'='*40}")
        
        lang_results = {}
        
        for page in PAGES:
            if lang == "en":
                url = f"{BASE_URL}/{page}"
            else:
                url = f"{BASE_URL}/{lang}/{page}"
            
            result = check_page(url, lang)
            lang_results[page] = result
            
            status_icon = "✅" if result.get("status") == 200 else "❌"
            lang_icon = "✅" if result.get("lang_correct") else "❌"
            
            print(f"  {status_icon} {page:30s} HTTP:{result.get('status')} Lang:{lang_icon}")
            
            if result.get("nav_issues"):
                for issue in result["nav_issues"]:
                    print(f"     ⚠️  Nav: {issue}")
            
            if result.get("content_issues"):
                for issue in result["content_issues"]:
                    print(f"     ⚠️  Content: {issue}")
        
        # Check articles
        print(f"\n  Articles:")
        for article in ARTICLES:
            if lang == "en":
                url = f"{BASE_URL}/articles/{article}"
            else:
                url = f"{BASE_URL}/{lang}/articles/{article}"
            
            result = check_page(url, lang)
            lang_results[f"articles/{article}"] = result
            
            status_icon = "✅" if result.get("status") == 200 else "❌"
            if result.get("status") != 200:
                print(f"  {status_icon} {article:40s} HTTP:{result.get('status')}")
        
        results[lang] = lang_results
    
    # Summary
    print("\n" + "=" * 80)
    print("AUDIT SUMMARY")
    print("=" * 80)
    
    total_pages = 0
    total_ok = 0
    total_issues = 0
    
    for lang, lang_results in results.items():
        ok_count = sum(1 for r in lang_results.values() if r.get("status") == 200)
        issue_count = sum(len(r.get("content_issues", [])) + len(r.get("nav_issues", [])) for r in lang_results.values())
        total_pages += len(lang_results)
        total_ok += ok_count
        total_issues += issue_count
        
        print(f"{lang.upper():10s} {ok_count:3d}/{len(lang_results):3d} pages OK  {issue_count:3d} issues")
    
    print(f"\nTotal: {total_ok}/{total_pages} pages OK, {total_issues} issues found")

if __name__ == "__main__":
    main()
