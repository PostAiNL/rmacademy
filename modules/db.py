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

# --- AUTHENTICATIE ---

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email, password, name=""):
    client = get_client()
    if not client: return "ERROR"
    
    hashed_pw = hash_password(password)
    
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
    client = get_client()
    if not client: return False
    
    hashed_pw = hash_password(password)
    try:
        res = client.table("users").select("password").eq("email", email).execute()
        if res.data:
            # Gebruik .get() om crash te voorkomen bij oude accounts zonder wachtwoord
            if res.data[0].get('password') == hashed_pw:
                return True
    except: pass
    return False

def get_user_data(email):
    client = get_client()
    if not client: return {}
    try:
        res = client.table("users").select("*").eq("email", email).execute()
        if res.data: return res.data[0]
    except: pass
    return {}

# --- PRO & REWARDS SYSTEEM (HIER ZAT DE FOUT) ---

def give_temp_pro_access(email, hours=24):
    client = get_client()
    if not client: return False
    expiry_time = (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()
    try:
        client.table("users").update({"pro_expiry": expiry_time}).eq("email", email).execute()
        return True
    except: return False

def check_pro_status_db(email):
    """Checkt of de PRO tijd nog geldig is."""
    client = get_client()
    if not client: return False
    try:
        res = client.table("users").select("pro_expiry").eq("email", email).execute()
        if res.data and res.data[0].get('pro_expiry'):
            expiry_str = res.data[0]['pro_expiry']
            # Convert string to datetime
            expiry_dt = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
            if expiry_dt > datetime.now(timezone.utc):
                return True
    except: pass
    return False

def get_pro_expiry_date(email):
    """Haalt de exacte datum op voor de countdown timer."""
    client = get_client()
    if not client: return None
    try:
        res = client.table("users").select("pro_expiry").eq("email", email).execute()
        if res.data and res.data[0].get('pro_expiry'):
            return datetime.fromisoformat(res.data[0]['pro_expiry'].replace('Z', '+00:00'))
    except: pass
    return None

def claim_feedback_reward(email):
    client = get_client()
    if not client: return "ERROR"
    try:
        res = client.table("users").select("has_claimed_feedback_reward").eq("email", email).execute()
        if res.data and res.data[0].get('has_claimed_feedback_reward'): 
            return "ALREADY_CLAIMED"
        
        # Geef reward
        if give_temp_pro_access(email, 24):
            client.table("users").update({"has_claimed_feedback_reward": True}).eq("email", email).execute()
            return "SUCCESS"
        return "ERROR"
    except: return "ERROR"

# --- STATS & FEEDBACK ---

def save_feedback(email, content, is_valid):
    client = get_client()
    if client:
        try: client.table("feedback").insert({"email": email, "content": content, "is_valid": is_valid}).execute()
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
        except: return False
    return False

def get_daily_stats_history(email):
    client = get_client()
    if not client: return []
    try:
        res = client.table("daily_stats").select("*").eq("user_email", email).order("date", desc=True).limit(7).execute()
        return res.data
    except: return []