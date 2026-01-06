import streamlit as st
import time
from modules import ai_coach

STRATEGY_CALL_URL = "https://calendly.com/rmecomacademy/30min"

def get_roadmap():
    return {
        "fase_1": {
            "title": "Fase 1: De Fundering", 
            "desc": "Zonder fundering stort je huis in. We beginnen met je idee en je naam.", 
            "steps": [
                {"id": "onboarding_done", "title": "Startschot & Doel", "content": "TEXT_ONLY", "xp_reward": 10, "text": "✅ Je hebt je eerste doel gesteld. Dit is de belangrijkste stap!"},
                {"id": "step_niche", "title": "Wat ga je verkopen?", "content": "TOOL_NICHE_FINDER", "xp_reward": 100, "teaser": "Weet je niet wat je moet verkopen? Gebruik de AI."},
                {"id": "step_domain", "title": "Domeinnaam Kiezen", "content": "TOOL_DOMAIN_CHECK", "xp_reward": 50},
                {"id": "step_bank", "title": "Zakelijke Rekening", "content": "TOOL_BANK_WIZARD", "xp_reward": 75},
                {"id": "step_creditcard", "title": "Creditcard Aanvragen", "content": "TOOL_CREDITCARD_WIZARD", "xp_reward": 50},
            ]
        },
        "fase_2": {
            "title": "Fase 2: Winkel Bouwen", 
            "desc": "Zet het design klaar voor je eerste bezoekers.",
            "steps": [
                {"id": "step_shopify_setup", "title": "Shopify Account Maken", "content": "TOOL_SHOPIFY_GUIDE", "xp_reward": 150},
                {"id": "step_theme", "title": "Logo & Huisstijl", "content": "TOOL_THEME_GUIDE", "xp_reward": 100},
                {"id": "step_payments", "title": "Betalingen Instellen", "content": "TOOL_PAYMENTS", "xp_reward": 125},
            ]
        },
        "fase_3": {
            "title": "Fase 3: Het Aanbod",
            "desc": "Maak van je product een onweerstaanbare deal.",
            "steps": [
                {"id": "step_supplier", "title": "Leverancier Koppelen", "content": "TOOL_SUPPLIER_HUB", "xp_reward": 100},
                {"id": "step_sample", "title": "Sample Bestellen", "content": "TOOL_SAMPLE_GUIDE", "xp_reward": 150, "text": "Bestel het product zelf om video's te maken en de kwaliteit te checken."},
            ]
        }
    }

