import streamlit as st
import streamlit.components.v1 as components
import os
import re
import json
from datetime import datetime
import pandas as pd
import requests
from shared_header import (
    render_header,
    render_admin_section,
    ACCOUNTS,
    INDUSTRIES,
    ACCOUNT_INDUSTRY_MAP,
    get_shared_data,
    render_unified_business_inputs,
)

# --- Page Config ---
st.set_page_config(
    page_title="Vocabulary Agent",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom Styling (Match Welcome Agent) ---
# Check dark mode from session state
if st.session_state.get('dark_mode', False):
    st.markdown("""
    <style>
        /* CSS Variables - DARK MODE */
        :root {
            --musigma-red: #8b1e1e;
            --accent-orange: #ff6b35;
            --accent-purple: #7c3aed;
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --text-light: #ffffff;
            --bg-card: #23272f;
            --bg-app: #0b0f14;
            --border-color: rgba(255,255,255,0.12);
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.3);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.4);
            --shadow-lg: 0 10px 25px rgba(0,0,0,0.5);
        }

        /* Dark background */
        body, .stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background: linear-gradient(135deg, #0b0f14 0%, #18181b 50%, #23272f 100%) !important;
            color: var(--text-primary) !important;
        }

        /* Smooth Animations */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes scaleIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }

        /* Section Title Boxes */
        .section-title-box {
            background: linear-gradient(135deg, var(--musigma-red) 0%, var(--accent-orange) 100%) !important;
            border-radius: 16px;
            padding: 1rem 2rem !important;
            margin: 0 0 0.5rem 0 !important;
            box-shadow: var(--shadow-lg) !important;
            text-align: center;
        }

        .section-title-box h3 {
            color: var(--text-light) !important;
            margin: 0 !important;
            font-weight: 700 !important;
            font-size: 1.3rem !important;
        }

        /* Button styling */
        .stButton > button { 
            background: linear-gradient(135deg, var(--musigma-red) 0%, var(--accent-orange) 100%);
            color: var(--text-light) !important;
            border: none;
            border-radius: 16px;
            padding: 1.1rem 2.75rem;
            font-weight: 700;
            font-size: 1.1rem;
            box-shadow: var(--shadow-md);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover { 
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(255, 107, 53, 0.5);
        }
        
        /* Smaller button for secondary actions */
        .stButton:has(button:not([kind="primary"])) > button,
        div[data-testid="column"]:has(.stButton) .stButton > button {
            padding: 0.5rem 1rem !important;
            font-size: 0.875rem !important;
            font-weight: 600 !important;
            min-height: 38px !important;
            max-height: 38px !important;
        }

        /* Vocabulary display styling */
        .vocab-display { 
            background: var(--bg-card) !important; 
            border: 2px solid var(--border-color);
            border-radius: 16px; 
            padding: 1.5rem !important; 
            line-height: 1.7 !important; 
            margin-top: 1rem;
            color: var(--text-primary) !important;
            font-size: 1rem;
            max-height: 650px;
            overflow-y: auto;
            box-shadow: var(--shadow-sm);
            animation: fadeInUp 0.7s ease-out;
        }
        
        /* Progress bar styling */
        .stProgress > div > div { 
            background: linear-gradient(90deg, var(--musigma-red), var(--accent-orange)) !important; 
            border-radius: 12px; 
            height: 12px !important;
        }
        
        /* SELECT BOXES STYLING - Dark Mode */
        .stSelectbox {
            margin-bottom: 1rem;
        }

        .stSelectbox > label {
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            color: var(--text-primary) !important;
            margin-bottom: 0.35rem !important;
        }

        .stSelectbox > div > div {
            background-color: rgba(35, 39, 47, 0.8) !important;
            border: 2px solid rgba(255, 107, 53, 0.3) !important;
            border-radius: 16px !important;
            padding: 0.35rem 0.65rem !important;
            min-height: 38px !important;
            max-height: 38px !important;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            display: flex !important;
            align-items: center !important;
        }

        .stSelectbox > div > div:hover {
            border-color: var(--accent-orange) !important;
            box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.2), inset 0 2px 4px rgba(0, 0, 0, 0.3);
        }

        .stSelectbox [data-baseweb="select"] {
            background-color: transparent !important;
            min-height: 32px !important;
            max-height: 32px !important;
        }

        .stSelectbox [data-baseweb="select"] > div {
            color: var(--text-light) !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            line-height: 1.3 !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
        }

        /* Dropdown popover container */
        [data-baseweb="popover"] {
            background-color: var(--bg-card) !important;
            border-radius: 16px !important;
            box-shadow: var(--shadow-lg) !important;
        }
        
        [data-baseweb="popover"] > div {
            background-color: var(--bg-card) !important;
        }
        
        /* Dropdown options styling */
        ul[role="listbox"] {
            background-color: var(--bg-card) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: 16px !important;
            box-shadow: var(--shadow-lg) !important;
            padding: 0.5rem !important;
            max-height: 280px !important;
            overflow-y: auto !important;
        }

        li[role="option"] {
            color: var(--text-light) !important;
            background-color: transparent !important;
            padding: 10px 14px !important;
            font-size: 0.95rem !important;
            border-radius: 10px !important;
            transition: all 0.2s ease !important;
            font-weight: 500 !important;
        }

        li[role="option"]:hover {
            background-color: rgba(124, 58, 237, 0.2) !important;
            color: var(--accent-purple) !important;
            transform: translateX(5px) !important;
        }

        li[role="option"][aria-selected="true"] {
            background-color: rgba(255, 107, 53, 0.2) !important;
            color: var(--accent-orange) !important;
            font-weight: 600 !important;
        }
        
        /* Disabled selectbox styling */
        .stSelectbox:has(select:disabled) > div > div {
            opacity: 1 !important;
            background: rgba(35, 39, 47, 0.8) !important;
            cursor: default !important;
            filter: brightness(0.9);
        }
        
        .stSelectbox:has(select:disabled) > div > div:hover {
            transform: none !important;
            border-color: rgba(255, 107, 53, 0.3) !important;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        }
        
        .stSelectbox:has(select:disabled) [data-baseweb="select"] > div {
            color: var(--text-secondary) !important;
            opacity: 0.8 !important;
        }
        
        /* TEXT AREA STYLING - Dark Mode */
        .stTextArea > label {
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            color: var(--text-primary) !important;
            margin-bottom: 0.35rem !important;
        }
        
        .stTextArea textarea {
            background: rgba(35, 39, 47, 0.8) !important;
            border: 2px solid rgba(255, 107, 53, 0.3) !important;
            border-radius: 16px !important;
            color: var(--text-light) !important;
            font-size: 1.05rem !important;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
            padding: 1.25rem !important;
            line-height: 1.7 !important;
            min-height: 150px !important;
            transition: all 0.3s ease;
        }

        .stTextArea textarea:focus {
            border-color: var(--accent-orange) !important;
            box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.2), inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
            outline: none !important;
        }

        .stTextArea textarea::placeholder {
            color: var(--text-secondary) !important;
            opacity: 0.6 !important;
        }
        
        .stTextArea textarea:disabled {
            background: rgba(35, 39, 47, 0.8) !important;
            opacity: 1 !important;
            cursor: default !important;
            color: var(--text-secondary) !important;
            border-color: rgba(255, 107, 53, 0.3) !important;
            filter: brightness(0.9);
        }
        
        .stTextArea:has(textarea:disabled) textarea:hover {
            border-color: rgba(255, 107, 53, 0.3) !important;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* All text elements readable in dark mode */
        h1, h2, h3, h4, h5, h6, p, span, div, label {
            color: var(--text-primary) !important;
        }
        
        /* Info boxes */
        .stAlert, [data-testid="stNotification"] {
            background-color: var(--bg-card) !important;
            color: var(--text-primary) !important;
            border-color: var(--border-color) !important;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    # LIGHT MODE
    st.markdown("""
    <style>
        /* CSS Variables - LIGHT MODE */
        :root {
            --musigma-red: #8b1e1e;
            --accent-orange: #ff6b35;
            --accent-purple: #7c3aed;
            --text-primary: #1e293b;
            --text-secondary: #6b7280;
            --text-light: #ffffff;
            --bg-card: #ffffff;
            --bg-app: #fafafa;
            --border-color: #e5e7eb;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
        }
        
        /* Light overall background */
        body, .stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 50%, #eeeeee 100%) !important;
            color: var(--text-primary) !important;
        }

        /* Smooth Animations */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes scaleIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }

        /* Section Title Boxes */
        .section-title-box {
            background: linear-gradient(135deg, var(--musigma-red) 0%, var(--accent-orange) 100%) !important;
            border-radius: 16px;
            padding: 1rem 2rem;
            margin: 0 0 0.5rem 0 !important;
            box-shadow: var(--shadow-lg) !important;
            text-align: center;
        }
        
        .section-title-box h3 {
            color: var(--text-light) !important;
            margin: 0 !important;
            font-weight: 700 !important;
            font-size: 1.3rem !important;
        }

        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, var(--musigma-red) 0%, var(--accent-orange) 100%);
            color: var(--text-light) !important;
            border: none;
            border-radius: 16px;
            padding: 1.1rem 2.75rem;
            font-weight: 700;
            font-size: 1.1rem;
            box-shadow: var(--shadow-md);
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(139, 30, 30, 0.4);
        }
        
        /* Smaller button for secondary actions */
        .stButton:has(button:not([kind="primary"])) > button,
        div[data-testid="column"]:has(.stButton) .stButton > button {
            padding: 0.5rem 1rem !important;
            font-size: 0.875rem !important;
            font-weight: 600 !important;
            min-height: 38px !important;
            max-height: 38px !important;
        }

        /* Vocabulary display styling */
        .vocab-display { 
            background: var(--bg-card) !important; 
            border: 2px solid var(--border-color);
            border-radius: 16px; 
            padding: 1.5rem !important; 
            line-height: 1.7 !important; 
            margin-top: 1rem;
            color: var(--text-primary) !important;
            font-size: 1rem;
            max-height: 650px;
            overflow-y: auto;
            box-shadow: var(--shadow-sm);
            animation: fadeInUp 0.7s ease-out;
        }
        
        /* Progress bar styling */
        .stProgress > div > div { 
            background: linear-gradient(90deg, var(--musigma-red), var(--accent-orange)) !important; 
            border-radius: 12px; 
            height: 12px !important;
        }

        /* SELECT BOXES STYLING - Light Mode */
        .stSelectbox {
            margin-bottom: 1rem;
        }

        .stSelectbox > label {
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            color: var(--text-primary) !important;
            margin-bottom: 0.35rem !important;
        }

        .stSelectbox > div > div {
            background-color: var(--bg-card) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: 16px !important;
            padding: 0.35rem 0.65rem !important;
            min-height: 38px !important;
            max-height: 38px !important;
            box-shadow: var(--shadow-sm);
            transition: all 0.3s ease;
            display: flex !important;
            align-items: center !important;
        }

        .stSelectbox > div > div:hover {
            border-color: var(--accent-purple) !important;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
        }

        .stSelectbox [data-baseweb="select"] {
            background-color: transparent !important;
            min-height: 32px !important;
            max-height: 32px !important;
        }

        .stSelectbox [data-baseweb="select"] > div {
            color: var(--text-primary) !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            line-height: 1.3 !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
        }

        /* Dropdown popover container */
        [data-baseweb="popover"] {
            background-color: var(--bg-card) !important;
            border-radius: 16px !important;
            box-shadow: var(--shadow-lg) !important;
        }
        
        [data-baseweb="popover"] > div {
            background-color: var(--bg-card) !important;
        }
        
        /* Dropdown options styling */
        ul[role="listbox"] {
            background-color: var(--bg-card) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: 16px !important;
            box-shadow: var(--shadow-lg) !important;
            padding: 0.5rem !important;
            max-height: 280px !important;
            overflow-y: auto !important;
        }

        li[role="option"] {
            color: var(--text-primary) !important;
            background-color: transparent !important;
            padding: 10px 14px !important;
            font-size: 0.95rem !important;
            border-radius: 10px !important;
            transition: all 0.2s ease !important;
            font-weight: 500 !important;
        }

        li[role="option"]:hover {
            background-color: rgba(124, 58, 237, 0.1) !important;
            color: var(--accent-purple) !important;
            transform: translateX(5px) !important;
        }

        li[role="option"][aria-selected="true"] {
            background-color: rgba(139, 30, 30, 0.15) !important;
            color: var(--musigma-red) !important;
            font-weight: 600 !important;
        }
        
        /* Ensure dropdown text is visible */
        li[role="option"] div,
        li[role="option"] span {
            color: var(--text-primary) !important;
        }
        
        li[role="option"]:hover div,
        li[role="option"]:hover span {
            color: var(--accent-purple) !important;
        }
        
        li[role="option"][aria-selected="true"] div,
        li[role="option"][aria-selected="true"] span {
            color: var(--musigma-red) !important;
        }
        
        /* Disabled selectbox styling */
        .stSelectbox:has(select:disabled) > div > div {
            opacity: 1 !important;
            background: var(--bg-card) !important;
            cursor: default !important;
            filter: brightness(0.97);
        }
        
        .stSelectbox:has(select:disabled) > div > div:hover {
            transform: none !important;
            border-color: var(--border-color) !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        .stSelectbox:has(select:disabled) [data-baseweb="select"] > div {
            color: var(--text-primary) !important;
            opacity: 0.8 !important;
        }

        /* TEXT AREA STYLING - Light Mode */
        .stTextArea > label {
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            color: var(--text-primary) !important;
            margin-bottom: 0.35rem !important;
        }
        
        .stTextArea textarea {
            background: var(--bg-card) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: 16px !important;
            color: var(--text-primary) !important;
            font-size: 1.05rem !important;
            box-shadow: var(--shadow-sm);
            padding: 1.25rem !important;
            line-height: 1.7 !important;
            min-height: 150px !important;
            transition: all 0.3s ease;
        }

        .stTextArea textarea:focus {
            border-color: var(--accent-orange) !important;
            box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15), 0 2px 4px rgba(0, 0, 0, 0.05) !important;
            outline: none !important;
        }

        .stTextArea textarea::placeholder {
            color: var(--text-secondary) !important;
            opacity: 0.5 !important;
        }
        
        .stTextArea textarea:disabled {
            background: var(--bg-card) !important;
            opacity: 1 !important;
            cursor: default !important;
            color: var(--text-primary) !important;
            border-color: var(--border-color) !important;
            filter: brightness(0.97);
        }
        
        .stTextArea:has(textarea:disabled) textarea:hover {
            border-color: var(--border-color) !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        /* Info boxes */
        .stAlert, [data-testid="stNotification"] {
            background-color: var(--bg-card) !important;
            color: var(--text-primary) !important;
            border-color: var(--border-color) !important;
        }
    </style>
    """, unsafe_allow_html=True)

# --- Initialize session state ---
if 'vocab_output' not in st.session_state:
    st.session_state.vocab_output = ""
if 'show_vocabulary' not in st.session_state:
    st.session_state.show_vocabulary = False
if 'feedback_submitted' not in st.session_state:
    st.session_state.feedback_submitted = False
if 'feedback_option' not in st.session_state:
    st.session_state.feedback_option = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'validation_attempted' not in st.session_state:
    st.session_state.validation_attempted = False

# --- Render Header ---
render_header(
    agent_name="Vocabulary Agent",
    agent_subtitle="Reviewing the business problem statement."
)

# --- Check for Admin Mode ---
# Check if admin panel should be shown via query params
try:
    if hasattr(st, 'query_params'):
        admin_toggled = 'adminPanelToggled' in st.query_params
    else:
        query_params = st.experimental_get_query_params()
        admin_toggled = 'adminPanelToggled' in query_params
except:
    admin_toggled = False

# If admin mode detected or session state shows admin, render admin section
if admin_toggled or st.session_state.get('current_page', '') == 'admin':
    st.session_state.current_page = 'admin'
    render_admin_section()
    st.stop()  # Stop rendering the rest of the page

# Begin scrollable content wrapper
st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)

# ===============================
# API Configuration
# ===============================

# ===============================
# API Configuration (Simplified)
# ===============================

# Constants
TENANT_ID = "talos"
HEADERS_BASE = {"Content-Type": "application/json"}
VOCAB_API_URL = "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758548233201&level=1"

# API config with simplified prompt
API_CONFIGS = [
    {
        "name": "vocabulary",
        "url": VOCAB_API_URL,
        "multiround_convo": 3,
        "description": "vocabulary",
        "prompt": lambda problem, outputs: (
            f"{problem}\n\nExtract the vocabulary from this problem statement."
        )
    }
]

# Global feedback file path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FEEDBACK_FILE = os.path.join(BASE_DIR, "feedback.csv")

# Initialize feedback file if not present
try:
    if not os.path.exists(FEEDBACK_FILE):
        df = pd.DataFrame(columns=["Timestamp", "Name", "Email", "Feedback", "FeedbackType",
                          "OffDefinitions", "Suggestions", "Account", "Industry", "ProblemStatement"])
        df.to_csv(FEEDBACK_FILE, index=False)
except (PermissionError, OSError) as e:
    if 'feedback_data' not in st.session_state:
        st.session_state.feedback_data = pd.DataFrame(
            columns=["Timestamp", "Name", "Email", "Feedback", "FeedbackType", "OffDefinitions", "Suggestions", "Account", "Industry", "ProblemStatement"])

# Token initialization


def _init_auth_token():
    token = os.environ.get("AUTH_TOKEN", "")
    try:
        if not token:
            token = st.secrets.get("AUTH_TOKEN", "")
    except Exception:
        pass
    return token or ""


if 'auth_token' not in st.session_state:
    st.session_state.auth_token = _init_auth_token()

# ===============================
# Utility Functions (Enhanced from n.py)
# ===============================


def json_to_text(data):
    """Extract text from JSON response"""
    if data is None:
        return ""
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        for key in ("result", "output", "content", "text", "answer", "response"):
            if key in data and data[key]:
                return json_to_text(data[key])
        if "data" in data:
            return json_to_text(data["data"])
        # Try to extract any string values
        for value in data.values():
            if isinstance(value, str) and len(value) > 10:  # Reasonable length for content
                return value
        return "\n".join(f"{k}: {json_to_text(v)}" for k, v in data.items() if v)
    if isinstance(data, list):
        return "\n".join(json_to_text(x) for x in data if x)
    return str(data)


def sanitize_text(text):
    """Remove markdown artifacts and clean up text"""
    if not text:
        return ""

    # Fix the "s" character issue
    text = re.sub(r'^\s*s\s+', '', text.strip())
    text = re.sub(r'\n\s*s\s+', '\n', text)

    text = re.sub(r'Q\d+\s*Answer\s*Explanation\s*:',
                  '', text, flags=re.IGNORECASE)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    text = re.sub(r'^\s*[-*]\s+', '• ', text, flags=re.MULTILINE)
    text = re.sub(r'<\/?[^>]+>', '', text)
    text = re.sub(r'& Key Takeaway:', 'Key Takeaway:', text)

    return text.strip()


def format_vocabulary_with_bold(text, extra_phrases=None):
    """Format vocabulary text with bold styling (Enhanced from n.py)"""
    if not text:
        return "No vocabulary data available"

    clean_text = sanitize_text(text)
    clean_text = clean_text.replace(" - ", " : ")
    clean_text = re.sub(r'(?m)^\s*[-*]\s+', '• ', clean_text)

    extra_patterns = []
    if extra_phrases:
        for p in extra_phrases:
            if any(ch in p for ch in r".^$*+?{}[]\|()"):
                extra_patterns.append(p)
            else:
                extra_patterns.append(re.escape(p))

    lines = clean_text.splitlines()
    n = len(lines)
    i = 0
    paragraph_html = []

    def collect_continuation(start_idx):
        block_lines = [lines[start_idx].rstrip()]
        j = start_idx + 1
        while j < n:
            next_line = lines[j]
            if not next_line.strip():
                break
            if re.match(r'^\s+', next_line) or re.match(r'^\s*[a-z]', next_line):
                block_lines.append(next_line.rstrip())
                j += 1
                continue
            if re.match(r'^\s*(?:•|-|\d+\.)\s+', next_line):
                break
            break
        return block_lines, j

    while i < n:
        ln = lines[i].rstrip()
        if not ln.strip():
            paragraph_html.append('')
            i += 1
            continue

        if extra_patterns:
            new_ln = ln
            for pat in extra_patterns:
                try:
                    new_ln = re.sub(
                        pat, lambda m: f"<strong>{m.group(0)}</strong>", new_ln, flags=re.IGNORECASE)
                except re.error:
                    new_ln = re.sub(re.escape(
                        pat), lambda m: f"<strong>{m.group(0)}</strong>", new_ln, flags=re.IGNORECASE)
            if new_ln != ln:
                paragraph_html.append(new_ln)
                i += 1
                continue

        if re.search(r'(Step\s*\d+\s*:)', ln, flags=re.IGNORECASE):
            block, j = collect_continuation(i)
            block_text = "<br>".join([b.strip() for b in block])
            paragraph_html.append(f"<strong>{block_text}</strong>")
            i = j
            continue

        m_num_colon = re.match(r'^\s*(\d+\.\s+[^:]+):\s*(.*)$', ln)
        if m_num_colon:
            heading = m_num_colon.group(1).strip()
            remainder = m_num_colon.group(2).strip()
            paragraph_html.append(
                f"<strong>{heading}:</strong> {remainder}" if remainder else f"<strong>{heading}:</strong>")
            i += 1
            continue

        m_num_no_colon = re.match(r'^\s*(\d+\.\s+.+)$', ln)
        if m_num_no_colon:
            block, j = collect_continuation(i)
            block_text = "<br>".join([b.strip() for b in block])
            paragraph_html.append(f"<strong>{block_text}</strong>")
            i = j
            continue

        m_bullet_heading = re.match(r'^\s*(?:•|\d+\.)\s*([^:]+):\s*(.*)$', ln)
        if m_bullet_heading:
            heading = m_bullet_heading.group(1).strip()
            remainder = m_bullet_heading.group(2).strip()
            paragraph_html.append(
                f"• <strong>{heading}:</strong> {remainder}" if remainder else f"• <strong>{heading}:</strong>")
            i += 1
            continue

        m_side = re.match(r'^\s*([^:]+):\s*(.*)$', ln)
        if m_side and len(m_side.group(1).split()) <= 8:
            left = m_side.group(1).strip()
            right = m_side.group(2).strip()
            paragraph_html.append(
                f"<strong>{left}:</strong> {right}" if right else f"<strong>{left}:</strong>")
            i += 1
            continue

        if re.fullmatch(r'\s*Revenue\s+Growth\s+Rate\s*', ln, flags=re.IGNORECASE):
            paragraph_html.append(f"<strong>{ln.strip()}</strong>")
            i += 1
            continue

        paragraph_html.append(ln)
        i += 1

    final_paragraphs = []
    temp_lines = []
    for entry in paragraph_html:
        if entry == '':
            if temp_lines:
                final_paragraphs.append("<br>".join(temp_lines))
                temp_lines = []
        else:
            temp_lines.append(entry)
    if temp_lines:
        final_paragraphs.append("<br>".join(temp_lines))

    para_wrapped = [
        f"<p style='margin:6px 0; line-height:1.45; font-size:0.98rem;'>{p}</p>" for p in final_paragraphs
    ]
    final_html = "\n".join(para_wrapped)

    formatted_output = f"""
    <div class="vocab-display">
        {final_html}
    </div>
    """
    formatted_output = re.sub(r'(<br>\s*){3,}', '<br><br>', formatted_output)
    return formatted_output


def submit_feedback(feedback_type, name="", email="", off_definitions="", suggestions="", additional_feedback=""):
    """Submit feedback to CSV file (Enhanced from n.py)"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get context data from session state
    account = st.session_state.get("current_account", "")
    industry = st.session_state.get("current_industry", "")
    problem_statement = st.session_state.get("current_problem", "")

    new_entry = pd.DataFrame([[
        timestamp, name, email, additional_feedback, feedback_type, off_definitions, suggestions, account, industry, problem_statement
    ]], columns=["Timestamp", "Name", "Email", "Feedback", "FeedbackType", "OffDefinitions", "Suggestions", "Account", "Industry", "ProblemStatement"])

    try:
        # Try file-based storage first
        if os.path.exists(FEEDBACK_FILE):
            existing = pd.read_csv(FEEDBACK_FILE)

            # Handle schema mismatch
            missing_cols = set(new_entry.columns) - set(existing.columns)
            for col in missing_cols:
                existing[col] = ''

            # Reorder existing columns to match the new entry's order
            existing = existing[new_entry.columns]

            updated = pd.concat([existing, new_entry], ignore_index=True)
        else:
            updated = new_entry

        try:
            updated.to_csv(FEEDBACK_FILE, index=False)
        except (PermissionError, OSError):
            # Fallback to session state on Streamlit Cloud
            if 'feedback_data' not in st.session_state:
                st.session_state.feedback_data = pd.DataFrame(
                    columns=new_entry.columns)
            st.session_state.feedback_data = pd.concat(
                [st.session_state.feedback_data, new_entry], ignore_index=True)
            st.info("📝 Feedback saved to session (cloud mode)")

        st.session_state.feedback_submitted = True
        return True
    except Exception as e:
        st.error(f"Error saving feedback: {str(e)}")
        return False


def reset_app_state():
    """Completely reset session state to initial values"""
    # Clear vocabulary-related state
    keys_to_clear = ['vocab_output', 'show_vocabulary', 'feedback_submitted',
                     'feedback_option', 'analysis_complete', 'validation_attempted']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    st.success("✅ Application reset successfully! You can start a new analysis.")

# ===============================
# Main Content
# ===============================


# Retrieve data from shared header
shared = get_shared_data()
account = shared.get("account") or ""
industry = shared.get("industry") or ""
problem = shared.get("problem") or ""

# Store current context in session state
st.session_state.current_account = account
st.session_state.current_industry = industry
st.session_state.current_problem = problem

# Normalize display values


def _norm_display(val, fallback):
    if not val or val in ("Select Account", "Select Industry", "Select Problem"):
        return fallback
    return val


display_account = _norm_display(account, "Unknown Company")
display_industry = _norm_display(industry, "Unknown Industry")

# Initialize edit mode session state
if 'vocab_edit_mode' not in st.session_state:
    st.session_state.vocab_edit_mode = False
if 'vocab_edit_account' not in st.session_state:
    st.session_state.vocab_edit_account = account
if 'vocab_edit_industry' not in st.session_state:
    st.session_state.vocab_edit_industry = industry
if 'vocab_edit_problem' not in st.session_state:
    st.session_state.vocab_edit_problem = problem

# Use the unified inputs (Welcome-style) so Vocabulary page matches all others
account, industry, problem = render_unified_business_inputs(
    page_key_prefix="vocab",
    show_titles=True,
    title_account_industry="Account & Industry",
    title_problem="Business Problem Description",
    save_button_label="✅ Save Problem Details",
)

st.markdown("---")

# ===============================
# Vocabulary Extraction Section
# ===============================

# Validation checks (without warnings)
has_account = account and account != "Select Account"
has_industry = industry and industry != "Select Industry"
has_problem = bool(problem.strip())

# Extract Vocabulary Button
extract_btn = st.button("🔍 Extract Vocabulary", type="primary", use_container_width=True,
                        disabled=not (has_account and has_industry and has_problem))

if extract_btn:
    # Set validation attempted flag
    st.session_state.validation_attempted = True

    # Final validation before processing
    if not has_account:
        st.error("❌ Please select an account before proceeding.")
        st.stop()

    if not has_industry:
        st.error("❌ Please select an industry before proceeding.")
        st.stop()

    if not has_problem:
        st.error("❌ Please enter a business problem description.")
        st.stop()

    # Build context
    full_context = f"""
    Business Problem:
    {problem.strip()}

    Context:
    Account: {account}
    Industry: {industry}
    """.strip()

    # Prepare headers with authentication
    headers = HEADERS_BASE.copy()
    headers.update({
        "Tenant-ID": TENANT_ID,
        "X-Tenant-ID": TENANT_ID
    })

    if st.session_state.auth_token:
        headers["Authorization"] = f"Bearer {st.session_state.auth_token}"

    with st.spinner("🔍 Extracting vocabulary and analyzing context..."):
        progress = st.progress(0)

        try:
            with requests.Session() as session:
                cfg = API_CONFIGS[0]
                goal = cfg["prompt"](full_context, {})

                # Make API request with timeout
                response = session.post(
                    cfg["url"],
                    headers=headers,
                    json={"agency_goal": goal},
                    timeout=60
                )

                progress.progress(0.5)

                if response.status_code == 200:
                    # Process successful response
                    result_data = response.json()
                    text_output = json_to_text(result_data)
                    cleaned_text = sanitize_text(text_output)

                    st.session_state.vocab_output = cleaned_text
                    st.session_state.show_vocabulary = True
                    st.session_state.analysis_complete = True

                    progress.progress(1.0)
                    st.success("✅ Vocabulary extraction complete!")

                else:
                    error_msg = f"API Error {response.status_code}: {response.text[:200]}"
                    st.session_state.vocab_output = error_msg
                    st.session_state.show_vocabulary = True
                    st.error(
                        f"API request failed with status {response.status_code}")

        except requests.exceptions.Timeout:
            error_msg = "Request timeout: The API took too long to respond."
            st.session_state.vocab_output = error_msg
            st.session_state.show_vocabulary = True
            st.error("Request timeout - please try again.")

        except requests.exceptions.ConnectionError:
            error_msg = "Connection error: Unable to connect to the API server."
            st.session_state.vocab_output = error_msg
            st.session_state.show_vocabulary = True
            st.error("Connection error - please check your network connection.")

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            st.session_state.vocab_output = error_msg
            st.session_state.show_vocabulary = True
            st.error(f"An unexpected error occurred: {str(e)}")

# ===============================
# Display Vocabulary Results
# ===============================

if st.session_state.get("show_vocabulary") and st.session_state.get("vocab_output"):
    st.markdown("---")

    # Display vocabulary with context (Enhanced from n.py)
    st.markdown(
        f"""
        <div style="margin: 20px 0;">
            <div class="section-title-box" style="padding: 1rem 1.5rem;">
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
                    <h3 style="margin-bottom:8px; color:white; font-weight:800; font-size:1.4rem; line-height:1.2;">
                        Vocabulary
                    </h3>
                    <p style="font-size:0.95rem; color:white; margin:0; line-height:1.5; text-align:center; max-width: 800px;">
                        Please note that it is an <strong>AI-generated Vocabulary</strong>, derived from 
                        the <em>company</em> <strong>{display_account}</strong> and 
                        the <em>industry</em> <strong>{display_industry}</strong> based on the 
                        <em>problem statement</em> you shared.<br>
                        In case you find something off, there's a provision to share feedback at the bottom 
                        we encourage you to use it.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Format and display vocabulary with account/industry substitutions
    vocab_text = st.session_state.vocab_output
    formatted_vocab = format_vocabulary_with_bold(vocab_text)

    # Replace generic mentions in the formatted HTML
    if display_account and display_account != "Unknown Company":
        formatted_vocab = re.sub(
            r'\bthe company\b', display_account, formatted_vocab, flags=re.IGNORECASE)
    if display_industry and display_industry != "Unknown Industry":
        formatted_vocab = re.sub(
            r'\bthe industry\b', display_industry, formatted_vocab, flags=re.IGNORECASE)

    st.markdown(formatted_vocab, unsafe_allow_html=True)

    # ===============================
    # User Feedback Section (Enhanced from n.py)
    # ===============================

    st.markdown("---")
    st.markdown('<div class="section-title-box" style="text-align:center;"><h3>💬 User Feedback</h3></div>',
                unsafe_allow_html=True)
    st.markdown(
        "Please share your thoughts or suggestions after reviewing the vocabulary results.")

    # Show feedback section if not submitted
    if not st.session_state.get('feedback_submitted', False):
        fb_choice = st.radio(
            "Select your feedback type:",
            options=[
                "I have read it, found it useful, thanks.",
                "I have read it, found some definitions to be off.",
                "The widget seems interesting, but I have some suggestions on the features.",
            ],
            index=None,
            key="feedback_radio",
        )

        if fb_choice:
            st.session_state.feedback_option = fb_choice

        # Feedback form 1: Positive feedback
        if fb_choice == "I have read it, found it useful, thanks.":
            with st.form("feedback_form_positive", clear_on_submit=True):
                st.info(
                    "Thank you for your positive feedback! Optional: Share your name and email.")
                col1, col2 = st.columns(2)
                with col1:
                    st.text_input(
                        "Account", value=display_account, disabled=True)
                with col2:
                    st.text_input(
                        "Industry", value=display_industry, disabled=True)
                name = st.text_input("Your Name (optional)")
                email = st.text_input("Your Email (optional)")
                submitted = st.form_submit_button("📨 Submit Positive Feedback")
                if submitted:
                    if submit_feedback(fb_choice, name=name, email=email):
                        st.success(
                            "✅ Thank you! Your positive feedback has been recorded.")

        # Feedback form 2: Definitions off (Enhanced with better section parsing)
        elif fb_choice == "I have read it, found some definitions to be off.":
            with st.form("feedback_form_defs", clear_on_submit=True):
                st.markdown(
                    "**Please select which sections have definitions that seem off:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.text_input(
                        "Account", value=display_account, disabled=True)
                with col2:
                    st.text_input(
                        "Industry", value=display_industry, disabled=True)
                name = st.text_input("Your Name")
                email = st.text_input("Your Email (optional)")

                vocab_text = st.session_state.get("vocab_output", "")
                step_sections = {}

                # Enhanced section parsing from n.py
                if vocab_text:
                    step_pattern = r'Step\s*(\d+)\s*:\s*([^\n]+)'
                    matches = re.finditer(
                        step_pattern, vocab_text, re.IGNORECASE)
                    for m in matches:
                        step_num = m.group(1)
                        step_title = m.group(2).strip()
                        step_sections[f"Step {step_num}"] = step_title

                # Default sections if none found
                if not step_sections:
                    step_sections = {
                        "Step 1": "Key Performance Indicators (KPIs)",
                        "Step 2": "Technical Definitions",
                        "Step 3": "Industry Context",
                        "Step 4": "Business Metrics",
                        "Step 5": "Strategic Implications",
                    }

                st.markdown("### Select problematic sections:")
                selected_issues = {}

                for i in range(1, 6):
                    step_key = f"Step {i}"
                    step_title = step_sections.get(step_key, f"Section {i}")

                    # Extract sub-items for more granular selection
                    sub_items = []
                    if vocab_text:
                        step_section_match = re.search(
                            rf'Step\s*{i}\s*:.*?(?=Step\s*\d+\s*:|$)',
                            vocab_text,
                            re.IGNORECASE | re.DOTALL
                        )
                        if step_section_match:
                            step_content = step_section_match.group(0)
                            sub_item_pattern = r'^\s*(\d+)\.\s+([^:\n]+)'
                            sub_matches = re.finditer(
                                sub_item_pattern, step_content, re.MULTILINE)
                            for sub_match in sub_matches:
                                item_text = sub_match.group(2).strip()
                                item_text = re.sub(r'<[^>]+>', '', item_text)
                                item_text = re.sub(
                                    r'\*\*([^*]+)\*\*', r'\1', item_text)
                                sub_items.append(item_text)

                    if not sub_items:
                        sub_items = [f"{step_title} - General"]

                    if i == 5 and not sub_items:
                        sub_items = [f"{step_key}: {step_title}"]

                    selected = st.multiselect(
                        f"**{step_key}: {step_title}**",
                        options=sub_items,
                        key=f"step_{i}_issues",
                        help=f"Select items from {step_key} that have definition issues"
                    )
                    if selected:
                        selected_issues[step_key] = selected

                additional_feedback = st.text_area(
                    "Additional comments:",
                    placeholder="Please provide more details about the definition issues you found..."
                )

                submitted = st.form_submit_button("📨 Submit Feedback")
                if submitted:
                    if not selected_issues:
                        st.warning(
                            "⚠️ Please select at least one section that has definition issues.")
                    else:
                        issues_list = [
                            f"{step} - {item}" for step, items in selected_issues.items() for item in items]
                        off_defs_text = " | ".join(issues_list)
                        if submit_feedback(fb_choice, name=name, email=email, off_definitions=off_defs_text, additional_feedback=additional_feedback):
                            st.success(
                                "✅ Thank you! Your feedback has been submitted.")

        # Feedback form 3: Suggestions
        elif fb_choice == "The widget seems interesting, but I have some suggestions on the features.":
            with st.form("feedback_form_suggestions", clear_on_submit=True):
                st.markdown(
                    "**Please share your suggestions for improvement:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.text_input(
                        "Account", value=display_account, disabled=True)
                with col2:
                    st.text_input(
                        "Industry", value=display_industry, disabled=True)
                name = st.text_input("Your Name")
                email = st.text_input("Your Email (optional)")
                suggestions = st.text_area(
                    "Your suggestions:",
                    placeholder="What features would you like to see improved or added?"
                )
                submitted = st.form_submit_button("📨 Submit Feedback")
                if submitted:
                    if not suggestions.strip():
                        st.warning("⚠️ Please provide your suggestions.")
                    else:
                        if submit_feedback(fb_choice, name=name, email=email, suggestions=suggestions):
                            st.success(
                                "✅ Thank you! Your feedback has been submitted.")
    else:
        # Feedback already submitted
        st.success("✅ Thank you! Your feedback has been recorded.")
        if st.button("📝 Submit Additional Feedback", key="reopen_feedback_btn"):
            st.session_state.feedback_submitted = False
            st.rerun()

    # ===============================
    # Download Section
    # ===============================

    st.markdown("---")
    st.markdown('<div class="section-title-box" style="text-align:center;"><h3>📥 Download Vocabulary</h3></div>',
                unsafe_allow_html=True)

    vocab_text = st.session_state.get("vocab_output", "")
    if vocab_text and not vocab_text.startswith("API Error") and not vocab_text.startswith("Error:"):
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"vocabulary_{display_account.replace(' ', '_')}_{ts}.txt"
        download_content = f"""Vocabulary Export
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Company: {display_account}
Industry: {display_industry}

{vocab_text}

---
Generated by Vocabulary Analysis Tool
"""
        st.download_button(
            "⬇️ Download Vocabulary as Text File",
            data=download_content,
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info(
            "No vocabulary available for download. Please complete the analysis first.")

# Close the scrollable-content wrapper
st.markdown('</div>', unsafe_allow_html=True)
