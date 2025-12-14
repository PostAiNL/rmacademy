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
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        except:
            client = None

def call_llm(system_prompt, user_prompt, model="gpt-4o-mini", json_mode=False):
    init_ai()
    if not HAS_OPENAI or not client: return None
    try:
        kwargs = {
            "model": model, 
            "messages": [{"role": "system", "content": system_prompt},{"role": "user", "content": user_prompt}], 
            "temperature": 0.7
        }
        if json_mode: kwargs["response_format"] = { "type": "json_object" }
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except: return None

# --- NIEUW: FEEDBACK VALIDATOR ---
def validate_feedback(text):
    """Checkt of feedback nuttig is."""
    init_ai()
    if not HAS_OPENAI or not client: return True 
    
    prompt = f"""
    Beoordeel deze feedback voor een app. Is het serieuze tekst (NL/EN)?
    Antwoord TRUE als het een echte zin is.
    Antwoord FALSE als het spam is (zoals 'asdf', 'test', 'bla bla', of te kort).
    
    Feedback: "{text}"
    """
    res = call_llm("Je bent een spam filter. Antwoord alleen TRUE of FALSE.", prompt)
    if res and "TRUE" in res.upper(): return True
    return False

# --- BESTAANDE FUNCTIES (NIET VERWIJDEREN) ---
def generate_product_description(product_name):
    prompt = f"Schrijf een AIDA productbeschrijving (NL) voor: {product_name}."
    return call_llm("Copywriter", prompt) or "AI niet beschikbaar."

def generate_influencer_dm(product_name):
    prompt = f"Schrijf een casual Instagram DM (NL) om een influencer te benaderen voor: {product_name}."
    return call_llm("Marketeer", prompt) or "AI niet beschikbaar."

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
    prompt = f"Schrijf een 'Over Ons' tekst voor webshop '{brand_name}' ({niche}). Max 100 woorden. Betrouwbaar."
    return call_llm("Je bent een Storytelling Expert.", prompt) or "Fout."

def generate_viral_scripts(product, benefits, platform="TikTok"):
    prompt = f"""Schrijf een viral {platform} script voor: '{product}'. Output JSON: {{ "hooks": ["..."], "full_script": "...", "creator_brief": "..." }}"""
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