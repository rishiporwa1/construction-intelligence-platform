"""
Gemini Multimodal Client Wrapper for Construction Intelligence
Handles Gemini 2.5/2.0 API calls, JSON extraction, error recovery,
and seamless fallback to Demonstration Mode.
"""

import os
import json
import logging
from PIL import Image
import streamlit as st

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try importing Google GenAI SDK
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-genai SDK not available; will operate in demo fallback mode.")

from modules.config import GEMINI_MODELS
from modules.mock_data import MOCK_SAFETY_AUDITS, MOCK_CRACK_DIAGNOSTICS, MOCK_CHAT_RESPONSES


def get_active_api_key(user_input_key: str = None) -> str:
    """Retrieve API key from user input, environment, or Streamlit secrets."""
    if user_input_key and user_input_key.strip():
        return user_input_key.strip()
    
    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key.strip():
        return env_key.strip()

    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"].strip()
    except Exception:
        pass

    return ""


def clean_json_response(raw_text: str) -> dict:
    """Safely extracts JSON object from LLM response text."""
    text = raw_text.strip()
    # Remove markdown code fences if present
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    # Find boundaries of JSON if surrounded by additional text
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        text = text[start_idx:end_idx + 1]

    return json.loads(text)


def analyze_site_safety(image: Image.Image, api_key: str = None, demo_mode: bool = False) -> tuple[dict, bool, str]:
    """
    Multimodal prompt analyzing worker PPE compliance under OSHA and IS 456 standards.
    Returns (result_dict, is_demo_mode, status_message)
    """
    active_key = get_active_api_key(api_key)

    if demo_mode or not active_key or not GENAI_AVAILABLE:
        # Return realistic high-fidelity mock data
        logger.info("Using Demonstration Mode for Safety Audit.")
        mock_result = MOCK_SAFETY_AUDITS[0]
        return mock_result, True, "Operating in Demonstration Mode (Pre-calculated OSHA/IS 456 Analysis)"

    system_instruction = """You are a Certified Construction Safety Auditor (OSHA 1926 & IS 456 / IS 3521 / IS 2925 accredited).
Analyze the provided construction site photo for worker PPE compliance and safety hazards.

You MUST respond strictly with a valid JSON object matching this schema:
{
  "safety_score": <integer from 0 to 100>,
  "overall_status": "<Compliant | Moderate Risk | High Risk | Critical Violation>",
  "executive_summary": "<A 2-3 sentence technical summary of site safety conditions>",
  "audit_timestamp": "<ISO timestamp>",
  "standards_referenced": ["OSHA 1926.100", "OSHA 1926.501", "IS 2925", "IS 3521", "IS 456"],
  "ppe_detection": [
    {
      "item": "<e.g., Safety Helmets (IS 2925 / OSHA 1926.100)>",
      "compliance_rate": "<e.g., 80%>",
      "detected_workers": <integer count of workers visible>,
      "compliant_workers": <integer count wearing item>,
      "status": "<Compliant | Partial | Non-Compliant | Not Required>",
      "details": "<Observation of helmets, chin straps, etc.>"
    },
    {
      "item": "<High-Visibility Vests (IS 15809 / OSHA 1926.201)>",
      "compliance_rate": "<e.g., 100%>",
      "detected_workers": <integer>,
      "compliant_workers": <integer>,
      "status": "<Compliant | Partial | Non-Compliant>",
      "details": "<Details>"
    },
    {
      "item": "<Steel-Toe Safety Boots (IS 15298 / OSHA 1926.96)>",
      "compliance_rate": "<e.g., 90%>",
      "detected_workers": <integer>,
      "compliant_workers": <integer>,
      "status": "<Compliant | Partial | Non-Compliant>",
      "details": "<Details>"
    },
    {
      "item": "<Fall Arrest Harnesses (IS 3521 / OSHA 1926.502)>",
      "compliance_rate": "<e.g., 40%>",
      "detected_workers": <integer>,
      "compliant_workers": <integer>,
      "status": "<Compliant | Partial | Non-Compliant | Not Applicable>",
      "details": "<Details on harness tie-off, anchor points, etc.>"
    }
  ],
  "identified_hazards": [
    {
      "hazard": "<Specific hazard description>",
      "severity": "<Low | Medium | High | Critical>",
      "location_in_frame": "<Spatial description, e.g. Left foreground, Scaffold upper tier>",
      "osha_standard": "<Applicable OSHA and IS standard clause>",
      "corrective_remedy": "<Actionable engineering or administrative remedy>"
    }
  ]
}
"""

    prompt = (
        "Perform a thorough multimodal site safety inspection of this construction site photo. "
        "Audit PPE compliance (helmets, high-vis vests, steel-toe boots, fall arrest harnesses) under OSHA 1926 and IS 456. "
        "Enumerate all identified hazards with severity and corrective remedies. Return strict JSON."
    )

    client = genai.Client(api_key=active_key)
    
    last_err = ""
    for model_name in GEMINI_MODELS:
        try:
            logger.info(f"Attempting site safety analysis with model: {model_name}")
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
                system_instruction=system_instruction
            )
            response = client.models.generate_content(
                model=model_name,
                contents=[prompt, image],
                config=config
            )
            parsed = clean_json_response(response.text)
            return parsed, False, f"Live Gemini Multimodal Analysis ({model_name})"
        except Exception as e:
            last_err = str(e)
            logger.warning(f"Model {model_name} failed: {e}. Trying next...")

    # Fallback to high fidelity mock if all live attempts encounter errors
    logger.error(f"Live Gemini API calls failed: {last_err}. Gracefully falling back to demonstration mode.")
    return MOCK_SAFETY_AUDITS[0], True, f"Demo Mode (Live API error: {last_err[:120]})"


