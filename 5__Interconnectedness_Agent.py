import streamlit as st
from shared_header import (
    render_header,
    render_unified_business_inputs,
)

# --- Page Config ---
st.set_page_config(
    page_title="Interconnectedness Agent",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom Styling (Match Welcome Agent) ---
if st.session_state.get('dark_mode', False):
    st.markdown("""
    <style>
        :root {
            --musigma-red: #8b1e1e; --accent-orange: #ff6b35; --accent-purple: #7c3aed;
            --text-primary: #f3f4f6; --text-secondary: #9ca3af; --text-light: #ffffff;
            --bg-card: #23272f; --bg-app: #0b0f14; --border-color: rgba(255,255,255,0.12);
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.3); --shadow-md: 0 4px 6px rgba(0,0,0,0.4); --shadow-lg: 0 10px 25px rgba(0,0,0,0.5);
        }
        body, .stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background: linear-gradient(135deg, #0b0f14 0%, #18181b 50%, #23272f 100%) !important;
            color: var(--text-primary) !important;
        }
        .section-title-box { background: linear-gradient(135deg, var(--musigma-red) 0%, var(--accent-orange) 100%) !important; border-radius: 16px; padding: 1rem 2rem !important; margin: 0 0 0.5rem 0 !important; box-shadow: var(--shadow-lg) !important; text-align: center; }
        .bpd-title { margin-top: 2.5rem !important; }
        .section-title-box h3 { color: var(--text-light) !important; margin: 0 !important; font-weight: 700 !important; font-size: 1.3rem !important; }
        .stSelectbox { margin-bottom: 1rem; }
        .stSelectbox > label { font-weight: 600 !important; font-size: 0.875rem !important; color: var(--text-primary) !important; margin-bottom: 0.35rem !important; }
        .stSelectbox > div > div { background-color: rgba(35, 39, 47, 0.8) !important; border: 2px solid rgba(255, 107, 53, 0.3) !important; border-radius: 16px !important; padding: 0.35rem 0.65rem !important; min-height: 38px !important; max-height: 38px !important; box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3); transition: all 0.3s ease; display: flex !important; align-items: center !important; }
        .stSelectbox > div > div:hover { border-color: var(--accent-orange) !important; box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.2), inset 0 2px 4px rgba(0, 0, 0, 0.3); }
        .stSelectbox [data-baseweb="select"] { background-color: transparent !important; min-height: 32px !important; max-height: 32px !important; }
        .stSelectbox [data-baseweb="select"] > div { color: var(--text-light) !important; font-size: 0.9rem !important; font-weight: 500 !important; line-height: 1.3 !important; padding: 0 !important; }
        [data-baseweb="popover"], ul[role="listbox"] { background-color: var(--bg-card) !important; border: 2px solid var(--border-color) !important; border-radius: 16px !important; box-shadow: var(--shadow-lg) !important; }
        li[role="option"] { color: var(--text-light) !important; padding: 10px 14px !important; font-size: 0.95rem !important; border-radius: 10px !important; transition: all 0.2s ease !important; }
        li[role="option"]:hover { background-color: rgba(124, 58, 237, 0.2) !important; color: var(--accent-purple) !important; transform: translateX(5px) !important; }
        li[role="option"][aria-selected="true"] { background-color: rgba(255, 107, 53, 0.2) !important; color: var(--accent-orange) !important; font-weight: 600 !important; }
        .stTextArea > label { font-weight: 600 !important; font-size: 0.875rem !important; color: var(--text-primary) !important; margin-bottom: 0.35rem !important; }
        .stTextArea textarea { background: rgba(35, 39, 47, 0.8) !important; border: 2px solid rgba(255, 107, 53, 0.3) !important; border-radius: 16px !important; color: var(--text-light) !important; font-size: 1.05rem !important; box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3); padding: 1.25rem !important; line-height: 1.7 !important; min-height: 150px !important; transition: all 0.3s ease; }
        .stTextArea textarea:focus { border-color: var(--accent-orange) !important; box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.2), inset 0 2px 4px rgba(0, 0, 0, 0.3) !important; }
        .stTextArea textarea:disabled { background: rgba(35, 39, 47, 0.8) !important; color: var(--text-secondary) !important; filter: brightness(0.9); }
        h1, h2, h3, h4, h5, h6, p, span, div, label { color: var(--text-primary) !important; }
        .stAlert, [data-testid="stNotification"] { background-color: var(--bg-card) !important; color: var(--text-primary) !important; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        :root {
            --musigma-red: #8b1e1e; --accent-orange: #ff6b35; --accent-purple: #7c3aed;
            --text-primary: #1e293b; --text-secondary: #6b7280; --text-light: #ffffff;
            --bg-card: #ffffff; --bg-app: #fafafa; --border-color: #e5e7eb;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05); --shadow-md: 0 4px 6px rgba(0,0,0,0.1); --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
        }
        body, .stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 50%, #eeeeee 100%) !important;
            color: var(--text-primary) !important;
        }
        .section-title-box { background: linear-gradient(135deg, var(--musigma-red) 0%, var(--accent-orange) 100%) !important; border-radius: 16px; padding: 1rem 2rem; margin: 0 0 0.5rem 0 !important; box-shadow: var(--shadow-lg) !important; text-align: center; }
        .bpd-title { margin-top: 2.5rem !important; }
        .section-title-box h3 { color: var(--text-light) !important; margin: 0 !important; font-weight: 700 !important; font-size: 1.3rem !important; }
        .stSelectbox { margin-bottom: 1rem; }
        .stSelectbox > label { font-weight: 600 !important; font-size: 0.875rem !important; color: var(--text-primary) !important; margin-bottom: 0.35rem !important; }
        .stSelectbox > div > div { background-color: var(--bg-card) !important; border: 2px solid var(--border-color) !important; border-radius: 16px !important; padding: 0.35rem 0.65rem !important; min-height: 38px !important; max-height: 38px !important; box-shadow: var(--shadow-sm); transition: all 0.3s ease; display: flex !important; align-items: center !important; }
        .stSelectbox > div > div:hover { border-color: var(--accent-purple) !important; box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2); }
        .stSelectbox [data-baseweb="select"] { background-color: transparent !important; min-height: 32px !important; max-height: 32px !important; }
        .stSelectbox [data-baseweb="select"] > div { color: var(--text-primary) !important; font-size: 0.9rem !important; font-weight: 500 !important; line-height: 1.3 !important; padding: 0 !important; }
        [data-baseweb="popover"], ul[role="listbox"] { background-color: var(--bg-card) !important; border: 2px solid var(--border-color) !important; border-radius: 16px !important; box-shadow: var(--shadow-lg) !important; }
        li[role="option"] { color: var(--text-primary) !important; padding: 10px 14px !important; font-size: 0.95rem !important; border-radius: 10px !important; transition: all 0.2s ease !important; }
        li[role="option"]:hover { background-color: rgba(124, 58, 237, 0.1) !important; color: var(--accent-purple) !important; transform: translateX(5px) !important; }
        li[role="option"][aria-selected="true"] { background-color: rgba(139, 30, 30, 0.15) !important; color: var(--musigma-red) !important; font-weight: 600 !important; }
        .stTextArea > label { font-weight: 600 !important; font-size: 0.875rem !important; color: var(--text-primary) !important; margin-bottom: 0.35rem !important; }
        .stTextArea textarea { background: var(--bg-card) !important; border: 2px solid var(--border-color) !important; border-radius: 16px !important; color: var(--text-primary) !important; font-size: 1.05rem !important; box-shadow: var(--shadow-sm); padding: 1.25rem !important; line-height: 1.7 !important; min-height: 150px !important; transition: all 0.3s ease; }
        .stTextArea textarea:focus { border-color: var(--accent-orange) !important; box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15), 0 2px 4px rgba(0, 0, 0, 0.05) !important; }
        .stTextArea textarea:disabled { background: var(--bg-card) !important; color: var(--text-primary) !important; filter: brightness(0.97); }
        .stAlert, [data-testid="stNotification"] { background-color: var(--bg-card) !important; color: var(--text-primary) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Initialize session state ---
if 'saved_account' not in st.session_state:
    st.session_state.saved_account = "Select Account"
if 'saved_industry' not in st.session_state:
    st.session_state.saved_industry = "Select Industry"
if 'saved_problem' not in st.session_state:
    st.session_state.saved_problem = ""
if 'enable_edit_interconnect' not in st.session_state:
    st.session_state.enable_edit_interconnect = False

# --- Render Header ---
render_header(
    agent_name="Interconnectedness Agent",
    agent_subtitle="Reviewing the business problem statement."
)

# Begin scrollable content wrapper
st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)

account, industry, problem = render_unified_business_inputs(
    page_key_prefix="interconnect",
    show_titles=True,
    title_account_industry="Account & Industry",
    title_problem="Business Problem Description",
    save_button_label="✅ Save Problem Details",
)

# --- Agent Analysis Section ---
st.markdown("---")
st.markdown("### 🔗 Interconnectedness Analysis")
st.success(f"""
This agent maps system dependencies and interconnections for **{account}** in the **{industry}** industry.

The analysis would identify how different components, stakeholders, and processes are linked in the business problem.
""")

# --- Back Button ---
st.markdown("---")
if st.button("⬅️ Back to Main Page"):
    # Keep launched_agent set - user remains locked to this agent
    st.switch_page("Welcome_Agent.py")

# End scrollable content wrapper
st.markdown('</div>', unsafe_allow_html=True)
