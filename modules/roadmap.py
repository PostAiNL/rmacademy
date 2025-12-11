import streamlit as st
import time
from modules import ai_coach

def get_roadmap():
    return {
        "fase_1": {
            "title": "Fase 1: De Fundering 🏗️",
            "desc": "Zonder fundering stort je huis in. Regel dit administratieve werk eerst, dan kun je door.", 
            "steps": [
                {
                    "id": "step_kvk", 
                    "title": "KVK Inschrijving (Cheat Sheet)", 
                    "icon": "📝", 
                    "locked": False,
                    "content": "TOOL_KVK_GUIDE", 
                    "xp_reward": 100, 
                    "video_url": "https://rmacademy.huddlecommunity.com/module/kvk-inschrijven"
                },
                {
                    "id": "step_bank", 
                    "title": "Bank & Creditcard Wizard", 
                    "icon": "💳", 
                    "locked": False,
                    "content": "TOOL_BANK_WIZARD", 
                    "xp_reward": 75,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/financieel"
                }
            ]
        },
        "fase_2": {
            "title": "Fase 2: Identiteit & Merk 🎨",
            "desc": "Nu wordt het leuk. We gaan je winkel een gezicht geven.",
            "steps": [
                {
                    "id": "step_brand_name", 
                    "title": "Naam & Slogan Generator", 
                    "icon": "🧠", 
                    "locked": False,
                    "content": "TOOL_BRAND_NAME", 
                    "xp_reward": 125,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/branding"
                },
                {
                    "id": "step_shopify_setup", 
                    "title": "Shopify Opzetten", 
                    "icon": "🛍️", 
                    "locked": False,
                    "content": "TOOL_SHOPIFY_GUIDE", 
                    "xp_reward": 150,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/shopify-setup"
                }
            ]
        },
        "fase_3": {
            "title": "Fase 3: Winst & Content 💰",
            "desc": "Bereken je prijzen en vul je shop met professionele teksten.",
            "steps": [
                {
                    "id": "step_pricing", 
                    "title": "Winst Calculator", 
                    "icon": "🧮", 
                    "locked": False,
                    "content": "TOOL_PROFIT_CALC", 
                    "xp_reward": 100,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/pricing"
                },
                {
                    "id": "step_about_us", 
                    "title": "'Over Ons' Pagina (Pro)", 
                    "icon": "📜", 
                    "locked": True, 
                    "content": "TOOL_ABOUT_US", 
                    "xp_reward": 150,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/copywriting"
                },
                {
                    "id": "step_legal", 
                    "title": "Juridische Pagina's (Pro)", 
                    "icon": "⚖️", 
                    "locked": True, 
                    "content": "TOOL_LEGAL_GEN", 
                    "xp_reward": 100,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/legal"
                }
            ]
        }
    }

