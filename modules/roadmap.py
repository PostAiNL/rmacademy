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
                {"id": "step_sample", "title": "Sample Bestellen", "content": "TEXT_ONLY", "xp_reward": 150, "text": "Bestel het product zelf om video's te maken en de kwaliteit te checken."},
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
                    # --- 1. PREMIUM HEADER ---
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); border: 1px solid #4338CA; padding: 25px; border-radius: 16px; margin-bottom: 25px; color: white;">
                        <h3 style="margin-top: 0; color: #FFFFFF !important; font-size: 1.25rem; display: flex; align-items: center; gap: 10px; font-weight: 700;">
                            <span style="font-size: 1.5rem;">🎨</span> De Gezichten van je Merk
                        </h3>
                        <p style="font-size: 1rem; color: #E0E7FF !important; line-height: 1.5; margin-bottom: 15px;">
                            Je logo en huisstijl zijn de "verpakking" van je webshop. Een professionele uitstraling zorgt voor direct vertrouwen bij je klant. <b>Onze regel:</b> Besteed hier maximaal 2 uur aan. Snelheid is belangrijker dan perfectie!
                        </p>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                            <span style="background: rgba(255,255,255,0.15); padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.3); color: white !important; font-weight: 600;">✅ Herkenbaarheid</span>
                            <span style="background: rgba(255,255,255,0.15); padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.3); color: white !important; font-weight: 600;">✅ Vertrouwen opbouwen</span>
                            <span style="background: rgba(255,255,255,0.15); padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.3); color: white !important; font-weight: 600;">✅ Merk-consistentie</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # --- 2. DE OPTIES ---
                    st.markdown("#### 💡 Kies je ontwerp-route")
                    
                    c1, c2, c3 = st.columns(3)
                    
                    with c1:
                        st.markdown("""
                        <div style="background: white; border: 2px solid #4F46E5; padding: 15px; border-radius: 12px; height: 100%;">
                            <p style="margin: 0; font-weight: 800; color: #4F46E5;">🏆 RM AI Logo Maker</p>
                            <p style="font-size: 0.8rem; color: #64748B; margin-top: 5px;"><b>Aanbevolen</b>. Maak binnen 10 seconden 3 professionele logo's. Gratis voor DEMO (3x) & PRO leden.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("👉 Start AI Logo Maker", key="go_to_marketing_btn", use_container_width=True, type="primary"):
                            st.session_state.nav_index = 3
                            st.rerun()

                    with c2:
                        st.markdown("""
                        <div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 100%;">
                            <p style="margin: 0; font-weight: 800; color: #0F172A;">Canva</p>
                            <p style="font-size: 0.8rem; color: #64748B; margin-top: 5px;"><b>Zelf ontwerpen</b>. Gebruik kant-en-klare templates voor logo's, banners en kleuren. Ideaal voor volledige controle.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.link_button("Start Canva", "https://www.canva.com", use_container_width=True)

                    with c3:
                        st.markdown("""
                        <div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 100%;">
                            <p style="margin: 0; font-weight: 800; color: #0F172A;">Looka / Fiverr</p>
                            <p style="font-size: 0.8rem; color: #64748B; margin-top: 5px;"><b>Uitbesteden</b>. Laat AI of een freelancer een premium merkidentiteit bouwen als je budget hebt.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.link_button("Check Looka", "https://looka.com", use_container_width=True)

                    # --- 3. DESIGN TIPS VOOR STARTERS ---
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("🎨 3 Design regels voor een winnende shop", expanded=False):
                        st.markdown("""
                        1. **De 2-Kleuren Regel:** Kies één hoofdkleur (bijv. blauw) en één accentkleur (bijv. wit of grijs). Teveel kleuren maken je shop onoverzichtelijk.
                        2. **Witruimte is je vriend:** Prop je website niet vol. Laat ruimte tussen tekst en afbeeldingen voor een luxe uitstraling.
                        3. **Hoge Kwaliteit:** Gebruik nooit korrelige of uitgerekte logo's. Download je logo altijd als PNG met transparante achtergrond.
                        """)

                    st.markdown("---")
                    
                    # --- 4. DE BEVESTIGING ---
                    st.markdown("#### ✅ Heb je je huisstijl klaar?")
                    branding_status = st.checkbox("Mijn logo en kleuren zijn definitief gekozen", key=f"branding_check_{step['id']}")
                    
                    if branding_status:
                        st.success("Mooi! Je merk heeft nu een gezicht. Op naar de volgende stap!")
                        st.session_state[usage_key] = True
                    else:
                        st.session_state[usage_key] = False

                elif step.get('content') == "TOOL_PAYMENTS":
                    # --- 1. PREMIUM HEADER ---
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%); border: 1px solid #BAE6FD; padding: 25px; border-radius: 16px; margin-bottom: 25px;">
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
                    # --- 1. PREMIUM HEADER ---
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); border: 1px solid #BBF7D0; padding: 25px; border-radius: 16px; margin-bottom: 25px;">
                        <h3 style="margin-top: 0; color: #166534; font-size: 1.2rem; display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 1.5rem;">🏦</span> De Financiële Fundering
                        </h3>
                        <p style="font-size: 0.95rem; color: #14532D; line-height: 1.5;">
                            Houd je privé-uitgaven en je webshop-omzet <b>altijd gescheiden</b>. Dit is niet alleen professioneel, maar bespaart je uren aan werk (en stress) bij je belastingaangifte.
                        </p>
                        <div style="display: flex; gap: 15px; margin-top: 15px; flex-wrap: wrap;">
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #86EFAC; color: #166534;">✅ Belastingproof</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #86EFAC; color: #166534;">✅ KvK-nummer nodig</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #86EFAC; color: #166534;">✅ Koppeling met Boekhouding</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # --- 2. DE VERGELIJKER ---
                    st.markdown("#### 💡 Kies de bank die bij je past")
                    
                    c1, c2, c3 = st.columns(3)
                    
                    with c1:
                        st.markdown("""
                        <div style="background: white; border: 2px solid #2563EB; padding: 15px; border-radius: 12px; height: 100%;">
                            <p style="margin: 0; font-weight: 800; color: #2563EB;">🏆 Knab</p>
                            <p style="font-size: 0.8rem; color: #64748B; margin-top: 5px;"><b>Beste voor starters</b>. Erg voordelig, goede app en koppelt perfect met vrijwel elk boekhoudpakket.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.link_button("Open Knab", "https://www.knab.nl/zakelijk", use_container_width=True)

                    with c2:
                        st.markdown("""
                        <div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 100%;">
                            <p style="margin: 0; font-weight: 800; color: #0F172A;">Bunq</p>
                            <p style="font-size: 0.8rem; color: #64748B; margin-top: 5px;"><b>Snelheid & Tech</b>. Je hebt binnen 5 minuten een rekening. Iets duurder, maar zeer innovatief.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.link_button("Open Bunq", "https://www.bunq.com", use_container_width=True)

                    with c3:
                        st.markdown("""
                        <div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 100%;">
                            <p style="margin: 0; font-weight: 800; color: #0F172A;">Revolut</p>
                            <p style="font-size: 0.8rem; color: #64748B; margin-top: 5px;"><b>Internationaal</b>. Ideaal als je veel met buitenlandse valuta werkt. Gebruiksvriendelijke interface.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.link_button("Open Revolut", "https://www.revolut.com/en-NL/business/", use_container_width=True)

                    # --- 3. CHECKLIST VOOR STARTERS ---
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("📋 Wat heb je nodig voor de aanvraag?", expanded=False):
                        st.markdown("""
                        Zorg dat je deze zaken bij de hand hebt voordat je op de knop drukt:
                        1. **KvK-uittreksel:** Meestal niet ouder dan 30 dagen.
                        2. **Geldig ID:** Paspoort of ID-kaart (rijbewijs wordt vaak niet geaccepteerd).
                        3. **Zakelijk adres:** Het adres waarop je KvK staat ingeschreven.
                        4. **Je telefoon:** De meeste banken vragen om een selfie-verificatie via hun app.
                        """)

                    st.markdown("---")
                    
                    # --- 4. DE BEVESTIGING ---
                    st.markdown("#### ✅ Status van je aanvraag")
                    bank_choice = st.selectbox("Bij welke bank heb je een rekening aangevraagd?", 
                                              ["Nog geen keuze gemaakt", "Knab", "Bunq", "Revolut", "Andere bank..."],
                                              key=f"bank_choice_{step['id']}")
                    
                    if bank_choice != "Nog geen keuze gemaakt":
                        st.success(f"Top! Je hebt gekozen voor **{bank_choice}**. Zodra je rekening actief is, kun je deze koppelen aan je shop.")
                        st.session_state[usage_key] = True
                    else:
                        st.session_state[usage_key] = False

                elif step.get('content') == "TOOL_CREDITCARD_WIZARD":
                    # --- 1. PREMIUM HEADER ---
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%); border: 1px solid #FED7AA; padding: 25px; border-radius: 16px; margin-bottom: 25px;">
                        <h3 style="margin-top: 0; color: #9A3412; font-size: 1.2rem; display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 1.5rem;">💳</span> De Motor van je Marketing
                        </h3>
                        <p style="font-size: 0.95rem; color: #7C2D12; line-height: 1.5;">
                            Om straks te kunnen schalen op TikTok en Facebook heb je een kaart nodig die direct geaccepteerd wordt. We raden <b>Online Debit Cards</b> aan: geen schulden, geen BKR-toetsing en binnen 10 minuten actief.
                        </p>
                        <div style="display: flex; gap: 15px; margin-top: 15px; flex-wrap: wrap;">
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #FDBA74; color: #9A3412;">✅ Direct Virtueel Beschikbaar</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #FDBA74; color: #9A3412;">✅ Veilig voor Ads (Meta/TikTok)</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #FDBA74; color: #9A3412;">✅ Geen jaarlijkse kosten</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # --- 2. DE VERGELIJKER ---
                    st.markdown("#### ⚡ Kies je kaart en start direct")
                    
                    c1, c2, c3 = st.columns(3)
                    
                    with c1:
                        st.markdown("""
                        <div style="background: white; border: 2px solid #F59E0B; padding: 15px; border-radius: 12px; height: 100%;">
                            <p style="margin: 0; font-weight: 800; color: #F59E0B;">🏆 N26 (Snelste)</p>
                            <p style="font-size: 0.8rem; color: #64748B; margin-top: 5px;"><b>Favoriet</b>. Je krijgt direct een virtuele kaart die je in je Apple/Google Pay kunt zetten en koppelen aan Shopify.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.link_button("Start met N26", "https://n26.com", use_container_width=True)

                    with c2:
                        st.markdown("""
                        <div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 100%;">
                            <p style="margin: 0; font-weight: 800; color: #0F172A;">Revolut</p>
                            <p style="font-size: 0.8rem; color: #64748B; margin-top: 5px;"><b>Multi-valuta</b>. Handig als je in dollars wilt inkopen. Zeer uitgebreide app met veel controle.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.link_button("Start met Revolut", "https://www.revolut.com", use_container_width=True)

                    with c3:
                        st.markdown("""
                        <div style="background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; height: 100%;">
                            <p style="margin: 0; font-weight: 800; color: #0F172A;">Bunq Card</p>
                            <p style="font-size: 0.8rem; color: #64748B; margin-top: 5px;"><b>Nederlands</b>. Als je al Bunq hebt voor je zakelijke rekening, kun je hier simpel een extra kaart aanmaken.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.link_button("Start met Bunq", "https://www.bunq.com", use_container_width=True)

                    # --- 3. EDUCATIEVE BIJSLUITER ---
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("❓ Waarom heb ik dit nu al nodig?", expanded=False):
                        st.markdown("""
                        Veel starters wachten hiermee, maar dat is een fout. 
                        - **Shopify:** Je hebt een kaart nodig om je €1/maand proefperiode te activeren.
                        - **Advertenties:** Facebook en TikTok accepteren geen iDEAL voor hun advertentie-accounts. Ze willen een kaart 'on file'.
                        - **Geen Schulden:** Omdat het 'Debit' kaarten zijn, kun je alleen uitgeven wat je er zelf op zet. Je loopt dus geen enkel financieel risico.
                        """)

                    st.markdown("---")
                    
                    # --- 4. DE BEVESTIGING ---
                    st.markdown("#### ✅ Status van je kaart")
                    card_status = st.radio("Is je kaart aangevraagd of al actief?", 
                                         ["Nog niet begonnen", "Aangevraagd", "Actief & Gekoppeld"],
                                         horizontal=True,
                                         key=f"card_status_{step['id']}")
                    
                    if card_status in ["Aangevraagd", "Actief & Gekoppeld"]:
                        st.success("Lekker bezig! Je bent nu financieel klaar om je shop te lanceren.")
                        st.session_state[usage_key] = True
                    else:
                        st.session_state[usage_key] = False
                # --- STANDAARD CONTENT TYPES (TEXT, NICHE, ETC) ---
                elif step.get('content') == "TEXT_ONLY":
                    st.info(step['text'])
                    st.session_state[usage_key] = True
                
                elif step.get('content') == "TOOL_NICHE_FINDER":
                    # 1. DE COACH TIP
                    st.markdown("""
                    <div style="background-color: #F0F9FF; border-left: 5px solid #0EA5E9; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                        <p style="margin: 0; font-weight: bold; color: #0369A1;">💡 Coach Tip voor Starters</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #0C4A6E;">
                            Een <b>niche</b> is simpelweg een specifieke groep mensen met een gezamenlijk probleem of passie. 
                            Vul hieronder in wat je leuk vindt (bijv. 'honden', 'auto's' of 'koken'). De AI zoekt daar passende 'winners' bij.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    niche_input = st.text_input("Waar liggen je interesses?", placeholder="bijv. interieur, baby's, sport...", key=f"niche_in_{step['id']}")
                    
                    if st.button("🚀 Zoek mijn winnende niche", key=f"nbtn_{step['id']}", use_container_width=True):
                        if niche_input:
                            with st.spinner("Onze AI scant huidige trends..."):
                                results = ai_coach.find_real_winning_products(niche_input)
                                if results:
                                    st.session_state[f"results_{step['id']}"] = results
                                    st.session_state[usage_key] = True
                                else:
                                    st.error("Kon geen resultaten ophalen. Probeer een ander woord.")
                        else:
                            st.warning("Vul eerst een interesse in!")

                    # Toon de resultaten als ze er zijn
                    if f"results_{step['id']}" in st.session_state:
                        st.markdown("### 💎 Jouw Potentiële Winners")
                        for item in st.session_state[f"results_{step['id']}"]:
                            with st.container(border=True):
                                c1, c2 = st.columns([2, 1])
                                c1.markdown(f"#### {item['title']}")
                                c2.markdown(f"<div style='text-align:right; color:#16A34A; font-weight:bold;'>Schatting: €{item['price']}</div>", unsafe_allow_html=True)
                                
                                st.markdown(f"**🎥 Viral Hook:** *{item['hook']}*")
                                
                                # WAAROM DIT WERKT (Marketing Hoek)
                                st.markdown(f"""
                                <div style="background-color: #F0FDF4; padding: 10px; border-radius: 6px; border: 1px solid #BBF7D0; margin-top: 10px;">
                                    <span style="font-size: 0.85rem; color: #166534;"><b>💪 Waarom dit werkt:</b> {item['why_works']}</span>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.link_button(f"Bekijk {item['title']} op TikTok", item['search_links']['tiktok'], use_container_width=True)

                        # 3. DE BESLISSING (Dwingt de starter tot actie)
                        st.markdown("---")
                        st.markdown("### 🏁 Maak je keuze")
                        final_choice = st.text_input("Welke niche of welk product heb je gekozen?", placeholder="Typ hier je keuze...", key=f"final_choice_{step['id']}")
                        
                        if final_choice:
                            st.success(f"Geweldig! **{final_choice}** wordt jouw focus. Klik nu op de knop hieronder om deze fase af te ronden.")
                            # We slaan de keuze op in de session state zodat de knop onderaan geactiveerd wordt
                            st.session_state[usage_key] = True
                        else:
                            st.info("Vul je definitieve keuze hierboven in om door te gaan naar de volgende stap.")
                            st.session_state[usage_key] = False

                elif step.get('content') == "TOOL_DOMAIN_CHECK":
                    # --- 1. PREMIUM HEADER ---
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); border: 1px solid #E2E8F0; padding: 25px; border-radius: 16px; margin-bottom: 25px;">
                        <h3 style="margin-top: 0; color: #1E293B; font-size: 1.2rem; display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 1.5rem;">🏢</span> Jouw Unieke Adres (Vastgoed)
                        </h3>
                        <p style="font-size: 0.95rem; color: #475569; line-height: 1.5;">
                            Dit is hoe klanten je winkel onthouden. Een sterke naam volgt de <b>3-seconden regel</b>: 
                            Binnen 3 seconden moet een klant je naam kunnen <b>begrijpen, spellen en onthouden</b> zonder na te denken.
                        </p>
                        <div style="display: flex; gap: 15px; margin-top: 15px; flex-wrap: wrap;">
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #CBD5E1; color: #64748B;">✅ Geen streepjes</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #CBD5E1; color: #64748B;">✅ Max 3 woorden</span>
                            <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #CBD5E1; color: #64748B;">✅ .nl of .com</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # --- 2. AI GENERATOR (UITGELIJD) ---
                    st.markdown("#### 💡 Hulp nodig bij het verzinnen van een domeinnaam?")
                    
                    # Haal de eerder gekozen niche op voor context
                    niche_context = st.session_state.get("final_choice_step_niche", "Vul hier in waar je webshop over gaat...")
                    
                    # De FIX voor de gelijke hoogte: vertical_alignment="bottom"
                    col_gen1, col_gen2 = st.columns([2.5, 1], vertical_alignment="bottom")
                    
                    brand_input = col_gen1.text_input(
                        "Waar gaat je webshop over?", 
                        value=niche_context,
                        placeholder="bijv. yoga, honden, gadgets...", 
                        key=f"domain_prompt_{step['id']}"
                    )
                    
                    if col_gen2.button("Genereer Namen ✨", key=f"gbtn_{step['id']}", use_container_width=True, type="primary"):
                        with st.spinner("AI bedenkt sterke merknamen..."):
                            prompt = f"Bedenk 10 korte, krachtige en catchy domeinnamen (zonder streepjes) voor een webshop in de niche: {brand_input}. Geef alleen de namen gescheiden door komma's, geen nummers."
                            suggestions_raw = ai_coach.call_llm("Brand Name Expert", prompt)
                            if suggestions_raw:
                                # We splitsen de tekst op komma's voor de visuele tags
                                st.session_state[f"domain_list_{step['id']}"] = [s.strip() for s in suggestions_raw.split(',')]

                    # --- 3. PREMIUM SUGGESTIES WEERGAVE ---
                    if f"domain_list_{step['id']}" in st.session_state:
                        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                        cols = st.columns(2)
                        for i, name in enumerate(st.session_state[f"domain_list_{step['id']}"]):
                            with cols[i % 2]:
                                st.markdown(f"""
                                <div style="background: white; border: 1px solid #E2E8F0; padding: 10px 15px; border-radius: 10px; margin-bottom: 8px; font-weight: 600; color: #2563EB; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                                    {name.lower()}
                                </div>
                                """, unsafe_allow_html=True)

                    st.markdown("---")

                    # --- 4. CHECK SECTIE ---
                    st.markdown("#### 🔍 Check Beschikbaarheid")
                    st.write("Controleer of je favoriete naam nog vrij is.")
                    
                    st.link_button("👉 Check beschikbaarheid op TransIP", "https://www.transip.nl", use_container_width=True)
                    
                    st.markdown("""
                    <div style="background-color: #FFF7ED; border: 1px solid #FED7AA; padding: 12px; border-radius: 10px; margin-top: 15px;">
                        <p style="margin: 0; color: #9A3412; font-size: 0.85rem; font-weight: 600;">
                            ⚠️ Belangrijk: Koop alleen het domein. Geen e-mail of hosting pakketten; dat regelen we later goedkoper via Shopify.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    # --- 5. BEVESTIGING ---
                    st.markdown("<br>", unsafe_allow_html=True)
                    chosen_domain = st.text_input("Welke domeinnaam heb je vastgelegd?", placeholder="bijv. www.jouwshop.nl", key=f"final_domain_{step['id']}")
                    
                    if chosen_domain and "." in chosen_domain:
                        st.success(f"🎉 **{chosen_domain}** is nu jouw eigendom!")
                        st.session_state[usage_key] = True
                    else:
                        st.session_state[usage_key] = False

                elif step.get('content') == "TOOL_SHOPIFY_GUIDE":
                    # --- 1. PREMIUM HEADER (NU MET WITTE TEKST VOOR LEESBAARHEID) ---
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #004C3F 0%, #008060 100%); border: 1px solid #002E25; padding: 25px; border-radius: 16px; margin-bottom: 25px; color: white;">
                        <h3 style="margin-top: 0; color: #FFFFFF !important; font-size: 1.25rem; display: flex; align-items: center; gap: 10px; font-weight: 700;">
                            <span style="font-size: 1.5rem;">🛍️</span> Je Winkelvloer Inrichten
                        </h3>
                        <p style="font-size: 1rem; color: #F0FDF4 !important; line-height: 1.5; margin-bottom: 15px;">
                            Shopify is het brein van je webshop. Via deze link krijg je een exclusieve starters-deal: <b>de eerste 3 maanden voor slechts €1 per maand.</b>
                        </p>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                            <span style="background: rgba(255,255,255,0.15); padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.3); color: white !important; font-weight: 600;">✅ Geen techniek nodig</span>
                            <span style="background: rgba(255,255,255,0.15); padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.3); color: white !important; font-weight: 600;">✅ €1/maand deal</span>
                            <span style="background: rgba(255,255,255,0.15); padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.3); color: white !important; font-weight: 600;">✅ Altijd opzegbaar</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # --- 2. STAPPENPLAN (BEGRIJPELIJK VOOR STARTERS) ---
                    st.markdown("#### 📝 Hoe pak je de €1 deal?")
                    st.markdown("""
                    Volg exact deze stappen om fouten te voorkomen:
                    1. **Klik op de knop** hieronder (opent in een nieuw venster).
                    2. Vul je e-mailadres in en kies **'Gratis starten'**.
                    3. Shopify stelt een paar vragen, je mag overal op **'Overslaan'** drukken.
                    4. Zodra je in je dashboard bent, kies je het **'Basis' plan**. Geen zorgen: de eerste 3 maanden betaal je slechts €1.
                    """)

                    # --- 3. DE ACTIE KNOP ---
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.link_button("🚀 Claim mijn €1 Shopify Deal", "https://www.shopify.com/nl/gratis-proef?term=shopify%20account%20aanmaken&adid=701863738970&campaignid=21369992074&branded_enterprise=1&BOID=brand&utm_medium=cpc&utm_source=google&gad_source=1&gad_campaignid=21369992074&gbraid=0AAAAAC3Mv89BeCV7AwsovoynLOajGIMt7&gclid=EAIaIQobChMI_97Byez3kQMVkpGDBx2sWymYEAAYASAAEgI0NPD_BwE", use_container_width=True, type="primary")
                    
                    # --- 4. BESPAARTIP (VISUEEL STERKER) ---
                    st.markdown("""
                    <div style="background-color: #F0FDF4; border: 1px solid #BBF7D0; padding: 15px; border-radius: 12px; margin-top: 20px;">
                        <p style="margin: 0; color: #166534; font-size: 0.9rem; font-weight: 700;">
                            💡 Bespaar-advies:
                        </p>
                        <p style="margin: 5px 0 0 0; color: #166534; font-size: 0.85rem;">
                            Kies <u>niet</u> voor de duurdere 'Shopify' of 'Advanced' opties. Het <b>Basic plan</b> heeft alles wat je nodig hebt om je eerste €10.000 omzet te draaien.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("---")
                    
                    # --- 5. BEVESTIGING ---
                    st.markdown("#### ✅ Registreer je winkel")
                    st.write("Om je voortgang bij te houden, hebben we je winkel-adres nodig.")
                    
                    shop_url = st.text_input("Wat is de naam van je shop?", placeholder="bijv. jouwshopnaam.myshopify.com", key=f"shop_url_input_{step['id']}")
                    
                    if shop_url:
                        # Automatisch ".myshopify.com" toevoegen als de gebruiker het vergeet
                        if ".myshopify.com" not in shop_url and "." not in shop_url:
                            shop_url = f"{shop_url}.myshopify.com"
                            st.info(f"We hebben je adres aangevuld naar: **{shop_url}**")

                        if ".myshopify.com" in shop_url:
                            st.success(f"Perfect! Je shop **{shop_url}** is succesvol gekoppeld aan de Academy.")
                            st.session_state.shop_url = shop_url
                            st.session_state[usage_key] = True
                        else:
                            st.error("Gebruik het adres dat eindigt op .myshopify.com")
                            st.session_state[usage_key] = False
                    else:
                        st.session_state[usage_key] = False
              
                elif step.get('content') == "TOOL_SUPPLIER_HUB":
                    st.info("""**🏆 De RM Private Agent (Aanbevolen)**
                    Exclusief voor studenten. Verpletter de concurrentie met:
                    - 🚀 **7-10 dagen levertijd** (NL/BE)
                    - 📦 **Custom Branding** (Je eigen logo op pakketjes)
                    - 🔍 **Handmatige kwaliteitscontrole** per order""")
                    
                    st.caption(disclaimer_text)
                    
                    s1, s2, s3 = st.columns(3)
                    with s1:
                        st.markdown("**1. RM Private Agent**")
                        if not is_pro:
                            # Gebruik st.link_button om direct naar de URL te gaan
                            st.link_button("🔒 Unlock Agent", STRATEGY_CALL_URL, use_container_width=True)
                        else:
                            # Voor studenten/pro leden kun je dit zo laten of een andere link geven
                            st.button("👉 Contact Coach", use_container_width=True)
                            
                    with s2:
                        st.markdown("**2. DSers**")
                        st.link_button("AliExpress", "https://www.dsers.com", use_container_width=True)
                        
                    with s3:
                        st.markdown("**3. CJ Dropshipping**")
                        st.link_button("CJ Web", "https://cjdropshipping.com", use_container_width=True)
                        
                    st.markdown("---")
                    if st.checkbox("Ik heb een leverancier gekoppeld", key=f"supp_{step['id']}"): 
                        st.session_state[usage_key] = True
                # Ruimte boven de knop
                st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                
                if not is_completed:
                    if st.session_state.get(usage_key, False):
                        if st.button(f"✅ Taak Voltooien (+{step['xp_reward']} XP)", key=f"finish_{step['id']}", type="primary", use_container_width=True):
                            return step['id'], step['xp_reward']
                    else:
                        st.button("Voer eerst de opdracht uit", disabled=True, use_container_width=True, key=f"dis_{step['id']}")
        
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

    return None, 0