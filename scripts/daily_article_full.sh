#!/bin/bash
# Europe Train Daily Article - Full Automation
# Generate article + translate + push to GitHub

set -e

LOG_FILE="/tmp/europe-train-daily.log"
WORK_DIR="/root/.openclaw/workspace/europe-train"
DATE=$(date +%Y%m%d)

echo "========================================" >> $LOG_FILE
echo "🚄 Europe Train Daily Article - $DATE" >> $LOG_FILE
echo "Start: $(date)" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

cd $WORK_DIR

# Step 1: Generate article
echo "📝 Step 1: Generating article..." >> $LOG_FILE
python3 scripts/generate_daily_article.py >> $LOG_FILE 2>&1

# Step 2: Sync to all language sites
echo "🌐 Step 2: Syncing articles..." >> $LOG_FILE
bash scripts/sync_articles_index.sh >> $LOG_FILE 2>&1

# Step 3: Translate content
echo "🔄 Step 3: Translating..." >> $LOG_FILE
python3 scripts/translate_article_content.py >> $LOG_FILE 2>&1 || true

# Step 4: Git commit and push
echo "📤 Step 4: Pushing to GitHub..." >> $LOG_FILE
git add -A
git commit -m "Daily article: $DATE" >> $LOG_FILE 2>&1 || true
git push origin main >> $LOG_FILE 2>&1 || echo "Push failed, will retry later" >> $LOG_FILE

echo "✅ Completed: $(date)" >> $LOG_FILE
echo "" >> $LOG_FILE
