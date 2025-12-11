import streamlit as st
import random
import string
import time
import smtplib
from datetime import datetime, timezone, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from supabase import create_client

# --- CONFIGURATIE VAN DE RANGEN ---
RANKS = {
    0: "🐣 Starter",
    200: "🔨 Bouwer",
    500: "🚀 Expert",       
    1000: "👑 E-com Boss"
}

# CONNECTIE MET SUPABASE
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except: return None

supabase = init_supabase()

# --- HULPFUNCTIE: BEPAAL RANG ---
def get_rank_info(xp):
    current_title = "🐣 Starter"
    next_xp = 200
    for threshold, title in sorted(RANKS.items()):
        if xp >= threshold:
            current_title = title
        else:
            next_xp = threshold
            break
    return current_title, next_xp

# --- DATA OPHALEN VOOR LEADERBOARD & TICKER ---
def get_leaderboard_data():
    """Haalt de top 10 users op uit Supabase."""
    if not supabase: return []
    try:
        # Haal users op, gesorteerd op XP
        response = supabase.table('users').select('email, xp, level, is_pro').order('xp', desc=True).limit(10).execute()
        data = response.data
        
        leaderboard = []
        for i, u in enumerate(data):
            # Email anonimiseren (bv. mark@gmail.com -> Mark G.)
            email_parts = u['email'].split('@')
            name_part = email_parts[0].capitalize()
            domain_char = email_parts[1][0].upper() if len(email_parts) > 1 else "X"
            display_name = f"{name_part} {domain_char}."
            
            title, _ = get_rank_info(u['xp'])
            
            leaderboard.append({
                "rank": i + 1,
                "name": display_name,
                "xp": u['xp'],
                "title": title,
                "is_pro": u['is_pro']
            })
        return leaderboard
    except Exception as e:
        print(f"Leaderboard error: {e}")
        return []

def get_real_activity():
    """Haalt recente activiteit op (of simuleert dit op basis van echte users)."""
    if not supabase: return "⚡ Live: Systeem wordt opgestart..."
    
    try:
        # We pakken 5 willekeurige actieve users om activiteit te simuleren
        # In een perfecte wereld heb je een 'activity_log' tabel, maar dit werkt ook prima.
        response = supabase.table('users').select('email, xp').gt('xp', 0).limit(20).execute()
        users = response.data
        
        if not users: return "⚡ Live: Wachten op eerste studenten..."
        
        user = random.choice(users)
        email_name = user['email'].split('@')[0].capitalize()
        
        # Willekeurige echte lijkende berichten
        msgs = [
            f"🔥 **{email_name}** is net gestegen in rang!",
            f"🚀 **{email_name}** heeft +50 XP verdiend.",
            f"💎 **{email_name}** is druk bezig in Fase 2.",
            f"👀 **{email_name}** gebruikt de Spy Tool.",
            f"📝 **{email_name}** is bezig met KVK inschrijving."
        ]
        return random.choice(msgs)
    except:
        return "⚡ Live: Druk bezig in de community..."

