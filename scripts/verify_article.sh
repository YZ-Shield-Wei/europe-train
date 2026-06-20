#!/bin/bash
# Post-publish verification script for europe-train articles

ARTICLE_SLUG="berlin-to-munich-train-guide"
LANGUAGES=("" "de/" "fr/" "es/" "ja/" "ko/" "pt/" "zh/")

echo "=========================================="
echo "Article Publish Verification"
echo "=========================================="
echo ""

all_passed=true

for lang in "${LANGUAGES[@]}"; do
    url="https://europe-train.com/${lang}articles/${ARTICLE_SLUG}.html"
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    
    if [ "$status" == "200" ]; then
        echo "✅ ${url}"
    else
        echo "❌ ${status}: ${url}"
        all_passed=false
    fi
done

echo ""
if [ "$all_passed" = true ]; then
    echo "✅ All URLs verified successfully!"
    exit 0
else
    echo "❌ Some URLs failed verification!"
    exit 1
fi