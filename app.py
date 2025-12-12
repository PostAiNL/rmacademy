import streamlit as st
import time
import urllib.parse
import random
import pandas as pd
import textwrap
from datetime import datetime, timedelta, timezone
import extra_streamlit_components as stx
from modules import ai_coach, ui, auth, shopify_client, competitor_spy, roadmap

# --- 0. CONFIGURATIE ---
STRATEGY_CALL_URL = "https://calendly.com/rmecomacademy/30min"
COMMUNITY_URL = "https://discord.com"
COACH_VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 

st.set_page_config(
    page_title="RM Ecom App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. PREMIUM CSS ENGINE ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        :root {
            --primary: #2563EB;
            --bg-light: #F8FAFC;
            --text-dark: #0F172A;
            --text-gray: #64748B;
            --white: #FFFFFF;
            --border: #CBD5E1;
        }

        * { -webkit-tap-highlight-color: transparent !important; }
        
        input[type="checkbox"] {
            accent-color: #2563EB !important;
            filter: none !important;
        }
        
        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border-color: #CBD5E1 !important;
        }
        ul[data-baseweb="menu"] { background-color: #FFFFFF !important; }
        li[data-baseweb="option"] { color: #0F172A !important; }

        .stApp {
            background-color: var(--bg-light) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-dark) !important;
        }
        
        [data-testid="stHeader"] {background: transparent;}
        [data-testid="stDecoration"] {display: none;}
        
        [data-testid="stSidebarCollapseButton"] { 
            display: block !important; 
            color: #2563EB !important;
        }
        [data-testid="stSidebarCollapseButton"] svg {
            fill: #2563EB !important;
            stroke: #2563EB !important;
        }
        
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1000px;
        }

        .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a, 
        .stMarkdown h4 a, .stMarkdown h5 a, .stMarkdown h6 a { 
            display: none !important; pointer-events: none; 
        }
        
        h1 {
            font-size: 2.2rem !important; font-weight: 800 !important;
            letter-spacing: -1px !important; color: #0F172A !important;
        }
        .logo-text {
            font-weight: 800; font-size: 1.1rem; color: #0F172A;
            display: flex; align-items: center; gap: 8px; margin-bottom: 15px;
        }

        .stButton button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            border: none !important;
            color: white !important;
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
            transition: transform 0.1s ease !important;
        }
        
        .stButton button:active, 
        .stButton button:focus, 
        .stButton button:focus-visible {
            background: #1E40AF !important;
            color: white !important;
            border: none !important;
            outline: none !important;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.2) !important;
        }

        .streamlit-expander, div[data-testid="stExpander"] {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
            margin-bottom: 10px !important;
            overflow: hidden;
        }
        
        div[data-testid="stExpander"] details { background-color: #FFFFFF !important; }
        div[data-testid="stExpander"] div[role="group"] { background-color: #FFFFFF !important; }
        div[data-testid="stExpander"] p { color: #0F172A !important; }
        
        .streamlit-expanderHeader {
            background-color: #FFFFFF !important;
            color: #1E293B !important;
        }
        .streamlit-expanderHeader p {
            font-size: 1rem !important;
            color: #1E293B !important;
            font-weight: 600 !important;
        }
        .streamlit-expanderHeader:hover {
            background-color: #F8FAFC !important;
            color: #2563EB !important;
        }
        .streamlit-expanderHeader svg {
            fill: #64748B !important;
        }

        div[data-testid="stWidgetLabel"] p, label p {
            color: #0F172A !important;
            font-weight: 600 !important;
        }
        .stTextInput input {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            color: #0F172A !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }
        .stTextInput input::placeholder {
            color: #94A3B8 !important;
            opacity: 1 !important;
        }
        .stTextInput input:focus {
            border-color: #2563EB !important;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
        }

        button[data-baseweb="tab"] { background-color: transparent !important; }
        button[data-baseweb="tab"] div p { color: #64748B !important; font-weight: 500; }
        button[data-baseweb="tab"][aria-selected="true"] div p { color: #2563EB !important; font-weight: 700; }
        div[data-baseweb="tab-highlight"] { background-color: #2563EB !important; }

        section[data-testid="stSidebar"] { background-color: var(--white); border-right: 1px solid var(--border); }
        section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }

        div[role="radiogroup"] > label > div:first-child { display: none !important; }
        div[role="radiogroup"] label {
            width: 100%; padding: 10px 14px; border-radius: 10px;
            color: var(--text-gray); font-weight: 500;
            cursor: pointer; transition: all 0.2s ease;
            margin-bottom: 4px; border: 1px solid transparent;
        }
        div[role="radiogroup"] label:hover { background-color: #F1F5F9; color: var(--text-dark); }
        div[role="radiogroup"] label[data-checked="true"] {
            background-color: #EFF6FF !important; color: #2563EB !important;
            font-weight: 600; border: 1px solid #DBEAFE;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 16px; background: var(--white); border: 1px solid var(--border);
            padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        .metric-container { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 25px; }
        .metric-card {
            background: var(--white); border: 1px solid var(--border); border-radius: 14px;
            padding: 16px; display: flex; flex-direction: column; align-items: center;
            text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.01);
        }
        .metric-label { font-size: 0.7rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }
        .metric-value { font-size: 1.6rem; font-weight: 800; color: var(--text-dark); }
        .metric-sub { font-size: 0.75rem; color: #10B981; font-weight: 600; margin-top: 2px; }

        .lock-container {
            text-align: center; padding: 60px 20px; background: white;
            border-radius: 16px; border: 1px solid #E2E8F0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.02);
        }

        .fab-container { position: fixed; bottom: 30px; right: 30px; z-index: 9999; }
        .fab-button {
            background: linear-gradient(135deg, #2563EB, #1D4ED8);
            color: white; width: 60px; height: 60px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 24px; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
            cursor: pointer; text-decoration: none; transition: transform 0.2s;
        }
        .fab-button:hover { transform: scale(1.1); }

        @media (max-width: 600px) {
            h1 { font-size: 1.8rem !important; line-height: 1.2 !important; }
            .logo-text { margin-bottom: 10px; }
            .block-container { padding-top: 1rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
            .metric-container { grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
            .metric-card { padding: 10px; }
            .metric-value { font-size: 1.2rem; }
            .metric-label { font-size: 0.6rem; }
            .fab-container { bottom: 20px; right: 20px; }
        }
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
        st.markdown("<div class='logo-text'>⚡ RM Ecom Academy</div>", unsafe_allow_html=True)
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
                
                if st.button("🚀 Start direct (gratis)", type="primary", use_container_width=True):
                    if email and "@" in email and first_name:
                        with st.spinner("Account aanmaken..."):
                            auth.login_or_register(email, ref_code_input=ref_code if 'ref_code' in locals() and ref_code else None, name_input=first_name)
                            cookie_manager.set("rmecom_user_email", email, expires_at=datetime.now() + timedelta(days=30))
                            st.rerun()
                    else:
                        st.warning("Vul je naam en een geldig e-mailadres in.")
                
                st.markdown("""
                <div style='text-align:center; margin-top:8px; line-height:1.4;'>
                    <div style='font-size:0.75rem; color:#64748B; font-weight:500; display:flex; align-items:center; justify-content:center; gap:6px;'>
                        <span style='opacity:0.8;'>🔒 Geen creditcard nodig</span> 
                        <span style='color:#CBD5E1;'>|</span> 
                        <span style='opacity:0.8;'>Direct toegang</span>
                    </div>
                    <div style='font-size:0.7rem; color:#94A3B8; margin-top:2px;'>
                        ⭐️ Al <b>550+ starters</b> gingen je voor.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            with tab_pro:
                st.markdown("<small style='color:#64748b'>Welkom terug, topper.</small>", unsafe_allow_html=True)
                pro_email = st.text_input("Jouw email:", placeholder="Vul hier je emailadres in...", key="log_mail")
                lic_key = st.text_input("Licentie code", placeholder="Vul hier je code in...", type="password", label_visibility="collapsed", key="log_lic")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("💎 Inloggen", type="primary", use_container_width=True):
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
                <div style="width:48px; height:48px; background:#EFF6FF; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0;">🗺️</div>
                <div>
                    <h4 style="margin:0; font-size:0.95rem; font-weight:600; color:#0F172A;">De 'Van 0 naar sales' roadmap</h4>
                    <p style="margin:2px 0 0 0; font-size:0.9rem; color:#64748B; line-height:1.4;">Precies weten wat je vandaag moet doen.</p>
                </div>
            </div>
            <div style="display:flex; gap:16px; margin-bottom:24px; align-items:center;">
                <div style="width:48px; height:48px; background:#F0FDF4; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0;">🤖</div>
                <div>
                    <h4 style="margin:0; font-size:0.95rem; font-weight:600; color:#0F172A;">Jouw eigen AI coach</h4>
                    <p style="margin:2px 0 0 0; font-size:0.9rem; color:#64748B; line-height:1.4;">Laat AI je teksten en scripts schrijven.</p>
                </div>
            </div>
            <div style="display:flex; gap:16px; align-items:center;">
                <div style="width:48px; height:48px; background:#FFF7ED; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0;">🏆</div>
                <div>
                    <h4 style="margin:0; font-size:0.95rem; font-weight:600; color:#0F172A;">Gamified groei</h4>
                    <p style="margin:2px 0 0 0; font-size:0.9rem; color:#64748B; line-height:1.4;">Level up en unlock tools terwijl je bouwt.</p>
                </div>
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

# --- SIDEBAR ---
with st.sidebar:
    rank_title, next_xp_goal_sidebar = auth.get_rank_info(user['xp'])
    display_name = user.get('first_name') or user['email'].split('@')[0].capitalize()
    
    st.markdown(f"""
    <div style="margin-bottom: 5px; padding-left: 2px;">
        <h3 style="margin:0; font-size:1rem; color:#0F172A;">👋 {display_name}</h3>
        <p style="margin:0; font-size: 0.75rem; color: #64748B;">{rank_title}</p>
    </div>
    """, unsafe_allow_html=True)

    prev_threshold = 0
    for t in [0, 200, 500, 1000]:
        if user['xp'] >= t: prev_threshold = t
    
    range_span = next_xp_goal_sidebar - prev_threshold
    if range_span <= 0: range_span = 1
        
    xp_pct = min((user['xp'] - prev_threshold) / range_span, 1.0) * 100
    
    st.markdown(textwrap.dedent(f"""
    <div style="background: #E2E8F0; border-radius: 4px; height: 8px; width: 100%; margin-top: 8px; margin-bottom: 15px;">
        <div style="background: #10B981; height: 100%; width: {xp_pct}%; border-radius: 4px; transition: width 0.5s;"></div>
    </div>
    """), unsafe_allow_html=True)
    
    menu_options = {
        "🏠 Dashboard": "Dashboard",
        "🎓 Gratis training": "Gratis Mini Training",
        "🎨 Logo maker": "Logo Maker",
        "🔍 Product ideeën": "Product Finder",
        "🧮 Winst Calculator": "Winst Calculator",
        "📊 Concurrenten": "Spy Tool",
        "🎬 Video ideeën": "Video Scripts",
        "🩺 Ads check": "Ads Doctor",
        "⚙️ Instellingen": "Instellingen"
    }
    
    display_options = []
    for icon_name, page_name in menu_options.items():
        if not is_pro and page_name in ["Product Finder", "Spy Tool", "Video Scripts", "Ads Doctor", "Logo Maker"]:
            display_options.append(f"{icon_name} 🔒")
        else:
            display_options.append(icon_name)

    selected_display = st.radio("Menu", display_options, label_visibility="collapsed")
    
    pg = "Dashboard"
    for key, val in menu_options.items():
        if key in selected_display:
            pg = val
            break

    if not is_pro:
        st.markdown("<div style='margin-top:auto;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-top: 10px; padding: 10px; background: #F8FAFC; border-radius: 8px; border: 1px dashed #CBD5E1; text-align: center;">
            <p style="font-size:0.75rem; margin-bottom:5px; color:#64748B;">Wil je dat we persoonlijk meekijken?</p>
            <a href="{STRATEGY_CALL_URL}" target="_blank" style="text-decoration:none; color: #2563EB; font-weight: 700; font-size: 0.85rem;">
                🚀 Word student en ontgrendel alle tools
            </a>
            <p style="font-size:0.7rem; margin-top:6px; color:#94A3B8;">
                Plan eerst een gratis call om te kijken naar jouw situatie
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- LOCK SCREEN COMPONENT ---
def render_pro_lock(title, desc):
    st.markdown(f"""
    <div class="lock-container">
        <div style="font-size: 40px; margin-bottom: 15px; opacity: 0.5;">🔒</div>
        <h3 style="margin-bottom: 10px; color: #1E293B;">{title}</h3>
        <p style="color: #64748B; font-size: 0.95rem; margin-bottom: 18px; max-width: 520px; margin-left: auto; margin-right: auto; line-height: 1.6;">
            {desc}
        </p>
        <div style="max-width:520px; margin:0 auto 20px auto; text-align:left; font-size:0.9rem; color:#0F172A;">
            <p style="margin:0 0 4px 0; font-weight:600;">Als student krijg je onder andere:</p>
            <ul style="margin:0 0 6px 18px; padding:0;">
                <li>Volledige toegang tot alle AI tools.</li>
                <li>Extra uitlegvideo's per fase.</li>
                <li>Persoonlijke hulp via community en calls.</li>
                <li>Tijdelijke unlocks zoals Spy tool verlopen niet.</li>
            </ul>
            <p style="margin:0; font-size:0.8rem; color:#64748B;">De meeste studenten zitten rond €75–€175 per maand afhankelijk van het niveau.</p>
        </div>
        <a href="{STRATEGY_CALL_URL}" target="_blank" style="text-decoration: none;">
            <div style="
                background: linear-gradient(135deg, #2563EB, #1D4ED8); 
                color: white; 
                padding: 12px 28px; 
                border-radius: 50px; 
                font-weight: 600; 
                font-size: 1rem; 
                display: inline-block;
                box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
                transition: transform 0.2s;
            ">
                📞 Plan gratis unlock call
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# --- CONTENT PAGES ---

if pg == "Dashboard":
    name = user.get('first_name') or user['email'].split('@')[0].capitalize()
    
    d_col1, d_col2 = st.columns([2, 1])
    
    with d_col1:
        st.markdown(f"""
        <div>
            <h1 style="margin:0; line-height:1.2;">{get_greeting()}, {name}</h1>
            <p style="margin:4px 0 0 0; color:#64748B; font-size:0.9rem;">
                Volg gewoon de volgende stap. Focus is key.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("▶️Start hier: Belangrijke update van Michael", expanded=False):
            st.markdown(f'<iframe width="100%" height="250" src="{COACH_VIDEO_URL.replace("watch?v=", "embed/")}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

    with d_col2:
        st.markdown(textwrap.dedent("""
        <div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.02);">
            <div style="font-size: 0.75rem; color: #64748B; font-weight: 700; text-transform: uppercase;">🎯 Jouw doel</div>
            <div style="font-size: 1.1rem; font-weight: 800; color: #0F172A; margin: 4px 0;">€10k Omzet</div>
            <div style="font-size: 0.8rem; color: #2563EB;">Nog 60 dagen te gaan</div>
        </div>
        """), unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    if "ticker_msg" not in st.session_state:
        st.session_state.ticker_msg = auth.get_real_activity()
    st.info(f"⚡ {st.session_state.ticker_msg}")

    current_title, next_xp_goal = auth.get_rank_info(user['xp'])
    xp_to_next = max(next_xp_goal - user['xp'], 0)
    next_reward_label = "Spy tool unlock" if user['level'] < 2 else "Video scripts unlock"

    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">Huidig level</div>
            <div class="metric-value">{user['level']}</div>
            <div class="metric-sub" style="color:#64748B;">{current_title}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Jouw XP</div>
            <div class="metric-value">{user['xp']}</div>
            <div class="metric-sub" style="color:#0EA5E9;">Nog {xp_to_next} XP tot volgende level</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Volgende beloning</div>
            <div class="metric-value">🎁</div>
            <div class="metric-sub" style="color:#2563EB;">{next_reward_label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_road, tab_leader = st.tabs(["📍 Mijn roadmap", "🏆 Toplijst"])

    with tab_road:
        completed_steps = auth.get_progress()
        full_map = roadmap.get_roadmap()
        
        next_step_title = "Alles afgerond! 🎉"
        next_step_phase = "Klaar"
        next_step_id = None
        found = False
        
        for fase_key, fase in full_map.items():
            for s in fase['steps']:
                if s['id'] not in completed_steps:
                    next_step_title = s['title']
                    next_step_phase = fase['title'].split(":")[0]
                    next_step_id = s['id']
                    found = True
                    break
            if found:
                break
            
        total_steps = sum(len(f['steps']) for f in full_map.values())
        done_count = len(completed_steps)
        pct = int(done_count/total_steps*100) if total_steps > 0 else 0

# --- FIX: Mission Card (Compactere versie) ---
        mission_html = f"""
<div style="background: linear-gradient(135deg, #2563EB 0%, #1E3A8A 100%); padding: 20px; border-radius: 16px; color: white; margin-bottom: 20px; box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.5); border: 1px solid #3B82F6; position: relative; overflow: hidden;">
    <div style="position: absolute; top: -15px; right: -15px; font-size: 140px; opacity: 0.1;">🚀</div>
    <div style="position: relative; z-index: 2;">
        <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.9; margin-bottom: 6px; font-weight: 700; color: #DBEAFE;">🎯 HUIDIGE MISSIE</div>
        <h2 style="margin: 0; font-size: 1.5rem; color: white; font-weight: 800; letter-spacing: -0.5px;">{next_step_title}</h2>
        <p style="margin: 6px 0 16px 0; font-size:0.95rem; opacity:0.95; max-width: 600px; line-height: 1.4;">
            Voltooi deze stap en verdien direct <strong style="color:#FCD34D">+50 XP</strong>.
        </p>
        <div style="margin-bottom: 16px;">
            <div style="display:flex; justify-content:space-between; font-size: 0.75rem; margin-bottom: 4px; opacity: 0.9;">
                <span>Voortgang roadmap</span>
                <span>{pct}%</span>
            </div>
            <div style="background: rgba(255,255,255,0.2); height: 6px; border-radius: 4px; overflow: hidden;">
                <div style="background: #10B981; width: {pct}%; height: 100%; box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);"></div>
            </div>
        </div>
        <a href="#mission" target="_self" style="text-decoration:none;">
            <div style="display: inline-block; background: linear-gradient(to bottom, #FBBF24, #F59E0B); color: #78350F; padding: 10px 24px; border-radius: 8px; font-weight: 800; font-size: 0.9rem; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.2); transition: transform 0.1s; border: 1px solid #D97706;">
                ▶ Start opdracht
            </div>
        </a>
    </div>
</div>
"""
        st.markdown(mission_html, unsafe_allow_html=True)
        
        for fase_key, fase in full_map.items():
            steps = fase['steps']
            fase_done = sum(1 for s in steps if s['id'] in completed_steps)
            fase_pct = fase_done / len(steps)
            
            if fase_pct < 1.0 or fase_key == list(full_map.keys())[-1]:
                st.markdown(f"#### {fase['title']}")
                st.caption(fase['desc'])
                
                for step in steps:
                    is_done = step['id'] in completed_steps
                    is_active = step['id'] == next_step_id
                    
                    if is_active:
                        st.markdown("<div id='mission'></div>", unsafe_allow_html=True)
                    
                    just_completed_id, xp = roadmap.render_step_card(step, is_done, is_pro, expanded=is_active)
                    if just_completed_id:
                        auth.mark_step_complete(just_completed_id, xp)
                        st.balloons()
                        st.rerun()
                st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    with tab_leader:
        leaders = auth.get_leaderboard_data()
        if not leaders:
            st.info("Nog geen data.")
        else:
            for p in leaders:
                is_me = p['name'].startswith(user.get('first_name') or '')
                bg = "#EFF6FF" if is_me else "white"
                border = "1px solid #3B82F6" if is_me else "1px solid #E2E8F0"
                
                st.markdown(textwrap.dedent(f"""
                <div style="background: {bg};
                            border:{border};
                            border-radius: 12px;
                            padding: 12px 14px;
                            display:flex;
                            align-items:center;
                            justify-content:space-between;
                            margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:26px; text-align:center; font-weight:700;">#{p['rank']}</div>
                        <div>
                            <div style="font-weight:600;">{p['name']}</div>
                            <div style="font-size:0.75rem; color:#64748B;">{p['title']}</div>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-weight:600;">{p['xp']} XP</div>
                        <div style="font-size:0.7rem; color:#22C55E;">{"Student" if p['is_pro'] else "Gratis"}</div>
                    </div>
                </div>
                """), unsafe_allow_html=True)

elif pg == "Gratis Mini Training":
    st.title("🎓 Gratis mini training")
    st.caption("Korte training om je eerste stappen als e-commerce starter snel helder te krijgen.")

    t1, t2 = st.columns(2)
    t3, t4 = st.columns(2)

    with t1:
        st.markdown("### 1. Mindset & realistische verwachtingen")
        with st.container(border=True):
            st.markdown('<iframe src="https://drive.google.com/file/d/1xyM_9q2i5FJBF__HvmhDrHTBueBoBstv/preview" width="100%" height="300" style="border-radius:8px; border:none;"></iframe>', unsafe_allow_html=True)
        st.info("Noteer na deze video in 3 bulletpoints waarom je deze webshop wilt. Dat helpt je bij tegenslag.")

    with t2:
        st.markdown("### 2. Hoe werkt een winstgevende webshop echt")
        with st.container(border=True):
            st.markdown('<iframe src="https://drive.google.com/file/d/1O4fa0FUA10MnCE4QqNNDe3XSLwLfkb_F/preview" width="100%" height="300" style="border-radius:8px; border:none;"></iframe>', unsafe_allow_html=True)
        st.info("Let extra op: verkeer, conversie en marge. Schrijf 1 actie op per blok.")

    with t3:
        st.markdown("### 3. Je eerste sale neerzetten")
        with st.container(border=True):
            st.markdown('<iframe src="https://drive.google.com/file/d/1xyM_9q2i5FJBF__HvmhDrHTBueBoBstv/preview" width="100%" height="300" style="border-radius:8px; border:none;"></iframe>', unsafe_allow_html=True)
        st.success("Na deze video kies je één product en één kanaal. Niet alles tegelijk.")

    with t4:
        st.markdown("### 4. Van 1 naar 100 sales")
        with st.container(border=True):
            st.markdown('<iframe src="https://drive.google.com/file/d/1O4fa0FUA10MnCE4QqNNDe3XSLwLfkb_F/preview" width="100%" height="300" style="border-radius:8px; border:none;"></iframe>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: #F0F9FF; padding: 25px; border-radius: 12px; border: 1px solid #BAE6FD; text-align: center;">
            <h4 style="color:#0369A1; margin-bottom:6px;">🚀 Klaar voor het echte werk?</h4>
            <p style="color:#0C4A6E; margin:0;">Je hebt de basis gezien. Wil je dat we meekijken zodat dit ook echt gaat draaien?</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("📞 Plan gratis strategie call", STRATEGY_CALL_URL, type="primary", use_container_width=True)

elif pg == "Logo Maker":
    st.title("🎨 Logo maker")
    
    if "logo_generations" not in st.session_state:
        st.session_state.logo_generations = 0
        
    has_access = is_pro or st.session_state.logo_generations < 3
    
    if not has_access:
        render_pro_lock(
            "Je gratis logo credits zijn op",
            "Je hebt 3 gratis logo's gemaakt. Word student om onbeperkt te genereren."
        )
    else:
        if not is_pro:
            credits_left = 3 - st.session_state.logo_generations
            st.info(f"🎁 Je hebt nog **{credits_left}** gratis logo generaties over.")
        else:
            st.caption("Genereer onbeperkt professionele logo's voor je webshop.")
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                brand_name = st.text_input("Bedrijfsnaam", placeholder="Bijv. Lumina")
                niche = st.text_input("Niche / industrie", placeholder="Bijv. Moderne verlichting")
            with col2:
                style = st.selectbox("Stijl", ["Minimalistisch", "Modern & strak", "Vintage / retro", "Luxe & elegant", "Speels & kleurrijk"])
                color = st.text_input("Voorkeurskleuren", placeholder="Bijv. Zwart en goud, of Pastelblauw")
            
            if st.button("✨ Genereer 3 logo concepten", type="primary", use_container_width=True):
                if not brand_name or not niche:
                    st.warning("Vul in ieder geval je bedrijfsnaam en niche in.")
                else:
                    st.session_state.logo_generations += 1
                    
                    with st.spinner("AI is aan het ontwerpen... dit duurt ongeveer 30 seconden voor 3 variaties."):
                        images = []
                        for i in range(3):
                            variation = ""
                            if i == 1: variation = "Make it slightly bolder."
                            if i == 2: variation = "Make it more elegant and thin."
                            
                            img_url = ai_coach.generate_logo(brand_name, niche, style + " " + variation, color)
                            if img_url: images.append(img_url)
                        
                        if images:
                            st.success("Logo's succesvol gegenereerd!")
                            cols = st.columns(3)
                            for idx, img in enumerate(images):
                                with cols[idx]:
                                    st.image(img, use_container_width=True)
                                    st.caption(f"Optie {idx+1}")
                            st.info("💡 Tip: Rechtsklik op de afbeelding om hem op te slaan.")
                        else:
                            st.error("Er ging iets mis bij het genereren. Probeer het opnieuw.")

elif pg == "Product Finder":
    st.title("🔍 Product ideeën voor jouw webshop")

    st.caption("Gebruik de AI voor inspiratie, maar gebruik altijd je eigen gezonde verstand (en de checklist hieronder) voordat je inkoopt.")

    if not is_pro:
        render_pro_lock(
            "Ontgrendel echte winnende producten",
            "Als student krijg je toegang tot de Product Inspirator, zoektools en de uitgebreide validator checklist."
        )
    else:
        with st.container(border=True):
            col_inp, col_btn = st.columns([3, 1])
            niche = col_inp.text_input("In welke niche zoek je een product?", "Gadgets")
            search_clicked = col_btn.button("🔎 Zoek ideeën", type="primary", use_container_width=True)

        if search_clicked and niche:
            results = ai_coach.find_real_winning_products(niche, "Viral")
            
            st.markdown(f"**Resultaten voor '{niche}':**")
            
            if not results:
                st.warning("De AI is even inspiratieloos. Probeer een andere niche.")
            else:
                for p in results:
                    title = p.get("title") or p.get("original_title") or "Naamloos product"
                    price = p.get("price", 29.95)
                    hook = p.get("hook", "")
                    search_links = p.get("search_links", {}) 

                    with st.container(border=True):
                        st.markdown(f"### {title}")
                        st.caption(f"Richtprijs verkoop: €{price}")
                        st.write(f"💡 **Waarom viral:** {hook}")
                        
                        if search_links:
                            c_tik, c_ali = st.columns(2)
                            c_tik.link_button("📱 Check op TikTok", search_links['tiktok'], use_container_width=True)
                            c_ali.link_button("📦 Check op AliExpress", search_links['ali'], use_container_width=True)
                        else:
                            df = pd.DataFrame([{"Title": title, "Price": price}])
                            csv = df.to_csv(index=False).encode('utf-8')
                            st.download_button("⬇️ Download CSV", csv, "product.csv", "text/csv", use_container_width=True)

        st.markdown("---")

        st.header("👮‍♀️ Product Validator")
        st.markdown("Heb je een idee gevonden (hierboven of ergens anders)? **Doe de check.** Wees streng, anders kost het je geld.")

        with st.container(border=True):
            c1 = st.checkbox("🤔 **Probleem/Wow:** Lost het een pijnlijk probleem op OF is het echt heel cool om te zien?")
            c2 = st.checkbox("🏪 **Niet lokaal:** Kun je dit NIET bij de Action, Kruidvat of HEMA kopen?")
            c3 = st.checkbox("💰 **Marge:** Kan ik het verkopen voor minimaal €25? (Anders maak je geen winst met ads)")
            c4 = st.checkbox("🎥 **Content:** Kan ik hier makkelijk zelf video's over maken met mijn telefoon?")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if c1 and c2 and c3 and c4:
                st.success("🏆 **GROEN LICHT!** Dit product heeft potentie. Ga naar de 'Winst Calculator' om je marges definitief te berekenen.")
                st.balloons()
            elif c1 or c2 or c3 or c4:
                st.warning("⚠️ **Twijfelgeval.** Je mist een paar cruciale punten. Zoek liever nog even verder naar een 'winner'.")
            else:
                st.info("Vink de boxjes aan om je product te keuren.")

elif pg == "Winst Calculator":
    st.title("🧮 Rijkrekenaar")
    st.caption("Veel starters gaan nat omdat ze hun marges niet kennen. Reken hier uit of je product winstgevend is.")

    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            verkoop_prijs = st.number_input("Verkoopprijs (wat de klant betaalt)", value=29.95, step=1.00)
            inkoop_prijs = st.number_input("Inkoop + Verzenden (AliExpress/Agent)", value=12.00, step=0.50)
        with c2:
            adv_kosten = st.number_input("Geschatte Ads kosten per sale (CPA)", value=10.00, step=1.00, help="Gemiddeld kost het 10-15 euro aan ads om 1 klant te vinden.")
            transactie_kosten = verkoop_prijs * 0.03 # 3% voor iDeal/Shopify payments

    # Berekeningen
    kosten_totaal = inkoop_prijs + adv_kosten + transactie_kosten
    winst = verkoop_prijs - kosten_totaal
    marge_pct = (winst / verkoop_prijs) * 100 if verkoop_prijs > 0 else 0
    break_even_roas = verkoop_prijs / (verkoop_prijs - inkoop_prijs) if (verkoop_prijs - inkoop_prijs) > 0 else 0

    st.markdown("---")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.metric("Netto Winst per sale", f"€{winst:.2f}", delta=f"{winst:.2f}", delta_color="normal" if winst > 0 else "inverse")
    with col_res2:
        st.metric("Winstmarge", f"{marge_pct:.1f}%")
    with col_res3:
        st.metric("Break-Even ROAS", f"{break_even_roas:.2f}", help="Je advertentie moet minimaal zoveel x geld opleveren om quitte te spelen.")

    if winst < 5:
        st.error("⚠️ Pas op! Je winst is erg laag (minder dan €5). Eén retourzending en je maakt verlies. Probeer je prijs te verhogen of goedkoper in te kopen.")
    elif winst > 10:
        st.balloons()
        st.success("✅ Dit ziet eruit als een gezond product!")

elif pg == "Spy Tool":
    st.title("📊 Concurrenten analyseren")

    has_access = is_pro
    if not has_access and user.get('spy_unlock_until'):
        try:
            if datetime.fromisoformat(user['spy_unlock_until']) > datetime.now(timezone.utc):
                has_access = True
        except Exception:
            has_access = has_access

    if has_access:
        if not is_pro:
            st.info("🕒 Tijdelijke toegang actief (24u).")
            
        with st.container(border=True):
            st.markdown("#### 🕵️‍♀️ Store Hunter")
            st.caption("Vul de URL in. Wij sorteren automatisch op hun **Best Verkopende** producten.")
            url = st.text_input("URL van concurrent", placeholder="https://sharkslides.com")
            
            if url and st.button("🚀 Scan bestsellers", type="primary", use_container_width=True):
                with st.spinner("Achterdeurtje zoeken en bestsellers ophalen..."):
                    products = competitor_spy.scrape_shopify_store(url)
                    
                    if products:
                        st.success(f"BINGO! {len(products)} Producten gevonden. Gesorteerd op populariteit.")
                        
                        for p in products:
                            with st.container(border=True):
                                c1, c2, c3 = st.columns([1, 2, 1])
                                
                                with c1:
                                    if p['image_url']:
                                        st.image(p['image_url'], use_container_width=True)
                                        if p['rank'] == 1:
                                            st.caption("🔥 #1 BESTSELLER")
                                    else:
                                        st.write("🖼️")
                                
                                with c2:
                                    st.markdown(f"**{p['title']}**")
                                    st.caption(f"Prijs: €{p['price']} | Online sinds: {p['published_at']}")
                                    st.markdown(f"[Bekijk op hun site]({p['original_url']})")
                                    
                                    if "2024" in p['published_at'] or "2025" in p['published_at']:
                                        st.markdown(":new: *Dit is een recent product!*")
                                
                                with c3:
                                    if st.button("📥 Importeer", key=f"imp_{p['handle']}", type="primary", use_container_width=True):
                                        my_shop = st.session_state.get("sh_url")
                                        my_token = st.session_state.get("sh_token")
                                        
                                        if my_shop and my_token:
                                            with st.spinner("Kopiëren naar jouw shop..."):
                                                res = shopify_client.push_product_to_shopify(my_shop, my_token, p)
                                                if res['success']:
                                                    st.toast("✅ Geïmporteerd! Check je Shopify admin.", icon="✅")
                                                else:
                                                    st.error(res['msg'])
                                        else:
                                            st.warning("⚠️ Koppel eerst je eigen Shopify store bij 'Instellingen'!")
                    else:
                        st.error("Kon geen producten vinden. Deze shop heeft hun beveiliging goed dichtgetimmerd.")
                        
    else:
        render_pro_lock("Concurrenten professioneel analyseren", "Zie de bestsellers van andere shops en importeer ze direct.")

elif pg == "Video Scripts":
    st.title("🎬 Video ideeën en scripts")

    has_access = is_pro
    if not has_access and user.get('scripts_unlock_until'):
        try:
            if datetime.fromisoformat(user['scripts_unlock_until']) > datetime.now(timezone.utc):
                has_access = True
        except Exception:
            has_access = has_access
        
    if has_access:
        with st.container(border=True):
            prod = st.text_input("Product of aanbod", placeholder="Bijvoorbeeld: Dames sandalen met zachte zool")
            if st.button("✨ Genereer video ideeën", type="primary", use_container_width=True) and prod:
                res = ai_coach.generate_viral_scripts(prod, "", "Viral")
                
                st.markdown("### 🔥 3 korte hooks voor je video")
                for h in res['hooks']:
                    st.info(h)
                
                with st.expander("📜 Volledig script voor 1 video"):
                    st.text_area("Script", res['full_script'], height=300)
                    
                with st.expander("✉️ Briefing tekst voor creators / UGC makers"):
                    st.code(res['creator_brief'], language="text")
                st.caption("Tip: kies één hook en neem die 5–10 keer op. De beste variant gebruik je in je advertentie.")
    else:
        render_pro_lock("Viral video scripts generator", "Laat AI complete TikTok en Reels scripts voor je product schrijven, inclusief briefing tekst.")

elif pg == "Ads Doctor":
    st.title("🩺 Ads check")

    if is_pro:
        with st.container(border=True):
            st.info("Upload een screenshot van je Facebook of TikTok Ads Manager en beschrijf kort wat er nu misgaat.")
            upload = st.file_uploader("Bestand kiezen", type=['png', 'jpg'])
            notities = st.text_area("Wat wil je verbeteren?", placeholder="Voorbeeld: hoge CPM, weinig kliks, veel add-to-cart maar weinig aankopen...")
            if st.button("Diagnose starten", type="primary", use_container_width=True):
                if not upload or not notities:
                    st.warning("Upload een screenshot en vul je vraag in.")
                else:
                    st.success("In de student omgeving koppelen we hier AI analyse en concrete advertentie acties aan.")
                    st.caption("Nu kun je dit screenshot alvast bewaren zodat je het makkelijk terugvindt.")
    else:
        render_pro_lock("Ads check", "Laat je advertenties beoordelen en krijg concrete verbeterpunten per campagne.")

elif pg == "Instellingen":
    st.title("⚙️ Instellingen")
    
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Profiel", "💰 Partner", "🔗 Koppelingen", "🆘 Hulp"])
    
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
                        <p style="margin:0; font-size:0.8rem; color:#64748B;">Status: {'Student 🎓' if is_pro else 'Gast 👤'}</p>
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
            st.caption("Deel deze code met mensen die willen starten. Zij krijgen een voordeel en jij ontvangt commissie per student die via jouw code instapt. Het exacte bedrag zie je hierboven bij 'Geschat verdiend'.")
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
            st.link_button("💬 Discord community", COMMUNITY_URL, use_container_width=True)
            st.link_button("📧 Email support", "mailto:support@rmecom.nl", use_container_width=True)
        
        with st.expander("Veelgestelde vragen"):
            st.write("**Hoe werkt de XP?**")
            st.caption("Je krijgt XP voor elke afgeronde stap in de roadmap. XP ontgrendelt tijdelijke en vaste tools.")
            st.write("**Wanneer wordt commissie uitbetaald?**")
            st.caption("Uitbetalingen gebeuren maandelijks zodra je saldo boven de afgesproken drempel ligt.")