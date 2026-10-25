"""
Tab 3: Planning & Real Estate Valuation (Epic 3)
Calculates Total Project Budget, CapEx Incurred, Current Market Asset Valuation in INR (Lakhs/Crores),
Steel & Cement engineering metrics, dynamic milestone progress, and Pollinations AI 3D architectural rendering.
"""

import urllib.parse
import streamlit as st
import plotly.graph_objects as go

from modules.config import STRUCTURE_CONFIGS, LOCATION_TIERS
from modules.ui_components import render_metric_card


def format_inr(amount_inr: float) -> str:
    """Formats raw INR amounts into clean Lakhs (L) or Crores (Cr)."""
    if amount_inr >= 10_000_000: # 1 Crore
        crores = amount_inr / 10_000_000
        return f"₹ {crores:.2f} Cr"
    elif amount_inr >= 100_000: # 1 Lakh
        lakhs = amount_inr / 100_000
        return f"₹ {lakhs:.2f} L"
    else:
        return f"₹ {amount_inr:,.0f}"


def get_current_milestone(completion_pct: int) -> tuple[str, str]:
    """Returns milestone phase and description based on progress."""
    if completion_pct < 20:
        return (
            "Phase 1: Substructure & Deep Foundation",
            "Piling, raft casting, basement retaining walls, and waterproof tanking."
        )
    elif completion_pct < 55:
        return (
            "Phase 2: RCC Superstructure & Shear Walls",
            "Column casting, post-tensioned beam-slab decks, and elevator core staging."
        )
    elif completion_pct < 80:
        return (
            "Phase 3: MEP Rough-In & Masonry",
            "AAC blockwork infill, electrical conduits, plumbing risers, and internal plastering."
        )
    else:
        return (
            "Phase 4: Architectural Finishing & Handover",
            "Curtain wall glazing, flooring, elevators, HVAC balancing, and fire NOC clearance."
        )


