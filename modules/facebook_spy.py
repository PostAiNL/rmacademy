import streamlit as st
from apify_client import ApifyClient
import urllib.parse

def search_facebook_ads(query, max_results=20):
    """
    Gebruikt de officiele apify/facebook-ads-scraper.
    Kosten: ca. $0.20 per succesvolle scan.
    """
    client = ApifyClient(st.secrets["apify"]["token"])

    # We bouwen de zoek-URL die de robot nodig heeft
    # We zoeken standaard in Nederland ('NL') en op alle actieve ads
    encoded_query = urllib.parse.quote(query)
    start_url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&q={encoded_query}&country=NL&media_type=all"

    run_input = {
        "startUrls": [{"url": start_url}],
        "maxAds": max_results, # We zetten hem op 20 om kosten te besparen
        "activeStatus": "active",
        "viewAllAds": True,
        "proxyConfiguration": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"] # CRUCIAAL voor Facebook
        }
    }

    try:
        # Start de robot
        run = client.actor("apify/facebook-ads-scraper").call(run_input=run_input)

        # Haal de resultaten op
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            # We pakken alleen de info die we echt nodig hebben
            results.append({
                "page_name": item.get("pageName", "Onbekend"),
                "media": item.get("adSnapshotUrl"), # Screenshot van de ad
                "days_active": 1, # De officiele scraper geeft vaak geen exacte begindatum, we zetten hem op 1
                "shop_link": item.get("ctaLink", "#") # De link naar de webshop
            })
        
        return results

    except Exception as e:
        print(f"Apify Error: {e}")
        return "ERROR"