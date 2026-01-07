import streamlit as st
import time
import urllib.parse
import random
import pandas as pd
import textwrap
import base64 
import os
from PIL import Image
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta, timezone
import extra_streamlit_components as stx
from modules import ai_coach, ui, auth, shopify_client, competitor_spy, roadmap, db

# --- 0. CONFIGURATIE ---
STRATEGY_CALL_URL = "https://www.paypro.nl/product/RM_Academy_APP_PRO/125684"
COMMUNITY_URL = "https://discord.gg/fCWhU6MC"
COACH_VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 

# Functie om afbeelding om te zetten naar Base64 string (voor icoon fix)
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Probeer het logo te laden als PIL image (voor Streamlit config)
fav_icon = "🚀"
logo_path = "assets/logo.png"
try:
    fav_icon = Image.open(logo_path) 
except:
    pass

st.set_page_config(
    page_title="RM Ecom Academy",
    page_icon=fav_icon,
    layout="wide",
    initial_sidebar_state="auto"
)

# --- 1.5 META TAGS & PWA ICON FIX (BASE64) ---
logo_b64 = get_base64_image(logo_path)
if logo_b64:
    icon_html = f'<link rel="icon" type="image/png" href="data:image/png;base64,{logo_b64}">'
    apple_icon_html = f'<link rel="apple-touch-icon" href="data:image/png;base64,{logo_b64}">'
else:
    icon_html = "" 
    apple_icon_html = ""

st.markdown(f"""
<head>
    {icon_html}
    {apple_icon_html}
    <meta name="application-name" content="RM Ecom">
    <meta name="apple-mobile-web-app-title" content="RM Ecom">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
</head>
<script>
    var link = document.querySelector("link[rel~='icon']");
    if (!link) {{
        link = document.createElement('link');
        link.rel = 'icon';
        document.getElementsByTagName('head')[0].appendChild(link);
    }}
    link.href = 'data:image/png;base64,{logo_b64 if logo_b64 else ""}';
</script>
""", unsafe_allow_html=True)

