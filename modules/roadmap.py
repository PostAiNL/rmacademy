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