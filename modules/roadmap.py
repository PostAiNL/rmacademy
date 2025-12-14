import streamlit as st
import time
import pandas as pd
from io import BytesIO
from modules import ai_coach

# HIER STAAT DE URL VOOR DE KNOP
STRATEGY_CALL_URL = "https://calendly.com/rmecomacademy/30min"
COMMUNITY_URL = "https://discord.com"

def get_roadmap():
    return {
        "fase_1": {
            "title": "Fase 1: De Fundering",
            "desc": "Zonder fundering stort je huis in. Regel de administratie en je adres op het web.", 
            "steps": [
                {
                    "id": "step_kvk", "title": "KVK inschrijving", "icon": "📝", "locked": False,
                    "content": "TOOL_KVK_GUIDE", "xp_reward": 100, 
                    "video_url": "https://rmacademy.huddlecommunity.com/module/kvk-inschrijven"
                },
                {
                    "id": "step_niche", "title": "Kies je Niche", "icon": "🎯", "locked": False,
                    "content": "TOOL_NICHE_FINDER", "xp_reward": 100,
                    "teaser": "Weet je niet wat je moet verkopen? Gebruik de Niche Finder."
                },
                {
                    "id": "step_bank", "title": "Bank & creditcard", "icon": "💳", "locked": False,
                    "content": "TOOL_BANK_WIZARD", "xp_reward": 75,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/financieel"
                },
                {
                    "id": "step_domain", "title": "Domeinnaam claimen", "icon": "🌐", "locked": False,
                    "content": "TOOL_DOMAIN_CHECK", "xp_reward": 50,
                    "teaser": "Check of je naam nog vrij is als .nl of .com"
                }
            ]
        },
        "fase_2": {
            "title": "Fase 2: De Winkel Bouwen", 
            "desc": "Zet de techniek en het design klaar voor je eerste bezoekers.",
            "steps": [
                {
                    "id": "step_shopify_setup", "title": "Shopify account", "icon": "🛍️", "locked": False,
                    "content": "TOOL_SHOPIFY_GUIDE", "xp_reward": 150,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/shopify-setup"
                },
                {
                    "id": "step_theme", "title": "Thema & Vormgeving", "icon": "🎨", "locked": False,
                    "content": "TOOL_THEME_GUIDE", "xp_reward": 100,
                    "teaser": "Kies een conversie-gericht thema. Studenten krijgen een Premium Thema t.w.v. €350."
                },
                {
                    "id": "step_payments", "title": "Kassa instellen (Betalingen)", "icon": "💶", "locked": False,
                    "content": "TOOL_PAYMENTS", "xp_reward": 125,
                    "teaser": "Kies hoe klanten betalen: Mollie, Stripe of Shopify Payments."
                },
                {
                    "id": "step_logo_maker", "title": "Logo ontwerp (AI)", "icon": "✨", "locked": False,
                    "content": "TOOL_LOGO_MAKER", "xp_reward": 100,
                    "teaser": "Ontwerp je eigen professionele logo in seconden."
                }
            ]
        },
        "fase_3": {
            "title": "Fase 3: Producten & Logistiek",
            "desc": "Wat ga je verkopen en hoe komt het bij de klant?",
            "steps": [
                {
                    "id": "step_supplier", "title": "Leverancier koppelen", "icon": "📦", "locked": False,
                    "content": "TOOL_SUPPLIER_HUB", "xp_reward": 100,
                    "teaser": "Gebruik onze gratis Private Agent voor snelle levertijden (5-8 dagen)."
                },
                {
                    "id": "step_pricing", "title": "Winst calculator", "icon": "🧮", "locked": False,
                    "content": "TOOL_PROFIT_CALC", "xp_reward": 75,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/pricing"
                },
                {
                    "id": "step_legal", "title": "Juridische pagina's", "icon": "⚖️", "locked": False, 
                    "content": "TOOL_LEGAL_GEN", "xp_reward": 50,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/legal"
                }
            ]
        },
        "fase_4": {
            "title": "Fase 4: Vertrouwen & Conversie",
            "desc": "Maak je shop klaar voor bezoekers en zorg dat ze kopen.",
            "steps": [
                {
                    "id": "step_about_us", "title": "'Over ons' pagina", "icon": "✍️", "locked": False, 
                    "content": "TOOL_ABOUT_US", "xp_reward": 100,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/copywriting"
                },
                {
                    "id": "step_reviews", "title": "Reviews & Trustpilot", "icon": "⭐", "locked": False,
                    "content": "TOOL_REVIEWS", "xp_reward": 100,
                    "teaser": "Genereer eigen reviews, importeer uit China of start met Trustpilot."
                },
                {
                    "id": "step_pixels", "title": "Pixels & Tracking", "icon": "🎯", "locked": False,
                    "content": "TOOL_PIXELS", "xp_reward": 125,
                    "teaser": "Installeer de TikTok & Meta pixel, anders gooi je geld weg."
                },
                {
                    "id": "step_email", "title": "Email Geld Machine", "icon": "📧", "locked": False,
                    "content": "TOOL_EMAIL_GEN", "xp_reward": 150,
                    "teaser": "Zet automatische mails aan die geld verdienen terwijl je slaapt."
                }
            ]
        },
        "fase_5": {
            "title": "Fase 5: Marketing & Opschalen",
            "desc": "Je winkel is klaar. Tijd om bezoekers te kopen en winst te maken.",
            "steps": [
                {
                    "id": "step_preflight", "title": "De 'Eerste Sale' Checklist", "icon": "🛫", "locked": False,
                    "content": "TOOL_PREFLIGHT", "xp_reward": 100,
                    "teaser": "Voorkom dat je geld weggooit. Check dit voordat je Ads aanzet."
                },
                {
                    "id": "step_winning_prod", "title": "Winnende Producten", "icon": "🔥", "locked": True,
                    "content": "TOOL_PRODUCT_SPY", "xp_reward": 200,
                    "teaser": "Gebruik de Spy Tool om bewezen bestsellers te vinden."
                },
                {
                    "id": "step_ads_script", "title": "Viral Video Scripts", "icon": "🎬", "locked": True,
                    "content": "TOOL_VIDEO_SCRIPTS", "xp_reward": 200,
                    "teaser": "Laat AI scripts schrijven die viraal gaan op TikTok."
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

    # --- LOCKED STATE (FIXED: HTML FLATTENED) ---
    if is_locked:
        teaser_text = step.get('teaser', 'Upgrade voor toegang.')
        # Alles op 1 regel of compacte strings om markdown code blocks te voorkomen
        lock_html = f"""
        <div style="position: relative; overflow: hidden; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); background: #F8FAFC;">
            <div style="filter: blur(5px); opacity: 0.5; padding: 20px; pointer-events: none; user-select: none;">
                <h3 style="color: #64748B;">██████ ██████</h3>
                <p style="color: #94A3B8;">█████ ████ ██████ ███ ████. ████ ██████ ██ █████.</p>
                <div style="display:flex; gap:10px; margin-top:10px;"><div style="height: 100px; background: #E2E8F0; width: 30%; border-radius: 8px;"></div><div style="height: 100px; background: #E2E8F0; width: 30%; border-radius: 8px;"></div><div style="height: 100px; background: #E2E8F0; width: 30%; border-radius: 8px;"></div></div>
            </div>
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(255,255,255,0.4); backdrop-filter: blur(4px);">
                <div style="background: white; padding: 20px 30px; border-radius: 16px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 1px solid #DBEAFE; max-width: 90%;">
                    <div style="font-size: 28px; margin-bottom: 5px;">🔒</div>
                    <h4 style="margin: 0; color: #1E293B; font-size: 1rem; font-weight: 700;">Student Only Tool</h4>
                    <p style="font-size: 0.85rem; color: #64748B; margin: 5px 0 15px 0;">{teaser_text}</p>
                    <a href="{STRATEGY_CALL_URL}" target="_blank" style="text-decoration: none;"><div style="background: linear-gradient(135deg, #2563EB, #1D4ED8); color: white; padding: 10px 20px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; transition: transform 0.1s; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);">🚀 Unlock via Shop Review Call</div></a>
                    <div style="margin-top: 8px; font-size: 0.7rem; color: #94A3B8;"><i class="bi bi-people-fill"></i> Al door 550+ studenten gebruikt</div>
                </div>
            </div>
        </div>
        """
        st.markdown(lock_html, unsafe_allow_html=True)
        return None, 0

    # --- OPEN STATE ---
    with st.expander("Open opdracht & tools", expanded=expanded):
        
        if step.get('video_url'):
            if is_pro:
                st.markdown(f"""<a href="{step['video_url']}" target="_blank" style="text-decoration:none;"><div style="margin-bottom: 20px; padding: 12px; background: #EFF6FF; border-radius: 10px; border: 1px solid #DBEAFE; display: flex; align-items: center; gap: 10px; transition: background 0.2s;"><span style="color: #1E40AF; font-weight: 600; font-size: 0.9rem;">Bekijk de video instructie</span><span style="margin-left:auto; color:#2563EB;">&rarr;</span></div></a>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="margin-bottom: 20px; padding: 12px; background: #F8FAFC; border-radius: 10px; border: 1px dashed #CBD5E1; display: flex; align-items: center; gap: 10px; opacity: 0.7;"><span style="color: #64748B; font-weight: 600; font-size: 0.9rem;">Video instructie (Student only)</span><span style="margin-left:auto;">🔒</span></div>""", unsafe_allow_html=True)

        if step['content'] == "TOOL_KVK_GUIDE":
            st.info("💡 Tip: Maak eerst een afspraak, het is vaak druk!")
            st.link_button("📅 Ga naar KVK.nl", "https://www.kvk.nl", use_container_width=True)
            if st.checkbox("✅ Ik heb mijn afspraak/inschrijving geregeld"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_NICHE_FINDER":
            st.write("Weet je niet wat je moet verkopen? Vul in wat je leuk vindt.")
            interest = st.text_input("Jouw interesses (bv. fitness, honden, gadgets, koken)")
            if st.button("🔍 Vind mijn niche"):
                st.session_state[usage_key] = True
                st.markdown("### 💡 Suggesties voor jou:")
                st.info(f"Gebaseerd op '{interest}' zou je dit kunnen proberen:")
                st.markdown("""
                1.  **Probleem-oplosser:** Een product dat een irritatie wegneemt binnen jouw interesse.
                2.  **Passie-product:** Iets wat mensen *trots* maakt (bv. bedrukte items).
                3.  **Viral Gadget:** Iets wat er cool uitziet op TikTok.
                """)
                st.success("Kies één richting en ga door naar fase 2!")

        elif step['content'] == "TOOL_BANK_WIZARD":
            c1, c2 = st.columns(2)
            c1.link_button("Knab (Bank)", "https://knab.nl", use_container_width=True)
            c2.link_button("N26 (Creditcard)", "https://n26.com", use_container_width=True)
            if st.checkbox("✅ Ik heb dit geregeld"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_DOMAIN_CHECK":
            st.write("Een goede naam is kort en makkelijk te spellen.")
            st.link_button("🔎 Check beschikbaarheid (TransIP)", "https://www.transip.nl", use_container_width=True)
            if st.checkbox("✅ Ik heb mijn domein vastgelegd"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_SHOPIFY_GUIDE":
            st.info("💰 **Actie:** Eerste 3 maanden voor €1/maand.")
            st.link_button("🚀 Claim €1 Shopify deal", "https://shopify.com", type="primary", use_container_width=True)
            if st.checkbox("✅ Account aangemaakt"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_THEME_GUIDE":
            st.write("Een goede winkel ziet er betrouwbaar uit. Begin niet te moeilijk.")
            
            tab_basic, tab_colors, tab_pro_theme = st.tabs(["🚀 Gratis Starten", "🧠 Kleuren Tips", "💎 Premium Thema"])
            
            with tab_basic:
                st.info("💡 **Advies voor beginners:** Gebruik het gratis **'Dawn'** of **'Sense'** thema in Shopify.")
                st.markdown("""
                **De Gouden Regels voor Design:**
                1.  **Less is More:** Witruimte is luxe. Prop het niet vol.
                2.  **Hoge kwaliteit foto's:** Geen korrelige plaatjes.
                3.  **Duidelijke knoppen:** Zorg dat de 'Koop Nu' knop opvalt.
                """)
                st.link_button("Naar Shopify Theme Store", "https://themes.shopify.com", use_container_width=True)

            with tab_colors:
                st.write("**Kleuren bepalen je verkoop.** Kies 1 hoofdkleur en 1 accentkleur.")
                c1, c2 = st.columns(2)
                with c1:
                    st.success("🔵 **Blauw:** Vertrouwen, veiligheid (Bol.com, Coolblue)")
                    st.error("🔴 **Rood:** Actie, urgentie, uitverkoop (MediaMarkt)")
                with c2:
                    st.warning("🟡 **Geel/Goud:** Goedkoop of Luxe (Jumbo of Rolex)")
                    st.info("⚫ **Zwart/Wit:** Modern, strak, fashion (Zara, Nike)")

            with tab_pro_theme:
                st.markdown("### 🎁 Uniek Studenten Voordeel")
                st.write("Een goed converterend 'Premium Thema' kost normaal **$350 - $500**.")
                
                if is_pro:
                    st.success("✅ **Jij krijgt dit GRATIS!**")
                    st.write("Omdat je student bent, mag je ons RM High-Converter theme gebruiken.")
                    st.link_button("📥 Download Premium Theme", COMMUNITY_URL, type="primary", use_container_width=True)
                else:
                    st.warning("🔒 **Alleen voor studenten**")
                    st.write("Bespaar direct honderden euro's en start met een voorsprong.")
                    st.link_button("🚀 Word Student & Claim Thema", STRATEGY_CALL_URL, type="primary", use_container_width=True)

            st.markdown("---")
            if st.checkbox("✅ Ik heb mijn thema en kleuren ingesteld"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_PAYMENTS":
            st.write("Om geld te ontvangen, moet je een 'Payment Provider' koppelen. Kies er één:")
            tab_mol, tab_shop, tab_stripe = st.tabs(["Mollie (NL/BE)", "Shopify Payments", "Stripe (Int)"])
            with tab_mol:
                st.info("ℹ️ **Beste voor Nederland & België** (iDEAL + Bancontact).")
                st.link_button("Maak Mollie account", "https://www.mollie.com", use_container_width=True)
            with tab_shop:
                st.info("⚡ **Snelste optie.** Geen apart account nodig.")
                st.caption("Ga in Shopify naar Instellingen > Payments.")
            with tab_stripe:
                st.info("🌍 **Beste voor internationaal** (Creditcards + Apple Pay).")
                st.link_button("Maak Stripe account", "https://stripe.com", use_container_width=True)
            st.markdown("---")
            if st.checkbox("✅ Ik heb een betaalmethode geactiveerd"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_LOGO_MAKER":
            with st.form(key=f"logo_{step['id']}"):
                brand_name = st.text_input("Bedrijfsnaam")
                niche = st.text_input("Niche")
                if st.form_submit_button("✨ Maak logo"):
                    if brand_name:
                        with st.spinner("Genereren..."):
                            st.session_state[result_key] = ai_coach.generate_logo(brand_name, niche, "Modern", "Black")
                            st.session_state[usage_key] = True
            if result_key in st.session_state:
                st.image(st.session_state[result_key])
                st.success("Gedaan!")

        elif step['content'] == "TOOL_SUPPLIER_HUB":
            st.write("Stop met AliExpress. Voor serieus resultaat heb je een **Private Agent** nodig.")
            if is_pro:
                st.success("🎉 **Je bent student!** Je hebt gratis toegang tot onze Private Agent.")
                st.markdown("Klik hieronder om direct contact op te nemen via onze community.")
                st.link_button("📲 Chat met onze Agent (Discord)", COMMUNITY_URL, type="primary", use_container_width=True)
            else:
                st.warning("⚠️ **Let op:** AliExpress is traag en onbetrouwbaar voor serieuze shops.")
                st.info("💎 **Studenten Deal:** Word student en krijg direct toegang tot onze snelle Private Agent.")
                st.link_button("📞 Plan call & Claim Agent", STRATEGY_CALL_URL, type="primary", use_container_width=True)
            st.markdown("---")
            if st.checkbox("✅ Ik heb mijn leverancier geregeld"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_PROFIT_CALC":
            with st.form(key=f"calc_{step['id']}"):
                p = st.number_input("Verkoopprijs", 30.0)
                c = st.number_input("Inkoop", 10.0)
                if st.form_submit_button("Bereken"):
                    st.session_state[usage_key] = True
                    st.session_state[result_key] = p - c
            if result_key in st.session_state: st.metric("Winst", f"€{st.session_state[result_key]}")

        elif step['content'] == "TOOL_LEGAL_GEN":
            with st.form(key=f"legal_{step['id']}"):
                name = st.text_input("Bedrijfsnaam")
                if st.form_submit_button("Genereer"):
                    st.session_state[usage_key] = True
                    st.session_state[result_key] = "Done"
            if result_key in st.session_state: st.success("Teksten klaar!")

        elif step['content'] == "TOOL_ABOUT_US":
            with st.form(key=f"about_{step['id']}"):
                name = st.text_input("Naam")
                if st.form_submit_button("Schrijf"):
                    st.session_state[usage_key] = True
                    st.session_state[result_key] = ai_coach.generate_about_us(name, "General")
            if result_key in st.session_state: st.text_area("Tekst", st.session_state[result_key])

        elif step['content'] == "TOOL_REVIEWS":
            st.write("Reviews zorgen voor vertrouwen. Zonder reviews koopt niemand.")
            tab_create, tab_imp, tab_trust = st.tabs(["✨ Zelf Maken (AI)", "📥 Importeren", "⭐ Trustpilot"])
            
            with tab_create:
                st.info("💎 **Pro Tip:** Genereer 5-10 realistische Nederlandse reviews.")
                with st.form(key=f"rev_gen_{step['id']}"):
                    prod_name = st.text_input("Productnaam")
                    vibe = st.selectbox("Vibe", ["Enthousiast", "Kort", "Zakelijk"])
                    if st.form_submit_button("🚀 Genereer CSV"):
                        # Dummy data generation logic
                        st.session_state[result_key] = "title,body,rating\nGreat,Love it,5"
                        st.session_state[usage_key] = True
                if result_key in st.session_state:
                    st.success("Gegenereerd!")
                    st.download_button("Download CSV", st.session_state[result_key], "reviews.csv")

            with tab_imp:
                st.write("Gebruik Judge.me voor import.")
                st.link_button("📦 Installeer Judge.me", "https://apps.shopify.com/judgeme", use_container_width=True)

            with tab_trust:
                st.link_button("✅ Maak Trustpilot Account", "https://business.trustpilot.com", use_container_width=True)

            st.markdown("---")
            if st.checkbox("✅ Ik heb reviews"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_PIXELS":
            st.write("Een Pixel is een 'spion' die bijhoudt wie wat koopt. Zonder dit kun je niet winstgevend adverteren.")
            
            st.info("💡 **Goed nieuws:** Je hoeft GEEN code aan te raken. We gebruiken de officiële Shopify koppelingen.")
            
            tab_tiktok, tab_meta, tab_check = st.tabs(["📱 TikTok Pixel", "📘 Meta (FB) Pixel", "✅ Check of het werkt"])
            
            with tab_tiktok:
                st.write("**De makkelijkste methode:**")
                st.markdown("""
                1. Installeer de officiële **TikTok** app in Shopify.
                2. Klik op 'Connect' en log in op je TikTok for Business account.
                3. Kies bij 'Data Sharing' voor **'Maximum'**.
                """)
                st.link_button("📦 Installeer TikTok App (Shopify)", "https://apps.shopify.com/tiktok", use_container_width=True)
            
            with tab_meta:
                st.write("**Verbind Instagram & Facebook:**")
                st.markdown("""
                1. Installeer de officiële **Facebook & Instagram** app.
                2. Koppel je Facebook Pagina en Ad Account.
                3. Zet 'Data Sharing' op **'Maximum'** (belangrijk voor iOS14+).
                """)
                st.link_button("📦 Installeer Meta App (Shopify)", "https://apps.shopify.com/facebook", use_container_width=True)
            
            with tab_check:
                st.write("Wil je zeker weten dat het werkt?")
                st.markdown("""
                Installeer deze gratis Chrome Extensies. Als je daarna je eigen site bezoekt, moeten de icoontjes oplichten.
                *   🔵 **Meta Pixel Helper**
                *   ⚫ **TikTok Pixel Helper**
                """)
                st.caption("Zie je groene vinkjes? Dan ben je klaar!")

            st.markdown("---")
            if st.checkbox("✅ Mijn pixels zijn gekoppeld en actief"): st.session_state[usage_key] = True


        elif step['content'] == "TOOL_EMAIL_GEN":
            st.markdown("""
            **Email Marketing is geen optie, het is noodzaak.** 
            De meeste beginners focussen alleen op Ads, maar 30% van je omzet moet uit email komen (gratis omzet).
            """)

            tab_strat, tab_gen, tab_pro_tool = st.tabs(["📚 Strategie & Flows", "✍️ AI Email Schrijver", "🎁 Student Tool (Gratis)"])

            with tab_strat:
                st.info("💡 **De 3 'Must-Have' Automations (Flows):**")
                st.markdown("""
                1.  **Welcome Series:** Voor nieuwe inschrijvers (Nieuwsbrief). Geef direct je kortingscode.
                2.  **Abandoned Checkout:** Iemand klikt op betalen maar stopt. Stuur na 1 uur en na 10 uur een herinnering.
                3.  **Post-Purchase:** Bedank de klant, vraag om een review en bied korting voor de volgende keer.
                """)
                st.markdown("**Aanbevolen Software:**")
                c1, c2 = st.columns(2)
                c1.link_button("Shopify Email (Gratis start)", "https://apps.shopify.com/shopify-email", use_container_width=True)
                c2.link_button("Klaviyo (Voor Pro's)", "https://www.klaviyo.com", use_container_width=True)

            with tab_gen:
                st.write("Laat AI je emails schrijven zodat je ze direct kunt kopiëren.")
                email_type = st.selectbox("Welke mail wil je schrijven?", ["Verlaten Winkelwagen", "Welkomstmail", "Review Verzoek"])
                
                with st.form(key=f"mail_{step['id']}"):
                    col_a, col_b = st.columns(2)
                    with col_a: prod = st.text_input("Productnaam")
                    with col_b: discount = st.text_input("Korting code", "WELKOM10")
                    
                    if st.form_submit_button("✍️ Genereer Email Script"):
                        st.session_state[usage_key] = True
                        if "Winkelwagen" in email_type:
                            st.session_state[result_key] = f"**Onderwerp: Je bent je {prod} vergeten! 😲**\n\nHoi,\n\nWe zagen dat je bijna klaar was, maar je bent weggegaan zonder af te rekenen.\nGebruik code **{discount}** voor korting!"
                        elif "Welkomstmail" in email_type:
                             st.session_state[result_key] = f"**Onderwerp: Welkom! Hier is je cadeautje 🎁**\n\nHoi topper,\n\nBedankt voor je interesse in {prod}.\nZoals beloofd: **{discount}**."
                        else:
                             st.session_state[result_key] = f"**Onderwerp: Wat vond je ervan? ⭐**\n\nHoi,\n\nHeb je {prod} al uitgepakt? We horen graag je mening!"
                
                if result_key in st.session_state:
                    st.success("Gegenereerd! Kopieer dit naar je email app.")
                    st.code(st.session_state[result_key], language="markdown")

            with tab_pro_tool:
                st.markdown("### 🚀 RM Auto-Pilot (AI)")
                st.write("Als student krijg je toegang tot onze exclusieve tool die **automatisch** koppelt met je Shopify store.")
                if is_pro:
                    st.success("✅ **Jij hebt toegang!**")
                    st.link_button("📥 Download Templates & Start Bot", COMMUNITY_URL, type="primary", use_container_width=True)
                else:
                    st.warning("🔒 **Alleen voor studenten**")
                    st.write("Stop met handmatig typen. Krijg onze 'One-Click-Import' templates.")
                    st.link_button("🔓 Unlock Studenten Tools", STRATEGY_CALL_URL, use_container_width=True)

            st.markdown("---")
            if st.checkbox("✅ Ik heb mijn automatische mails ingesteld"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_PREFLIGHT":
            st.write("Gooi geen geld weg aan ads als je winkel niet werkt. Check dit:")
            with st.container(border=True):
                c1 = st.checkbox("💳 Ik heb zelf een testbestelling gedaan (belangrijk!)")
                c2 = st.checkbox("🚚 Verzendkosten worden correct berekend in de checkout")
                c3 = st.checkbox("🇬🇧 Er staan geen gekke Engelse teksten meer op de site")
                c4 = st.checkbox("📱 De site ziet er goed uit op mobiel")
                
                if c1 and c2 and c3 and c4:
                    st.success("✅ Je bent er klaar voor! Op naar de sales.")
                    st.session_state[usage_key] = True
                else:
                    st.info("Vink alles af om door te gaan.")

        elif step['content'] == "TOOL_PRODUCT_SPY":
            st.write("Ga naar 'Product Ideeën' in het menu.")
            if st.checkbox("✅ Gedaan"): st.session_state[usage_key] = True
        
        elif step['content'] == "TOOL_VIDEO_SCRIPTS":
            st.write("Ga naar 'Video Ideeën' in het menu.")
            if st.checkbox("✅ Gedaan"): st.session_state[usage_key] = True

        st.markdown("<br>", unsafe_allow_html=True)
        if not is_completed:
            if st.session_state.get(usage_key, False):
                if st.button(f"🎉 Afronden (+{step['xp_reward']} XP)", key=f"btn_{step['id']}", type="primary", use_container_width=True):
                    return step['id'], step['xp_reward']
            else:
                st.button("Afronden", disabled=True, key=f"dis_{step['id']}", use_container_width=True)

    return None, 0