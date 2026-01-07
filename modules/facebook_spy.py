import streamlit as st
from apify_client import ApifyClient
import urllib.parse

def search_facebook_ads(query, max_results=15): # We verlagen het naar 15 voor meer succes
    client = ApifyClient(st.secrets["apify"]["token"])

    encoded_query = urllib.parse.quote(query)
    # We voegen de taal toe aan de URL
    start_url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&q={encoded_query}&country=NL&media_type=all"

    run_input = {
        "startUrls": [{"url": start_url}],
        "maxAds": max_results,
        "activeStatus": "active",
        "viewAllAds": True,
        # NIEUW: We dwingen de robot om heel traag en menselijk te werken
        "maxConcurrency": 1, 
        "proxyConfiguration": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
            "apifyProxyCountry": "NL" # We dwingen een Nederlandse proxy af
        }
    }

    try:
        # We gebruiken een langere timeout zodat de robot de tijd krijgt
        run = client.actor("apify/facebook-ads-scraper").call(run_input=run_input, timeout_secs=120)

        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append({
                "page_name": item.get("pageName", "Onbekend"),
                "media": item.get("adSnapshotUrl"),
                "days_active": 1,
                "shop_link": item.get("ctaLink", "#")
            })
        
        # Als we ondanks alles 0 resultaten hebben, is hij waarschijnlijk alsnog geblokkeerd
        if len(results) == 0:
            return "ERROR"
            
        return results

    except Exception as e:
        print(f"Apify Error: {e}")
        return "ERROR"