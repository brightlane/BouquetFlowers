#!/usr/bin/env python3
"""
generate_sitemap.py — BouquetFlowers
Run from repo root: python3 generate_sitemap.py
Crawls all HTML files, builds sitemap.xml, pings search engines.
"""
import os
import glob
import datetime
import urllib.request
import json

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
BASE_URL     = "https://brightlane.github.io/BouquetFlowers"
SITEMAP_PATH = "sitemap.xml"
TODAY        = datetime.date.today().isoformat()
INDEXNOW_KEY = "3dd8ef03a39841008c6f5fe0c38144d5"

# Priority rules by path pattern
PRIORITY_MAP = [
    ("index.html",   "1.0",  "daily"),
    ("blog.html",    "0.9",  "daily"),
    ("404.html",     "0.1",  "monthly"),
    ("/bing/",       "0.8",  "weekly"),
    ("/bing-fr/",    "0.8",  "weekly"),
    ("/bing-es/",    "0.8",  "weekly"),
    ("/bing-zh/",    "0.8",  "weekly"),
    ("/bing-ru/",    "0.8",  "weekly"),
    ("/blog/",       "0.7",  "weekly"),
    ("/delivery/",   "0.7",  "weekly"),
    ("/daily/",      "0.6",  "daily"),
]

def get_priority(path):
    path = path.replace("\\", "/")
    for pattern, priority, freq in PRIORITY_MAP:
        if pattern in path:
            return priority, freq
    return "0.7", "weekly"

# ─────────────────────────────────────────────
# COLLECT ALL HTML FILES
# ─────────────────────────────────────────────
html_files = glob.glob("**/*.html", recursive=True)
html_files = [f for f in html_files if "node_modules" not in f]
html_files.sort()

urls = []
for f in html_files:
    # Convert local path to URL
    url_path = f.replace("\\", "/")
    if url_path == "index.html":
        url = BASE_URL + "/"
    else:
        url = BASE_URL + "/" + url_path
    priority, freq = get_priority(url_path)
    urls.append((url, priority, freq))

# ─────────────────────────────────────────────
# BUILD SITEMAP XML
# ─────────────────────────────────────────────
lines = ['<?xml version="1.0" encoding="UTF-8"?>']
lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
lines.append('        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
lines.append('        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9')
lines.append('          http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">')

for url, priority, freq in urls:
    lines.append(f'  <url>')
    lines.append(f'    <loc>{url}</loc>')
    lines.append(f'    <lastmod>{TODAY}</lastmod>')
    lines.append(f'    <changefreq>{freq}</changefreq>')
    lines.append(f'    <priority>{priority}</priority>')
    lines.append(f'  </url>')

lines.append('</urlset>')

sitemap_content = "\n".join(lines)
with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
    f.write(sitemap_content)

print(f"✅ sitemap.xml generated — {len(urls)} URLs")

# ─────────────────────────────────────────────
# UPDATE ROBOTS.TXT WITH SITEMAP REFERENCE
# ─────────────────────────────────────────────
robots_path = "robots.txt"
sitemap_line = f"Sitemap: {BASE_URL}/sitemap.xml"

if os.path.exists(robots_path):
    with open(robots_path, "r") as f:
        robots = f.read()
    if "Sitemap:" not in robots:
        with open(robots_path, "a") as f:
            f.write(f"\n{sitemap_line}\n")
        print(f"✅ robots.txt updated with sitemap reference")
    else:
        # Update existing sitemap line
        import re
        robots = re.sub(r'Sitemap:.*', sitemap_line, robots)
        with open(robots_path, "w") as f:
            f.write(robots)
        print(f"✅ robots.txt sitemap line refreshed")
else:
    with open(robots_path, "w") as f:
        f.write(f"User-agent: *\nAllow: /\n{sitemap_line}\n")
    print(f"✅ robots.txt created")

# ─────────────────────────────────────────────
# PING SEARCH ENGINES
# ─────────────────────────────────────────────
sitemap_url = f"{BASE_URL}/sitemap.xml"
ping_urls = [
    f"https://www.google.com/ping?sitemap={sitemap_url}",
    f"https://www.bing.com/ping?sitemap={sitemap_url}",
]

for ping in ping_urls:
    try:
        with urllib.request.urlopen(ping, timeout=10) as r:
            engine = "Google" if "google" in ping else "Bing"
            print(f"✅ {engine} pinged — HTTP {r.status}")
    except Exception as e:
        print(f"   Ping note: {e}")

# ─────────────────────────────────────────────
# INDEXNOW
# ─────────────────────────────────────────────
all_url_list = [u for u, _, _ in urls]
payload = json.dumps({
    "host": "brightlane.github.io",
    "key": INDEXNOW_KEY,
    "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
    "urlList": all_url_list[:10000]
}).encode("utf-8")

try:
    req = urllib.request.Request(
        "https://api.indexnow.org/IndexNow",
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        print(f"✅ IndexNow — HTTP {resp.status} — {len(all_url_list)} URLs submitted")
except Exception as e:
    print(f"   IndexNow note: {e}")

print(f"\n📄 Sitemap: {sitemap_url}")
print(f"   Total URLs indexed: {len(urls)}")
