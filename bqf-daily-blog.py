import datetime, hashlib, os, re

AFF_BASE = "https://www.floristone.com/main.cfm?source_id=aff&AffiliateID=21885"
BASE_URL = "https://brightlane.github.io/BouquetFlowers"
today = datetime.date.today()
date_str = str(today)
year = today.year
seed = int(hashlib.md5(date_str.encode()).hexdigest()[:8], 16)

cities = [
    "New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia",
    "San Antonio","San Diego","Dallas","San Jose","Austin","Seattle",
    "Denver","Nashville","Miami","Atlanta","Tampa","Minneapolis",
    "Toronto","Montreal","Vancouver","Calgary","Edmonton","Ottawa",
    "Winnipeg","Boston","Portland","Las Vegas","Baltimore","Washington DC",
]

occasions = [
    {"name":"Mother's Day","slug":"mothers-day","tag":"md"},
    {"name":"Birthday",    "slug":"birthday",   "tag":"bd"},
    {"name":"Anniversary", "slug":"anniversary","tag":"an"},
    {"name":"Sympathy",    "slug":"sympathy",   "tag":"sy"},
    {"name":"Get Well",    "slug":"get-well",   "tag":"gw"},
    {"name":"Romance",     "slug":"romance",    "tag":"ro"},
    {"name":"Thank You",   "slug":"thank-you",  "tag":"ty"},
    {"name":"New Baby",    "slug":"new-baby",   "tag":"nb"},
]

titles = [
    "Boutique {occ} Flowers in {city} — Same-Day Delivery {year}",
    "Luxury {occ} Bouquets Delivered to {city} — Free Same Day",
    "Best Boutique {occ} Flowers in {city} — No Hidden Fees",
    "Send Premium {occ} Flowers to {city} — Farm Fresh Today",
]

intros = [
    "Looking for luxury {occ} flowers in {city}? Floristone's boutique collection delivers farm-fresh premium bouquets same-day across {city} — free delivery, $0 service fees.",
    "Send stunning {occ} flowers to {city} today. Floristone crafts premium boutique arrangements from farm-fresh blooms and delivers same-day across {city} with free delivery.",
    "Discover Floristone's boutique {occ} flowers for {city}. Premium roses, peonies, orchids — delivered same-day with free delivery and $0 hidden fees. 4.8 stars from 18,742 customers.",
    "Premium {occ} flowers in {city} delivered same-day. Floristone's luxury boutique bouquets are crafted fresh daily and delivered free, with zero service fees.",
]

