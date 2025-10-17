import streamlit as st
from shared_header import render_header, ACCOUNTS, INDUSTRIES, ACCOUNT_INDUSTRY_MAP

# --- Page Config ---
st.set_page_config(
    page_title="Business Problem Analysis Platform",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Render Header ---
render_header(
    agent_name="Business Problem Analysis Platform",
    agent_subtitle="Specialized AI agents to extract, classify, and analyze key dimensions of your business challenges",
    enable_admin_access=False  # Disable admin access on login page
)
# --- Global Scroll Fix (📍 scroll_stopper_v1) ---
st.markdown("""
<style>
/* =========================
   📍 scroll_stopper_v1
   Fixes double scrollbar + stops scroll at header edge
   ========================= */

/* Remove unwanted global scrollbars */
html, body, [data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"] {
    overflow: hidden !important;
}

/* Scrollable content below the fixed header */
.scrollable-content {
    /* rely on shared_header for layout; only set horizontal padding here */
    padding: 0 2rem;
    box-sizing: border-box;
}

/* Nuke any top padding/margin so content starts flush to header */
.scrollable-content .block-container,
.scrollable-content [data-testid="stVerticalBlock"],
.scrollable-content .element-container:first-child,
.scrollable-content .stMarkdown:first-child {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Section title spacing (leaner to match image 2); first section has no extra top margin */
.scrollable-content .section-title-box {
    margin: 0.75rem 0 0.5rem 0 !important;
}
.scrollable-content .section-title-box:first-of-type {
    margin-top: 0 !important;
}

/* Streamlit scrollbar styling */
.scrollable-content::-webkit-scrollbar {
    width: 8px;
}
.scrollable-content::-webkit-scrollbar-thumb {
    background: rgba(140, 140, 140, 0.5);
    border-radius: 4px;
}
.scrollable-content::-webkit-scrollbar-thumb:hover {
    background: rgba(100, 100, 100, 0.8);
}
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'employee_id' not in st.session_state:
    st.session_state.employee_id = ""
if 'launched_agent' not in st.session_state:
    st.session_state.launched_agent = None
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# SAVED states (used by agent pages - only updated on Save button)
# Initialize these FIRST as they are the source of truth
if 'saved_account' not in st.session_state:
    st.session_state.saved_account = "Select Account"
if 'saved_industry' not in st.session_state:
    st.session_state.saved_industry = "Select Industry"
if 'saved_problem' not in st.session_state:
    st.session_state.saved_problem = ""

# Widget states (can change with widget interactions)
# DON'T use keys for widgets - manage state manually to avoid conflicts
# Initialize ONLY if not already set
if 'business_account' not in st.session_state:
    st.session_state.business_account = st.session_state.saved_account

if 'business_industry' not in st.session_state:
    st.session_state.business_industry = st.session_state.saved_industry

if 'business_problem' not in st.session_state:
    st.session_state.business_problem = st.session_state.saved_problem

# Edit confirmation flag - tracks if user confirmed they want to change saved data
if 'edit_confirmed' not in st.session_state:
    st.session_state.edit_confirmed = False

# Flag to prevent showing dialog after cancel button click
if 'cancel_clicked' not in st.session_state:
    st.session_state.cancel_clicked = False

# Counter used to force selectbox re-render when we programmatically change values
if 'selectbox_key_counter' not in st.session_state:
    st.session_state.selectbox_key_counter = 0

# Counter to force selectbox refresh after cancel
if 'selectbox_key_counter' not in st.session_state:
    st.session_state.selectbox_key_counter = 0


def render_login_page():
    # Apply login page specific styling
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
            /* Dark Mode Login Styling */
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
                --shadow-lg: 0 10px 25px rgba(0,0,0,0.5);
            }
            
            /* Dark background for login page */
            .stApp, [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #0b0f14 0%, #18181b 50%, #23272f 100%) !important;
            }
            
            /* Login card container */
            .login-card {
                background: linear-gradient(135deg, rgba(35, 39, 47, 0.95), rgba(24, 24, 27, 0.95));
                border: 2px solid rgba(255, 107, 53, 0.3);
                border-radius: 24px;
                padding: 3rem 2.5rem;
                max-width: 500px;
                margin: 4rem auto;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 80px rgba(255, 107, 53, 0.1);
                backdrop-filter: blur(10px);
            }
            
            .login-title {
                background: linear-gradient(135deg, #ff6b35, #7c3aed);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 2.5rem;
                font-weight: 800;
                text-align: center;
                margin-bottom: 0.5rem;
                letter-spacing: -0.5px;
            }
            
            .login-subtitle {
                color: var(--text-secondary);
                text-align: center;
                font-size: 1.05rem;
                margin-bottom: 2.5rem;
                font-weight: 400;
            }
            
            /* Input field styling for dark mode */
            .stTextInput input {
                background-color: rgba(35, 39, 47, 0.8) !important;
                border: 2px solid rgba(255, 107, 53, 0.3) !important;
                border-radius: 16px !important;
                color: var(--text-light) !important;
                font-size: 1.1rem !important;
                padding: 1.2rem 1.5rem !important;
                transition: all 0.3s ease !important;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
            }
            
            .stTextInput input:focus {
                border-color: var(--accent-orange) !important;
                box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.2), inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
                outline: none !important;
            }
            
            .stTextInput input::placeholder {
                color: var(--text-secondary) !important;
                opacity: 0.6 !important;
            }
            
            .stTextInput label {
                color: var(--text-primary) !important;
                font-weight: 600 !important;
                font-size: 1.05rem !important;
                margin-bottom: 0.75rem !important;
            }
            
            /* Login button styling */
            .stButton > button {
                background: linear-gradient(135deg, var(--musigma-red) 0%, var(--accent-orange) 100%) !important;
                color: var(--text-light) !important;
                border: none !important;
                border-radius: 16px !important;
                padding: 1.2rem 2.5rem !important;
                font-weight: 700 !important;
                font-size: 1.2rem !important;
                box-shadow: 0 8px 20px rgba(255, 107, 53, 0.4) !important;
                transition: all 0.3s ease !important;
                margin-top: 1rem !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-3px) !important;
                box-shadow: 0 12px 30px rgba(255, 107, 53, 0.6) !important;
            }
            
            /* Error message styling */
            .stAlert {
                background-color: rgba(220, 38, 38, 0.15) !important;
                border: 2px solid rgba(220, 38, 38, 0.4) !important;
                border-radius: 12px !important;
                color: #fca5a5 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Light Mode Login Styling
        st.markdown("""
        <style>
            /* Light Mode Login Styling */
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
            }
            
            /* Light background for login page */
            .stApp, [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 50%, #eeeeee 100%) !important;
            }
            
            /* Login card container */
            .login-card {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(249, 250, 251, 0.98));
                border: 2px solid rgba(255, 107, 53, 0.2);
                border-radius: 24px;
                padding: 3rem 2.5rem;
                max-width: 500px;
                margin: 4rem auto;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08), 0 0 80px rgba(255, 107, 53, 0.05);
            }
            
            .login-title {
                background: linear-gradient(135deg, #ff6b35, #7c3aed);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 2.5rem;
                font-weight: 800;
                text-align: center;
                margin-bottom: 0.5rem;
                letter-spacing: -0.5px;
            }
            
            .login-subtitle {
                color: var(--text-secondary);
                text-align: center;
                font-size: 1.05rem;
                margin-bottom: 2.5rem;
                font-weight: 400;
            }
            
            /* Input field styling for light mode */
            .stTextInput input {
                background-color: #ffffff !important;
                border: 2px solid rgba(255, 107, 53, 0.2) !important;
                border-radius: 16px !important;
                color: var(--text-primary) !important;
                font-size: 1.1rem !important;
                padding: 1.2rem 1.5rem !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
            }
            
            .stTextInput input:focus {
                border-color: var(--accent-orange) !important;
                box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15), 0 2px 4px rgba(0, 0, 0, 0.05) !important;
                outline: none !important;
            }
            
            .stTextInput input::placeholder {
                color: var(--text-secondary) !important;
                opacity: 0.5 !important;
            }
            
            .stTextInput label {
                color: var(--text-primary) !important;
                font-weight: 600 !important;
                font-size: 1.05rem !important;
                margin-bottom: 0.75rem !important;
            }
            
            /* Login button styling */
            .stButton > button {
                background: linear-gradient(135deg, var(--musigma-red) 0%, var(--accent-orange) 100%) !important;
                color: var(--text-light) !important;
                border: none !important;
                border-radius: 16px !important;
                padding: 1.2rem 2.5rem !important;
                font-weight: 700 !important;
                font-size: 1.2rem !important;
                box-shadow: 0 8px 20px rgba(255, 107, 53, 0.3) !important;
                transition: all 0.3s ease !important;
                margin-top: 1rem !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-3px) !important;
                box-shadow: 0 12px 30px rgba(255, 107, 53, 0.5) !important;
            }
            
            /* Error message styling */
            .stAlert {
                background-color: rgba(220, 38, 38, 0.1) !important;
                border: 2px solid rgba(220, 38, 38, 0.3) !important;
                border-radius: 12px !important;
                color: #dc2626 !important;
            }
        </style>
        """, unsafe_allow_html=True)

    # Dynamic header padding adjustment + Fixed login layout (CSS-only; no JS scroll lock)
    st.markdown("""
        <style>
            /* ====================================
               LOGIN PAGE OVERRIDE - NO SCROLLING
               ==================================== */
            
            /* LOGIN PAGE: Override shared header - complete lock */
            body, html {
                overflow: hidden !important;
                position: fixed !important;
                width: 100vw !important;
                height: 100vh !important;
            }
            
            .stApp {
                overflow: hidden !important;
                position: fixed !important;
                width: 100vw !important;
                height: 100vh !important;
            }
            
            .main,
            [data-testid="stAppViewContainer"] {
                overflow: hidden !important;
                position: fixed !important;
                top: var(--header-height, 100px) !important;
                left: 0 !important;
                right: 0 !important;
                bottom: 0 !important;
            }
            
            /* LOGIN PAGE: Fixed container - no movement */
            .main .block-container {
                position: fixed !important;
                top: var(--header-height, 100px) !important;
                left: 0 !important;
                right: 0 !important;
                bottom: 0 !important;
                padding: 0 !important;
                margin: 0 !important;
                overflow: hidden !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }
            
            /* Remove all extra spacing */
            .section-title-box {
                margin-top: 0 !important;
                margin-bottom: 0.5rem !important;
            }
            
            /* Force content to start immediately */
            .element-container:first-child,
            .stMarkdown:first-child {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
            
            /* LOGIN PAGE: Fixed centered card container */
            .login-card {
                max-width: 500px !important;
                padding: 1.2rem 2rem !important;
                margin: 0 auto !important;
                position: relative !important;
            }
            
            .login-title {
                font-size: 1.5rem !important;
                margin-bottom: 0.3rem !important;
                line-height: 1.2 !important;
            }
            
            .login-subtitle {
                font-size: 0.8rem !important;
                margin-bottom: 0.5rem !important;
                line-height: 1.2 !important;
            }
            
            /* Compact input spacing */
            .stTextInput {
                margin-bottom: 0.4rem !important;
                margin-top: 0 !important;
            }
            
            .stTextInput input {
                padding: 0.6rem 1rem !important;
                font-size: 0.9rem !important;
            }
            
            .stTextInput label {
                font-size: 0.85rem !important;
                margin-bottom: 0.3rem !important;
            }
            
            .stButton > button {
                margin-top: 0.2rem !important;
                padding: 0.65rem 1.5rem !important;
                font-size: 0.95rem !important;
            }
            
            /* Compact error messages */
            .stAlert {
                padding: 0.4rem 0.75rem !important;
                font-size: 0.8rem !important;
                margin-top: 0.4rem !important;
            }
            
            /* Reduce column spacing */
            [data-testid="column"] {
                padding: 0 0.5rem !important;
            }
            
            /* Hide scrollbars completely on login page */
            ::-webkit-scrollbar {
                display: none !important;
                width: 0 !important;
                height: 0 !important;
            }
            
            * {
                scrollbar-width: none !important;
                -ms-overflow-style: none !important;
            }
            
            /* Center the login form content */
            .element-container {
                width: 100% !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Create centered login card with custom HTML
    st.markdown("""
        <div class="login-card">
            <h1 class="login-title">Business Problem Analysis Platform</h1>
            <p class="login-subtitle">AI-powered agents to extract vocabulary, analyze systems, and classify business problem dimensions</p>
        </div>
    """, unsafe_allow_html=True)

    # Create a centered container for the form
    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col2:
        employee_id = st.text_input(
            "Employee ID",
            placeholder="Enter your employee ID...",
            key="employee_id_input",
            label_visibility="visible"
        )

        if st.button("Login", use_container_width=True):
            if employee_id:
                st.session_state.employee_id = employee_id
                st.session_state.page = "main_app"
                st.rerun()
            else:
                st.error("⚠️ Please enter a valid Employee ID.")


def render_main_app():
    # --- Theme Toggle ---
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False

    # --- Custom Styling with Theme Support ---
    if st.session_state.dark_mode:
        # DARK MODE
        st.markdown("""
        <style>
            /* SUPER AGGRESSIVE DROPDOWN FIX - FORCE ORANGE BACKGROUND */
            [data-baseweb="popover"],
            [data-baseweb="popover"] > *,
            [data-baseweb="popover"] > * > *,
            [data-baseweb="popover"] > * > * > *,
            [data-baseweb="popover"] div,
            ul[role="listbox"],
            [role="listbox"],
            [role="listbox"] > *,
            [role="listbox"] div {
                background-color: #ff6b35 !important;
                background: #ff6b35 !important;
            }
            
            /* CSS Variables for Dark Mode */
            :root {
                --musigma-red: #8b1e1e;
                --accent-orange: #ff6b35;
                --accent-purple: #7c3aed;
                --text-primary: #f3f4f6;
                --text-secondary: #9ca3af;
                --text-light: #ffffff;
                --bg-card: #23272f;
                --bg-app: #0b0f14;
                --border-color: rgba(255,255,255,0.06);
                --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
                --shadow-md: 0 4px 6px rgba(0,0,0,0.4);
                --shadow-lg: 0 10px 15px rgba(0,0,0,0.5);
            }
            
            /* Dark overall background */
            body, .stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                background: linear-gradient(135deg, #0b0f14 0%, #18181b 50%, #23272f 100%) !important;
                color: var(--text-primary) !important;
            }
            
            /* Sidebar background in dark mode */
            [data-testid="stSidebar"] {
                background: linear-gradient(135deg, #0b0f14 0%, #18181b 100%) !important;
            }

            /* SELECT BOXES STYLING - Compact and consistent */
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
                background-color: #1f2933 !important;
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

            /* Dropdown popover container - VERY AGGRESSIVE - ORANGE */
            [data-baseweb="popover"],
            [data-baseweb="popover"] *,
            div[data-baseweb="popover"],
            [data-baseweb="popover"] > div,
            [data-baseweb="popover"] > div > div {
                background-color: #ff6b35 !important;
                background: #ff6b35 !important;
            }
            
            [data-baseweb="popover"] {
                border-radius: 16px !important;
                box-shadow: var(--shadow-lg) !important;
            }
            
            /* Dropdown options styling - VERY AGGRESSIVE - ORANGE */
            ul[role="listbox"],
            ul[role="listbox"] *,
            [role="listbox"],
            div[role="listbox"] {
                background-color: #ff6b35 !important;
                background: #ff6b35 !important;
            }
            
            ul[role="listbox"] {
                border: 2px solid rgba(255, 107, 53, 0.3) !important;
                border-radius: 16px !important;
                box-shadow: var(--shadow-lg) !important;
                padding: 0.5rem !important;
                max-height: 280px !important;
                overflow-y: auto !important;
            }

            li[role="option"] {
                color: #000000 !important;
                background-color: transparent !important;
                padding: 10px 14px !important;
                font-size: 0.95rem !important;
                border-radius: 10px !important;
                transition: all 0.2s ease !important;
                font-weight: 600 !important;
            }

            li[role="option"]:hover {
                background-color: rgba(139, 30, 30, 0.8) !important;
                color: #ffffff !important;
                transform: translateX(5px) !important;
            }

            li[role="option"][aria-selected="true"] {
                background-color: var(--musigma-red) !important;
                color: #ffffff !important;
                font-weight: 700 !important;
            }
            
            /* Ensure dropdown text is visible - BLACK ON ORANGE */
            li[role="option"] div,
            li[role="option"] span {
                color: #000000 !important;
                font-weight: 600 !important;
            }
            
            li[role="option"]:hover div,
            li[role="option"]:hover span {
                color: var(--text-light) !important;
            }
            
            li[role="option"][aria-selected="true"] div,
            li[role="option"][aria-selected="true"] span {
                color: var(--text-light) !important;
            }

            /* TEXT AREA STYLING */
            .stTextArea textarea {
                background: var(--bg-card) !important;
                border: 2px solid var(--border-color) !important;
                border-radius: 16px !important;
                color: var(--text-primary) !important;
                font-size: 1.05rem !important;
                box-shadow: var(--shadow-sm);
                padding: 1.25rem !important;
                line-height: 1.7 !important;
                min-height: 180px !important;
            }

            .stTextArea textarea::placeholder {
                color: var(--text-secondary) !important;
                opacity: 0.7 !important;
            }

            /* BUTTON STYLING */
            .stButton > button {
                background: linear-gradient(135deg, var(--musigma-red) 0%, var(--accent-orange) 100%);
                color: var(--text-light) !important;
                border: none;
                border-radius: 16px;
                padding: 1.1rem 2.75rem;
                font-weight: 700;
                font-size: 1.1rem;
                box-shadow: var(--shadow-md);
            }

            .stButton > button:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(255, 107, 53, 0.5);
            }
            
            /* SECTION TITLE BOXES - DARK MODE */
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
            /* CSS Variables for Light Mode */
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

            /* SELECT BOXES STYLING - Compact and consistent */
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
            }

            /* TEXT AREA STYLING */
            .stTextArea textarea {
                background: var(--bg-card) !important;
                border: 2px solid var(--border-color) !important;
                border-radius: 16px !important;
                color: var(--text-primary) !important;
                font-size: 1.05rem !important;
                box-shadow: var(--shadow-sm);
                padding: 1.25rem !important;
                line-height: 1.7 !important;
                min-height: 180px !important;
            }

            .stTextArea textarea::placeholder {
                color: var(--text-secondary) !important;
                opacity: 0.7 !important;
            }

            /* BUTTON STYLING */
            .stButton > button {
                background: linear-gradient(135deg, var(--musigma-red) 0%, var(--accent-orange) 100%);
                color: var(--text-light) !important;
                border: none;
                border-radius: 16px;
                padding: 1.1rem 2.75rem;
                font-weight: 700;
                font-size: 1.1rem;
                box-shadow: var(--shadow-md);
            }

            .stButton > button:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(139, 30, 30, 0.4);
            }
            
            /* SECTION TITLE BOXES - LIGHT MODE */
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
            
            /* All text elements readable in light mode */
            h1, h2, h3, h4, h5, h6, p, span, div, label {
                color: var(--text-primary) !important;
            }
        </style>
        """, unsafe_allow_html=True)

    # Begin scrollable area after CSS injections
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)

    # --- Account & Industry Section ---
    st.markdown(
        '<div class="section-title-box"><h3>Account & Industry</h3></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Track if we need to show confirmation dialog (before rendering dropdowns)
    show_confirmation = False
    account_change_value = None

    with col1:
        # Account Dropdown with dynamic key to force refresh after cancel
        account_input = st.selectbox(
            "Select Account:",
            options=ACCOUNTS,
            index=ACCOUNTS.index(
                st.session_state.business_account) if st.session_state.business_account in ACCOUNTS else 0,
            key=f"account_select_{st.session_state.selectbox_key_counter}"
        )

        # Detect if user actually changed the account from what's stored in business_account
        if account_input != st.session_state.business_account:
            # Check if user just clicked cancel - if so, skip all logic this render
            if st.session_state.cancel_clicked:
                # Reset the flag and don't show dialog
                st.session_state.cancel_clicked = False
                # Don't process any changes - the values are already restored from cancel button
                # Just skip to rendering the dropdowns with restored values
                pass
            elif st.session_state.saved_problem and not st.session_state.edit_confirmed:
                # Mark that we need to show confirmation dialog after columns
                show_confirmation = True
                account_change_value = account_input
            else:
                # No saved data yet, or already confirmed - allow change freely
                st.session_state.business_account = account_input
                # Auto-map industry
                if account_input in ACCOUNT_INDUSTRY_MAP:
                    st.session_state.business_industry = ACCOUNT_INDUSTRY_MAP[account_input]

    with col2:
        # Industry dropdown with dynamic key to force refresh after cancel
        current_industry = st.session_state.business_industry
        current_account = st.session_state.business_account
        is_auto_mapped = current_account in ACCOUNT_INDUSTRY_MAP

        industry_input = st.selectbox(
            "Industry:",
            options=INDUSTRIES,
            index=INDUSTRIES.index(
                current_industry) if current_industry in INDUSTRIES else 0,
            disabled=is_auto_mapped,
            help="Industry is automatically mapped for this account" if is_auto_mapped else "Select the industry for this analysis",
            key=f"industry_select_{st.session_state.selectbox_key_counter}"
        )

        # Update session state if manually selected (not auto-mapped)
        if not is_auto_mapped and industry_input != st.session_state.business_industry:
            st.session_state.business_industry = industry_input

    # Show confirmation dialog AFTER both columns if needed
    if show_confirmation:
        st.markdown("""
            <style>
            .confirmation-box {
                background: linear-gradient(135deg, rgba(255,107,53,0.08), rgba(124,58,237,0.08));
                border: 2px solid rgba(255,107,53,0.25);
                border-radius: 12px;
                padding: 18px 24px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin: 15px 0;
            }
            .confirmation-message {
                color: #ff6b35;
                font-size: 15px;
                font-weight: 600;
                margin-bottom: 0;
                text-align: center;
            }
            </style>
        """, unsafe_allow_html=True)

        # Create the info box container
        st.markdown("""
            <div class="confirmation-box">
                <div class="confirmation-message">
                    💡 <strong>Proceed with new problem?</strong><br>
                    <span style="font-size: 13px; font-weight: 400; color: #555;">Changing the account will update your business problem details.</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Small cute buttons centered
        col1, col2, col3, col4, col5 = st.columns([3, 1.2, 0.6, 1.2, 3])

        with col2:
            yes_btn = st.button("Yes", key="confirm_edit", type="primary")
            if yes_btn:
                st.session_state.edit_confirmed = True
                st.session_state.business_account = account_change_value
                if account_change_value in ACCOUNT_INDUSTRY_MAP:
                    st.session_state.business_industry = ACCOUNT_INDUSTRY_MAP[account_change_value]
                st.session_state.selectbox_key_counter += 1
                st.rerun()

        with col4:
            no_btn = st.button("No", key="cancel_edit", type="secondary")
            if no_btn:
                st.session_state.cancel_clicked = True
                st.session_state.business_account = st.session_state.saved_account
                st.session_state.business_industry = st.session_state.saved_industry
                st.session_state.selectbox_key_counter += 1
                st.rerun()

        # Add CSS for small cute buttons
        st.markdown("""
            <style>
            /* Small cute buttons */
            button[kind="primary"],
            button[kind="secondary"] {
                padding: 0.35rem 0.9rem !important;
                min-height: 36px !important;
                max-height: 36px !important;
                border-radius: 8px !important;
                font-size: 0.85rem !important;
                font-weight: 600 !important;
            }
            </style>
        """, unsafe_allow_html=True)

    # --- Business Problem Section ---
    st.markdown(
        '<div class="section-title-box"><h3>Business Problem Description</h3></div>', unsafe_allow_html=True)

    problem_input = st.text_area(
        "Describe your business problem in detail:",
        value=st.session_state.business_problem,
        height=180,
        placeholder="Feel free to just type down your problem statement, or copy-paste if you have it handy somewhere...",
        label_visibility="collapsed"
    )

    # Update business_problem from text area
    if problem_input != st.session_state.business_problem:
        st.session_state.business_problem = problem_input

    # --- Save Button ---
    if st.button("✅ Save Problem Details", use_container_width=True, type="primary"):
        # Validate inputs
        if st.session_state.business_account == "Select Account" or st.session_state.business_industry == "Select Industry" or not st.session_state.business_problem.strip():
            st.error(
                "⚠️ Please select an Account, Industry, and provide a Business Problem description.")
        else:
            # SAVE to persistent variables that won't be affected by widget changes
            st.session_state.saved_account = st.session_state.business_account
            st.session_state.saved_industry = st.session_state.business_industry
            st.session_state.saved_problem = st.session_state.business_problem
            # Reset edit confirmation flag
            st.session_state.edit_confirmed = False
            st.success("✅ Problem details saved! You can now launch an agent.")
            st.rerun()

    st.markdown("---")
    st.markdown("### 🤖 Available Agents")

    # --- Agent Definitions - All 7 Agents ---
    agents = [
        {"name": "Vocabulary Agent", "icon": "📚",
            "page": "pages/1__Vocabulary_Agent.py"},
        {"name": "Current System Agent", "icon": "⚙️",
            "page": "pages/2__Current_System_Agent.py"},
        {"name": "Volatility Agent", "icon": "📊",
            "page": "pages/3__Volatility_Agent.py"},
        {"name": "Ambiguity Agent", "icon": "❓",
            "page": "pages/4__Ambiguity_Agent.py"},
        {"name": "Interconnectedness Agent", "icon": "🔗",
            "page": "pages/5__Interconnectedness_Agent.py"},
        {"name": "Uncertainty Agent", "icon": "🎲",
            "page": "pages/6__Uncertainty_Agent.py"},
        {"name": "Hardness Summary Agent", "icon": "💪",
            "page": "pages/7__Hardness_Summary_Agent.py"},
    ]

    # --- Show Active Agent Status ---
    if st.session_state.launched_agent:
        # Find which agent is active
        active_agent = next(
            (agent for agent in agents if agent["page"] == st.session_state.launched_agent), None)
        if active_agent:
            st.info(f"""
            🔒 **Active Agent:** {active_agent['icon']} {active_agent['name']}
            
            You are currently working with the **{active_agent['name']}**. You can only access this agent during this session.
            To change agents, please use "🚪 Logout & Start Over" button below.
            """)

            # Quick return button to active agent
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(f"↩️ Return to {active_agent['icon']} {active_agent['name']}", use_container_width=True, type="primary"):
                    st.switch_page(active_agent["page"])

    # --- Agent Launch Buttons (3 columns x 3 rows) ---
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # First row - 3 agents
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            agent = agents[i]
            is_disabled = (
                st.session_state.launched_agent is not None and st.session_state.launched_agent != agent["page"])
            if st.button(f"{agent['icon']} {agent['name']}", use_container_width=True, disabled=is_disabled, type="secondary", key=f"agent_{i}"):
                if st.session_state.saved_problem:  # Check SAVED problem
                    st.session_state.launched_agent = agent["page"]
                    st.switch_page(agent["page"])
                else:
                    st.warning(
                        "Please save your business problem details before launching an agent.")

    # Second row - 3 agents
    cols = st.columns(3)
    for i in range(3, 6):
        with cols[i-3]:
            agent = agents[i]
            is_disabled = (
                st.session_state.launched_agent is not None and st.session_state.launched_agent != agent["page"])
            if st.button(f"{agent['icon']} {agent['name']}", use_container_width=True, disabled=is_disabled, type="secondary", key=f"agent_{i}"):
                if st.session_state.saved_problem:  # Check SAVED problem
                    st.session_state.launched_agent = agent["page"]
                    st.switch_page(agent["page"])
                else:
                    st.warning(
                        "Please save your business problem details before launching an agent.")

    # Third row - 1 agent (centered)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        agent = agents[6]
        is_disabled = (
            st.session_state.launched_agent is not None and st.session_state.launched_agent != agent["page"])
        if st.button(f"{agent['icon']} {agent['name']}", use_container_width=True, disabled=is_disabled, type="secondary", key=f"agent_6"):
            if st.session_state.saved_problem:  # Check SAVED problem
                st.session_state.launched_agent = agent["page"]
                st.switch_page(agent["page"])
            else:
                st.warning(
                    "Please save your business problem details before launching an agent.")

    # --- Logout Button ---
    st.markdown("---")
    if st.button("🚪 Logout & Start Over", use_container_width=True):
        # Save employee ID and current data before clearing
        eid = st.session_state.employee_id
        saved_acc = st.session_state.get("saved_account", "Select Account")
        saved_ind = st.session_state.get("saved_industry", "Select Industry")
        saved_prob = st.session_state.get("saved_problem", "")

        # Clear only the launched_agent to unlock all agents
        # Keep the saved data so user can continue with same inputs or change them
        st.session_state.launched_agent = None

        # Reset edit confirmation flag
        st.session_state.edit_confirmed = False

        # Keep the saved data intact
        st.session_state.saved_account = saved_acc
        st.session_state.saved_industry = saved_ind
        st.session_state.saved_problem = saved_prob

        st.success(
            "✅ Session reset! You can now choose a different agent or modify your inputs.")
        st.rerun()

    # End scrollable area
    st.markdown('</div>', unsafe_allow_html=True)


# --- PAGE ROUTER ---
if st.session_state.page == "login":
    render_login_page()
elif st.session_state.page == "main_app":
    # Render main app (it will create the scrollable container internally)
    render_main_app()
