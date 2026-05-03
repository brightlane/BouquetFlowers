"""
Run this once in your BouquetFlowers repo root:
    python3 bqf-fix-index.py
Fixes index.html in place — all issues corrected automatically.
"""
import re, os

# ─────────────────────────────────────────────
# CORRECT AFFILIATE URL — DO NOT CHANGE
# ─────────────────────────────────────────────
AFF_URL = "https://www.floristone.com/main.cfm?cat=r&source_id=aff&AffiliateID=2013017799"

if not os.path.exists('index.html'):
    print("ERROR: index.html not found. Run from repo root.")
    exit(1)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()
original = content

# 1. Fix any wrong affiliate IDs (21885 → 2013017799)
content = content.replace('AffiliateID=21885', 'AffiliateID=2013017799')

# 2. Fix http:// → https:// on floristone URLs
content = content.replace('http://www.floristone.com', 'https://www.floristone.com')

# 3. Remove &occ= tags from all affiliate URLs
content = re.sub(r'(https://www\.floristone\.com/main\.cfm\?[^"\']*?)&occ=[a-z]+', r'\1', content)

# 4. Fix wrong endpoint (index.cfm → main.cfm)
content = content.replace('floristone.com/index.cfm', 'floristone.com/main.cfm')

# 5. Ensure cat=r is in all affiliate links
def fix_affiliate_url(m):
    url = m.group(0)
    if 'cat=r' not in url and 'AffiliateID=2013017799' in url:
        url = url.replace('?source_id=', '?cat=r&source_id=')
    return url
content = re.sub(r'https://www\.floristone\.com/main\.cfm\?[^"\'<\s]+', fix_affiliate_url, content)

# 6. Fix canonical
content = re.sub(
    r'<link rel="canonical" href="https://www\.floristone\.com[^"]*"',
    '<link rel="canonical" href="https://brightlane.github.io/BouquetFlowers/"',
    content
)

# 7. Fix og:url
content = re.sub(
    r'<meta property="og:url" content="https://www\.floristone\.com[^"]*"',
    '<meta property="og:url" content="https://brightlane.github.io/BouquetFlowers/"',
    content
)

# 8. Fix review count if old value present
content = content.replace('12,400+', '18,742+')
content = content.replace('12,400', '18,742')
content = content.replace('"reviewCount": "12400"', '"reviewCount": "18742"')

# 9. Fix hardcoded copyright year → auto-year
content = re.sub(
    r'© 20\d\d (BouquetFlowers|Floristone)',
    r'© <span id="yr-bqf"></span> \1',
    content
)
if 'yr-bqf' in content and 'getElementById("yr-bqf")' not in content:
    content = content.replace(
        '</body>',
        '<script>document.getElementById("yr-bqf").textContent=new Date().getFullYear();</script>\n</body>'
    )

# 10. Add llms.txt + sitemap links to footer if missing
if 'llms.txt' not in content:
    content = content.replace(
        '</footer>',
        '<p style="text-align:center;font-size:11px;margin-top:8px;">'
        '<a href="https://brightlane.github.io/BouquetFlowers/llms.txt" style="color:rgba(255,255,255,0.3);">llms.txt</a> · '
        '<a href="https://brightlane.github.io/BouquetFlowers/sitemap.xml" style="color:rgba(255,255,255,0.3);">Sitemap</a>'
        '</p></footer>'
    )

# 11. Add evergreen countdown bar if missing
if 'mday-bar' not in content:
    countdown = f'''<div id="mday-bar" style="background:#b5204e;color:#fff;text-align:center;padding:10px 16px;font-size:0.88rem;font-weight:700;">
    🌸 Mother\'s Day is coming — <a href="{AFF_URL}" style="color:white;text-decoration:underline;">Order Boutique Flowers — Same-Day Delivery</a>
</div>
<script>
(function(){{
  var el=document.getElementById("mday-bar");
  function getNextMD(){{
    var y=new Date().getFullYear();
    function md(yr){{var d=new Date(yr,4,1);var day=d.getDay();var fs=(6-day)%7+1;return new Date(yr,4,fs+7);}}
    var t=md(y); if(new Date()>t)t=md(y+1); return t;
  }}
  var target=getNextMD();
  function update(){{
    var diff=target-new Date();
    if(diff<=0)return;
    var days=Math.floor(diff/86400000);
    var hrs=Math.floor((diff%86400000)/3600000);
    var mins=Math.floor((diff%3600000)/60000);
    var txt=days>1?"Only "+days+" days until Mother\'s Day":days===1?"Mother\'s Day is TOMORROW":(hrs+"h "+mins+"m until Mother\'s Day");
    el.innerHTML="🌸 "+txt+" — <a href=\'{AFF_URL}\' style=\'color:white;text-decoration:underline;\'>Order Boutique Flowers</a>";
  }}
  update(); setInterval(update,60000);
}})();
</script>
'''
    content = content.replace('<body>', '<body>\n' + countdown, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Report
wrong_id = original.count('AffiliateID=21885')
occ_tags = len(re.findall(r'&occ=[a-z]+', original))
http_count = original.count('http://www.floristone.com')

print(f"✅ index.html fixed!")
print(f"   Wrong IDs fixed (21885 → 2013017799): {wrong_id}")
print(f"   http:// → https:// fixes: {http_count}")
print(f"   &occ= tags removed: {occ_tags}")
print(f"   Affiliate URL: {AFF_URL}")
