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
                
               # --- LOGO & HUISSTIJL ---
                if step.get('content') == "TOOL_THEME_GUIDE":
                    st.write("Je logo en huisstijl bepalen de uitstraling van je merk. Gebruik onze ingebouwde AI of kies voor een externe tool.")
                    st.info("⭐ **Onze aanbeveling: De RM AI Logo Maker.** Je vindt deze tool in het zijmenu onder **'Marketing & Design'**. Hiermee genereer je binnen 10 seconden een  professioneel logo dat direct klaar is voor gebruik. Dit is de snelste en meest kosteneffectieve optie voor onze cursisten.")
                    st.caption(disclaimer_text)
                    l1, l2, l3 = st.columns(3)
                    with l1:
                        st.markdown("**1. RM AI Logo Maker**")
                        st.markdown("*(Aanbevolen: Zie menu)*")
                        # DE FIX: Knop die de navigatie aanpast
                        if st.button("👉 Ga naar 'Marketing & Design'", key="go_to_marketing_btn", use_container_width=True):
                            st.session_state.nav_index = 3  # Index 3 is 'Marketing & Design'
                            st.rerun()
                    with l2:
                        st.markdown("**2. Canva (Huisstijl)**")
                        st.link_button("Start Canva", "https://www.canva.com", use_container_width=True)
                    with l3:
                        st.markdown("**3. Looka (AI Alternatief)**")
                        st.link_button("Start Looka", "https://looka.com", use_container_width=True)
                    if st.checkbox("Logo en huisstijl zijn klaar", key=f"theme_{step['id']}"): st.session_state[usage_key] = True
                # --- BETALINGEN INSTELLEN ---
                elif step.get('content') == "TOOL_PAYMENTS":
                    st.write("Zorg dat je klanten veilig kunnen betalen via iDEAL, Bancontact en Creditcard.")
                    st.info("⭐ **Onze aanbeveling: Mollie.** Veruit de beste ervaringen voor de Nederlandse en Belgische markt. Snelle uitbetalingen en top-tier support.")
                    st.caption(disclaimer_text)
                    p1, p2, p3 = st.columns(3)
                    with p1:
                        st.markdown("**1. Mollie (Aangeraden)**")
                        st.link_button("Open Mollie", "https://www.mollie.com/nl", use_container_width=True)
                    with p2:
                        st.markdown("**2. Shopify Payments**")
                        st.link_button("Activeer in Shopify", "https://www.shopify.com", use_container_width=True)
                    with p3:
                        st.markdown("**3. Stripe**")
                        st.link_button("Open Stripe", "https://stripe.com/nl", use_container_width=True)
                    if st.checkbox("Betaalmethodes gekoppeld", key=f"pay_{step['id']}"): st.session_state[usage_key] = True

                # --- ZAKELIJKE REKENING ---
                elif step.get('content') == "TOOL_BANK_WIZARD":
                    st.write("Houd zakelijk en privé strikt gescheiden vanaf dag één.")
                    st.info("⭐ **Onze aanbeveling: Knab.** De favoriet onder e-commerce ondernemers. Het koppelt moeiteloos met je webshop en boekhouding.")
                    st.caption(disclaimer_text)
                    b1, b2, b3 = st.columns(3)
                    with b1:
                        st.markdown("**1. Knab (Aangeraden)**")
                        st.link_button("Open Knab", "https://www.knab.nl/zakelijk", use_container_width=True)
                    with b2:
                        st.markdown("**2. Bunq**")
                        st.link_button("Open Bunq", "https://www.bunq.com", use_container_width=True)
                    with b3:
                        st.markdown("**3. Revolut Business**")
                        st.link_button("Open Revolut", "https://www.revolut.com", use_container_width=True)
                    if st.checkbox("Bankrekening aangevraagd", key=f"bank_{step['id']}"): st.session_state[usage_key] = True

                # --- CREDITCARD ---
                elif step.get('content') == "TOOL_CREDITCARD_WIZARD":
                    st.write("Noodzakelijk voor het betalen van je advertentiekosten en Shopify-abonnement.")
                    st.info("⭐ **Onze aanbeveling: N26.** Onze studenten hebben hier de minste problemen; de kaart is vaak binnen enkele minuten al virtueel te gebruiken.")
                    st.caption(disclaimer_text)
                    cc1, cc2, cc3 = st.columns(3)
                    with cc1:
                        st.markdown("**1. N26 (Aangeraden)**")
                        st.link_button("Vraag N26 aan", "https://n26.com", use_container_width=True)
                    with cc2:
                        st.markdown("**2. Revolut**")
                        st.link_button("Vraag Revolut aan", "https://www.revolut.com", use_container_width=True)
                    with cc3:
                        st.markdown("**3. Bunq Card**")
                        st.link_button("Vraag Bunq aan", "https://www.bunq.com", use_container_width=True)
                    if st.checkbox("Creditcard aangevraagd", key=f"cc_{step['id']}"): st.session_state[usage_key] = True

                # --- STANDAARD CONTENT TYPES (TEXT, NICHE, ETC) ---
                elif step.get('content') == "TEXT_ONLY":
                    st.info(step['text'])
                    st.session_state[usage_key] = True
                
                elif step.get('content') == "TOOL_NICHE_FINDER":
                    st.write("Gebruik AI om een gat in de markt te vinden.")
                    st.text_input("Wat zijn je hobby's?", key=f"niche_in_{step['id']}")
                    if st.button("Genereer Ideeën", key=f"nbtn_{step['id']}"):
                        st.session_state[usage_key] = True
                        st.success("1. Huisdier accessoires | 2. Smart home | 3. Duurzame mode")

                elif step.get('content') == "TOOL_DOMAIN_CHECK":
                    st.write("Check of je droom-domeinnaam nog beschikbaar is.")
                    st.link_button("Check op TransIP", "https://www.transip.nl", use_container_width=True)
                    if st.checkbox("Domein is geregistreerd", key=f"c_{step['id']}"): st.session_state[usage_key] = True

                elif step.get('content') == "TOOL_SHOPIFY_GUIDE":
                    st.write("Gebruik de officiële link voor de €1 actie.")
                    st.link_button("Claim Shopify €1 Deal", "https://www.shopify.com", use_container_width=True)
                    if st.checkbox("Shopify geactiveerd", key=f"shop_{step['id']}"): st.session_state[usage_key] = True

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