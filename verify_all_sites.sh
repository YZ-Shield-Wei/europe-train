#!/bin/bash
echo "=========================================="
echo "Verifying all sites articles count"
echo "=========================================="
echo ""

for lang in "" "de/" "fr/" "es/" "ja/" "ko/" "pt/" "zh/"; do
    url="https://europe-train.com/${lang}articles/"
    count=$(curl -s "$url" | grep -c 'article-card' 2>/dev/null)
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    echo "${lang:-en}: ${count} articles (HTTP ${status})"
done
