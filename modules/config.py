"""
Configuration, Constants, and Engineering Benchmarks for
Multimodal Construction Intelligence Platform (Skill Wallet Capstone Project 1)
"""

APP_TITLE = "Multimodal Construction Intelligence Platform"
APP_SUBTITLE = "AI-Powered Infrastructure Inspection, Structural Diagnostics & Real Estate Intelligence"
CAPSTONE_TAG = "Skill Wallet Capstone Project 1"
VERSION = "v2.5.0-PROD"

# Primary Gemini Model Choices in order of priority
GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]

# Structure Types and Material/Cost Norms (Indian Construction Benchmarks)
STRUCTURE_CONFIGS = {
    "Residential High-Rise (RCC Shear Wall)": {
        "base_cost_sqft": 3200,
        "steel_kg_sqft": 4.5,    # Fe 500D TMT
        "cement_bags_sqft": 0.42, # 50kg bags (OPC/PPC)
        "land_ratio_multiplier": 3.8,
        "description": "Multi-storey residential towers utilizing cast-in-situ reinforced concrete shear walls."
    },
    "Commercial Office Complex (Post-Tensioned Slabs)": {
        "base_cost_sqft": 4100,
        "steel_kg_sqft": 5.2,
        "cement_bags_sqft": 0.48,
        "land_ratio_multiplier": 4.5,
        "description": "Grade-A IT/corporate park with post-tensioned wide-span beam-slab systems and curtain glazing."
    },
    "Industrial PEB Warehouse (Pre-Engineered Building)": {
        "base_cost_sqft": 2100,
        "steel_kg_sqft": 3.1,
        "cement_bags_sqft": 0.28,
        "land_ratio_multiplier": 2.2,
        "description": "Logistics hub with structural steel portal frames, insulated sandwich roofing, and FM2 flooring."
    },
    "Luxury Villa Community (Framed RCC / Masonry)": {
        "base_cost_sqft": 3600,
        "steel_kg_sqft": 3.6,
        "cement_bags_sqft": 0.38,
        "land_ratio_multiplier": 3.2,
        "description": "Gated high-end residential villas with duplex RCC framed design and premium architectural finishes."
    },
    "Institutional & Educational Campus": {
        "base_cost_sqft": 2900,
        "steel_kg_sqft": 4.0,
        "cement_bags_sqft": 0.39,
        "land_ratio_multiplier": 2.8,
        "description": "Auditoriums, lecture complexes, and labs engineered for high occupant load per NBC 2016."
    }
}

# Location Tiers in India
LOCATION_TIERS = {
    "Tier 1 (Mumbai MMR, Delhi-NCR, Bengaluru, Hyderabad)": {
        "tier_name": "Tier 1 Metro",
        "cost_multiplier": 1.25,
        "market_rate_sqft_range": (12000, 26000),
        "appreciation_rate": 0.09, # 9% annual appreciation
        "cities": ["Mumbai", "Bengaluru", "Delhi-NCR", "Hyderabad"]
    },
    "Tier 2 (Pune, Ahmedabad, Chennai, Kolkata, Kochi, Chandigarh)": {
        "tier_name": "Tier 2 Growth Hub",
        "cost_multiplier": 1.05,
        "market_rate_sqft_range": (6500, 14500),
        "appreciation_rate": 0.075,
        "cities": ["Pune", "Ahmedabad", "Chennai", "Kolkata", "Kochi", "Chandigarh"]
    },
    "Tier 3 (Indore, Lucknow, Coimbatore, Jaipur, Bhubaneswar, Vizag)": {
        "tier_name": "Tier 3 Emerging Smart City",
        "cost_multiplier": 0.90,
        "market_rate_sqft_range": (3800, 7800),
        "appreciation_rate": 0.06,
        "cities": ["Indore", "Lucknow", "Coimbatore", "Jaipur", "Bhubaneswar", "Visakhapatnam"]
    }
}

# Concrete Crack Defect Types per IS 456 & ACI 224R
DEFECT_TYPES = [
    "Hairline",
    "Settlement",
    "Structural Shear",
    "Thermal Expansion",
    "Spalling"
]

# Weather Condition Presets
WEATHER_CONDITIONS = {
    "High Wind (> 38 km/h / Gale Warning)": {
        "status": "High Risk",
        "color": "#EF4444",
        "icon": "💨",
        "wind_speed": "42 km/h",
        "temp": "28°C",
        "humidity": "65%",
        "safety_bulletins": [
            "🔴 CRANE SHUTDOWN: Immediately suspend all tower crane slewing and mobile boom placers per OSHA 1926.1431 and IS 13367.",
            "⚠️ SCAFFOLDING LOCKOUT: Restrict all personnel from external perimeter suspended cradles and mast climbers.",
            "🛠️ DEBRIS CONTAINMENT: Fasten loose aluminum formwork panels, corrugated roof sheets, and peripheral safety mesh.",
            "🔒 TOWER CRANE PROTOCOL: Release mechanical slewing brakes on all tower cranes to allow free weathervaning."
        ]
    },
    "Heavy Rain (Monsoon / Cloudburst Alert)": {
        "status": "Severe Hazard",
        "color": "#3B82F6",
        "icon": "🌧️",
        "wind_speed": "24 km/h",
        "temp": "24°C",
        "humidity": "95%",
        "safety_bulletins": [
            "🚫 CONCRETING MORATORIUM: Halt all exposed concrete pouring to avoid washing out cement matrix and uncalibrated w/c ratio rise.",
            "⚡ ELECTRICAL ISOLATION: De-energize un-sheltered temporary distribution boards (DBs) and inspect GFCI/ELCB breakers.",
            "🚜 TRENCH & PIT SHORING: Inspect deep foundation excavations for hydrostatic collapse; activate high-head dewatering sump pumps.",
            "🚶 SLIP & TRIP MITIGATION: Prohibit steel-beam walking; mandate non-slip rubberized cleated footwear."
        ]
    },
    "Extreme Heat (> 40°C / Hot Weather Concreting)": {
        "status": "Advisory / Thermal Stress",
        "color": "#F59E0B",
        "icon": "☀️",
        "wind_speed": "12 km/h",
        "temp": "43°C",
        "humidity": "25%",
        "safety_bulletins": [
            "🧊 IS 7861 (Part 1) CONCRETE PROTOCOL: Replace 30% mixing water with chilled flake ice; maintain delivery concrete temp < 32°C.",
            "💧 ACCELERATED CURING: Double ponding & wet hessian burlap wrapping cycles; apply paraffin-based curing compound immediately after initial set.",
            "🕒 SHIFT RESCHEDULING: Mandate split shifts; shift mass-concreting and post-tensioning to night hours (19:00 - 05:00 hrs).",
            "🚰 WORKER WELFARE: Provide mandatory electrolyte hydration booths every 30 meters; enforce 15-min shade rest hourly."
        ]
    },
    "Normal / Favorable Working Conditions": {
        "status": "Optimal Operational",
        "color": "#10B981",
        "icon": "🌤️",
        "wind_speed": "14 km/h",
        "temp": "27°C",
        "humidity": "55%",
        "safety_bulletins": [
            "✅ ALL WORK CLEARED: Full authorization for hot works, high-altitude facade glazing, and structural concreting.",
            "📋 STANDARD IS 456 CURING: Maintain uninterrupted water curing for minimum 7 days (OPC) or 10 days (blended cements).",
            "🔍 DAILY LOGGING: Perform standard pre-shift inspection of wire ropes, safety harnesses, and fire extinguishers."
        ]
    }
}
