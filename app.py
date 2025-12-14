--- START OF FILE app.py ---

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
from modules import ai_coach, ui, auth, shopify_client, competitor_spy, roadmap

# --- 0. CONFIGURATIE ---
STRATEGY_CALL_URL = "https://calendly.com/rmecomacademy/30min"
COMMUNITY_URL = "https://discord.com"
COACH_VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 

# Probeer het logo te laden
fav_icon = "🚀"
try:
    fav_icon = Image.open("assets/logo.png") 
except:
    pass

st.set_page_config(
    page_title="RM Ecom Academy",
    page_icon=fav_icon,
    layout="wide",
    initial_sidebar_state="auto"
)

# --- 1.5 META TAGS & PWA NAAM FIX ---
st.markdown("""
<script>
    var link = document.querySelector("link[rel~='icon']");
    if (!link) {
        link = document.createElement('link');
        link.rel = 'icon';
        document.getElementsByTagName('head')[0].appendChild(link);
    }
    link.href = 'assets/logo.png';
</script>
<meta name="application-name" content="RM Ecom Academy">
<meta name="apple-mobile-web-app-title" content="RM Ecom">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
""", unsafe_allow_html=True)

# --- 1. CSS ENGINE (MET BOOTSTRAP ICONS & SAMSUNG FIXES & BLUE THEME) ---
st.markdown("""
    <style>
        /* Import Bootstrap Icons */
        @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css");

        /* ==============================================
           1. ALGEMENE CONFIGURATIE
           ============================================== */
        :root {
            --primary: #2563EB;
            --bg-light: #F8FAFC;
            --text-dark: #0F172A;
            --white: #FFFFFF;
            /* Donkerdere randkleur voor betere zichtbaarheid op Samsung */
            --border: #94A3B8; 
            
            /* FORCEER LIGHT MODE */
            color-scheme: light !important; 
        }

        .stApp {
            background-color: var(--bg-light) !important;
            color: var(--text-dark) !important;
        }

        /* Iconen styling */
        .bi { margin-right: 6px; vertical-align: -0.125em; }
        h1, h2, h3 { color: #0F172A !important; }
        * { -webkit-tap-highlight-color: transparent !important; }

        /* ==============================================
           2. HEADER WEG & KNOP ZICHTBAAR
           ============================================== */
        header[data-testid="stHeader"] { background-color: transparent !important; border-bottom: none !important; pointer-events: none !important; }

        [data-testid="stSidebarCollapseButton"] {
            display: flex !important; visibility: visible !important; pointer-events: auto !important;
            align-items: center !important; justify-content: center !important; position: fixed !important;
            top: 15px !important; left: 15px !important; z-index: 1000005 !important;
            background-color: #FFFFFF !important; border: 2px solid #94A3B8 !important; /* Dikkere rand */
            border-radius: 8px !important; width: 44px !important; height: 44px !important;
        }
        [data-testid="stSidebarCollapseButton"] svg { fill: #2563EB !important; stroke: #2563EB !important; }
        @media (min-width: 992px) { [data-testid="stSidebarCollapseButton"] { display: none !important; } }
        [data-testid="stDecoration"], [data-testid="stToolbar"], [data-testid="stStatusWidget"], footer, #MainMenu, [data-testid="stHeaderActionElements"] { 
            visibility: hidden !important; display: none !important; 
        }
        .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a { display: none !important; pointer-events: none; }

        /* ==============================================
           3. UI ELEMENTEN & SAMSUNG ZICHTBAARHEID FIX
           ============================================== */
        
        /* A. INPUT VELDEN: Dikke rand & Zwarte tekst */
        input, textarea, select, .stTextInput > div > div > input {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border: 2px solid #94A3B8 !important; /* ZICHTBARE RAND */
            border-radius: 8px !important;
            -webkit-text-fill-color: #0F172A !important;
            opacity: 1 !important;
        }

        /* B. LABELS */
        .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextarea label, label p {
            color: #0F172A !important; font-weight: 700 !important;
        }

        /* C. ROADMAP ITEMS (EXPANDERS) */
        /* 1. Normale staat: Wit blok, Donkere rand, ZWARTE TEKST */
        .streamlit-expanderHeader {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border: 2px solid #94A3B8 !important; /* ZICHTBARE RAND */
            border-radius: 8px !important;
            transition: all 0.2s;
            margin-bottom: 8px !important;
        }
        /* Dit was ik vergeten in het vorige bericht -> Forceer tekst zwart in rust */
        .streamlit-expanderHeader p, .streamlit-expanderHeader span, .streamlit-expanderHeader div { 
            color: #0F172A !important; 
            font-weight: 600 !important; 
        }
        .streamlit-expanderHeader svg { 
            fill: #0F172A !important; 
        }

        /* 2. Interactie staat (Klik/Focus): Donkere achtergrond, WITTE TEKST */
        .streamlit-expanderHeader:hover, .streamlit-expanderHeader:active, .streamlit-expanderHeader:focus, .streamlit-expanderHeader:focus-visible {
            background-color: #1E293B !important; 
            border-color: #0F172A !important; 
            color: #FFFFFF !important;
        }
        /* Forceer alle tekst/iconen naar wit bij interactie */
        .streamlit-expanderHeader:hover *, .streamlit-expanderHeader:active *, .streamlit-expanderHeader:focus *, .streamlit-expanderHeader:focus-visible * {
            color: #FFFFFF !important; 
            fill: #FFFFFF !important; 
            stroke: #FFFFFF !important;
        }

        /* Dropdown menu fix */
        div[data-baseweb="select"] > div { background-color: #FFFFFF !important; color: #0F172A !important; border-color: #94A3B8 !important; }
        ul[data-baseweb="menu"] { background-color: #FFFFFF !important; border: 1px solid #94A3B8 !important; }
        li[data-baseweb="option"] { color: #0F172A !important; background-color: #FFFFFF !important; }
        li[data-baseweb="option"]:hover, li[data-baseweb="option"][aria-selected="true"] { background-color: #EFF6FF !important; }

        /* Checkbox fix */
        input[type="checkbox"] { 
            accent-color: #2563EB !important; 
            background-color: #FFFFFF !important;
            border: 1px solid #94A3B8 !important; /* Randje zichtbaar maken */
        }

        /* ==============================================
           4. LAYOUT & STIJL
           ============================================== */
        .block-container { padding-top: 3rem !important; padding-bottom: 5rem !important; max-width: 1000px; }
        [data-testid="stSidebar"] .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; }
        
        /* Visuele Roadmap */
        .progress-container { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; position: relative; padding: 0 10px; }
        .progress-line { position: absolute; top: 50%; left: 0; width: 100%; height: 3px; background: #E2E8F0; z-index: 1; transform: translateY(-50%); }
        .progress-step { width: 32px; height: 32px; border-radius: 50%; display: flex; justify-content: center; align-items: center; z-index: 2; position: relative; background: white; border: 2px solid #E2E8F0; color: #94A3B8; font-weight: bold; font-size: 0.8rem; transition: all 0.3s; }
        .progress-step.active { border-color: #2563EB; color: white; background: #2563EB; box-shadow: 0 0 0 4px rgba(37,99,235,0.1); }
        .progress-step.completed { background: #10B981; border-color: #10B981; color: white; }
        .progress-label { position: absolute; bottom: -25px; left: 50%; transform: translateX(-50%); font-size: 0.7rem; white-space: nowrap; color: #64748B; font-weight: 600; }

        /* Cards styling */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            background: white; border-radius: 16px; padding: 24px; margin-bottom: 20px;
        }

        /* ==============================================
           5. FORCEREN VAN BLAUWE THEMA KLEUREN
           ============================================== */
        
        /* Start Direct Knop -> BLAUW */
        div.stButton > button[kind="primary"] {
            background-color: #2563EB !important; 
            border-color: #2563EB !important; 
            color: white !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #1D4ED8 !important; 
            border-color: #1D4ED8 !important;
        }
        div.stButton > button[kind="primary"]:focus {
            box-shadow: none !important;
            border-color: #1D4ED8 !important;
        }

        /* Tab lijntjes -> BLAUW */
        div[data-baseweb="tab-highlight"] { background-color: #2563EB !important; }
        
        /* Tab tekst kleuren */
        button[data-baseweb="tab"] div p { color: #64748B !important; font-weight: 600 !important; }
        button[data-baseweb="tab"][aria-selected="true"] div p { color: #2563EB !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. COOKIE MANAGER ---
cookie_manager = stx.CookieManager()
if "user" not in st.session_state:
    cookie_email = cookie_manager.get("rmecom_user_email")
    if cookie_email:
        try:
            auth.login_or_register(cookie_email)
        except: pass

# --- 3. LOGIN SCHERM ---
if "user" not in st.session_state:
    if "status" in st.query_params:
        st.query_params.clear()

    col_left, col_right = st.columns([1, 1.1], gap="large", vertical_alignment="center")

    with col_left:
        st.markdown("<div class='logo-text'><i class='bi bi-lightning-charge-fill' style='color:#2563EB;'></i> RM Ecom Academy</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <h1>Van 0 naar <span style='color:#2563EB'>€15k/maand</span> met je eigen webshop.</h1>
        <p style='color:#64748B; font-size:1.05rem; margin-bottom: 30px; line-height: 1.6;'>
            De enige app die je stap-voor-stap begeleidt. Geen technische kennis nodig. Start vandaag <b>gratis</b>.
        </p>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            tab_free, tab_pro = st.tabs(["Start challenge", "Student login"])
            with tab_free:
                col_name, col_email = st.columns(2)
                with col_name:
                    first_name = st.text_input("Voornaam", placeholder="Je naam...", label_visibility="collapsed", key="reg_name")
                with col_email:
                    email = st.text_input("Email", placeholder="Je email...", label_visibility="collapsed", key="login_email_free")
                with st.expander("Heb je een vriendencode? (optioneel)"):
                    ref_code = st.text_input("Vriendencode", placeholder="bv. JAN-482", label_visibility="collapsed", key="ref_code_input")
                st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
                if st.button("Start direct (gratis)", type="primary", use_container_width=True):
                    if email and "@" in email and first_name:
                        with st.spinner("Account aanmaken..."):
                            auth.login_or_register(email, ref_code_input=ref_code if 'ref_code' in locals() and ref_code else None, name_input=first_name)
                            cookie_manager.set("rmecom_user_email", email, expires_at=datetime.now() + timedelta(days=30))
                            st.rerun()
                    else:
                        st.warning("Vul je naam en een geldig e-mailadres in.")
                st.markdown("""<div style='text-align:center; margin-top:8px; line-height:1.4;'><div style='font-size:0.75rem; color:#64748B; font-weight:500;'><i class="bi bi-lock-fill" style="font-size:10px; color:#64748B;"></i> Geen creditcard nodig <span style='color:#CBD5E1;'>|</span> Direct toegang</div></div>""", unsafe_allow_html=True)
                
                # --- REVIEWS ---
                st.markdown("""
                <div style='display: flex; align-items: center; justify-content: center; gap: 6px; margin-top: 10px; opacity: 0.9;'>
                    <div style="color: #F59E0B; font-size: 0.8rem;">
                        <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i>
                    </div>
                    <span style='font-size: 0.75rem; color: #64748B; font-weight: 500;'>4.9/5 (550+ studenten)</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            with tab_pro:
                st.markdown("<small style='color:#64748b'>Welkom terug, topper.</small>", unsafe_allow_html=True)
                pro_email = st.text_input("Jouw email:", placeholder="Vul hier je emailadres in...", key="log_mail")
                lic_key = st.text_input("Licentie code", placeholder="Vul hier je code in...", type="password", label_visibility="collapsed", key="log_lic")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Inloggen", type="primary", use_container_width=True):
                    if pro_email and lic_key:
                        auth.login_or_register(pro_email, license_input=lic_key)
                        cookie_manager.set("rmecom_user_email", pro_email, expires_at=datetime.now() + timedelta(days=30))
                        st.rerun()
                    else:
                        st.warning("Vul al je gegevens in.")

    with col_right:
        st.markdown("<br class='desktop-only'>", unsafe_allow_html=True)
        raw_html = """
        <div style="background: white; padding: 30px; border-radius: 20px; border: 1px solid #E2E8F0; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.08); color: #0F172A;">
            <h3 style="margin-top:0; color:#0F172A; font-size:1.15rem; font-weight: 700;">Dit krijg je gratis:</h3>
            <div style="display:flex; gap:16px; margin-bottom:24px; align-items:center;">
                <div style="width:48px; height:48px; background:#EFF6FF; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px;">
                    <i class="bi bi-map-fill" style="color:#2563EB;"></i>
                </div>
                <div><h4 style="margin:0; font-size:0.95rem; font-weight:600; color:#0F172A;">De 'Van 0 naar sales' roadmap</h4></div>
            </div>
            <div style="display:flex; gap:16px; margin-bottom:24px; align-items:center;">
                <div style="width:48px; height:48px; background:#F0FDF4; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px;">
                    <i class="bi bi-robot" style="color:#16A34A;"></i>
                </div>
                <div><h4 style="margin:0; font-size:0.95rem; font-weight:600; color:#0F172A;">Jouw eigen AI coach</h4></div>
            </div>
            <div style="display:flex; gap:16px; align-items:center;">
                <div style="width:48px; height:48px; background:#FFF7ED; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px;">
                    <i class="bi bi-trophy-fill" style="color:#EA580C;"></i>
                </div>
                <div><h4 style="margin:0; font-size:0.95rem; font-weight:600; color:#0F172A;">Level-based groei</h4></div>
            </div>
        </div>
        """
        st.markdown(raw_html.replace("\n", ""), unsafe_allow_html=True)
    st.stop()

# --- 4. INGELOGDE DATA ---
user = st.session_state.user
is_pro = user['is_pro']

def get_greeting():
    hour = datetime.now().hour
    if hour < 12: return "Goedemorgen"
    elif hour < 18: return "Goedemiddag"
    else: return "Goedenavond"

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded}"
    except:
        return None

