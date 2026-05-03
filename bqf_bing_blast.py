import os
import json
import hashlib
import urllib.request
from datetime import datetime

# ─────────────────────────────────────────────
# 1. CONFIG — DO NOT CHANGE AFFILIATE URL
# ─────────────────────────────────────────────
AFF_URL  = "https://www.floristone.com/main.cfm?cat=r&source_id=aff&AffiliateID=2013017799"
BASE_URL = "https://brightlane.github.io/BouquetFlowers"
TODAY    = datetime.now().strftime("%Y-%m-%d")
YEAR     = datetime.now().strftime("%Y")
seed     = int(hashlib.md5(TODAY.encode()).hexdigest()[:8], 16)
INDEXNOW_KEY = "3dd8ef03a39841008c6f5fe0c38144d5"

# ─────────────────────────────────────────────
# 2. CROSS-LINKS
# ─────────────────────────────────────────────
RELATED_SITES = [
    ("Send Flowers Online",     "https://brightlane.github.io/SendFlowersOnline/"),
    ("Mother's Day Flowers",    "https://brightlane.github.io/MothersDayFlowers/"),
    ("Valentine's Day Flowers", "https://brightlane.github.io/ValentinesDayFlowers/"),
    ("FTD Flowers",             "https://brightlane.github.io/FtdFlowers/"),
    ("Same Day Flowers",        "https://brightlane.github.io/SameDayFlowers/"),
    ("Christmas Flowers",       "https://brightlane.github.io/ChristmasFlowers/"),
    ("Flower Delivery",         "https://brightlane.github.io/FlowerDelivery/"),
    ("Same Day Florist",        "https://brightlane.github.io/SameDayFlorist/"),
]
RELATED_HTML = " &nbsp;|&nbsp; ".join(
    f'<a href="{url}">{name}</a>' for name, url in RELATED_SITES
)

