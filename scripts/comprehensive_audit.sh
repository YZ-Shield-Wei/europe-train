#!/bin/bash
# Comprehensive website audit
# Checks all pages for consistency, language, and structure

echo "=========================================="
echo "EUROPE-TRAIN.COM COMPREHENSIVE AUDIT"
echo "=========================================="
echo ""

LANGS=("en" "zh" "de" "fr" "es" "ja" "ko" "pt")
PAGES=("" "articles/" "tickets.html")
ARTICLES=(
    "paris-to-rome-train-guide.html"
    "berlin-to-munich-train-guide.html"
    "paris-zurich-train-vs-flight.html"
    "tgv-lyria-experience.html"
    "london-paris-eurostar-guide.html"
    "swiss-scenic-trains.html"
    "france-tgv-guide.html"
    "germany-ice-guide.html"
    "italy-frecciarossa-guide.html"
    "spain-ave-guide.html"
    "seat-reservation-guide.html"
    "train-station-guide.html"
    "europe-train-ticket-rules.html"
    "delay-compensation-guide.html"
    "train-apps-comparison.html"
)

# Track issues
TOTAL_ISSUES=0

for lang in "${LANGS[@]}"; do
    echo ""
    echo "=========================================="
    echo "LANGUAGE: $lang"
    echo "=========================================="
    
    # Check main pages
    for page in "${PAGES[@]}"; do
        if [ "$lang" == "en" ]; then
            url="https://europe-train.com/${page}"
        else
            url="https://europe-train.com/${lang}/${page}"
        fi
        
        status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
        
        if [ "$status" == "200" ]; then
            # Check language attribute
            lang_attr=$(curl -s "$url" | grep -o 'lang="[^"]*"' | head -1)
            
            # Check for English content in non-EN pages
            if [ "$lang" != "en" ]; then
                # Check title
                title=$(curl -s "$url" | grep -o '<title>[^<]*</title>' | head -1)
                
                # Check for common English words in title
                if echo "$title" | grep -qi "travel\|guide\|train.*tips\|european.*train"; then
                    echo "  ⚠️  $page - English title detected: $title"
                    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
                else
                    echo "  ✅ $page (HTTP $status, lang=$lang_attr)"
                fi
            else
                echo "  ✅ $page (HTTP $status, lang=$lang_attr)"
            fi
        else
            echo "  ❌ $page (HTTP $status)"
            TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
        fi
    done
    
    # Check articles
    echo ""
    echo "  Articles:"
    for article in "${ARTICLES[@]}"; do
        if [ "$lang" == "en" ]; then
            url="https://europe-train.com/articles/${article}"
        else
            url="https://europe-train.com/${lang}/articles/${article}"
        fi
        
        status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
        
        if [ "$status" == "200" ]; then
            # Check language attribute
            lang_attr=$(curl -s "$url" | grep -o 'lang="[^"]*"' | head -1)
            
            # Check for English content in non-EN pages
            if [ "$lang" != "en" ]; then
                title=$(curl -s "$url" | grep -o '<title>[^<]*</title>' | head -1)
                
                # Check for common English words in title
                if echo "$title" | grep -qi "complete guide\|train guide\|travel guide"; then
                    echo "    ⚠️  $article - English title: ${title:0:80}..."
                    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
                else
                    echo "    ✅ ${article:0:40} (lang=$lang_attr)"
                fi
            else
                echo "    ✅ ${article:0:40} (lang=$lang_attr)"
            fi
        else
            echo "    ❌ $article (HTTP $status)"
            TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
        fi
    done
done

echo ""
echo "=========================================="
echo "AUDIT SUMMARY"
echo "=========================================="
echo "Total issues found: $TOTAL_ISSUES"

if [ $TOTAL_ISSUES -eq 0 ]; then
    echo "✅ All pages passed the audit!"
else
    echo "⚠️  $TOTAL_ISSUES issues need to be fixed"
fi
