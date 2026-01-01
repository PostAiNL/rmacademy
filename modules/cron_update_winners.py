import os
import random
from apify_client import ApifyClient
from supabase import create_client

# Gebruik de variabelen die je al in je secrets hebt of stel ze hier lokaal in
APIFY_TOKEN = st.secrets["apify"]["token"]
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]

def update_daily_winners():
    print("🚀 Starten met ophalen van nieuwe winners...")
    
    # 1. Scrapen via Apify
    client = ApifyClient(APIFY_TOKEN)
    run_input = {
        "searchQueries": ["tiktokmademebuyit"],
        "resultsPerPage": 3,
        "shouldDownloadCovers": True,
    }
    
    try:
        run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
        items = list(client.dataset(run["defaultDatasetId"]).list_items().items)
        
        if not items:
            print("❌ Geen items gevonden.")
            return

        # 2. Voorbereiden voor Database
        new_rows = []
        reasons = [
            "Hoge impuls-aankoop waarde. Perfect voor TikTok Shop.",
            "Lage concurrentie op Meta Ads, hoge viraliteit op TikTok.",
            "Probleem-oplosser die makkelijk te demonstreren is in video."
        ]

        for idx, item in enumerate(items):
            new_rows.append({
                "title": item.get('text', 'Winning Product')[:100],
                "video_url": item.get('webVideoUrl', ''),
                "cover_url": item.get('videoMeta', {}).get('coverUrl', ''),
                "reason": reasons[idx] if idx < len(reasons) else "Top trend van dit moment."
            })

        # 3. Opslaan in Supabase
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Eerst de oude van gisteren verwijderen
        supabase.table("daily_winners").delete().neq("title", "LEEG").execute()
        
        # Nieuwe toevoegen
        supabase.table("daily_winners").insert(new_rows).execute()
        
        print(f"✅ Succes! {len(new_rows)} winners in de database gezet.")

    except Exception as e:
        print(f"❌ Fout opgetreden: {e}")

if __name__ == "__main__":
    update_daily_winners()