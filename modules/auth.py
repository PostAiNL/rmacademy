import streamlit as st
import random
import string
import time
import smtplib
import hashlib
import os
from datetime import datetime, timezone, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from supabase import create_client

# --- CONFIGURATIE ---
APP_URL = "https://app.rmacademy.nl" 

RANKS = {
    0: "🐣 Starter",
    200: "🔨 Bouwer",
    500: "🚀 Expert",       
    1000: "👑 E-com Boss",
    3000: "💎 Legend",
    5000: "🔥 Master",
    10000: "🦄 Grandmaster"
}

@st.cache_resource
def init_supabase():
    try:
        url = os.environ.get("SUPABASE_URL") or st.secrets.get("supabase", {}).get("url")
        key = os.environ.get("SUPABASE_KEY") or st.secrets.get("supabase", {}).get("key")
        if not url or not key: return None
        return create_client(url, key)
    except:
        return None

supabase = init_supabase()

def get_rank_info(xp):
    current_title = "🐣 Starter"
    next_xp = 200
    sorted_ranks = sorted(RANKS.items())
    for i, (threshold, title) in enumerate(sorted_ranks):
        if xp >= threshold:
            current_title = title
            next_xp = sorted_ranks[i+1][0] if i + 1 < len(sorted_ranks) else threshold * 2
        else: break
    return current_title, next_xp

def login_or_register(email, license_input=None, ref_code_input=None, name_input=None):
    email = email.lower().strip()
    if not supabase: return None
    try:
        res = supabase.table('users').select("*").eq('email', email).execute()
        if res.data:
            user_data = res.data[0]
            st.session_state.user = user_data
            st.session_state.is_pro = user_data.get('is_pro', False)
            return user_data
        return None
    except:
        return None

@st.cache_data(ttl=60, show_spinner=False)
def get_progress():
    if "user" not in st.session_state or not supabase: return []
    try:
        uid = st.session_state.user.get('id')
        if not uid or uid == 'temp': return []
        res = supabase.table('progress').select("step_id").eq('user_id', uid).execute()
        return [r['step_id'] for r in res.data]
    except: return []

def mark_step_complete(step_id, xp_reward):
    if "user" not in st.session_state or not supabase: return
    user = st.session_state.user
    uid = user.get('id')
    if not uid or uid == 'temp': return
    try:
        check = supabase.table('progress').select('*').eq('user_id', uid).eq('step_id', step_id).execute()
        if check.data: return 
        supabase.table('progress').insert({"user_id": uid, "step_id": step_id}).execute()
        new_xp = user.get('xp', 0) + xp_reward
        new_level = 1
        sorted_ranks = sorted(RANKS.items())
        for i, (threshold, title) in enumerate(sorted_ranks):
            if new_xp >= threshold: new_level = i + 1
            else: break
        supabase.table('users').update({"xp": new_xp, "level": new_level}).eq('id', uid).execute()
        st.session_state.user['xp'] = new_xp
        st.session_state.user['level'] = new_level
    except:
        pass

def get_affiliate_stats():
    if "user" not in st.session_state or not supabase: return 0, 0, 0
    try:
        res = supabase.table('users').select("is_pro").eq('referred_by', st.session_state.user['id']).execute()
        pro = sum(1 for u in res.data if u['is_pro'])
        return len(res.data), pro, pro * 250
    except: return 0, 0, 0

def send_welcome_email(email, first_name, password):
    try:
        smtp_config = st.secrets["smtp"]
        secret_key = st.secrets["supabase"]["key"]
        login_token = hashlib.sha256(f"{email}{secret_key}".encode()).hexdigest()
        magic_link = f"{APP_URL}/?autologin={login_token}&user={email}"
        
        logo_url = "https://www.rmacademy.nl/cdn/shop/files/Ontwerp_zonder_titel_255b5006-5ae5-4298-a452-e75045d79ae0.png?v=1754056357&width=600"

        msg = MIMEMultipart()
        msg['From'] = f"RM Ecom Academy <{smtp_config['user']}>"
        msg['To'] = email
        msg['Subject'] = f"Welkom in onze academy, {first_name}! 🚀"

        html_body = f"""
        <html>
        <body style="font-family: sans-serif; color: #0F172A;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <img src="{logo_url}" style="width: 150px; margin-bottom: 20px;">
                <h2>Welkom bij de Academy, {first_name}!</h2>
                <p>Klik op de knop hieronder om direct in te loggen op je dashboard:</p>
                <a href="{magic_link}" style="display:inline-block; padding: 14px 30px; background:#2563EB; color:white; text-decoration:none; border-radius:8px; font-weight:bold;">Naar mijn Dashboard 🚀</a>
                <br><br>
                <p><b>Jouw gegevens:</b><br>Email: {email}<br>Wachtwoord: {password}</p>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, 'html'))
        server = smtplib.SMTP_SSL(smtp_config['server'], 465)
        server.login(smtp_config['user'], smtp_config['password'])
        server.send_message(msg)
        server.quit()
        return True
    except: return False
