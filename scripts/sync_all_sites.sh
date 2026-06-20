#!/bin/bash
# Sync articles index to all language sites with proper localization

cd /root/.openclaw/workspace/europe-train

LANGS=("de" "fr" "es" "ja" "ko" "pt")

# For each language, copy EN index and update paths
for lang in "${LANGS[@]}"; do
    echo "Processing ${lang}..."
    
    # Copy EN index as base
    cp articles/index.html ${lang}/articles/index.html
    
    # Update language attribute
    sed -i "s/lang=\"en\"/lang=\"${lang}\"/g" ${lang}/articles/index.html
    
    # Update navigation links to include language prefix
    sed -i "s|href=\"/\"|href=\"/${lang}/\"|g" ${lang}/articles/index.html
    sed -i "s|href=\"/articles/\"|href=\"/${lang}/articles/\"|g" ${lang}/articles/index.html
    sed -i "s|href=\"/routes.html\"|href=\"/${lang}/routes.html\"|g" ${lang}/articles/index.html
    sed -i "s|href=\"/tickets.html\"|href=\"/${lang}/tickets.html\"|g" ${lang}/articles/index.html
    sed -i "s|href=\"/passes.html\"|href=\"/${lang}/passes.html\"|g" ${lang}/articles/index.html
    sed -i "s|href=\"/live-status.html\"|href=\"/${lang}/live-status.html\"|g" ${lang}/articles/index.html
    
    # Update lang switcher - remove active from EN, add to current lang
    sed -i 's|href="/" class="active"|href="/"|g' ${lang}/articles/index.html
    sed -i "s|href=\"/${lang}/\"|href=\"/${lang}/\" class=\"active\"|g" ${lang}/articles/index.html
    
    echo "✅ ${lang}/articles/index.html updated"
done

echo ""
echo "All language sites synced!"
