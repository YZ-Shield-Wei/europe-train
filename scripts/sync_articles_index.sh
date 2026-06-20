#!/bin/bash
# Sync articles index to all language sites

cd /root/.openclaw/workspace/europe-train

# Define languages
LANGS=("de" "fr" "es" "ja" "ko" "pt" "zh")

# Copy EN index as base template
cp articles/index.html /tmp/articles_index_template.html

for lang in "${LANGS[@]}"; do
    echo "Syncing ${lang}/articles/index.html..."
    
    # Create directory if not exists
    mkdir -p ${lang}/articles
    
    # Copy template
    cp /tmp/articles_index_template.html ${lang}/articles/index.html
    
    # Update language-specific paths and text
    sed -i "s|lang=\"en\"|lang=\"${lang}\"|g" ${lang}/articles/index.html
    sed -i "s|href=\"/\"|href=\"/${lang}/\"|g" ${lang}/articles/index.html
    sed -i "s|href=\"/articles/\"|href=\"/${lang}/articles/\"|g" ${lang}/articles/index.html
    sed -i "s|href=\"/routes.html\"|href=\"/${lang}/routes.html\"|g" ${lang}/articles/index.html
    sed -i "s|href=\"/tickets.html\"|href=\"/${lang}/tickets.html\"|g" ${lang}/articles/index.html
    sed -i "s|href=\"/passes.html\"|href=\"/${lang}/passes.html\"|g" ${lang}/articles/index.html
    sed -i "s|href=\"/live-status.html\"|href=\"/${lang}/live-status.html\"|g" ${lang}/articles/index.html
    
    # Update lang switcher active state
    sed -i "s|href=\"/\" class=\"active\"|href=\"/\"|g" ${lang}/articles/index.html
    sed -i "s|href=\"/${lang}/\"|href=\"/${lang}/\" class=\"active\"|g" ${lang}/articles/index.html
    
    echo "✅ ${lang}/articles/index.html updated"
done

echo ""
echo "All language sites synced!"