def render_tab_valuation():
    """Render Tab 3 - Planning & Real Estate Valuation Module."""
    st.markdown("### 📊 Planning, Material Estimation & Real Estate Asset Valuation (INR)")
    st.caption("Parametric construction budget estimator, CPWD material consumption ratios (Steel/Cement), CapEx tracking, and AI 3D architectural concept visualization.")

    # Controls Row
    col_inputs, col_summary = st.columns([1.1, 0.9], gap="large")

    with col_inputs:
        st.markdown("#### 1. Project Specifications")
        
        structure_type = st.selectbox(
            "Structure Typology",
            options=list(STRUCTURE_CONFIGS.keys()),
            index=0,
            help="Defines structural structural load, reinforcement density, and cost benchmarks."
        )

        built_up_sqft = st.number_input(
            "Built-up Area (Sq. Ft.)",
            min_value=1_000,
            max_value=1_000_000,
            value=35_000,
            step=2_500,
            help="Total gross built-up area (BUA) across all floors."
        )

        location_tier = st.selectbox(
            "Location Tier (Indian Real Estate Geography)",
            options=list(LOCATION_TIERS.keys()),
            index=0,
            help="Applies regional labor indices, material logistics costs, and prevailing real estate market rates."
        )

        completion_pct = st.slider(
            "Project Completion Progress (%)",
            min_value=0,
            max_value=100,
            value=45,
            step=1,
            help="Current milestone completion status used to compute incurred CapEx and work-in-progress valuation."
        )

        finish_grade = st.radio(
            "Architectural Specification Grade",
            options=["Standard Commercial / Premium Residential", "Luxury High-End Grade (+18% Fitout)"],
            horizontal=True
        )

    # Compute Quantities and Valuations
    struct_info = STRUCTURE_CONFIGS[structure_type]
    tier_info = LOCATION_TIERS[location_tier]

    base_sqft_cost = struct_info["base_cost_sqft"] * tier_info["cost_multiplier"]
    if "Luxury" in finish_grade:
        base_sqft_cost *= 1.18

    # Budget Calculations
    total_civil_budget = built_up_sqft * base_sqft_cost
    prelims_contingency = total_civil_budget * 0.08
    total_project_budget = total_civil_budget + prelims_contingency

    # CapEx Incurred
    capex_incurred = total_project_budget * (completion_pct / 100.0)

    # Market Valuation: Incomplete asset valuation combines land equity, incurred CapEx, and developer margin
    market_rate_sqft_avg = sum(tier_info["market_rate_sqft_range"]) / 2.0
    completed_market_value = built_up_sqft * market_rate_sqft_avg
    
    # Work-in-progress asset valuation (Land baseline + Incurred CapEx + 15% progress value addition)
    land_equity_component = completed_market_value * 0.35 # 35% typical land ratio in Indian metros
    current_asset_valuation = land_equity_component + (capex_incurred * 1.15)
    if completion_pct == 100:
        current_asset_valuation = completed_market_value

    # Material Estimations (Standard Civil Engineering Norms)
    total_steel_kg = built_up_sqft * struct_info["steel_kg_sqft"]
    total_steel_mt = total_steel_kg / 1000.0

    total_cement_bags = int(built_up_sqft * struct_info["cement_bags_sqft"])
    total_cement_mt = (total_cement_bags * 50) / 1000.0

    # Milestone details
    milestone_title, milestone_desc = get_current_milestone(completion_pct)

    with col_summary:
        st.markdown("#### 2. Financial & Milestone Overview")
        
        # Milestone Progress Bar
        st.markdown(f"**Current Milestone:** `{milestone_title}`")
        st.progress(completion_pct / 100.0)
        st.caption(f"{milestone_desc} (Progress: **{completion_pct}%**)")

        # Metric Cards
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        with m1:
            render_metric_card("Total Project Budget", format_inr(total_project_budget), f"@ ₹{base_sqft_cost:,.0f} / sqft", "#F59E0B")
        with m2:
            render_metric_card("CapEx Incurred", format_inr(capex_incurred), f"{completion_pct}% funds disbursed", "#3B82F6")

        st.markdown("<br>", unsafe_allow_html=True)
        m3, m4 = st.columns(2)
        with m3:
            render_metric_card("Current Asset Valuation", format_inr(current_asset_valuation), "WIP market equity (INR)", "#10B981")
        with m4:
            render_metric_card("Valuation at Handover", format_inr(completed_market_value), f"@ ₹{market_rate_sqft_avg:,.0f}/sqft", "#8B5CF6")

    st.markdown("---")

    # Material Requirements & Engineering Ratios Row
    st.markdown("#### 3. Structural Material Requirements (CPWD & IS Norms)")
    st.caption("Accredited consumption factors for Fe 500D TMT Reinforcement Steel and 50kg Bags of OPC 53 / PPC Cement.")

    mat1, mat2, mat3, mat4 = st.columns(4)
    with mat1:
        render_metric_card("TMT Steel Rebar (Fe 500D)", f"{total_steel_mt:,.1f} MT", f"Norm: {struct_info['steel_kg_sqft']} kg/sqft", "#F59E0B")
    with mat2:
        render_metric_card("Cement Consumption", f"{total_cement_bags:,} Bags", f"({total_cement_mt:,.0f} MT total)", "#10B981")
    with mat3:
        river_sand_cft = int(built_up_sqft * 1.8)
        render_metric_card("Fine Aggregates (M-Sand)", f"{river_sand_cft:,} cft", "Norm: 1.8 cft/sqft", "#64748B")
    with mat4:
        coarse_agg_cft = int(built_up_sqft * 2.4)
        render_metric_card("Coarse Aggregates (20mm)", f"{coarse_agg_cft:,} cft", "Norm: 2.4 cft/sqft", "#64748B")

    st.markdown("---")

    # Pollinations AI Conceptual 3D Architectural Rendering
    st.markdown("#### 4. Conceptual 3D Architectural Rendering (Pollinations AI Integration)")
    st.caption("Automated photorealistic 3D architectural rendering synthesis tailored to your structural typology, materials, and city landscape.")

    render_c1, render_c2 = st.columns([1, 1], gap="medium")

    with render_c1:
        st.markdown("##### 🎨 Architectural Rendering Parameters")
        arch_style = st.selectbox(
            "Architectural Style",
            ["Modern Brutalist Concrete & Curtain Glazing", "Contemporary Biophilic Parametric Architecture", "Neo-Futuristic Glass & Exposed Steel", "Minimalist Scandinavian Timber & Stone", "Classical Indo-Saracenic Revival"],
            index=1
        )
        time_lighting = st.selectbox(
            "Atmospheric Lighting",
            ["Golden Hour Sunset Lighting, warm dramatic reflections", "Crisp Architectural Midday Sunlight, clear blue sky", "Dusk Blue Hour with warm interior illumination", "Dramatic Moody Overcast Sky, diffuse soft shadows"],
            index=0
        )
        facade_material = st.selectbox(
            "Facade Materiality",
            ["Double Glazed Low-E Glass, bronze louvers, vertical gardens", "Exposed Fair-Faced Architectural Concrete, black aluminum trims", "Terracotta Baguettes, composite aluminum cladding panels", "Local Basalt Stone, perforated corten steel screens"],
            index=0
        )

        # Dynamic Pollinations prompt generator
        default_prompt = (
            f"ultra-detailed 8k photorealistic architectural rendering of a {structure_type} in {tier_info['tier_name']}, "
            f"{arch_style}, {facade_material}, {time_lighting}, octane render, architectural digest photography, "
            f"award-winning civil engineering, highly detailed landscaping and scale people"
        )

        custom_prompt = st.text_area(
            "Render Synthesis Prompt (Customizable)",
            value=default_prompt,
            height=110
        )

        render_seed = st.number_input("Random Seed (for variation)", min_value=1, max_value=999999, value=42)

        generate_render_btn = st.button("🖼️ Generate 3D Concept Render", type="primary", use_container_width=True)

    with render_c2:
        st.markdown("##### 🏛️ Conceptual Architectural Visualization")
        
        encoded_prompt = urllib.parse.quote(custom_prompt.strip())
        pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=640&nologo=true&seed={render_seed}&model=flux"

        if generate_render_btn or "pollinations_active_url" not in st.session_state:
            st.session_state["pollinations_active_url"] = pollinations_url

        active_url = st.session_state.get("pollinations_active_url", pollinations_url)
        
        st.image(
            active_url,
            caption=f"AI 3D Concept Render: {structure_type} ({arch_style})",
            use_container_width=True
        )

        st.markdown(f"""
        <div style="font-size: 0.78rem; color: #94A3B8; word-break: break-all; margin-top: 4px;">
            <b>Live Render Stream:</b> <a href="{active_url}" target="_blank" style="color: #F59E0B;">Direct CDN High-Res URL</a>
        </div>
        """, unsafe_allow_html=True)
