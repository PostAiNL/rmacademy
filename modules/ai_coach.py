import streamlit as st
import json
import warnings

# Warnings onderdrukken
warnings.simplefilter("ignore")

# Proberen OpenAI te laden
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Proberen DuckDuckGo te laden (voor product finder)
try:
    from duckduckgo_search import DDGS
except: pass

client = None

def init_ai():
    """Maakt de verbinding met OpenAI klaar."""
    global client
    # Alleen verbinden als we de library hebben én de secret key
    if HAS_OPENAI and "OPENAI_API_KEY" in st.secrets:
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        except Exception as e:
            print(f"Init Error: {e}")
            client = None

def call_llm(system_prompt, user_prompt, model="gpt-4o-mini", json_mode=False):
    """Stuurt een bericht naar de AI en geeft tekst terug."""
    init_ai() # <--- CRUCIALE FIX: Altijd eerst verbinden!
    
    if not HAS_OPENAI or not client: 
        return None
        
    try:
        kwargs = {
            "model": model, 
            "messages": [{"role": "system", "content": system_prompt},{"role": "user", "content": user_prompt}], 
            "temperature": 0.7
        }
        if json_mode: kwargs["response_format"] = { "type": "json_object" }
        
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except Exception as e: 
        print(f"AI Call Error: {e}")
        return None

# --- 1. PRODUCT FINDER (FALLBACK & LIVE) ---
def generate_fallback_products(niche):
    return [{"original_title": f"Viral {niche} Gadget", "image_url": "https://via.placeholder.com/300", "price": 29.95, "cost": 8.00, "hook": "Wow factor!"}]

def find_real_winning_products(niche, filter_type="Viral"):
    # (Ingekorte versie voor overzicht, voeg je DDGS logica hier toe indien nodig)
    return generate_fallback_products(niche)

# --- 2. BRANDING TOOLS (GEFIXT) ---

def generate_brand_names(niche, vibe):
    init_ai()
    
    # Fallback (Als AI stuk is)
    if not HAS_OPENAI or not client: 
        n = niche.replace(" ", "").capitalize()
        return [
            {"name": f"{n}HQ", "slogan": f"De nummer 1 in {niche}."},
            {"name": f"The{n}Club", "slogan": "Exclusief voor liefhebbers."},
            {"name": f"Nova{n}", "slogan": "De nieuwe standaard."},
            {"name": f"Purely{n}", "slogan": "Puur kwaliteit."},
            {"name": f"{vibe}{n}", "slogan": f"{vibe} en vertrouwd."}
        ]
    
    # De Nieuwe Prompt (Vraagt om Naam EN Slogan)
    prompt = f"""
    Verzin 5 unieke webshop concepten voor de niche: '{niche}'. 
    Vibe: '{vibe}'.
    
    Voor elk concept wil ik:
    1. Een pakkende naam (max 2 woorden).
    2. Een korte, krachtige slogan (Nederlands).
    
    Output JSON formaat: 
    {{ "suggestions": [ {{"name": "Naam1", "slogan": "Slogan1"}}, {{"name": "Naam2", "slogan": "Slogan2"}} ] }}
    """
    
    res = call_llm("Je bent een Senior Branding Expert.", prompt, json_mode=True)
    
    if res:
        try: return json.loads(res).get('suggestions', [])
        except: pass
        
    return [] # Leeg als het faalt

def generate_slogan(brand_name, niche):
    init_ai() # <--- FIX
    if not HAS_OPENAI or not client: return f"{brand_name}: De beste keuze voor {niche}."
    
    prompt = f"Verzin een korte, krachtige Nederlandse slogan voor webshop '{brand_name}' in niche '{niche}'. Max 6 woorden. Geen aanhalingstekens."
    return call_llm("Je bent een top Copywriter.", prompt) or "Kwaliteit voorop."

def generate_about_us(brand_name, niche):
    init_ai() # <--- FIX
    if not HAS_OPENAI or not client: return f"Welkom bij {brand_name}. Wij zijn experts in {niche}!"
    
    prompt = f"""
    Schrijf een betrouwbare 'Over Ons' tekst voor webshop '{brand_name}' die producten verkoopt in: {niche}.
    
    Structuur:
    1. Het probleem (waarom we bestaan).
    2. Onze passie/oplossing.
    3. Onze belofte (klanttevredenheid).
    
    Toon: Persoonlijk, warm en professioneel. Gebruik ongeveer 120 woorden.
    """
    return call_llm("Je bent een Storytelling Expert.", prompt) or "Tekst kon niet gegenereerd worden."