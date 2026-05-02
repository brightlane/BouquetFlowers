#!/usr/bin/env python3
"""
Fix wrong affiliate ID across all HTML files in the repo.
Run from the root of your BouquetFlowers repo:
    python fix_affiliate.py
"""

import os
import glob

REPLACEMENTS = [
    ("AffiliateID=21885",          "AffiliateID=2013017799"),
    ("https://www.floristone.com", "http://www.floristone.com"),
    ("https://floristone.com",     "http://www.floristone.com"),
    ("http://floristone.com",      "http://www.floristone.com"),
]

fixed = []
skipped = []

html_files = glob.glob("**/*.html", recursive=True)

for path in html_files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        fixed.append(path)
    else:
        skipped.append(path)

print(f"\n✅ Fixed {len(fixed)} files:")
for p in fixed:
    print(f"   {p}")

print(f"\n⏭️  Skipped {len(skipped)} files (already correct or no match):")
for p in skipped:
    print(f"   {p}")
