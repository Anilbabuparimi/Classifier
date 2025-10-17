import streamlit as st
from shared_header import render_header, render_unified_business_inputs

# --- Page Config ---
st.set_page_config(
    page_title="Hardness Summary Agent",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --- Initialize session state ---
if 'saved_account' not in st.session_state:
    st.session_state.saved_account = "Select Account"
if 'saved_industry' not in st.session_state:
    st.session_state.saved_industry = "Select Industry"
if 'saved_problem' not in st.session_state:
    st.session_state.saved_problem = ""
if 'enable_edit_hardness' not in st.session_state:
    st.session_state.enable_edit_hardness = False

# --- Render Header ---
render_header(
    agent_name="Hardness Summary Agent",
    agent_subtitle="Reviewing the business problem statement."
)

# Begin scrollable content wrapper
st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)

# Retrieve data
account, industry, problem = render_unified_business_inputs(
    page_key_prefix="hardness",
    show_titles=True,
    title_account_industry="Account & Industry",
    title_problem="Business Problem Description",
    save_button_label="✅ Save Problem Details",
)

 

# End scrollable content wrapper
st.markdown('</div>', unsafe_allow_html=True)

# --- Agent Analysis Section ---
st.markdown("---")
st.markdown("### 🧩 Comprehensive Hardness Analysis")
st.success(f"""
This agent provides a comprehensive problem hardness summary for **{account}** in the **{industry}** industry.

The analysis synthesizes insights from Vocabulary, Current System, Volatility, Ambiguity, Interconnectedness, and Uncertainty agents to provide an overall complexity assessment.
""")

# --- Back Button ---
st.markdown("---")
if st.button("⬅️ Back to Main Page"):
    # Keep launched_agent set - user remains locked to this agent
    st.switch_page("Welcome_Agent.py")