# --- SIDEBAR (MET DUIDELIJKE PROGRESSIE) ---
with st.sidebar:
    rank_title, next_xp_goal_sidebar = auth.get_rank_info(user['xp'])
    display_name = user.get('first_name') or user['email'].split('@')[0].capitalize()
    
    st.markdown(f"""
    <div style="margin-bottom: 2px; padding-left: 5px;">
        <h3 style="margin:0; font-size:1.0rem; color:#0F172A;"><i class="bi bi-person-circle"></i> {display_name}</h3>
        <p style="margin:0; font-size: 0.75rem; color: #64748B;">
            <span style="background:#EFF6FF; padding:2px 6px; border-radius:4px; border:1px solid #DBEAFE; color:#2563EB; font-weight:600;">Lvl {user['level']}</span> {rank_title}
        </p>
    </div>
    """, unsafe_allow_html=True)

    prev_threshold = 0
    for t in [0, 200, 500, 1000]:
        if user['xp'] >= t: prev_threshold = t
    range_span = next_xp_goal_sidebar - prev_threshold
    if range_span <= 0: range_span = 1
    xp_pct = min((user['xp'] - prev_threshold) / range_span, 1.0) * 100
    
    st.markdown(textwrap.dedent(f"""
    <div style="background: #E2E8F0; border-radius: 4px; height: 6px; width: 100%; margin-top: 8px; margin-bottom: 4px;">
        <div style="background: #2563EB; height: 100%; width: {xp_pct}%; border-radius: 4px; transition: width 0.5s;"></div>
    </div>
    <div style="text-align:right; font-size:0.7rem; color:#94A3B8; margin-bottom:15px;">
        {user['xp']} / {next_xp_goal_sidebar} XP
    </div>
    """), unsafe_allow_html=True)
    
    options = ["Dashboard", "Gratis training", "Logo maker", "Product ideeën", "Winst Calculator", "Concurrenten", "Video ideeën", "Ads check", "Instellingen"]
    icons = ["house-fill", "mortarboard-fill", "palette-fill", "search", "calculator-fill", "bar-chart-fill", "camera-reels-fill", "bandaid-fill", "gear-fill"]
    
    menu_display_options = []
    for opt in options:
        if not is_pro and opt in ["Logo maker", "Product ideeën", "Concurrenten", "Video ideeën", "Ads check"]:
            menu_display_options.append(f"{opt} 🔒")
        else:
            menu_display_options.append(opt)

    selected_display = option_menu(
        menu_title=None,
        options=menu_display_options,
        icons=icons,
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#64748B", "font-size": "14px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "1px", "padding": "8px", "--hover-color": "#EFF6FF", "color": "#0F172A"},
            "nav-link-selected": {"background-color": "#2563EB", "color": "white", "font-weight": "600"},
        }
    )
    
    pg = selected_display.replace(" 🔒", "")

    if not is_pro:
        st.markdown(f"""
        <div style="margin-top: 10px; padding: 8px; background: #F8FAFC; border-radius: 6px; border: 1px dashed #94A3B8; text-align: center;">
            <a href="{STRATEGY_CALL_URL}" target="_blank" style="text-decoration:none; color: #2563EB; font-weight: 700; font-size: 0.8rem;">
                Word student <i class="bi bi-arrow-right"></i>
            </a>
        </div>
        """, unsafe_allow_html=True)