city     = cities[seed % len(cities)]
occasion = occasions[(seed // 7) % len(occasions)]
title_t  = titles[(seed // 13) % len(titles)]
intro_t  = intros[(seed // 17) % len(intros)]
title    = title_t.format(occ=occasion["name"], city=city, year=year)
intro    = intro_t.format(occ=occasion["name"].lower(), city=city)
aff_link = f"{AFF_BASE}&occ={occasion['tag']}"
city_slug = city.lower().replace(" ", "-")
filename  = f"blog-{city_slug}-{occasion['slug']}-{date_str}.html"

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | BouquetFlowers</title>
    <meta name="description" content="Send premium {occasion['name'].lower()} bouquets to {city}. Free same-day delivery, $0 service fees, from $29.99. 4.8 stars from 18,742 customers.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{BASE_URL}/{filename}">
    <script type="application/ld+json">
    {{"@context":"https://schema.org","@graph":[
      {{"@type":"Article","headline":"{title}","datePublished":"{date_str}","dateModified":"{date_str}","author":{{"@type":"Organization","name":"BouquetFlowers"}}}},
      {{"@type":"Product","name":"Floristone Boutique {occasion['name']} — {city}","offers":{{"@type":"Offer","priceCurrency":"USD","price":"29.99","availability":"https://schema.org/InStock","url":"{aff_link}","deliveryLeadTime":{{"@type":"QuantitativeValue","value":"0","unitCode":"DAY"}}}},"aggregateRating":{{"@type":"AggregateRating","ratingValue":"4.8","reviewCount":"18742"}}}}
    ]}}
    </script>
    <style>
        :root{{--rose:#b5204e;--rose-dk:#7e1235;--bg:#fdf8f3;--border:#f2e9de;--mid:#666;}}
        *{{box-sizing:border-box;margin:0;padding:0;}}
        body{{font-family:system-ui,sans-serif;background:var(--bg);color:#333;line-height:1.7;}}
        .nav{{background:#fff;padding:14px 5%;border-bottom:1px solid var(--border);font-weight:700;color:var(--rose-dk);display:flex;justify-content:space-between;align-items:center;font-family:'Playfair Display',Georgia,serif;}}
        .nav a{{font-size:0.85rem;color:var(--rose);text-decoration:none;font-family:system-ui,sans-serif;}}
        .article{{max-width:760px;margin:0 auto;padding:50px 24px 80px;}}
        .eyebrow{{font-size:0.75rem;font-weight:700;color:var(--rose);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px;display:block;}}
        h1{{font-size:clamp(1.8rem,4vw,2.5rem);color:#1a1a1a;margin-bottom:16px;line-height:1.2;font-family:'Playfair Display',Georgia,serif;}}
        .byline{{font-size:0.85rem;color:#999;margin-bottom:32px;border-bottom:1px solid var(--border);padding-bottom:16px;}}
        h2{{font-size:1.3rem;color:#1a1a1a;margin:32px 0 10px;font-family:'Playfair Display',Georgia,serif;}}
        p{{margin-bottom:16px;font-size:1rem;color:#444;}}
        .cta-box{{background:linear-gradient(135deg,#7e1235 0%,#b5204e 100%);color:#fff;text-align:center;padding:40px 24px;border-radius:16px;margin:40px 0;}}
        .cta-box h2{{color:#fff;margin:0 0 10px;font-size:1.5rem;}}
        .cta-box p{{color:rgba(255,255,255,0.88);margin-bottom:20px;}}
        .cta-btn{{background:#fff;color:var(--rose-dk);padding:14px 32px;border-radius:99px;font-weight:900;text-decoration:none;display:inline-block;font-size:1rem;}}
        .trust-row{{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-top:12px;}}
        .trust-row span{{font-size:0.75rem;color:rgba(255,255,255,0.8);font-weight:700;}}
        .faq-box{{background:#fff;border:1px solid var(--border);border-radius:12px;padding:24px;margin:32px 0;}}
        .faq-box strong{{display:block;color:#1a1a1a;margin-bottom:8px;}}
        .faq-box p{{margin:0;font-size:0.92rem;}}
        .back{{display:block;text-align:center;margin-top:32px;font-size:0.85rem;color:var(--rose);text-decoration:none;}}
        footer{{background:#1c1c1e;color:#888;text-align:center;padding:24px;font-size:0.78rem;}}
    </style>
</head>
<body>
<nav>Flori<em style="font-style:italic;color:var(--rose)">stone</em> Boutique <a href="{BASE_URL}/">← Back to home</a></nav>
<article class="article">
    <span class="eyebrow">{occasion['name']} · {city} · {date_str}</span>
    <h1>{title}</h1>
    <p class="byline">BouquetFlowers · Premium boutique delivery in {city} · {date_str}</p>
    <p>{intro}</p>
    <h2>Why Floristone is {city}'s top boutique flower delivery</h2>
    <p>4.8/5 stars from 18,742 verified customers. Free same-day delivery. $0 service fees. Local florists in {city} craft every arrangement from farm-fresh blooms cut on the day of delivery. Premium roses, peonies, orchids, and designer bouquets — all with live order tracking and a 100% freshness guarantee.</p>
    <h2>What to send for {occasion['name']} in {city}</h2>
    <p>Red roses from $49.99. Pink peonies from $29.99. Orchid towers from $129.99 — they last 4–8 weeks making them exceptional value. Wildflower baskets from $39.99. All delivered same-day in {city} with free delivery and $0 service fees included in the displayed price.</p>
    <div class="cta-box">
        <h2>Order Boutique {occasion['name']} Flowers to {city}</h2>
        <p>From $29.99 · Free delivery · $0 fees · 4.8★ from 18,742 customers</p>
        <a href="{aff_link}" class="cta-btn">🌸 Order Now →</a>
        <div class="trust-row">
            <span>✓ FREE DELIVERY</span><span>✓ $0 FEES</span><span>✓ FARM FRESH</span><span>✓ LIVE TRACKING</span>
        </div>
    </div>
    <div class="faq-box">
        <strong>Q: Can I get boutique {occasion['name'].lower()} flowers delivered same-day in {city}?</strong>
        <p>Yes. Floristone's local florist network in {city} guarantees same-day delivery with free delivery and $0 service fees. Order before the daily cutoff for same-day arrival. The price shown is the final price — no hidden charges.</p>
    </div>
    <a href="{BASE_URL}/" class="back">← Browse all boutique flowers</a>
</article>
<footer>This page contains affiliate links. We may earn a commission at no cost to you. © {year} BouquetFlowers</footer>
</body>
</html>"""

with open(filename, "w", encoding="utf-8") as f:
    f.write(html)

# Update sitemap
sitemap_entry = f'  <url><loc>{BASE_URL}/{filename}</loc><lastmod>{date_str}</lastmod><changefreq>never</changefreq><priority>0.7</priority></url>'
if os.path.exists("sitemap.xml"):
    with open("sitemap.xml", "r") as f:
        sm = f.read()
    if filename not in sm:
        sm = sm.replace("</urlset>", f"{sitemap_entry}\n</urlset>")
        with open("sitemap.xml", "w") as f:
            f.write(sm)

print(f"Generated: {filename}")
print(f"City: {city} | Occasion: {occasion['name']}")
print(f"Affiliate ID: 21885 ✓")