# ─────────────────────────────────────────────
# 3. 1500 CITIES USA + CANADA
# ─────────────────────────────────────────────
ALL_CITIES = list(dict.fromkeys([
    "New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia",
    "San Antonio","San Diego","Dallas","San Jose","Austin","Jacksonville",
    "Fort Worth","Columbus","Charlotte","San Francisco","Indianapolis","Seattle",
    "Denver","Nashville","Oklahoma City","El Paso","Washington DC","Las Vegas",
    "Louisville","Memphis","Portland","Baltimore","Milwaukee","Albuquerque",
    "Tucson","Fresno","Sacramento","Mesa","Kansas City","Atlanta","Omaha",
    "Colorado Springs","Raleigh","Long Beach","Virginia Beach","Minneapolis",
    "Tampa","New Orleans","Arlington","Bakersfield","Honolulu","Anaheim",
    "Aurora","Santa Ana","Corpus Christi","Riverside","St Louis","Lexington",
    "Pittsburgh","Stockton","Anchorage","Cincinnati","St Paul","Greensboro",
    "Toledo","Newark","Plano","Henderson","Orlando","Lincoln","Jersey City",
    "Chandler","Fort Wayne","St Petersburg","Laredo","Norfolk","Madison",
    "Durham","Lubbock","Winston Salem","Garland","Glendale","Hialeah","Reno",
    "Baton Rouge","Irvine","Chesapeake","Irving","Scottsdale","North Las Vegas",
    "Fremont","Gilbert","San Bernardino","Boise","Birmingham","Rochester",
    "Richmond","Spokane","Des Moines","Montgomery","Modesto","Fayetteville",
    "Tacoma","Shreveport","Fontana","Moreno Valley","Akron","Yonkers",
    "Augusta","Little Rock","Grand Rapids","Huntington Beach","Salt Lake City",
    "Tallahassee","Huntsville","Worcester","Knoxville","Providence","Brownsville",
    "Santa Clarita","Garden Grove","Oceanside","Fort Lauderdale","Chattanooga",
    "Tempe","Cape Coral","Eugene","Rancho Cucamonga","Peoria","Ontario",
    "Salem","Elk Grove","Corona","Springfield","Fort Collins","Jackson",
    "Alexandria","Hayward","Lakewood","Clarksville","Lancaster","Salinas",
    "Palmdale","Sunnyvale","Pomona","Escondido","Surprise","Pasadena",
    "Torrance","Rockford","Paterson","Joliet","Savannah","Bridgeport","Syracuse",
    "McAllen","Hollywood","Macon","Mesquite","Dayton","Metairie","Cary",
    "Orange","Fullerton","Hampton","Murfreesboro","Killeen","Warren",
    "West Valley City","Columbia","Sterling Heights","New Haven","Olathe",
    "Miramar","Cedar Rapids","Charleston","Thousand Oaks","Visalia","Elizabeth",
    "Gainesville","Waco","Roseville","Sioux Falls","Hartford","Coral Springs",
    "Stamford","Topeka","Bellevue","Denton","Victorville","Beaumont","Midland",
    "Elgin","Lansing","West Palm Beach","Clearwater","Manchester","Arvada",
    "Costa Mesa","Pueblo","Downey","Inglewood","Carlsbad","Pompano Beach",
    "Berkeley","Westminster","Cambridge","Provo","Miami Gardens","Palm Bay",
    "Wichita","Murrieta","Temecula","El Monte","West Covina","Burbank",
    "Simi Valley","Vallejo","Fairfield","Santa Rosa","Hesperia","Chino",
    "Chino Hills","Menifee","Jurupa Valley","Daly City","San Mateo",
    "Santa Clara","Mountain View","Redding","Santa Barbara","Ventura","Oxnard",
    "Hawthorne","Compton","Carson","Whittier","Culver City","Alhambra",
    "El Cajon","Vista","San Marcos","Santee","National City","Poway","La Mesa",
    "Tuscaloosa","Dothan","Auburn AL","Decatur AL","Florence AL","Gadsden",
    "Hoover","Goodyear","Avondale","Buckeye","Casa Grande","Maricopa",
    "Lake Havasu City","Prescott","Conway","Jonesboro","North Little Rock",
    "Springdale","Rogers","Fort Smith","Pine Bluff","Hot Springs","Bentonville",
    "Boulder","Highlands Ranch","Longmont","Loveland","Broomfield","New Britain",
    "Meriden","West Haven","Danbury","Stratford","Milford","Hamden",
    "Wilmington DE","Dover DE","Newark DE","Middletown DE","Lakeland",
    "Deerfield Beach","Boca Raton","Davie","Plantation","Sunrise","Weston",
    "Boynton Beach","Delray Beach","Melbourne FL","Daytona Beach","Deltona",
    "Kissimmee","Sandy Springs","Johns Creek","Alpharetta","Warner Robins",
    "Peachtree City","Smyrna GA","Nampa","Idaho Falls","Pocatello","Caldwell",
    "Bloomington IL","Decatur IL","Waukegan","Cicero","Evanston","Schaumburg",
    "Bolingbrook","Naperville","Carmel IN","Fishers","Hammond","Gary","Muncie",
    "Terre Haute","Bloomington IN","Anderson","Elkhart","Kokomo","Davenport",
    "Cedar Falls","Iowa City","Waterloo","Ames","Council Bluffs","Dubuque",
    "Sioux City","Manhattan KS","Salina","Hutchinson","Leavenworth","Shawnee",
    "Overland Park","Lawrence KS","Bowling Green KY","Covington KY",
    "Richmond KY","Hopkinsville","Owensboro","Lafayette LA","Lake Charles",
    "Monroe LA","Bossier City","Kenner","New Iberia","Portland ME","Lewiston",
    "Bangor","Auburn ME","Biddeford","Frederick MD","Rockville","Gaithersburg",
    "Hagerstown","Annapolis","Lowell","Brockton","New Bedford","Lynn","Quincy",
    "Fall River","Newton MA","Somerville","Lawrence MA","Springfield MA",
    "Flint","Kalamazoo","Dearborn","Livonia","Clinton Township","Canton MI",
    "Westland","Troy MI","Farmington Hills","Southfield","Duluth",
    "Bloomington MN","Brooklyn Park","Plymouth MN","St Cloud","Eagan",
    "Coon Rapids","Burnsville","Blaine","Lakeville","Gulfport","Southaven",
    "Hattiesburg","Biloxi","Meridian MS","St Joseph","St Charles","Blue Springs",
    "Florissant","Independence MO","Billings","Missoula","Great Falls","Bozeman",
    "Butte","Helena MT","Fargo","Bismarck","Grand Forks","Minot","West Fargo",
    "Rapid City","Aberdeen SD","Brookings","Watertown SD","Grand Island",
    "Kearney","Green Bay","Kenosha","Racine","Appleton","Waukesha","Oshkosh",
    "Eau Claire","Janesville","La Crosse WI","Sheboygan","Wausau","Beloit",
    "Cheyenne","Casper","Laramie","Gillette","Rock Springs","Ogden",
    "St George UT","Orem","Sandy UT","West Jordan","South Jordan","Layton",
    "Taylorsville","Murray","Everett","Renton","Kirkland","Redmond WA",
    "Bellingham","Kent","Yakima","Beaverton","Bend","Medford OR","Corvallis",
    "Gresham","Hillsboro","Sparks","Carson City","Elko","Las Cruces",
    "Rio Rancho","Santa Fe","Roswell NM","Farmington NM","Clovis NM","Hobbs",
    "Alamogordo","Carlsbad NM","Thornton","Centennial","Allentown","Erie",
    "Reading","Scranton","Bethlehem","Lancaster PA","York","Harrisburg",
    "Buffalo","Albany","New Rochelle","Mount Vernon","Schenectady","Utica",
    "Troy NY","Woodbridge NJ","Lakewood NJ","Toms River","Hamilton NJ",
    "Trenton","Edison","Cranston","Warwick","Pawtucket","East Providence",
    "Woonsocket","Waterbury","Montpelier VT","Rutland VT","Burlington VT",
    "Concord NH","Derry","Dover NH","Rochester NH","Nashua","Newport News",
    "Roanoke","Lynchburg","Charlottesville","Blacksburg","High Point",
    "Concord NC","Wilmington NC","Greenville NC","North Charleston",
    "Mount Pleasant SC","Greenville SC","Rock Hill","Spartanburg","Athens GA",
    "Marietta","Columbus GA","Savannah GA","Albany GA","Valdosta GA","Macon GA",
    "Johnson City","Kingsport","Jackson TN","Smyrna TN","Bartlett TN",
    "Brentwood TN","Mobile","Folsom","Citrus Heights","Rancho Cordova",
    "Turlock","Merced CA","Madera","Hanford","Porterville","Tulare","Hemet",
    "Perris","Lake Elsinore","Indio","Palm Springs","Palm Desert","El Centro",
    "Yucaipa","Rialto","Upland","Claremont","La Puente","Baldwin Park","Covina",
    "Azusa","Glendora","San Dimas","Diamond Bar","Lynwood","South Gate",
    "Bellflower","Cerritos","Seal Beach","Cypress CA","Buena Park","La Habra",
    "Placentia","Yorba Linda","Brea","La Mirada","Pico Rivera","Montebello",
    "Rosemead","Norwalk CA","Antioch CA","Peoria AZ","Noblesville IN",
    "Greenwood IN","Lafayette IN","Abilene TX","Amarillo TX","Wichita Falls TX",
    "Tyler TX","Longview TX","College Station TX","Bryan TX","Temple TX",
    "San Angelo TX","Odessa TX","Round Rock TX","Cedar Park TX","Georgetown TX",
    "Frisco TX","McKinney TX","Allen TX","Richardson TX","Grand Prairie TX",
    "Pearland TX","Sugar Land TX","Pasadena TX","League City TX","Carrollton TX",
    "Lewisville TX","Coeur d Alene","Twin Falls","Pensacola","Sarasota",
    "Fort Myers","Naples FL","Ocala","Port Charlotte","Bradenton","St Augustine",
    "Tupelo MS","Augusta ME","Pierre SD","Juneau AK",
    # CANADA
    "Toronto","Montreal","Vancouver","Calgary","Edmonton","Ottawa",
    "Winnipeg","Quebec City","Hamilton","Kitchener","London ON","Victoria BC",
    "Halifax NS","Oshawa","Windsor ON","Saskatoon","Regina","St Catharines",
    "Kelowna","Barrie","Abbotsford","Sudbury","Kingston ON","Saguenay",
    "Trois Rivieres","Guelph","Moncton","Brantford","Saint John NB","Thunder Bay",
    "Nanaimo","Burnaby","Surrey","Mississauga","Brampton","Markham",
    "Vaughan","Richmond Hill","Oakville","Burlington ON","Laval","Gatineau",
    "Longueuil","Sherbrooke","Levis","Chilliwack","Kamloops","Prince George",
    "Red Deer","Lethbridge","Medicine Hat","Fort McMurray","Grande Prairie",
    "Airdrie","Spruce Grove","St Albert","Leduc","Lloydminster","Camrose",
    "Moose Jaw","Prince Albert SK","Yorkton SK","Swift Current","North Battleford",
    "Brandon MB","Thompson MB","Portage la Prairie","Steinbach","Selkirk MB",
    "Fredericton","Miramichi","Edmundston","Bathurst NB","Campbellton",
    "Sydney NS","Truro NS","New Glasgow NS","Dartmouth","Bridgewater NS",
    "Charlottetown","Summerside","Stratford PEI","Cornwall PEI",
    "St Johns NL","Corner Brook","Gander","Grand Falls NL","Mount Pearl",
    "Labrador City","Whitehorse","Yellowknife","Iqaluit","Coquitlam",
    "Delta BC","Langley BC","Maple Ridge","New Westminster BC","North Vancouver",
    "Port Coquitlam","Port Moody","West Vancouver","Niagara Falls ON",
    "Peterborough","Sault Ste Marie","Waterloo ON","Whitby ON","Ajax ON",
    "Pickering ON","Newmarket ON","Sarnia","Canmore","Cold Lake","Wetaskiwin",
    "Weyburn SK","Estevan SK","Humboldt SK","Dauphin MB","Flin Flon",
    "The Pas MB","Morden MB","Winkler MB","Woodstock ON","Chatham ON",
    "Belleville ON","Cornwall ON","Timmins","North Bay ON","Orillia",
    "Midland ON","Collingwood","Drummondville","Saint Jean QC","Granby QC",
    "Shawinigan","Victoriaville QC","Baie Comeau","Alma QC","Rouyn Noranda",
    "Val d Or QC","Sept Iles","Repentigny","Blainville","Mirabel","Brossard",
    "Terrebonne","Saint Jerome","Mascouche","Chateauguay","Vaudreuil Dorion",
]))

