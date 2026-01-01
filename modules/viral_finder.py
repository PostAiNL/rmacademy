from apify_client import ApifyClient
import streamlit as st
import random

APIFY_TOKEN = st.secrets["apify"]["token"]

def estimate_sales_revenue(views, likes):
    """Schatting van sales en omzet."""
    conversion_rate = 0.0015 # 0.15%
    avg_price = 29.95
    est_sales = int(views * conversion_rate)
    est_revenue = int(est_sales * avg_price)
    viral_score = min(100, int((likes / views * 500) + (views / 10000)))
    return est_sales, est_revenue, viral_score

@st.cache_data(ttl=3600, show_spinner=False)
def search_tiktok_winning_products(keyword, min_views, sort_by="views"):
    """Zoekfunctie met error handling voor API limieten."""
    try:
        if "PLAK_HIER" in APIFY_TOKEN or not APIFY_TOKEN:
            return []

        client = ApifyClient(APIFY_TOKEN)
        search_term = f"{keyword} musthave" if " " not in keyword else keyword

        run_input = {
            "searchQueries": [search_term], 
            "resultsPerPage": 10, # Iets minder resultaten bespaart API-tegoed
            "shouldDownloadCovers": True,
        }

        run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
        dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
        
        results = []
        for item in dataset_items:
            views = item.get('playCount', 0)
            likes = item.get('diggCount', 0)
            
            if views >= min_views:
                est_sales, est_revenue, score = estimate_sales_revenue(views, likes)
                results.append({
                    "id": item.get('id', str(random.randint(1000,9999))),
                    "desc": item.get('text', 'Geen titel'),
                    "views": views,
                    "likes": likes,
                    "cover": item.get('videoMeta', {}).get('coverUrl', ''),
                    "url": item.get('webVideoUrl', ''),
                    "est_revenue": est_revenue,
                    "viral_score": score
                })
        
        # Sorteren
        if sort_by == "revenue": results.sort(key=lambda x: x['est_revenue'], reverse=True)
        elif sort_by == "score": results.sort(key=lambda x: x['viral_score'], reverse=True)
        else: results.sort(key=lambda x: x['views'], reverse=True)
            
        return results

    except Exception as e:
        # Check of het een limiet-fout is
        error_msg = str(e).lower()
        if "limit exceeded" in error_msg or "usage exceeded" in error_msg:
            return "LIMIT_REACHED"
        print(f"Scraper Error: {e}")
        return []

@st.cache_data(ttl=86400) # Slaat de resultaten 24 uur op
def get_daily_pro_picks():
    """Haalt een vaste set 'PRO' winners op, met fallback als de API op is."""
    try:
        client = ApifyClient(st.secrets["apify"]["token"])
        search_queries = ["tiktokmademebuyit", "amazonfinds 2025"]
        query = random.choice(search_queries)
        
        run_input = {
            "searchQueries": [query],
            "resultsPerPage": 3,
            "shouldDownloadCovers": True,
        }
        
        run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
        items = list(client.dataset(run["defaultDatasetId"]).list_items().items)
        
        # Voeg analyse labels toe
        for item in items:
            item['pro_reason'] = random.choice([
                "Hoge 'Impulse Buy' factor door visuele demonstratie.",
                "Probleem-oplosser met lage inkoopwaarde en hoge marge.",
                "Trend is momenteel groeiend in de VS, EU volgt vaak binnen 2 weken."
            ])
        return items

    except Exception as e:
        # Als de limiet bereikt is (of een andere fout), toon deze vaste 'fallback' winners
        print(f"Apify Error: {e}")
        return [
            {
                "text": "Portable Blender Pro",
                "webVideoUrl": "https://www.tiktok.com",
                "videoMeta": {"coverUrl": "https://placehold.co/600x400?text=Blender+Pro"},
                "pro_reason": "Bewezen winnaar in de fitness niche. Hoge marges via lokale leveranciers."
            },
            {
                "text": "Crystal Hair Eraser",
                "webVideoUrl": "https://www.tiktok.com",
                "videoMeta": {"coverUrl": "https://placehold.co/600x400?text=Hair+Eraser"},
                "pro_reason": "Gaat momenteel viraal in Duitsland en Frankrijk. Perfect voor UGC content."
            },
            {
                "text": "Sunset Lamp Projector",
                "webVideoUrl": "https://www.tiktok.com",
                "videoMeta": {"coverUrl": "https://placehold.co/600x400?text=Sunset+Lamp"},
                "pro_reason": "Hoge visuele aantrekkingskracht op TikTok. Ideaal voor sfeer-branding."
            }
        ]