def diagnose_concrete_crack(image: Image.Image, api_key: str = None, demo_mode: bool = False, sample_key: str = None) -> tuple[dict, bool, str]:
    """
    Multimodal prompt classifying defect type (Hairline, Settlement, Structural Shear, Thermal Expansion, Spalling)
    with estimated crack width (mm), root causes, recommended engineering repairs, and urgency.
    Returns (result_dict, is_demo_mode, status_message)
    """
    active_key = get_active_api_key(api_key)

    if demo_mode or not active_key or not GENAI_AVAILABLE:
        # Match demo result if preset sample
        if sample_key and sample_key in MOCK_CRACK_DIAGNOSTICS:
            mock_result = MOCK_CRACK_DIAGNOSTICS[sample_key]
        else:
            mock_result = MOCK_CRACK_DIAGNOSTICS["sample_crack_1.jpg"]
        return mock_result, True, "Operating in Demonstration Mode (Pre-calculated Structural Integrity Diagnostics)"

    system_instruction = """You are a Principal Chartered Structural Engineer and Forensic Concrete Pathologist (IS 456:2000, ACI 224R, and BS EN 1504 certified).
Analyze the provided concrete or masonry surface image to diagnose cracking and structural distress.

You MUST respond strictly with a valid JSON object matching this schema:
{
  "defect_type": "<Hairline | Settlement | Structural Shear | Thermal Expansion | Spalling>",
  "structural_element": "<e.g., RCC Beam-Column Junction | Foundation Footing | Masonry Infill Wall | Slab Soffit>",
  "estimated_crack_width_mm": <float, e.g. 2.5>,
  "is_456_threshold_mm": <float, e.g. 0.3 for mild or 0.2 for severe exposure>,
  "is_456_status": "<Within Permissible Architectural Limits | EXCEEDS PERMISSIBLE LIMIT (Severely Critical)>",
  "urgency": "<Monitoring Only (Low) | Attention Needed (Medium) | Urgent Engineering Intervention (High) | Immediate Structural Evacuation (Critical)>",
  "risk_index": <integer from 0 to 100>,
  "root_causes": [
    "<Primary geotechnical, loading, chemical, or shrinkage mechanism>",
    "<Secondary contributing factor>"
  ],
  "recommended_engineering_repairs": [
    {
      "protocol": "<Engineering technique, e.g., Low-viscosity epoxy pressure injection | Structural polyurethane re-grouting | Carbon Fiber Reinforced Polymer (CFRP) wrapping | Micro-concrete patch repair>",
      "specification": "<Relevant standard e.g. IS 456 Annex E / ASTM C881 / ACI 440.2R>",
      "details": "<Step-by-step application guidelines, surface prep, injection pressure, and resin properties>"
    }
  ],
  "is_456_guidelines": "<Detailed technical reference citing IS 456:2000 Clause 35.3.2 crack limits and structural integrity protocols>"
}
"""

    prompt = (
        "Conduct a forensic structural engineering assessment of this concrete/wall defect. "
        "Classify the defect type into Hairline, Settlement, Structural Shear, Thermal Expansion, or Spalling. "
        "Estimate crack width in millimeters, determine root causes, assess urgency, cite IS 456:2000 clauses, "
        "and recommend actionable engineering repairs (epoxy injection, structural re-grouting, CFRP). Return strict JSON."
    )

    client = genai.Client(api_key=active_key)
    
    last_err = ""
    for model_name in GEMINI_MODELS:
        try:
            logger.info(f"Attempting crack diagnostics with model: {model_name}")
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
                system_instruction=system_instruction
            )
            response = client.models.generate_content(
                model=model_name,
                contents=[prompt, image],
                config=config
            )
            parsed = clean_json_response(response.text)
            return parsed, False, f"Live Gemini Multimodal Diagnostics ({model_name})"
        except Exception as e:
            last_err = str(e)
            logger.warning(f"Model {model_name} failed: {e}. Trying next...")

    # Fallback to high fidelity mock
    return MOCK_CRACK_DIAGNOSTICS["sample_crack_1.jpg"], True, f"Demo Mode (Live API error: {last_err[:120]})"


