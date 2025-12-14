import streamlit as st
import json
import warnings

warnings.simplefilter("ignore")

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

client = None

def init_ai():
    global client
    if HAS_OPENAI and "OPENAI_API_KEY" in st.secrets:
        try: client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        except: client = None

def call_llm(system_prompt, user_prompt, model="gpt-4o-mini", json_mode=False):
    init_ai()
    if not HAS_OPENAI or not client: return None
    try:
        kwargs = {"model": model, "messages": [{"role": "system", "content": system_prompt},{"role": "user", "content": user_prompt}], "temperature": 0.7}
        if json_mode: kwargs["response_format"] = { "type": "json_object" }
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except: return None

# --- NIEUWE MARKETING FUNCTIES ---

def generate_product_description(product_name):
    init_ai()
    if not HAS_OPENAI or not client: 
        return f"**{product_name}**\n\nOntdek de magie van {product_name}. Dit product lost al je problemen op en ziet er geweldig uit. Bestel vandaag nog!"
    
    prompt = f"""
    Schrijf een onweerstaanbare productbeschrijving voor '{product_name}' volgens het AIDA model (Attention, Interest, Desire, Action).
    Taal: Nederlands.
    Stijl: Enthousiast en overtuigend.
    Opmaak: Gebruik Markdown (dikgedrukt, bulletpoints).
    """
    return call_llm("Je bent een expert copywriter.", prompt)

def generate_influencer_dm(product_name):
    init_ai()
    if not HAS_OPENAI or not client:
        return f"Hoi! Ik zag je profiel en vind je content te gek. We verkopen {product_name} en zouden graag samenwerken. Heb je interesse?"
    
    prompt = f"""
    Schrijf een kort, casual DM bericht om een Instagram influencer te benaderen voor een samenwerking.
    Product: {product_name}.
    Doel: Gratis product sturen in ruil voor een video.
    Toon: Casual, niet als een robot of sales-persoon.
    """
    return call_llm("Je bent een influencer marketing manager.", prompt)

def generate_legal_text(company_name):
    return f"""
    **PRIVACY BELEID {company_name.upper()}**
    
    Versie 1.0 - {company_name} respecteert de privacy van alle gebruikers van haar site en draagt er zorg voor dat de persoonlijke informatie die u ons verschaft vertrouwelijk wordt behandeld.
    
    **1. Gebruik van gegevens**
    Wij gebruiken uw gegevens om de bestellingen zo snel en gemakkelijk mogelijk te laten verlopen.
    
    **2. Derden**
    Wij zullen uw persoonlijke gegevens niet aan derden verkopen en zullen deze uitsluitend aan derden ter beschikking stellen die zijn betrokken bij het uitvoeren van uw bestelling.
    
    (Dit is een standaard template. Raadpleeg altijd een jurist voor volledige zekerheid.)
    """

# --- BESTAANDE FUNCTIES ---

def find_real_winning_products(niche, filter_type="Viral"):
    init_ai()
    tiktok_url = f"https://www.tiktok.com/search?q={niche.replace(' ', '+')}+must+have"
    aliexpress_url = f"https://www.aliexpress.com/wholesale?SearchText={niche.replace(' ', '+')}+gadget"
    
    if not HAS_OPENAI or not client: 
        return [{"title": f"Viral {niche} Concept", "price": 29.95, "hook": "Zoek live met de knoppen hieronder.", "search_links": {"tiktok": tiktok_url, "ali": aliexpress_url}}]

    prompt = f"""
    Geef 3 'viral-waardige' dropshipping productideeën voor niche: '{niche}'.
    Output JSON: {{ "suggestions": [ {{"title": "Naam", "price": 29.95, "hook": "Uitleg"}} ] }}
    """
    res = call_llm("Je bent een E-commerce Product Researcher.", prompt, json_mode=True)
    results = []
    if res:
        try: 
            data = json.loads(res).get('suggestions', [])
            for item in data:
                item["search_links"] = {"tiktok": tiktok_url, "ali": aliexpress_url}
                results.append(item)
        except: pass
    return results

def generate_about_us(brand_name, niche):
    init_ai()
    if not HAS_OPENAI or not client: return f"Welkom bij {brand_name}. Wij zijn experts in {niche}!"
    prompt = f"Schrijf een 'Over Ons' tekst voor webshop '{brand_name}' ({niche}). Max 100 woorden. Betrouwbaar."
    return call_llm("Je bent een Storytelling Expert.", prompt) or "Fout."

def generate_viral_scripts(product, benefits, platform="TikTok"):
    init_ai()
    if not HAS_OPENAI or not client: 
        return {"hooks": ["Stop scrolling!", "Dit moet je zien."], "full_script": "Demo script...", "creator_brief": "Maak een video."}

    prompt = f"""
    Schrijf een viral {platform} script voor: '{product}'.
    Output JSON: {{ "hooks": ["..."], "full_script": "...", "creator_brief": "..." }}
    """
    res = call_llm("Je bent een Viral Video Expert.", prompt, json_mode=True)
    if res:
        try: return json.loads(res)
        except: pass
    return {"hooks": [], "full_script": "", "creator_brief": ""}

def generate_logo(brand_name, niche, style, colors):
    init_ai()
    if not HAS_OPENAI or not client: return f"https://placehold.co/1024x1024/2563EB/FFFFFF/png?text={brand_name}"
    prompt = f"Flat vector logo symbol for '{brand_name}', style {style}, colors {colors}. Minimalist icon on white background."
    try:
        response = client.images.generate(model="dall-e-3", prompt=prompt, size="1024x1024", quality="standard", n=1)
        return response.data[0].url
    except: return None