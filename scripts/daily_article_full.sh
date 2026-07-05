#!/bin/bash
# Europe Train Daily Article - Manual Article Sync & Push
# 
# Workflow:
# 1. User manually writes article in en/articles/
# 2. This script runs daily at 5 AM to:
#    - Sync article to all language sites
#    - Translate content
#    - Push to GitHub via API (avoids SIGKILL)
#
# NOTE: Does NOT auto-generate articles. Only syncs/pushes manual content.

set -e

LOG_FILE="/tmp/europe-train-daily.log"
WORK_DIR="/root/.openclaw/workspace/europe-train"
DATE=$(date +%Y%m%d)

echo "========================================" >> $LOG_FILE
echo "🚄 Europe Train Daily Sync & Push - $DATE" >> $LOG_FILE
echo "Start: $(date)" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

cd $WORK_DIR

# Step 1: Sync to all language sites
echo "🌐 Step 1: Syncing articles to all languages..." >> $LOG_FILE
bash scripts/sync_articles_index.sh >> $LOG_FILE 2>&1 || true

# Step 2: Translate content
echo "🔄 Step 2: Translating content..." >> $LOG_FILE
python3 scripts/translate_article_content.py >> $LOG_FILE 2>&1 || true

# Step 3: Push using GitHub API (avoids SIGKILL)
echo "📤 Step 3: Pushing to GitHub via API..." >> $LOG_FILE
python3 scripts/push_all_articles_api.py >> $LOG_FILE 2>&1

echo "✅ Completed: $(date)" >> $LOG_FILE
echo "" >> $LOG_FILE
