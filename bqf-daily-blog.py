#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bqf-daily-blog.py -- BouquetFlowers daily blog updater
Run from repo root: python3 bqf-daily-blog.py
Reads blog.html from disk and writes it back with today's date.
Never hardcodes HTML inside Python -- avoids all encoding issues.
"""
import os
import re
import datetime

# ─────────────────────────────────────────────
# CONFIG -- DO NOT CHANGE AFFILIATE URL
# ─────────────────────────────────────────────
AFF_URL   = "https://www.floristone.com/main.cfm?cat=r&source_id=aff&AffiliateID=2013017799"
BASE_URL  = "https://brightlane.github.io/BouquetFlowers"
TODAY     = datetime.date.today().isoformat()
YEAR      = datetime.date.today().year

# ─────────────────────────────────────────────
# READ blog.html
# ─────────────────────────────────────────────
blog_path = "blog.html"
if not os.path.exists(blog_path):
    print(f"ERROR: {blog_path} not found. Run from repo root.")
    exit(1)

with open(blog_path, "r", encoding="utf-8") as f:
    content = f.read()

original = content

# ─────────────────────────────────────────────
# FIXES
# ─────────────────────────────────────────────

# 1. Fix any wrong affiliate IDs
content = content.replace("AffiliateID=21885", "AffiliateID=2013017799")

# 2. Fix http -> https
content = content.replace("http://www.floristone.com", "https://www.floristone.com")

# 3. Remove &occ= tags
content = re.sub(
    r"(https://www\.floristone\.com/main\.cfm\?[^\"'<\s]*?)&occ=[a-z]+",
    r"\1",
    content
)

# 4. Fix missing cat=r
def fix_cat(m):
    url = m.group(0)
    if "cat=r" not in url and "AffiliateID=2013017799" in url:
        url = url.replace("?source_id=", "?cat=r&source_id=")
    return url
content = re.sub(
    r"https://www\.floristone\.com/main\.cfm\?[^\"'<\s]+",
    fix_cat,
    content
)

# 5. Update lastmod date in schema if present
content = re.sub(r'"dateModified"\s*:\s*"\d{4}-\d{2}-\d{2}"', f'"dateModified": "{TODAY}"', content)

# ─────────────────────────────────────────────
# WRITE BACK
# ─────────────────────────────────────────────
if content != original:
    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ blog.html updated — {TODAY}")
else:
    print(f"✅ blog.html already clean — no changes needed")

print(f"   Affiliate URL: {AFF_URL}")
print(f"   Base URL: {BASE_URL}")