def render_step_card(step, is_completed, is_pro, expanded=False):
    # Styling variabelen (Ongewijzigd gebleven voor je ronde hoeken/stijl)
    bg_color = "#F0FDF4" if is_completed else "#FFFFFF" if expanded else "#F8FAFC"
    border_color = "#BBF7D0" if is_completed else "#2563EB" if expanded else "#E2E8F0"
    title_color = "#166534" if is_completed else "#0F172A"
    badge = "<i class='bi bi-check-circle-fill'></i>" if is_completed else "NU DOEN" if expanded else ""
    
    # DISCLAIMER TEKST (Universeel)
    disclaimer_text = "⚠️ *Disclaimer: Wij raden deze opties aan op basis van de positieve ervaringen van honderden succesvolle cursisten, maar het staat je volledig vrij om een andere aanbieder te kiezen die bij jou past.*"

    # 1. DE HEADER VAN DE STAP (TITELKAART)
    st.markdown(f"""
    <div style="border: 1px solid {border_color}; background-color: {bg_color}; border-radius: 12px; padding: 16px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: {'0 4px 12px rgba(37, 99, 235, 0.1)' if expanded else 'none'};">
        <div style="font-weight:700; color:{title_color}; font-size: 1rem;">{step['title']}</div>
        <div style="font-size: 0.7rem; font-weight: 800; color: {border_color if not expanded else '#2563EB'};">{badge}</div>
    </div>
    """, unsafe_allow_html=True)

    is_locked = step.get('locked', False) and not is_pro

    if is_locked:
        st.markdown(f"<div style='background:#F1F5F9; padding:10px; border-radius:8px; text-align:center; font-size:0.8rem; color:#64748B; margin-bottom:20px;'>🔒 {step.get('teaser', 'Upgrade voor toegang')}</div>", unsafe_allow_html=True)
        return None, 0
    else:
        st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
        
        with st.expander("🔽 Opdracht & Tools bekijken", expanded=expanded):
            st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
            
            usage_key = f"used_{step['id']}"
            with st.container():
                
                if step.get('content') == "TOOL_THEME_GUIDE":
                    st.markdown("""
                    <div style="background: #F0F9FF; border: 1px solid #BAE6FD; padding: 25px; border-radius: 16px; margin-bottom: 25px;">
                        <h3 style="margin-top: 0; color: #0369A1; font-size: 1.2rem; display: flex; align-items: center; gap: 10px; font-weight: 700;">
                            <span style="font-size: 1.5rem;">🎨</span> Het Gezicht van je Merk
                        </h3>
                        <p style="font-size: 1rem; color: #1E293B; line-height: 1.6; margin-bottom: 20px;">
                            Je logo en huisstijl bepalen de uitstraling van je merk. Snelheid is hierbij belangrijker dan perfectie! Onze regel: Besteed hier maximaal 2 uur aan.
                        </p>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Herkenbaarheid</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Vertrouwen opbouwen</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Merk-consistentie</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown("""<div style="background: white; border: 2px solid #4F46E5; padding: 15px; border-radius: 12px; height: 120px;"><p style="margin: 0; font-weight: 800; color: #4F46E5;">🏆 RM AI Logo Maker</p><p style="font-size: 0.75rem; color: #64748B; margin-top: 5px;">Genereer binnen 10 seconden 3 professionele logo's.</p></div>""", unsafe_allow_html=True)
                        if st.button("👉 Start AI Logo Maker", key="go_to_marketing_btn", use_container_width=True, type="primary"):
                            st.session_state.nav_index = 3
                            st.rerun()
                    with c2:
                        st.markdown("""<div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 120px;"><p style="margin: 0; font-weight: 800; color: #0F172A;">Canva</p><p style="font-size: 0.75rem; color: #64748B; margin-top: 5px;">Zelf ontwerpen met kant-en-klare templates.</p></div>""", unsafe_allow_html=True)
                        st.link_button("Start Canva", "https://www.canva.com", use_container_width=True)
                    with c3:
                        st.markdown("""<div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 120px;"><p style="margin: 0; font-weight: 800; color: #0F172A;">Looka</p><p style="font-size: 0.75rem; color: #64748B; margin-top: 5px;">Laat AI een volledige merkidentiteit bouwen.</p></div>""", unsafe_allow_html=True)
                        st.link_button("Check Looka", "https://looka.com", use_container_width=True)

                    branding_status = st.checkbox("Mijn logo en kleuren zijn definitief gekozen", key=f"branding_check_{step['id']}")
                    if branding_status: st.session_state[usage_key] = True

                elif step.get('content') == "TOOL_PAYMENTS":
                    # --- 1. PREMIUM HEADER ---
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #F0F9FF 0%, #eff6ff 100%); border: 1px solid #BAE6FD; padding: 25px; border-radius: 16px; margin-bottom: 25px;">
                        <h3 style="margin-top: 0; color: #0369A1; font-size: 1.2rem; display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 1.5rem;">💳</span> De Kassa Activeren
                        </h3>
                        <p style="font-size: 0.95rem; color: #0C4A6E; line-height: 1.5;">
                            Zonder betaalmethodes kun je geen sales draaien. In Nederland en België zijn <b>iDEAL</b> en <b>Bancontact</b> essentieel. Je koppelt hiervoor een 'Payment Provider' aan je Shopify shop.
                        </p>
                        <div style="display: flex; gap: 15px; margin-top: 15px; flex-wrap: wrap;">
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1;">✅ iDEAL Geactiveerd</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1;">✅ Bancontact Klaar</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1;">✅ Creditcard Support</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # --- 2. DE VERGELIJKER ---
                    st.markdown("#### 💡 Kies je betaalpartner")
                    
                    c1, c2, c3 = st.columns(3)
                    
                    with c1:
                        st.markdown("""
                        <div style="background: white; border: 2px solid #0284C7; padding: 15px; border-radius: 12px; height: 100%;">
                            <p style="margin: 0; font-weight: 800; color: #0284C7;">🏆 Mollie (Aangeraden)</p>
                            <p style="font-size: 0.8rem; color: #64748B; margin-top: 5px;"><b>Beste voor NL/BE</b>. Extreem makkelijk in te stellen, top-support en de meest vertrouwde checkout voor jouw klanten.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.link_button("Open Mollie Account", "https://www.mollie.com/nl", use_container_width=True, type="primary")

                    with c2:
                        st.markdown("""
                        <div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 100%;">
                            <p style="margin: 0; font-weight: 800; color: #0F172A;">Shopify Payments</p>
                            <p style="font-size: 0.8rem; color: #64748B; margin-top: 5px;"><b>Alles-in-één</b>. Direct ingebouwd in Shopify. Handig voor creditcards, maar soms lastiger met iDEAL verificatie voor starters.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.link_button("Bekijk in Shopify", "https://www.shopify.com", use_container_width=True)

                    with c3:
                        st.markdown("""
                        <div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 100%;">
                            <p style="margin: 0; font-weight: 800; color: #0F172A;">Stripe</p>
                            <p style="font-size: 0.8rem; color: #64748B; margin-top: 5px;"><b>Global Standard</b>. De grootste ter wereld. Vooral sterk als je internationaal gaat buiten de Benelux. Alleen aan te raden bij een groter bereik.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.link_button("Check Stripe", "https://stripe.com/nl", use_container_width=True)

                    # --- 3. CHECKLIST ---
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("📝 Wat heb je nodig voor een snelle goedkeuring?", expanded=False):
                        st.markdown("""
                        Betaalproviders zijn streng. Zorg dat dit op je website staat voordat je de aanvraag indient:
                        1. **Contactgegevens:** Je e-mail en (zakelijk) adres moeten vindbaar zijn.
                        2. **KvK-nummer:** Vermeld dit in de footer van je shop.
                        3. **Voorwaarden:** Zorg dat je 'Algemene Voorwaarden' en 'Privacy Policy' pagina's live staan.
                        4. **Zakelijke Rekening:** Gebruik de rekening die je in de vorige stap hebt geopend.
                        """)

                    st.markdown("---")
                    
                    # --- 4. DE BEVESTIGING ---
                    st.markdown("#### ✅ Checkout Status")
                    pay_status = st.radio("Zijn de betaalmethodes gekoppeld?", 
                                         ["Nog niet begonnen", "Aanvraag ingediend", "✅ iDEAL & Bancontact zijn live!"],
                                         horizontal=True,
                                         key=f"pay_status_{step['id']}")
                    
                    if pay_status == "✅ iDEAL & Bancontact zijn live!":
                        st.success("Gefeliciteerd! Je winkel is nu technisch klaar om geld te verdienen. 🔥")
                        st.session_state[usage_key] = True
                    else:
                        st.session_state[usage_key] = False

                elif step.get('content') == "TOOL_BANK_WIZARD":
                    st.markdown("""
                    <div style="background: #F0F9FF; border: 1px solid #BAE6FD; padding: 25px; border-radius: 16px; margin-bottom: 25px;">
                        <h3 style="margin-top: 0; color: #0369A1; font-size: 1.2rem; display: flex; align-items: center; gap: 10px; font-weight: 700;">
                            <span style="font-size: 1.5rem;">🏦</span> De Financiële Fundering
                        </h3>
                        <p style="font-size: 1rem; color: #1E293B; line-height: 1.6; margin-bottom: 20px;">
                            Houd je privé-uitgaven en je webshop-omzet <b>altijd gescheiden</b>. Dit is niet alleen professioneel, maar bespaart je uren aan werk bij je belastingaangifte.
                        </p>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Belastingproof</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ KvK-nummer nodig</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Boekhoudkoppeling</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown("""<div style="background: white; border: 2px solid #2563EB; padding: 15px; border-radius: 12px; height: 120px;"><p style="margin: 0; font-weight: 800; color: #2563EB;">🏆 Knab</p><p style="font-size: 0.75rem; color: #64748B; margin-top: 5px;">Beste voor starters. Voordelig en koppelt perfect met boekhouding.</p></div>""", unsafe_allow_html=True)
                        st.link_button("Open Knab", "https://www.knab.nl/zakelijk", use_container_width=True)
                    with c2:
                        st.markdown("""<div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 120px;"><p style="margin: 0; font-weight: 800; color: #0F172A;">Bunq</p><p style="font-size: 0.75rem; color: #64748B; margin-top: 5px;">Snelheid & Tech. Binnen 5 minuten een actieve rekening.</p></div>""", unsafe_allow_html=True)
                        st.link_button("Open Bunq", "https://www.bunq.com", use_container_width=True)
                    with c3:
                        st.markdown("""<div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 120px;"><p style="margin: 0; font-weight: 800; color: #0F172A;">Revolut</p><p style="font-size: 0.75rem; color: #64748B; margin-top: 5px;">Internationaal. Ideaal voor werken met buitenlandse valuta.</p></div>""", unsafe_allow_html=True)
                        st.link_button("Open Revolut", "https://www.revolut.com/en-NL/business/", use_container_width=True)

                    with st.expander("📋 Wat heb je nodig voor de aanvraag?", expanded=False):
                        st.markdown("1. KvK-uittreksel | 2. Geldig ID | 3. Zakelijk adres | 4. Je telefoon (verificatie)")

                    bank_choice = st.selectbox("Bij welke bank heb je een rekening aangevraagd?", ["Nog geen keuze gemaakt", "Knab", "Bunq", "Revolut", "Andere bank..."], key=f"bank_choice_{step['id']}")
                    if bank_choice != "Nog geen keuze gemaakt":
                        st.success(f"Top! Je hebt gekozen voor **{bank_choice}**.")
                        st.session_state[usage_key] = True

                elif step.get('content') == "TOOL_CREDITCARD_WIZARD":
                    st.markdown("""
                    <div style="background: #F0F9FF; border: 1px solid #BAE6FD; padding: 25px; border-radius: 16px; margin-bottom: 25px;">
                        <h3 style="margin-top: 0; color: #0369A1; font-size: 1.2rem; display: flex; align-items: center; gap: 10px; font-weight: 700;">
                            <span style="font-size: 1.5rem;">💳</span> De Motor van je Marketing
                        </h3>
                        <p style="font-size: 1rem; color: #1E293B; line-height: 1.6; margin-bottom: 20px;">
                            Om straks te kunnen adverteren op TikTok en Facebook heb je een kaart nodig die direct geaccepteerd wordt. We raden <b>Online Debit Cards</b> aan: geen schulden en binnen 10 minuten actief.
                        </p>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Direct Virtueel Beschikbaar</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Veilig voor Ads</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Geen jaarlijkse kosten</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown("""<div style="background: white; border: 2px solid #F59E0B; padding: 15px; border-radius: 12px; height: 120px;"><p style="margin: 0; font-weight: 800; color: #F59E0B;">🏆 N26 (Snelste)</p><p style="font-size: 0.75rem; color: #64748B; margin-top: 5px;">Direct een virtuele kaart voor Apple/Google Pay en Shopify.</p></div>""", unsafe_allow_html=True)
                        st.link_button("Start met N26", "https://n26.com", use_container_width=True)
                    with c2:
                        st.markdown("""<div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 120px;"><p style="margin: 0; font-weight: 800; color: #0F172A;">Revolut</p><p style="font-size: 0.75rem; color: #64748B; margin-top: 5px;">Handig voor multi-valuta inkoop. Veel controle via de app.</p></div>""", unsafe_allow_html=True)
                        st.link_button("Start met Revolut", "https://www.revolut.com", use_container_width=True)
                    with c3:
                        st.markdown("""<div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 120px;"><p style="margin: 0; font-weight: 800; color: #0F172A;">Bunq Card</p><p style="font-size: 0.75rem; color: #64748B; margin-top: 5px;">Nederlands. Eenvoudig een extra kaart aanmaken bij je rekening.</p></div>""", unsafe_allow_html=True)
                        st.link_button("Start met Bunq", "https://www.bunq.com", use_container_width=True)

                    with st.expander("❓ Waarom heb ik dit nu al nodig?", expanded=False):
                        st.markdown("- **Shopify:** Voor de €1 deal. - **Ads:** Meta/TikTok accepteren geen iDEAL. - **Veilig:** Debit = geen schulden.")

                    card_status = st.radio("Is je kaart aangevraagd of al actief?", ["Nog niet begonnen", "Aangevraagd", "Actief & Gekoppeld"], horizontal=True, key=f"card_status_{step['id']}")
                    if card_status in ["Aangevraagd", "Actief & Gekoppeld"]:
                        st.session_state[usage_key] = True
                # --- STANDAARD CONTENT TYPES (TEXT, NICHE, ETC) ---
                elif step.get('content') == "TEXT_ONLY":
                    st.info(step['text'])
                    st.session_state[usage_key] = True
                
                if step.get('content') == "TOOL_NICHE_FINDER":
                    st.markdown("""
                    <div style="background: #F0F9FF; border: 1px solid #BAE6FD; padding: 25px; border-radius: 16px; margin-bottom: 25px;">
                        <h3 style="margin-top: 0; color: #0369A1; font-size: 1.2rem; display: flex; align-items: center; gap: 10px; font-weight: 700;">
                            <span style="font-size: 1.5rem;">🎯</span> De Perfecte Niche Kiezen
                        </h3>
                        <p style="font-size: 1rem; color: #1E293B; line-height: 1.6; margin-bottom: 20px;">
                            Een <b>niche</b> is simpelweg een specifieke groep mensen met een gezamenlijk probleem of passie. Vul hieronder in wat je leuk vindt (bijv. 'honden', 'auto's' of 'koken'). De AI zoekt daar passende 'winners' bij.
                        </p>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Veel vraag in de markt</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Goed voor starters</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Hoge winstmarges</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    niche_input = st.text_input("Waar liggen je interesses?", placeholder="bijv. interieur, baby's, sport...", key=f"niche_in_{step['id']}")
                    if st.button("🚀 Zoek mijn winnende niche", key=f"nbtn_{step['id']}", use_container_width=True):
                        if niche_input:
                            with st.spinner("Onze AI scant huidige trends..."):
                                results = ai_coach.find_real_winning_products(niche_input)
                                if results:
                                    st.session_state[f"results_{step['id']}"] = results
                        else: st.warning("Vul eerst een interesse in!")

                    if f"results_{step['id']}" in st.session_state:
                        st.markdown("### 💎 Jouw Potentiële Winners")
                        for item in st.session_state[f"results_{step['id']}"]:
                            with st.container(border=True):
                                c1, c2 = st.columns([2, 1])
                                c1.markdown(f"#### {item['title']}")
                                clean_price = str(item['price']).replace('€', '').strip()
                                c2.markdown(f"<div style='text-align:right; color:#16A34A; font-weight:bold;'>Schatting: €{clean_price}</div>", unsafe_allow_html=True)
                                st.markdown(f"**🎥 Viral Hook:** *{item['hook']}*")
                                st.markdown(f"""<div style="background-color: #F0FDF4; padding: 10px; border-radius: 6px; border: 1px solid #BBF7D0; margin-top: 10px;"><span style="font-size: 0.85rem; color: #166534;"><b>💪 Waarom dit werkt:</b> {item['why_works']}</span></div>""", unsafe_allow_html=True)
                                st.link_button(f"Bekijk {item['title']} op TikTok", item['search_links']['tiktok'], use_container_width=True)

                        st.markdown("---")
                        st.markdown("### 🏁 Maak je keuze")
                        final_choice = st.text_input("Welke niche of welk product heb je gekozen?", placeholder="Typ hier je keuze...", key=f"final_choice_{step['id']}")
                        if final_choice:
                            st.success(f"Geweldig! **{final_choice}** wordt jouw focus.")
                            st.session_state[usage_key] = True
                elif step.get('content') == "TOOL_DOMAIN_CHECK":
                    st.markdown("""
                    <div style="background: #F0F9FF; border: 1px solid #BAE6FD; padding: 25px; border-radius: 16px; margin-bottom: 25px;">
                        <h3 style="margin-top: 0; color: #0369A1; font-size: 1.2rem; display: flex; align-items: center; gap: 10px; font-weight: 700;">
                            <span style="font-size: 1.5rem;">🏢</span> Jouw Unieke Adres (Vastgoed)
                        </h3>
                        <p style="font-size: 1rem; color: #1E293B; line-height: 1.6; margin-bottom: 20px;">
                            Dit is hoe klanten je winkel onthouden. Een sterke naam volgt de <b>3-seconden regel</b>: Binnen 3 seconden moet een klant je naam kunnen begrijpen, spellen en onthouden.
                        </p>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Geen streepjes</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Max 3 woorden</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Kies .nl of .com</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    niche_context = st.session_state.get("final_choice_step_niche", "mijn webshop")
                    col_gen1, col_gen2 = st.columns([2.5, 1], vertical_alignment="bottom")
                    brand_input = col_gen1.text_input("Waar gaat je webshop over?", value=niche_context, key=f"domain_prompt_{step['id']}")
                    
                    if col_gen2.button("Genereer Namen ✨", key=f"gbtn_{step['id']}", use_container_width=True, type="primary"):
                        with st.spinner("AI bedenkt namen..."):
                            prompt = f"Bedenk 10 korte catchy domeinnamen zonder streepjes voor: {brand_input}. Geef alleen namen gescheiden door komma's."
                            suggestions_raw = ai_coach.call_llm("Brand Name Expert", prompt)
                            if suggestions_raw: st.session_state[f"domain_list_{step['id']}"] = [s.strip() for s in suggestions_raw.split(',')]

                    if f"domain_list_{step['id']}" in st.session_state:
                        cols = st.columns(2)
                        for i, name in enumerate(st.session_state[f"domain_list_{step['id']}"]):
                            with cols[i % 2]:
                                st.markdown(f"""<div style="background: white; border: 1px solid #E2E8F0; padding: 10px; border-radius: 10px; margin-bottom: 8px; font-weight: 600; color: #2563EB; text-align: center;">{name.lower()}</div>""", unsafe_allow_html=True)

                    st.markdown("---")
                    st.markdown("#### 🔍 Check Beschikbaarheid")
                    st.link_button("👉 Check beschikbaarheid op TransIP", "https://www.transip.nl", use_container_width=True)
                    st.markdown("""<div style="background-color: #FFF7ED; border: 1px solid #FED7AA; padding: 12px; border-radius: 10px; margin-top: 15px;"><p style="margin: 0; color: #9A3412; font-size: 0.85rem; font-weight: 600;">💰 Geld-bespaar tip: Koop alléén de domeinnaam.</p><p style="margin: 5px 0 0 0; color: #9A3412; font-size: 0.8rem;">Neem geen extra 'Hosting' of 'E-mail' pakketten. In de volgende stappen koppelen we je domein direct aan Shopify.</p></div>""", unsafe_allow_html=True)

                    chosen_domain = st.text_input("Claim je plek: Welke domeinnaam is van jou?", placeholder="bijv. www.jouwshop.nl", key=f"final_domain_{step['id']}")
                    if chosen_domain and "." in chosen_domain:
                        st.success(f"🎉 **{chosen_domain}** is vastgelegd!")
                        st.session_state[usage_key] = True

                elif step.get('content') == "TOOL_SHOPIFY_GUIDE":
                    st.markdown("""
                    <div style="background: #F0F9FF; border: 1px solid #BAE6FD; padding: 25px; border-radius: 16px; margin-bottom: 25px;">
                        <h3 style="margin-top: 0; color: #0369A1; font-size: 1.2rem; display: flex; align-items: center; gap: 10px; font-weight: 700;">
                            <span style="font-size: 1.5rem;">🛍️</span> Je Winkelvloer Inrichten
                        </h3>
                        <p style="font-size: 1rem; color: #1E293B; line-height: 1.6; margin-bottom: 20px;">
                            Shopify is het brein van je webshop. Via de RM Academy link krijg je een exclusieve deal: <b>de eerste 3 maanden voor slechts €1 per maand.</b>
                        </p>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Geen techniek nodig</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ €1/maand deal</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Altijd opzegbaar</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("#### 📝 Hoe pak je de €1 deal?")
                    st.markdown("1. Klik op de knop | 2. Vul e-mail in | 3. Skip de vragen | 4. Kies het 'Basic' plan.")
                    st.link_button("🚀 Claim mijn €1 Shopify Deal", "https://www.shopify.com/nl/gratis-proef", use_container_width=True, type="primary")
                    
                    st.markdown("""<div style="background-color: #F0FDF4; border: 1px solid #BBF7D0; padding: 15px; border-radius: 12px; margin-top: 20px;"><p style="margin: 0; color: #166534; font-size: 0.85rem; font-weight: 700;">💡 Bespaar-advies:</p><p style="margin: 5px 0 0 0; color: #166534; font-size: 0.8rem;">Kies niet voor de duurdere plannen. Het <b>Basic plan</b> heeft alles wat je nodig hebt.</p></div>""", unsafe_allow_html=True)

                    shop_url = st.text_input("Wat is de naam van je shop?", placeholder="bijv. jouwshopnaam.myshopify.com", key=f"shop_url_input_{step['id']}")
                    if shop_url:
                        if ".myshopify.com" not in shop_url and "." not in shop_url: shop_url = f"{shop_url}.myshopify.com"
                        if ".myshopify.com" in shop_url:
                            st.success(f"Perfect! Shop **{shop_url}** is geregistreerd.")
                            st.session_state[usage_key] = True
              
                elif step.get('content') == "TOOL_SUPPLIER_HUB":
                    st.markdown("""
                    <div style="background: #F0F9FF; border: 1px solid #BAE6FD; padding: 25px; border-radius: 16px; margin-bottom: 25px;">
                        <h3 style="margin-top: 0; color: #0369A1; font-size: 1.2rem; display: flex; align-items: center; gap: 10px; font-weight: 700;">
                            <span style="font-size: 1.5rem;">📦</span> De Logistieke Machine
                        </h3>
                        <p style="font-size: 1rem; color: #1E293B; line-height: 1.6; margin-bottom: 20px;">
                            Je leverancier is je belangrijkste partner. Stop met 3 weken wachten via AliExpress en kies voor een systeem dat schaalbaar is en snelle levertijden garandeert.
                        </p>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ 7-10 Dagen Levering</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Eigen Brand Logo</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Handmatige Check</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown("""<div style="background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); border: 2px solid #F59E0B; padding: 15px; border-radius: 12px; height: 120px;"><p style="margin: 0; font-weight: 800; color: #92400E;">🏆 RM Private Agent</p><p style="font-size: 0.75rem; color: #B45309; margin-top: 5px;">Elite Methode. Alleen voor studenten.</p></div>""", unsafe_allow_html=True)
                        if not is_pro: st.link_button("🔒 Unlock Agent", STRATEGY_CALL_URL, use_container_width=True, type="primary")
                        else: st.button("✅ Toegang Verleend", disabled=True, use_container_width=True)
                    with c2:
                        st.markdown("""<div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 120px;"><p style="margin: 0; font-weight: 800; color: #0F172A;">DSers</p><p style="font-size: 0.75rem; color: #64748B; margin-top: 5px;">De Test-fase via AliExpress.</p></div>""", unsafe_allow_html=True)
                        st.link_button("Open DSers", "https://www.dsers.com", use_container_width=True)
                    with c3:
                        st.markdown("""<div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 120px;"><p style="margin: 0; font-weight: 800; color: #0F172A;">CJ Dropshipping</p><p style="font-size: 0.75rem; color: #64748B; margin-top: 5px;">De Middenweg met eigen warehouses.</p></div>""", unsafe_allow_html=True)
                        st.link_button("Open CJ Drop", "https://cjdropshipping.com", use_container_width=True)

                    supplier_ready = st.checkbox("Ik heb mijn shop gekoppeld aan een leverancier", key=f"supp_check_{step['id']}")
                    if supplier_ready: st.session_state[usage_key] = True

                elif step.get('content') == "TOOL_SAMPLE_GUIDE":
                    st.markdown("""
                    <div style="background: #F0F9FF; border: 1px solid #BAE6FD; padding: 25px; border-radius: 16px; margin-bottom: 25px;">
                        <h3 style="margin-top: 0; color: #0369A1; font-size: 1.2rem; display: flex; align-items: center; gap: 10px; font-weight: 700;">
                            <span style="font-size: 1.5rem;">📸</span> De Geheime Sleutel tot Sales
                        </h3>
                        <p style="font-size: 1rem; color: #1E293B; line-height: 1.6; margin-bottom: 20px;">
                            De winnaars maken <b>originele content</b>. Bestel het product zelf om video's te maken en de kwaliteit te checken. Dit bouwt 10x meer vertrouwen op.
                        </p>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Unieke Video Content</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Kwaliteit Controle</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #7DD3FC; color: #0369A1; font-weight: 600;">✅ Geen Copyright Issues</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    c1, c2 = st.columns(2)
                    c1.link_button("Zoek op Amazon.nl (Snelst)", "https://www.amazon.nl", use_container_width=True)
                    c2.link_button("Bestel bij Leverancier", "https://www.aliexpress.com", use_container_width=True)

                    sample_ordered = st.checkbox("Ik heb het product besteld en ga content maken", key=f"sample_check_{step['id']}")
                    if sample_ordered: st.session_state[usage_key] = True

    # Dit is cruciaal: stuur altijd (None, 0) terug als er niet op een knop is gedrukt
    return None, 0