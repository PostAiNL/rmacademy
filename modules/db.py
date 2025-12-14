import streamlit as st
from datetime import datetime, timedelta, timezone

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

def claim_feedback_reward(email):
    """
    Probeert de 24u reward te claimen.
    Returns: "SUCCESS", "ALREADY_CLAIMED", of "ERROR"
    """
    client = get_client()
    if not client: return "ERROR"
    
    try:
        # 1. Check of gebruiker al bestaat en reward heeft gehad
        res = client.table("users").select("*").eq("email", email).execute()
        
        if res.data:
            user_data = res.data[0]
            if user_data.get('has_claimed_feedback_reward', False):
                return "ALREADY_CLAIMED"

        # 2. Geef reward en zet vinkje aan
        expiry_time = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
        
        data = {
            "email": email, 
            "pro_expiry": expiry_time,
            "has_claimed_feedback_reward": True
        }
        
        client.table("users").upsert(data).execute()
        return "SUCCESS"
        
    except Exception as e:
        print(f"DB Error: {e}")
        return "ERROR"

def check_pro_status_db(email):
    """Checkt of de gebruiker nog geldige pro tijd heeft in DB."""
    client = get_client()
    if not client: return False
    
    try:
        res = client.table("users").select("pro_expiry").eq("email", email).execute()
        if res.data:
            expiry_str = res.data[0]['pro_expiry']
            if expiry_str:
                expiry_dt = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
                if expiry_dt > datetime.now(timezone.utc):
                    return True
    except: pass
    return False

def save_feedback(email, content, is_valid):
    """Slaat feedback op."""
    client = get_client()
    if client:
        try:
            client.table("feedback").insert({
                "email": email, 
                "content": content, 
                "is_valid": is_valid
            }).execute()
        except: pass