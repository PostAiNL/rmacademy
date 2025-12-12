import streamlit as st
import time
from modules import ai_coach

# HIER STAAT DE URL VOOR DE KNOP
STRATEGY_CALL_URL = "https://calendly.com/rmecomacademy/30min"

def get_roadmap():
    return {
        "fase_1": {
            "title": "Fase 1: De Fundering",
            "desc": "Zonder fundering stort je huis in. Regel dit administratieve werk eerst.", 
            "steps": [
                {
                    "id": "step_kvk", "title": "KVK inschrijving)", "icon": "", "locked": False,
                    "content": "TOOL_KVK_GUIDE", "xp_reward": 100, 
                    "video_url": "https://rmacademy.huddlecommunity.com/module/kvk-inschrijven"
                },
                {
                    "id": "step_bank", "title": "Bank & creditcard wizard", "icon": "", "locked": False,
                    "content": "TOOL_BANK_WIZARD", "xp_reward": 75,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/financieel"
                }
            ]
        },
        "fase_2": {
            "title": "Fase 2: Identiteit & Merk", 
            "desc": "Geef je winkel een gezicht en een naam die blijft hangen.",
            "steps": [
                {
                    "id": "step_brand_name", "title": "Naam & slogan generator", "icon": "", "locked": False,
                    "content": "TOOL_BRAND_NAME", "xp_reward": 125,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/branding"
                },
                # NIEUWE STAP: LOGO MAKER
                {
                    "id": "step_logo_maker", "title": "Logo maker (AI)", "icon": "", "locked": False,
                    "content": "TOOL_LOGO_MAKER", "xp_reward": 150,
                    "teaser": "Ontwerp je eigen professionele logo in seconden."
                },
                {
                    "id": "step_shopify_setup", "title": "Shopify opzetten", "icon": "", "locked": False,
                    "content": "TOOL_SHOPIFY_GUIDE", "xp_reward": 150,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/shopify-setup"
                }
            ]
        },
        "fase_3": {
            "title": "Fase 3: Winst & Content",
            "desc": "Bereken je prijzen en vul je shop met professionele teksten.",
            "steps": [
                {
                    "id": "step_pricing", "title": "Winst calculator", "icon": "", "locked": False,
                    "content": "TOOL_PROFIT_CALC", "xp_reward": 100,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/pricing"
                },
                {
                    "id": "step_about_us", "title": "'Over ons' pagina", "icon": "", "locked": True, 
                    "content": "TOOL_ABOUT_US", "xp_reward": 150,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/copywriting",
                    "teaser": "Laat AI je merkverhaal schrijven in 1 klik."
                },
                {
                    "id": "step_legal", "title": "Juridische pagina's", "icon": "", "locked": True, 
                    "content": "TOOL_LEGAL_GEN", "xp_reward": 100,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/legal",
                    "teaser": "Genereer waterdichte juridische teksten."
                }
            ]
        }
    }

