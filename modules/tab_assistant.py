"""
Tab 4: Daily Site Assistant & Weather-Aware Advisory (Epic 5)
Provides dynamic weather safety alerts (High Wind, Heavy Rain, Extreme Heat, Normal)
and an interactive multi-turn construction engineering assistant chatbot.
"""

import streamlit as st
from modules.config import WEATHER_CONDITIONS
from modules.gemini_client import chat_engineering_assistant
from modules.ui_components import get_status_pill_html

QUICK_PROMPTS = [
    "How to prevent slump loss and cold joints in M35 concrete under 42°C ambient heat?",
    "What is the IS 456 minimum concrete cover requirement for severe coastal marine exposure?",
    "At what wind speed must tower crane and mobile boom placer operations be suspended?",
    "What are the mandatory curing duration standards for fly-ash blended PPC concrete?"
]


def render_tab_assistant(api_key: str, demo_mode: bool):
    """Render Tab 4 - Daily Site Assistant & Weather-Aware Advisory Module."""
    st.markdown("### 🌤️ Daily Site Assistant & Weather-Aware Safety Advisory (Epic 5)")
    st.caption("Real-time weather risk mitigation protocols (IS 13367 / IS 7861 / OSHA 1926) and multi-turn construction engineering conversational intelligence.")

    # 1. Weather Safety Advisory Section
    st.markdown("#### 1. Dynamic Weather-Aware Safety Advisory")
    
    selected_weather = st.selectbox(
        "Current Site Weather Condition",
        options=list(WEATHER_CONDITIONS.keys()),
        index=0,
        help="Select prevailing weather conditions to trigger automated safety advisories and operational moratoriums."
    )

    weather_data = WEATHER_CONDITIONS[selected_weather]
    w_status = weather_data["status"]
    w_icon = weather_data["icon"]
    w_color = weather_data["color"]

    # Weather Banner
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.9); border: 2px solid {w_color}; border-radius: 10px; padding: 18px 22px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 2.2rem;">{w_icon}</span>
                <div>
                    <h4 style="margin: 0; color: #F8FAFC;">{selected_weather}</h4>
                    <span style="color: #94A3B8; font-size: 0.85rem;">Wind: <b>{weather_data['wind_speed']}</b> | Temp: <b>{weather_data['temp']}</b> | Rel. Humidity: <b>{weather_data['humidity']}</b></span>
                </div>
            </div>
            <div>
                {get_status_pill_html(w_status, w_status)}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Display dynamic safety bulletins
    st.markdown("##### ⚠️ Mandatory Safety Mandates & Engineering Protocols:")
    bulletin_cols = st.columns(2)
    for idx, bulletin in enumerate(weather_data["safety_bulletins"]):
        col_target = bulletin_cols[idx % 2]
        with col_target:
            st.markdown(f"""
            <div style="background: #131E31; border-left: 3px solid {w_color}; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px; font-size: 0.88rem; color: #F1F5F9;">
                {bulletin}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 2. Interactive Multi-Turn Construction Engineering Chatbot
    st.markdown("#### 2. Interactive Multi-Turn Construction Engineering Assistant")
    st.caption("Ask questions regarding IS Codes (IS 456, IS 1893, IS 875, IS 13920), OSHA 1926 regulations, concrete mix design, structural curing, and site scheduling.")

    # Quick prompt buttons
    st.markdown("##### 💡 Suggested Engineering Inquiries:")
    chip_cols = st.columns(len(QUICK_PROMPTS))
    chosen_prompt_from_chip = None
    for idx, prompt_text in enumerate(QUICK_PROMPTS):
        with chip_cols[idx]:
            # Truncated button text
            short_title = prompt_text.split("?")[0][:36] + "..."
            if st.button(f"📌 {short_title}", key=f"chip_{idx}", use_container_width=True):
                chosen_prompt_from_chip = prompt_text

    # Initialize chat history in session state
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": (
                    "**Welcome to the Construction Engineering Intelligence Assistant.**\n\n"
                    "I am programmed with comprehensive expertise in **IS 456:2000, OSHA 1926, NBC 2016**, "
                    "structural forensics, concrete mix technology, and construction QA/QC.\n\n"
                    "How can I assist your site operations today?"
                )
            }
        ]

    # Render Chat History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["chat_messages"]:
            avatar = "🤖" if msg["role"] == "assistant" else "👷"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    # Handle input from user chat input OR quick chip
    user_query = st.chat_input("Enter your structural engineering or site query here...")
    active_prompt = chosen_prompt_from_chip if chosen_prompt_from_chip else user_query

    if active_prompt:
        # Append user message
        st.session_state["chat_messages"].append({"role": "user", "content": active_prompt})
        with st.chat_message("user", avatar="👷"):
            st.markdown(active_prompt)

        # Generate response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Consulting structural engineering knowledge base & regulatory standards..."):
                response_text = chat_engineering_assistant(
                    messages=st.session_state["chat_messages"][:-1],
                    prompt=active_prompt,
                    api_key=api_key,
                    demo_mode=demo_mode
                )
                st.markdown(response_text)
                st.session_state["chat_messages"].append({"role": "assistant", "content": response_text})

    # Clear chat button
    col_space, col_clear = st.columns([5, 1])
    with col_clear:
        if st.button("🗑️ Reset Chat", use_container_width=True):
            st.session_state["chat_messages"] = [
                {
                    "role": "assistant",
                    "content": "Chat history reset. How can I assist your site operations today?"
                }
            ]
            st.rerun()
