#!/usr/bin/env python3
"""
Fix wrong affiliate IDs and URLs across all HTML and Python files.
Run from the root of your BouquetFlowers repo:
    python3 update_affiliate_links.py
"""
import os
import re
import glob

# ─────────────────────────────────────────────
# CORRECT AFFILIATE URL — DO NOT CHANGE
# ─────────────────────────────────────────────
CORRECT_URL = "https://www.floristone.com/main.cfm?cat=r&source_id=aff&AffiliateID=2013017799"

REPLACEMENTS = [
    # Fix wrong affiliate ID
    ("AffiliateID=21885",           "AffiliateID=2013017799"),
    # Fix http:// → https://
    ("http://www.floristone.com",   "https://www.floristone.com"),
    ("http://floristone.com",       "https://www.floristone.com"),
    ("https://floristone.com",      "https://www.floristone.com"),
    # Fix wrong endpoint
    ("floristone.com/index.cfm",    "floristone.com/main.cfm"),
]

def fix_occ_tags(content):
    """Remove &occ=xx tags from affiliate URLs"""
    return re.sub(
        r'(https://www\.floristone\.com/main\.cfm\?[^"\'<\s]*?)&occ=[a-z]+',
        r'\1',
        content
    )

def fix_missing_cat(content):
    """Ensure cat=r is present in affiliate URLs"""
    def add_cat(m):
        url = m.group(0)
        if 'cat=r' not in url and 'AffiliateID=2013017799' in url:
            url = url.replace('?source_id=', '?cat=r&source_id=')
        return url
    return re.sub(r'https://www\.floristone\.com/main\.cfm\?[^"\'<\s]+', add_cat, content)

fixed = []
skipped = []

extensions = ["**/*.html", "**/*.py", "**/*.js", "**/*.json", "**/*.txt", "**/*.yml"]
all_files = []
for pattern in extensions:
    all_files.extend(glob.glob(pattern, recursive=True))

# Skip node_modules
all_files = [f for f in all_files if 'node_modules' not in f]

for path in all_files:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        skipped.append(path)
        continue

    original = content

    # Apply simple replacements
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)

    # Remove &occ= tags
    content = fix_occ_tags(content)

    # Ensure cat=r present
    content = fix_missing_cat(content)

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        fixed.append(path)
    else:
        skipped.append(path)

print(f"\n✅ Fixed {len(fixed)} files:")
for p in fixed:
    print(f"   {p}")
print(f"\n⏭️  Skipped {len(skipped)} files (already correct or no match)")
print(f"\n   Correct affiliate URL: {CORRECT_URL}")