def render_step_card(step, is_completed, is_pro, expanded=False):
    # --- 1. BADGES & KLEUREN ---
    if is_completed:
        badge = "<span style='background:#DCFCE7; color:#166534; padding:4px 10px; border-radius:12px; font-size:0.75rem; font-weight:700; border:1px solid #BBF7D0;'>✅ GEDAAN</span>"
        border_color = "#BBF7D0"
        bg_color = "#FFFFFF"
    elif step['locked'] and not is_pro:
        # GEEN BADGE BIJ LOCKED ITEMS (SCHONER)
        badge = "" 
        border_color = "#E2E8F0"
        bg_color = "#FFFFFF"
    else:
        badge = "<span style='background:#EFF6FF; color:#2563EB; padding:4px 10px; border-radius:12px; font-size:0.75rem; font-weight:700; border:1px solid #DBEAFE;'>START</span>"
        border_color = "#2563EB" if expanded else "#E2E8F0"
        bg_color = "#FFFFFF"

    is_locked = step['locked'] and not is_pro
    usage_key = f"tool_used_{step['id']}"
    result_key = f"tool_result_{step['id']}"

    # --- RENDER CARD HEADER ---
    st.markdown(f"""
    <div style="border: 1px solid {border_color}; border-radius: 12px; padding: 16px; background: {bg_color}; margin-bottom: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.03); display: flex; justify-content: space-between; align-items: center; transition: all 0.2s;">
        <div style="font-weight:600; font-size:1rem; display:flex; align-items:center; gap:12px; color:{'#94A3B8' if is_locked else '#1E293B'};">
            <span style="font-size:1.4rem; opacity:{'0.5' if is_locked else '1'};">{step['icon']}</span> {step['title']}
        </div>
        <div>{badge}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- LOCKED STATE ---
    if is_locked:
        teaser_text = step.get('teaser', 'Upgrade voor toegang.')
        st.markdown(f"""
<div style="background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 12px; padding: 30px; text-align: center; margin-bottom: 20px;">
    <div style="font-size: 24px; margin-bottom: 10px; opacity: 0.6;">🔒</div>
    <h4 style="margin: 0 0 5px 0; color: #1E293B; font-size: 1rem;">Student only</h4>
    <p style="font-size: 0.9rem; color: #64748B; margin: 0 auto 20px auto; max-width: 400px;">{teaser_text}</p>
    <a href="{STRATEGY_CALL_URL}" target="_blank" style="text-decoration: none;">
        <div style="background: linear-gradient(135deg, #2563EB, #1D4ED8); color: white; padding: 10px 24px; border-radius: 50px; font-weight: 600; font-size: 0.9rem; display: inline-block; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2); transition: transform 0.2s;">
            📞 Plan gratis unlock call
        </div>
    </a>
</div>
""", unsafe_allow_html=True)
        return None, 0

    # --- OPEN STATE ---
    expander_label = "Open opdracht & tools"
    
    with st.expander(expander_label, expanded=expanded):
        
        if step.get('video_url'):
            if is_pro:
                st.markdown(f"""
                <a href="{step['video_url']}" target="_blank" style="text-decoration:none;">
                    <div style="margin-bottom: 20px; padding: 12px; background: #EFF6FF; border-radius: 10px; border: 1px solid #DBEAFE; display: flex; align-items: center; gap: 10px; transition: background 0.2s;">
                        <span style="font-size: 1.2rem;"></span>
                        <span style="color: #1E40AF; font-weight: 600; font-size: 0.9rem;">Bekijk de video instructie</span>
                        <span style="margin-left:auto; color:#2563EB;">&rarr;</span>
                    </div>
                </a>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="margin-bottom: 20px; padding: 12px; background: #F8FAFC; border-radius: 10px; border: 1px dashed #CBD5E1; display: flex; align-items: center; gap: 10px; opacity: 0.7;">
                    <span style="font-size: 1.2rem;"></span>
                    <span style="color: #64748B; font-weight: 600; font-size: 0.9rem;">Video instructie (Student only)</span>
                    <span style="margin-left:auto;">🔒</span>
                </div>
                """, unsafe_allow_html=True)

        if step['content'] == "TOOL_KVK_GUIDE":
            st.info("💡 **Tip:** Maak eerst een afspraak, het is vaak druk!")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### 1. Afspraak maken")
                if st.button("📅 Open KVK website", use_container_width=True):
                    st.session_state[usage_key] = True
                    st.link_button("Ga naar KVK.nl", "https://www.kvk.nl")
            with c2:
                st.markdown("##### 2. Omschrijving generator")
                with st.form(key=f"kvk_{step['id']}"):
                    niche = st.text_input("Wat verkoop je?", placeholder="bv. Babykleding")
                    if st.form_submit_button("Genereer"):
                        st.session_state[result_key] = f"Online detailhandel in {niche} en aanverwante artikelen."
                        st.session_state[usage_key] = True
            if result_key in st.session_state:
                st.success("Kopieer dit voor je inschrijving:")
                st.code(st.session_state[result_key], language="text")

        elif step['content'] == "TOOL_BANK_WIZARD":
            st.write("Een zakelijke rekening en creditcard zijn verplicht.")
            c1, c2 = st.columns(2)
            c1.link_button("Knab (Bank)", "https://knab.nl", use_container_width=True)
            c2.link_button("N26 (Creditcard)", "https://n26.com", use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.checkbox("✅ Ik heb dit geregeld"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_BRAND_NAME":
            st.write("Laat AI 5 unieke namen bedenken.")
            with st.form(key=f"brand_{step['id']}"):
                niche = st.text_input("Niche", placeholder="Huisdieren")
                vibe = st.selectbox("Stijl", ["Modern", "Luxe", "Speels"])
                if st.form_submit_button("✨ Genereer namen", type="primary"):
                    st.session_state[usage_key] = True
                    with st.spinner("AI is aan het denken..."):
                        time.sleep(1)
                        st.session_state[result_key] = ai_coach.generate_brand_names(niche, vibe)
            if result_key in st.session_state:
                for item in st.session_state[result_key]:
                    st.info(f"**{item['name']}** - {item['slogan']}")
        
        # --- HIER IS DE NIEUWE LOGO MAKER STAP IN DE ROADMAP ---
        elif step['content'] == "TOOL_LOGO_MAKER":
            st.write("Genereer een logo voor je nieuwe merknaam.")
            with st.form(key=f"logo_{step['id']}"):
                brand_name = st.text_input("Bedrijfsnaam")
                niche = st.text_input("Niche")
                if st.form_submit_button("✨ Maak logo", type="primary"):
                    if brand_name and niche:
                        with st.spinner("Logo wordt ontworpen..."):
                            # Hier roepen we de echte AI functie aan
                            img_url = ai_coach.generate_logo(brand_name, niche, "Modern & Minimal", "Black & White")
                            if img_url:
                                st.session_state[result_key] = img_url
                                st.session_state[usage_key] = True
                            else:
                                st.error("Fout bij genereren.")
            
            if result_key in st.session_state:
                st.image(st.session_state[result_key], caption="Jouw logo")
                st.success("Logo gegenereerd!")

        elif step['content'] == "TOOL_SHOPIFY_GUIDE":
            st.info("💰 **Actie:** Krijg Shopify de eerste 3 maanden voor €1/maand.")
            st.link_button("🚀 Claim €1 Shopify deal", "https://shopify.com", type="primary", use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.checkbox("✅ Ik heb een account aangemaakt"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_PROFIT_CALC":
            st.write("Bereken je winst per product.")
            with st.form(key=f"calc_{step['id']}"):
                c1, c2 = st.columns(2)
                p = c1.number_input("Verkoopprijs (€)", 30.00)
                c = c2.number_input("Inkoop (€)", 10.00)
                if st.form_submit_button("Bereken winst"):
                    st.session_state[usage_key] = True
                    st.session_state[result_key] = p - c
            if result_key in st.session_state:
                st.metric("Bruto winst", f"€{st.session_state[result_key]:.2f}")

        elif step['content'] == "TOOL_ABOUT_US":
            with st.form(key=f"about_{step['id']}"):
                name = st.text_input("Bedrijfsnaam")
                niche = st.text_input("Niche")
                if st.form_submit_button("✍️ Schrijf tekst"):
                    st.session_state[usage_key] = True
                    st.session_state[result_key] = ai_coach.generate_about_us(name, niche)
            if result_key in st.session_state: st.text_area("Resultaat", st.session_state[result_key])

        elif step['content'] == "TOOL_LEGAL_GEN":
            with st.form(key=f"legal_{step['id']}"):
                name = st.text_input("Bedrijfsnaam")
                if st.form_submit_button("Genereer pagina's"):
                    st.session_state[usage_key] = True
                    st.session_state[result_key] = f"Algemene voorwaarden voor {name}..."
            if result_key in st.session_state: st.success("Teksten gegenereerd!")

        st.markdown("<br>", unsafe_allow_html=True)
        if not is_completed:
            can_complete = st.session_state.get(usage_key, False)
            if can_complete:
                if st.button(f"🎉 Afronden & +{step['xp_reward']} XP claimen", key=f"btn_{step['id']}", type="primary", use_container_width=True):
                    return step['id'], step['xp_reward']
            else:
                st.caption("🔒 *Gebruik eerst de tool/link hierboven om af te ronden.*")
                st.button("Afronden", disabled=True, key=f"dis_{step['id']}", use_container_width=True)

    return None, 0