# ─────────────────────────────────────────────
# 4. OCCASIONS — no occ tags
# ─────────────────────────────────────────────
OCCASIONS = [
    {"en":"Mother's Day Flowers","fr":"Fleurs fête des mères","zh":"母亲节鲜花","es":"Flores día de la madre","ru":"Цветы на День матери","slug":"mothers-day"},
    {"en":"Birthday Flowers",    "fr":"Fleurs d'anniversaire","zh":"生日鲜花",  "es":"Flores de cumpleaños","ru":"Цветы на день рождения","slug":"birthday"},
    {"en":"Anniversary Flowers", "fr":"Fleurs d'anniversaire de mariage","zh":"周年纪念花","es":"Flores de aniversario","ru":"Цветы на годовщину","slug":"anniversary"},
    {"en":"Sympathy Flowers",    "fr":"Fleurs de sympathie","zh":"慰问鲜花",   "es":"Flores de condolencia","ru":"Цветы соболезнования","slug":"sympathy"},
    {"en":"Get Well Flowers",    "fr":"Fleurs de rétablissement","zh":"祝愿康复花","es":"Flores de recuperación","ru":"Цветы пожелания здоровья","slug":"get-well"},
    {"en":"Romance Flowers",     "fr":"Fleurs romantiques","zh":"浪漫鲜花",    "es":"Flores románticas","ru":"Романтические цветы","slug":"romance"},
    {"en":"Thank You Flowers",   "fr":"Fleurs de remerciement","zh":"感谢鲜花", "es":"Flores de agradecimiento","ru":"Цветы благодарности","slug":"thank-you"},
    {"en":"New Baby Flowers",    "fr":"Fleurs nouveau-né","zh":"新生儿鲜花",    "es":"Flores bebé recién nacido","ru":"Цветы на рождение ребёнка","slug":"new-baby"},
]

