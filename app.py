"""
Multimodal Construction Intelligence Platform (Skill Wallet Capstone Project 1)
Author: Production-Ready Full-Stack AI Engineer
Streamlit Community Cloud 1-Click Ready
"""

import os
import streamlit as st

# Configure Streamlit page setup (must be first Streamlit command)
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from modules.config import APP_TITLE, APP_SUBTITLE, CAPSTONE_TAG, VERSION
from modules.ui_components import apply_custom_css, render_hero_header, get_status_pill_html
from modules.gemini_client import get_active_api_key
from modules.tab_safety import render_tab_safety
from modules.tab_cracks import render_tab_cracks
from modules.tab_valuation import render_tab_valuation
from modules.tab_assistant import render_tab_assistant

def main():
    # Inject Custom Industrial Tech CSS Styling
    apply_custom_css()

    # Sidebar: Authentication, Architecture Overview, and Navigation
    with st.sidebar:
        st.markdown(f"## 🏗️ {APP_TITLE}")
        st.caption(f"**{CAPSTONE_TAG}** • `{VERSION}`")
        st.markdown("---")

        # 1. API Configuration & Demonstration Fallback
        st.markdown("### 🔑 Gemini AI Credentials")
        
        detected_env_key = os.environ.get("GEMINI_API_KEY", "")
        detected_secrets_key = ""
        try:
            detected_secrets_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            pass

        has_env_key = bool(detected_env_key or detected_secrets_key)
        
        user_key_input = st.text_input(
            "Enter Google Gemini API Key",
            type="password",
            placeholder="AIzaSy...",
            help="Your API key remains local to your browser session. Leave empty to use Demonstration Mode."
        )

        active_key = get_active_api_key(user_key_input)
        key_is_available = bool(active_key)

        # Force or Toggle Demonstration Mode
        if not key_is_available:
            demo_mode = st.checkbox("Demonstration Mode (Active)", value=True, disabled=True,
                                    help="Automatically engaged when no API key is provided.")
            st.markdown(
                '<div style="background: rgba(245,158,11,0.15); border: 1px solid #F59E0B; padding: 8px 12px; border-radius: 6px; font-size: 0.8rem; color: #FCD34D;">'
                '⚡ <b>Demonstration Mode Active:</b> Full high-fidelity simulation enabled with pre-calculated OSHA audits, crack diagnostics, and sample imagery.'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            demo_mode = st.checkbox("Force Demonstration Mode", value=False,
                                    help="Toggle to preview simulated benchmark responses even with an active key.")
            if not demo_mode:
                st.markdown(
                    '<div style="background: rgba(16,185,129,0.15); border: 1px solid #10B981; padding: 8px 12px; border-radius: 6px; font-size: 0.8rem; color: #6EE7B7;">'
                    '✅ <b>Live Gemini Connected:</b> Multimodal 2.5 Flash / 2.0 Flash enabled.'
                    '</div>',
                    unsafe_allow_html=True
                )

        st.markdown("---")

        # 2. System Architecture & Standards Accordion
        st.markdown("### 🏛️ System Architecture")
        with st.expander("Engineering Stack & Standards", expanded=False):
            st.markdown("""
            - **Multimodal AI**: Google Gemini 2.5 Flash / 2.0 Flash Vision
            - **Safety Codes**: OSHA 1926 & IS 456 / IS 2925 / IS 3521
            - **Structural Forensics**: IS 456:2000 Cl. 35 & ACI 224R
            - **Real Estate Estimation**: CPWD Schedule of Rates (DSR) & RICS India
            - **3D Render Synthesis**: Pollinations AI FLUX Engine
            - **Weather Advisory**: IS 13367 (Cranes) & IS 7861 (Hot Weather)
            - **Persistence**: Zero external DB; stateless Streamlit Community Cloud
            """)

        st.markdown("### 📑 Core Modules")
        st.markdown("""
        1. **🦺 Site Safety & PPE**: Automated OSHA/IS 456 compliance grading
        2. **🧱 Crack Diagnostics**: Concrete forensic defect classifier
        3. **📊 Planning & Valuation**: CapEx, INR valuation & 3D rendering
        4. **🌤️ Daily Site Assistant**: Dynamic weather protocols & chat
        """)

        st.markdown("---")
        st.caption("Developed for Skill Wallet Capstone Evaluation • Fully Responsive • Python 3.10+")

    # Render Hero Header Banner
    render_hero_header()

    # Active Mode Notification Banner in main window if in Demo Mode
    if demo_mode or not key_is_available:
        st.markdown(
            '<div class="demo-banner">'
            '<span>💡 <b>Reviewer Note:</b> You are exploring in <b>Demonstration Mode</b>. '
            'You can test all 4 modules with 1-click using pre-loaded inspection frames, '
            'material calculators, 3D renders, and weather advisories. To connect live Gemini AI, provide an API key in the sidebar.</span>'
            '</div>',
            unsafe_allow_html=True
        )

    # Core Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🦺 Tab 1: Site Safety & PPE Audit",
        "🧱 Tab 2: Crack Diagnostics & Integrity",
        "📊 Tab 3: Planning & Valuation",
        "🌤️ Tab 4: Daily Site Assistant & Weather"
    ])

    with tab1:
        render_tab_safety(api_key=active_key, demo_mode=demo_mode)

    with tab2:
        render_tab_cracks(api_key=active_key, demo_mode=demo_mode)

    with tab3:
        render_tab_valuation()

    with tab4:
        render_tab_assistant(api_key=active_key, demo_mode=demo_mode)


if __name__ == "__main__":
    main()
