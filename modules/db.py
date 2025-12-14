import streamlit as st
from datetime import datetime, timedelta, timezone
import hashlib

# Zorg dat 'supabase' in je requirements.txt staat
try:
    from supabase import create_client, Client
    HAS_DB = True
except ImportError:
    HAS_DB = False

def get_client():
    if not HAS_DB: return None
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except: return None

# --- AUTHENTICATIE MET WACHTWOORD (DEZE MISTE JE) ---

def hash_password(password):
    """Simpele hashing voor veiligheid."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email, password, name=""):
    """Maakt een gebruiker aan in Supabase users tabel."""
    client = get_client()
    if not client: return "ERROR"
    
    hashed_pw = hash_password(password)
    
    # We voegen nu ook wachtwoord en naam toe
    data = {
        "email": email, 
        "password": hashed_pw,
        "first_name": name,
        "pro_expiry": None # Standaard geen pro
    }
    
    try:
        # 1. Check of gebruiker al bestaat
        res = client.table("users").select("*").eq("email", email).execute()
        if res.data: 
            return "EXISTS"
        
        # 2. Nieuwe gebruiker invoegen
        client.table("users").insert(data).execute()
        return "SUCCESS"
    except Exception as e:
        print(f"DB Auth Error: {e}")
        return "ERROR"

def verify_user(email, password):
    """Checkt of email en wachtwoord kloppen."""
    client = get_client()
    if not client: return False
    
    hashed_pw = hash_password(password)
    try:
        res = client.table("users").select("password").eq("email", email).execute()
        if res.data:
            # Check of het wachtwoord in de database matcht met de hash
            stored_pw = res.data[0].get('password')
            if stored_pw == hashed_pw:
                return True
    except: pass
    return False

def get_user_data(email):
    """Haalt extra data op (zoals naam)."""
    client = get_client()
    if not client: return {}
    try:
        res = client.table("users").select("*").eq("email", email).execute()
        if res.data: return res.data[0]
    except: pass
    return {}

# --- PRO / FEEDBACK / STATS FUNCTIES ---

def give_temp_pro_access(email, hours=24):
    client = get_client()
    if not client: return False
    expiry_time = (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()
    try:
        # Upsert zorgt dat het werkt, ook als de user nog niet bestond (zou niet moeten kunnen nu, maar voor zekerheid)
        data = {"email": email, "pro_expiry": expiry_time}
        client.table("users").upsert(data).execute()
        return True
    except: return False

def check_pro_status_db(email):
    client = get_client()
    if not client: return False
    try:
        res = client.table("users").select("pro_expiry").eq("email", email).execute()
        if res.data and res.data[0].get('pro_expiry'):
            expiry_str = res.data[0]['pro_expiry']
            expiry_dt = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
            if expiry_dt > datetime.now(timezone.utc): return True
    except: pass
    return False

def claim_feedback_reward(email):
    client = get_client()
    if not client: return "ERROR"
    try:
        # Check status
        res = client.table("users").select("has_claimed_feedback_reward").eq("email", email).execute()
        if res.data and res.data[0].get('has_claimed_feedback_reward'): 
            return "ALREADY_CLAIMED"
        
        # Geef reward en zet vinkje
        give_temp_pro_access(email, 24)
        client.table("users").update({"has_claimed_feedback_reward": True}).eq("email", email).execute()
        return "SUCCESS"
    except Exception as e: 
        print(e)
        return "ERROR"

def save_feedback(email, content, is_valid):
    client = get_client()
    if client:
        try: 
            client.table("feedback").insert({
                "email": email, 
                "content": content, 
                "is_valid": is_valid
            }).execute()
        except: pass

def save_daily_stats(email, revenue, spend, cogs):
    client = get_client()
    if client:
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            client.table("daily_stats").insert({
                "user_email": email, 
                "date": today, 
                "revenue": revenue, 
                "ad_spend": spend, 
                "cogs": cogs
            }).execute()
            return True
        except Exception as e: 
            print(e)
            return False
    return False

def get_daily_stats_history(email):
    client = get_client()
    if not client: return []
    try:
        res = client.table("daily_stats").select("*").eq("user_email", email).order("date", desc=True).limit(7).execute()
        return res.data
    except: return []