# ─────────────────────────────────────────────
# 5. MULTILINGUAL CONTENT
# ─────────────────────────────────────────────
LANGS = {
    "en": {
        "dir":    "bing",
        "title":  lambda o,c: f"Send {o['en']} Online to {c} — Free Same-Day Delivery",
        "h1":     lambda o,c: f"Send {o['en']} Online to {c}",
        "meta":   lambda o,c: f"Send {o['en'].lower()} online to {c}. Free same-day delivery, $0 fees, from $29.99. 4.8 stars from 18,742 customers.",
        "intro":  lambda o,c: f"Looking to send {o['en'].lower()} online to {c} today? Floristone delivers farm-fresh flowers same-day to every neighbourhood in {c} — free delivery, $0 service fees, freshness guaranteed.",
        "h2a":    lambda o,c: f"How to send {o['en'].lower()} online to {c}",
        "bodyA":  lambda o,c: f"Order in 2 minutes. Choose your arrangement, add a card message, enter the delivery address in {c}, and checkout. Floristone's local florists in {c} cut flowers fresh and deliver same-day. Free delivery, $0 fees.",
        "h2b":    lambda o,c: f"Why Floristone is the best way to send flowers online to {c}",
        "bodyB":  lambda o,c: f"4.8/5 stars from 18,742 verified customers. Free same-day delivery. $0 service fees. Local florists in {c} — no warehouse transit, no wilted stems. Live tracking on every order.",
        "cta":    lambda o,c: f"Send {o['en']} to {c} Now",
        "faqQ":   lambda o,c: f"Can I send {o['en'].lower()} online to {c} today?",
        "faqA":   lambda o,c: f"Yes. Floristone guarantees same-day delivery across {c} with free delivery and $0 fees. Order before the daily cutoff for guaranteed same-day arrival.",
        "note":   "From $29.99 · Free delivery · $0 fees · 4.8★",
        "back":   "← Back to home",
        "footer": f"© {YEAR} BouquetFlowers · This page contains affiliate links.",
    },
    "fr": {
        "dir":    "bing-fr",
        "title":  lambda o,c: f"Envoyer des {o['fr']} à {c} — Livraison gratuite le jour même",
        "h1":     lambda o,c: f"Envoyer des {o['fr']} à {c}",
        "meta":   lambda o,c: f"Envoyez des {o['fr'].lower()} à {c} en ligne. Livraison gratuite le jour même, 0$ de frais, dès 29,99$.",
        "intro":  lambda o,c: f"Vous souhaitez envoyer des {o['fr'].lower()} à {c} aujourd'hui? Floristone livre le jour même dans tout {c} — livraison gratuite, 0$ de frais de service.",
        "h2a":    lambda o,c: f"Comment envoyer des {o['fr'].lower()} à {c}",
        "bodyA":  lambda o,c: f"Commandez en 2 minutes. Choisissez votre arrangement, ajoutez un message, entrez l'adresse de livraison à {c} et validez. Les fleuristes locaux de Floristone à {c} livrent le jour même.",
        "h2b":    lambda o,c: f"Pourquoi Floristone est le meilleur moyen d'envoyer des fleurs à {c}",
        "bodyB":  lambda o,c: f"4,8/5 étoiles de 18 742 clients vérifiés. Livraison gratuite le jour même. 0$ de frais. Fleuristes locaux à {c} — fleurs fraîches garanties.",
        "cta":    lambda o,c: f"Envoyer des {o['fr']} à {c}",
        "faqQ":   lambda o,c: f"Puis-je envoyer des {o['fr'].lower()} à {c} aujourd'hui?",
        "faqA":   lambda o,c: f"Oui. Floristone garantit la livraison le jour même à {c} avec livraison gratuite et 0$ de frais.",
        "note":   "Dès 29,99$ · Livraison gratuite · 0$ frais · 4,8★",
        "back":   "← Retour à l'accueil",
        "footer": f"© {YEAR} BouquetFlowers · Ce site contient des liens affiliés.",
    },
    "zh": {
        "dir":    "bing-zh",
        "title":  lambda o,c: f"在线向{c}发送{o['zh']} — 当日免费送达",
        "h1":     lambda o,c: f"在线向{c}发送{o['zh']}",
        "meta":   lambda o,c: f"在线向{c}发送{o['zh']}。当日免费送达，零服务费，低至$29.99。18,742位客户评分4.8星。",
        "intro":  lambda o,c: f"想今天在线向{c}发送{o['zh']}？Floristone当日送达{c}每个社区——免费配送，零服务费，新鲜花卉保证。",
        "h2a":    lambda o,c: f"如何在线向{c}发送{o['zh']}",
        "bodyA":  lambda o,c: f"两分钟完成下单。选择花束，添加贺卡信息，输入{c}的配送地址并结账。Floristone在{c}的本地花店当日新鲜配送。",
        "h2b":    lambda o,c: f"为什么Floristone是向{c}在线送花的最佳选择",
        "bodyB":  lambda o,c: f"18,742位验证客户评分4.8/5。当日免费配送。零服务费。{c}的本地花店——新鲜直送，含实时追踪。",
        "cta":    lambda o,c: f"立即向{c}发送{o['zh']}",
        "faqQ":   lambda o,c: f"今天能在线向{c}发送{o['zh']}吗？",
        "faqA":   lambda o,c: f"是的。Floristone保证在{c}免费当日配送，服务费$0。在每日截止时间前下单即可。",
        "note":   "低至$29.99 · 免费配送 · $0服务费 · 4.8★",
        "back":   "← 返回首页",
        "footer": f"© {YEAR} BouquetFlowers · 本页面含有联盟链接。",
    },
    "es": {
        "dir":    "bing-es",
        "title":  lambda o,c: f"Enviar {o['es']} online a {c} — Entrega gratis el mismo día",
        "h1":     lambda o,c: f"Enviar {o['es']} online a {c}",
        "meta":   lambda o,c: f"Envía {o['es'].lower()} online a {c}. Entrega gratis el mismo día, $0 cargos, desde $29.99.",
        "intro":  lambda o,c: f"¿Quieres enviar {o['es'].lower()} online a {c} hoy? Floristone entrega el mismo día en todo {c} — entrega gratis, $0 cargos de servicio, flores frescas garantizadas.",
        "h2a":    lambda o,c: f"Cómo enviar {o['es'].lower()} online a {c}",
        "bodyA":  lambda o,c: f"Ordena en 2 minutos. Elige tu arreglo, agrega un mensaje, ingresa la dirección en {c} y paga. Los floristas locales de Floristone en {c} entregan el mismo día.",
        "h2b":    lambda o,c: f"Por qué Floristone es la mejor forma de enviar flores online a {c}",
        "bodyB":  lambda o,c: f"4.8/5 estrellas de 18,742 clientes verificados. Entrega gratuita el mismo día. $0 cargos. Floristas locales en {c} — flores frescas garantizadas.",
        "cta":    lambda o,c: f"Enviar {o['es']} a {c} ahora",
        "faqQ":   lambda o,c: f"¿Puedo enviar {o['es'].lower()} online a {c} hoy?",
        "faqA":   lambda o,c: f"Sí. Floristone garantiza entrega el mismo día en {c} con entrega gratis y $0 de cargos.",
        "note":   "Desde $29.99 · Entrega gratis · $0 cargos · 4.8★",
        "back":   "← Volver al inicio",
        "footer": f"© {YEAR} BouquetFlowers · Esta página contiene enlaces de afiliado.",
    },
    "ru": {
        "dir":    "bing-ru",
        "title":  lambda o,c: f"Отправить {o['ru']} онлайн в {c} — Бесплатная доставка в день заказа",
        "h1":     lambda o,c: f"Отправить {o['ru']} онлайн в {c}",
        "meta":   lambda o,c: f"Отправьте {o['ru'].lower()} онлайн в {c}. Бесплатная доставка в день заказа, $0 сборов, от $29.99.",
        "intro":  lambda o,c: f"Хотите отправить {o['ru'].lower()} онлайн в {c} сегодня? Floristone доставляет в день заказа по всему {c} — бесплатная доставка, $0 сервисных сборов.",
        "h2a":    lambda o,c: f"Как отправить {o['ru'].lower()} онлайн в {c}",
        "bodyA":  lambda o,c: f"Заказ занимает 2 минуты. Выберите букет, добавьте сообщение, введите адрес доставки в {c} и оформите заказ. Местные флористы Floristone в {c} доставят в день заказа.",
        "h2b":    lambda o,c: f"Почему Floristone — лучший способ отправить цветы онлайн в {c}",
        "bodyB":  lambda o,c: f"4.8/5 от 18 742 подтверждённых клиентов. Бесплатная доставка в день заказа. $0 сборов. Местные флористы в {c} — свежие цветы гарантированы.",
        "cta":    lambda o,c: f"Отправить {o['ru']} в {c}",
        "faqQ":   lambda o,c: f"Можно ли отправить {o['ru'].lower()} онлайн в {c} сегодня?",
        "faqA":   lambda o,c: f"Да. Floristone гарантирует доставку в день заказа по {c} с бесплатной доставкой и $0 сборов.",
        "note":   "От $29.99 · Бесплатная доставка · $0 сборов · 4.8★",
        "back":   "← На главную",
        "footer": f"© {YEAR} BouquetFlowers · Эта страница содержит партнёрские ссылки.",
    },
}

