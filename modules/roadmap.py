import streamlit as st
import time
import pandas as pd
from io import BytesIO
from modules import ai_coach

STRATEGY_CALL_URL = "https://calendly.com/rmecomacademy/30min"
COMMUNITY_URL = "https://discord.com"

def get_roadmap():
    return {
        "fase_1": {
            "title": "Fase 1: De Start",
            "desc": "Zonder fundering stort je huis in. Regel eerst de administratie en je adres op het web.", 
            "steps": [
                {
                    "id": "step_kvk", "title": "KVK Nummer Regelen", "icon": "", "locked": False,
                    "content": "TOOL_KVK_GUIDE", "xp_reward": 100, 
                    "video_url": "https://rmacademy.huddlecommunity.com/module/kvk-inschrijven"
                },
                {
                    "id": "step_niche", "title": "Wat ga je verkopen?", "icon": "", "locked": False,
                    "content": "TOOL_NICHE_FINDER", "xp_reward": 100,
                    "teaser": "Weet je niet wat je moet verkopen? Vraag de AI om hulp."
                },
                {
                    "id": "step_bank", "title": "Zakelijke Rekening", "icon": "", "locked": False,
                    "content": "TOOL_BANK_WIZARD", "xp_reward": 75,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/financieel"
                },
                {
                    "id": "step_domain", "title": "Domeinnaam Kiezen", "icon": "", "locked": False,
                    "content": "TOOL_DOMAIN_CHECK", "xp_reward": 50,
                    "teaser": "Check of je naam nog vrij is als .nl of .com"
                }
            ]
        },
        "fase_2": {
            "title": "Fase 2: Winkel Bouwen", 
            "desc": "Zet de techniek en het design klaar voor je eerste bezoekers.",
            "steps": [
                {
                    "id": "step_shopify_setup", "title": "Shopify Account Maken", "icon": "", "locked": False,
                    "content": "TOOL_SHOPIFY_GUIDE", "xp_reward": 150,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/shopify-setup"
                },
                {
                    "id": "step_theme", "title": "Logo & Huisstijl", "icon": "", "locked": False,
                    "content": "TOOL_THEME_GUIDE", "xp_reward": 100,
                    "teaser": "Kies een conversie-gericht thema. Studenten krijgen een Premium Thema t.w.v. €350."
                },
                {
                    "id": "step_payments", "title": "Betalingen Instellen", "icon": "", "locked": False,
                    "content": "TOOL_PAYMENTS", "xp_reward": 125,
                    "teaser": "Kies hoe klanten betalen: Mollie, Stripe of Shopify Payments."
                },
                {
                    "id": "step_legal_safe", "title": "Juridisch & Regels", "icon": "", "locked": False,
                    "content": "TOOL_LEGAL_SAFE_NEW", "xp_reward": 150,
                    "teaser": "Voorkom boetes. Genereer je Algemene Voorwaarden & Privacy Policy."
                }
            ]
        },
        "fase_3": {
            "title": "Fase 3: Producten",
            "desc": "Wat ga je verkopen en hoe komt het bij de klant?",
            "steps": [
                {
                    "id": "step_supplier", "title": "Leverancier Koppelen", "icon": "", "locked": False,
                    "content": "TOOL_SUPPLIER_HUB", "xp_reward": 100,
                    "teaser": "Gebruik onze gratis Private Agent voor snelle levertijden (5-8 dagen)."
                },
                {
                    "id": "step_pricing", "title": "Verkoopprijs Bepalen", "icon": "", "locked": False,
                    "content": "TOOL_PROFIT_CALC", "xp_reward": 75,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/pricing"
                }
            ]
        },
        "fase_4": {
            "title": "Fase 4: Klaar voor Bezoekers",
            "desc": "Maak je shop betrouwbaar zodat mensen durven te kopen.",
            "steps": [
                {
                    "id": "step_about_us", "title": "'Over ons' Pagina", "icon": "", "locked": False, 
                    "content": "TOOL_ABOUT_US", "xp_reward": 100,
                    "video_url": "https://rmacademy.huddlecommunity.com/module/copywriting"
                },
                {
                    "id": "step_reviews", "title": "Reviews Instellen", "icon": "", "locked": False,
                    "content": "TOOL_REVIEWS", "xp_reward": 100,
                    "teaser": "Genereer eigen reviews, importeer uit China of start met Trustpilot."
                },
                {
                    "id": "step_pixels", "title": "Bezoekers Meten (Pixels)", "icon": "", "locked": False,
                    "content": "TOOL_PIXELS", "xp_reward": 125,
                    "teaser": "Installeer de TikTok & Meta pixel, anders gooi je geld weg."
                },
                {
                    "id": "step_email", "title": "Automatische E-mails", "icon": "", "locked": False,
                    "content": "TOOL_EMAIL_GEN", "xp_reward": 150,
                    "teaser": "Zet automatische mails aan die geld verdienen terwijl je slaapt."
                }
            ]
        },
        "fase_5": {
            "title": "Fase 5: Je Eerste Sales",
            "desc": "Je winkel is klaar. Tijd om bezoekers te trekken en te verkopen.",
            "steps": [
                {
                    "id": "step_24h_live", "title": "Launch Checklist", "icon": "", "locked": False,
                    "content": "TOOL_24H_CHECK", "xp_reward": 150,
                    "teaser": "Je shop is live, wat nu? Check deze lijst om niks te vergeten."
                },
                {
                    "id": "step_winning_prod", "title": "Winnende Producten Kiezen", "icon": "🔥", "locked": True,
                    "content": "TOOL_PRODUCT_SPY", "xp_reward": 200,
                    "teaser": "Gebruik de Spy Tool om bewezen bestsellers te vinden."
                },
                {
                    "id": "step_influencer", "title": "Influencers Benaderen", "icon": "", "locked": False,
                    "content": "TOOL_INFLUENCER_OUTREACH", "xp_reward": 100,
                    "teaser": "Laat AI een bericht schrijven om influencers te benaderen."
                }
            ]
        },
        "fase_6": {
            "title": "Fase 6: Dagelijks Beheer",
            "desc": "De shop staat. Nu begint het echte werk: Testen, Analyseren en Winst pakken.",
            "steps": [
                {
                    "id": "step_testing_ads", "title": "Dag 1: Advertenties Starten", "icon": "", "locked": False,
                    "content": "TEXT_ONLY", "text": "Start met €20-€50 per dag. Test minimaal 3 verschillende video's. Zet alles uit wat na €15 geen 'Winkelwagen toevoeging' heeft.",
                    "xp_reward": 150
                },
                {
                    "id": "step_analysis", "title": "Dag 3: Resultaten Bekijken", "icon": "", "locked": False,
                    "content": "TEXT_ONLY", "text": "Kijk naar je CPC (onder €0.50?), CTR (boven 1%?) en ROAS. Slechte cijfers? Nieuwe video's maken. Goede cijfers? Budget verhogen.",
                    "xp_reward": 150
                },
                {
                    "id": "step_kill_scale", "title": "Dag 7: Doorgaan of Stoppen?", "icon": "", "locked": False,
                    "content": "TEXT_ONLY", "text": "Heb je winst? Schaal op (20% budget erbij per dag). Geen winst? Stop met dit product en begin opnieuw met Fase 3.",
                    "xp_reward": 200
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
        badge = "<span style='background:#EFF6FF; color:#2563EB; padding:4px 10px; border-radius:12px; font-size:0.75rem; font-weight:700; border:1px solid #DBEAFE;'>👇Start hieronder👇</span>"
        border_color = "#2563EB" if expanded else "#E2E8F0"
        bg_color = "#FFFFFF"

    is_locked = step['locked'] and not is_pro
    usage_key = f"tool_used_{step['id']}"
    
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
        lock_html = f"""
        <div style="position: relative; overflow: hidden; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); background: #F8FAFC;">
            <div style="filter: blur(5px); opacity: 0.5; padding: 20px; pointer-events: none; user-select: none;">
                <h3 style="color: #64748B;">██████ ██████</h3>
                <p style="color: #94A3B8;">█████ ████ ██████ ███ ████. ████ ██████ ██ █████.</p>
                <div style="display:flex; gap:10px; margin-top:10px;"><div style="height: 100px; background: #E2E8F0; width: 30%; border-radius: 8px;"></div><div style="height: 100px; background: #E2E8F0; width: 30%; border-radius: 8px;"></div></div>
            </div>
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(255,255,255,0.4); backdrop-filter: blur(4px);">
                <div style="background: white; padding: 20px 30px; border-radius: 16px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 1px solid #DBEAFE; max-width: 90%;">
                    <div style="font-size: 28px; margin-bottom: 5px;">🔒</div>
                    <h4 style="margin: 0; color: #1E293B; font-size: 1rem; font-weight: 700;">Student Only Tool</h4>
                    <p style="font-size: 0.85rem; color: #64748B; margin: 5px 0 15px 0;">{teaser_text}</p>
                    <a href="{STRATEGY_CALL_URL}" target="_blank" style="text-decoration: none;"><div style="background: linear-gradient(135deg, #2563EB, #1D4ED8); color: white; padding: 10px 20px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; transition: transform 0.1s; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);">🚀 Unlock via Shop Review Call</div></a>
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

        if step.get('content') == "TEXT_ONLY":
            st.info(step['text'])
            st.session_state[usage_key] = True

        elif step['content'] == "TOOL_KVK_GUIDE":
            st.info("💡 Tip: Maak eerst een afspraak, het is vaak druk bij de KVK!")
            st.link_button("📅 Ga naar KVK.nl", "https://www.kvk.nl/inschrijven/", use_container_width=True)
            if st.checkbox("✅ Ik heb mijn afspraak/inschrijving geregeld"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_NICHE_FINDER":
            st.write("Weet je niet wat je moet verkopen?")
            interest = st.text_input("Jouw interesses (bv. fitness, honden, gadgets, koken)")
            if st.button("🔍 Vraag AI om suggesties"):
                st.session_state[usage_key] = True
                if not interest: st.warning("Vul iets in!")
                else:
                    st.info(f"💡 Suggesties voor '{interest}':")
                    st.markdown("""
                    1.  **Probleem-oplosser:** Een product dat een irritatie wegneemt binnen jouw interesse.
                    2.  **Passie-product:** Iets wat mensen *trots* maakt (bv. bedrukte items).
                    3.  **Viral Gadget:** Iets wat er cool uitziet op TikTok.
                    """)
                    st.success("Kies één richting en ga door!")

        elif step['content'] == "TOOL_BANK_WIZARD":
            c1, c2 = st.columns(2)
            c1.link_button("Knab (Bank)", "https://knab.nl", use_container_width=True)
            c2.link_button("N26 (Creditcard)", "https://n26.com", use_container_width=True)
            if st.checkbox("✅ Ik heb dit geregeld"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_DOMAIN_CHECK":
            st.link_button("🔎 Check beschikbaarheid (TransIP)", "https://www.transip.nl", use_container_width=True)
            if st.checkbox("✅ Ik heb mijn domein vastgelegd"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_SHOPIFY_GUIDE":
            st.info("💰 **Actie:** Eerste 3 maanden voor €1/maand.")
            st.link_button("🚀 Claim €1 Shopify deal", "https://shopify.com", type="primary", use_container_width=True)
            if st.checkbox("✅ Account aangemaakt"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_THEME_GUIDE":
            tab_basic, tab_pro_theme = st.tabs(["🚀 Gratis Starten", "💎 Premium Thema"])
            with tab_basic:
                st.info("💡 **Advies:** Gebruik het gratis **'Dawn'** of **'Sense'** thema.")
                st.link_button("Naar Shopify Theme Store", "https://themes.shopify.com", use_container_width=True)
            with tab_pro_theme:
                if is_pro:
                    st.success("✅ **Jij krijgt dit GRATIS!**")
                    st.link_button("📥 Download Premium Theme", COMMUNITY_URL, type="primary", use_container_width=True)
                else:
                    st.warning("🔒 **Alleen voor studenten**")
                    st.link_button("🚀 Word Student", STRATEGY_CALL_URL, type="primary", use_container_width=True)
            if st.checkbox("✅ Ik heb mijn thema en kleuren ingesteld"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_PAYMENTS":
            st.link_button("Maak Mollie account (NL/BE)", "https://www.mollie.com", use_container_width=True)
            if st.checkbox("✅ Ik heb een betaalmethode geactiveerd"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_LEGAL_SAFE_NEW":
            st.write("**Voorkom boetes.** Genereer hier je teksten.")
            company_name = st.text_input("Bedrijfsnaam")
            email_contact = st.text_input("Contact Email")
            if st.button("📝 Genereer Juridische Teksten"):
                if company_name and email_contact:
                    res = ai_coach.generate_legal_text(company_name)
                    st.text_area("Kopieer dit naar je 'Privacy Policy' pagina:", res, height=200)
                    st.session_state[usage_key] = True
                else:
                    st.warning("Vul beide velden in.")

        elif step['content'] == "TOOL_SUPPLIER_HUB":
            if is_pro:
                st.success("🎉 **Je bent student!** Je hebt gratis toegang tot onze Private Agent.")
                st.link_button("📲 Chat met onze Agent (Discord)", COMMUNITY_URL, type="primary", use_container_width=True)
            else:
                st.info("💎 **Studenten Deal:** Krijg toegang tot onze snelle Private Agent.")
                st.link_button("📞 Plan call & Claim Agent", STRATEGY_CALL_URL, type="primary", use_container_width=True)
            if st.checkbox("✅ Ik heb mijn leverancier geregeld"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_PROFIT_CALC":
            p = st.number_input("Verkoopprijs", 30.0)
            c = st.number_input("Inkoop", 10.0)
            if st.button("Bereken Winst"):
                st.session_state[usage_key] = True
                st.metric("Winst", f"€{p-c}")

        elif step['content'] == "TOOL_ABOUT_US":
            name = st.text_input("Naam")
            if st.button("Schrijf 'Over Ons'"):
                st.session_state[usage_key] = True
                st.text_area("Tekst", ai_coach.generate_about_us(name, "General"))

        elif step['content'] == "TOOL_REVIEWS":
            st.link_button("📦 Installeer Judge.me", "https://apps.shopify.com/judgeme", use_container_width=True)
            if st.checkbox("✅ Ik heb reviews"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_PIXELS":
            st.info("Installeer de TikTok & Meta apps in Shopify en zet Data Sharing op 'Maximum'.")
            st.link_button("📦 Installeer Meta App", "https://apps.shopify.com/facebook", use_container_width=True)
            if st.checkbox("✅ Mijn pixels zijn gekoppeld"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_EMAIL_GEN":
            st.write("Laat AI je emails schrijven.")
            with st.form(key=f"mail_{step['id']}"):
                prod = st.text_input("Productnaam")
                if st.form_submit_button("✍️ Genereer Email Script"):
                    st.session_state[usage_key] = True
                    st.code(f"Onderwerp: Je bent je {prod} vergeten!\n\nHoi,\n\nWe zagen dat je bijna klaar was. Hier is 10% korting: WELKOM10", language="text")

        elif step['content'] == "TOOL_24H_CHECK":
            st.write("Je shop is live! Check dit direct:")
            c1 = st.checkbox("💳 Zelf een testbestelling gedaan")
            c2 = st.checkbox("📧 Bevestigingsmail ontvangen")
            c3 = st.checkbox("📱 Mobiele weergave gecheckt")
            if c1 and c2 and c3:
                st.success("✅ Gefeliciteerd! Je bent echt live.")
                st.session_state[usage_key] = True

        elif step['content'] == "TOOL_INFLUENCER_OUTREACH":
            st.write("Ga naar 'Marketing & Design' in het menu om dit te doen.")
            if st.checkbox("✅ Gedaan"): st.session_state[usage_key] = True

        elif step['content'] == "TOOL_PRODUCT_SPY":
            st.write("Ga naar 'Producten Zoeken' in het menu.")
            if st.checkbox("✅ Gedaan"): st.session_state[usage_key] = True

        st.markdown("<br>", unsafe_allow_html=True)
        if not is_completed:
            if st.session_state.get(usage_key, False):
                if st.button(f"🎉 Afronden (+{step['xp_reward']} XP)", key=f"btn_{step['id']}", type="primary", use_container_width=True):
                    return step['id'], step['xp_reward']
            else:
                st.button("Afronden", disabled=True, key=f"dis_{step['id']}", use_container_width=True)

    return None, 0