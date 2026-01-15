import streamlit as st
from supabase import create_client
from datetime import datetime, timedelta, timezone

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
        res = supabase.table('users').select("*").eq('email', email).execute()
        if res.data: return "EXISTS"
        
        new_user = {
            "email": email,
            "password": password, 
            "first_name": first_name,
            "xp": 0,
            "level": 1,
            "ai_credits": 3,              # Nieuw: Startkapitaal voor AI
            "is_pro": False,
            "is_academy_student": False,  # Nieuw: De hardlock vlag
            "referral_code": f"{first_name[:3].upper()}-{email[:2].upper()}",
            "feedback_reward_claimed": False
        }
        supabase.table('users').insert(new_user).execute()
        return "SUCCESS"
    except:
        return "ERROR"

def verify_user(email, password):
    if not supabase: return False
    try:
        res = supabase.table('users').select("*").eq('email', email).eq('password', password).execute()
        return len(res.data) > 0
    except: return False

# --- AI CREDITS (Punt 5) ---
def update_user_credits(email, new_credits):
    """Zorgt dat AI credits persistent worden opgeslagen."""
    if not supabase: return False
    try:
        supabase.table('users').update({"ai_credits": new_credits}).eq('email', email).execute()
        return True
    except: return False

# --- WIZARD & BRAND IDENTITY ---
def update_onboarding_data(email, shop_name, income_goal):
    from modules import auth
    try:
        if auth.supabase:
            res = auth.supabase.table('users').update({
                "shop_name": shop_name,
                "income_goal": income_goal
            }).eq('email', email).execute()
            return True
    except Exception as e:
        print(f"Update error: {e}")
    return False

@st.cache_data(ttl=300)
def get_user_data(email):
    if not supabase: return {}
    try:
        res = supabase.table('users').select("*").eq('email', email).execute()
        if res.data: return res.data[0]
    except: pass
    return {}

# --- PRO STATUS & REWARDS ---
@st.cache_data(ttl=300)
def check_pro_status_db(email):
    if not supabase: return False
    try:
        res = supabase.table('users').select("is_pro, pro_expiry").eq('email', email).execute()
        if not res.data: return False
        
        user_data = res.data[0]
        # Als de permanente vlag op True staat
        if user_data.get('is_pro'): return True 
        
        # Check op tijdelijke expiry (van feedback)
        if user_data.get('pro_expiry'):
            expiry = datetime.fromisoformat(user_data['pro_expiry'].replace('Z', '+00:00'))
            if expiry > datetime.now(timezone.utc): return True
        return False
    except: return False

def get_pro_expiry_date(email):
    if not supabase: return None
    try:
        res = supabase.table('users').select("pro_expiry").eq('email', email).execute()
        if res.data and res.data[0]['pro_expiry']:
            return datetime.fromisoformat(res.data[0]['pro_expiry'].replace('Z', '+00:00'))
    except: pass
    return None

# --- FEEDBACK (Punt 2) ---
def save_feedback(email, message, is_valid):
    if not supabase: return False
    try:
        data = {"user_email": email, "message": message, "is_valid": is_valid, "created_at": datetime.now(timezone.utc).isoformat()}
        supabase.table('feedback').insert(data).execute()
        return True
    except: return False

def claim_feedback_reward(email, message=None):
    """Zorgt dat de feedback wordt opgeslagen EN de gebruiker 24u PRO krijgt."""
    if not supabase: return "ERROR"
    try:
        # 1. Check of al geclaimd
        res = supabase.table('users').select("feedback_reward_claimed").eq('email', email).execute()
        if res.data and res.data[0].get('feedback_reward_claimed'): 
            return "ALREADY_CLAIMED"
        
        # 2. Sla de feedback tekst op in de 'feedback' tabel
        if message:
            supabase.table('feedback').insert({
                "user_email": email,
                "message": message,
                "created_at": datetime.now(timezone.utc).isoformat()
            }).execute()
        
        # 3. Geef 24 uur PRO toegang
        now = datetime.now(timezone.utc)
        expiry_date = now + timedelta(hours=24)
        expiry_str = expiry_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        
        supabase.table('users').update({
            "pro_expiry": expiry_str, 
            "feedback_reward_claimed": True
        }).eq('email', email).execute()
        
        return "SUCCESS"
    except Exception as e:
        print(f"Database Error Feedback: {e}")
        return "ERROR"

