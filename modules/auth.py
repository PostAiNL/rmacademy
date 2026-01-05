import streamlit as st
import random
import string
import time
import smtplib
import os  # NIEUW: Nodig voor Render environment variables
from datetime import datetime, timezone, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from supabase import create_client

# --- CONFIGURATIE ---
APP_URL = "https://rmacademy.onrender.com" 

RANKS = {
    0: "🐣 Starter",
    200: "🔨 Bouwer",
    500: "🚀 Expert",       
    1000: "👑 E-com Boss",
    3000: "💎 Legend",
    5000: "🔥 Master",
    10000: "🦄 Grandmaster"
}

# CONNECTIE MET SUPABASE (Verbeterd voor Render)
@st.cache_resource
def init_supabase():
    try:
        # Check eerst Render Environment Variables, dan pas st.secrets
        url = os.environ.get("SUPABASE_URL") or st.secrets.get("supabase", {}).get("url")
        key = os.environ.get("SUPABASE_KEY") or st.secrets.get("supabase", {}).get("key")
        
        if not url or not key:
            st.error("Supabase URL of Key ontbreekt in de instellingen!")
            return None
            
        return create_client(url, key)
    except Exception as e:
        st.error(f"Supabase Connectie Fout: {e}")
        return None

supabase = init_supabase()

# --- HULPFUNCTIE: BEPAAL RANG ---
def get_rank_info(xp):
    current_title = "🐣 Starter"
    next_xp = 200
    sorted_ranks = sorted(RANKS.items())
    for i, (threshold, title) in enumerate(sorted_ranks):
        if xp >= threshold:
            current_title = title
            if i + 1 < len(sorted_ranks):
                next_xp = sorted_ranks[i+1][0]
            else:
                next_xp = threshold * 2
        else:
            break
    return current_title, next_xp

# --- DATA OPHALEN VOOR LEADERBOARD ---
def get_leaderboard_data():
    if not supabase: return []
    try:
        response = supabase.table('users').select('email, first_name, xp, level, is_pro').order('xp', desc=True).limit(10).execute()
        leaderboard = []
        for i, u in enumerate(response.data):
            display_name = u.get('first_name') or u['email'].split('@')[0].capitalize()
            title, _ = get_rank_info(u['xp'])
            leaderboard.append({
                "rank": i + 1,
                "name": display_name,
                "xp": u['xp'],
                "title": title,
                "is_pro": u['is_pro']
            })
        return leaderboard
    except: return []

# --- LOGIN / REGISTER ---
def login_or_register(email, license_input=None, ref_code_input=None, name_input=None):
    email = email.lower().strip()
    user = None
    if supabase:
        try:
            res = supabase.table('users').select("*").eq('email', email).execute()
            if res.data: user = res.data[0]
        except Exception as e:
            st.error(f"Inloggen mislukt: {e}")

    if not user:
         st.session_state.user = {
            "id": "temp",
            "email": email,
            "first_name": name_input or "Gast",
            "xp": 0, "level": 1, "is_pro": False, "referral_code": "TEMP"
         }
         return

    st.session_state.user = user
    st.session_state.is_pro = user.get('is_pro', False)
    st.toast("Succesvol ingelogd!", icon="🚀")

def get_progress():
    if "user" not in st.session_state or not supabase: return []
    try:
        if st.session_state.user['id'] == 'temp': return []
        res = supabase.table('progress').select("step_id").eq('user_id', st.session_state.user['id']).execute()
        return [r['step_id'] for r in res.data]
    except: return []

def mark_step_complete(step_id, xp_reward):
    if "user" not in st.session_state: return
    
    # Live voortgang opslaan
    if st.session_state.user['id'] == 'temp':
        st.session_state.user['xp'] += xp_reward
        return

    uid = st.session_state.user['id']
    if not supabase: return

    try:
        # 1. Check of stap al in DB staat
        check = supabase.table('progress').select('*').eq('user_id', uid).eq('step_id', step_id).execute()
        if check.data: 
            return 

        # 2. Voeg toe aan progress tabel
        supabase.table('progress').insert({"user_id": uid, "step_id": step_id}).execute()
        
        # 3. Bereken nieuwe XP en Level
        current_xp = st.session_state.user.get('xp', 0)
        new_xp = current_xp + xp_reward
        
        # Bereken level nummer (1, 2, 3, etc)
        sorted_ranks = sorted(RANKS.items())
        new_level = 1
        for i, (threshold, title) in enumerate(sorted_ranks):
            if new_xp >= threshold:
                new_level = i + 1
            else:
                break
        
        old_title, _ = get_rank_info(current_xp)
        new_title, _ = get_rank_info(new_xp)
        
        # 4. Update de users tabel (XP ÉN LEVEL)
        res_user = supabase.table('users').update({
            "xp": new_xp, 
            "level": new_level
        }).eq('id', uid).execute()

        if res_user.data:
            st.session_state.user['xp'] = new_xp
            st.session_state.user['level'] = new_level
            
            if new_title != old_title:
                st.balloons()
                st.success(f"🏆 Promotie naar {new_title}!")
             
    except Exception as e:
        st.error(f"Fout bij opslaan: {e}")

def get_affiliate_stats():
    if "user" not in st.session_state or st.session_state.user['id'] == 'temp' or not supabase: 
        return 0, 0, 0
    try:
        res = supabase.table('users').select("is_pro").eq('referred_by', st.session_state.user['id']).execute()
        total = len(res.data)
        pro = sum(1 for u in res.data if u['is_pro'])
        return total, pro, pro * 250
    except: return 0, 0, 0