# --- 1. CSS ENGINE (GEOPTIMALISEERD VOOR SNELHEID & LOOKS) ---
st.markdown("""
    <style>
        /* Import Bootstrap Icons */
        @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css");

        /* ==============================================
           ANTI-LAAD SCHERM & SNELHEID FIXES
           ============================================== */
        
        /* Verberg de 'Running Man' / Wielrenner rechtsboven */
        [data-testid="stStatusWidget"] {
            visibility: hidden !important;
            height: 0px !important;
            width: 0px !important;
            display: none !important;
        }

        /* Verberg de gekleurde regenboogbalk bovenaan */
        [data-testid="stDecoration"] {
            display: none !important;
        }

        /* CRUCIAAL: Verberg de grijze waas/blur tijdens het laden */
        [data-testid="stOverlay"], .stOverlay {
            display: none !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        
        /* Zorg dat de header transparant blijft */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
            z-index: 1 !important;
        }

        /* ==============================================
           ALGEMENE CONFIGURATIE
           ============================================== */
        :root {
            --primary: #2563EB;
            --bg-light: #F8FAFC;
            --text-dark: #0F172A;
            --white: #FFFFFF;
            --border: #CBD5E1;
            color-scheme: light !important; 
        }

        .stApp {
            background-color: var(--bg-light) !important;
            color: var(--text-dark) !important;
        }

        .bi { margin-right: 6px; vertical-align: -0.125em; }
        h1, h2, h3 { color: #0F172A !important; }
        p, .stMarkdown, .stCaption, [data-testid="stCaptionContainer"], small { color: #0F172A !important; }
        * { -webkit-tap-highlight-color: transparent !important; }

        /* ==============================================
           UI ELEMENTEN
           ============================================== */
        /* De Hamburger Knop */
        button[kind="header"] {
            background-color: #EFF6FF !important; 
            border: 1px solid #DBEAFE !important; 
            border-radius: 8px !important;
            color: #0F172A !important;
            opacity: 1 !important;
            margin-top: 2px !important;
            height: 40px !important;
            width: 40px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        button[kind="header"] svg {
            fill: #2563EB !important;
            stroke: #2563EB !important;
            width: 24px !important;
            height: 24px !important;
        }

        /* Mobiele Sidebar Fixes */
        @media (max-width: 992px) {
            section[data-testid="stSidebar"] {
                background-color: #FFFFFF !important;
                border-right: 1px solid #E2E8F0 !important;
            }
            [data-testid="stSidebarCollapseButton"] {
                background-color: #F1F5F9 !important;
                border-radius: 50% !important;
                border: 1px solid #E2E8F0 !important;
                color: #0F172A !important;
                width: 36px !important;
                height: 36px !important;
                margin-right: 10px !important;
                margin-top: 10px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                z-index: 999999 !important;
            }
            [data-testid="stSidebarCollapseButton"] svg {
                fill: #0F172A !important;
                stroke: #0F172A !important;
            }
            [data-testid="stSidebarCollapsedControl"] {
                color: #0F172A !important;
                background-color: white !important;
                display: block !important;
                z-index: 999999 !important;
                border: 1px solid #000 !important;
            }
        }
        
        [data-testid="stHeaderActionElements"] { display: none !important; }
        #MainMenu { visibility: hidden !important; }
        footer { visibility: hidden !important; }

        .block-container {
            padding-top: 2rem !important; 
            padding-bottom: 5rem !important;
            max-width: 1000px;
        }
        
        h1 { 
            font-size: 1.8rem !important; 
            font-weight: 800 !important; 
            letter-spacing: 0px !important; 
            color: #0F172A !important; 
            margin-top: 3px !important; 
            padding-top: 0px !important;
            margin-bottom: 10px !important;
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem !important; 
            padding-left: 1rem !important; 
            padding-right: 1rem !important;
        }

        /* Inputs & Knoppen */
        input, textarea, select, .stTextInput > div > div > input {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border: 1px solid #CBD5E1 !important;
            -webkit-text-fill-color: #0F172A !important;
            opacity: 1 !important;
        }
        .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextarea label, label p {
            color: #0F172A !important;
            font-weight: 600 !important;
        }
        
        div.stButton > button[kind="primary"] { background-color: #2563EB !important; border-color: #2563EB !important; color: white !important; }
        div.stButton > button[kind="primary"]:hover { background-color: #1D4ED8 !important; border-color: #1D4ED8 !important; }
        div.stButton > button:not([kind="primary"]) { background-color: #FFFFFF !important; color: #0F172A !important; border: 1px solid #CBD5E1 !important; }
        div.stButton > button:not([kind="primary"]):hover { border-color: #2563EB !important; color: #2563EB !important; background-color: #F8FAFC !important; }
        
        /* Klik effect voor sneller gevoel */
        div.stButton > button:active { transform: scale(0.98); }

        /* EXPANDER FIX: Ronde hoeken zonder dubbele strepen */
        div[data-testid="stExpander"] {
            border: none !important;
            box-shadow: none !important;
            background-color: transparent !important;
        }

        details {
            border-radius: 20px !important;
            overflow: hidden;
            border: 1px solid #BAE6FD !important; /* De hoofdrand */
            margin-bottom: 15px;
            background-color: white !important;
        }

        details > summary {
            background-color: #EFF6FF !important;
            border: none !important;
            padding: 10px 20px !important;
            color: #0F172A !important;
            list-style: none;
        }

        details > summary:hover {
            background-color: #E0F2FE !important;
        }

        /* DE FIX: Verwijder de automatische streep van Streamlit tussen kop en inhoud */
        details[open] > summary {
            border-bottom: none !important;
        }

        /* Target de interne container van de expander content */
        div[data-testid="stExpanderDetails"] {
            border-top: none !important; /* Verwijdert de irritante streep */
            padding-top: 15px !important;
        }

        .streamlit-expanderContent {
            border: none !important;
            background-color: white !important;
        }

        /* STATS GRID */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 16px; background: var(--white); border: 1px solid var(--border);
            padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        .stat-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 25px; margin-top: 10px; }
        .stat-card { background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 12px 4px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.02); display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .stat-icon { font-size: 0.75rem; color: #64748B; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; white-space: nowrap; }
        .stat-value { font-size: 1.4rem; font-weight: 800; color: #0F172A; line-height: 1.2; }
        .stat-sub { font-size: 0.7rem; color: #94A3B8; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; }

/* Verbeterde Mobiele Optimalisatie */
    @media (max-width: 600px) {
        /* 1. Meer ruimte onderin de uitklap-vakken (Fases & Uitleg) */
        div[data-testid="stExpanderDetails"] {
            padding-bottom: 30px !important; /* Dit zorgt voor witruimte onder de knop */
            padding-left: 15px !important;
            padding-right: 15px !important;
        }

        /* 2. De Gouden Knop extra ruimte geven */
        div[style*="background: linear-gradient(135deg, #FFD700"] {
            margin-top: 20px !important;
            margin-bottom: 10px !important; /* Ruimte tussen knop en de rand van het witte vlak */
            padding: 16px !important;
        }

        /* 3. De blauwe aanbevelingskaart ("Wat ga je verkopen?") */
        div[style*="background: linear-gradient(135deg, #2563EB"] {
            padding: 20px !important;
            border-radius: 15px !important;
        }

        /* 4. Lettergrootte van de titel in de blauwe kaart iets verkleinen voor mobiel */
        div[style*="font-size: 1.8rem"] {
            font-size: 1.4rem !important;
            line-height: 1.2 !important;
        }

        /* 5. De tekst in de 'Daily Habit' (groene balk) */
        .stAlert div {
            font-size: 0.85rem !important;
        }
    }

        /* LEVEL UP OVERLAY */
        @keyframes popIn { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        .levelup-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(15, 23, 42, 0.9); z-index: 9999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            animation: popIn 0.5s ease-out forwards;
        }
        .levelup-card {
            background: white; padding: 40px; border-radius: 20px; text-align: center; max-width: 400px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.3); border: 2px solid #FBBF24;
        }
        
        /* VISUAL ROADMAP */
        .progress-container { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; position: relative; padding: 0 10px; width: 100%; }
        .progress-line { position: absolute; top: 15px; left: 0; width: 100%; height: 3px; background: #E2E8F0; z-index: 1; }
        .progress-step { width: 32px; height: 32px; border-radius: 50%; display: flex; justify-content: center; align-items: center; z-index: 2; position: relative; background: white; border: 2px solid #E2E8F0; color: #94A3B8; font-weight: bold; font-size: 0.8rem; transition: all 0.3s; }
        .progress-step.active { border-color: #2563EB; color: white; background: #2563EB; box-shadow: 0 0 0 4px rgba(37,99,235,0.1) !important; }
        .progress-step.completed { background: #10B981; border-color: #10B981; color: white; }
        .progress-label { position: absolute; bottom: -25px; left: 50%; transform: translateX(-50%); font-size: 0.7rem; white-space: nowrap; color: #64748B; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- 2. COOKIE MANAGER ---
cookie_manager = stx.CookieManager()

# 1. Check op Magic Link (Autologin via email)
if "autologin" in st.query_params and "user" in st.query_params:
    token = st.query_params["autologin"]
    email = st.query_params["user"]
    
    # Controleer of de token klopt
    import hashlib
    secret_key = st.secrets["supabase"]["key"]
    expected_token = hashlib.sha256(f"{email}{secret_key}".encode()).hexdigest()
    
    if token == expected_token:
        # Token is valide, log de gebruiker in
        auth.login_or_register(email)
        cookie_manager.set("rmecom_user_email", email, expires_at=datetime.now() + timedelta(days=30), path="/")
        
        # Ruim de URL op
        st.query_params.clear()
        st.rerun()

# --- INITIALISEER PAGINA STATUS ---
if "view" not in st.session_state:
    st.session_state.view = "main"

def set_view(name):
    st.session_state.view = name
    st.rerun()

# Check of we de gebruiker moeten inloggen
if "user" not in st.session_state:
    # Belangrijk: Geef de browser tijd om cookies te verzenden (Render fix)
    time.sleep(0.6) 
    all_cookies = cookie_manager.get_all()
    
    # Debug (optioneel): st.write(all_cookies)
    
    if all_cookies and "rmecom_user_email" in all_cookies:
        cookie_email = all_cookies["rmecom_user_email"]
        if cookie_email and len(cookie_email) > 3: # Check of het een echt emailadres is
            auth.login_or_register(cookie_email)
            st.rerun()

# --- 3. LOGIN SCHERM (PIXEL PERFECT MOBILE) ---
if "user" not in st.session_state:
    if "status" in st.query_params: st.query_params.clear()
    
    st.markdown("""
    <style>
        div.stButton > button[kind="primary"] { 
            background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important;
            border: 1px solid #B45309 !important;
            color: white !important;
            font-weight: 800 !important;
            font-size: 1rem !important;
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
            box-shadow: 0 4px 6px rgba(245, 158, 11, 0.3);
            transition: all 0.2s;
            margin-top: 0px !important;
        }
        div.stButton > button[kind="primary"]:hover { 
            transform: scale(1.02);
            box-shadow: 0 6px 12px rgba(245, 158, 11, 0.4);
        }
        .compact-title {
            font-size: 1.8rem !important;
            line-height: 1.2 !important;
            margin-bottom: 5px !important;
            margin-top: 0px !important;
            font-weight: 800 !important;
        }
        .compact-sub {
            font-size: 0.95rem !important;
            color: #64748B !important;
            line-height: 1.4 !important;
            margin-bottom: 15px !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 20px !important;
            padding-top: 15px !important;
            padding-bottom: 15px !important;
        }
        @media only screen and (max-width: 600px) {
            .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
            .compact-title { font-size: 1.35rem !important; margin-bottom: 4px !important; line-height: 1.2 !important; }
            .compact-sub { font-size: 0.85rem !important; margin-bottom: 8px !important; line-height: 1.3 !important; }
            .logo-text { font-size: 0.8rem !important; margin-bottom: 0px !important; }
            div[data-testid="stVerticalBlockBorderWrapper"] > div { padding: 12px !important; padding-top: 10px !important; }
            div[data-testid="stExpander"] { margin-bottom: 0px !important; }
            .stTextInput { margin-bottom: 0px !important; }
            div[class*="stGap"] { gap: 0.5rem !important; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1.1], gap="large", vertical_alignment="center")
    
    with col_left:
        st.markdown("<div class='logo-text' style='font-size: 0.9rem; font-weight: 600; color: #475569; margin-bottom: 0px;'><i class='bi bi-lightning-charge-fill' style='color:#2563EB;'></i> RM Ecom Academy</div>", unsafe_allow_html=True)
        st.markdown("""
        <h1 class='compact-title'>
            Van 0 naar <span style='color:#166534; background: #DCFCE7; padding: 0 6px; border-radius: 6px;'>€15k/maand</span> met je eigen webshop.
        </h1>
        <p class='compact-sub'>
            De enige app die je stap-voor-stap begeleidt. Geen technische kennis nodig. Start vandaag <b>gratis</b>.
        </p>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            tab_free, tab_pro = st.tabs(["Nieuw Account", "Inloggen"])
            with tab_free:
                col_name, col_email = st.columns(2)
                first_name = col_name.text_input("Voornaam", placeholder="Je naam...", label_visibility="collapsed", key="reg_name")
                email = col_email.text_input("Email", placeholder="Je email...", label_visibility="collapsed", key="reg_email")
                password = st.text_input("Wachtwoord verzinnen", placeholder="Wachtwoord...", type="password", label_visibility="collapsed", key="reg_pass")
                with st.expander("Heb je een vriendencode?"):
                    ref_code = st.text_input("Vriendencode", placeholder="bv. JAN-482", label_visibility="collapsed", key="ref_code_input")
                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                if st.button("Start direct (gratis)", type="primary", use_container_width=True):
                    if email and "@" in email and first_name and password:
                        with st.spinner("Account aanmaken..."):
                            status = db.create_user(email, password, first_name)
                            if status == "SUCCESS":
                                auth.send_welcome_email(email, first_name, password)
                                auth.login_or_register(email, ref_code_input=ref_code if 'ref_code' in locals() and ref_code else None, name_input=first_name)
                                cookie_manager.set("rmecom_user_email", email, expires_at=datetime.now() + timedelta(days=30), path="/")
                                st.rerun()
                            elif status == "EXISTS": st.warning("Dit emailadres bestaat al. Probeer in te loggen.")
                            else: st.error("Er ging iets mis met de database.")
                    else: st.warning("Vul alle velden in.")
                st.markdown("""<div style='text-align:center; margin-top:4px; line-height:1.2;'><div style='font-size:0.7rem; color:#475569; font-weight:500;'><i class="bi bi-check-circle-fill" style="font-size:10px; color:#16A34A;"></i> Geen creditcard nodig <span style='color:#CBD5E1;'>|</span> Direct toegang</div></div>""", unsafe_allow_html=True)
                st.markdown("""<div style='display: flex; align-items: center; justify-content: center; gap: 4px; margin-top: 2px; opacity: 1.0;'><div style="color: #F59E0B; font-size: 0.75rem;"><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i></div><span style='font-size: 0.75rem; color: #475569; font-weight: 600;'>4.9/5 (550+ studenten)</span></div>""", unsafe_allow_html=True)
            
            with tab_pro:
                log_email = st.text_input("Email", placeholder="Email...", key="log_email_in")
                log_pass = st.text_input("Wachtwoord", placeholder="Wachtwoord...", type="password", key="log_pass_in")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Inloggen", type="primary", use_container_width=True):
                    if log_email and log_pass:
                        if db.verify_user(log_email, log_pass):
                            auth.login_or_register(log_email)
                            cookie_manager.set("rmecom_user_email", log_email, expires_at=datetime.now() + timedelta(days=30), path="/")
                            st.rerun()
                        else: st.error("Onjuiste gegevens.")
                    else: st.warning("Vul alles in.")
    
    with col_right:
        st.markdown("<br class='desktop-only'>", unsafe_allow_html=True)
        raw_html = """
        <div style="background: white; padding: 30px; border-radius: 20px; border: 1px solid #E2E8F0; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.08); color: #0F172A;">
            <h3 style="margin-top:0; color:#0F172A; font-size:1.1rem; font-weight: 700; margin-bottom: 15px;">Dit krijg je gratis:</h3>
            <div style="display:flex; gap:16px; margin-bottom:20px; align-items:center;">
                <div style="width:48px; height:48px; background:#EFF6FF; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink: 0;"><i class="bi bi-map-fill" style="color:#2563EB;"></i></div>
                <div><h4 style="margin:0; font-size:0.9rem; font-weight:600; color:#1E293B;">De 'Van 0 naar sales' roadmap</h4><p style="margin:0; font-size:0.8rem; color:#64748B;">Stap-voor-stap handleiding.</p></div>
            </div>
            <div style="display:flex; gap:16px; margin-bottom:20px; align-items:center;">
                <div style="width:48px; height:48px; background:#F0FDF4; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink: 0;"><i class="bi bi-robot" style="color:#16A34A;"></i></div>
                <div><h4 style="margin:0; font-size:0.9rem; font-weight:600; color:#1E293B;">Jouw eigen AI coach</h4><p style="margin:0; font-size:0.8rem; color:#64748B;">24/7 hulp bij al je vragen.</p></div>
            </div>
            <div style="display:flex; gap:16px; align-items:center;">
                <div style="width:48px; height:48px; background:#FFF7ED; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink: 0;"><i class="bi bi-trophy-fill" style="color:#EA580C;"></i></div>
                <div><h4 style="margin:0; font-size:0.9rem; font-weight:600; color:#1E293B;">Level-based groei</h4><p style="margin:0; font-size:0.8rem; color:#64748B;">Verdien tools door actie te nemen.</p></div>
            </div>
        </div>
        """
        st.markdown(raw_html.replace("\n", ""), unsafe_allow_html=True)
    st.stop()

# --- 4. INGELOGDE DATA (CACHED & SYNCHRONISED) ---
user = st.session_state.user

# ==============================================================================
# 🔥 DATA SYNC FIX: Haal altijd de laatste XP/Level op uit de Database
# ==============================================================================
if user.get('id') != 'temp' and auth.supabase:
    try:
        # We vragen de database: "Geef me de laatste status van deze gebruiker"
        refresh_data = auth.supabase.table('users').select("*").eq('email', user['email']).execute()
        
        if refresh_data.data:
            # We overschrijven de sessie met de verse data uit de database
            # Hierdoor springt je XP niet terug naar 0 na een refresh
            st.session_state.user.update(refresh_data.data[0])
            user = st.session_state.user # Update de variabele voor de rest van het script
    except Exception as e:
        # Als database faalt, gebruik wat we hebben (geen crash)
        pass 
# ==============================================================================
# 💰 PAYPRO BETALING VERWERKEN (SUCCESS PAGE OVERLAY)
# ==============================================================================
if "payment" in st.query_params and st.query_params["payment"] == "success":
    # 1. Update database & Sessie
    if not user.get('is_pro'):
        db.set_user_pro(user['email'])
        st.session_state.user['is_pro'] = True
        user['is_pro'] = True

    # 2. Toon de "Success" UI (Full Screen Overlay)
    st.markdown("""
        <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: white; z-index: 99999; display: flex; justify-content: center; align-items: center; text-align: center; padding: 20px;">
            <div style="max-width: 500px; padding: 40px; border-radius: 24px; box-shadow: 0 20px 50px rgba(0,0,0,0.1); border: 1px solid #E2E8F0; background: white;">
                <div style="font-size: 80px; margin-bottom: 20px;">🎉</div>
                <h1 style="color: #0F172A; font-size: 2.2rem; margin-bottom: 10px; font-weight: 800;">Welkom bij de Elite!</h1>
                <p style="color: #64748B; font-size: 1.1rem; line-height: 1.6; margin-bottom: 30px;">
                    Je betaling is geslaagd. Je hebt nu onbeperkt toegang tot alle <b>PRO Tools</b>, de <b>Academy</b> en de <b>Daily Winners</b>.
                </p>
                <div style="background: #F0FDF4; border: 1px solid #BBF7D0; padding: 15px; border-radius: 12px; margin-bottom: 30px;">
                    <p style="margin: 0; color: #166534; font-weight: 700; font-size: 0.95rem;">
                        ✅ PRO STATUS: ACTIEF
                    </p>
                </div>
                <a href="/" target="_self" style="text-decoration: none;">
                    <div style="background: #2563EB; color: white; padding: 16px 32px; border-radius: 12px; font-weight: 800; font-size: 1.1rem; cursor: pointer; box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2); transition: transform 0.2s;">
                        Naar mijn Dashboard 🚀
                    </div>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.balloons()
    st.stop() # Dit zorgt dat de rest van de pagina niet laadt achter de overlay

is_pro_license = user.get('is_pro', False)
# ⚠️ TEST MODE AAN (Zet hier een # voor als je live gaat!)
# is_pro_license = True 

@st.cache_data(ttl=300, show_spinner=False)
def get_cached_pro_status(email):
    return db.check_pro_status_db(email), db.get_pro_expiry_date(email)

@st.cache_data(ttl=300, show_spinner=False)
def get_cached_user_data(email):
    return db.get_user_data(email) 

is_temp_pro_db, pro_expiry_dt = get_cached_pro_status(user['email'])
user_extra = get_cached_user_data(user['email'])

# Zorg dat shop naam ook behouden blijft bij refresh
if user_extra and user_extra.get('shop_name'):
    st.session_state.shop_name = user_extra.get('shop_name')
    st.session_state.income_goal = user_extra.get('income_goal')

time_left_str = None
is_temp_pro = False 

if pro_expiry_dt:
    now = datetime.now(timezone.utc)
    if pro_expiry_dt.tzinfo is None:
        pro_expiry_dt = pro_expiry_dt.replace(tzinfo=timezone.utc)
        
    if pro_expiry_dt > now:
        is_temp_pro = True
        diff = pro_expiry_dt - now
        hours = diff.seconds // 3600
        mins = (diff.seconds % 3600) // 60
        time_left_str = f"{hours}u {mins}m"
    else:
        is_temp_pro = False 

is_pro = is_pro_license or is_temp_pro

def calculate_level_data(current_xp):
    levels = [(0, "Starter"), (200, "Bouwer"), (500, "Expert"), (1000, "E-com Boss"), (3000, "Legend"), (5000, "Master"), (10000, "Grandmaster")]
    current_rank, next_goal, prev_goal, level_num = levels[0][1], levels[1][0], levels[0][0], 1
    for i, (threshold, title) in enumerate(levels):
        if current_xp >= threshold:
            current_rank, level_num, prev_goal = title, i + 1, threshold
            next_goal = levels[i+1][0] if i + 1 < len(levels) else threshold * 2
        else: break
    return level_num, current_rank, next_goal, prev_goal

user_level_num, rank_title, next_xp_goal_sidebar, prev_threshold = calculate_level_data(user['xp'])
user['level'] = user_level_num 

if "prev_level" not in st.session_state: st.session_state.prev_level = user['level']
if "ai_credits" not in st.session_state: st.session_state.ai_credits = 3 

# --- 4.5 PERSISTENT AI CREDITS & FUNCTIES ---
def check_credits():
    if is_pro: 
        return True
    
    # Haal credits uit de database data (niet alleen session state)
    current_credits = user.get('ai_credits', 0)
    
    if current_credits > 0:
        # Update in database (maak deze functie aan in db.py of gebruik een update query)
        new_credits = current_credits - 1
        db.update_user_credits(user['email'], new_credits) 
        # Update lokale sessie zodat de UI direct verandert
        st.session_state.user['ai_credits'] = new_credits
        return True
    return False

def get_greeting():
    hour = datetime.now().hour
    return "Goedemorgen" if hour < 12 else "Goedemiddag" if hour < 18 else "Goedenavond"

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file: encoded = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded}"
    except: return None

# --- SIDEBAR ---
with st.sidebar:
    # WORKFLOW STATE HANDLER: Check if we need to switch tabs
    if "nav_index" not in st.session_state: st.session_state.nav_index = 0
    
    display_name = user.get('first_name') or user['email'].split('@')[0].capitalize()
    st.markdown(f"""<div style="margin-bottom: 2px; padding-left: 5px;"><h3 style="margin:0; font-size:1.0rem; color:#0F172A;"><i class="bi bi-person-circle"></i> {display_name}</h3><p style="margin:0; font-size: 0.75rem; color: #64748B;"><span style="background:#EFF6FF; padding:2px 6px; border-radius:4px; border:1px solid #DBEAFE; color:#2563EB; font-weight:600;">Lvl {user['level']}</span> {rank_title}</p></div>""", unsafe_allow_html=True)
    range_span = next_xp_goal_sidebar - prev_threshold
    if range_span <= 0: range_span = 1
    xp_pct = min((user['xp'] - prev_threshold) / range_span, 1.0) * 100
    st.markdown(f"""<div style="background: transparent; border-radius: 4px; height: 6px; width: 100%; margin-top: 8px; margin-bottom: 4px; border: 1px solid #F1F5F9;"><div style="background: #2563EB; height: 100%; width: {xp_pct}%; border-radius: 4px; transition: width 0.5s;"></div></div><div style="text-align:right; font-size:0.7rem; color:#94A3B8; margin-bottom:15px;">{user['xp']} / {next_xp_goal_sidebar} XP</div>""", unsafe_allow_html=True)
    
# --- PAS DIT STUK AAN IN DE SIDEBAR ---
    if is_temp_pro and not is_pro_license and time_left_str:
        st.markdown(f"""
        <div style="margin-bottom:15px; background: linear-gradient(135deg, #DCFCE7 0%, #BBF7D0 100%); padding: 10px; border-radius: 8px; border: 1px solid #86EFAC; display: flex; align-items: center; justify-content: space-between;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size: 1.2rem;">⏳</span>
                <div style="line-height:1.1;">
                    <div style="font-size: 0.7rem; color: #166534; font-weight: 700; text-transform: uppercase;">PRO TIJD OVER</div>
                    <div style="font-size: 0.95rem; color: #14532D; font-weight: 800;">{time_left_str}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif not is_pro:
        st.markdown(f"""<div style="margin-bottom:10px; font-size:0.8rem; color:#64748B; background:#F1F5F9; padding:6px; border-radius:6px; text-align:center;">⚡ <b>{st.session_state.ai_credits}</b>/3 dagelijkse AI credits</div>""", unsafe_allow_html=True)
    
# --- VERVANG VANAF HIER ---
    options = ["Dashboard", "Academy", "Producten Zoeken", "Marketing & Design", "Financiën", "Instellingen"]
    icons = ["house-fill", "mortarboard-fill", "search", "palette-fill", "cash-stack", "gear-fill"]
    
    menu_display_options = []
    for opt in options:
        if not is_pro and opt in ["Producten Zoeken", "Marketing & Design"]:
             menu_display_options.append(f"{opt} 🔒")
        else:
             menu_display_options.append(opt)

    # De menu_key zorgt ervoor dat het menu 'geforceerd' verspringt als de app merkt dat de index verandert
    menu_key = f"menu_state_{st.session_state.nav_index}"

    selected_display = option_menu(
        menu_title=None,
        options=menu_display_options,
        icons=icons,
        default_index=st.session_state.nav_index,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#FFFFFF"}, 
            "icon": {"color": "#64748B", "font-size": "14px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "padding": "10px", "--hover-color": "#EFF6FF", "color": "#0F172A"}, 
            "nav-link-selected": {"background-color": "#2563EB", "color": "white", "font-weight": "600"},
        },
        key=menu_key
    )

    # Als de gebruiker op een menu-item klikt, updaten we de nav_index
    if selected_display:
        clean_selection = selected_display.replace(" 🔒", "")
        new_index = options.index(clean_selection)
        if new_index != st.session_state.nav_index:
            st.session_state.nav_index = new_index
            st.rerun()

    # Deze variabele bepaalt welke pagina de gebruiker ziet
    pg = options[st.session_state.nav_index]
    # --- TOT HIER ---

    # --- NIEUW: AUTO-CLOSE SIDEBAR OP MOBIEL ---
    st.markdown("""
        <script>
            var width = window.innerWidth;
            if (width <= 992) {
                const closeBtn = window.parent.document.querySelector('[data-testid="stSidebarCollapseButton"]');
                if (closeBtn) {
                    setTimeout(function() {
                        closeBtn.click();
                    }, 150);
                }
            }
        </script>
    """, unsafe_allow_html=True)
    
    if not is_pro:
        st.markdown(f"""
        <a href="{STRATEGY_CALL_URL}" target="_blank" style="text-decoration:none;">
            <div style="margin-top: 20px; background: linear-gradient(135deg, #FFD700 0%, #F59E0B 100%); padding: 15px; border-radius: 12px; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3); text-align: center; border: 1px solid #FCD34D; transition: transform 0.2s;">
                <div style="font-weight: 800; color: #78350F; font-size: 1.1rem; margin-bottom: 4px;">🚀 UNLOCK PRO</div>
                <div style="font-size: 0.75rem; color: #92400E; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Word PRO Lid (€49,95)</div>
            </div>
        </a>
        """, unsafe_allow_html=True)

# =========================================================
# 🛠️ GLOBAL: VOORTGANG LADEN (BELANGRIJK VOOR ALLE PAGINA'S)
# =========================================================
if "force_completed" not in st.session_state: st.session_state.force_completed = []

@st.cache_data(ttl=60, show_spinner=False)
def get_cached_progress_db(uid): return auth.get_progress()

db_progress = get_cached_progress_db(user['id'])
completed_steps = list(set(db_progress + st.session_state.force_completed))

# WORKFLOW NAVIGATION LOGIC
# Update nav_index state based on menu selection
if selected_display:
    clean_selection = selected_display.replace(" 🔒", "")
    try:
        st.session_state.nav_index = options.index(clean_selection)
    except: pass
    pg = clean_selection
else:
    pg = "Dashboard"

# --- AANGEPASTE RENDER PRO LOCK ---
def render_pro_lock(title, desc, warning_text="Deze tool geeft onze studenten een oneerlijk voordeel. Daarom is dit afgeschermd."):
    lock_html = f"""
    <div style="position: relative; overflow: hidden; border-radius: 12px; border: 1px solid #E2E8F0; margin-top: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); background: #F8FAFC; min-height: 320px;">
        <div style="filter: blur(5px); opacity: 0.5; padding: 20px; pointer-events: none; user-select: none;">
            <div style="height: 20px; background: #CBD5E1; width: 60%; margin-bottom: 15px; border-radius: 4px;"></div>
            <div style="display:flex; gap:10px; margin-bottom: 10px;">
                <div style="height: 150px; background: #E2E8F0; width: 30%; border-radius: 8px;"></div>
                <div style="height: 150px; background: #E2E8F0; width: 70%; border-radius: 8px;"></div>
            </div>
            <div style="height: 15px; background: #E2E8F0; width: 90%; margin-bottom: 8px; border-radius: 4px;"></div>
            <div style="height: 15px; background: #E2E8F0; width: 80%; border-radius: 4px;"></div>
        </div>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 85%; max-width: 400px; z-index: 10;">
            <div style="background: white; padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.12); border: 1px solid #E2E8F0;">
                <div style="font-size: 28px; margin-bottom: 10px;">🔒</div>
                <h3 style="margin: 0 0 8px 0; color: #1E293B; font-size: 1.1rem; font-weight: 700;">{title}</h3>
                <p style="font-size: 0.85rem; color: #64748B; margin: 0 0 15px 0; line-height: 1.4;">{desc}</p>
                <div style="background: #FEF2F2; color: #991B1B; padding: 8px; border-radius: 6px; font-size: 0.75rem; margin-bottom: 15px; border: 1px solid #FECACA; font-weight: 600; line-height: 1.3;">
                    ⚠️ {warning_text}
                </div>
                <a href="{STRATEGY_CALL_URL}" target="_blank" style="text-decoration: none;">
                    <div style="background: linear-gradient(135deg, #2563EB, #1D4ED8); color: white; padding: 10px 20px; border-radius: 50px; font-weight: 600; font-size: 0.9rem; display: inline-block; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2); transition: transform 0.1s;">
                        Word PRO Lid (€49,95)
                    </div>
                </a>
            </div>
        </div>
    </div>
    """
    st.markdown(lock_html.replace("\n", ""), unsafe_allow_html=True)

# --- ONBOARDING WIZARD (VERBETERD) ---
# We kijken direct in het 'user' object dat we bovenaan het script al hebben gesynct met de DB
has_shop_name = user.get('shop_name') is not None and user.get('shop_name') != ""
wizard_already_done = st.session_state.get("wizard_complete", False)

# Alleen tonen als: Geen shopnaam in DB EN niet net afgerond EN XP is echt 0
if not has_shop_name and not wizard_already_done and user.get('xp', 0) == 0:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        welcome_name = user.get('first_name', 'Ondernemer')
        st.markdown(f"""<div style="text-align: center; padding: 20px;"><h1 style="color: #2563EB; margin-bottom: 10px;">👋Welkom bij RM Academy, {welcome_name}!</h1><p style="font-size: 1.1rem; color: #64748B;">Laten we je profiel instellen voor maximaal succes.</p></div>""", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            shop_name_input = st.text_input("Hoe gaat je webshop heten?", placeholder="Bijv. Nova Gadgets")
            goal_input = st.selectbox("Wat is je eerste maandelijkse doel?", ["€5.000 /maand (Sidehustle)", "€10.000 /maand (Serieus)", "€15.000+ /maand (Fulltime)"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 Start Mijn Avontuur (+10 XP)", type="primary", use_container_width=True):
                if shop_name_input:
                    with st.spinner("Profiel opslaan..."):
                        # 1. Direct naar DB schrijven via de gecorrigeerde functie
                        success = db.update_onboarding_data(user['email'], shop_name_input, goal_input)
                        
                        if success:
                            # 2. XP verhogen in DB
                            new_xp = user.get('xp', 0) + 10
                            auth.supabase.table('users').update({"xp": new_xp}).eq('email', user['email']).execute()
                            
                            # 3. CRUCIAAL: Update de sessie data direct
                            st.session_state.user['shop_name'] = shop_name_input
                            st.session_state.user['income_goal'] = goal_input
                            st.session_state.user['xp'] = new_xp
                            st.session_state.wizard_complete = True
                            
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Kon profiel niet opslaan. Controleer database verbinding.")
                else: 
                    st.warning("Vul een naam in!")
    
    # Blokkeer de rest van de app
    st.stop()

# =========================================================
# 📄 LEGAL PAGES & FOOTER DEFINITIES
# =========================================================

def render_footer():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        # Gebruik de huidige datum voor het jaartal
        current_year = datetime.now().year
        st.markdown(f"<p style='font-size:0.8rem; color:#64748B;'>© {current_year} RM Ecom Academy. Alle rechten voorbehouden.</p>", unsafe_allow_html=True)
    with col2:
        if st.button("🔒 Privacybeleid", key="btn_footer_priv", use_container_width=True):
            st.session_state.view = "privacy"
            st.rerun()
    with col3:
        if st.button("📄 Voorwaarden", key="btn_footer_terms", use_container_width=True):
            st.session_state.view = "terms"
            st.rerun()

def render_privacy_page():
    st.markdown("<h1>🔒 Privacybeleid</h1>", unsafe_allow_html=True)
    if st.button("⬅️ Terug naar Dashboard", type="primary", key="priv_back_top"):
        st.session_state.view = "main"
        st.rerun()
    
    with st.container(border=True):
        st.markdown(f"""
        ### 1. Hoe we je gegevens gebruiken
        RM Ecom Academy gebruikt je e-mail en voornaam alleen om je account te beheren en je voortgang (XP en Levels) op te slaan in onze beveiligde database.
        
        ### 2. Cookies
        We gebruiken lokale cookies om je ingelogd te houden. Zonder deze cookies zou je bij elke verversing opnieuw moeten inloggen.
        
        ### 3. Derden
        Je gegevens worden nooit verkocht. We maken gebruik van Supabase voor database-opslag en OpenAI voor de AI-coach functies. De data die je invoert bij de AI-tools wordt anoniem verwerkt.
        
        ### 4. Verwijderen
        Wil je je account en al je XP-data verwijderen? Stuur een e-mail naar support@rmacademy.nl en we regelen het binnen 48 uur.
        """)
    st.button("Terug naar Dashboard", key="btn_priv_bottom", on_click=lambda: setattr(st.session_state, 'view', 'main'))

def render_terms_page():
    st.markdown("<h1>📄 Algemene Voorwaarden</h1>", unsafe_allow_html=True)
    if st.button("⬅️ Terug naar Dashboard", type="primary", key="terms_back_top"):
        st.session_state.view = "main"
        st.rerun()
        
    with st.container(border=True):
        st.markdown(f"""
        ### 1. Gebruik van de App
        Door gebruik te maken van RM Ecom Academy ga je akkoord met onze methodiek. Je bent zelf verantwoordelijk voor de uitvoering van je webshop.
        
        ### 2. AI & Credits
        Misbruik van de AI-tools (zoals het genereren van ongepaste content) kan leiden tot een directe blokkering van je account zonder teruggave van credits.
        
        ### 3. Partner Programma
        Referral commissies (€250,- per student) worden pas uitgekeerd nadat de aangebrachte student de wettelijke bedenktijd van 14 dagen heeft doorlopen en de betaling definitief is.
        
        ### 4. PRO Lidmaatschap
        PRO-toegang is persoonlijk. Het delen van accounts is niet toegestaan en wordt gedetecteerd door ons systeem.
        
        ### 5. Resultaten
        E-commerce resultaten verschillen per persoon. Wij bieden de tools en roadmap, maar kunnen geen omzetgaranties geven.
        """)
    st.button("Terug naar Dashboard", key="btn_terms_bottom", on_click=lambda: setattr(st.session_state, 'view', 'main'))

# =========================================================
# 🏠 PAGINA ROUTING (PRIVACY, VOORWAARDEN OF DASHBOARD)
# =========================================================

if st.session_state.view == "privacy":
    render_privacy_page()

elif st.session_state.view == "terms":
    render_terms_page()

else:
    # --- DIT IS DE ORIGINELE APP INHOUD ---
    if pg == "Dashboard":
        # 1. Level Up Melding (Subtiel rechtsboven, geen popup)
        if user['level'] > st.session_state.prev_level:
            st.balloons()
            # We updaten de status direct zodat de melding bij de volgende klik weer weggaat
            st.session_state.prev_level = user['level']
            
            st.markdown(f"""
    <div style="position: fixed; top: 80px; right: 20px; z-index: 9999; animation: slideIn 0.5s ease-out;">
        <div style="background: linear-gradient(135deg, #FFD700 0%, #F59E0B 100%); 
                    padding: 15px 25px; 
                    border-radius: 12px; 
                    box-shadow: 0 10px 25px rgba(0,0,0,0.2); 
                    border: 1px solid #FCD34D;
                    display: flex; 
                    align-items: center; 
                    gap: 15px;">
            <span style="font-size: 24px;">🏆</span>
            <div style="text-align: left;">
                <div style="color: #78350F; font-weight: 800; font-size: 0.9rem; margin: 0; line-height: 1;">LEVEL UP!</div>
                <div style="color: #92400E; font-size: 0.8rem; font-weight: 600; margin-top: 4px;">Je bent nu Level {user['level']}</div>
            </div>
        </div>
    </div>

    <style>
    @keyframes slideIn {{
        0% {{ transform: translateX(100%); opacity: 0; }}
        100% {{ transform: translateX(0); opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)


        if "force_completed" not in st.session_state: st.session_state.force_completed = []
        @st.cache_data(ttl=60, show_spinner=False)
        def get_cached_progress_db(uid): return auth.get_progress()
        db_progress = get_cached_progress_db(user['id'])
        completed_steps = list(set(db_progress + st.session_state.force_completed))
    # --- 1. LOGICA & VARIABELEN (FIXED: OPSLAAN & WEERGAVE) ---
        full_map = roadmap.get_roadmap()
        # Haal ALTIJD de laatste voortgang op uit de database
        db_progress = auth.get_progress()
        completed_steps = list(set(db_progress + st.session_state.force_completed))
        
        all_roadmap_ids = [s['id'] for fase in full_map.values() for s in fase['steps']]
        valid_done_count = len([sid for sid in completed_steps if sid in all_roadmap_ids])
        total_steps_count = len(all_roadmap_ids)
        
        progress_pct = int((valid_done_count / total_steps_count) * 100) if total_steps_count > 0 else 0
        safe_progress = min(progress_pct, 100)
        is_finished = valid_done_count >= total_steps_count

        # Initialiseer knoppen
        btn_url = "#roadmap_start"
        btn_pro_url = STRATEGY_CALL_URL
        btn_student_url = "https://calendly.com/rmecomacademy/30min"

        if not is_finished:
            # --- BLAUWE KAART LOGICA ---
            next_step_title, next_step_phase_index, next_step_id, next_step_locked, next_step_desc = "Laden...", 0, None, False, ""
            for idx, (fase_key, fase) in enumerate(full_map.items()):
                phase_done = True
                for s in fase['steps']:
                    if s['id'] not in completed_steps:
                        next_step_title, next_step_desc, next_step_phase_index, next_step_id, next_step_locked = s['title'], s.get('teaser', 'Voltooi deze stap.'), idx + 1, s['id'], s.get('locked', False)
                        phase_done = False
                        break
                if not phase_done: break
                
            card_bg = "linear-gradient(135deg, #2563EB 0%, #1E40AF 100%)"
            accent_color = "#FFFFFF"
            card_icon = "bi-crosshair"
            buttons_html = f"""<div style="margin-top: 15px;"><a href="#roadmap_start" target="_self" style="text-decoration:none;"><div style="display: inline-block; background: #FBBF24; color: #000; padding: 12px 25px; border-radius: 12px; font-weight: 900; font-size: 0.95rem; cursor: pointer; box-shadow: 0 4px 15px rgba(251, 191, 36, 0.4);">🚀 Start Opdracht</div></a></div>"""

        else:
            # --- GOUDEN KAART LOGICA (NA VOLTOOIING) ---
            next_step_title = "Toegang Verleend tot de Elite 🏆"
            
            # DEZE REGELS ONTBREKEN WAARSCHIJNLIJK:
            card_bg = "linear-gradient(135deg, #FFD700 0%, #F59E0B 50%, #D97706 100%)"
            card_icon = "bi-trophy-fill"  # <--- DIT IS DE FIX
            
            next_step_desc = (
                "<div style='line-height: 1.5; color: white !important;'>"
                "Gefeliciteerd! Je hebt de volledige Roadmap voltooid. Je hoort nu bij de top 5% van starters die daadwerkelijk actie onderneemt. <br><br>"
                "<b>De volgende stap:</b> Je fundament staat. Nu is het tijd om te schalen naar <b>€15.000+/maand</b>. Hiervoor heb je onze winnende advertentie-strategieën en Private Agents nodig."
                "</div>"
            )
            
            next_step_phase_index = 6
            
            buttons_html = f"""
<div style='display: flex; gap: 12px; flex-wrap: wrap; align-items: center; margin-top: 20px;'>
<a href='{btn_student_url}' target='_blank' style='text-decoration:none;'>
<div style='background: #1a1a1a; color: #FFD700; padding: 12px 24px; border-radius: 10px; font-weight: 900; font-size: 0.95rem; box-shadow: 0 4px 15px rgba(0,0,0,0.3); border: 1px solid #FFD700;'>
🚀 Word student (Gratis call)
</div>
</a>
<a href='{btn_pro_url}' target='_blank' style='text-decoration:none;'>
<div style='background: rgba(255,255,255,0.2); color: #FFFFFF; padding: 12px 24px; border-radius: 10px; font-weight: 800; font-size: 0.95rem; border: 2px solid #FFFFFF; backdrop-filter: blur(5px);'>
⚡ Activeer PRO
</div>
</a>
</div>
""".replace("\n", "")

    # --- 2. HEADER & PROGRESS ---
        db_shop_name = user.get('shop_name')
        db_goal = user.get('income_goal')
        us = db_shop_name if db_shop_name and str(db_shop_name) != "None" else "Mijn Webshop"
        ug = db_goal if db_goal and str(db_goal) != "None" else "€15k/maand"
        
        st.markdown(f"<h1>Goedemorgen, {user.get('first_name', 'Gast')} 👋</h1>", unsafe_allow_html=True)
        st.caption(f"🚀 {us}: **{ug}** | 📈 Voortgang: **{safe_progress}%**")
        st.progress(safe_progress / 100)

# --- 3. UITLEG SECTIE IN KASSA STIJL ---
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        with st.expander("ℹ️ **UITLEG: Hoe werkt ons platform?** ❓", expanded=False):
            # De hoofdcontainer in Kassa-stijl
            st.markdown("""
            <div style="background: #F0F9FF; border: 1px solid #BAE6FD; padding: 25px; border-radius: 16px; margin-bottom: 10px;">
                <h3 style="margin-top: 0; color: #0369A1; font-size: 1.3rem; display: flex; align-items: center; gap: 10px; font-weight: 700;">
                    <span style="font-size: 1.5rem;">🚀</span> Welkom bij de Academy
                </h3>
                <p style="font-size: 1rem; color: #1E293B; line-height: 1.6; margin-bottom: 10px;">
    Volg de Roadmap stap-voor-stap en gebruik onze AI-tools om jouw winstgevende webshop te bouwen.
</p>
<p style="font-size: 0.85rem; color: #64748B; margin-bottom: 0;">
    <i>Samen bouwen wij jouw succes! - Team RM Ecom</i>
</p>
            </div>
            """, unsafe_allow_html=True)

            col_vid, col_txt = st.columns([1.3, 1], gap="medium")
            
            with col_vid:
                # Video direct in de kolom
                st.video(COACH_VIDEO_URL)
            
            with col_txt:
                st.markdown("#### Belangrijke info:")
                
                # De badges/pills in de nieuwe stijl
                st.markdown("""
                <div style="margin-bottom: 12px;">
                    <div style="margin-bottom: 8px;">
                        <span style="background: white; padding: 3px 10px; border-radius: 6px; border: 1px solid #CBD5E1; color: #475569; font-weight: 800; font-size: 0.7rem; text-transform: uppercase;">DEMO</span> 
                        <span style="font-size: 0.9rem; color: #1E293B; margin-left: 5px;">Roadmap + 3 AI credits</span>
                    </div>
                    <div style="margin-bottom: 8px;">
                        <span style="background: white; padding: 3px 10px; border-radius: 6px; border: 1px solid #FCD34D; color: #92400E; font-weight: 800; font-size: 0.7rem; text-transform: uppercase;">PRO Lid ⚡</span> 
                        <span style="font-size: 0.9rem; color: #1E293B; margin-left: 5px;">Onbeperkt AI + Spy-tools + Giveaway 🎁</span>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <span style="background: white; padding: 3px 10px; border-radius: 6px; border: 1px solid #2563EB; color: #1E40AF; font-weight: 800; font-size: 0.7rem; text-transform: uppercase;">STUDENT 🎓</span> 
                        <span style="font-size: 0.9rem; color: #1E293B; margin-left: 5px;">Volledige cursus + 1op1 Coaching</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if not is_pro:
                    # De GOUDEN PRO KNOP (matcht met de sidebar)
                    st.markdown(f"""
                    <a href="{STRATEGY_CALL_URL}" target="_blank" style="text-decoration:none;">
                        <div style="background: linear-gradient(135deg, #FFD700 0%, #F59E0B 100%); 
                                    padding: 14px; border-radius: 12px; text-align: center; 
                                    box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3); 
                                    border: 1px solid #FCD34D; transition: transform 0.2s;">
                            <div style="font-weight: 800; color: #78350F; font-size: 1rem;">🚀 UPGRADE NAAR PRO</div>
                            <div style="font-size: 0.7rem; color: #92400E; font-weight: 700; text-transform: uppercase;">Unlock alle tools (€49,95)</div>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
                else:
                    st.success("✅ Je bent een PRO lid!")

        # --- 4. DAILY HABIT SECTIE ---
        daily_id = f"daily_habit_{datetime.now().strftime('%Y%m%d')}"
        is_daily_done = daily_id in completed_steps

        st.markdown("### 📅 Jouw Focus (Roadmap)")
        with st.container(border=False):
            if not is_daily_done:
                c1, c2 = st.columns([3, 1], vertical_alignment="center")
                c1.markdown("Heb je vandaag minstens 15 minuten aan je shop gewerkt? Consistentie is de sleutel tot succes.")
                if c2.button("✅ Ja, Claim XP", type="primary", use_container_width=True, key="dashboard_daily_focus"):
                    auth.mark_step_complete(daily_id, 10)
                    st.cache_data.clear()
                    st.rerun()
            else:
                st.success("Lekker bezig! Je hebt je daily habit voor vandaag gehaald. 🔥")

# --- 1. RENDERING VAN DE ORANJE KAART (Zorg dat dit blok boven de nieuwe code staat) ---
        st.markdown(f"""
        <div style="background: {card_bg}; padding: 25px; border-radius: 20px; margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.3); box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
            <div style="color: white !important; font-family: sans-serif;">
                <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; font-weight: 800; color: white !important; opacity: 0.9;">
                    <i class="bi {card_icon}"></i> ELITE STATUS BEREIKBAAR
                </div>
                <h2 style="margin: 0; font-size: 1.8rem; color: white !important; font-weight: 900; line-height: 1.2; margin-bottom: 10px; border: none; padding: 0;">
                    {next_step_title}
                </h2>
                <p style="margin: 0; font-size: 1.1rem; line-height: 1.4; color: white !important; max-width: 650px; font-weight: 500;">
                    {next_step_desc}
                </p>
                {buttons_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- 2. DE XP BOOSTER (NU ONDER DE KAART + 2-STAP LOGICA) ---
        if user['xp'] < 1000:
            st.markdown("### 🚀 Laatste stap naar Level 4")
            with st.container(border=True):
                st.write(f"Je hebt nu **{user['xp']} XP**. Deel de RM Academy APP om de laatste XP te verdienen en de 'E-com Boss' status te claimen.")
                
                col_1, col_2 = st.columns(2)
                
                with col_1:
                    # WhatsApp Bericht met FOMO en Urgentie
                    whatsapp_tekst = """STOP met wat je doet! Ik heb net de 'gouden' app van RM Academy ontdekt. Je krijgt nu GRATIS toegang tot hun WinningHunter (viral producten), Concurrenten-Spy en AI LogoMaker. Dit is letterlijk de toolkit waarmee zij €10k+ maanden draaien. Ik heb geen idee hoelang dit nog gratis blijft: https://app.rmacademy.nl"""
                    
                    # De tekst veilig omzetten voor een URL
                    share_msg = urllib.parse.quote(whatsapp_tekst)
                    wa_url = f"https://wa.me/?text={share_msg}"
                    
                    st.link_button("📲 1. Deel via WhatsApp", wa_url, use_container_width=True)
                
                with col_2:
                    # De 'Vrijgave' check
                    has_shared = st.checkbox("Ik heb de link gedeeld ✅", key="booster_check")
                    
                    if has_shared:
                        if st.button("✅ 2. Claim +100 XP Boost", type="primary", use_container_width=True):
                            auth.mark_step_complete("final_share_boost_milestone", 100)
                            st.balloons()
                            st.success("Boom! Je bent nu een E-com Boss! 🏆")
                            time.sleep(2)
                            st.rerun()
                    else:
                        # Grijze knop als er nog niet gevinkt is
                        st.button("Claim XP (Deel eerst)", disabled=True, use_container_width=True)

        # --- 7. STATS GRID ---
        needed = next_xp_goal_sidebar - user['xp']
        next_reward = "Spy tool" if user['level'] < 2 else "Video scripts"
        st.markdown(f"""
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-icon">Level</div>
                <div class="stat-value">{user['level']}</div>
                <div class="stat-sub">{rank_title}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">XP</div>
                <div class="stat-value">{user['xp']}</div>
                <div class="stat-sub">Nog {needed} voor Lvl {user['level']+1}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">Beloning</div>
                <div class="stat-value" style="font-size: 1.2rem;">\U0001F381</div>
                <div class="stat-sub" style="color:#2563EB;">{next_reward}</div>
            </div>
        </div>""", unsafe_allow_html=True)
        
        
        st.markdown("<div id='roadmap_start' style='height: 0px;'></div>", unsafe_allow_html=True)
        st.markdown("### 📍 Jouw Roadmap")
        st.caption("Klik op een fase om je taken te bekijken.")
        
        active_phase_idx = next_step_phase_index 
        for idx, (fase_key, fase) in enumerate(full_map.items()):
            phase_num = idx + 1
            is_current_phase = (phase_num == active_phase_idx)
            if phase_num < active_phase_idx: phase_icon, phase_label = "✅", f"{fase['title']} (Voltooid)"
            elif phase_num == active_phase_idx: phase_icon, phase_label = "📍", f"{fase['title']} (Nu Actief)" 
            else: phase_icon, phase_label = "📂", fase['title']
                
            with st.expander(f"{phase_icon} {phase_label}", expanded=is_current_phase):
                st.caption(fase['desc'])
                for step in fase['steps']:
                    is_done = step['id'] in completed_steps
                    if is_done:
                        with st.expander(f"✅ {step['title']}", expanded=False): st.info("Deze stap heb je al afgerond. Goed bezig!")
                    else:
                        is_recommended = (step['id'] == next_step_id)
                        just_completed_id, xp = roadmap.render_step_card(step, is_done, is_pro, expanded=is_recommended)
                        if just_completed_id:
                            with st.spinner("Opslaan..."):
                                auth.mark_step_complete(just_completed_id, xp)
                                if "force_completed" not in st.session_state: st.session_state.force_completed = []
                                st.session_state.force_completed.append(just_completed_id)
                                st.toast(f"🚀 Lekker bezig! +{xp} XP", icon="🎉") 
                                st.rerun()
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    elif pg == "Academy":
        # --- CSS VOOR PREMIUM LOOK ---
        st.markdown("""
        <style>
            .premium-card {
                background: white; border: 1px solid #E2E8F0; border-radius: 12px;
                padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            }
            .locked-module {
                background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 8px;
                padding: 12px 15px; margin-bottom: 8px; color: #94A3B8;
                display: flex; align-items: center; justify-content: space-between; font-size: 0.9rem;
            }
            div.stButton > button[kind="secondary"] {
                border: 1px solid #E2E8F0 !important; background: white !important;
                color: #475569 !important; justify-content: flex-start !important;
                padding-left: 15px !important; text-align: left !important;
            }
            div.stButton > button[kind="primary"] {
                background: #2563EB !important; border: 1px solid #2563EB !important;
                justify-content: flex-start !important; padding-left: 15px !important;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("<h1><i class='bi bi-mortarboard-fill'></i> Academy</h1>", unsafe_allow_html=True)
        
        tab_free, tab_pro_course = st.tabs(["🎁 Gratis Mini Training", "🎓 Volledige Cursus (70+ Video's)"])

        # =========================================================
        # --- TAB 1: GRATIS MINI TRAINING (Iedereen ziet dit) ---
        # =========================================================
        with tab_free:
            # Info banner
            st.markdown("""
            <div style="background: #F0F9FF; border: 1px solid #BAE6FD; padding: 15px; border-radius: 12px; display: flex; align-items: center; gap: 10px; margin-bottom: 20px; color: #0369A1;">
                <span>ℹ️ Je hebt <b>Preview Toegang</b>: 4 van de 74 lessen zijn direct beschikbaar.</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Video Grid
            c1, c2 = st.columns(2)
            
            videos = [
                {"t": "1. Van Chaos naar Actie 🚀", "id": "nYN7EyMb7uQ", "desc": "Zet je mindset aan voor succes en begrijp het RM systeem."},
                {"t": "2. Jouw volgende stap 📈", "id": "yIJJbwIZL6k", "desc": "Hoe je de roadmap gebruikt om binnen 30 dagen live te zijn."},
                {"t": "3. Kies het juiste product 📦", "id": "CM5CtnXrvEU", "desc": "De 'Winning Product' formule uitgelegd door experts."},
                {"t": "4. Je eerste advertentie 🔥", "id": "cA8Gvhfic-s", "desc": "Stap-voor-stap je eerste campagne opzetten in Meta."}
            ]

            for i, vid in enumerate(videos):
                col = c1 if i % 2 == 0 else c2
                with col:
                    with st.container(border=True):
                        st.markdown(f"**{vid['t']}**")
                        st.video(f"https://www.youtube.com/embed/{vid['id']}")
                        st.caption(vid['desc'])
                        # Optioneel: XP knop per video
                        if st.button(f"Klaar (+5 XP)", key=f"vid_xp_{i}"):
                            auth.mark_step_complete(f"academy_vid_{i}", 5)
                            st.toast("Lekker bezig! +5 XP verdiend.")

            # Locked Modules in Kassa-stijl
            st.markdown("<br>#### 🔒 Jouw volgende modules (PRO/Student only):", unsafe_allow_html=True)
            
            locked_cols = st.columns(2)
            locked_data = [
                "Module 5: Shopify Masterclass", "Module 7: Facebook Ads Setup",
                "Module 9: Opschalen naar 10K", "Module 11: Private Agents",
                "Module 12: Viral Content Geheimen", "Module 14: Klantenservice Automatisatie"
            ]
            
            for i, mod in enumerate(locked_data):
                l_col = locked_cols[0] if i % 2 == 0 else locked_cols[1]
                l_col.markdown(f"""
                <div style="background: #F8FAFC; border: 1px dashed #CBD5E1; padding: 12px; border-radius: 8px; margin-bottom: 8px; color: #64748B; font-size: 0.85rem;">
                    <i class="bi bi-lock-fill"></i> {mod}
                </div>
                """, unsafe_allow_html=True)

            # De "Eindstation" CTA
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="text-align: center; background: white; padding: 30px; border-radius: 16px; border: 1px solid #E2E8F0;">
                <h4>Wil je toegang tot alle 74 video's en tools?</h4>
                <p style="color: #64748B;">Zet de volgende stap in je ondernemersreis.</p>
                <a href="{STRATEGY_CALL_URL}" target="_blank" style="text-decoration:none;">
                    <div style="background: linear-gradient(135deg, #FFD700 0%, #F59E0B 100%); padding: 15px 30px; border-radius: 12px; display: inline-block; font-weight: 800; color: #78350F;">
                        🚀 UPGRADE NAAR PRO & UNLOCK ALLES
                    </div>
                </a>
            </div>
            """, unsafe_allow_html=True)

        # =========================================================
        # --- TAB 2: DE ECHTE CURSUS (DE HARDE LOCK) ---
        # =========================================================
        with tab_pro_course:
            # Check op de speciale 'Academy Student' status (niet alleen PRO)
            is_academy_student = user.get('is_academy_student', False)

            if not is_academy_student:
                # DIT SCHERM ZIE JE ALTIJD, TENZIJ HANDMATIG TOEGEVOEGD IN DB
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background: white; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
                    <div style="font-size: 50px; margin-bottom: 20px;">🎓</div>
                    <h2 style="color: #0F172A; margin-bottom: 10px;">Full Academy Toegang</h2>
                    <p style="color: #64748B; font-size: 1.1rem; max-width: 500px; margin: 0 auto 25px auto;">
                        De volledige cursus met 70+ video's, copy-paste templates en 1-op-1 begeleiding is <b>exclusief voor traject-studenten</b>.
                    </p>
                    <div style="background: #FFF7ED; border: 1px solid #FED7AA; padding: 12px; border-radius: 8px; margin-bottom: 30px; display: inline-block;">
                        <p style="margin: 0; color: #9A3412; font-size: 0.9rem; font-weight: 700;">
                            🔒 Toegang wordt pas verleend na een Strategie Gesprek.
                        </p>
                    </div>
                    <br>
                    <a href="https://calendly.com/rmecomacademy/30min" target="_blank" style="text-decoration: none;">
                        <div style="background: #2563EB; color: white; padding: 15px 35px; border-radius: 8px; font-weight: 800; font-size: 1.1rem; display: inline-block; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);">
                            📞 Plan Gratis Strategie Call
                        </div>
                    </a>
                </div>
                """, unsafe_allow_html=True)
            else:
                # --- DE VIDEOS (Alleen voor geverifieerde studenten) ---
                course_content = {
                    "Module 1: Welkom": [
                        {"title": "Introductie - Welkom bij RM Ecom Academy", "url": "https://youtu.be/N7sftaU3T_E", "duration": "5 min"},
                        {"title": "Jouw 100K Laserfocus Systeem", "url": "https://youtu.be/aBpsJN0D3QE", "duration": "10 min"},
                        {"title": "Jouw Transformatieplan in 70 Dagen", "url": "https://youtu.be/gx5dJ6nUrf4", "duration": "15 min"},
                        {"title": "De eerste stappen naar succes", "url": "https://youtu.be/ajnJeKuKp7c", "duration": "8 min"},
                    ],
                    "Module 2: Het begin": [
                        {"title": "Het openen van een zakelijke rekening", "url": "https://youtu.be/x90vvuup1I8", "duration": "10 min"},
                        {"title": "Een creditcard aanvragen", "url": "https://youtu.be/lrhhCsRCcUE", "duration": "5 min"},
                        {"title": "Mindset voor de 70-dagen transformatieplan", "url": "https://youtu.be/_0W4z1yR_Lg", "duration": "20 min"},
                    ],
                    "Module 3: Dropshipping": [
                        {"title": "Wat betekend branded dropshipping?", "url": "https://youtu.be/puq-WqF8JMQ", "duration": "10 min"},
                        {"title": "Wat is dropshipping en hoe werkt het?", "url": "https://youtu.be/Dq8E6G5Fgc8", "duration": "15 min"},
                    ],
                    "Module 4: De fundering": [
                        {"title": "Een markt kiezen", "url": "https://youtu.be/vcxTcT5rnV4", "duration": "15 min"},
                        {"title": "Een niche kiezen", "url": "https://youtu.be/4bfnKWIQYbY", "duration": "20 min"},
                    ],
                    "Module 5: Shopify": [
                        {"title": "Shopify account aanmaken", "url": "https://youtu.be/gwxx5fUouKQ", "duration": "5 min"},
                        {"title": "Website termen", "url": "https://youtu.be/d9NPDvrYUHc", "duration": "5 min"},
                        {"title": "Rondleiding Shopify (algemeen)", "url": "https://youtu.be/zkMAybKHnnc", "duration": "15 min"},
                        {"title": "De webshop inrichten", "url": "https://youtu.be/xBS66G6OK84", "duration": "25 min"},
                        {"title": "Een betaling ontvangen (Shopify Payments)", "url": "https://youtu.be/hW2hmKlBcEQ", "duration": "10 min"},
                        {"title": "Een domein kiezen en aanschaffen", "url": "https://youtu.be/PxNTMe-qsOA", "duration": "5 min"},
                        {"title": "Custom codes gebruiken", "url": "https://youtu.be/zi3fXCyBYdI", "duration": "10 min"},
                        {"title": "De navigatie van je webshop", "url": "https://youtu.be/F3INLon0pnY", "duration": "10 min"},
                        {"title": "Een productpagina aanmaken", "url": "https://youtu.be/0PJ4NpR1ibs", "duration": "15 min"},
                        {"title": "Een collectiepagina aanmaken", "url": "https://youtu.be/Grh2GVnKJRk", "duration": "10 min"},
                        {"title": "Een verzendmethode instellen", "url": "https://youtu.be/8aGzEJrV0M8", "duration": "10 min"},
                        {"title": "Kortingscodes aanmaken", "url": "https://youtu.be/k2uGrjto_fo", "duration": "5 min"},
                        {"title": "Conversie optimaliseren (CRO)", "url": "https://youtu.be/0QNxhi7aXBA", "duration": "20 min"},
                        {"title": "De checkout optimaliseren", "url": "https://youtu.be/y0-giNe1Pes", "duration": "10 min"},
                        {"title": "Shopify markten instellen", "url": "https://youtu.be/OCPcbo0JsMo", "duration": "15 min"},
                    ],
                    "Module 6: Apps in Shopify": [
                        {"title": "Poky", "url": "https://youtu.be/qKLYDk9-7x8", "duration": "5 min"},
                        {"title": "Section store", "url": "https://youtu.be/Gc3G_x2D_4k", "duration": "5 min"},
                        {"title": "Parcel panel", "url": "https://youtu.be/TsMKOtsIz7Y", "duration": "5 min"},
                        {"title": "Slize Cart by AMP", "url": "https://youtu.be/JLNFlfSLqjI", "duration": "5 min"},
                        {"title": "BF size charts", "url": "https://youtu.be/iP__ahhzXfo", "duration": "5 min"},
                        {"title": "Kaching Bundles en hoe AOV verhogen", "url": "https://youtu.be/9SBXwXFrIkQ", "duration": "10 min"},
                        {"title": "Conversie Verhogen - Trust Badges", "url": "https://youtu.be/718tg9QR50Y", "duration": "5 min"},
                    ],
                    "Module 7: Facebook (Setup)": [
                        {"title": "Start van je Facebook blueprint", "url": "https://youtu.be/pvIAASq9jfg", "duration": "10 min"},
                        {"title": "De Businessmanager aanmaken", "url": "https://youtu.be/_7vF_nc6dzo", "duration": "10 min"},
                        {"title": "Een Rondleiding door de businessmanager", "url": "https://youtu.be/M-BAExvxyzU", "duration": "15 min"},
                        {"title": "Het aanmaken van een Facebookpagina", "url": "https://youtu.be/2sh_raKCa_Q", "duration": "5 min"},
                        {"title": "Het opwarmen van de pagina", "url": "https://youtu.be/FY08rYyjwlM", "duration": "5 min"},
                        {"title": "Het aanmaken van je advertentieaccount", "url": "https://youtu.be/dmJIS8Ujuec", "duration": "5 min"},
                        {"title": "Opzetten van je agency advertentieaccount", "url": "https://youtu.be/JOUW_LINK_HIER", "duration": "10 min"},
                        {"title": "Het aanmaken en koppelen van je pixel", "url": "https://youtu.be/NeIB1Ime_2cR", "duration": "15 min"},
                        {"title": "Het verifiëren van je domein", "url": "https://youtu.be/eE9aziZogjw", "duration": "5 min"},
                        {"title": "Facebook structuur opzetten", "url": "https://youtu.be/JOUW_LINK_HIER", "duration": "10 min"},
                        {"title": "Je Instagram account koppelen", "url": "https://youtu.be/ZOaOr56EqGc", "duration": "5 min"},
                    ],
                    "Module 8: Facebook Live gaan": [
                        {"title": "Wat is een ABO campagne?", "url": "https://youtu.be/0w32dh7yS9I", "duration": "10 min"},
                        {"title": "Wat is een CBO campagne?", "url": "https://youtu.be/zBk2oR_MGbI", "duration": "10 min"},
                        {"title": "Het aanmaken van een testcampagne", "url": "https://youtu.be/gwlKJ9XhwBE", "duration": "20 min"},
                        {"title": "Facebooktermen", "url": "https://youtu.be/EVE_Xhu1qjI", "duration": "10 min"},
                        {"title": "Het instellen van kolommen", "url": "https://youtu.be/M1ek9iua7sg", "duration": "5 min"},
                        {"title": "Opschalen van je advertenties (de basis)", "url": "https://youtu.be/qGG30Y-0HVw", "duration": "15 min"},
                        {"title": "Hoe analyseer je advertenties?", "url": "https://youtu.be/C3qXa4r-8yo", "duration": "15 min"},
                        {"title": "Wat doe je als een product onder presteert?", "url": "https://youtu.be/u0giYTGBcfA", "duration": "10 min"},
                        {"title": "Comments automatisch verbergen", "url": "https://youtu.be/FIyEYO6yd18", "duration": "5 min"},
                        {"title": "Wetracked of Trackbee installeren", "url": "https://youtu.be/dsk8nUqkDtI", "duration": "10 min"},
                    ],
                    "Module 9: Facebook geavanceerd": [
                        {"title": "Veilig opschalen met 20%", "url": "https://youtu.be/yHEDftamMc8", "duration": "10 min"},
                        {"title": "Gemiddeld opschalen met 50%", "url": "https://youtu.be/mHVh_PY-ja4", "duration": "10 min"},
                        {"title": "Agressief opschalen met 100%", "url": "https://youtu.be/8ayQ1ecqoCg", "duration": "10 min"},
                        {"title": "Ultra agressief opschalen (Surfscalen)", "url": "https://youtu.be/lfskezYSM1Y", "duration": "15 min"},
                        {"title": "Creatives testen (voor een lage cpc)", "url": "https://youtu.be/SCjQilN9W2s", "duration": "15 min"},
                    ],
                    "Module 10: Branding": [
                        {"title": "Social Media branding", "url": "https://youtu.be/3Vccoluq43U", "duration": "10 min"},
                        {"title": "Logo maken", "url": "https://youtu.be/GqehPhoMnX0", "duration": "10 min"},
                    ],
                    "Module 11: Agent (Prive leverancier)": [
                        {"title": "Het gebruiken van een privé leverancier", "url": "https://youtu.be/lvIv6vq2dQY", "duration": "10 min"},
                        {"title": "De kwaliteit van je producten checken", "url": "https://youtu.be/WDCebfTe4jQ", "duration": "5 min"},
                        {"title": "Een gepersonaliseerde verpakking maken", "url": "https://youtu.be/2GZIH6HnV2k", "duration": "10 min"},
                    ],
                    "Module 12: Content Creation": [
                        {"title": "De 5 stadia van bewustzijn", "url": "https://youtu.be/RBvrN_JdNsI", "duration": "10 min"},
                        {"title": "Canva rondleiding", "url": "https://youtu.be/SekM6oFOQNs", "duration": "15 min"},
                        {"title": "Advertentie creatives maken", "url": "https://youtu.be/aJHm6_yFgSg", "duration": "20 min"},
                        {"title": "Video's vanuit de AD library downloaden", "url": "https://youtu.be/WFE3l88O5iM", "duration": "5 min"},
                        {"title": "De opbouw van een winnende video creatie", "url": "https://youtu.be/Oeh276FU0iQ", "duration": "15 min"},
                        {"title": "Scroll stoppers maken voor je video", "url": "https://youtu.be/TeohCu7NEwE", "duration": "10 min"},
                        {"title": "Advertentieteksten schrijven met Chat-GPT", "url": "https://youtu.be/LVk0No917sI", "duration": "10 min"},
                        {"title": "UGC content gebruiken", "url": "https://youtu.be/GKmWZFkgFeg", "duration": "10 min"},
                    ],
                    "Module 13: Klantenservice": [
                        {"title": "Hoe ga je met klanten om?", "url": "https://youtu.be/08qt2ND4pLY", "duration": "10 min"},
                        {"title": "Klantenservice templates", "url": "https://youtu.be/JOUW_LINK_HIER", "duration": "5 min"},
                        {"title": "Retourfunnel (verminder je retouren)", "url": "https://youtu.be/C5So4rh8Xx0", "duration": "10 min"},
                    ],
                    "Module 14: Must Have": [
                        {"title": "Handige Tools (MUST HAVE)", "url": "https://youtu.be/9cmTsNGat2s", "duration": "10 min"},
                        {"title": "Ad strategie (Collecties)", "url": "https://youtu.be/7YNWLMsexnw", "duration": "15 min"},
                        {"title": "Website reviews (Fouten van anderen)", "url": "https://youtu.be/gzOMw4O-b00", "duration": "20 min"},
                    ],
                }

                col_nav, col_content = st.columns([1, 2.2], gap="large")
                with col_nav:
                    st.markdown("#### 📂 Modules")
                    module_names = list(course_content.keys())
                    if "curr_module" not in st.session_state: st.session_state.curr_module = module_names[0]
                    selected_module = st.selectbox("Kies module:", module_names, label_visibility="collapsed")
                    st.session_state.curr_module = selected_module
                    videos_in_module = course_content[selected_module]
                    if "curr_video" not in st.session_state: st.session_state.curr_video = videos_in_module[0]['title']
                    
                    for v in videos_in_module:
                        title = v['title']
                        is_active = (title == st.session_state.curr_video)
                        btn_type = "primary" if is_active else "secondary"
                        if st.button(f"📺 {title}", key=f"nav_{title}", type=btn_type, use_container_width=True):
                            st.session_state.curr_video = title
                            st.rerun()

                with col_content:
                    current_video = next((v for v in videos_in_module if v['title'] == st.session_state.curr_video), videos_in_module[0])
                    st.markdown(f"### {current_video['title']}")
                    st.video(current_video['url'])
                    
                    vid_id = f"vid_{abs(hash(current_video['title']))}"
                    if vid_id not in completed_steps:
                        if st.button("✅ Les Afronden (+15 XP)", type="primary"):
                            auth.mark_step_complete(vid_id, 15)
                            st.balloons()
                            st.rerun()
                    else:
                        st.success("Deze les is voltooid! ✅")


    elif pg == "Producten Zoeken":
        # --- HEADER ---
        st.markdown("<h1><i class='bi bi-search'></i> Winning Product Hunter</h1>", unsafe_allow_html=True)
        st.caption("De ultieme toolkit om winstgevende producten te vinden en te analyseren.")

        # =========================================================
        # 🏆 SECTIE 1: PRO DAILY WINNERS (EXCLUSIEF VOOR PRO)
        # =========================================================
        if is_pro:
            with st.container(border=True):
                st.markdown("### 🏆 PRO Daily Winners")
                st.write("Onze AI selectie van de 3 grootste kanshebbers van vandaag.")
                if st.button("✨ Onthul Winners van Vandaag", type="primary", use_container_width=True):
                    picks = db.get_daily_winners_from_db()
                    if picks:
                        st.session_state.pro_daily_picks = picks
                    else:
                        st.error("Winners worden momenteel ververst. Probeer het over 5 minuten opnieuw.")

                if "pro_daily_picks" in st.session_state:
                    picks = st.session_state.pro_daily_picks
                    cols = st.columns(3)
                    for idx, item in enumerate(picks):
                        with cols[idx]:
                            with st.container(border=True):
                                if item.get('cover_url'): st.image(item['cover_url'], use_container_width=True)
                                st.markdown(f"**{item.get('title', 'Product')[:35]}...**")
                                st.info(f"💡 {item.get('reason', 'Hoge viraliteit.')}")
                                c1, c2 = st.columns(2)
                                c1.link_button("🎵 Bekijk", item.get('video_url', '#'), use_container_width=True)
                                if c2.button("✍️ Script", key=f"pro_script_{idx}", use_container_width=True):
                                    st.session_state.workflow_product = item.get('title', '')
                                    st.session_state.nav_index = 3
                                    st.rerun()
        else:
            # Gratis gebruikers zien de 'Locked' state voor Daily Winners
            render_pro_lock("Daily Winners 🔒", "Krijg elke dag 3 kant-en-klare winstgevende producten.", "Exclusief voor PRO studenten.")

        # =========================================================
        # 🔍 SECTIE 2: DE ZOEK TOOLS (1x Gratis voor Demo gebruikers)
        # =========================================================
        st.markdown("---")
        tab1, tab2, tab3 = st.tabs(["🔥 Viral TikTok Hunter", "🧿 Meta Ad Spy", "🕵️ Concurrenten Spy"]) 
        
        # --- TAB 1: TIKTOK HUNTER ---
        with tab1:
            st.markdown("""
                <div style="background:#F8FAFC; border-left: 4px solid #2563EB; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                    <p style="margin:0; color:#1E293B; font-weight: 700;">🌪️ The Viral Hunter</p>
                    <p style="margin:0; color:#64748B; font-size:0.9rem;">Vind producten die <b>nu</b> viraal gaan op TikTok.</p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.container(border=True):
                st.write("**Stel je filters in:**")
                search_query = st.text_input("Zoekwoord of Hashtag:", value="tiktokmademebuyit", key="hunter_q")
                col_f1, col_f2 = st.columns(2)
                min_v = col_f1.selectbox("Min. Views", [10000, 100000, 500000], index=1)
                sort_o = col_f2.selectbox("Sorteer op", ["Views", "Omzet", "Viral Score"])

                # Knop label verandert op basis van status
                btn_label = "🚀 Zoek Winners" if is_pro else "🚀 Zoek Winners (1x Gratis Zoeken)"
                
                if st.button(btn_label, type="primary", use_container_width=True):
                    if db.can_user_search(user['email'], is_pro):
                        with st.status(f"🕵️‍♂️ Scannen naar '{search_query}'...", expanded=True) as status:
                            from modules import viral_finder
                            results = viral_finder.search_tiktok_winning_products(search_query, min_v, sort_o)
                            if results == "LIMIT_REACHED":
                                status.update(label="⚠️ Serverlimiet bereikt", state="error", expanded=False)
                            else:
                                status.update(label="Analyse voltooid!", state="complete", expanded=False)
                            st.session_state.tiktok_results = results
                    else:
                        st.warning("⚠️ Je hebt je gratis zoekopdracht voor vandaag verbruikt.")
                        st.info("Upgrade naar PRO voor onbeperkt product-onderzoek.")

            # Resultaten tonen (als ze er zijn)
            if st.session_state.get("tiktok_results") == "LIMIT_REACHED":
                st.error("De servers zijn momenteel overbelast. Probeer de PRO Daily Winners.")
            elif st.session_state.get("tiktok_results"):
                res = st.session_state.tiktok_results
                for i in range(0, len(res), 2):
                    ca, cb = st.columns(2)
                    def draw_item(col, item, k):
                        with col:
                            with st.container(border=True):
                                if item.get('cover'): st.image(item['cover'], use_container_width=True)
                                st.markdown(f"**{item['desc'][:50]}...**")
                                st.metric("Views", f"{item['views']//1000}k")
                                c1, c2 = st.columns(2)
                                c1.link_button("🎵 Bekijk", item['url'], use_container_width=True)
                                if c2.button("✍️ Script", key=f"tk_scr_{k}", use_container_width=True):
                                    st.session_state.workflow_product = item['desc']
                                    st.session_state.nav_index = 3
                                    st.rerun()
                    draw_item(ca, res[i], i)
                    if i+1 < len(res): draw_item(cb, res[i+1], i+1)

        # --- TAB 2: META AD SPY ---
        with tab2:
            st.markdown("### 🧿 Meta (Facebook) Ad Spy")
            with st.container(border=True):
                fb_query = st.text_input("Zoekwoord voor advertenties:", placeholder="Bijv. Home Decor", key="fb_q")
                fb_btn_label = "🕵️‍♂️ Scan Facebook Ads" if is_pro else "🕵️‍♂️ Scan Facebook Ads (1x Gratis)"
                
                if st.button(fb_btn_label, type="primary", use_container_width=True):
                    if db.can_user_search(user['email'], is_pro):
                        with st.spinner("Facebook Ad Library wordt doorzocht..."):
                            from modules import facebook_spy
                            st.session_state.fb_results = facebook_spy.search_facebook_ads(fb_query, max_results=30)
                    else:
                        st.warning("⚠️ Je dagelijkse gratis scan is op!")

                if st.session_state.get("fb_results"):
                    for ad in st.session_state.fb_results[:12]:
                        with st.container(border=True):
                            c1, c2 = st.columns([1, 2])
                            if ad['media']: c1.image(ad['media'], use_container_width=True)
                            c2.markdown(f"**{ad['page_name']}**")
                            c2.caption(f"Actief: {ad['days_active']} dagen")
                            c2.link_button("🛒 Bekijk Shop", ad['shop_link'], use_container_width=True)

        # --- TAB 3: CONCURRENTEN SPY ---
        with tab3:
            st.markdown("### 🕵️ Shopify Store Spy")
            # Deze tool is technisch lichter, maar we houden hem voor PRO om waarde te behouden
            if is_pro:
                url_in = st.text_input("URL van concurrent:", placeholder="www.concurrent.nl")
                if url_in and st.button("🚀 Scan Producten", type="primary"):
                    from modules import competitor_spy
                    prods = competitor_spy.scrape_shopify_store(url_in)
                    if prods:
                        for p in prods:
                            st.write(f"📦 **{p['title']}** - {p['price']}")
            else:
                render_pro_lock("Store Spy 🔒", "Scan elke Shopify store voor hun bestsellers.", "Exclusief voor studenten.")


    elif pg == "Marketing & Design": 
        st.markdown("<h1><i class='bi bi-palette-fill'></i> Marketing & Design</h1>", unsafe_allow_html=True)
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Logo Maker", "Video Scripts", "Teksten Schrijven", "Advertentie Check", "🩺 Store Doctor"])
        
        with tab1:
            st.markdown("**ℹ️ Wat doet deze tool?**\n\nMaak binnen 10 seconden een uniek logo voor je merk. Typ je naam in en kies een stijl.")
            
            # --- INIT SESSION STATE VOOR LOGOS ---
            if "logo_generations" not in st.session_state: st.session_state.logo_generations = 0
            if "generated_logos" not in st.session_state: st.session_state.generated_logos = [] 
            
            # Check toegang
            has_access = is_pro or st.session_state.logo_generations < 3
            
            if not has_access: 
                render_pro_lock("Credits op", "Je hebt 3 gratis logo's gemaakt. Word student om onbeperkt te genereren.", "Concurrenten betalen €200 voor een logo. Jij krijgt dit gratis.")
            else:
                if not is_pro: 
                    st.info(f"🎁 Je hebt nog **{3 - st.session_state.logo_generations}** gratis logo generaties over.")
                
                with st.container(border=True):
                    col1, col2 = st.columns(2)
                    brand_name = col1.text_input("Bedrijfsnaam", placeholder="Bijv. Lumina")
                    niche = col1.text_input("Niche", placeholder="Bijv. Online growth, speed")
                    style = col2.selectbox("Stijl", ["Minimalistisch", "Modern & strak", "Vintage", "Luxe", "Speels"])
                    color = col2.text_input("Voorkeurskleuren", placeholder="Bijv. Zwart en goud")
                    
                    # GENEREER KNOP
                    if st.button("Genereer logo's", type="primary", use_container_width=True):
                        if not brand_name or not niche: 
                            st.warning("Vul alles in.")
                        else:
                            st.session_state.logo_generations += 1
                            with st.spinner("Onze designers zijn bezig... (Dit duurt ca. 10 sec)"):
                                import requests
                                
                                new_logos = []
                                for i in range(3):
                                    img_url = ai_coach.generate_logo(brand_name, niche, style, color)
                                    if img_url and "placehold" not in img_url:
                                        try:
                                            resp = requests.get(img_url)
                                            if resp.status_code == 200:
                                                new_logos.append({
                                                    "url": img_url,
                                                    "data": resp.content,
                                                    "name": f"logo_{brand_name}_{i+1}.png"
                                                })
                                        except: pass
                                
                                if new_logos:
                                    st.session_state.generated_logos = new_logos
                                else:
                                    st.error("Er ging iets mis bij het genereren. Probeer het opnieuw.")

                # --- WEERGAVE ---
                if st.session_state.generated_logos:
                    st.markdown("---")
                    st.markdown("### 🎉 Jouw resultaten:")
                    st.success("Tip: Klik op de knop onder het logo om hem in hoge kwaliteit op te slaan.")
                    
                    cols = st.columns(3)
                    for idx, logo in enumerate(st.session_state.generated_logos):
                        with cols[idx]:
                            st.image(logo["url"], use_container_width=True)
                            st.download_button(
                                label="📥 Download Logo",
                                data=logo["data"],
                                file_name=logo["name"],
                                mime="image/png",
                                key=f"dl_btn_persistent_{idx}",
                                use_container_width=True
                            )
                    
                    if st.button("Opnieuw beginnen (Wist huidige logo's)", type="secondary"):
                        st.session_state.generated_logos = []
                        st.rerun()

        with tab2:
            st.markdown("**ℹ️ Wat doet deze tool?**\n\nWeet je niet wat je moet zeggen in je video? Deze tool schrijft virale scripts voor TikTok en Instagram Reels.")
            if is_pro:
                with st.container(border=True):
                    # Haal het product op dat is doorgestuurd vanuit de Hunter
                    default_prod = st.session_state.get('workflow_product', '')
                    
                    # De 'value' zorgt dat het veld al ingevuld is
                    prod = st.text_input("Voor welk product wil je een script?", value=default_prod, key="vid_prod_input")
                    
                    if st.button("Genereer scripts", type="primary", key="vid_btn"):
                        if prod:
                            with st.spinner("AI schrijft je virale script..."):
                                res = ai_coach.generate_viral_scripts(prod, "", "Viral")
                                st.markdown("### 🪝 Hooks")
                                for h in res['hooks']: st.info(h)
                                with st.expander("📄 Volledig Script"): st.write(res['full_script'])
                                with st.expander("📝 Briefing voor Creator"): st.code(res['creator_brief'])
                        else:
                            st.warning("Vul eerst een productnaam in.")
            else: render_pro_lock("Viral video scripts", "Laat AI scripts schrijven.", "Dit script ging vorige week 3x viraal. Alleen voor studenten.")
        
        with tab3:
            st.markdown("**ℹ️ Wat doet deze tool?**\nLaat AI een verkopende productbeschrijving schrijven of een berichtje maken om naar influencers te sturen.")
            t_desc, t_inf = st.tabs(["🛍️ Beschrijvingen", "🤳 Influencer Script"])
            with t_desc:
                with st.container(border=True):
                    # WORKFLOW PRE-FILL
                    default_prod = st.session_state.get('workflow_product', '')
                    prod_name = st.text_input("Productnaam / URL (AliExpress)", value=default_prod, placeholder="Bv. Galaxy Star Projector")
                    
                    if st.button("✨ Genereer Beschrijving", type="primary", use_container_width=True):
                        if not prod_name: st.warning("Vul een naam in.")
                        elif check_credits():
                            with st.spinner("AI is aan het schrijven..."):
                                res = ai_coach.generate_product_description(prod_name)
                                st.markdown(res)
                                st.success("Tekst gegenereerd!")
                        else: st.warning("Je dagelijkse credits zijn op. Word student voor onbeperkt toegang.")
            with t_inf:
                with st.container(border=True):
                    inf_prod = st.text_input("Jouw Product", placeholder="Bv. Organic Face Serum")
                    if st.button("📩 Genereer DM Script", type="primary", use_container_width=True):
                        if not inf_prod: st.warning("Vul een product in.")
                        elif check_credits():
                            with st.spinner("Script schrijven..."):
                                res = ai_coach.generate_influencer_dm(inf_prod)
                                st.code(res, language="text")
                                st.success("Kopieer en plak dit in Instagram DM!")
                        else: st.warning("Je dagelijkse credits zijn op.")
        
        with tab4:
            st.markdown("### 🩺 De Advertentie Dokter")
            st.write("Upload een screenshot van je ad. De AI beoordeelt hem als een strenge media-buyer.")
            
            if is_pro:
                with st.container(border=True):
                    # Stap 1: Context geven
                    c1, c2, c3 = st.columns(3)
                    platform = c1.selectbox("Platform", ["Facebook / Insta Feed", "Instagram Story/Reel", "TikTok"])
                    goal = c2.selectbox("Doel", ["Sales (Conversie)", "Leads", "Kliks"])
                    niche_ad = c3.text_input("Niche", placeholder="Bv. Beauty")
                    
                    # Stap 2: Upload
                    uploaded_file = st.file_uploader("Upload screenshot van je ad (of video thumbnail)", type=['png', 'jpg', 'jpeg'])
                    
                    if uploaded_file and st.button("Start Diagnose 🚑", type="primary", use_container_width=True):
                        if not niche_ad:
                            st.warning("Vul ook even je niche in voor beter advies.")
                        else:
                            with st.spinner("De dokter kijkt naar je advertentie... even geduld."):
                                 # We roepen de nieuwe Vision functie aan
                                 audit = ai_coach.analyze_ad_screenshot(uploaded_file, platform, goal, niche_ad)
                                 
                                 if audit:
                                     st.markdown("---")
                                     
                                     # SCORE CARD
                                     score = audit.get('score', 5)
                                     
                                     # Kleur bepalen
                                     if score >= 8: color = "green"
                                     elif score >= 6: color = "orange"
                                     else: color = "red"
                                     
                                     # De Header
                                     st.markdown(f"""
                                     <div style="text-align:center; padding: 20px; background:#F8FAFC; border-radius:12px; border:1px solid #E2E8F0;">
                                         <h2 style="margin:0; color:{color}; font-size: 3rem;">{score}/10</h2>
                                         <h3 style="margin:0; color:#1E293B;">{audit.get('titel', 'Analyse Compleet')}</h3>
                                     </div>
                                     """, unsafe_allow_html=True)
                                     
                                     st.markdown("<br>", unsafe_allow_html=True)
                                     
                                     # De Details
                                     c_hook, c_copy = st.columns(2)
                                     with c_hook:
                                         st.info(f"**👁️ De Hook (Beeld):**\n\n{audit.get('analyse_hook')}")
                                     with c_copy:
                                         st.info(f"**✍️ De Copy (Tekst):**\n\n{audit.get('analyse_copy')}")
                                         
                                     # De Actiepunten
                                     st.markdown("#### 🛠️ Direct aanpassen:")
                                     for punt in audit.get('verbeterpunten', []):
                                         st.error(f"👉 {punt}")
                                         
                                     st.success("Pas dit aan en test opnieuw!")
                                 else:
                                     st.error("Kon de afbeelding niet analyseren. Probeer een kleiner bestand of ander formaat.")

            else: 
                render_pro_lock("Ad Audit", "Laat je advertenties beoordelen door AI.", "Voorkom dat je €1000 verspilt aan een slechte advertentie. Laat de AI hem eerst checken.")

        # --- TAB 5: STORE DOCTOR (NIEUW) ---
        with tab5:
            st.markdown("### 🩺 The Store Doctor")
            st.write("Laat AI je webshop scannen en krijg direct een rapportcijfer + verbeterpunten.")
            
            if is_pro:
                with st.container(border=True):
                    store_url = st.text_input("Jouw Webshop URL:", placeholder="bijv. www.mijnshop.nl")
                    
                    if st.button("🏥 Start Audit", type="primary", use_container_width=True):
                        if "." not in store_url:
                            st.warning("Vul een geldige URL in.")
                        else:
                            with st.spinner("De dokter is bezig met de operatie... 👨‍⚕️"):
                                # 1. Scrape tekst
                                scrape_res = competitor_spy.scrape_homepage_text(store_url)
                                
                                if scrape_res['status'] == 'success':
                                    # 2. AI Analyse
                                    audit_rapport = ai_coach.analyze_store_audit(scrape_res)
                                    
                                    st.markdown("---")
                                    st.markdown("### 📋 Het Rapport")
                                    st.markdown(audit_rapport)
                                    st.balloons()
                                else:
                                    st.error(f"Kon de shop niet scannen: {scrape_res['message']}")
            else:
                render_pro_lock("Store Doctor", "Laat je shop keuren door AI.", "Voorkom dat je live gaat met fouten die je sales kosten.")

    elif pg == "Financiën":
        st.markdown("<h1><i class='bi bi-cash-stack'></i> Financiën</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["💡 Winst Calculator", "📈 Dagelijkse Stats"])
        
        with tab1:
            st.markdown("""
            <div style="background:#F0FDF4; padding:15px; border-radius:8px; border:1px solid #BBF7D0; margin-bottom:20px; color:#166534;">
                <b>💰 Gratis Tool:</b> Gebruik dit <u>VOORDAT</u> je geld uitgeeft aan inkoop.
                Weet zeker dat je product winstgevend is.
            </div>
            """, unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("### 🧮 Product Profit Calculator")
                c1, c2 = st.columns(2)
                
                # WORKFLOW PRE-FILL
                default_price = st.session_state.get('workflow_price', 29.95)
                
                vp = c1.number_input("Verkoopprijs (€)", value=float(default_price), step=1.0)
                ip = c1.number_input("Inkoop + Verzenden (€)", value=12.00, step=0.50)
                cpa = c2.number_input("Verwachte Ads kosten (CPA) (€)", value=10.00, step=0.50, help="Gemiddeld kost een sale €10-€15 aan ads.")
                
                tr = vp * 0.03 # Transactiekosten schatting
                winst = vp - (ip + cpa + tr)
                marge = (winst / vp * 100) if vp > 0 else 0
                
                st.markdown("---")
                cc1, cc2, cc3 = st.columns(3)
                cc1.metric("Transactiekosten (est.)", f"€{tr:.2f}")
                cc2.metric("Netto Winst", f"€{winst:.2f}", delta="Goed bezig" if winst > 5 else "Risicovol", delta_color="normal")
                cc3.metric("Marge", f"{marge:.1f}%", delta="> 20% is doel" if marge > 20 else "Te laag", delta_color="normal")
                
                if winst < 0:
                    st.error("⚠️ Pas op: Je maakt verlies met deze prijzen!")

        with tab2:
            st.markdown("**ℹ️ Wat doet deze tool?**\n\nHier zie je in één oogopslag of je vandaag winst of verlies hebt gemaakt. Vul elke ochtend je cijfers in.")
            with st.container(border=True):
                st.markdown("#### 📅 Resultaten van vandaag")
                c1, c2, c3 = st.columns(3)
                rev = c1.number_input("Totale Omzet (€)", 0.0, step=10.0, help="Alles wat Shopify zegt dat je hebt verkocht.")
                spend = c2.number_input("Advertentiekosten (€)", 0.0, step=5.0, help="Wat je aan Facebook/TikTok hebt betaald.")
                cogs = c3.number_input("Inkoopkosten (€)", 0.0, step=5.0, help="Wat de producten jou kosten bij de leverancier.")
                if st.button("Opslaan in Database", type="primary"):
                    if db.save_daily_stats(user['email'], rev, spend, cogs): st.success("Opgeslagen! Check de grafieken hieronder.")
                    else: st.error("Kon niet opslaan (Database error).")
            history = db.get_daily_stats_history(user['email'])
            if history:
                st.markdown("### 📊 Trends & Cijfers (Laatste 7 dagen)")
                df = pd.DataFrame(history)
                df['Profit'] = df['revenue'] - df['ad_spend'] - df['cogs']
                df['ROAS'] = df.apply(lambda x: x['revenue'] / x['ad_spend'] if x['ad_spend'] > 0 else 0, axis=1)
                total_rev = df['revenue'].sum()
                total_profit = df['Profit'].sum()
                avg_roas = df['ROAS'].mean()
                col1, col2, col3 = st.columns(3)
                col1.metric("Totaal Omzet", f"€{total_rev:.2f}")
                col2.metric("Netto Winst", f"€{total_profit:.2f}", delta="Winstgevend" if total_profit > 0 else "Verlies", delta_color="normal")
                col3.metric("Gemiddelde ROAS", f"{avg_roas:.2f}", delta="> 3.0 is top" if avg_roas > 3 else "Kan beter", delta_color="off")
                st.bar_chart(df, x="date", y="Profit", color="#10B981") 
                with st.expander("Bekijk ruwe data"): st.dataframe(df)
            else: st.info("Nog geen data. Vul hierboven je eerste dag in om de grafieken te zien!")

    elif pg == "Instellingen":
        st.markdown("<h1><i class='bi bi-gear-fill'></i> Instellingen</h1>", unsafe_allow_html=True)
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Profiel", "Partner", "Koppelingen", "Hulp", "Feedback"])
        
        with tab1:
            # --- PROFIEL PAGINA (PLAYER CARD STYLE) ---
            st.markdown("### 👤 Jouw Profiel")
            
            with st.container(border=True):
                col_p1, col_p2 = st.columns([1, 3], vertical_alignment="center")
                
                with col_p1:
                    # Grote Avatar Letter
                    display_name = user.get('first_name') or "Gast"
                    letter = display_name[0].upper()
                    st.markdown(f"""
                    <div style="width:80px; height:80px; background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); 
                    border-radius:50%; display:flex; justify-content:center; align-items:center; 
                    font-size:35px; color:#2563EB; font-weight:800; border:3px solid #BFDBFE; margin: 0 auto;">
                        {letter}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_p2:
                    # Naam & Status Badge
                    user_status = "Student 🎓" if is_pro else "Gast 👤"
                    status_color = "#DCFCE7" if is_pro else "#F1F5F9"
                    status_text_color = "#166534" if is_pro else "#64748B"
                    
                    st.markdown(f"""
                    <h3 style="margin:0; padding:0;">{display_name}</h3>
                    <div style="margin-top:5px; margin-bottom:10px;">
                        <span style="background:{status_color}; color:{status_text_color}; padding: 4px 10px; border-radius:15px; font-size:0.8rem; font-weight:700; border: 1px solid rgba(0,0,0,0.05);">
                            {user_status}
                        </span>
                        <span style="color:#94A3B8; font-size:0.9rem; margin-left:10px;">{user['email']}</span>
                    </div>
                    """, unsafe_allow_html=True)

                # Voortgangsbalkje in profiel
                st.markdown("---")
                c_lvl, c_xp = st.columns([1, 4], vertical_alignment="bottom")
                c_lvl.markdown(f"**Lvl {user['level']}**")
                # Herbereken percentage voor visualisatie
                range_span = next_xp_goal_sidebar - prev_threshold
                xp_pct = min((user['xp'] - prev_threshold) / range_span, 1.0)
                c_xp.progress(xp_pct)
                c_xp.caption(f"Nog {next_xp_goal_sidebar - user['xp']} XP tot volgende level")

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🚪 Uitloggen", use_container_width=True):
                    cookie_manager.delete("rmecom_user_email")
                    st.session_state.clear()
                    st.rerun()

        with tab2:
            # --- DYNAMISCHE HEADER OP BASIS VAN STATUS ---
            if is_pro:
                st.markdown("""
                <div style="text-align:center; margin-bottom: 20px;">
                    <h2 style="color:#1E40AF; margin-bottom:5px;">💼 RM Partner Programma</h2>
                    <p style="color:#64748B;">Je bent nu PRO-lid. Verdien <b>€250,-</b> per student die onze curcus via jouw gaat volgen</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align:center; margin-bottom: 20px;">
                    <h2 style="color:#166534; margin-bottom:5px;">💸 Verdien €250,- per echte student</h2>
                    <p style="color:#64748B;">Help anderen starten en gebruik je winst om zelf gratis <b>PRO</b> te worden.</p>
                </div>
                """, unsafe_allow_html=True)

            # 2. De Stats (Blijft hetzelfde, maar met strakkere labels)
            stats = auth.get_affiliate_stats()
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric("Kliks op link", stats[0] * 5)
            with col_s2:
                st.metric("Inschrijvingen", stats[1])
            with col_s3:
                st.metric("Commissie", f"€{stats[2]}", delta="Betaalbaar op aanvraag")

            # 3. Conversie blok
            with st.container(border=True):
                if is_pro:
                    st.markdown("#### 📈 Jouw Partner Business")
                    st.write("Als PRO-lid heb je een streepje voor. Deel je ervaringen in de community en help anderen.")
                else:
                    st.markdown("#### 🚀 Hoe word ik gratis PRO?")
                    st.write("Eén enkele referral (Student levert je €250,- op. Dat is genoeg voor **5 maanden gratis PRO-toegang**.")

            # --- DEEL ACTIES ---
            current_ref = user.get('referral_code', 'TEMP')
            share_link = f"https://rmacademy.onrender.com/?ref={current_ref}"
            
            st.markdown("### 🔗 Jouw Unieke Partner Link")
            st.code(share_link, language="text")
            
            c_whatsapp, c_copy = st.columns(2)
            with c_whatsapp:
                share_text = f"Hee! Ik volg nu het RM Ecom traject. Als je ook een webshop wilt starten, gebruik mijn link voor een vliegende start: {share_link}"
                wa_url = f"https://wa.me/?text={urllib.parse.quote(share_text)}"
                st.link_button("💚 Deel via WhatsApp", wa_url, use_container_width=True)
            
            with c_copy:
                if st.button("📋 Link Kopiëren", use_container_width=True):
                    st.toast("Link gekopieerd naar klembord!", icon="✅")
                    if "share_xp_claimed" not in st.session_state:
                        auth.mark_step_complete("share_bonus_action", 50)
                        st.session_state.share_xp_claimed = True
                        st.rerun()

            # 4. Extra uitleg voor PRO
            if is_pro:
                with st.expander("ℹ️ Uitbetalingsinformatie"):
                    st.write("""
                    - Commissies worden 30 dagen na de inschrijving van de student goedgekeurd (ivm wettelijke bedenktijd).
                    - Uitbetalingen vinden plaats op de 1e van de maand.
                    - Stuur een bericht via de 'Hulp' tab om je eerste uitbetaling aan te vragen.
                    """)
                
        with tab3:
            with st.container(border=True):
                st.markdown("#### Shopify koppeling")
                sh_url = st.text_input("Shop URL", value=st.session_state.get("sh_url", ""), placeholder="mijnshop.myshopify.com")
                sh_token = st.text_input("Private app token", type="password", value=st.session_state.get("sh_token", ""))
                if st.button("Opslaan", use_container_width=True):
                    st.session_state["sh_url"] = sh_url.strip()
                    st.session_state["sh_token"] = sh_token.strip()
                    st.success("Opgeslagen.")
        
        with tab4:
            # --- HULP PAGINA (DUIDELIJKE KEUZE) ---
            st.markdown("### 🆘 Waar heb je hulp bij nodig?")
            st.markdown("Kies de juiste weg voor het snelste antwoord.")

            col_h1, col_h2 = st.columns(2)

            with col_h1:
                with st.container(border=True):
                    st.markdown("""
                    <div style="text-align:center;">
                        <div style="font-size:40px; margin-bottom:10px;">💬</div>
                        <h4 style="margin:0;">Vragen over E-com?</h4>
                        <p style="font-size:0.85rem; color:#64748B; min-height:40px;">
                            "Hoe werkt Shopify?", "Is dit product goed?".<br>Vraag het aan 500+ andere studenten.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button("Naar Discord Community", COMMUNITY_URL, type="primary", use_container_width=True)

            with col_h2:
                with st.container(border=True):
                    st.markdown("""
                    <div style="text-align:center;">
                        <div style="font-size:40px; margin-bottom:10px;">⚙️</div>
                        <h4 style="margin:0;">Account Problemen?</h4>
                        <p style="font-size:0.85rem; color:#64748B; min-height:40px;">
                            Inloggen lukt niet, wachtwoord vergeten of betalingsvragen.<br>Wij helpen je persoonlijk.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button("Stuur Email", "mailto:support@rmecom.nl", use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("❓ Veelgestelde vragen"):
                st.markdown("""
                **Is de app gratis?**
                Ja, de basis is gratis. Voor geavanceerde tools (Spy Tool, AI content) heb je de cursus nodig.
                
                **Hoe krijg ik meer XP?**
                Voltooi stappen in de Roadmap of gebruik de tools in het dashboard.
                
                **Mijn vriendencode werkt niet?**
                Neem even contact op via de mail, dan lossen we het op!
                """)
        
        with tab5:
            st.markdown("#### 💡 Jouw mening telt")
            
            # Check in de database of de gebruiker de beloning al eens heeft gehad
            has_claimed_before = user.get('feedback_reward_claimed', False)

            if has_claimed_before and not is_pro_license:
                if is_temp_pro:
                    st.success(f"✅ Je 24u PRO toegang is momenteel actief! (Nog {time_left_str})")
                else:
                    st.info("Je hebt je eenmalige 24u PRO beloning al gebruikt. Word PRO lid voor onbeperkte toegang.")
                    st.link_button("Word PRO Lid", STRATEGY_CALL_URL, use_container_width=True)
            
            elif st.session_state.get("feedback_done", False):
                st.success("Bedankt! Je feedback is verwerkt.")
            
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); border: 1px solid #FCD34D; padding: 15px; border-radius: 12px; margin-bottom: 20px;">
                    <h4 style="margin: 0; color: #92400E; font-size: 1rem;">🎁 Cadeau: 24u PRO Toegang</h4>
                    <p style="margin: 2px 0 0 0; font-size: 0.85rem; color: #B45309;">
                        Geef ons eerlijke feedback en unlock direct alle PRO tools voor 24 uur.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                fb_text = st.text_area("Wat vind je van de app tot nu toe?", placeholder="Wat mis je nog? Wat kan beter?", height=120, key="feedback_text_input")
                
                if st.button("Verstuur & Claim 24u PRO 🚀", use_container_width=True, key="feedback_submit_btn"):
                    if len(fb_text) > 20:
                        with st.spinner("Bezig met verwerken..."):
                            is_valid = ai_coach.validate_feedback(fb_text)
                            
                            if is_valid:
                                status = db.claim_feedback_reward(user['email'], fb_text)
                                
                                if status == "SUCCESS":
                                    st.cache_data.clear() # ZEER BELANGRIJK: Maakt de cache leeg
                                    st.session_state.feedback_done = True
                                    st.balloons()
                                    st.success("🎉 PRO Geactiveerd! Je hebt nu 24 uur toegang.")
                                    time.sleep(2)
                                    st.rerun() # Herlaad de app met de nieuwe status
                                else:
                                    st.error("Je hebt deze beloning al eens geclaimd.")
                            else:
                                st.warning("Je feedback is te kort of onduidelijk. Vertel ons echt wat je vindt!")
                    else:
                        st.warning("Vertel ons iets meer (minimaal 20 tekens) om de beloning te unlocken.")

    # --- DE FOOTER (STAAT ONDERAAN ELKE PAGINA) ---
    render_footer()

