import streamlit as st
import time
import urllib.parse
import random
import pandas as pd
from datetime import datetime, timedelta
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

# --- 1. PREMIUM CSS ENGINE (10/10 STYLE) ---
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
    </style>
""", unsafe_allow_html=True)

# --- 2. COOKIE MANAGER (AUTO LOGIN) ---
cookie_manager = stx.CookieManager()

if "user" not in st.session_state:
    cookie_email = cookie_manager.get("rmecom_user_email")
    if cookie_email:
        try: auth.login_or_register(cookie_email) 
        except: pass

# --- 3. LOGIN SCHERM ---
if "user" not in st.session_state:
    if "status" in st.query_params: st.query_params.clear()

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        st.markdown("# RM Academy") 
        st.markdown("""
        <h3 style='margin-bottom: 10px; font-weight: 600; color: #1E293B;'>Start je webshop.</h3>
        <p style='color: #64748B; font-size: 1.1rem; margin-bottom: 30px; line-height: 1.6;'>
        Geen gedoe. Gewoon een helder stappenplan van A tot Z. 
        Start direct met het <b>gratis stappenplan</b>.
        </p>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            tab_free, tab_pro = st.tabs(["🚀 Nieuw Account", "💎 Studenten inloggen"])

            with tab_free:
                st.markdown("<small style='color:#64748b'>Geen creditcard nodig. Direct toegang.</small>", unsafe_allow_html=True)
                email = st.text_input("Vul hier je e-mailadres in:", placeholder="naam@voorbeeld.nl")
                with st.expander("Heb je een vrienden-code? (Optioneel)"):
                    ref_code = st.text_input("Vrienden Code", placeholder="bv. JAN-482")
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("🚀 Start Direct (Gratis)", type="primary", use_container_width=True):
                    if email and "@" in email:
                        with st.spinner("Account aanmaken..."):
                            auth.login_or_register(email, ref_code_input=ref_code if 'ref_code' in locals() else None)
                            cookie_manager.set("rmecom_user_email", email, expires_at=datetime.now() + timedelta(days=30))
                            st.rerun()
                    else: st.warning("Vul een geldig e-mailadres in.")

            with tab_pro:
                st.markdown("<small style='color:#64748b'>Vul je licentiecode in.</small>", unsafe_allow_html=True)
                pro_email = st.text_input("Jouw Email", key="log_mail")
                lic_key = st.text_input("Licentie Code", placeholder="PRO-XXXX-XXXX")
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("💎 Inloggen", type="primary", use_container_width=True):
                    if pro_email and lic_key:
                        auth.login_or_register(pro_email, license_input=lic_key)
                        cookie_manager.set("rmecom_user_email", pro_email, expires_at=datetime.now() + timedelta(days=30))
                        st.rerun()
                    else: st.warning("Vul alles in.")

    with col_right:
        st.markdown("<br class='desktop-only'>", unsafe_allow_html=True)
        st.markdown("""
            <img src="https://images.unsplash.com/photo-1556742049-0cfed4f7a07d?q=80&w=2070&auto=format&fit=crop" 
                 style="width: 100%; height: 450px; object-fit: cover; border-radius: 16px; margin-bottom: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.1);">
        """, unsafe_allow_html=True)
        st.markdown("""
        ### Waarom deze app?
        ✅ **Stap-voor-stap Roadmap** - Geen chaos meer.  
        🧠 **AI Assistentie** - Laat AI je teksten schrijven.  
        🏆 **Gamification** - Verdien XP en level up.  
        💸 **Verdien Geld** - Nodig vrienden uit (€100 beloning).
        """)
        
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
    st.markdown(f"""
    <div style="margin-bottom: 5px; padding-left: 2px;">
        <h3 style="margin:0; font-size:1rem; color:#0F172A;">👋 {user['email'].split('@')[0].title()}</h3>
        <p style="margin:0; font-size: 0.75rem; color: #64748B;">{auth.get_rank_info(user['xp'])[0]}</p>
    </div>
    """, unsafe_allow_html=True)

    current_title, next_xp_goal = auth.get_rank_info(user['xp'])
    prev_threshold = 0
    for t in [0, 200, 500, 1000]:
        if user['xp'] >= t: prev_threshold = t
    xp_pct = min((user['xp'] - prev_threshold) / (next_xp_goal - prev_threshold), 1.0) if next_xp_goal > prev_threshold else 1.0
    st.progress(xp_pct)
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    menu_options = {
        "🏠 Dashboard": "Dashboard",
        "🎓 Training (Gratis)": "Gratis Mini Training",
        "🔎 Product Finder": "Product Finder",
        "🕵️ Spy Tool": "Spy Tool",
        "🎬 Scripts": "Video Scripts",
        "🩺 Ads Doctor": "Ads Doctor",
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
            <p style="font-size:0.75rem; margin-bottom:5px; color:#64748B;">Klaar voor de volgende stap?</p>
            <a href="{STRATEGY_CALL_URL}" target="_blank" style="text-decoration:none; color: #2563EB; font-weight: 700; font-size: 0.85rem;">
                🚀 Word Student
            </a>
        </div>
        """, unsafe_allow_html=True)

# --- LOCK SCREEN COMPONENT ---
def render_pro_lock(title, desc):
    st.markdown(f"""
    <div class="lock-container">
        <div style="font-size: 40px; margin-bottom: 15px; opacity: 0.5;">🔒</div>
        <h3 style="margin-bottom: 10px; color: #1E293B;">{title}</h3>
        <p style="color: #64748B; font-size: 0.95rem; margin-bottom: 25px; max-width: 500px; margin-left: auto; margin-right: auto; line-height: 1.6;">
            {desc}<br>
            <b>Upgrade naar student voor onbeperkte toegang en coaching.</b>
        </p>
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
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "ticker_msg" not in st.session_state: st.session_state.ticker_msg = auth.get_real_activity()
    st.info(f"⚡ {st.session_state.ticker_msg}")

    next_reward = "Spy Tool" if user['level'] < 2 else "Scripts"
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">HUIDIG LEVEL</div>
            <div class="metric-value">{user['level']}</div>
            <div class="metric-sub" style="color:#64748B;">Starter</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">JOUW XP</div>
            <div class="metric-value">{user['xp']}</div>
            <div class="metric-sub">+25 Vandaag</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">VOLGENDE BELONING</div>
            <div class="metric-value">🎁</div>
            <div class="metric-sub" style="color:#2563EB;">{next_reward}</div>
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
                    found = True; break
            if found: break
            
        total_steps = sum(len(f['steps']) for f in full_map.values())
        done_count = len(completed_steps)
        pct = int(done_count/total_steps*100) if total_steps > 0 else 0

        # GECORRIGEERDE BANNER: GEEN INSPRINGING IN DE HTML STRING
        st.markdown(f"""
<div style="background: linear-gradient(120deg, #2563EB, #1E40AF); padding: 24px; border-radius: 16px; color: white; margin-bottom: 25px; box-shadow: 0 8px 20px -5px rgba(37, 99, 235, 0.4);">
    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; margin-bottom: 8px;">🚀 Huidige Missie</div>
    <h2 style="margin: 0; font-size: 1.4rem; color: white; font-weight: 700;">{next_step_title}</h2>
    <div style="margin-top: 20px; background: rgba(255,255,255,0.2); height: 6px; border-radius: 4px; overflow: hidden;">
        <div style="background: white; width: {pct}%; height: 100%;"></div>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
        <span style="font-size: 0.85rem; opacity: 0.9;">{done_count}/{total_steps} stappen</span>
        <a href="#mission" target="_self" style="text-decoration:none;">
            <div style="background: white; color: #2563EB; padding: 8px 16px; border-radius: 8px; font-weight: bold; font-size: 0.85rem; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                ▶ Start Opdracht
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
                <div style="background: {bg}; border: {border}; padding: 14px; border-radius: 12px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
                    <div style="display:flex; align-items:center; gap: 12px;">
                        <div style="font-weight:700; color: #94A3B8; width: 25px;">{p['rank']}.</div>
                        <div>
                            <div style="font-weight:600; font-size:0.95rem; color:#1E293B;">{p['name']}</div>
                            <div style="font-size:0.75rem; color: #64748B;">{p['title']}</div>
                        </div>
                    </div>
                    <div style="font-weight: 700; font-size: 0.85rem; color: #2563EB; background:#DBEAFE; padding: 4px 8px; border-radius: 6px;">
                        {p['xp']} XP
                    </div>
                </div>
                """, unsafe_allow_html=True)

elif pg == "Gratis Mini Training":
    st.markdown("<h1>🎁 Gratis Mini Cursus</h1>", unsafe_allow_html=True)
    st.caption("Bekijk de lessen direct en pas ze toe. Geen kosten, puur waarde.")
    
    t1, t2, t3, t4 = st.tabs(["1. Mindset", "2. Product", "3. Sales", "4. Scale"])
    
    with t1:
        st.markdown("### 🧠 De Mindset van een Winnaar")
        with st.container(border=True):
             st.markdown('<iframe src="https://drive.google.com/file/d/17H4ioDVVGqTxcz3zQS4lIHtbe4HbCeCI/preview" width="100%" height="400" style="border-radius:8px; border:none;"></iframe>', unsafe_allow_html=True)
        st.info("💡 De meeste mensen falen omdat ze opgeven bij de eerste tegenslag. Bekijk hoe jij dat voorkomt.")

    with t2:
        st.markdown("### 📦 Winnende Producten Vinden")
        with st.container(border=True):
             st.markdown('<iframe src="https://drive.google.com/file/d/134ghHGlE-cK671n6fk1NgmbLPIR_HkXe/preview" width="100%" height="400" style="border-radius:8px; border:none;"></iframe>', unsafe_allow_html=True)
        st.markdown("👉 **Actie:** Gebruik de **Product Finder** in het menu om direct je eerste winnaar te vinden.")

    with t3:
        st.markdown("### 💸 Je Eerste Sale Genereren")
        with st.container(border=True):
             st.markdown('<iframe src="https://drive.google.com/file/d/1xyM_9q2i5FJBF__HvmhDrHTBueBoBstv/preview" width="100%" height="400" style="border-radius:8px; border:none;"></iframe>', unsafe_allow_html=True)
        st.success("Het hoeft niet perfect te zijn om te verkopen. Lanceer snel.")

    with t4:
        st.markdown("### 📈 Van 1 naar 100 Sales")
        with st.container(border=True):
             st.markdown('<iframe src="https://drive.google.com/file/d/1O4fa0FUA10MnCE4QqNNDe3XSLwLfkb_F/preview" width="100%" height="400" style="border-radius:8px; border:none;"></iframe>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: #F0F9FF; padding: 25px; border-radius: 12px; border: 1px solid #BAE6FD; text-align: center;">
            <h4 style="color:#0369A1;">🚀 Klaar voor het echte werk?</h4>
            <p style="color:#0C4A6E;">Je hebt de basis gezien. Wil je dat wij je persoonlijk helpen om dit <b>gegarandeerd</b> te laten slagen?</p>
            <br>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("📞 Plan Gratis Strategie Call", STRATEGY_CALL_URL, type="primary", use_container_width=True)

elif pg == "Product Finder":
    st.title("🔎 Product Finder")
    if not is_pro:
        render_pro_lock(
            "Ontgrendel de Database", 
            "Krijg toegang tot winnende producten, inclusief marges en leveranciers. Onze studenten vinden hiermee dagelijks winnaars."
        )
    else:
        with st.container(border=True):
            col_inp, col_btn = st.columns([3, 1])
            niche = col_inp.text_input("Niche", "Gadgets", label_visibility="collapsed")
            search_clicked = col_btn.button("🔎 Zoek", type="primary", use_container_width=True)

        if search_clicked:
            results = ai_coach.find_real_winning_products(niche, "Viral")
            st.markdown(f"**Resultaten voor '{niche}':**")
            for p in results:
                with st.container(border=True):
                    c1, c2 = st.columns([1, 2])
                    with c1: st.image(p['image_url'], use_column_width=True)
                    with c2:
                        st.markdown(f"### {p['title']}")
                        st.caption(f"Verkoopprijs: €{p['price']}")
                        st.write(p['hook'])
                        
                        df = pd.DataFrame([{"Handle": p['title'], "Price": p['price']}])
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button("⬇️ Download CSV", csv, "product.csv", "text/csv", use_container_width=True)

elif pg == "Spy Tool":
    st.title("🕵️ Spy Tool")
    
    # LOGIC: Temp Access
    has_access = is_pro
    if not has_access and user.get('spy_unlock_until'):
        from datetime import datetime, timezone
        if datetime.fromisoformat(user['spy_unlock_until']) > datetime.now(timezone.utc): has_access = True

    if has_access:
        if not is_pro: st.info("🕒 Tijdelijke toegang actief (24u)")
        with st.container(border=True):
            url = st.text_input("Shopify URL", placeholder="https://concurrent.nl")
            if url and st.button("🚀 Analyseer", type="primary", use_container_width=True):
                # Detailed Animation
                progress_text = "Verbinding maken..."
                bar = st.progress(0, text=progress_text)
                steps = ["Sitemap scannen...", "Database downloaden...", "Traffic analyseren...", "Omzet berekenen...", "Klaar!"]
                for i, txt in enumerate(steps):
                    time.sleep(0.5)
                    bar.progress((i+1)*20, text=txt)
                bar.empty()
                st.success("Analyse succesvol!")
                
                c1, c2 = st.columns(2)
                c1.metric("Geschatte Omzet", "€12,450", "+12%")
                c2.metric("Bestseller", "Galaxy Lamp")
    else:
        render_pro_lock("Bespioneer Concurrenten", "Zie direct de omzet en bestsellers van elke Shopify store.")

elif pg == "Video Scripts":
    st.title("🎬 Viral Scripts")
    
    has_access = is_pro
    if not has_access and user.get('scripts_unlock_until'):
        from datetime import datetime, timezone
        if datetime.fromisoformat(user['scripts_unlock_until']) > datetime.now(timezone.utc): has_access = True
        
    if has_access:
        with st.container(border=True):
            prod = st.text_input("Product Naam")
            if st.button("✨ Schrijf Scripts", type="primary", use_container_width=True) and prod:
                res = ai_coach.generate_viral_scripts(prod, "", "Viral")
                
                st.markdown("### 🔥 3 Virale Hooks")
                for h in res['hooks']: st.info(h)
                
                with st.expander("📜 Volledig Script"):
                    st.text_area("Script", res['full_script'], height=300)
                    
                with st.expander("✉️ Briefing voor Influencers"):
                    st.code(res['creator_brief'], language="text")
    else:
        render_pro_lock("Viral Scripts Generator", "Genereer in 1 klik virale scripts voor TikTok & Reels.")

elif pg == "Ads Doctor":
    st.title("🩺 Ads Doctor")
    if is_pro:
        with st.container(border=True):
            st.info("Upload een screenshot van je Facebook/TikTok Ads Manager.")
            st.file_uploader("Bestand kiezen", type=['png', 'jpg'])
            st.button("Diagnose Starten", type="primary", use_container_width=True)
    else:
        render_pro_lock("Ads Doctor", "Onze AI analyseert je advertenties en vertelt je hoe je ze winstgevend maakt.")

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
                <div class="metric-label">Leden</div>
                <div class="metric-value">{stats[0]}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Pro Leden</div>
                <div class="metric-value">{stats[1]}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Verdiend</div>
                <div class="metric-value">€{stats[2]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("#### Jouw Unieke Code")
            st.caption("Deel deze code. Vrienden krijgen korting, jij krijgt €250 per aangemeld lid.")
            st.code(user['referral_code'], language="text")

    with tab3:
        with st.container(border=True):
            st.markdown("#### Shopify API")
            st.text_input("Shop URL", value=st.session_state.get("sh_url", ""))
            st.text_input("Token", type="password", value=st.session_state.get("sh_token", ""))
            st.button("Opslaan", use_container_width=True)
            
    with tab4:
        with st.container(border=True):
            st.markdown("#### Support")
            st.link_button("💬 Discord Community", "https://discord.com", use_container_width=True)
            st.link_button("📧 Email Support", "mailto:support@rmecom.nl", use_container_width=True)
        
        with st.expander("Veelgestelde Vragen"):
            st.write("**V: Hoe werkt de XP?**")
            st.caption("A: Je krijgt XP voor elke stap die je afrondt.")
            st.write("**V: Wanneer krijg ik uitbetaald?**")
            st.caption("A: Elke 1e van de maand.")