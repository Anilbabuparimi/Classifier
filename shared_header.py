"""
Shared header component for all agents
This provides consistent header with logo, title, and theme toggle across all agents
"""
import streamlit as st
import streamlit.components.v1 as components
import os
import pandas as pd

# Logo URL for the header
LOGO_URL = "https://yt3.googleusercontent.com/ytc/AIdro_k-7HkbByPWjKpVPO3LCF8XYlKuQuwROO0vf3zo1cqgoaE=s900-c-k-c0x00ffffff-no-rj"

# Feedback file path for admin section
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # agents/
FEEDBACK_FILE = os.path.join(BASE_DIR, "feedback.csv")

# ================================
# 🏢 Account & Industry Mapping (Expanded + Stable Auto-Mapping)
# ================================

ACCOUNT_INDUSTRY_MAP = {
    "Select Account": "Select Industry",

    # --- Pharmaceutical & Healthcare ---
    "Abbott Ireland": "Pharma",
    "Abbott Laboratories": "Pharma",
    "Abbvie": "Pharma",
    "BMS Germany": "Pharma",
    "BMS Japan": "Pharma",
    "Bristol-Myers Squibb": "Pharma",
    "Envista": "Healthcare",
    "Gilead Sciences, Inc.": "Pharma",
    "J&J Inc": "Pharma",
    "J&J Japan": "Pharma",
    "J&J Singapore": "Pharma",
    "Novartis": "Pharma",
    "Sanofi": "Pharma",

    # --- Technology ---
    "Dell": "Technology",
    "Microsoft": "Technology",
    "RECURSION": "Technology",

    # --- Energy & Oil/Gas ---
    "Chevron India": "Energy",
    "CHEVRON U.S.A. INC.": "Energy",
    "OXY": "Energy",
    "SABIC": "Energy",

    # --- Financial Services ---
    "BMO": "Finance",
    "Citigroup": "Finance",

    # --- Retail & Consumer Goods ---
    "Coles": "Retail",
    "Home Depot": "Retail",
    "Nike": "Consumer Goods",
    "THD": "Retail",
    "Walmart": "Retail",
    "Walmart Mexico": "Retail",

    # --- Food & Beverage ---
    "ADM": "Food & Beverage",
    "Mars": "Consumer Goods",
    "MARS China": "Consumer Goods",

    # --- Airlines & Aviation ---
    "Southwest": "Airlines",

    # --- Telecommunications ---
    "T Mobile": "Telecom",

    # --- Travel & Hospitality ---
    "NCLH": "Hospitality",

    # --- Aerospace & Defense ---
    "RTX": "Aerospace",

    # --- Consulting & Services ---
    "Itkan": "Technology",
    "Loyalty Pacific": "Services",
    "Skills Development": "Education",

    # --- Others ---
    "Others": "Other"
}

# --- All accounts (alphabetically sorted, with Others at the end) ---
ALL_ACCOUNTS = [
    acc for acc in ACCOUNT_INDUSTRY_MAP.keys()
    if acc != "Select Account" and acc != "Others"
]
ALL_ACCOUNTS.sort()
# Add "Others" at the end
ALL_ACCOUNTS.append("Others")

# --- Final ordered account list ---
ACCOUNTS = ["Select Account"] + ALL_ACCOUNTS

# --- Unique Industries ---
all_industries = list(set(ACCOUNT_INDUSTRY_MAP.values()))
INDUSTRIES = sorted([i for i in all_industries if i != "Select Industry"])
if "Other" not in INDUSTRIES:
    INDUSTRIES.append("Other")
INDUSTRIES = ["Select Industry"] + INDUSTRIES



