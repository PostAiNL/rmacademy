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
    init_ai()
    
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

# --- IN ai_coach.py ---

def find_real_winning_products(niche, filter_type="Viral"):
    """
    Genereert concepten en zoekopdrachten in plaats van fake data.
    """
    init_ai()
    
    # Directe links voor de gebruiker om ZELF te kijken (dit is veel waardevoller)
    tiktok_url = f"https://www.tiktok.com/search?q={niche.replace(' ', '+')}+must+have"
    aliexpress_url = f"https://www.aliexpress.com/wholesale?SearchText={niche.replace(' ', '+')}+gadget&SortType=total_tranpro_desc"
    
    if not HAS_OPENAI or not client: 
        # Fallback zonder AI
        return [{
            "title": f"Viral {niche} Concept", 
            "price": 29.95, 
            "hook": "De AI kan nu even geen concepten bedenken, maar gebruik de knoppen hieronder om live te zoeken.",
            "search_links": {"tiktok": tiktok_url, "ali": aliexpress_url}
        }]

    prompt = f"""
    Ik ben een beginner in dropshipping. Geef mij 3 unieke, 'viral-waardige' productideeën voor de niche: '{niche}'.
    Verzin geen bestaande merken, maar beschrijf het soort product.
    
    Voor elk product wil ik:
    1. Een pakkende productnaam.
    2. Een realistische verkoopprijs (tussen 20 en 60 euro).
    3. Eén zin waarom dit 'viral' zou kunnen gaan (de 'Wow-factor').
    
    Output JSON: {{ "suggestions": [ {{"title": "Naam", "price": 29.95, "hook": "Uitleg"}} ] }}
    """
    
    res = call_llm("Je bent een E-commerce Product Researcher.", prompt, json_mode=True)
    
    results = []
    if res:
        try: 
            data = json.loads(res).get('suggestions', [])
            for item in data:
                # Voeg de zoeklinks toe aan elk AI resultaat
                item["search_links"] = {"tiktok": tiktok_url, "ali": aliexpress_url}
                results.append(item)
        except: pass
        
    return results

# --- 2. BRANDING TOOLS ---

def generate_brand_names(niche, vibe):
    init_ai()
    
    if not HAS_OPENAI or not client: 
        n = niche.replace(" ", "").capitalize()
        return [
            {"name": f"{n}HQ", "slogan": f"De nummer 1 in {niche}."},
            {"name": f"The{n}Club", "slogan": "Exclusief voor liefhebbers."},
            {"name": f"Nova{n}", "slogan": "De nieuwe standaard."},
            {"name": f"Purely{n}", "slogan": "Puur kwaliteit."},
            {"name": f"{vibe}{n}", "slogan": f"{vibe} en vertrouwd."}
        ]
    
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
        
    return [] 

def generate_slogan(brand_name, niche):
    init_ai()
    if not HAS_OPENAI or not client: return f"{brand_name}: De beste keuze voor {niche}."
    
    prompt = f"Verzin een korte, krachtige Nederlandse slogan voor webshop '{brand_name}' in niche '{niche}'. Max 6 woorden. Geen aanhalingstekens."
    return call_llm("Je bent een top Copywriter.", prompt) or "Kwaliteit voorop."

def generate_about_us(brand_name, niche):
    init_ai()
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

# --- 3. VIDEO TOOLS ---

def generate_viral_scripts(product, benefits, platform="TikTok"):
    init_ai()
    if not HAS_OPENAI or not client: 
        return {
            "hooks": ["Wacht tot je dit ziet!", "Dit verandert alles.", "Stop met scrollen!"],
            "full_script": "Demo script: Introductie, Probleem, Oplossing (Jouw Product), Call to Action.",
            "creator_brief": "Maak een video van 15-30 seconden. Goede belichting."
        }

    prompt = f"""
    Schrijf een viral {platform} script voor het product: '{product}'.
    Voordelen: {benefits}
    
    Ik wil JSON output met:
    1. 'hooks': Lijst met 3 scroll-stopping openingszinnen.
    2. 'full_script': Een volledig script met visuele instructies [tussen haken] en gesproken tekst.
    3. 'creator_brief': Korte instructie voor de content creator (UGC).
    """
    
    res = call_llm("Je bent een Viral Video Expert.", prompt, json_mode=True)
    if res:
        try: return json.loads(res)
        except: pass
        
    return {"hooks": [], "full_script": "", "creator_brief": ""}

# --- 4. LOGO GENERATOR (100% FLAT VECTOR FIX) ---

def generate_logo(brand_name, niche, style, colors):
    """Genereert een logo URL via DALL-E 3 - GEFORCEERD PLAT DESIGN."""
    init_ai()
    
    if not HAS_OPENAI or not client:
        return f"https://placehold.co/1024x1024/2563EB/FFFFFF/png?text={brand_name}+Logo"

    # We gebruiken een technische prompt die DALL-E dwingt om een "digitaal bestand" te maken
    # in plaats van een "foto van een product".
    prompt = f"""
    A single, centered, 2D vector graphic logo symbol for the brand '{brand_name}'.
    Style context: {style} ({niche}).
    Color palette: {colors}.
    
    CRITICAL VISUAL RULES:
    1. IMAGE TYPE: Flat Vector Art / Clip Art. NOT a photo.
    2. BACKGROUND: Pure white (#FFFFFF) void. No shadows on the background.
    3. CONTENT: Only the graphic symbol and the text '{brand_name}'.
    4. FORBIDDEN: Do NOT render bags, business cards, walls, 3D mockups, office supplies, or realistic textures.
    5. STYLE: Minimalist, clean lines, solid colors, flat design (like an App Icon).
    """

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        print(f"DALL-E Error: {e}")
        return None

# --- IN ai_coach.py ---

def validate_feedback(text):
    """Checkt of feedback nuttig/echt is."""
    init_ai()
    if not HAS_OPENAI or not client: return True # Fallback: altijd goedkeuren als AI uit staat
    
    prompt = f"""
    Beoordeel de volgende feedback van een gebruiker over een e-commerce app.
    Is dit serieuze, leesbare feedback (Nederlands of Engels)? 
    Of is het onzin/spam (zoals 'asdf', 'test', 'bla bla')?
    
    Feedback: "{text}"
    
    Antwoord ALLEEN met 'TRUE' (als het serieus is) of 'FALSE' (als het onzin is).
    """
    
    res = call_llm("Je bent een spam filter.", prompt)
    if res and "TRUE" in res.upper():
        return True
    return False