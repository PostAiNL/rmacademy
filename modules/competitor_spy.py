import requests
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime
from deep_translator import GoogleTranslator

# Bekende Shopify Apps
KNOWN_APPS = {
    "loox.io": "Loox Reviews", "judge.me": "Judge.me", "klaviyo": "Klaviyo",
    "shopify-product-reviews": "Shopify Reviews", "yotpo": "Yotpo", "privy": "Privy",
    "dsers": "DSers", "oberlo": "Oberlo", "printful": "Printful", "pagefly": "PageFly",
    "shogun": "Shogun", "debutify": "Debutify", "roas": "TripleWhale/Hyros",
    "smsbump": "SMSBump", "recart": "Recart", "pushowl": "PushOwl", "gorgias": "Gorgias"
}

def analyze_store(store_url):
    """
    Haalt store data op. Probeert nu ook voorraad te checken voor betere schattingen.
    """
    clean_url = store_url.replace("https://", "").replace("http://", "").split("/")[0]
    base_url = f"https://{clean_url}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    store_data = {
        "name": clean_url, "theme": "Onbekend", "apps": [],
        "product_count": 0, "avg_price": 0, "last_update": "-",
        "best_sellers": [], "status": "Offline", "speed": 0
    }

    # 1. HTML & APPS Check
    try:
        start = time.time()
        r = requests.get(base_url, headers=headers, timeout=10)
        store_data['speed'] = round(time.time() - start, 2)
        
        if r.status_code == 200:
            store_data['status'] = "Online"
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Theme detection
            m = re.search(r'Shopify\.theme\s*=\s*({.*?})', r.text)
            if m:
                nm = re.search(r'"name":"(.*?)"', m.group(1))
                if nm: store_data['theme'] = nm.group(1)
            
            # App detection
            found = []
            for s in soup.find_all('script'):
                src = s.get('src', '').lower()
                for k, v in KNOWN_APPS.items():
                    if k in src and v not in found: found.append(v)
            store_data['apps'] = found
    except: pass

    # 2. PRODUCT DATA & SALES ESTIMATION
    try:
        api = f"{base_url}/products.json?limit=12&sort_by=best-selling"
        r = requests.get(api, headers=headers, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            products = data.get('products', [])
            store_data['product_count'] = len(products)
            
            translator = GoogleTranslator(source='auto', target='nl')
            cleaned = []
            total_price = 0
            
            for p in products:
                # Dagen online
                pub = p.get('published_at', '')
                days = 0
                if pub:
                    try:
                        d = datetime.strptime(pub[:10], "%Y-%m-%d")
                        days = (datetime.now() - d).days
                    except: pass
                
                # Image
                img = "https://via.placeholder.com/300?text=Geen+Foto"
                if p.get('images') and len(p['images']) > 0:
                    src = p['images'][0].get('src', '')
                    img = src if src.startswith('http') else f"https:{src}"

                # Data extractie
                variant = p['variants'][0] if p['variants'] else {}
                pr = float(variant.get('price', 0))
                cmp = variant.get('compare_at_price')
                compare_price = float(cmp) if cmp else pr * 1.5
                total_price += pr
                
                # Check echte inventory (indien niet verborgen door Shopify)
                stock = variant.get('inventory_quantity', None)
                
                # Vertaling
                try: title_nl = translator.translate(p['title'])
                except: title_nl = p['title']
                
                # Opties ophalen voor import (Kleur, Maat etc)
                options = []
                for opt in p.get('options', []):
                    options.append({"name": opt['name'], "values": opt['values']})

                cleaned.append({
                    "title": title_nl,
                    "original_title": p['title'],
                    "description": p.get('body_html', ''),
                    "image_url": img,
                    "price": pr,
                    "compare_price": compare_price,
                    "handle": p['handle'],
                    "product_url": f"{base_url}/products/{p['handle']}",
                    "days_online": days,
                    "options": options,
                    "inventory": stock # Kan None zijn
                })
            
            store_data['best_sellers'] = cleaned
            if products: 
                store_data['avg_price'] = round(total_price/len(products), 2)
                store_data['last_update'] = products[0].get('updated_at', '')[:10]

    except Exception as e: print(f"API Error: {e}")

    return store_data

def estimate_revenue(price):
    """
    Geeft een conservatieve schatting van de DAGELIJJKSE potentie.
    We noemen dit nu 'Sales Potential' ipv harde revenue.
    """
    try:
        p = float(price)
        # Formule aangepast: Goedkopere items verkopen vaker, dure minder.
        if p < 20: multiplier = 15 # Volume product
        elif p < 50: multiplier = 10 
        else: multiplier = 5 # High ticket
        
        return p * multiplier
    except: return 0

def get_best_sellers(url):
    return analyze_store(url).get('best_sellers', [])