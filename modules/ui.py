import streamlit as st

def inject_style_and_hacks(brand_color="#0ea5e9"):
    st.markdown(f"""
    <style>
        .stApp {{ background-color: #f8fafc; }}
        
        /* Card Styling */
        .nav-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }}
        .nav-card:hover {{
            transform: translateY(-2px);
            border-color: {brand_color};
        }}
        
        /* Buttons */
        button[kind="primary"] {{
            background-color: {brand_color} !important;
            border: none !important;
            color: white !important;
            font-weight: bold !important;
        }}
        
        /* Metrics */
        div[data-testid="stMetricValue"] {{
            font-size: 1.5rem !important;
            color: {brand_color} !important;
        }}
    </style>
    """, unsafe_allow_html=True)