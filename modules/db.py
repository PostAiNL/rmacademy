import streamlit as st
from supabase import create_client
from datetime import datetime, timedelta, timezone
import pytz

# --- INIT SUPABASE ---
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except:
        return None

supabase = init_supabase()

# --- USER MANAGEMENT ---
def create_user(email, password, first_name):
    if not supabase: return "ERROR"
    try:
        # 1. Check of user bestaat
        res = supabase.table('users').select("*").eq('email', email).execute()
        if res.data:
            return "EXISTS"
        
        # 2. Maak user aan
        new_user = {
            "email": email,
            "password": password, # In productie: Hash dit!
            "first_name": first_name,
            "xp": 0,
            "level": 1,
            "is_pro": False,
            "referral_code": f"{first_name[:3].upper()}-{email[:2].upper()}"
        }
        supabase.table('users').insert(new_user).execute()
        return "SUCCESS"
    except Exception as e:
        print(f"DB Error: {e}")
        return "ERROR"

def verify_user(email, password):
    if not supabase: return False
    try:
        res = supabase.table('users').select("*").eq('email', email).eq('password', password).execute()
        return len(res.data) > 0
    except:
        return False

# --- PRO STATUS & REWARDS ---
def check_pro_status_db(email):
    """Check of de gebruiker een geldige PRO licentie of tijdelijke toegang heeft."""
    if not supabase: return False
    try:
        # 1. Check vaste licentie
        res = supabase.table('users').select("is_pro, pro_expiry").eq('email', email).execute()
        if not res.data: return False
        
        user_data = res.data[0]
        if user_data.get('is_pro'): return True # Vaste PRO
        
        # 2. Check tijdelijke toegang
        if user_data.get('pro_expiry'):
            expiry = datetime.fromisoformat(user_data['pro_expiry'])
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            if expiry > datetime.now(timezone.utc):
                return True
                
        return False
    except:
        return False

def get_pro_expiry_date(email):
    if not supabase: return None
    try:
        res = supabase.table('users').select("pro_expiry").eq('email', email).execute()
        if res.data and res.data[0]['pro_expiry']:
            return datetime.fromisoformat(res.data[0]['pro_expiry'])
    except: pass
    return None

# --- FEEDBACK OPSLAAN & CLAIMEN (NIEUW) ---
def save_feedback(email, message, is_valid):
    """Slaat de feedback op in de 'feedback' tabel."""
    if not supabase: return False
    try:
        data = {
            "user_email": email,
            "message": message,
            "is_valid": is_valid,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        supabase.table('feedback').insert(data).execute()
        return True
    except Exception as e:
        print(f"Save Feedback Error: {e}")
        return False

def claim_feedback_reward(email):
    """Activeert 24u PRO als beloning voor feedback."""
    if not supabase: return "ERROR"
    try:
        # 1. Check of al geclaimd
        res = supabase.table('users').select("feedback_reward_claimed").eq('email', email).execute()
        if res.data and res.data[0].get('feedback_reward_claimed'):
            return "ALREADY_CLAIMED"
        
        # 2. Bereken nieuwe tijd (Nu + 24 uur)
        new_expiry = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
        
        # 3. Update User
        supabase.table('users').update({
            "pro_expiry": new_expiry,
            "feedback_reward_claimed": True
        }).eq('email', email).execute()
        
        return "SUCCESS"
    except Exception as e:
        print(f"Claim Reward Error: {e}")
        return "ERROR"

# --- FINANCIËN ---
def save_daily_stats(email, revenue, ad_spend, cogs):
    if not supabase: return False
    try:
        data = {
            "user_email": email,
            "revenue": revenue,
            "ad_spend": ad_spend,
            "cogs": cogs,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        supabase.table('daily_stats').insert(data).execute()
        return True
    except: return False

def get_daily_stats_history(email):
    if not supabase: return []
    try:
        res = supabase.table('daily_stats').select("*").eq('user_email', email).order('date', desc=True).limit(7).execute()
        return res.data
    except: return []