# --- LOCK SCREEN COMPONENT (BLURRED STYLE) ---
def render_pro_lock(title, desc):
    lock_html = f"""
    <div style="position: relative; overflow: hidden; border-radius: 12px; border: 1px solid #94A3B8; margin-top: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); background: #F8FAFC;">
        <div style="filter: blur(5px); opacity: 0.5; padding: 30px; pointer-events: none; user-select: none;">
            <h3 style="color: #64748B; margin-bottom: 15px;">██████ ██████</h3>
            <div style="height: 15px; background: #CBD5E1; width: 80%; margin-bottom: 10px; border-radius: 4px;"></div>
            <div style="height: 15px; background: #E2E8F0; width: 60%; margin-bottom: 10px; border-radius: 4px;"></div>
            <div style="height: 15px; background: #E2E8F0; width: 70%; margin-bottom: 20px; border-radius: 4px;"></div>
            <div style="display:flex; gap:15px;">
                <div style="height: 120px; background: #E2E8F0; width: 30%; border-radius: 8px;"></div>
                <div style="height: 120px; background: #E2E8F0; width: 30%; border-radius: 8px;"></div>
                <div style="height: 120px; background: #E2E8F0; width: 30%; border-radius: 8px;"></div>
            </div>
        </div>
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(255,255,255,0.4); backdrop-filter: blur(4px);">
            <div style="background: white; padding: 30px 40px; border-radius: 16px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 1px solid #DBEAFE; max-width: 400px;">
                <div style="font-size: 32px; margin-bottom: 10px;">🔒</div>
                <h3 style="margin: 0 0 5px 0; color: #1E293B; font-size: 1.1rem; font-weight: 700;">{title}</h3>
                <p style="font-size: 0.9rem; color: #64748B; margin: 0 0 20px 0; line-height: 1.5;">{desc}</p>
                <a href="{STRATEGY_CALL_URL}" target="_blank" style="text-decoration: none;">
                    <div style="background: linear-gradient(135deg, #2563EB, #1D4ED8); color: white; padding: 12px 28px; border-radius: 50px; font-weight: 600; font-size: 0.95rem; display: inline-block; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2); transition: transform 0.1s;">
                        🚀 Unlock via Shop Review Call
                    </div>
                </a>
                <div style="margin-top: 12px; font-size: 0.75rem; color: #94A3B8; font-weight: 500;">
                    <i class="bi bi-people-fill"></i> Al door 550+ studenten gebruikt
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(lock_html.replace("\n", ""), unsafe_allow_html=True)

# --- CONTENT PAGES ---

if pg == "Dashboard":
    name = user.get('first_name') or user['email'].split('@')[0].capitalize()
    
    st.markdown(f"<h1 style='margin-bottom: 15px;'>{get_greeting()}, {name} <i class='bi bi-hand-thumbs-up-fill' style='color:#FBBF24;'></i></h1>", unsafe_allow_html=True)
    
    completed_steps = auth.get_progress()
    full_map = roadmap.get_roadmap()
    
    next_step_title = "Alles afgerond! 🎉"
    next_step_phase = "Klaar"
    next_step_phase_index = 0
    next_step_id = None
    next_step_locked = False
    
    # Bepaal huidige fase index voor progress bar
    fase_keys = list(full_map.keys())
    for idx, (fase_key, fase) in enumerate(full_map.items()):
        phase_done = True
        for s in fase['steps']:
            if s['id'] not in completed_steps:
                next_step_title = s['title']
                next_step_phase = fase['title'].split(":")[0]
                next_step_phase_index = idx + 1 # 1-based index voor visual
                next_step_id = s['id']
                next_step_locked = s.get('locked', False)
                phase_done = False
                break
        if not phase_done: break
        # Als we hier zijn is de hele fase klaar, check of we bij de laatste zijn
        if phase_done and idx == len(fase_keys) - 1:
            next_step_phase_index = 6 # Alles klaar

    # --- NIEUWE FEATURE: VISUELE PROGRESS BAR (PUNT 3) ---
    html_steps = ""
    labels = ["Start", "Bouwen", "Product", "Trust", "Scale"]
    
    for i in range(1, 6):
        status_class = ""
        if i < next_step_phase_index:
            status_class = "completed"
        elif i == next_step_phase_index:
            status_class = "active"
        
        icon_content = f'<i class="bi bi-check-lg"></i>' if status_class == "completed" else f"{i}"
        
        # ALLES OP 1 REGEL OM FOUTEN TE VOORKOMEN
        html_steps += f'<div class="progress-step {status_class}">{icon_content}<div class="progress-label">{labels[i-1]}</div></div>'
    
    st.markdown(f'<div class="progress-container"><div class="progress-line"></div>{html_steps}</div>', unsafe_allow_html=True)
    # --- EINDE NIEUWE FEATURE ---

    logo_base64 = get_image_base64("assets/logo.png")
    
    if logo_base64:
        bg_icon_html = f"""<div style="position: absolute; top: 20px; right: 20px; width: 150px; opacity: 0.25; pointer-events: none;"><img src="{logo_base64}" style="width: 100%; height: auto;"></div>"""
    else:
        bg_icon_html = '<div style="position: absolute; top: 10px; right: 20px; font-size: 100px; opacity: 0.15; color: white;"><i class="bi bi-rocket-takeoff-fill"></i></div>'

    # --- SLIMME KAART (LOCKED vs UNLOCKED) ---
    is_step_pro = next_step_locked and not is_pro
    
    if is_step_pro:
        card_bg = "linear-gradient(135deg, #0F172A 0%, #1E293B 100%)" 
        accent_color = "#F59E0B" 
        btn_text = "🚀 Word Student"
        btn_bg = "linear-gradient(to bottom, #FBBF24, #D97706)"
        btn_url = STRATEGY_CALL_URL
        btn_target = "_blank"
        card_icon = "bi-lock-fill"
        status_text = "Deze stap is exclusief voor studenten."
        title_color = "#FFFFFF" 
        card_border = "1px solid #F59E0B"
    else:
        card_bg = "linear-gradient(135deg, #2563EB 0%, #1E40AF 100%)"
        accent_color = "#DBEAFE" 
        btn_text = "Start Direct <i class='bi bi-play-fill'></i>"
        btn_bg = "#FBBF24"
        btn_url = "#mission"
        btn_target = "_self"
        card_icon = "bi-crosshair"
        status_text = "Focus op deze taak om verder te komen."
        title_color = "#FFFFFF"
        card_border = "1px solid rgba(255,255,255,0.1)"

    # Platgeslagen HTML string
    mission_html = f"""<div style="background: {card_bg}; padding: 24px; border-radius: 16px; color: white; margin-bottom: 20px; box-shadow: 0 10px 30px -5px rgba(0,0,0,0.4); border: {card_border}; position: relative; overflow: hidden;">{bg_icon_html}<div style="position: relative; z-index: 2;"><div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.9; margin-bottom: 8px; font-weight: 700; color: {accent_color};"><i class="bi {card_icon}"></i> JOUW VOLGENDE STAP</div><div style="margin: 0; font-size: 1.7rem; color: {title_color} !important; font-weight: 800; letter-spacing: -0.5px; line-height: 1.2; text-shadow: 0 2px 4px rgba(0,0,0,0.3); margin-bottom: 8px;">{next_step_title}</div><p style="margin: 8px 0 24px 0; font-size:0.95rem; opacity:0.9; max-width: 600px; line-height: 1.6; color: #F1F5F9;">{status_text}</p><a href="{btn_url}" target="{btn_target}" style="text-decoration:none;"><div style="display: inline-block; background: {btn_bg}; color: #78350F; padding: 12px 28px; border-radius: 8px; font-weight: 800; font-size: 0.95rem; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.2); transition: transform 0.1s; border: 1px solid rgba(255,255,255,0.2);">{btn_text}</div></a></div></div>"""
    st.markdown(mission_html, unsafe_allow_html=True)
    
    current_title, next_xp_goal = auth.get_rank_info(user['xp'])
    needed = next_xp_goal - user['xp']
    next_reward = "Spy tool" if user['level'] < 2 else "Video scripts"

    cols = st.columns(3) 
    with cols[0]:
        st.markdown(f"""<div style="background:white; padding:15px; border-radius:12px; border:1px solid #E2E8F0; text-align:center;"><div style="font-size:0.75rem; color:#64748B; font-weight:700;"><i class="bi bi-bar-chart-fill"></i> LEVEL</div><div style="font-size:1.5rem; font-weight:800; color:#0F172A;">{user['level']}</div><div style="font-size:0.75rem; color:#64748B;">{current_title}</div></div>""", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""<div style="background:white; padding:15px; border-radius:12px; border:1px solid #E2E8F0; text-align:center;"><div style="font-size:0.75rem; color:#64748B; font-weight:700;"><i class="bi bi-lightning-fill"></i> XP</div><div style="font-size:1.5rem; font-weight:800; color:#0F172A;">{user['xp']}</div><div style="font-size:0.75rem; color:#64748B;">Nog {needed} tot next lvl</div></div>""", unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""<div style="background:white; padding:15px; border-radius:12px; border:1px solid #E2E8F0; text-align:center;"><div style="font-size:0.75rem; color:#64748B; font-weight:700;"><i class="bi bi-gift-fill"></i> NEXT REWARD</div><div style="font-size:1.5rem; font-weight:800; color:#0F172A;">🎁</div><div style="font-size:0.75rem; color:#2563EB;">{next_reward}</div></div>""", unsafe_allow_html=True)
    
    st.markdown("<div id='mission' style='height: 20px;'></div>", unsafe_allow_html=True)

    # --- ROADMAP MET FOCUS MODE ---
    st.markdown("### 📍 Roadmap")

    for fase_key, fase in full_map.items():
        steps = fase['steps']
        
        st.markdown(f"#### {fase['title']}")
        st.caption(fase['desc'])
        
        for step in steps:
            is_done = step['id'] in completed_steps
            is_active = step['id'] == next_step_id
            
            if is_done:
                with st.expander(f"✅ {step['title']}", expanded=False):
                    st.info("Deze stap heb je al afgerond. Goed bezig!")
            
            elif is_active:
                just_completed_id, xp = roadmap.render_step_card(step, is_done, is_pro, expanded=True)
                if just_completed_id:
                    auth.mark_step_complete(just_completed_id, xp)
                    st.balloons()
                    st.rerun()
            
            else:
                icon = "bi-lock-fill" if step.get('locked', False) else "bi-circle"
                st.markdown(f"""<div style="padding: 12px 16px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #94A3B8; font-size: 0.9rem; margin-bottom: 8px; display: flex; align-items: center; gap: 10px;"><i class="bi {icon}"></i> {step['title']}</div>""", unsafe_allow_html=True)
        
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

