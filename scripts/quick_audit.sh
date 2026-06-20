#!/bin/bash
# Quick audit of all language sites

echo "=========================================="
echo "EUROPE-TRAIN.COM QUICK AUDIT"
echo "=========================================="
echo ""

LANGS=("en" "zh" "de" "fr" "es" "ja" "ko" "pt")
PAGES=("" "articles/" "tickets.html")

for lang in "${LANGS[@]}"; do
    echo ""
    echo "=== $lang ==="
    
    for page in "${PAGES[@]}"; do
        if [ "$lang" == "en" ]; then
            url="https://europe-train.com/${page}"
        else
            url="https://europe-train.com/${lang}/${page}"
        fi
        
        status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
        
        if [ "$status" == "200" ]; then
            # Check if content is translated (non-EN only)
            if [ "$lang" != "en" ]; then
                # Check for English words in title
                title=$(curl -s "$url" | grep -o '<title>[^<]*</title>' | head -1)
                if echo "$title" | grep -qi "travel\|guide\|train"; then
                    echo "  ⚠️  $page ($status) - English content detected"
                else
                    echo "  ✅ $page ($status)"
                fi
            else
                echo "  ✅ $page ($status)"
            fi
        else
            echo "  ❌ $page ($status)"
        fi
    done
done
