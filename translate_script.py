#!/usr/bin/env python3
"""
翻译 europe-train.com zh/articles 目录下所有HTML文件中的英文段落
"""

import os
import re
import glob

# 文件列表
articles_dir = "/root/.openclaw/workspace/europe-train/zh/articles"
files = sorted(glob.glob(os.path.join(articles_dir, "*.html")))

print(f"找到 {len(files)} 个HTML文件")
for f in files:
    print(f"  - {os.path.basename(f)}")