# --- ECHTE EMAIL FUNCTIE ---
def send_welcome_email(to_email, referral_code):
    try:
        smtp_server = st.secrets["email"]["smtp_server"]
        smtp_port = st.secrets["email"]["smtp_port"]
        smtp_user = st.secrets["email"]["smtp_user"]
        smtp_password = st.secrets["email"]["smtp_password"]
        sender_email = st.secrets["email"]["sender_email"]

        subject = "Welkom bij RM Ecom Academy! 🚀"
        body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="background-color: #f8fafc; padding: 20px; text-align: center;">
                <h2>Welkom bij de Academy!</h2>
                <p>Je account is succesvol aangemaakt.</p>
                <div style="background: #fff; padding: 15px; border-radius: 8px; display: inline-block; border: 1px solid #e2e8f0;">
                    <strong>Jouw Vrienden Code:</strong><br>
                    <span style="font-size: 20px; color: #0ea5e9; font-weight: bold;">{referral_code}</span>
                </div>
            </div>
          </body>
        </html>
        """

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Mail Fout: {e}")
        return False

def generate_referral_code(name):
    prefix = name[:3].upper() if len(name) >=3 else "USER"
    suffix = ''.join(random.choices(string.digits, k=3))
    return f"{prefix}-{suffix}"

def login_or_register(email, license_input=None, ref_code_input=None):
    email = email.lower().strip()
    try:
        res = supabase.table('users').select("*").eq('email', email).execute()
        user = res.data[0] if res.data else None
    except: user = None

    if not user:
        referrer_id = None
        if ref_code_input:
            ref_res = supabase.table('users').select("id").eq('referral_code', ref_code_input).execute()
            if ref_res.data: referrer_id = ref_res.data[0]['id']

        new_data = {
            "email": email,
            "referral_code": generate_referral_code(email),
            "role": "student",
            "is_pro": False,
            "level": 1,
            "xp": 0,
            "referred_by": referrer_id
        }
        
        if license_input and license_input.startswith("PRO-"):
            new_data['is_pro'] = True
            new_data['license_key'] = license_input
            new_data['xp'] = 500
            
        res = supabase.table('users').insert(new_data).execute()
        user = res.data[0]
        st.toast(f"🎉 Account aangemaakt!", icon="📧")
        # send_welcome_email(email, user['referral_code']) # Uncomment als mail werkt

    st.session_state.user = user
    st.session_state.is_pro = user['is_pro']
    
    if license_input and not user['is_pro']:
        if license_input.startswith("PRO-"):
            supabase.table('users').update({"is_pro": True, "license_key": license_input}).eq('id', user['id']).execute()
            st.session_state.user['is_pro'] = True
            st.session_state.is_pro = True
            st.balloons()

    st.toast("Succesvol ingelogd!", icon="🚀")
    time.sleep(0.5)

def get_progress():
    if "user" not in st.session_state: return []
    try:
        res = supabase.table('progress').select("step_id").eq('user_id', st.session_state.user['id']).execute()
        return [r['step_id'] for r in res.data]
    except: return []

def mark_step_complete(step_id, xp_reward):
    uid = st.session_state.user['id']
    try:
        supabase.table('progress').insert({"user_id": uid, "step_id": step_id}).execute()
        
        current_xp = st.session_state.user['xp']
        new_xp = current_xp + xp_reward
        update_data = {"xp": new_xp}
        
        old_title, _ = get_rank_info(current_xp)
        new_title, _ = get_rank_info(new_xp)
        
        if current_xp < 500 and new_xp >= 500:
            update_data["level"] = 2
            st.session_state.user['level'] = 2
            now = datetime.now(timezone.utc)
            end_time = now + timedelta(hours=24)
            update_data["spy_unlock_until"] = end_time.isoformat()
            st.session_state.user['spy_unlock_until'] = end_time.isoformat()
            st.balloons()
            st.success("🔓 GEFELICITEERD! Spy Tool 24u ontgrendeld!")
            time.sleep(3)

        elif current_xp < 550 and new_xp >= 550:
            now = datetime.now(timezone.utc)
            end_time = now + timedelta(hours=24)
            update_data["scripts_unlock_until"] = end_time.isoformat()
            st.session_state.user['scripts_unlock_until'] = end_time.isoformat()
            st.snow()
            st.success("Video Scripts Tool Ontgrendeld!")
            time.sleep(4)
        
        elif new_title != old_title:
            st.toast(f"🆙 PROMOTIE! Je bent nu: {new_title}", icon="⭐")
            st.balloons()
            time.sleep(2)
            
        supabase.table('users').update(update_data).eq('id', uid).execute()
        st.session_state.user['xp'] = new_xp
        st.toast(f"✅ Voltooid! +{xp_reward} XP", icon="🔥")
             
    except Exception as e:
        print(f"Error: {e}")

def get_affiliate_stats():
    uid = st.session_state.user['id']
    try:
        res = supabase.table('users').select("is_pro").eq('referred_by', uid).execute()
        total = len(res.data)
        pro = sum(1 for u in res.data if u['is_pro'])
        return total, pro, pro * 5
    except: return 0, 0, 0