# --- FINANCIËN ---
def save_daily_stats(email, revenue, ad_spend, cogs):
    if not supabase: return False
    try:
        data = {"user_email": email, "revenue": revenue, "ad_spend": ad_spend, "cogs": cogs, "date": datetime.now().strftime("%Y-%m-%d")}
        supabase.table('daily_stats').insert(data).execute()
        return True
    except: return False

def get_daily_stats_history(email):
    if not supabase: return []
    try:
        res = supabase.table('daily_stats').select("*").eq('user_email', email).order('date', desc=True).limit(7).execute()
        return res.data
    except: return []

def set_user_pro(email):
    """Zet een gebruiker op permanente PRO status (bv na betaling)."""
    if not supabase: return False
    try:
        # Voor betalende klanten zetten we is_pro op True, pro_expiry is dan optioneel/back-up
        expiry_date = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
        
        data = {
            "is_pro": True,
            "pro_expiry": expiry_date
        }
        
        supabase.table('users').update(data).eq('email', email).execute()
        return True
    except Exception as e:
        return False

def get_daily_winners_from_db():
    """Haalt winners uit DB, of geeft fallback als de tabel leeg is."""
    if not supabase: return []
    try:
        res = supabase.table('daily_winners').select("*").execute()
        if res.data and len(res.data) > 0:
            return res.data
        
        # FALLBACK: Als je tabel in Supabase nog leeg is, tonen we deze demo-data
        return [
            {"title": "Portable Blender Pro", "reason": "Hoge viraliteit op TikTok fitness-niche.", "video_url": "https://tiktok.com", "cover_url": "https://placehold.co/600x400?text=Blender+Pro"},
            {"title": "Crystal Hair Eraser", "reason": "Bewezen winnaar in de beauty-niche.", "video_url": "https://tiktok.com", "cover_url": "https://placehold.co/600x400?text=Hair+Eraser"},
            {"title": "Sunset Lamp Projector", "reason": "Perfect voor UGC content en sfeer-branding.", "video_url": "https://tiktok.com", "cover_url": "https://placehold.co/600x400?text=Sunset+Lamp"}
        ]
    except Exception as e:
        print(f"DB Error winners: {e}")
        return []

def can_user_search(email, is_pro):
    if is_pro: return True # PRO mag altijd
    
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        # Check of er vandaag al een record is voor deze user in een 'logs' tabel
        res = supabase.table('search_logs').select("*").eq('email', email).eq('date', today).execute()
        if len(res.data) >= 1: # Limiet van 1 per dag
            return False
        
        # Log de zoekopdracht direct
        supabase.table('search_logs').insert({"email": email, "date": today}).execute()
        return True
    except:
        return False # Bij error voor de zekerheid blokkeren

def update_password(email, new_password):
    if not supabase: return False
    try:
        supabase.table('users').update({"password": new_password}).eq('email', email).execute()
        return True
    except:
        return False

# --- BONUS: EERSTE 100 STUDENTEN LOGICA ---
def claim_founder_bonus(email):
    """
    Checkt of er nog plek is bij de eerste 100.
    Zo ja: zet 'is_academy_student' op True.
    Geeft terug: (True/False, overgebleven_plekken)
    """
    if not supabase: return False, 0
    
    try:
        # 1. Tel hoeveel studenten er al zijn
        # We selecteren 1 kolom om data te besparen, count='exact' telt de rijen
        res = supabase.table('users').select("id", count="exact").eq("is_academy_student", True).execute()
        current_count = res.count
        
        limit = 100
        
        if current_count < limit:
            # 2. Er is plek! Ken de status toe
            supabase.table('users').update({"is_academy_student": True}).eq("email", email).execute()
            spots_left = limit - (current_count + 1)
            return True, spots_left
        else:
            # 3. Helaas, vol.
            return False, 0
            
    except Exception as e:
        print(f"Bonus Error: {e}")
        return False, 0