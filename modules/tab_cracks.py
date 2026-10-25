"""
Tab 2: Crack Diagnostics & Structural Integrity (Epic 2)
Forensic AI assessment for concrete and masonry distress.
Classifies defect type (Hairline, Settlement, Structural Shear, Thermal Expansion, Spalling),
estimated crack width in mm, root causes, engineering repairs, urgency, and IS 456 clauses.
"""

import os
from PIL import Image
import streamlit as st
import plotly.graph_objects as go

from modules.gemini_client import diagnose_concrete_crack
from modules.ui_components import (
    render_metric_card,
    get_status_pill_html,
    download_json_button
)

SAMPLE_CRACK_OPTIONS = {
    "Select a pre-loaded concrete inspection sample...": None,
    "Sample 1: Structural Shear Crack (RCC Column-Beam Joint)": "sample_images/sample_crack_1.jpg",
    "Sample 2: Hairline Plaster Crazing (Non-Structural Shrinkage)": "sample_images/sample_crack_2.jpg",
    "Sample 3: Severe Spalling & Exposed Rebar (Carbonation Delamination)": "sample_images/sample_crack_3.jpg"
}


def render_crack_width_gauge(width_mm: float, threshold_mm: float = 0.3):
    """Plotly gauge indicator showing estimated crack width vs IS 456 permissible threshold."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=width_mm,
        delta={'reference': threshold_mm, 'increasing': {'color': "#EF4444"}, 'decreasing': {'color': "#10B981"}},
        title={'text': f"Crack Width (mm)<br><span style='font-size:11px; color:#94A3B8;'>IS 456 Max Limit: {threshold_mm} mm</span>", 'font': {'size': 14, 'color': '#F8FAFC'}},
        number={'suffix': " mm", 'font': {'size': 24, 'color': '#F8FAFC', 'family': 'JetBrains Mono'}},
        gauge={
            'axis': {'range': [0, max(5.0, width_mm * 1.3)], 'tickcolor': "#94A3B8"},
            'bar': {'color': "#EF4444" if width_mm > threshold_mm else "#10B981"},
            'bgcolor': "rgba(255,255,255,0.05)",
            'borderwidth': 1,
            'bordercolor': "rgba(255,255,255,0.1)",
            'steps': [
                {'range': [0, 0.3], 'color': "rgba(16, 185, 129, 0.2)"},
                {'range': [0.3, 1.5], 'color': "rgba(245, 158, 11, 0.2)"},
                {'range': [1.5, max(5.0, width_mm * 1.3)], 'color': "rgba(239, 68, 68, 0.25)"}
            ],
            'threshold': {
                'line': {'color': "#EF4444", 'width': 3},
                'thickness': 0.75,
                'value': threshold_mm
            }
        }
    ))
    fig.update_layout(
        height=200,
        margin=dict(t=30, b=10, l=30, r=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def render_tab_cracks(api_key: str, demo_mode: bool):
    """Render Tab 2 - Crack Diagnostics & Structural Integrity Module."""
    st.markdown("### 🧱 Concrete Defect Diagnostics & Structural Integrity (IS 456 / ACI 224R)")
    st.caption("Forensic multimodal classification of concrete defects: Hairline, Settlement, Structural Shear, Thermal Expansion, and Spalling with repair specifications.")

    col_input, col_view = st.columns([1, 1], gap="medium")

    chosen_image = None
    image_source_name = ""
    sample_key = None

    with col_input:
        st.markdown("#### 1. Input Defect Surface Photo")

        selected_preset = st.selectbox(
            "Quick Demo: Choose Defect Specimen",
            options=list(SAMPLE_CRACK_OPTIONS.keys()),
            help="Choose a concrete defect specimen for instant diagnostic assessment."
        )

        uploaded_file = st.file_uploader(
            "Or Upload Defect Photo (JPG, JPEG, PNG)",
            type=["jpg", "jpeg", "png"],
            help="Upload high-clarity photos of concrete beam, column, wall, or slab cracks."
        )

        if uploaded_file is not None:
            try:
                chosen_image = Image.open(uploaded_file).convert("RGB")
                image_source_name = uploaded_file.name
                sample_key = None
            except Exception as e:
                st.error(f"Error loading image: {e}")
        elif selected_preset and SAMPLE_CRACK_OPTIONS[selected_preset]:
            preset_path = SAMPLE_CRACK_OPTIONS[selected_preset]
            if os.path.exists(preset_path):
                chosen_image = Image.open(preset_path).convert("RGB")
                image_source_name = selected_preset
                sample_key = os.path.basename(preset_path)

        diag_btn = st.button(
            "🔍 Execute Structural Diagnostics",
            type="primary",
            use_container_width=True,
            disabled=(chosen_image is None)
        )

    with col_view:
        st.markdown("#### 2. Defect Inspection Preview")
        if chosen_image is not None:
            st.image(chosen_image, caption=f"Specimen: {image_source_name}", use_container_width=True)
        else:
            st.info("👈 Upload an image or select a specimen to evaluate crack mechanics.")

    # Execute Analysis
    if diag_btn and chosen_image is not None:
        with st.spinner("Classifying defect mechanics, estimating crack width, and querying IS 456 / ACI repair standards..."):
            result, is_demo, msg = diagnose_concrete_crack(
                chosen_image,
                api_key=api_key,
                demo_mode=demo_mode,
                sample_key=sample_key
            )
            st.session_state["crack_diag_result"] = result
            st.session_state["crack_is_demo"] = is_demo
            st.session_state["crack_msg"] = msg

    # Display Diagnostics Results
    if "crack_diag_result" in st.session_state:
        res = st.session_state["crack_diag_result"]
        is_demo = st.session_state.get("crack_is_demo", False)
        msg = st.session_state.get("crack_msg", "")

        st.markdown("---")

        header_c1, header_c2 = st.columns([3, 1])
        with header_c1:
            defect_name = res.get("defect_type", "Defect")
            urgency = res.get("urgency", "Urgent")
            st.markdown(f"#### 🔬 Diagnostic Finding: **{defect_name}** {get_status_pill_html(urgency, urgency)}", unsafe_allow_html=True)
            if is_demo:
                st.markdown(f'<div class="demo-banner">ℹ️ <b>Demonstration Mode:</b> {msg}</div>', unsafe_allow_html=True)
            else:
                st.success(f"⚡ {msg}")
        with header_c2:
            download_json_button(
                data=res,
                file_name="structural_defect_diagnostic_report.json",
                label="📥 Export Forensic Report"
            )

        # Metric Cards Row
        width_val = float(res.get("estimated_crack_width_mm", 0.0))
        limit_val = float(res.get("is_456_threshold_mm", 0.3))
        risk_idx = res.get("risk_index", 50)
        element = res.get("structural_element", "Concrete Substrate")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            render_metric_card("Defect Classification", defect_name, element, "#F59E0B")
        with m2:
            width_color = "#EF4444" if width_val > limit_val else "#10B981"
            render_metric_card("Estimated Crack Width", f"{width_val:.2f} mm", f"Threshold: {limit_val} mm", width_color)
        with m3:
            urg_color = "#EF4444" if "critical" in urgency.lower() or "high" in urgency.lower() else "#F59E0B"
            render_metric_card("Engineering Urgency", urgency.split("(")[0].strip(), urgency, urg_color)
        with m4:
            render_metric_card("Structural Distress Risk", f"{risk_idx} / 100", "Composite safety index", urg_color)

        st.markdown("<br>", unsafe_allow_html=True)

        # Two Column Diagnostics Breakdown
        col_gauge, col_causes = st.columns([1, 1], gap="medium")

        with col_gauge:
            st.markdown("##### 📏 IS 456 Crack Width Verification")
            st.plotly_chart(render_crack_width_gauge(width_val, limit_val), use_container_width=True)
            
            # IS 456 Status Box
            status_text = res.get("is_456_status", "")
            if "EXCEEDS" in status_text or width_val > limit_val:
                st.error(f"⚠️ **IS 456:2000 Compliance Breach:** {status_text}")
            else:
                st.success(f"✅ **IS 456:2000 Status:** {status_text}")
            
            if res.get("is_456_guidelines"):
                st.caption(f"**Code Reference:** {res['is_456_guidelines']}")

        with col_causes:
            st.markdown("##### 🧬 Forensic Root Cause Analysis")
            root_causes = res.get("root_causes", [])
            if root_causes:
                for idx, cause in enumerate(root_causes, 1):
                    st.markdown(f"""
                    <div style="background: #1E293B; border-left: 3px solid #F59E0B; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px;">
                        <span style="font-size: 0.82rem; color: #F59E0B; font-weight: 700;">MECHANISM #{idx}</span>
                        <div style="font-size: 0.88rem; color: #F8FAFC; margin-top: 3px;">{cause}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("No root causes identified.")

        # Recommended Engineering Repairs
        st.markdown("##### 🛠️ Prescribed Remediation & Structural Repair Protocols")
        repairs = res.get("recommended_engineering_repairs", [])
        if repairs:
            for idx, rep in enumerate(repairs, 1):
                proto = rep.get("protocol", "Repair Protocol")
                spec = rep.get("specification", "Standard Spec")
                details = rep.get("details", "")
                with st.expander(f"Protocol #{idx}: {proto} — [{spec}]", expanded=True):
                    st.markdown(f"**Governing Technical Specification:** `{spec}`")
                    st.markdown(f"**Implementation Procedure:** {details}")
        else:
            st.write("No repair recommendations available.")

        with st.expander("🔍 View Raw Diagnostic JSON", expanded=False):
            st.json(res)
