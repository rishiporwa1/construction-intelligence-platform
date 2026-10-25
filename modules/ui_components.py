"""
Reusable UI Components, CSS Injection, Metric Cards, Status Pills, and Visualizations
for Multimodal Construction Intelligence Platform
"""

import streamlit as st
import plotly.graph_objects as go
import json

def apply_custom_css():
    """Inject polished industrial tech styling for the platform."""
    st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3.5rem;
        max-width: 95rem;
    }

    /* Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(245, 158, 11, 0.35);
        border-radius: 12px;
        padding: 22px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 0 15px rgba(245, 158, 11, 0.1);
    }
    
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #F59E0B 0%, #FBBF24 50%, #F8FAFC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        font-weight: 400;
        margin-top: 6px;
        margin-bottom: 0;
    }

    /* Card styling */
    .metric-card {
        background: #1E293B;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: rgba(245, 158, 11, 0.4);
        transform: translateY(-2px);
    }
    .metric-title {
        color: #94A3B8;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 4px;
    }
    .metric-val {
        color: #F8FAFC;
        font-size: 1.8rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1.2;
    }
    .metric-sub {
        color: #64748B;
        font-size: 0.78rem;
        margin-top: 5px;
    }

    /* Status Pills */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.4px;
        text-transform: uppercase;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    .pill-compliant {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid #10B981;
    }
    .pill-moderate {
        background: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid #F59E0B;
    }
    .pill-high {
        background: rgba(249, 115, 22, 0.18);
        color: #F97316;
        border: 1px solid #F97316;
    }
    .pill-critical {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid #EF4444;
        animation: pulse-red 2s infinite;
    }
    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        70% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    /* Section Cards */
    .section-card {
        background: #131E31;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Demo Mode Banner */
    .demo-banner {
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid #F59E0B;
        border-radius: 8px;
        padding: 10px 16px;
        color: #FCD34D;
        font-size: 0.85rem;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Code & JSON styling */
    pre, code {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Streamlit Tabs custom look */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        border-radius: 8px 8px 0px 0px;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0px 18px;
        color: #94A3B8;
    }
    .stTabs [aria-selected="true"] {
        color: #F59E0B !important;
        border-bottom: 3px solid #F59E0B !important;
        background: rgba(245, 158, 11, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)


def render_hero_header():
    """Renders the top application branding banner."""
    st.markdown("""
    <div class="hero-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <h1 class="hero-title">🏗️ Multimodal Construction Intelligence Platform</h1>
                <p class="hero-subtitle">Production-Ready AI Inspection • PPE Compliance (OSHA & IS 456) • Crack Diagnostics • Real Estate Valuation • Site Safety Advisory</p>
            </div>
            <div>
                <span style="background: rgba(245,158,11,0.2); color: #FBBF24; border: 1px solid #F59E0B; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 700;">
                    SKILL WALLET CAPSTONE 1
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(title: str, value: str, subtext: str = "", border_color: str = "#F59E0B"):
    """Renders a styled metric card."""
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid {border_color};">
        <div class="metric-title">{title}</div>
        <div class="metric-val">{value}</div>
        {f'<div class="metric-sub">{subtext}</div>' if subtext else ''}
    </div>
    """, unsafe_allow_html=True)


def get_status_pill_html(status_text: str, severity: str = "info") -> str:
    """Returns HTML for a color-coded status badge."""
    sev = severity.lower()
    if any(k in sev for k in ["compliant", "safe", "optimal", "low"]):
        cls = "pill-compliant"
        icon = "✓"
    elif any(k in sev for k in ["moderate", "medium", "advisory", "attention"]):
        cls = "pill-moderate"
        icon = "⚠️"
    elif any(k in sev for k in ["high", "warning"]):
        cls = "pill-high"
        icon = "⚡"
    elif any(k in sev for k in ["critical", "severe", "violation", "breach"]):
        cls = "pill-critical"
        icon = "🚨"
    else:
        cls = "pill-moderate"
        icon = "ℹ️"
    
    return f'<span class="status-pill {cls}">{icon} {status_text}</span>'


def render_compliance_donut(score: int, title: str = "Safety Index"):
    """Creates a stylized Plotly gauge / donut chart for Safety Score."""
    # Color logic
    if score >= 80:
        bar_color = "#10B981" # Green
    elif score >= 60:
        bar_color = "#F59E0B" # Amber
    elif score >= 40:
        bar_color = "#F97316" # Orange
    else:
        bar_color = "#EF4444" # Red

    fig = go.Figure(go.Pie(
        values=[score, 100 - score],
        hole=0.72,
        marker=dict(colors=[bar_color, "rgba(255,255,255,0.06)"]),
        textinfo='none',
        hoverinfo='none',
        sort=False,
        direction='clockwise',
        rotation=90
    ))

    fig.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=190,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[
            dict(
                text=f"<b>{score}%</b><br><span style='font-size:12px; color:#94A3B8;'>{title}</span>",
                x=0.5, y=0.5,
                font=dict(size=24, color="#F8FAFC", family="JetBrains Mono"),
                showarrow=False
            )
        ]
    )
    return fig


def render_hazard_severity_bar(hazards_list: list):
    """Plotly horizontal bar showing counts of hazards by severity."""
    severities = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    colors = {
        "Critical": "#EF4444",
        "High": "#F97316",
        "Medium": "#F59E0B",
        "Low": "#10B981"
    }

    for h in hazards_list:
        sev = h.get("severity", "Medium")
        if sev in severities:
            severities[sev] += 1
        else:
            severities["Medium"] += 1

    fig = go.Figure()
    for sev, count in severities.items():
        fig.add_trace(go.Bar(
            y=[sev],
            x=[count],
            orientation='h',
            name=sev,
            marker=dict(color=colors[sev], line=dict(color='rgba(255,255,255,0.1)', width=1)),
            text=[f"{count} identified"],
            textposition='auto',
        ))

    fig.update_layout(
        showlegend=False,
        height=180,
        margin=dict(t=10, b=25, l=80, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.06)',
            tickfont=dict(color='#94A3B8'),
            dtick=1
        ),
        yaxis=dict(
            tickfont=dict(color='#F8FAFC', size=12, family="Inter")
        )
    )
    return fig


def download_json_button(data: dict, file_name: str, label: str = "📥 Download Structured JSON Report"):
    """Renders a download button for structured JSON."""
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    st.download_button(
        label=label,
        data=json_str,
        file_name=file_name,
        mime="application/json",
        use_container_width=True
    )