# ─────────────────────────────────────────────
# 6. HTML TEMPLATE
# ─────────────────────────────────────────────
def build_page(lang_key, lang, occasion, city, slug):
    return f"""<!DOCTYPE html>
<html lang="{lang_key}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{lang['title'](occasion,city)} | BouquetFlowers</title>
    <meta name="description" content="{lang['meta'](occasion,city)}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{BASE_URL}/{lang['dir']}/{slug}">
    <script type="application/ld+json">
    {{"@context":"https://schema.org","@graph":[
      {{"@type":"Article","headline":"{lang['h1'](occasion,city)}","datePublished":"{TODAY}","dateModified":"{TODAY}","inLanguage":"{lang_key}","author":{{"@type":"Organization","name":"BouquetFlowers"}}}},
      {{"@type":"Product","name":"Floristone {occasion['en']} — {city}","offers":{{"@type":"Offer","priceCurrency":"USD","price":"29.99","availability":"https://schema.org/InStock","url":"{AFF_URL}","deliveryLeadTime":{{"@type":"QuantitativeValue","value":"0","unitCode":"DAY"}}}},"aggregateRating":{{"@type":"AggregateRating","ratingValue":"4.8","reviewCount":"18742"}}}},
      {{"@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"{lang['faqQ'](occasion,city)}","acceptedAnswer":{{"@type":"Answer","text":"{lang['faqA'](occasion,city)}"}}}}]}}
    ]}}
    </script>
    <style>
        :root{{--brand:#FF2E63;--blue:#003366;--bg:#f9f9ff;--border:#e6e6f0;}}
        *{{box-sizing:border-box;margin:0;padding:0;}}
        body{{font-family:system-ui,sans-serif;background:var(--bg);color:#333;line-height:1.7;}}
        .nav{{background:#fff;padding:14px 5%;border-bottom:1px solid var(--border);font-weight:700;color:var(--brand);display:flex;justify-content:space-between;align-items:center;}}
        .nav a{{font-size:0.85rem;color:var(--brand);text-decoration:none;}}
        .article{{max-width:760px;margin:0 auto;padding:50px 24px 80px;}}
        .eyebrow{{font-size:0.75rem;font-weight:700;color:var(--brand);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px;display:block;}}
        h1{{font-size:clamp(1.8rem,4vw,2.5rem);color:#1a1a1a;margin-bottom:16px;line-height:1.2;}}
        .byline{{font-size:0.85rem;color:#999;margin-bottom:32px;border-bottom:1px solid var(--border);padding-bottom:16px;}}
        h2{{font-size:1.3rem;color:#1a1a1a;margin:32px 0 10px;}}
        p{{margin-bottom:16px;font-size:1rem;color:#444;}}
        .trust-bar{{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;background:#fff;padding:12px;border:1px solid var(--border);border-radius:8px;margin-bottom:28px;font-size:0.8rem;font-weight:700;color:#444;}}
        .cta-box{{background:linear-gradient(135deg,#003366 0%,#FF2E63 100%);color:#fff;text-align:center;padding:40px 24px;border-radius:16px;margin:40px 0;}}
        .cta-box h2{{color:#fff;margin:0 0 10px;font-size:1.5rem;}}
        .cta-box p{{color:rgba(255,255,255,0.88);margin-bottom:20px;}}
        .cta-btn{{background:#fff;color:var(--brand);padding:14px 32px;border-radius:99px;font-weight:900;text-decoration:none;display:inline-block;font-size:1rem;}}
        .trust-row{{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-top:12px;}}
        .trust-row span{{font-size:0.75rem;color:rgba(255,255,255,0.8);font-weight:700;}}
        .faq-box{{background:#fff;border:1px solid var(--border);border-radius:12px;padding:24px;margin:32px 0;}}
        .faq-box strong{{display:block;color:#1a1a1a;margin-bottom:8px;}}
        .faq-box p{{margin:0;font-size:0.92rem;}}
        .related{{background:#fff;border-top:1px solid var(--border);padding:20px 24px;text-align:center;font-size:0.82rem;}}
        .related a{{color:var(--brand);text-decoration:none;font-weight:600;}}
        .related a:hover{{text-decoration:underline;}}
        .back{{display:block;text-align:center;margin-top:32px;font-size:0.85rem;color:var(--brand);text-decoration:none;}}
        footer{{background:#111;color:#888;text-align:center;padding:24px;font-size:0.78rem;}}
    </style>
</head>
<body>
<nav class="nav">BouquetFlowers <a href="{BASE_URL}/">{lang['back']}</a></nav>
<article class="article">
    <span class="eyebrow">{occasion[lang_key]} · {city} · {TODAY}</span>
    <h1>{lang['h1'](occasion,city)}</h1>
    <p class="byline">BouquetFlowers · {city} · {TODAY}</p>
    <div class="trust-bar">
        <span>✓ Free Delivery</span><span>✓ $0 Fees</span><span>✓ 4.8★ 18,742 reviews</span><span>✓ Same Day</span>
    </div>
    <p>{lang['intro'](occasion,city)}</p>
    <h2>{lang['h2a'](occasion,city)}</h2>
    <p>{lang['bodyA'](occasion,city)}</p>
    <h2>{lang['h2b'](occasion,city)}</h2>
    <p>{lang['bodyB'](occasion,city)}</p>
    <div class="cta-box">
        <h2>{lang['cta'](occasion,city)}</h2>
        <p>{lang['note']}</p>
        <a href="{AFF_URL}" class="cta-btn" target="_blank" rel="nofollow sponsored noopener">🌷 {lang['cta'](occasion,city)}</a>
        <div class="trust-row">
            <span>✓ FREE DELIVERY</span><span>✓ $0 FEES</span><span>✓ FRESHNESS GUARANTEED</span>
        </div>
    </div>
    <div class="faq-box">
        <strong>Q: {lang['faqQ'](occasion,city)}</strong>
        <p>{lang['faqA'](occasion,city)}</p>
    </div>
    <a href="{BASE_URL}/" class="back">{lang['back']}</a>
</article>
<div class="related">
    <strong>More Flower Delivery Sites:</strong><br><br>
    {RELATED_HTML}
</div>
<footer>{lang['footer']}</footer>
</body>
</html>"""

