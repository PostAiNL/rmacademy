import streamlit as st
import random
import string
import time
import smtplib
import hashlib
import os  # NIEUW: Nodig voor Render environment variables
from datetime import datetime, timezone, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from supabase import create_client

# --- CONFIGURATIE ---
APP_URL = "https://rmacademy.onrender.com" 

RANKS = {
    0: "🐣 Starter",
    200: "🔨 Bouwer",
    500: "🚀 Expert",       
    1000: "👑 E-com Boss",
    3000: "💎 Legend",
    5000: "🔥 Master",
    10000: "🦄 Grandmaster"
}

# CONNECTIE MET SUPABASE (Verbeterd voor Render)
@st.cache_resource
def init_supabase():
    try:
        # Check eerst Render Environment Variables, dan pas st.secrets
        url = os.environ.get("SUPABASE_URL") or st.secrets.get("supabase", {}).get("url")
        key = os.environ.get("SUPABASE_KEY") or st.secrets.get("supabase", {}).get("key")
        
        if not url or not key:
            st.error("Supabase URL of Key ontbreekt in de instellingen!")
            return None
            
        return create_client(url, key)
    except Exception as e:
        st.error(f"Supabase Connectie Fout: {e}")
        return None

supabase = init_supabase()

# --- HULPFUNCTIE: BEPAAL RANG ---
def get_rank_info(xp):
    current_title = "🐣 Starter"
    next_xp = 200
    sorted_ranks = sorted(RANKS.items())
    for i, (threshold, title) in enumerate(sorted_ranks):
        if xp >= threshold:
            current_title = title
            if i + 1 < len(sorted_ranks):
                next_xp = sorted_ranks[i+1][0]
            else:
                next_xp = threshold * 2
        else:
            break
    return current_title, next_xp

# --- DATA OPHALEN VOOR LEADERBOARD ---
def get_leaderboard_data():
    if not supabase: return []
    try:
        response = supabase.table('users').select('email, first_name, xp, level, is_pro').order('xp', desc=True).limit(10).execute()
        leaderboard = []
        for i, u in enumerate(response.data):
            display_name = u.get('first_name') or u['email'].split('@')[0].capitalize()
            title, _ = get_rank_info(u['xp'])
            leaderboard.append({
                "rank": i + 1,
                "name": display_name,
                "xp": u['xp'],
                "title": title,
                "is_pro": u['is_pro']
            })
        return leaderboard
    except: return []

# --- LOGIN / REGISTER ---
def login_or_register(email, license_input=None, ref_code_input=None, name_input=None):
    email = email.lower().strip()
    user = None
    if supabase:
        try:
            res = supabase.table('users').select("*").eq('email', email).execute()
            if res.data: user = res.data[0]
        except Exception as e:
            st.error(f"Inloggen mislukt: {e}")

    if not user:
         st.session_state.user = {
            "id": "temp",
            "email": email,
            "first_name": name_input or "Gast",
            "xp": 0, "level": 1, "is_pro": False, "referral_code": "TEMP"
         }
         return

    st.session_state.user = user
    st.session_state.is_pro = user.get('is_pro', False)
    st.toast("Succesvol ingelogd!", icon="🚀")

def get_progress():
    if "user" not in st.session_state or not supabase: return []
    try:
        if st.session_state.user['id'] == 'temp': return []
        res = supabase.table('progress').select("step_id").eq('user_id', st.session_state.user['id']).execute()
        return [r['step_id'] for r in res.data]
    except: return []

def mark_step_complete(step_id, xp_reward):
    if "user" not in st.session_state: return
    
    # Live voortgang opslaan
    if st.session_state.user['id'] == 'temp':
        st.session_state.user['xp'] += xp_reward
        return

    uid = st.session_state.user['id']
    if not supabase: return

    try:
        # 1. Check of stap al in DB staat
        check = supabase.table('progress').select('*').eq('user_id', uid).eq('step_id', step_id).execute()
        if check.data: 
            return 

        # 2. Voeg toe aan progress tabel
        supabase.table('progress').insert({"user_id": uid, "step_id": step_id}).execute()
        
        # 3. Bereken nieuwe XP en Level
        current_xp = st.session_state.user.get('xp', 0)
        new_xp = current_xp + xp_reward
        
        # Bereken level nummer (1, 2, 3, etc)
        sorted_ranks = sorted(RANKS.items())
        new_level = 1
        for i, (threshold, title) in enumerate(sorted_ranks):
            if new_xp >= threshold:
                new_level = i + 1
            else:
                break
        
        old_title, _ = get_rank_info(current_xp)
        new_title, _ = get_rank_info(new_xp)
        
        # 4. Update de users tabel (XP ÉN LEVEL)
        res_user = supabase.table('users').update({
            "xp": new_xp, 
            "level": new_level
        }).eq('id', uid).execute()

        if res_user.data:
            st.session_state.user['xp'] = new_xp
            st.session_state.user['level'] = new_level
            
            if new_title != old_title:
                st.balloons()
                st.success(f"🏆 Promotie naar {new_title}!")
             
    except Exception as e:
        st.error(f"Fout bij opslaan: {e}")

