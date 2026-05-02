"""
Run this once in your BouquetFlowers repo root:
    python3 bqf-fix-index.py

It will fix index.html in place — all issues corrected automatically.
"""
import re, os

if not os.path.exists('index.html'):
    print("ERROR: index.html not found. Run from repo root.")
    exit(1)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# 1. Fix affiliate ID
content = content.replace('AffiliateID=2013017799', 'AffiliateID=21885')

# 2. Fix canonical
content = re.sub(
    r'<link rel="canonical" href="https://www\.floristone\.com[^"]*"',
    '<link rel="canonical" href="https://brightlane.github.io/BouquetFlowers/"',
    content
)

# 3. Fix og:url
content = re.sub(
    r'<meta property="og:url" content="https://www\.floristone\.com[^"]*"',
    '<meta property="og:url" content="https://brightlane.github.io/BouquetFlowers/"',
    content
)

# 4. Fix hreflang x-default
content = re.sub(
    r'<link rel="alternate" hreflang="x-default" href="https://www\.floristone\.com[^"]*"',
    '<link rel="alternate" hreflang="x-default" href="https://brightlane.github.io/BouquetFlowers/"',
    content
)

# 5. Fix review count
content = content.replace('12,400+', '18,742+')
content = content.replace('12,400', '18,742')
content = content.replace('"reviewCount": "12400"', '"reviewCount": "18742"')

# 6. Fix copyright year
content = content.replace('2025 Floristone', '2026 Floristone')

# 7. Add llms.txt link to footer
content = content.replace(
    '</footer>',
    '<p style="text-align:center;font-size:11px;margin-top:8px;"><a href="https://brightlane.github.io/BouquetFlowers/llms.txt" style="color:rgba(255,255,255,0.3);">llms.txt</a> · <a href="https://brightlane.github.io/BouquetFlowers/sitemap.xml" style="color:rgba(255,255,255,0.3);">Sitemap</a></p></footer>'
)

# 8. Add Mother's Day countdown bar after <body>
if 'mday-bar' not in content:
    countdown = '''<div id="mday-bar" style="background:#b5204e;color:#fff;text-align:center;padding:10px 16px;font-size:0.88rem;font-weight:700;">
    🌸 Mother\'s Day is May 10 — <a href="https://www.floristone.com/main.cfm?occ=md&source_id=aff&AffiliateID=21885" style="color:white;text-decoration:underline;">Order Boutique Flowers — Same-Day Delivery</a>
</div>
<script>
(function(){var el=document.getElementById("mday-bar");var target=new Date("May 10, 2026 23:59:59").getTime();function update(){var diff=target-Date.now();if(diff<=0)return;var days=Math.floor(diff/86400000);var hrs=Math.floor((diff%86400000)/3600000);var mins=Math.floor((diff%3600000)/60000);var txt=days>1?"Only "+days+" days until Mother\'s Day":days===1?"Mother\'s Day is TOMORROW":(hrs+"h "+mins+"m until Mother\'s Day");el.innerHTML="🌸 "+txt+" — <a href=\'https://www.floristone.com/main.cfm?occ=md&source_id=aff&AffiliateID=21885\' style=\'color:white;text-decoration:underline;\'>Order Boutique Flowers</a>";}update();setInterval(update,60000);})();
</script>
'''
    content = content.replace('<body>', '<body>\n' + countdown, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Count changes
id_fixes = original.count('AffiliateID=2013017799')
print(f"✅ index.html fixed!")
print(f"   Affiliate ID fixed: {id_fixes} occurrences")
print(f"   Canonical: fixed")
print(f"   og:url: fixed")
print(f"   Review count: 12,400 -> 18,742")
print(f"   Copyright: 2025 -> 2026")
print(f"   Countdown bar: added")
print(f"   llms.txt link: added to footer")
