import streamlit as st
import random
import string
import time
import smtplib
from datetime import datetime, timezone, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from supabase import create_client

# --- CONFIGURATIE ---
# [BELANGRIJK] Vul hier de link in naar jouw live app, zodat de link in de email werkt.
APP_URL = "https://rmacademy.onrender.com" 

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
        response = supabase.table('users').select('email, xp').gt('xp', 0).limit(20).execute()
        users = response.data
        
        if not users: return "⚡ Live: Wachten op eerste studenten..."
        
        user = random.choice(users)
        email_name = user['email'].split('@')[0].capitalize()
        
        msgs = [
            f" {email_name} is net gestegen in rang!",
            f" {email_name} heeft +50 XP verdiend.",
            f" {email_name} is druk bezig in Fase 2.",
            f" {email_name} gebruikt de Spy Tool.",
            f" {email_name} is bezig met KVK inschrijving."
        ]
        return random.choice(msgs)
    except:
        return "⚡ Live: Druk bezig in de community..."

# --- ECHTE EMAIL FUNCTIE (MOOI OPGEMAAKT) ---
def send_welcome_email(to_email, referral_code):
    try:
        smtp_server = st.secrets["email"]["smtp_server"]
        smtp_port = st.secrets["email"]["smtp_port"]
        smtp_user = st.secrets["email"]["smtp_user"]
        smtp_password = st.secrets["email"]["smtp_password"]
        sender_email = st.secrets["email"]["sender_email"]

        # Maak de directe link aan (zorg dat je app dit leest uit query params)
        referral_link = f"{APP_URL}?ref_code={referral_code}"

        subject = "🚀 Welkom bij RM Ecom Academy - Start & Verdien"
        
        # HTML Email Design
        body = f"""
        <html>
          <body style="font-family: 'Helvetica', 'Arial', sans-serif; background-color: #f3f4f6; margin: 0; padding: 0;">
            <div style="max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                
                <!-- HEADER -->
                <div style="background-color: #2563EB; padding: 30px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 24px;">RM Ecom Academy</h1>
                </div>

                <!-- CONTENT -->
                <div style="padding: 40px 30px; color: #334155; line-height: 1.6;">
                    <h2 style="color: #0F172A; margin-top: 0;">Welkom aan boord! 🚀</h2>
                    <p>Je account is succesvol aangemaakt. Je kunt nu direct starten met de gratis roadmap om je eerste sales te genereren.</p>
                    
                    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;">

                    <h3 style="color: #0F172A;">💰 Verdien €250 per Student</h3>
                    <p>Ken jij iemand anders die ook een webshop wil starten? Nodig ze uit en ontvang <strong>€250 commissie</strong> zodra zij Student worden.</p>

                    <p style="margin-bottom: 5px; font-weight: bold;">Jouw Vrienden Code:</p>
                    <div style="background: #f1f5f9; padding: 15px; border-radius: 8px; border: 1px dashed #cbd5e1; text-align: center; margin-bottom: 20px;">
                        <span style="font-size: 24px; color: #2563EB; font-weight: 800; letter-spacing: 1px;">{referral_code}</span>
                    </div>

                    <p style="margin-bottom: 5px; font-weight: bold;">Jouw Directe Link:</p>
                    <p style="font-size: 14px; color: #64748b; margin-top: 0;">Deel deze link, dan wordt jouw code automatisch ingevuld:</p>
                    <a href="{referral_link}" style="display: block; background-color: #2563EB; color: #ffffff; text-decoration: none; text-align: center; padding: 12px; border-radius: 8px; font-weight: bold; margin-top: 10px;">
                        🔗 Kopieer Jouw Link
                    </a>
                    <p style="font-size: 12px; color: #94a3b8; text-align: center; margin-top: 5px;">{referral_link}</p>
                </div>

                <!-- FOOTER -->
                <div style="background-color: #f8fafc; padding: 20px; text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #e2e8f0;">
                    <p>&copy; 2024 RM Ecom Academy. Alle rechten voorbehouden.</p>
                </div>
            </div>
          </body>
        </html>
        """

        msg = MIMEMultipart()
        msg['From'] = f"RM Ecom Academy <{sender_email}>"
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
        # --- NIEUWE GEBRUIKER REGISTREREN ---
        referrer_id = None
        
        # Check of er een referral code is ingevuld
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
        
        # Check of er direct PRO licentie is ingevuld
        if license_input and license_input.startswith("PRO-"):
            new_data['is_pro'] = True
            new_data['license_key'] = license_input
            new_data['xp'] = 500
            
        res = supabase.table('users').insert(new_data).execute()
        user = res.data[0]
        
        st.toast(f"🎉 Account aangemaakt!", icon="📧")
        
        # --- EMAIL VERSTUREN (INGESCHAKELD) ---
        # Stuurt de welkomstmail met de referral code en link
        send_welcome_email(email, user['referral_code'])

    st.session_state.user = user
    st.session_state.is_pro = user['is_pro']
    
    # Check of bestaande user nu PRO code invult
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
        
        # Unlock logica
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
        
        # AANGEPAST: 250 EURO PER STUDENT
        return total, pro, pro * 250
    except: return 0, 0, 0

def get_user_by_email(email):
    """Haalt gebruiker op basis van email op zonder nieuwe login flow."""
    try:
        res = supabase.table('users').select("*").eq('email', email).execute()
        if res.data:
            return res.data[0]
    except:
        return None
    return None