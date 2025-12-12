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

st.set_page_config(
    page_title="RM Ecom App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. PREMIUM CSS ENGINE ---
st.markdown("""
    <style>
        /* [GLOBAL VARIABLES] */
        :root {
            --primary: #2563EB;
            --bg-light: #F8FAFC;
            --text-dark: #0F172A;
            --text-gray: #64748B;
            --white: #FFFFFF;
            --border: #E2E8F0;
        }

        /* [APP BACKGROUND] */
        .stApp {
            background-color: var(--bg-light);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-dark);
        }
        
        /* [HEADER WEG] */
        [data-testid="stHeader"] {background: transparent;}
        [data-testid="stDecoration"] {display: none;}
        [data-testid="stSidebarCollapseButton"] { display: block !important; color: var(--text-dark); }
        
        /* [SIDEBAR - CLEAN] */
        section[data-testid="stSidebar"] {
            background-color: var(--white);
            border-right: 1px solid var(--border);
        }
        section[data-testid="stSidebar"] .block-container {
            padding: 1.5rem 1rem !important;
        }
        
        /* [NAVIGATIE MENU] */
        div[role="radiogroup"] {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        div[role="radiogroup"] > label > div:first-child {
            display: None;
        }
        div[role="radiogroup"] label {
            width: 100%;
            padding: 10px 14px;
            border-radius: 10px;
            border: 1px solid transparent;
            background-color: transparent;
            color: var(--text-gray);
            font-weight: 500;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        div[role="radiogroup"] label:hover {
            background-color: #F1F5F9;
            color: var(--text-dark);
        }
        
        div[role="radiogroup"] label[data-checked="true"] {
            background-color: #EFF6FF !important;
            color: #2563EB !important;
            font-weight: 600;
            border: 1px solid #DBEAFE;
            box-shadow: 0 1px 2px rgba(37, 99, 235, 0.05);
        }

        /* [MAIN CONTENT] */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 5rem;
            max-width: 1100px;
        }

        /* [CARDS] */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 16px;
            background: var(--white);
            border: 1px solid var(--border);
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            padding: 24px;
            margin-bottom: 20px;
        }
        
        /* [BUTTONS] */
        .stButton button {
            border-radius: 10px !important;
            font-weight: 600;
            border: none;
            padding: 0.6rem 1.2rem;
            transition: transform 0.1s;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .stButton button:hover {
            transform: translateY(-1px);
        }
        .stButton button[kind="primary"] {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
        }

        /* [METRICS GRID] */
        .metric-container {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 15px;
            margin-bottom: 25px;
        }
        .metric-card {
            background: var(--white);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.01);
        }
        .metric-label { font-size: 0.7rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
        .metric-value { font-size: 1.6rem; font-weight: 800; color: var(--text-dark); }
        .metric-sub { font-size: 0.75rem; color: #10B981; font-weight: 600; margin-top: 2px; }

        /* [LOCK SCREEN] */
        .lock-container {
            text-align: center;
            padding: 60px 20px;
            background: white;
            border-radius: 16px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.02);
        }

        /* [FAB] */
        .fab-container {
            position: fixed; bottom: 30px; right: 30px; z-index: 9999;
        }
        .fab-button {
            background: linear-gradient(135deg, #2563EB, #1D4ED8);
            color: white; width: 60px; height: 60px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 24px; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
            cursor: pointer; text-decoration: none; transition: transform 0.2s;
        }
        .fab-button:hover { transform: scale(1.1); }

        /* Responsive Mobile */
        @media (max-width: 600px) {
            .metric-container { grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
            .metric-card { padding: 10px; }
            .metric-value { font-size: 1.2rem; }
            .metric-label { font-size: 0.6rem; }
            h1 { font-size: 1.6rem !important; }
            .fab-container { bottom: 20px; right: 20px; }
        }

/* --- 10/10 OPTIMALISATIE CSS --- */

/* Verberg de lelijke link-ketting naast titels */
.stMarkdown h1 a {
    display: none !important;
    pointer-events: none;
}

/* Mobiele optimalisatie voor de H1 Titel */
@media (max-width: 600px) {
    h1 span {
        font-size: 1.8rem !important; /* Kleiner op mobiel */
    }
    p {
        font-size: 0.95rem !important;
    }
    /* Minder witruimte aan de zijkanten op mobiel */
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
}

/* Verberg de standaard Streamlit Header (Deploy knop etc voor bezoekers) */
header[data-testid="stHeader"] {
    display: none !important;
}

/* Logo styling */
.logo-text {
    font-weight: 800;
    font-size: 1.2rem;
    color: #0F172A;
    letter-spacing: -0.5px;
    margin-bottom: 0px;
}

/* [INPUT FIELDS - MODERN LOOK] */
/* Maak invoervelden wit met een randje ipv grijs */
.stTextInput input {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    color: #0F172A !important;
    border-radius: 8px !important;
}
.stTextInput input:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 2px rgba(37,99,235,0.2) !important;
}

/* [EXPANDER CLEANUP] */
/* Maak de expander (invite code) iets rustiger */
.streamlit-expanderHeader {
    background-color: transparent !important;
    font-size: 0.9rem !important;
    color: #64748B !important;
}

/* [MOBIELE OPTIMALISATIES] */
@media (max-width: 600px) {
    /* Titel iets compacter op mobiel */
    h1 { font-size: 2rem !important; }
    h1 span { font-size: 2rem !important; }
    
    /* Zorg dat de features (rechts) niet te ver wegvallen */
    .block-container { padding-bottom: 2rem !important; }
}

        /* [GLOBAL VARIABLES] */
        :root {
            --primary: #2563EB;
            --bg-light: #F8FAFC;
            --text-dark: #0F172A;
            --text-gray: #64748B;
            --white: #FFFFFF;
            --border: #E2E8F0;
        }

        /* [APP BACKGROUND] */
        .stApp {
            background-color: var(--bg-light);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-dark);
        }
        
        /* [LAYOUT OPTIMALISATIE - MINDER WITRUIMTE] */
        .block-container {
            padding-top: 2rem !important;     /* Was veel groter */
            padding-bottom: 3rem !important;
            max-width: 1000px;                /* Iets smaller voor betere leesbaarheid */
        }
        
        /* [HEADER WEG] */
        [data-testid="stHeader"] {display: none;}
        [data-testid="stDecoration"] {display: none;}
        
        /* [TITEL AANPASSING] */
        h1 {
            font-size: 2.2rem !important;     /* Iets kleiner en eleganter */
            font-weight: 800 !important;
            letter-spacing: -1px !important;
        }
        
        /* [INPUT FIELDS - MODERN WIT] */
        .stTextInput input {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #0F172A !important;
            border-radius: 8px !important;
            padding: 10px 12px !important;
        }
        .stTextInput input:focus {
            border-color: #2563EB !important;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
        }

        /* [BUTTONS] */
        .stButton button {
            border-radius: 8px !important;
            font-weight: 600;
            border: none;
            padding: 0.7rem 1.2rem;
            transition: transform 0.1s;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
        }
        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 8px -1px rgba(37, 99, 235, 0.3);
        }

        /* [LOGO TEXT] */
        .logo-text {
            font-weight: 800;
            font-size: 1.1rem;
            color: #0F172A;
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 15px; /* Minder afstand tot titel */
        }

        /* [MOBIELE AANPASSINGEN] */
        @media (max-width: 600px) {
            .block-container { padding-top: 1rem !important; }
            h1 { font-size: 1.8rem !important; line-height: 1.2 !important; }
            .logo-text { margin-bottom: 10px; }
        }

    </style>
""", unsafe_allow_html=True)

# --- 2. COOKIE MANAGER (AUTO LOGIN) ---
cookie_manager = stx.CookieManager()

if "user" not in st.session_state:
    cookie_email = cookie_manager.get("rmecom_user_email")
    if cookie_email:
        try:
            auth.login_or_register(cookie_email)
        except:
            pass

# ... (Bestaande imports en CSS)

# --- 3. LOGIN SCHERM (FINAL TWEAKS) ---
if "user" not in st.session_state:
    if "status" in st.query_params:
        st.query_params.clear()

    col_left, col_right = st.columns([1, 1.1], gap="large", vertical_alignment="center")

    with col_left:
        # Logo
        st.markdown("<div class='logo-text'>⚡ RM Ecom Academy</div>", unsafe_allow_html=True)
        
        # Header
        st.markdown("""
        <h1 style='margin-bottom: 12px; line-height: 1.15; color: #0F172A;'>
            Van 0 naar <span style='color:#2563EB'>€15k/maand</span> met je eigen webshop.
        </h1>
        <p style='color:#64748B; font-size:1.05rem; margin-bottom: 30px; line-height: 1.6;'>
            De enige app die je stap-voor-stap begeleidt. Geen technische kennis nodig. Start vandaag <b>gratis</b>.
        </p>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            tab_free, tab_pro = st.tabs(["🚀 Start Challenge", "💎 Student Login"])

            with tab_free:
                email = st.text_input("Email", placeholder="jouw@email.com", label_visibility="collapsed", key="login_email_free")
                
                # De expander is prima zo: subtiel maar beschikbaar
                with st.expander("Heb je een Vrienden-code? (Optioneel)"):
                    ref_code = st.text_input("Vrienden Code", placeholder="bv. JAN-482", key="ref_code_input")
                
                # Witruimte boven de knop iets kleiner gemaakt (van 8px naar 5px)
                st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
                
                if st.button("🚀 Start Direct (Gratis)", type="primary", use_container_width=True):
                    if email and "@" in email:
                        with st.spinner("Account aanmaken..."):
                            auth.login_or_register(email, ref_code_input=ref_code if 'ref_code' in locals() and ref_code else None)
                            cookie_manager.set("rmecom_user_email", email, expires_at=datetime.now() + timedelta(days=30))
                            st.rerun()
                    else:
                        st.warning("Vul een geldig e-mailadres in.")
                
                # AANGEPAST: Dichter op de knop en strakker uitgelijnd
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
                
                # NIEUW: Extra witregel aan de onderkant zoals gevraagd
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            with tab_pro:
                st.markdown("<small style='color:#64748b'>Welkom terug, topper.</small>", unsafe_allow_html=True)
                pro_email = st.text_input("Jouw Email", key="log_mail")
                lic_key = st.text_input("Licentie Code", type="password", placeholder="PRO-XXXX-XXXX")
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("💎 Inloggen", type="secondary", use_container_width=True):
                    if pro_email and lic_key:
                        auth.login_or_register(pro_email, license_input=lic_key)
                        cookie_manager.set("rmecom_user_email", pro_email, expires_at=datetime.now() + timedelta(days=30))
                        st.rerun()
                    else:
                        st.warning("Vul al je gegevens in.")

    with col_right:
        st.markdown("<br class='desktop-only'>", unsafe_allow_html=True)
        # Rechterkant blijft ongewijzigd (was al goed)
        raw_html = """
        <div style="background: white; padding: 30px; border-radius: 20px; border: 1px solid #E2E8F0; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.08); color: #0F172A;">
            <h3 style="margin-top:0; color:#0F172A; font-size:1.15rem; font-weight: 700;">Dit krijg je gratis:</h3>
            <div style="display:flex; gap:16px; margin-bottom:24px; align-items:center;">
                <div style="width:48px; height:48px; background:#EFF6FF; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0;">🗺️</div>
                <div>
                    <h4 style="margin:0; font-size:0.95rem; font-weight:600; color:#0F172A;">De 'Van 0 naar Sales' Roadmap</h4>
                    <p style="margin:2px 0 0 0; font-size:0.9rem; color:#64748B; line-height:1.4;">Precies weten wat je vandaag moet doen.</p>
                </div>
            </div>
            <div style="display:flex; gap:16px; margin-bottom:24px; align-items:center;">
                <div style="width:48px; height:48px; background:#F0FDF4; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0;">🤖</div>
                <div>
                    <h4 style="margin:0; font-size:0.95rem; font-weight:600; color:#0F172A;">Jouw eigen AI Coach</h4>
                    <p style="margin:2px 0 0 0; font-size:0.9rem; color:#64748B; line-height:1.4;">Laat AI je teksten en scripts schrijven.</p>
                </div>
            </div>
            <div style="display:flex; gap:16px; align-items:center;">
                <div style="width:48px; height:48px; background:#FFF7ED; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0;">🏆</div>
                <div>
                    <h4 style="margin:0; font-size:0.95rem; font-weight:600; color:#0F172A;">Gamified Groei</h4>
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
    if hour < 12:
        return "Goedemorgen"
    elif hour < 18:
        return "Goedemiddag"
    else:
        return "Goedenavond"

# --- SIDEBAR ---
with st.sidebar:
    rank_title, next_xp_goal_sidebar = auth.get_rank_info(user['xp'])

    st.markdown(f"""
    <div style="margin-bottom: 5px; padding-left: 2px;">
        <h3 style="margin:0; font-size:1rem; color:#0F172A;">👋 {user['email'].split('@')[0].title()}</h3>
        <p style="margin:0; font-size: 0.75rem; color: #64748B;">{rank_title}</p>
    </div>
    """, unsafe_allow_html=True)

    prev_threshold = 0
    for t in [0, 200, 500, 1000]:
        if user['xp'] >= t:
            prev_threshold = t
    xp_pct = min((user['xp'] - prev_threshold) / (next_xp_goal_sidebar - prev_threshold), 1.0) if next_xp_goal_sidebar > prev_threshold else 1.0
    st.progress(xp_pct)
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    # AANGEPASTE MENU LABELS VOOR BEGINNERS
    menu_options = {
        "🏠 Dashboard": "Dashboard",
        "🎓 Gratis training": "Gratis Mini Training",
        "🔍 Product ideeën": "Product Finder",
        "📊 Concurrenten": "Spy Tool",
        "🎬 Video ideeën": "Video Scripts",
        "🩺 Ads check": "Ads Doctor",
        "⚙️ Instellingen": "Instellingen"
    }
    
    display_options = []
    for icon_name, page_name in menu_options.items():
        if not is_pro and page_name in ["Product Finder", "Spy Tool", "Video Scripts", "Ads Doctor"]:
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
                🚀 Word Student en ontgrendel alle tools
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
            <p style="margin:0 0 4px 0; font-weight:600;">Als Student krijg je onder andere:</p>
            <ul style="margin:0 0 6px 18px; padding:0;">
                <li>Volledige toegang tot alle AI tools.</li>
                <li>Extra uitlegvideo's per fase.</li>
                <li>Persoonlijke hulp via community en calls.</li>
                <li>Tijdelijke unlocks zoals Spy Tool verlopen niet.</li>
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
                📞 Plan Gratis Unlock Call
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# --- CONTENT PAGES ---

if pg == "Dashboard":
    name = user['email'].split('@')[0].capitalize()
    
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:end; margin-bottom: 20px;">
        <div>
            <h1 style="margin:0; line-height:1.2;">{get_greeting()}, {name}</h1>
            <p style="margin:4px 0 0 0; color:#64748B; font-size:0.9rem;">
                Volg gewoon de volgende stap. Niet alles tegelijk hoeven te snappen is precies de bedoeling.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "ticker_msg" not in st.session_state:
        st.session_state.ticker_msg = auth.get_real_activity()
    st.info(f"⚡ {st.session_state.ticker_msg}")

    current_title, next_xp_goal = auth.get_rank_info(user['xp'])
    xp_to_next = max(next_xp_goal - user['xp'], 0)
    next_reward_label = "Spy Tool unlock" if user['level'] < 2 else "Video Scripts unlock"

    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">HUIDIG LEVEL</div>
            <div class="metric-value">{user['level']}</div>
            <div class="metric-sub" style="color:#64748B;">{current_title}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">JOUW XP</div>
            <div class="metric-value">{user['xp']}</div>
            <div class="metric-sub" style="color:#0EA5E9;">Nog {xp_to_next} XP tot volgende rang</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">VOLGENDE BELONING</div>
            <div class="metric-value">🎁</div>
            <div class="metric-sub" style="color:#2563EB;">{next_reward_label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_road, tab_leader = st.tabs(["📍 Mijn Roadmap", "🏆 Toplijst"])

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

        st.markdown(f"""
<div style="background: linear-gradient(120deg, #2563EB, #1E40AF); padding: 24px; border-radius: 16px; color: white; margin-bottom: 25px; box-shadow: 0 8px 20px -5px rgba(37, 99, 235, 0.4);">
    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; margin-bottom: 8px;">🚀 Huidige Missie</div>
    <h2 style="margin: 0; font-size: 1.4rem; color: white; font-weight: 700;">{next_step_title}</h2>
    <p style="margin: 6px 0 14px 0; font-size:0.85rem; opacity:0.9;">
        Voltooi de volgende stap. Daarna bepalen we samen wat logisch is om hierna te doen.
    </p>
    <div style="margin-top: 10px; background: rgba(255,255,255,0.2); height: 6px; border-radius: 4px; overflow: hidden;">
        <div style="background: white; width: {pct}%; height: 100%;"></div>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
        <span style="font-size: 0.85rem; opacity: 0.9;">{done_count}/{total_steps} stappen afgerond</span>
        <a href="#mission" target="_self" style="text-decoration:none;">
            <div style="background: white; color: #2563EB; padding: 8px 16px; border-radius: 8px; font-weight: bold; font-size: 0.85rem; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                ▶ Start opdracht
            </div>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)
        
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
                is_me = p['name'].startswith(user['email'].split('@')[0].capitalize())
                bg = "#EFF6FF" if is_me else "white"
                border = "1px solid #3B82F6" if is_me else "1px solid #E2E8F0"
                
                st.markdown(f"""
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
                """, unsafe_allow_html=True)

elif pg == "Gratis Mini Training":
    st.title("🎓 Gratis Mini Training")
    st.caption("Korte training om je eerste stappen als e-commerce starter snel helder te krijgen.")

    t1, t2 = st.columns(2)
    t3, t4 = st.columns(2)

    with t1:
        st.markdown("### 1. Mindset & Realistische Verwachtingen")
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
        st.link_button("📞 Plan Gratis Strategie Call", STRATEGY_CALL_URL, type="primary", use_container_width=True)

elif pg == "Product Finder":
    st.title("🔍 Product ideeën voor jouw webshop")

    st.caption("Let op: op dit moment werkt deze tool met voorbeelddata. Je krijgt dus vooral inspiratie en structuur. Voor echte, actuele data en begeleiding is Student nodig.")

    if not is_pro:
        render_pro_lock(
            "Ontgrendel echte winnende producten",
            "Als Student krijg je toegang tot een uitgebreidere product finder, inclusief marges, positionering en vervolgstappen in de roadmap."
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
                st.warning("Geen resultaten gevonden. Probeer een andere niche of iets algemeners.")
            else:
                for p in results:
                    title = p.get("title") or p.get("original_title") or "Naamloos product"
                    price = p.get("price", 0)
                    image_url = p.get("image_url")
                    hook = p.get("hook", "")

                    with st.container(border=True):
                        c1, c2 = st.columns([1, 2])
                        with c1:
                            if image_url:
                                st.image(image_url, use_column_width=True)
                            else:
                                st.write("Geen afbeelding beschikbaar.")
                        with c2:
                            st.markdown(f"### {title}")
                            st.caption(f"Suggestie verkoopprijs: €{price}")
                            if hook:
                                st.write(hook)
                            
                            df = pd.DataFrame([{"Title": title, "Price": price}])
                            csv = df.to_csv(index=False).encode('utf-8')
                            st.download_button("⬇️ Download als CSV voor Shopify", csv, "product.csv", "text/csv", use_container_width=True)

                st.info("Slimme volgorde: kies maximaal 1–2 ideeën uit deze lijst en werk ze uit in de winstcalculator in de roadmap.")

elif pg == "Spy Tool":
    st.title("📊 Concurrenten analyseren")

    # LOGIC: Temp Access
    has_access = is_pro
    if not has_access and user.get('spy_unlock_until'):
        try:
            if datetime.fromisoformat(user['spy_unlock_until']) > datetime.now(timezone.utc):
                has_access = True
        except Exception:
            has_access = has_access

    if has_access:
        if not is_pro:
            st.info("🕒 Tijdelijke toegang actief (24u). Word Student om deze tool blijvend te gebruiken.")
        with st.container(border=True):
            url = st.text_input("Shopify URL van de concurrent", placeholder="https://concurrent.nl")
            if url and st.button("🚀 Analyseer shop", type="primary", use_container_width=True):
                progress_text = "Verbinding maken..."
                bar = st.progress(0, text=progress_text)
                steps = ["Sitemap scannen...", "Producten ophalen...", "Traffic indicaties berekenen...", "Omzet inschatten...", "Klaar!"]
                for i, txt in enumerate(steps):
                    time.sleep(0.5)
                    bar.progress((i+1)*20, text=txt)
                bar.empty()
                st.success("Analyse voorbeeld is klaar. In de Student omgeving koppelen we hier echte data en next steps aan.")

                c1, c2 = st.columns(2)
                c1.metric("Geschatte Omzet (voorbeeld)", "€12.450", "+12%")
                c2.metric("Bestseller (voorbeeld)", "Galaxy Lamp")
                st.caption("Dit is een demo weergave. In het Student programma laten we je zien hoe je hier echte acties aan koppelt.")
    else:
        render_pro_lock("Concurrenten professioneel analyseren", "Zie omzet, bestsellers en positionering van andere shops zodat je niet in het donker bouwt.")

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
        render_pro_lock("Viral Video Scripts Generator", "Laat AI complete TikTok en Reels scripts voor je product schrijven, inclusief briefing tekst.")

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
                    st.success("In de Student omgeving koppelen we hier AI analyse en concrete advertentie acties aan.")
                    st.caption("Nu kun je dit screenshot alvast bewaren zodat je het makkelijk terugvindt.")
    else:
        render_pro_lock("Ads check", "Laat je advertenties beoordelen en krijg concrete verbeterpunten per campagne.")

elif pg == "Instellingen":
    st.title("⚙️ Instellingen")
    
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Profiel", "💰 Partner", "🔗 Koppelingen", "🆘 Hulp"])
    
    with tab1:
        with st.container(border=True):
            letter = user['email'][0].upper()
            st.markdown(f"""
                <div style="display:flex; align-items:center; gap:20px; margin-bottom:20px;">
                    <div style="width:60px; height:60px; background:#EFF6FF; border-radius:50%; display:flex; justify-content:center; align-items:center; font-size:24px; color:#2563EB; font-weight:bold; border:2px solid #2563EB;">
                        {letter}
                    </div>
                    <div>
                        <h3 style="margin:0;">{user['email']}</h3>
                        <p style="margin:0; color:#64748B;">Status: {'Student 🎓' if is_pro else 'Gast 👤'}</p>
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
            st.caption("Deel deze code met mensen die willen starten. Zij krijgen een voordeel en jij ontvangt commissie per Student die via jouw code instapt. Het exacte bedrag zie je hierboven bij 'Geschat verdiend'.")
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
            st.link_button("💬 Discord Community", COMMUNITY_URL, use_container_width=True)
            st.link_button("📧 Email Support", "mailto:support@rmecom.nl", use_container_width=True)
        
        with st.expander("Veelgestelde vragen"):
            st.write("**Hoe werkt de XP?**")
            st.caption("Je krijgt XP voor elke afgeronde stap in de roadmap. XP ontgrendelt tijdelijke en vaste tools.")
            st.write("**Wanneer wordt commissie uitbetaald?**")
            st.caption("Uitbetalingen gebeuren maandelijks zodra je saldo boven de afgesproken drempel ligt.")