def render_header(agent_name="Agent Platform", agent_subtitle="AI-powered business analysis", enable_admin_access=True):
    """
    Render a fixed arch-shaped header with Mu Sigma logo (white circular button, clickable for admin), heading centered, Mu Sigma red background, and dark/light mode toggle at top right inside the arch.
    """
    st.markdown(
        f"""
        <style>
        .fixed-app-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            z-index: 1000;
            background: linear-gradient(90deg, #8b1e1e 0%, #ff6b35 100%);
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
            padding: 0.7rem 0.7rem 0.7rem 0.7rem;
        }}
        .header-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header-logo-btn {{
            border: none;
            background: none;
            padding: 0;
            margin: 0;
            cursor: pointer;
            outline: none;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 60px;
        }}
        .header-logo-circle {{
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: #fff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.10);
            border: 3px solid #fff;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .header-logo-img {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            object-fit: cover;
        }}
        .header-title-block {{
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        .header-title {{
            font-size: 2.1rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 0.10rem;
            letter-spacing: 0.5px;
            text-align: center;
        }}
        .header-subtitle {{
            font-size: 1.15rem;
            color: #f3f4f6;
            font-weight: 400;
            margin-top: 0.10rem;
            text-align: center;
        }}
        .header-toggle {{
            margin-left: 1.5rem;
            display: flex;
            align-items: center;
        }}
        .stApp {{ padding-top: 80px !important; }}
        </style>
        <div class="fixed-app-header">
            <div class="header-row">
                <form method="post" style="margin:0;padding:0;">
                    <button class="header-logo-btn" name="admin_logo_btn" type="submit" title="Admin access">
                        <span class="header-logo-circle">
                            <img src="{LOGO_URL}" class="header-logo-img" alt="Mu Sigma Logo" />
                        </span>
                    </button>
                </form>
                <div class="header-title-block">
                    <div class="header-title">{agent_name}</div>
                    <div class="header-subtitle">{agent_subtitle}</div>
                </div>
                <div class="header-toggle" id="header-toggle"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Handle logo click for admin access (Streamlit-native)
    if enable_admin_access:
        if st.button("", key="admin_logo_btn", help="Admin access", use_container_width=False):
            st.session_state.current_page = 'admin'
            st.rerun()

    # Dark/Light mode toggle inside header (top right)
    dark_mode = st.session_state.get('dark_mode', False)
    st.markdown("<div style='position:fixed;right:56px;top:28px;z-index:1101;'>", unsafe_allow_html=True)
    toggle = st.toggle("🌙 Dark Mode", value=dark_mode, key="dark_mode_toggle", help="Toggle dark/light mode")
    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state.dark_mode = toggle
    if toggle != dark_mode:
        st.rerun()

    # Add vertical space after header
    st.write("")

def render_admin_section():
    """
    Render the admin section with password protection and feedback download
    This is called when the logo is clicked and admin mode is activated
    """
    # Check session state for admin page
    if st.session_state.get('current_page', '') == 'admin':
        st.markdown("""
        <style>
        :root {
            --musigma-red: #8b1e1e;
            --accent-orange: #ff6b35;
            --accent-purple: #7c3aed;
            --text-primary: #1a1a1a;
            --text-secondary: #6b7280;
            --text-light: #ffffff;
            --bg-card: #ffffff;
            --bg-app: #fafafa;
            --border-color: #e5e7eb;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
        }

        .section-title-box {
            background: linear-gradient(135deg, var(--musigma-red) 0%, var(--accent-orange) 100%) !important;
            border-radius: 16px;
            padding: 0.65rem 1.5rem !important;
            margin: 0.5rem 0 1rem 0 !important;
            box-shadow: var(--shadow-lg) !important;
            text-align: center;
        }
        .section-title-box h3 {
            color: var(--text-light) !important;
            margin: 0 !important;
            font-weight: 700 !important;
            font-size: 1.15rem !important;
            line-height: 1.3 !important;
            text-align: center !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
        st.markdown('<div class="section-title-box"><h3>📊 Admin Panel</h3></div>',
                    unsafe_allow_html=True)

        # Back button to return to main app
        if st.button("← Back to Agent", use_container_width=True):
            st.session_state.current_page = ''
            # Clear query params and reload
            try:
                if hasattr(st, 'query_params'):
                    st.query_params.clear()
            except:
                pass
            st.rerun()

        # Password protection
        if 'admin_authenticated' not in st.session_state:
            st.session_state.admin_authenticated = False

        if not st.session_state.admin_authenticated:
            st.markdown("### 🔒 Authentication Required")
            password = st.text_input(
                "Enter Admin Password:", type="password", key="admin_password_input")

            # Get password from secrets or environment
            try:
                admin_password = st.secrets.get(
                    "ADMIN_PASSWORD", os.environ.get("ADMIN_PASSWORD", "admin123"))
            except:
                admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")

            if st.button("Access Admin Panel", use_container_width=True):
                if password == admin_password:
                    st.session_state.admin_authenticated = True
                    st.success("✅ Access granted!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password")
        else:
            # Admin panel content
            st.markdown("### 📥 Download Feedback Report")

            # Check if feedback file exists
            if os.path.exists(FEEDBACK_FILE):
                try:
                    df = pd.read_csv(FEEDBACK_FILE)

                    if len(df) > 0:
                        # Filter options
                        filter_option = st.selectbox(
                            "Filter Feedback:",
                            ["All Feedback", "Positive Feedback",
                                "Definitions Off", "Suggestions"],
                            key="admin_filter_select"
                        )

                        # Apply filter
                        if filter_option == "Positive Feedback":
                            filtered_df = df[df['FeedbackType'] == 'positive']
                        elif filter_option == "Definitions Off":
                            filtered_df = df[df['FeedbackType']
                                             == 'definitions_off']
                        elif filter_option == "Suggestions":
                            filtered_df = df[df['FeedbackType']
                                             == 'suggestions']
                        else:
                            filtered_df = df

                        # Display count
                        st.info(
                            f"📊 Showing {len(filtered_df)} of {len(df)} feedback entries")

                        # Display table with full width
                        st.dataframe(
                            filtered_df, use_container_width=True, height=400)

                        # Download button
                        csv = filtered_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Filtered Report (CSV)",
                            data=csv,
                            file_name=f"feedback_report_{filter_option.lower().replace(' ', '_')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    else:
                        st.warning("No feedback data available yet.")
                except Exception as e:
                    st.error(f"Error loading feedback: {str(e)}")
            else:
                st.warning(f"Feedback file not found at: {FEEDBACK_FILE}")

        st.markdown('</div>', unsafe_allow_html=True)


def get_shared_data():
    """
    Get shared data from session state or URL parameters
    Returns a dictionary with employee_id, account, industry, and problem
    """
    # Initialize data dictionary
    data = {
        'employee_id': '',
        'account': '',
        'industry': '',
        'problem': ''
    }

    # Try to get from URL parameters first
    try:
        import urllib.parse

        # For Streamlit >= 1.28.0
        if hasattr(st, 'query_params'):
            query_params = st.query_params
            data['employee_id'] = query_params.get('employee_id', [''])[0] if isinstance(
                query_params.get('employee_id', ''), list) else query_params.get('employee_id', '')
            data['account'] = query_params.get('account', [''])[0] if isinstance(
                query_params.get('account', ''), list) else query_params.get('account', '')
            data['industry'] = query_params.get('industry', [''])[0] if isinstance(
                query_params.get('industry', ''), list) else query_params.get('industry', '')
            data['problem'] = query_params.get('problem', [''])[0] if isinstance(
                query_params.get('problem', ''), list) else query_params.get('problem', '')

            # URL decode the values
            data['employee_id'] = urllib.parse.unquote(data['employee_id'])
            data['account'] = urllib.parse.unquote(data['account'])
            data['industry'] = urllib.parse.unquote(data['industry'])
            data['problem'] = urllib.parse.unquote(data['problem'])
    except Exception as e:
        pass

    # Store in session state if not already present or update if URL has data
    if data['employee_id'] and ('employee_id' not in st.session_state or not st.session_state.employee_id):
        st.session_state.employee_id = data['employee_id']
    if data['account'] and ('business_account' not in st.session_state or not st.session_state.business_account):
        st.session_state.business_account = data['account']
    if data['industry'] and ('business_industry' not in st.session_state or not st.session_state.business_industry):
        st.session_state.business_industry = data['industry']
    if data['problem'] and ('business_problem' not in st.session_state or not st.session_state.business_problem):
        st.session_state.business_problem = data['problem']

    # Return from session state (prioritize session state over URL)
    return {
        'employee_id': st.session_state.get('employee_id', data['employee_id']),
        'account': st.session_state.get('business_account', data['account']),
        'industry': st.session_state.get('business_industry', data['industry']),
        'problem': st.session_state.get('business_problem', data['problem'])
    }


def render_unified_business_inputs(page_key_prefix: str = "global", show_titles: bool = True,
                                   title_account_industry: str = "Account & Industry",
                                   title_problem: str = "Business Problem Description",
                                   save_button_label: str = "✅ Save Problem Details"):
    """
    Render a standardized Account/Industry + Business Problem input UI with the same
    styling and confirmation behavior used on the Welcome page. Intended for reuse across agents.

    Behavior highlights:
    - Uses st.session_state saved_* keys as source of truth, and business_* as working values
    - Confirmation popup appears when user changes Account while a saved_problem exists
    - Consistent selectbox and textarea styling for both light and dark modes
    - Returns a tuple (account, industry, problem) representing current working values

    Args:
        page_key_prefix: Prefix to make widget keys unique per page (e.g., "vocab", "volatility")
        show_titles: Whether to render section title boxes
        title_account_industry: Title text for the Account & Industry section
        title_problem: Title text for the Problem Description section
        save_button_label: Label for the Save button
    """
    # Initialize saved state (source of truth)
    if 'saved_account' not in st.session_state:
        st.session_state.saved_account = "Select Account"
    if 'saved_industry' not in st.session_state:
        st.session_state.saved_industry = "Select Industry"
    if 'saved_problem' not in st.session_state:
        st.session_state.saved_problem = ""

    # Working values (what widgets show before Save)
    if 'business_account' not in st.session_state:
        st.session_state.business_account = st.session_state.saved_account
    if 'business_industry' not in st.session_state:
        st.session_state.business_industry = st.session_state.saved_industry
    if 'business_problem' not in st.session_state:
        st.session_state.business_problem = st.session_state.saved_problem

    # Confirmation and control flags
    if 'edit_confirmed' not in st.session_state:
        st.session_state.edit_confirmed = False
    if 'cancel_clicked' not in st.session_state:
        st.session_state.cancel_clicked = False
    if 'selectbox_key_counter' not in st.session_state:
        st.session_state.selectbox_key_counter = 0

    # Inject the same input styles as Welcome page (light/dark aware)
    if st.session_state.get('dark_mode', False):
        st.markdown("""
        <style>
            :root { --musigma-red:#8b1e1e; --accent-orange:#ff6b35; --accent-purple:#7c3aed;
                    --text-primary:#f3f4f6; --text-secondary:#9ca3af; --text-light:#ffffff;
                    --bg-card:#23272f; --bg-app:#0b0f14; --border-color:rgba(255,255,255,0.12);
                    --shadow-sm:0 2px 4px rgba(0,0,0,0.3); --shadow-md:0 4px 6px rgba(0,0,0,0.4);
                    --shadow-lg:0 10px 25px rgba(0,0,0,0.5); }

            /* Selects */
            .stSelectbox { margin-bottom: 1rem; }
            .stSelectbox > label { font-weight:600!important; font-size:0.875rem!important; color:var(--text-primary)!important; margin-bottom:0.35rem!important; }
            .stSelectbox > div > div { background-color: rgba(35,39,47,0.8)!important; border:2px solid rgba(255,107,53,0.3)!important; border-radius:16px!important; padding:0.35rem 0.65rem!important; min-height:38px!important; max-height:38px!important; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3); display:flex!important; align-items:center!important; }
            .stSelectbox [data-baseweb="select"] { background-color:transparent!important; min-height:32px!important; max-height:32px!important; }
            .stSelectbox [data-baseweb="select"] > div { color:var(--text-light)!important; font-size:0.9rem!important; font-weight:500!important; line-height:1.3!important; white-space:nowrap!important; overflow:hidden!important; text-overflow:ellipsis!important; padding:0!important; display:flex!important; align-items:center!important; }

            /* Popover + listbox (Welcome page orange style in dark mode) */
            [data-baseweb="popover"], [data-baseweb="popover"] > div, [data-baseweb="popover"] > div > div { background:#ff6b35!important; }
            [data-baseweb="popover"] { border-radius:16px!important; box-shadow:var(--shadow-lg)!important; }
            ul[role="listbox"] { background:#ff6b35!important; border:2px solid rgba(255,107,53,0.3)!important; border-radius:16px!important; box-shadow:var(--shadow-lg)!important; padding:0.5rem!important; max-height:280px!important; overflow-y:auto!important; }
            li[role="option"] { color:#000000!important; background:transparent!important; padding:10px 14px!important; font-size:0.95rem!important; border-radius:10px!important; transition:all 0.2s ease!important; font-weight:600!important; }
            li[role="option"]:hover { background-color: rgba(139,30,30,0.8)!important; color:#ffffff!important; transform: translateX(5px)!important; }
            li[role="option"][aria-selected="true"] { background-color: var(--musigma-red)!important; color:#ffffff!important; font-weight:700!important; }

            /* Textarea */
            .stTextArea textarea { background: var(--bg-card)!important; border:2px solid var(--border-color)!important; border-radius:16px!important; color:var(--text-primary)!important; font-size:1.05rem!important; box-shadow:var(--shadow-sm); padding:1.25rem!important; line-height:1.7!important; min-height:180px!important; }
            .stTextArea textarea::placeholder { color:var(--text-secondary)!important; opacity:0.7!important; }

            /* Section titles */
            .section-title-box { background: linear-gradient(135deg, var(--musigma-red) 0%, var(--accent-orange) 100%)!important; border-radius:16px; padding:1rem 2rem; margin:0 0 0.5rem 0!important; box-shadow:var(--shadow-lg)!important; text-align:center; }
            .section-title-box h3 { color:var(--text-light)!important; margin:0!important; font-weight:700!important; font-size:1.3rem!important; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            :root { --musigma-red:#8b1e1e; --accent-orange:#ff6b35; --accent-purple:#7c3aed;
                    --text-primary:#1e293b; --text-secondary:#6b7280; --text-light:#ffffff;
                    --bg-card:#ffffff; --bg-app:#fafafa; --border-color:#e5e7eb;
                    --shadow-sm:0 1px 2px rgba(0,0,0,0.05); --shadow-md:0 4px 6px rgba(0,0,0,0.1);
                    --shadow-lg:0 10px 15px rgba(0,0,0,0.1); }

            .stSelectbox { margin-bottom: 1rem; }
            .stSelectbox > label { font-weight:600!important; font-size:0.875rem!important; color:var(--text-primary)!important; margin-bottom:0.35rem!important; }
            .stSelectbox > div > div { background-color: var(--bg-card)!important; border:2px solid var(--border-color)!important; border-radius:16px!important; padding:0.35rem 0.65rem!important; min-height:38px!important; max-height:38px!important; box-shadow: var(--shadow-sm); display:flex!important; align-items:center!important; }
            .stSelectbox [data-baseweb="select"] { background-color:transparent!important; min-height:32px!important; max-height:32px!important; }
            .stSelectbox [data-baseweb="select"] > div { color:var(--text-primary)!important; font-size:0.9rem!important; font-weight:500!important; line-height:1.3!important; white-space:nowrap!important; overflow:hidden!important; text-overflow:ellipsis!important; padding:0!important; display:flex!important; align-items:center!important; }

            [data-baseweb="popover"] { background-color: var(--bg-card)!important; border-radius:16px!important; box-shadow:var(--shadow-lg)!important; }
            [data-baseweb="popover"] > div { background-color: var(--bg-card)!important; }
            ul[role="listbox"] { background-color: var(--bg-card)!important; border:2px solid var(--border-color)!important; border-radius:16px!important; box-shadow:var(--shadow-lg)!important; padding:0.5rem!important; max-height:280px!important; overflow-y:auto!important; }
            li[role="option"] { color:var(--text-primary)!important; background:transparent!important; padding:10px 14px!important; font-size:0.95rem!important; border-radius:10px!important; transition:all 0.2s ease!important; font-weight:500!important; }
            li[role="option"]:hover { background-color: rgba(124,58,237,0.1)!important; color:var(--accent-purple)!important; transform: translateX(5px)!important; }
            li[role="option"][aria-selected="true"] { background-color: rgba(139,30,30,0.15)!important; color: var(--musigma-red)!important; font-weight:600!important; }

            .stTextArea textarea { background: var(--bg-card)!important; border:2px solid var(--border-color)!important; border-radius:16px!important; color:var(--text-primary)!important; font-size:1.05rem!important; box-shadow:var(--shadow-sm); padding:1.25rem!important; line-height:1.7!important; min-height:180px!important; }
            .stTextArea textarea::placeholder { color:var(--text-secondary)!important; opacity:0.7!important; }

            .section-title-box { background: linear-gradient(135deg, var(--musigma-red) 0%, var(--accent-orange) 100%)!important; border-radius:16px; padding:1rem 2rem; margin:0 0 0.5rem 0!important; box-shadow:var(--shadow-lg)!important; text-align:center; }
            .section-title-box h3 { color:var(--text-light)!important; margin:0!important; font-weight:700!important; font-size:1.3rem!important; }
        </style>
        """, unsafe_allow_html=True)

    # Optional section title
    if show_titles:
        st.markdown(f'<div class="section-title-box"><h3>{title_account_industry}</h3></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    show_confirmation = False
    account_change_value = None

    with c1:
        account_input = st.selectbox(
            "Select Account:",
            options=ACCOUNTS,
            index=ACCOUNTS.index(st.session_state.business_account) if st.session_state.business_account in ACCOUNTS else 0,
            key=f"{page_key_prefix}_account_select_{st.session_state.selectbox_key_counter}"
        )

        if account_input != st.session_state.business_account:
            if st.session_state.cancel_clicked:
                st.session_state.cancel_clicked = False
            elif st.session_state.saved_problem and not st.session_state.edit_confirmed:
                show_confirmation = True
                account_change_value = account_input
            else:
                st.session_state.business_account = account_input
                if account_input in ACCOUNT_INDUSTRY_MAP:
                    st.session_state.business_industry = ACCOUNT_INDUSTRY_MAP[account_input]

    with c2:
        current_industry = st.session_state.business_industry
        current_account = st.session_state.business_account
        is_auto_mapped = current_account in ACCOUNT_INDUSTRY_MAP
        industry_input = st.selectbox(
            "Industry:", options=INDUSTRIES,
            index=INDUSTRIES.index(current_industry) if current_industry in INDUSTRIES else 0,
            disabled=is_auto_mapped,
            help="Industry is automatically mapped for this account" if is_auto_mapped else "Select the industry for this analysis",
            key=f"{page_key_prefix}_industry_select_{st.session_state.selectbox_key_counter}"
        )
        if not is_auto_mapped and industry_input != st.session_state.business_industry:
            st.session_state.business_industry = industry_input

    if show_confirmation:
        st.markdown(
            """
            <style>
            .confirmation-box { background: linear-gradient(135deg, rgba(255,107,53,0.08), rgba(124,58,237,0.08)); border: 2px solid rgba(255,107,53,0.25); border-radius: 12px; padding: 18px 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 15px 0; }
            .confirmation-message { color: #ff6b35; font-size: 15px; font-weight: 600; margin-bottom: 0; text-align: center; }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="confirmation-box">
              <div class="confirmation-message">💡 <strong>Proceed with new problem?</strong><br>
                <span style="font-size: 13px; font-weight: 400; color: #555;">Changing the account will update your business problem details.</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        colA, colB, colC, colD, colE = st.columns([3, 1.2, 0.6, 1.2, 3])
        with colB:
            if st.button("Yes", key=f"{page_key_prefix}_confirm_edit", type="primary"):
                st.session_state.edit_confirmed = True
                st.session_state.business_account = account_change_value
                if account_change_value in ACCOUNT_INDUSTRY_MAP:
                    st.session_state.business_industry = ACCOUNT_INDUSTRY_MAP[account_change_value]
                st.session_state.selectbox_key_counter += 1
                st.rerun()
        with colD:
            if st.button("No", key=f"{page_key_prefix}_cancel_edit", type="secondary"):
                st.session_state.cancel_clicked = True
                st.session_state.business_account = st.session_state.saved_account
                st.session_state.business_industry = st.session_state.saved_industry
                st.session_state.selectbox_key_counter += 1
                st.rerun()

    # Problem section
    if show_titles:
        st.markdown(f'<div class="section-title-box"><h3>{title_problem}</h3></div>', unsafe_allow_html=True)

    problem_input = st.text_area(
        "Describe your business problem in detail:",
        value=st.session_state.business_problem,
        height=180,
        placeholder="Feel free to just type down your problem statement, or copy-paste if you have it handy somewhere...",
        label_visibility="collapsed",
        key=f"{page_key_prefix}_problem_textarea"
    )
    if problem_input != st.session_state.business_problem:
        st.session_state.business_problem = problem_input

    saved = False
    if st.button(save_button_label, use_container_width=True, type="primary", key=f"{page_key_prefix}_save_btn"):
        if (st.session_state.business_account == "Select Account" or
            st.session_state.business_industry == "Select Industry" or
            not st.session_state.business_problem.strip()):
            st.error("⚠️ Please select an Account, Industry, and provide a Business Problem description.")
        else:
            st.session_state.saved_account = st.session_state.business_account
            st.session_state.saved_industry = st.session_state.business_industry
            st.session_state.saved_problem = st.session_state.business_problem
            st.session_state.edit_confirmed = False
            saved = True
            st.success("✅ Problem details saved!")
            st.rerun()

    # Return current working values
    return (
        st.session_state.business_account,
        st.session_state.business_industry,
        st.session_state.business_problem,
    )


def display_shared_data(shared_data=None, show_change_button=True):
    """
    Display the shared data (employee_id, account, industry, problem) in a nice format

    Args:
        shared_data: Optional dict with data to display. If None, will call get_shared_data()
        show_change_button: Whether to show a button to change the input data
    """
    data = shared_data if shared_data else get_shared_data()

    if data['employee_id'] or data['problem']:
        st.markdown("""
        <style>
        .shared-data-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            color: white;
        }
        .shared-data-title {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 15px;
            text-align: center;
        }
        .shared-data-item {
            margin: 10px 0;
            padding: 10px;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            backdrop-filter: blur(10px);
        }
        .shared-data-label {
            font-weight: 600;
            font-size: 0.9rem;
            opacity: 0.9;
        }
        .shared-data-value {
            margin-top: 5px;
            font-size: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="shared-data-container">',
                    unsafe_allow_html=True)
        st.markdown(
            '<div class="shared-data-title">📋 Current Analysis Context</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="shared-data-item">
                <div class="shared-data-label">👤 Employee ID</div>
                <div class="shared-data-value">{data['employee_id'] or 'Not provided'}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="shared-data-item">
                <div class="shared-data-label">🏢 Account</div>
                <div class="shared-data-value">{data['account'] or 'Not provided'}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="shared-data-item">
                <div class="shared-data-label">🏭 Industry</div>
                <div class="shared-data-value">{data['industry'] or 'Not provided'}</div>
            </div>
            """, unsafe_allow_html=True)

        if data['problem']:
            st.markdown(f"""
            <div class="shared-data-item">
                <div class="shared-data-label">📄 Business Problem</div>
                <div class="shared-data-value">{data['problem']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if show_change_button:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🔄 Change Input Data", use_container_width=True, type="secondary"):
                    # Show input form
                    st.session_state.show_input_form = True
    else:
        st.warning(
            "⚠️ No input data found. Please provide your business problem details.")
        st.session_state.show_input_form = True


def show_input_form():
    """
    Display form to change/input the shared data
    Uses the globally defined ACCOUNTS and INDUSTRIES lists
    Auto-maps industry when account is selected
    """
    data = get_shared_data()

    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; 
                border-radius: 12px; 
                margin-bottom: 30px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <h3 style='color: white; margin: 0 0 10px 0; text-align: center;'>
            📝 Update Your Business Problem
        </h3>
        <p style='color: rgba(255,255,255,0.9); margin: 0; text-align: center; font-size: 0.95rem;'>
            Provide or update details about your business problem for analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state for form inputs if not present
    if 'form_account' not in st.session_state:
        st.session_state.form_account = data.get('account', 'Select Account')
    if 'form_industry' not in st.session_state:
        st.session_state.form_industry = data.get(
            'industry', 'Select Industry')
    if 'form_problem' not in st.session_state:
        st.session_state.form_problem = data.get('problem', '')

    col1, col2 = st.columns(2)

    with col1:
        # Get current account index
        current_account = st.session_state.form_account
        account_index = ACCOUNTS.index(
            current_account) if current_account in ACCOUNTS else 0

        # Account dropdown - auto-mapping happens immediately on selection
        account_input = st.selectbox(
            "🏢 Select Account",
            ACCOUNTS,
            index=account_index,
            key="form_account_selector"
        )

        # Auto-map industry immediately when account changes
        if account_input != st.session_state.form_account:
            st.session_state.form_account = account_input
            # Trigger auto-mapping
            if account_input in ACCOUNT_INDUSTRY_MAP:
                st.session_state.form_industry = ACCOUNT_INDUSTRY_MAP[account_input]
                st.rerun()

        # Update session state
        st.session_state.form_account = account_input

    with col2:
        # Auto-map industry based on selected account
        if account_input in ACCOUNT_INDUSTRY_MAP:
            auto_industry = ACCOUNT_INDUSTRY_MAP[account_input]
            st.session_state.form_industry = auto_industry
        else:
            auto_industry = st.session_state.form_industry

        industry_index = INDUSTRIES.index(
            auto_industry) if auto_industry in INDUSTRIES else 0

        industry_input = st.selectbox(
            "🏭 Select Industry",
            INDUSTRIES,
            index=industry_index,
            key="form_industry_selector",
            disabled=(account_input == "Select Account"),
            help="Industry is auto-mapped based on account selection" if account_input in ACCOUNT_INDUSTRY_MAP else None
        )

        st.session_state.form_industry = industry_input

    business_problem = st.text_area(
        "📄 Describe Your Business Problem",
        value=st.session_state.form_problem,
        placeholder="Enter your business problem statement here. Be as detailed as possible...",
        height=150,
        key="form_problem_textarea"
    )

    st.session_state.form_problem = business_problem

    col_submit1, col_submit2, col_submit3 = st.columns([1, 1, 1])
    with col_submit2:
        if st.button("✅ Update Problem Details", use_container_width=True, type="primary", key="submit_form_button"):
            if account_input == "Select Account" or industry_input == "Select Industry":
                st.error("⚠️ Please select both Account and Industry!")
            elif not business_problem or len(business_problem.strip()) < 10:
                st.error(
                    "⚠️ Please provide a detailed business problem (at least 10 characters)!")
            else:
                # Update session state with final values
                st.session_state.business_account = account_input
                st.session_state.business_industry = industry_input
                st.session_state.business_problem = business_problem
                st.session_state.account = account_input
                st.session_state.industry = industry_input
                st.session_state.problem_text = business_problem
                st.session_state.show_input_form = False
                st.success("✅ Problem details updated successfully!")
                st.rerun()


def handle_account_change():
    """Callback function to handle account selection change"""
    # This triggers when account dropdown changes
    # The auto-mapping happens in the main show_input_form function
    pass