def get_affiliate_stats():
    if "user" not in st.session_state or st.session_state.user['id'] == 'temp' or not supabase: 
        return 0, 0, 0
    try:
        res = supabase.table('users').select("is_pro").eq('referred_by', st.session_state.user['id']).execute()
        total = len(res.data)
        pro = sum(1 for u in res.data if u['is_pro'])
        return total, pro, pro * 250
    except: return 0, 0, 0

def send_welcome_email(email, first_name, password):
    try:
        smtp_config = st.secrets["smtp"]
        secret_key = st.secrets["supabase"]["key"]
        login_token = hashlib.sha256(f"{email}{secret_key}".encode()).hexdigest()
        magic_link = f"{APP_URL}/?autologin={login_token}&user={email}"
        
        # LOGO URL - Vervang dit door de directe link naar je logo afbeelding
        logo_url = "https://www.rmacademy.nl/cdn/shop/files/Ontwerp_zonder_titel_255b5006-5ae5-4298-a452-e75045d79ae0.png?v=1754056357&width=600" # Zet hier je eigen logo link

        msg = MIMEMultipart()
        msg['From'] = f"RM Ecom Academy <{smtp_config['user']}>"
        msg['To'] = email
        msg['Subject'] = f"Welkom in onze academy, {first_name}! 🚀"

        html_body = f"""
        <html>
        <head>
            <style>
                .button {{
                    display: inline-block; padding: 14px 30px; background-color: #2563EB; color: #ffffff !important; 
                    text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; margin: 10px 0;
                }}
                .card {{
                    background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 20px; border-radius: 12px; margin: 20px 0;
                }}
                .step-circle {{
                    display: inline-block; width: 24px; height: 24px; background-color: #FBBF24; color: #000; 
                    border-radius: 50%; text-align: center; line-height: 24px; font-weight: bold; font-size: 14px; margin-right: 10px;
                }}
            </style>
        </head>
        <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #0F172A; line-height: 1.6; padding: 0; margin: 0; background-color: #ffffff;">
            <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px;">
                
                <!-- Logo Section -->
                <div style="text-align: center; margin-bottom: 30px;">
                    <img src="{logo_url}" alt="RM Ecom Academy" style="width: 150px; height: auto;">
                </div>

                <!-- Hero Section -->
                <div style="text-align: center;">
                    <h1 style="font-size: 26px; font-weight: 800; margin-bottom: 10px; color: #0F172A;">Level 1 Ontgrendeld. <br>Welkom bij de Academy, {first_name}!</h1>
                    <p style="font-size: 16px; color: #64748B;">Je staat aan de start van je eigen e-commerce imperium. We gaan direct aan de slag om je eerste sales te realiseren.</p>
                </div>

                <!-- Action Section -->
                <div style="text-align: center; margin: 30px 0;">
                    <p style="font-weight: bold; margin-bottom: 5px;">STAP 1: START JE ROUTMAP</p>
                    <a href="{magic_link}" class="button">Naar mijn Dashboard 🚀</a>
                    <p style="font-size: 12px; color: #94A3B8; margin-top: 10px;">(Je wordt automatisch ingelogd via deze knop)</p>
                </div>

                <!-- Account Credentials Card -->
                <div class="card">
                    <p style="margin-top: 0; font-weight: bold; font-size: 14px; color: #64748B; letter-spacing: 1px; text-transform: uppercase;">Jouw Toegangspas</p>
                    <table style="width: 100%;">
                        <tr>
                            <td style="padding: 5px 0; color: #0F172A;"><strong>Email:</strong></td>
                            <td style="padding: 5px 0; color: #2563EB;">{email}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0; color: #0F172A;"><strong>Wachtwoord:</strong></td>
                            <td style="padding: 5px 0; color: #0F172A;">{password}</td>
                        </tr>
                    </table>
                </div>

                <!-- What's Next Section -->
                <div style="margin-top: 40px;">
                    <h3 style="font-size: 18px; border-bottom: 2px solid #F1F5F9; padding-bottom: 10px;">Wat gaan we vandaag doen?</h3>
                    
                    <div style="margin-top: 20px; display: flex; align-items: flex-start;">
                        <span class="step-circle">1</span>
                        <div>
                            <p style="margin: 0; font-weight: bold;">De Roadmap Starten</p>
                            <p style="margin: 0; font-size: 14px; color: #64748B;">Open je dashboard en voltooi 'Fase 1: De Fundering'.</p>
                        </div>
                    </div>

                    <div style="margin-top: 20px; display: flex; align-items: flex-start;">
                        <span class="step-circle" style="background-color: #22C55E; color: white;">2</span>
                        <div>
                            <p style="margin: 0; font-weight: bold;">Gratis Mini-Training</p>
                            <p style="margin: 0; font-size: 14px; color: #64748B;">Ga in het menu naar 'Academy' en bekijk de eerste 4 video's.</p>
                        </div>
                    </div>
                </div>

                <!-- Footer -->
                <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #F1F5F9; text-align: center;">
                    <p style="font-size: 14px; color: #94A3B8;">Vragen? We staan voor je klaar in de community.</p>
                    <p style="font-size: 12px; color: #CBD5E1;">© 2026 RM Ecom Academy. Alle rechten voorbehouden.</p>
                </div>

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
    except Exception as e:
        print(f"FOUT BIJ VERSTUREN EMAIL: {str(e)}")
        return False