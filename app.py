import streamlit as st
import requests
from datetime import datetime
import base64
from pathlib import Path


# API

import os

API_KEY = os.getenv("AZURE_API_KEY")
FULL_API_URL = "https://cvprofilefoundry-test.cognitiveservices.azure.com/openai/deployments/gpt-4o-2024-08-06-CVProfiler-v1-3/chat/completions?api-version=2025-01-01-preview"

# SYSTEM PROMPT FOR FINE-TUNED MODEL
SYSTEM_PROMPT = """You are a Protocol Education recruitment specialist creating educator profiles. You have been trained on gold-standard CV-profile pairs.

When interview notes are provided alongside the CV, integrate both sources to create a compelling profile:

Use INTERVIEW NOTES for:
- Personality traits and teaching style
- Recent roles and current situation
- Specific examples and achievements
- What makes this educator stand out and appeal to schools

Use CV for:
- Formal qualifications and employment history
- Complete timeline and background context
- Verifiable facts and certifications

Blend both sources naturally to create a profile that shows competence AND personality. When interview notes mention recent information that differs from the CV, prioritize the interview insights as they are more current.

If only a CV is provided, create the profile as normal using your training."""


# PAGE CONFIGURATION

st.set_page_config(
    page_title="Protocol Education - CV Profile Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# LOAD LOGO

def load_logo():
    logo_path = Path("logo.webp")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
            return f"data:image/webp;base64,{logo_data}"
    return None

logo_base64 = load_logo()

# WEBSITE DESIGN

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    
    .main {{
        padding: 0 !important;
        background: #ffffff;
    }}
    
    .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}
    
    /* NAVIGATION BAR */
    .nav-bar {{
        background: #ffffff;
        padding: 1.25rem 3rem;
        border-bottom: 1px solid #e5e7eb;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    
    .logo-container {{
        max-width: 200px;
    }}
    
    /* HERO SECTION - STUNNING BLUE GRADIENT */
    .hero {{
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
        padding: 4rem 3rem 5rem 3rem;
        position: relative;
        overflow: hidden;
    }}
    
    .hero::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.4;
    }}
    
    .hero-content {{
        position: relative;
        z-index: 1;
        max-width: 1200px;
        margin: 0 auto;
        text-align: center;
    }}
    
    .hero-title {{
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }}
    
    .hero-subtitle {{
        font-size: 1.25rem;
        color: rgba(255,255,255,0.95);
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
    }}
    
    /* CONTENT CONTAINER */
    .content-wrapper {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 3rem 3rem 4rem 3rem;
    }}
    
    /* STEP BADGES */
    .step-badge {{
        display: inline-flex;
        align-items: center;
        background: #eff6ff;
        color: #1e40af;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
        margin-bottom: 1rem;
        letter-spacing: 0.025em;
    }}
    
    /* SECTION HEADERS */
    h2 {{
        color: #1e293b;
        font-size: 1.875rem;
        font-weight: 700;
        margin: 2rem 0 1.5rem 0;
        letter-spacing: -0.01em;
    }}
    
    h3 {{
        color: #334155;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
    }}
    
    /* BUTTONS - STUNNING DESIGN */
    .stButton>button {{
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.875rem 2rem;
        border: none;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3), 0 2px 4px -1px rgba(37, 99, 235, 0.2);
        transition: all 0.2s ease;
        cursor: pointer;
        letter-spacing: 0.025em;
    }}
    
    .stButton>button:hover {{
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4), 0 4px 6px -2px rgba(37, 99, 235, 0.3);
        transform: translateY(-2px);
    }}
    
    .stButton>button:active {{
        transform: translateY(0);
    }}
    
    /* TEXT AREAS - CLEAN & PROFESSIONAL */
    .stTextArea>div>div>textarea {{
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        font-size: 0.9375rem;
        line-height: 1.6;
        transition: all 0.2s ease;
        font-family: 'Inter', sans-serif;
    }}
    
    .stTextArea>div>div>textarea:focus {{
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        outline: none;
    }}
    
    .stTextArea>div>div>textarea::placeholder {{
        color: #9ca3af;
        font-weight: 400;
    }}
    
    /* PROFILE OUTPUT BOX - ELEGANT */
    .profile-output {{
        background: linear-gradient(to bottom, #f8fafc 0%, #ffffff 100%);
        border: 2px solid #3b82f6;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.1), 0 2px 4px -1px rgba(59, 130, 246, 0.06);
        position: relative;
    }}
    
    .profile-output::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
        border-radius: 12px 0 0 12px;
    }}
    
    .profile-text {{
        color: #1e293b;
        font-size: 1rem;
        line-height: 1.75;
        padding-left: 1rem;
    }}
    
    /* INFO BOXES */
    .stAlert {{
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        color: #1e40af;
    }}
    
    /* CHARACTER COUNTER */
    .char-counter {{
        text-align: right;
        font-size: 0.875rem;
        color: #64748b;
        margin-top: 0.5rem;
        font-weight: 500;
    }}
    
    /* SUCCESS BANNER */
    .success-banner {{
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.3);
    }}
    
    /* ITERATION BADGE */
    .iteration-badge {{
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(245, 158, 11, 0.3);
    }}
    
    /* SIDEBAR */
    .css-1d391kg, [data-testid="stSidebar"] {{
        background: #f8fafc;
        border-right: 1px solid #e5e7eb;
    }}
    
    [data-testid="stSidebar"] .stMetric {{
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        margin-bottom: 0.75rem;
    }}
    
    /* EXPANDER */
    .streamlit-expanderHeader {{
        background-color: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        font-weight: 500;
        color: #475569;
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: #f1f5f9;
    }}
    
    /* DIVIDER */
    hr {{
        margin: 2.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
    }}
    
    /* FOOTER */
    .footer {{
        background: #f8fafc;
        border-top: 1px solid #e5e7eb;
        padding: 2.5rem 3rem;
        text-align: center;
        color: #64748b;
        font-size: 0.875rem;
        margin-top: 4rem;
    }}
    
    .footer-title {{
        color: #1e293b;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }}
    
    /* LOADING SPINNER */
    .stSpinner > div {{
        border-top-color: #3b82f6 !important;
    }}
    
    /* REMOVE STREAMLIT BRANDING */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* RESPONSIVE */
    @media (max-width: 768px) {{
        .hero {{
            padding: 3rem 1.5rem;
        }}
        
        .hero-title {{
            font-size: 2rem;
        }}
        
        .content-wrapper {{
            padding: 2rem 1.5rem;
        }}
        
        .nav-bar {{
            padding: 1rem 1.5rem;
        }}
    }}
    </style>
""", unsafe_allow_html=True)


# INITIALISE SESSION STATE

if "current_profile" not in st.session_state:
    st.session_state.current_profile = ""
if "iteration_count" not in st.session_state:
    st.session_state.iteration_count = 0
if "history" not in st.session_state:
    st.session_state.history = []


# API FUNCTION

def call_fine_tuned_model(messages):
    headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    payload = {"messages": messages, "temperature": 0.7, "max_tokens": 2000}
    
    try:
        response = requests.post(FULL_API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API Error {response.status_code}: {response.text[:200]}"
    except Exception as e:
        return f"Error: {str(e)}"

# NAVIGATION

if logo_base64:
    st.markdown(f"""
        <div class="nav-bar">
            <img src="{logo_base64}" class="logo-container" alt="Protocol Education">
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="nav-bar"><div style="color:#ffffff; font-size:1.5rem; font-weight:700;">Protocol Education</div></div>', unsafe_allow_html=True)


# HERO SECTION

st.markdown("""
    <div class="hero">
        <div class="hero-content">
            <h1 class="hero-title">CV Profile Generator</h1>
            <p class="hero-subtitle">Transform educator CVs into compelling profiles with AI-powered precision</p>
        </div>
    </div>
""", unsafe_allow_html=True)


# MAIN CONTENT

st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# STEP 1
st.markdown('<div class="step-badge">STEP 1</div>', unsafe_allow_html=True)
st.markdown("## Paste CV Content")

cv_text = st.text_area(
    "CV Input",
    height=280,
    max_chars=20000,
    placeholder="Paste your your CV first and then your interview notes",
    key="cv_input",
    label_visibility="collapsed"
)

char_count = len(cv_text)
st.markdown(f'<div class="char-counter">{char_count:,} / 20,000 characters</div>', unsafe_allow_html=True)

# STEP 2
st.markdown("---")
st.markdown('<div class="step-badge">STEP 2</div>', unsafe_allow_html=True)
st.markdown("## Generate Profile")

generate_button = st.button("Generate Educator Profile", key="generate", type="primary")

if generate_button:
    if not cv_text.strip():
        st.error("Please paste a CV first")
    elif len(cv_text.strip()) < 50:
        st.error("CV text is too short - please paste more content")
    else:
        with st.spinner("Analyzing CV and generating profile..."):
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Create an educator profile from this CV:\n\n{cv_text}"}
            ]
            
            profile = call_fine_tuned_model(messages)
            
            if not profile.startswith("API Error") and not profile.startswith("Error"):
                st.session_state.current_profile = profile
                st.session_state.iteration_count = 0
                st.session_state.history = [{
                    "version": 1,
                    "type": "Initial",
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "content": profile
                }]
                st.markdown('<div class="success-banner">Profile Generated Successfully</div>', unsafe_allow_html=True)
                st.rerun()
            else:
                st.error(profile)

# STEP 3 - DISPLAY & REFINE
if st.session_state.current_profile:
    st.markdown("---")
    st.markdown('<div class="step-badge">STEP 3</div>', unsafe_allow_html=True)
    st.markdown("## Review & Refine")
    
    if st.session_state.iteration_count > 0:
        st.markdown(f'<div class="iteration-badge">{st.session_state.iteration_count} Refinement(s) Applied</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="profile-output"><div class="profile-text">{st.session_state.current_profile}</div></div>', unsafe_allow_html=True)
    
    with st.expander("View copyable text"):
        st.text_area("Profile Text", value=st.session_state.current_profile, height=200, label_visibility="collapsed")
    
    st.markdown("### Refine the Profile")
    st.info("Be specific about what you want to change - you can refine as many times as needed")

    
    refinement_request = st.text_area(
        "Refinement Request",
        height=100,
        placeholder="Example: Make it more engaging, add more about teaching philosophy, emphasize leadership experience",
        key="refinement_input",
        label_visibility="collapsed"
    )
    
    refine_button = st.button("Apply Refinement", key="refine", type="primary")
    
    if refine_button:
        if not refinement_request.strip():
            st.error("Please describe what you want to change")
        else:
            with st.spinner("Refining profile..."):
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Current profile:\n\n{st.session_state.current_profile}\n\nRefinement: {refinement_request}"}
                ]
                
                refined_profile = call_fine_tuned_model(messages)
                
                if not refined_profile.startswith("API Error") and not refined_profile.startswith("Error"):
                    st.session_state.iteration_count += 1
                    st.session_state.current_profile = refined_profile
                    st.session_state.history.append({
                        "version": len(st.session_state.history) + 1,
                        "type": "Refinement",
                        "request": refinement_request,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "content": refined_profile
                    })
                    st.markdown('<div class="success-banner">Profile Refined Successfully</div>', unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.error(refined_profile)
    
    if len(st.session_state.history) > 1:
        st.markdown("---")
        with st.expander(f"Version History ({len(st.session_state.history)} versions)"):
            for version in reversed(st.session_state.history):
                st.markdown(f"**Version {version['version']}** — {version['type']} at {version['timestamp']}")
                if version['type'] == "Refinement":
                    st.markdown(f"*Request: {version['request']}*")
                st.text_area("Version Content", value=version['content'], height=150, disabled=True, key=f"h_{version['version']}", label_visibility="collapsed")
                if version != list(reversed(st.session_state.history))[-1]:
                    st.markdown("---")

st.markdown('</div>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### Quick Actions")
    if st.button("Start Fresh", key="reset"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Session Stats")
    
    if st.session_state.current_profile:
        st.metric("Status", "Active")
        st.metric("Refinements", st.session_state.iteration_count)
        st.metric("Versions", len(st.session_state.history))
    else:
        st.metric("Status", "Ready")

# FOOTER
st.markdown("""
    <div class="footer">
        <div class="footer-title">Protocol Education CV Profile Generator</div>
        <div>Powered by Azure Fine-Tuned GPT-4o | Secure & Confidential</div>
    </div>
""", unsafe_allow_html=True)
