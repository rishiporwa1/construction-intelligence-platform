"""
Tab 1: Site Safety & PPE Audit (Epic 2)
Multimodal analysis of PPE compliance (helmets, high-vis vests, steel-toe boots, harnesses)
under OSHA 1926 and IS 456 standards with structured JSON, metric cards, status pills, and export.
"""

import os
from PIL import Image
import streamlit as st
import pandas as pd

from modules.gemini_client import analyze_site_safety
from modules.ui_components import (
    render_metric_card,
    get_status_pill_html,
    render_compliance_donut,
    render_hazard_severity_bar,
    download_json_button
)

SAMPLE_SAFETY_OPTIONS = {
    "Select a pre-loaded sample photo...": None,
    "Sample 1: High-Rise Scaffolding Elevation (Fall & PPE Audit)": "sample_images/sample_safety_1.jpg",
    "Sample 2: Ground Trench & Rebar Crew (Excavation Zone)": "sample_images/sample_safety_2.jpg"
}


def render_tab_safety(api_key: str, demo_mode: bool):
    """Render Tab 1 - Site Safety & PPE Audit Module."""
    st.markdown("### 🦺 Site Safety & Worker PPE Compliance Audit (OSHA & IS 456)")
    st.caption("Upload site imagery or choose a pre-loaded inspection frame. Gemini Multimodal Vision conducts automated PPE detection, regulatory compliance checks, and hazard severity grading.")

    col_input, col_view = st.columns([1, 1], gap="medium")

    chosen_image = None
    image_source_name = ""

    with col_input:
        st.markdown("#### 1. Input Inspection Imagery")
        
        # Preset selector
        selected_preset = st.selectbox(
            "Quick Demo: Load Curated Inspection Frame",
            options=list(SAMPLE_SAFETY_OPTIONS.keys()),
            help="Choose an engineered site photo to test the PPE audit pipeline instantly."
        )

        uploaded_file = st.file_uploader(
            "Or Upload Construction Site Photo (JPG, JPEG, PNG)",
            type=["jpg", "jpeg", "png"],
            help="Supported formats: JPG, PNG. High-resolution imagery produces optimal PPE detection precision."
        )

        if uploaded_file is not None:
            try:
                chosen_image = Image.open(uploaded_file).convert("RGB")
                image_source_name = uploaded_file.name
            except Exception as e:
                st.error(f"Error loading uploaded image: {e}")
        elif selected_preset and SAMPLE_SAFETY_OPTIONS[selected_preset]:
            preset_path = SAMPLE_SAFETY_OPTIONS[selected_preset]
            if os.path.exists(preset_path):
                chosen_image = Image.open(preset_path).convert("RGB")
                image_source_name = selected_preset

        audit_btn = st.button(
            "🚀 Run Multimodal Safety Audit",
            type="primary",
            use_container_width=True,
            disabled=(chosen_image is None)
        )

    with col_view:
        st.markdown("#### 2. Site Camera Preview")
        if chosen_image is not None:
            st.image(chosen_image, caption=f"Active Frame: {image_source_name}", use_container_width=True)
        else:
            st.info("👈 Upload an image or select a sample frame to initiate automated inspection.")

    # Execute Analysis
    if audit_btn and chosen_image is not None:
        with st.spinner("Analyzing worker PPE and safety conditions under OSHA 1926 & IS 456..."):
            result, is_demo, msg = analyze_site_safety(chosen_image, api_key=api_key, demo_mode=demo_mode)
            st.session_state["safety_audit_result"] = result
            st.session_state["safety_is_demo"] = is_demo
            st.session_state["safety_msg"] = msg

    # Display Results if available in session state
    if "safety_audit_result" in st.session_state:
        res = st.session_state["safety_audit_result"]
        is_demo = st.session_state.get("safety_is_demo", False)
        msg = st.session_state.get("safety_msg", "")

        st.markdown("---")
        
        # Status header banner
        status_col1, status_col2 = st.columns([3, 1])
        with status_col1:
            st.markdown(f"#### 📊 Site Audit Report: {get_status_pill_html(res.get('overall_status', 'Unknown'), res.get('overall_status', 'info'))}", unsafe_allow_html=True)
            if is_demo:
                st.markdown(f'<div class="demo-banner">ℹ️ <b>Demonstration Mode:</b> {msg}</div>', unsafe_allow_html=True)
            else:
                st.success(f"⚡ {msg}")
        with status_col2:
            download_json_button(
                data=res,
                file_name="site_safety_audit_report.json",
                label="📥 Export JSON Audit"
            )

        # Executive Summary
        if res.get("executive_summary"):
            st.info(f"**Inspector Executive Summary:** {res['executive_summary']}")

        # Top Metric Cards
        score = res.get("safety_score", 0)
        ppe_list = res.get("ppe_detection", [])
        hazards_list = res.get("identified_hazards", [])

        total_workers = max([item.get("detected_workers", 0) for item in ppe_list], default=0)
        critical_hazards = sum(1 for h in hazards_list if h.get("severity") in ["Critical", "High"])

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            score_color = "#10B981" if score >= 80 else ("#F59E0B" if score >= 60 else "#EF4444")
            render_metric_card("Safety Compliance Score", f"{score} / 100", "OSHA & IS 456 weighted index", score_color)
        with m2:
            render_metric_card("Overall Site Status", res.get("overall_status", "N/A"), "Mandatory site status", score_color)
        with m3:
            render_metric_card("Personnel Monitored", f"{total_workers} Workers", "Detected in frame", "#3B82F6")
        with m4:
            haz_color = "#EF4444" if critical_hazards > 0 else "#10B981"
            render_metric_card("High/Critical Hazards", f"{critical_hazards} Active", "Actionable infractions", haz_color)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts & Checklist Row
        chart_col, details_col = st.columns([1, 1], gap="medium")

        with chart_col:
            st.markdown("##### 📈 Safety Index & Hazard Breakdown")
            st.plotly_chart(render_compliance_donut(score, title="Safety Score"), use_container_width=True)
            if hazards_list:
                st.plotly_chart(render_hazard_severity_bar(hazards_list), use_container_width=True)

        with details_col:
            st.markdown("##### 🛡️ Worker PPE Detection Checklist")
            if ppe_list:
                for item in ppe_list:
                    status_pill = get_status_pill_html(item.get("status", "Unknown"), item.get("status", "info"))
                    st.markdown(f"""
                    <div style="background: #1E293B; border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 12px 16px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 600; font-size: 0.95rem; color: #F8FAFC;">{item.get('item')}</span>
                            {status_pill}
                        </div>
                        <div style="margin-top: 6px; font-size: 0.85rem; color: #94A3B8;">
                            <b>Compliance:</b> {item.get('compliance_rate', 'N/A')} ({item.get('compliant_workers', 0)}/{item.get('detected_workers', 0)} workers)
                        </div>
                        <div style="font-size: 0.82rem; color: #CBD5E1; margin-top: 3px;">
                            {item.get('details', '')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("No specific PPE items reported.")

        # Identified Site Hazards & Corrective Remedies
        st.markdown("##### 🚨 Identified Hazards & Regulatory Corrective Remedies")
        if hazards_list:
            for idx, haz in enumerate(hazards_list, 1):
                sev = haz.get("severity", "Medium")
                sev_html = get_status_pill_html(sev, sev)
                with st.expander(f"Hazard #{idx}: {haz.get('hazard')} ({sev.upper()})", expanded=(sev in ["Critical", "High"])):
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        st.markdown(f"**Severity Level:** {sev_html}", unsafe_allow_html=True)
                        st.markdown(f"**Location in Frame:** `{haz.get('location_in_frame', 'N/A')}`")
                        st.markdown(f"**Governing Standard:** `{haz.get('osha_standard', 'OSHA 1926 / IS 456')}`")
                    with c2:
                        st.markdown("**🔧 Prescribed Corrective Remedy:**")
                        st.info(haz.get("corrective_remedy", "Immediate site safety officer inspection required."))
        else:
            st.success("✅ Zero critical hazards detected in inspected frame.")

        # Raw Structured JSON Expander
        with st.expander("🔍 View Raw Structured JSON Payload", expanded=False):
            st.json(res)