def render_step_card(step, is_completed, is_pro, expanded=False):
    status_icon = "✅ Voltooid" if is_completed else "⭕ Te doen"
    is_locked = step['locked'] and not is_pro
    
    # Als deze stap de 'Active Mission' is, maken we de kaart visueel opvallender
    border_style = "2px solid #0ea5e9" if expanded else "1px solid #e2e8f0"
    
    usage_key = f"tool_used_{step['id']}"
    result_key = f"tool_result_{step['id']}" # Opslag voor resultaten (zodat ze niet verdwijnen)
    
    # LOCK SCREEN (PRO STEPS)
    if is_locked:
        st.markdown(f"""
        <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 10px; padding: 15px; opacity: 0.8; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#64748b;">🔒 {step['title']}</h4>
                <span style="background:#e2e8f0; color:#475569; padding:2px 8px; border-radius:10px; font-size:0.7em; font-weight:bold;">STUDENT ONLY</span>
            </div>
            <p style="font-size:0.85em; margin-top:5px; color:#64748b;">
                Word student om deze AI-tool te gebruiken en nog eens <b>{step['xp_reward']} XP</b> te verdienen.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return None, 0

    # OPEN STEPS
    # We gebruiken custom CSS/HTML om de border te highlighten als hij 'expanded' is
    with st.container(border=False):
        # Header kaartje
        st.markdown(f"""
        <div style="border: {border_style}; border-radius: 10px; padding: 15px; background: white; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-weight:bold; font-size:1.1em;">{step['icon']} {step['title']}</div>
                <div style="font-size:0.9em;">{status_icon}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Link naar Huddle (Buiten de expander zodat hij altijd zichtbaar is)
        if step.get('video_url'):
            if is_pro:
                st.markdown(f"<div style='margin-top:5px; font-size:0.9em;'>🎥 <a href='{step['video_url']}' target='_blank' style='text-decoration:none; color:#0ea5e9;'>Bekijk video instructie</a></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='margin-top:5px; font-size:0.85em; color:#94a3b8;'>🎥 <i>Video instructie (Alleen Studenten)</i></div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True) # Sluit header div

        # De Tool Expander
        expander_label = "🚀 Start deze Opdracht" if expanded else "📂 Open Opdracht & Tool"
        
        with st.expander(expander_label, expanded=expanded):
            
            # --- TOOL: KVK GUIDE ---
            if step['content'] == "TOOL_KVK_GUIDE":
                st.info("💡 **Tip:** Maak een afspraak, want het is vaak druk! Je hebt een 'Eenmanszaak' nodig.")
                
                c_links, c_gen = st.columns(2)
                with c_links:
                    st.markdown("#### 🔗 Direct Regelen")
                    if st.button("📅 Naar KVK Afspraak Pagina", use_container_width=True):
                        st.session_state[usage_key] = True
                        st.markdown(f'<meta http-equiv="refresh" content="0;url=https://www.kvk.nl/inschrijven-en-wijzigen/inschrijven-onderneming/">', unsafe_allow_html=True)
                    st.markdown("- **Rechtsvorm:** Eenmanszaak\n- **SBI Code:** `4791`")

                with c_gen:
                    st.markdown("#### 📝 Omschrijving Generator")
                    with st.form(key=f"kvk_form_{step['id']}"):
                        kvk_niche = st.text_input("Wat verkoop je?", placeholder="bv. Babykleding")
                        submit_kvk = st.form_submit_button("Genereer Omschrijving")
                        
                        if submit_kvk and kvk_niche:
                            st.session_state[result_key] = f"Online detailhandel gespecialiseerd in {kvk_niche} en aanverwante artikelen."
                            st.session_state[usage_key] = True
                    
                    if result_key in st.session_state:
                        st.success("Kopieer dit voor je inschrijving:")
                        st.code(st.session_state[result_key], language="text")

            # --- TOOL: BANK WIZARD ---
            elif step['content'] == "TOOL_BANK_WIZARD":
                st.write("Je hebt twee dingen nodig om te starten:")
                tab_bank, tab_cc = st.tabs(["1. Zakelijke Rekening", "2. Creditcard (Verplicht)"])
                with tab_bank:
                    st.info("Gebruik NOOIT je privé rekening. Houd zakelijk gescheiden.")
                    col_b1, col_b2 = st.columns(2)
                    col_b1.link_button("🏦 Knab (Aanrader)", "https://knab.nl", use_container_width=True)
                    col_b2.link_button("🌈 Bunq", "https://bunq.com", use_container_width=True)
                with tab_cc:
                    st.warning("⚠️ Zonder creditcard kun je Shopify & Facebook Ads NIET betalen.")
                    st.write("Geen creditcard? Gebruik N26 of Revolut.")
                    c_cc1, c_cc2 = st.columns(2)
                    c_cc1.link_button("💳 N26 (Gratis)", "https://n26.com", use_container_width=True)
                    c_cc2.link_button("💳 Revolut (Gratis)", "https://revolut.com", use_container_width=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.checkbox("Ik heb een rekening of creditcard aangevraagd"):
                    st.session_state[usage_key] = True

            # --- TOOL: PROFIT CALCULATOR ---
            elif step['content'] == "TOOL_PROFIT_CALC":
                st.write("Reken je niet rijk. Bereken hier je **echte** winst per product.")
                
                # Gebruik FORM zodat pagina niet herlaadt tijdens typen
                with st.form(key=f"calc_form_{step['id']}"):
                    c1_p, c2_p, c3_p = st.columns(3)
                    price = c1_p.number_input("Verkoopprijs (incl BTW)", value=29.95, step=1.0)
                    cost = c2_p.number_input("Inkoop (Aliexpress/Lev.)", value=8.00, step=1.0)
                    ads = c3_p.number_input("Geschatte Ads kosten (CPA)", value=10.00, step=1.0)
                    submit_calc = st.form_submit_button("💰 Bereken Winst", type="primary")

                if submit_calc:
                    st.session_state[usage_key] = True 
                    btw_bedrag = price - (price / 1.21) 
                    shopify_fee = (price * 0.02) + 0.25
                    totale_kosten = cost + ads + btw_bedrag + shopify_fee
                    winst = price - totale_kosten
                    marge = (winst / price) * 100
                    
                    # Sla resultaat op
                    st.session_state[result_key] = {
                        "omzet": price,
                        "kosten": totale_kosten,
                        "winst": winst,
                        "marge": marge
                    }

                # Toon resultaat als het bestaat
                if result_key in st.session_state:
                    res = st.session_state[result_key]
                    st.markdown("---")
                    c_res1, c_res2, c_res3 = st.columns(3)
                    c_res1.metric("🛒 Omzet", f"€{res['omzet']:.2f}")
                    c_res2.metric("💸 Totale Kosten", f"€{res['kosten']:.2f}", help="Inclusief Inkoop, Ads, BTW (21%) en Shopify fees")
                    color = "normal" if res['winst'] > 0 else "inverse"
                    c_res3.metric("💰 Netto Winst", f"€{res['winst']:.2f}", f"{res['marge']:.1f}% Marge", delta_color=color)

            # --- TOOL: BRAND NAME ---
            elif step['content'] == "TOOL_BRAND_NAME":
                st.write("Vind direct een unieke naam inclusief slogan.")
                
                with st.form(key=f"brand_form_{step['id']}"):
                    c1_bn, c2_bn = st.columns([2, 1])
                    with c1_bn: bn_niche = st.text_input("Wat verkoop je?", placeholder="Autos")
                    with c2_bn: bn_vibe = st.selectbox("Uitstraling?", ["Stoer", "Luxe", "Modern"])
                    submit_brand = st.form_submit_button("✨ Genereer Merk Concepten", type="primary")

                if submit_brand:
                    if not bn_niche: 
                        st.warning("Vul in wat je verkoopt.")
                    else:
                        st.session_state[usage_key] = True
                        with st.spinner("🧠 De AI bedenkt namen & slogans..."):
                            suggestions = ai_coach.generate_brand_names(bn_niche, bn_vibe)
                            st.session_state[result_key] = suggestions
                
                if result_key in st.session_state:
                    for item in st.session_state[result_key]:
                        with st.container(border=True):
                            col_text, col_check = st.columns([3, 1])
                            col_text.subheader(item.get('name'))
                            col_text.markdown(f"📣 *{item.get('slogan')}*")
                            col_check.link_button("Check URL", f"https://www.sidn.nl/zoeken?q={item.get('name')}")

            # --- TOOL: SHOPIFY GUIDE ---
            elif step['content'] == "TOOL_SHOPIFY_GUIDE":
                st.write("Volg deze 3 fases om je winkel technisch perfect te zetten.")
                st.info("💡 **Pro Tip:** Gebruik de '3 maanden voor €1' deal. Dit scheelt je direct €90 startkapitaal.")
                st.link_button("🚀 Claim de €1 Shopify Deal", "https://shopify.com", type="primary", use_container_width=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                tab_setup, tab_design, tab_sales = st.tabs(["⚙️ 1. Instellingen", "🎨 2. Design", "💳 3. Kassa & Verzending"])
                
                check_count = 0
                with tab_setup:
                    if st.checkbox("Account aangemaakt"): check_count += 1
                    if st.checkbox("Wachtwoord verwijderd"): check_count += 1
                with tab_design:
                    if st.checkbox("Thema 'Dawn' geïnstalleerd"): check_count += 1
                    st.link_button("🎨 Maak gratis logo in Canva", "https://www.canva.com/create/logos/")
                with tab_sales:
                    if st.checkbox("Betalingen geactiveerd"): check_count += 1
                    if st.checkbox("Verzendtarief op €0,00 (Gratis) gezet"): check_count += 1
                
                if check_count >= 1: st.session_state[usage_key] = True

            # --- TOOL: OVER ONS ---
            elif step['content'] == "TOOL_ABOUT_US":
                st.write("Genereer je verhaal.")
                
                with st.form(key=f"about_form_{step['id']}"):
                    au_name = st.text_input("Bedrijfsnaam")
                    au_niche = st.text_input("Niche")
                    submit_about = st.form_submit_button("✍️ Schrijf Tekst")
                
                if submit_about:
                    st.session_state[usage_key] = True
                    with st.spinner("AI is aan het schrijven..."):
                        res = ai_coach.generate_about_us(au_name, au_niche)
                        st.session_state[result_key] = res
                
                if result_key in st.session_state:
                    st.text_area("Resultaat", st.session_state[result_key], height=200)

            # --- TOOL: LEGAL ---
            elif step['content'] == "TOOL_LEGAL_GEN":
                st.write("Genereer juridische teksten.")
                
                with st.form(key=f"legal_form_{step['id']}"):
                    l_name = st.text_input("Bedrijfsnaam")
                    l_mail = st.text_input("Email")
                    submit_legal = st.form_submit_button("Genereer Beleid")
                
                if submit_legal:
                    st.session_state[usage_key] = True
                    # Simpele generatie (placeholder voor echte AI call indien nodig)
                    res = f"Retourneren bij {l_name} kan binnen 14 dagen via {l_mail}. Wij storten het bedrag binnen 5 werkdagen terug."
                    st.session_state[result_key] = res
                
                if result_key in st.session_state:
                    st.text_area("Retourbeleid", st.session_state[result_key], height=150)

            # NORMALE TEKST
            else:
                st.markdown(step['content'])
            
            # --- AFVINK KNOP ---
            if not is_completed:
                st.markdown("<br>", unsafe_allow_html=True)
                tool_used = st.session_state.get(usage_key, False)
                
                if tool_used:
                    if st.button(f"✅ Markeer als gedaan (+{step['xp_reward']} XP)", key=f"done_{step['id']}", type="primary"):
                        return step['id'], step['xp_reward']
                else:
                    st.caption(f"🔒 *Gebruik eerst de tool hierboven om deze stap te voltooien.*")
                    st.button(f"Markeer als gedaan (+{step['xp_reward']} XP)", key=f"disabled_{step['id']}", disabled=True)
                    
    return None, 0