def chat_engineering_assistant(messages: list, prompt: str, api_key: str = None, demo_mode: bool = False) -> str:
    """
    Multi-turn conversation with construction engineering assistant chatbot.
    """
    active_key = get_active_api_key(api_key)

    if demo_mode or not active_key or not GENAI_AVAILABLE:
        # Check keywords for high quality domain response
        p_lower = prompt.lower()
        if "slump" in p_lower or "heat" in p_lower or "hot" in p_lower:
            return MOCK_CHAT_RESPONSES["slump"]
        elif "cover" in p_lower or "marine" in p_lower or "coastal" in p_lower:
            return MOCK_CHAT_RESPONSES["cover"]
        elif "wind" in p_lower or "crane" in p_lower:
            return MOCK_CHAT_RESPONSES["wind"]
        elif "cure" in p_lower or "curing" in p_lower or "fly ash" in p_lower:
            return MOCK_CHAT_RESPONSES["curing"]
        else:
            return f"**Senior Construction Engineering Specialist (Demo Response)**:\n\nRegarding your question on *'{prompt}'*:\n\nUnder **IS 456:2000** and international site engineering best practices:\n- Ensure structural load verification before striking formwork props.\n- Verify test cube compressive strengths (7-day and 28-day curing in water bath).\n- Enforce strict adherence to safety exclusion zones and PPE under OSHA 1926.\n\n*(Connect your Gemini API Key in the sidebar for unlimited, real-time context-aware multi-turn dialogue!)*"

    system_instruction = """You are a Senior Project Director & Principal Structural Engineer (Fellow of Institution of Engineers India).
You provide authoritative, precise, and practical advice on construction engineering, IS Codes (IS 456, IS 1893, IS 875, IS 13920, IS 1200),
OSHA 1926 site safety protocols, concrete mix design, material quality control, and site project management.
Format your responses with clear markdown headers, bold bullet points, and actionable engineering steps.
"""

    client = genai.Client(api_key=active_key)
    
    # Build conversation context
    formatted_contents = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        formatted_contents.append(f"{role.upper()}: {msg['content']}")
    formatted_contents.append(f"USER: {prompt}")
    conversation_prompt = "\n\n".join(formatted_contents)

    for model_name in GEMINI_MODELS:
        try:
            config = types.GenerateContentConfig(
                temperature=0.3,
                system_instruction=system_instruction
            )
            response = client.models.generate_content(
                model=model_name,
                contents=conversation_prompt,
                config=config
            )
            return response.text
        except Exception as e:
            logger.warning(f"Chat model {model_name} failed: {e}")

    return MOCK_CHAT_RESPONSES["default"]