elif pg == "Gratis training":
    st.markdown("<h1><i class='bi bi-mortarboard-fill'></i> Gratis mini training</h1>", unsafe_allow_html=True)
    st.caption("Korte training om je eerste stappen als e-commerce starter snel helder te krijgen.")
    t1, t2 = st.columns(2)
    t3, t4 = st.columns(2)
    
    def video_header(text):
        st.markdown(f"<div style='font-weight:700; font-size:0.95rem; margin-bottom:8px; color:#0F172A;'>{text}</div>", unsafe_allow_html=True)

    with t1:
        video_header("1. Mindset & realistische verwachtingen")
        with st.container(border=True):
            st.markdown('<iframe src="https://drive.google.com/file/d/1xyM_9q2i5FJBF__HvmhDrHTBueBoBstv/preview" width="100%" height="300" style="border-radius:8px; border:none;"></iframe>', unsafe_allow_html=True)
        st.info("Noteer na deze video in 3 bulletpoints waarom je deze webshop wilt. Dat helpt je bij tegenslag.")
    with t2:
        video_header("2. Hoe werkt een winstgevende webshop echt")
        with st.container(border=True):
            st.markdown('<iframe src="https://drive.google.com/file/d/1O4fa0FUA10MnCE4QqNNDe3XSLwLfkb_F/preview" width="100%" height="300" style="border-radius:8px; border:none;"></iframe>', unsafe_allow_html=True)
        st.info("Let extra op: verkeer, conversie en marge. Schrijf 1 actie op per blok.")
    with t3:
        video_header("3. Je eerste sale neerzetten")
        with st.container(border=True):
            st.markdown('<iframe src="https://drive.google.com/file/d/1xyM_9q2i5FJBF__HvmhDrHTBueBoBstv/preview" width="100%" height="300" style="border-radius:8px; border:none;"></iframe>', unsafe_allow_html=True)
        st.success("Na deze video kies je één product en één kanaal. Niet alles tegelijk.")
    with t4:
        video_header("4. Van 1 naar 100 sales")
        with st.container(border=True):
            st.markdown('<iframe src="https://drive.google.com/file/d/1O4fa0FUA10MnCE4QqNNDe3XSLwLfkb_F/preview" width="100%" height="300" style="border-radius:8px; border:none;"></iframe>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div style="background: #F0F9FF; padding: 25px; border-radius: 12px; border: 1px solid #BAE6FD; text-align: center;"><h4 style="color:#0369A1; margin-bottom:6px;">Klaar voor het echte werk?</h4><p style="color:#0C4A6E; margin:0;">Je hebt de basis gezien. Wil je dat we meekijken zodat dit ook echt gaat draaien?</p></div>""", unsafe_allow_html=True)
        st.link_button("Plan gratis strategie call", STRATEGY_CALL_URL, type="primary", use_container_width=True)

elif pg == "Logo maker":
    st.markdown("<h1><i class='bi bi-palette-fill'></i> Logo maker</h1>", unsafe_allow_html=True)
    if "logo_generations" not in st.session_state: st.session_state.logo_generations = 0
    has_access = is_pro or st.session_state.logo_generations < 3
    if not has_access:
        render_pro_lock("Je gratis logo credits zijn op", "Je hebt 3 gratis logo's gemaakt. Word student om onbeperkt te genereren.")
    else:
        if not is_pro:
            credits_left = 3 - st.session_state.logo_generations
            st.info(f"🎁 Je hebt nog **{credits_left}** gratis logo generaties over.")
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                brand_name = st.text_input("Bedrijfsnaam", placeholder="Bijv. Lumina")
                niche = st.text_input("Niche / industrie", placeholder="Bijv. Moderne verlichting")
            with col2:
                style = st.selectbox("Stijl", ["Minimalistisch", "Modern & strak", "Vintage / retro", "Luxe & elegant", "Speels & kleurrijk"])
                color = st.text_input("Voorkeurskleuren", placeholder="Bijv. Zwart en goud, of Pastelblauw")
            # CLEAN BUTTON TEXT
            if st.button("Genereer 3 logo concepten", type="primary", use_container_width=True):
                if not brand_name or not niche: st.warning("Vul alles in.")
                else:
                    st.session_state.logo_generations += 1
                    with st.spinner("AI is aan het ontwerpen..."):
                        images = []
                        for i in range(3):
                            img_url = ai_coach.generate_logo(brand_name, niche, style, color)
                            if img_url: images.append(img_url)
                        if images:
                            st.success("Logo's gegenereerd!")
                            cols = st.columns(3)
                            for idx, img in enumerate(images):
                                with cols[idx]: 
                                    st.image(img, use_container_width=True)
                                    st.caption(f"Optie {idx+1}")
                        else: st.error("Mislukt.")

elif pg == "Product ideeën":
    st.markdown("<h1><i class='bi bi-search'></i> Product ideeën</h1>", unsafe_allow_html=True)
    if not is_pro: render_pro_lock("Ontgrendel echte winnende producten", "Als student krijg je toegang tot de Product Inspirator.")
    else:
        with st.container(border=True):
            col_inp, col_btn = st.columns([3, 1])
            niche = col_inp.text_input("In welke niche zoek je een product?", "Gadgets")
            # CLEAN BUTTON TEXT
            if col_btn.button("Zoek ideeën", type="primary", use_container_width=True):
                results = ai_coach.find_real_winning_products(niche, "Viral")
                if results:
                    st.markdown(f"**Resultaten voor '{niche}':**")
                    for p in results:
                        title = p.get("title", "Naamloos product")
                        price = p.get("price", 29.95)
                        hook = p.get("hook", "")
                        search_links = p.get("search_links", {})
                        with st.container(border=True):
                            st.markdown(f"### {title}")
                            st.caption(f"Richtprijs verkoop: €{price}")
                            st.write(f"💡 **Waarom viral:** {hook}")
                            if search_links:
                                c1, c2 = st.columns(2)
                                c1.link_button("TikTok", search_links['tiktok'], use_container_width=True)
                                c2.link_button("AliExpress", search_links['ali'], use_container_width=True)
        st.markdown("---")
        st.header("Product Validator")
        with st.container(border=True):
            c1 = st.checkbox("Probleem/Wow: Lost het een pijnlijk probleem op?")
            c2 = st.checkbox("Niet lokaal: Kun je dit NIET lokaal kopen?")
            c3 = st.checkbox("Marge: Kan ik het verkopen voor min €25?")
            c4 = st.checkbox("Content: Kan ik hier zelf video's over maken?")
            if c1 and c2 and c3 and c4: st.success("GROEN LICHT! Ga naar de calculator.")

elif pg == "Winst Calculator":
    st.markdown("<h1><i class='bi bi-calculator-fill'></i> Rijkrekenaar</h1>", unsafe_allow_html=True)
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            verkoop_prijs = st.number_input("Verkoopprijs", value=29.95)
            inkoop_prijs = st.number_input("Inkoop + Verzenden", value=12.00)
        with c2:
            adv_kosten = st.number_input("Ads kosten (CPA)", value=10.00)
            transactie = verkoop_prijs * 0.03
    winst = verkoop_prijs - (inkoop_prijs + adv_kosten + transactie)
    marge = (winst / verkoop_prijs * 100) if verkoop_prijs > 0 else 0
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Netto Winst", f"€{winst:.2f}")
    c2.metric("Marge", f"{marge:.1f}%")

elif pg == "Concurrenten":
    st.markdown("<h1><i class='bi bi-graph-up-arrow'></i> Concurrenten</h1>", unsafe_allow_html=True)
    if is_pro:
        with st.container(border=True):
            url = st.text_input("URL van concurrent")
            # CLEAN BUTTON TEXT
            if url and st.button("Scan bestsellers", type="primary"):
                 with st.spinner("Scannen..."):
                     products = competitor_spy.scrape_shopify_store(url)
                     if products:
                         for p in products:
                             with st.container(border=True):
                                 c1, c2 = st.columns([1, 3])
                                 if p['image_url']: c1.image(p['image_url'])
                                 c2.markdown(f"**{p['title']}**")
                                 c2.caption(f"Prijs: €{p['price']}")
                                 c2.markdown(f"[Bekijk]({p['original_url']})")
    else: render_pro_lock("Concurrenten spy tool", "Zie bestsellers van andere shops.")

elif pg == "Video ideeën":
    st.markdown("<h1><i class='bi bi-camera-video-fill'></i> Video ideeën</h1>", unsafe_allow_html=True)
    if is_pro:
        with st.container(border=True):
            prod = st.text_input("Product")
            # CLEAN BUTTON TEXT
            if st.button("Genereer scripts", type="primary") and prod:
                res = ai_coach.generate_viral_scripts(prod, "", "Viral")
                st.markdown("### Hooks")
                for h in res['hooks']: st.info(h)
                with st.expander("Script"): st.text_area("Script", res['full_script'])
                with st.expander("Briefing"): st.code(res['creator_brief'])
    else: render_pro_lock("Viral video scripts", "Laat AI scripts schrijven.")

elif pg == "Ads check":
    st.markdown("<h1><i class='bi bi-activity'></i> Ads check</h1>", unsafe_allow_html=True)
    if is_pro:
        with st.container(border=True):
            st.info("Upload screenshot van Ads Manager.")
            st.file_uploader("Bestand")
            st.text_area("Vraag")
            st.button("Diagnose starten", type="primary")
    else: render_pro_lock("Ads check", "Laat je advertenties beoordelen.")

elif pg == "Instellingen":
    st.markdown("<h1><i class='bi bi-gear-fill'></i> Instellingen</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["Profiel", "Partner", "Koppelingen", "Hulp"])
    
    with tab1:
        with st.container(border=True):
            display_name = user.get('first_name') or user['email'].split('@')[0].capitalize()
            letter = display_name[0].upper()
            st.markdown(f"""
                <div style="display:flex; align-items:center; gap:20px; margin-bottom:20px;">
                    <div style="width:60px; height:60px; background:#EFF6FF; border-radius:50%; display:flex; justify-content:center; align-items:center; font-size:24px; color:#2563EB; font-weight:bold; border:2px solid #2563EB;">
                        {letter}
                    </div>
                    <div>
                        <h3 style="margin:0;">{display_name}</h3>
                        <p style="margin:0; color:#64748B;">{user['email']}</p>
                        <p style="margin:0; font-size:0.8rem; color:#64748B;">Status: {'Student' if is_pro else 'Gast'}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Uitloggen", use_container_width=True):
                cookie_manager.delete("rmecom_user_email")
                st.session_state.clear()
                st.rerun()

    with tab2:
        stats = auth.get_affiliate_stats()
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-card">
                <div class="metric-label">Totaal aangemeld</div>
                <div class="metric-value">{stats[0]}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Studenten via jou</div>
                <div class="metric-value">{stats[1]}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Geschat verdiend</div>
                <div class="metric-value">€{stats[2]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("#### Jouw vrienden code")
            st.caption("Deel deze code met mensen die willen starten. Zij krijgen een voordeel en jij ontvangt commissie.")
            st.code(user['referral_code'], language="text")

    with tab3:
        with st.container(border=True):
            st.markdown("#### Shopify koppeling")
            st.caption("Vul hier je shop URL en privé API token in als je producten vanuit de tools naar Shopify wilt sturen.")
            
            sh_url = st.text_input("Shop URL", value=st.session_state.get("sh_url", ""), placeholder="mijnshop.myshopify.com")
            sh_token = st.text_input("Private app token", type="password", value=st.session_state.get("sh_token", ""))

            col_save, col_test = st.columns(2)
            with col_save:
                if st.button("Opslaan", use_container_width=True):
                    st.session_state["sh_url"] = sh_url.strip()
                    st.session_state["sh_token"] = sh_token.strip()
                    st.success("Shopify gegevens opgeslagen in deze sessie.")
            with col_test:
                if st.button("Test met demo product", use_container_width=True):
                    if not sh_url or not sh_token:
                        st.warning("Vul eerst je Shop URL en token in.")
                    else:
                        demo_product = {
                            "title": "Demo product vanuit RM Ecom",
                            "description": "Dit is een testproduct om te checken of de koppeling werkt.",
                            "price": 29.95,
                            "compare_price": 59.95,
                            "niche": "Demo",
                            "image_url": "",
                            "meta_title": "Demo product RM Ecom",
                            "meta_description": "Testproduct om je Shopify koppeling te controleren."
                        }
                        with st.spinner("Demo product sturen naar Shopify..."):
                            result = shopify_client.push_product_to_shopify(sh_url, sh_token, demo_product)
                        if result.get("success"):
                            st.success(result.get("msg", "Product succesvol doorgestuurd."))
                        else:
                            st.error(result.get("msg", "Er ging iets mis. Controleer je gegevens en probeer het opnieuw."))

    with tab4:
        with st.container(border=True):
            st.markdown("#### Support")
            st.link_button("Discord community", COMMUNITY_URL, use_container_width=True)
            st.link_button("Email support", "mailto:support@rmecom.nl", use_container_width=True)
        
        with st.expander("Veelgestelde vragen"):
            st.write("**Hoe werkt de XP?**")
            st.caption("Je krijgt XP voor elke afgeronde stap in de roadmap. XP ontgrendelt tijdelijke en vaste tools.")
            st.write("**Wanneer wordt commissie uitbetaald?**")
            st.caption("Uitbetalingen gebeuren maandelijks zodra je saldo boven de afgesproken drempel ligt.")