# ─────────────────────────────────────────────
# 7. GENERATE 2000 PAGES
# ─────────────────────────────────────────────
PAGES_PER_LANG  = 400
CITIES_PER_LANG = PAGES_PER_LANG // len(OCCASIONS)
batch_start     = seed % len(ALL_CITIES)
city_batch      = [ALL_CITIES[(batch_start + i) % len(ALL_CITIES)] for i in range(CITIES_PER_LANG)]

all_urls = []
total    = 0

for lang_key, lang in LANGS.items():
    folder = lang['dir']
    os.makedirs(folder, exist_ok=True)
    for city in city_batch:
        city_slug = city.lower().replace(" ", "-").replace("'", "")
        for occasion in OCCASIONS:
            slug = f"send-{occasion['slug']}-online-{city_slug}.html"
            html = build_page(lang_key, lang, occasion, city, slug)
            with open(f"{folder}/{slug}", "w", encoding="utf-8") as f:
                f.write(html)
            all_urls.append(f"{BASE_URL}/{folder}/{slug}")
            total += 1

# ─────────────────────────────────────────────
# 8. INDEXNOW PING
# ─────────────────────────────────────────────
payload = json.dumps({
    "host": "brightlane.github.io",
    "key": INDEXNOW_KEY,
    "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
    "urlList": all_urls[:10000]
}).encode("utf-8")

try:
    req = urllib.request.Request(
        "https://api.indexnow.org/IndexNow",
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        print(f"IndexNow: HTTP {resp.status} — {len(all_urls)} URLs submitted")
except Exception as e:
    print(f"IndexNow note: {e}")

print(f"\n✅ BouquetFlowers Bing Blast complete!")
print(f"   Affiliate URL: {AFF_URL}")
print(f"   Languages    : {', '.join(LANGS.keys())}")
print(f"   Cities/lang  : {len(city_batch)}")
print(f"   Occasions    : {len(OCCASIONS)}")
print(f"   Total pages  : {total}")
print(f"   Today batch  : {city_batch[:5]}...")
