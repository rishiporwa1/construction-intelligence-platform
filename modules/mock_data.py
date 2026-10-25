"""
High-Fidelity Synthetic & Demonstration Data Engine
Provides realistic OSHA & IS 456 safety audits, crack diagnostics, and engineering responses
when running without an active Gemini API key or in Demonstration Mode.
"""

from datetime import datetime

# Sample Safety Audit Results for Demonstration Mode
MOCK_SAFETY_AUDITS = [
    {
        "safety_score": 68,
        "overall_status": "Moderate Risk",
        "executive_summary": "Audit conducted on perimeter scaffolding elevation. Compliance is satisfactory for hard hats and steel-toe footwear, but serious fall arrest and PPE lapses were observed at working heights exceeding 6 meters. Immediate corrective scaffolding ties and lifeline installations are mandated under OSHA 1926.501 and IS 3521.",
        "audit_timestamp": datetime.now().isoformat(),
        "standards_referenced": ["OSHA 1926.501", "OSHA 1926.100", "IS 2925:1984", "IS 3521:1999", "IS 456:2000 Cl. 35"],
        "ppe_detection": [
            {
                "item": "Safety Helmets (IS 2925 / OSHA 1926.100)",
                "compliance_rate": "80%",
                "detected_workers": 5,
                "compliant_workers": 4,
                "status": "Partial",
                "details": "4 out of 5 workers wearing Type 1 Class E industrial hard hats; 1 worker in lower zone unbuckled."
            },
            {
                "item": "High-Visibility Vests (IS 15809 / OSHA 1926.201)",
                "compliance_rate": "100%",
                "detected_workers": 5,
                "compliant_workers": 5,
                "status": "Compliant",
                "details": "All workers wearing Class 2 retro-reflective high-vis safety vests."
            },
            {
                "item": "Steel-Toe Safety Boots (IS 15298 / OSHA 1926.96)",
                "compliance_rate": "100%",
                "detected_workers": 5,
                "compliant_workers": 5,
                "status": "Compliant",
                "details": "Ankle-high puncture-resistant protective safety boots observed on all personnel."
            },
            {
                "item": "Full Body Harness & Lanyard (IS 3521 / OSHA 1926.502)",
                "compliance_rate": "33%",
                "detected_workers": 3,
                "compliant_workers": 1,
                "status": "Non-Compliant",
                "details": "Only 1 worker properly tied off to an independent static lifeline; 2 workers unhooked on cantilevered stage."
            }
        ],
        "identified_hazards": [
            {
                "hazard": "Cantilever Scaffolding Edge Without Lanyard Tie-Off",
                "severity": "Critical",
                "location_in_frame": "Elevation Level 3, Eastern Scaffolding Bay",
                "osha_standard": "OSHA 1926.501(b)(1) & IS 3521 Fall Protection",
                "corrective_remedy": "Issue immediate Stop-Work Order on Bay 3. Install 12mm dual polyamide static lifelines and enforce 100% tie-off with shock-absorbing lanyards before work resumption."
            },
            {
                "hazard": "Uncovered Floor Penetration Adjacent to Material Hoist",
                "severity": "High",
                "location_in_frame": "Mid-deck platform slab opening",
                "osha_standard": "OSHA 1926.501(b)(4) Hole Cover Protocol",
                "corrective_remedy": "Fasten securely marked 25mm structural plywood cover labeled 'HOLE - DO NOT REMOVE' capable of supporting 2x maximum anticipated axle load."
            },
            {
                "hazard": "Obstructed Emergency Egress by Formwork Timbers",
                "severity": "Medium",
                "location_in_frame": "Lower transit gangway walkway",
                "osha_standard": "OSHA 1926.25 Housekeeping & IS 456 Site Safety",
                "corrective_remedy": "Clear timber runners and tie-wire scrap into designated timber skips within 2 hours."
            }
        ]
    },
    {
        "safety_score": 92,
        "overall_status": "Compliant",
        "executive_summary": "Superstructure casting inspection reveals outstanding compliance with Indian and international safety norms. Workers demonstrate full adherence to helmet straps, reflective gear, protective footwear, and edge handrail protections. General housekeeping is well maintained.",
        "audit_timestamp": datetime.now().isoformat(),
        "standards_referenced": ["OSHA 1926.100", "OSHA 1926.102", "IS 2925:1984", "IS 15298"],
        "ppe_detection": [
            {
                "item": "Safety Helmets (IS 2925 / OSHA 1926.100)",
                "compliance_rate": "100%",
                "detected_workers": 4,
                "compliant_workers": 4,
                "status": "Compliant",
                "details": "All workers wearing chin-strapped industrial safety helmets."
            },
            {
                "item": "High-Visibility Vests (IS 15809)",
                "compliance_rate": "100%",
                "detected_workers": 4,
                "compliant_workers": 4,
                "status": "Compliant",
                "details": "Clean fluorescent vests with certified retro-reflective bands."
            },
            {
                "item": "Steel-Toe Safety Boots (IS 15298)",
                "compliance_rate": "100%",
                "detected_workers": 4,
                "compliant_workers": 4,
                "status": "Compliant",
                "details": "Standard puncture-resistant steel toe protection verified."
            },
            {
                "item": "Fall Arrest Harnesses (IS 3521)",
                "compliance_rate": "100%",
                "detected_workers": 2,
                "compliant_workers": 2,
                "status": "Compliant",
                "details": "Workers near leading edge secured with double-lanyard carabiners to certified anchor points."
            }
        ],
        "identified_hazards": [
            {
                "hazard": "Uncapped Vertical Rebar Dowels (Impalement Risk)",
                "severity": "Medium",
                "location_in_frame": "Ground slab rebar starter cage",
                "osha_standard": "OSHA 1926.701(b) Rebar Protection",
                "corrective_remedy": "Install high-visibility mushroom safety caps or wood troughs over all exposed starter bars."
            }
        ]
    }
]

# Sample Crack Diagnostics for Demonstration Mode
MOCK_CRACK_DIAGNOSTICS = {
    "sample_crack_1.jpg": {
        "defect_type": "Structural Shear",
        "structural_element": "Reinforced Concrete (RCC) Column-Beam Joint",
        "estimated_crack_width_mm": 2.8,
        "is_456_threshold_mm": 0.3,
        "is_456_status": "EXCEEDS PERMISSIBLE LIMIT (Severely Critical)",
        "urgency": "Urgent Engineering Intervention (High)",
        "risk_index": 88,
        "root_causes": [
            "Principal diagonal tension stress exceeding tensile capacity of concrete (f_cr = 0.7*sqrt(f_ck)).",
            "Inadequate shear stirrup containment spacing near column-beam junction under combined gravity and lateral cyclic shear.",
            "Differential settlement or seismic shear stress concentration."
        ],
        "recommended_engineering_repairs": [
            {
                "protocol": "Low-Viscosity Structural Epoxy Pressure Injection",
                "specification": "ASTM C881 / IS 456 Annex E",
                "details": "Seal exterior surface with epoxy mastic, install injection ports at 150mm intervals, and inject low-viscosity thermosetting epoxy resin (viscosity < 200 cps) from bottom upwards until refusal."
            },
            {
                "protocol": "Carbon Fiber Reinforced Polymer (CFRP) Shear Jacketing",
                "specification": "ACI 440.2R / FIB Bulletin 14",
                "details": "Wrap 2 layers of bidirectional woven CFRP fabric around column face with structural saturant epoxy to restore shear ductility and confinement."
            },
            {
                "protocol": "Non-Destructive Testing (NDT) Verification",
                "specification": "IS 13311 (Part 1 & 2)",
                "details": "Conduct Ultrasonic Pulse Velocity (UPV) and Rebound Hammer survey post-curing to confirm crack depth penetration and structural continuity."
            }
        ],
        "is_456_guidelines": "IS 456:2000 Clause 35.3.2 strictly specifies crack width limits: 0.3 mm for mild exposure, 0.2 mm for moderate, and 0.1 mm for severe coastal exposure. The current 2.8 mm crack represents structural shear distress requiring immediate shoring and propping."
    },
    "sample_crack_2.jpg": {
        "defect_type": "Hairline",
        "structural_element": "External Masonry & Plastered Wall Surface",
        "estimated_crack_width_mm": 0.15,
        "is_456_threshold_mm": 0.3,
        "is_456_status": "Within Permissible Architectural Limits",
        "urgency": "Monitoring Only (Low)",
        "risk_index": 22,
        "root_causes": [
            "Plastic shrinkage and rapid surface moisture loss during early cement plaster hydration.",
            "High sand fineness modulus variance or rich cement-sand plaster mix ratio.",
            "Differential thermal movement between masonry substrate and external render."
        ],
        "recommended_engineering_repairs": [
            {
                "protocol": "Elastomeric Waterproof Anti-Carbonation Coating",
                "specification": "BS EN 1504-2",
                "details": "Open crack to 2mm V-groove with angle grinder, brush apply acrylic-polymer crack-fill paste, and coat with two layers of crack-bridging elastomeric exterior emulsion."
            },
            {
                "protocol": "Periodic Crack Monitoring Gauge (Demec Points)",
                "specification": "BS 7542",
                "details": "Install acrylic calibrated tell-tale crack monitoring plates to verify if the crack is active or dormant over 90 days."
            }
        ],
        "is_456_guidelines": "Hairline crazing under 0.2 mm in non-structural plaster does not threaten load-bearing capacity but requires moisture barrier sealing to prevent internal dampness."
    },
    "sample_crack_3.jpg": {
        "defect_type": "Spalling",
        "structural_element": "RCC Perimeter Beam Soffit with Exposed Rebar",
        "estimated_crack_width_mm": 8.5,
        "is_456_threshold_mm": 0.2,
        "is_456_status": "SEVERE SERVICEABILITY & STRUCTURAL FAILURE",
        "urgency": "Immediate Structural Evacuation (Critical)",
        "risk_index": 95,
        "root_causes": [
            "Deep carbonation front reaching reinforcement depth (pH dropped < 9.0), destroying protective passive ferric oxide layer.",
            "Chloride-induced electrochemical corrosion causing expansive iron oxide formation (expanding volume 3x to 6x), creating bursting tensile stress in concrete cover.",
            "Substandard concrete cover (less than IS 456 specified 40mm for severe environments)."
        ],
        "recommended_engineering_repairs": [
            {
                "protocol": "Mechanical Concrete Chipping & Substrate Preparation",
                "specification": "ICRI Guideline 310.1R",
                "details": "Chop loose, unsound concrete 20mm behind corroded reinforcing bars using light pneumatic chisels to relieve corrosion wedging."
            },
            {
                "protocol": "Rebar De-Rusting & Sacrificial Zinc Primer Application",
                "specification": "IS 9077 / ASTM A775",
                "details": "Grit-blast exposed rebar to SA 2.5 bright metal finish; immediately apply two coats of zinc-rich epoxy primer (90% metallic zinc in dry film)."
            },
            {
                "protocol": "Polymer Modified Mortar (PMM) / Micro-Concrete Re-Grouting",
                "specification": "IS 456 Cl. 26.5 & EN 1504-3 Class R4",
                "details": "Apply aliphatic epoxy bonding agent and build up section with styrene-butadiene rubber (SBR) polymer modified structural repair mortar."
            }
        ],
        "is_456_guidelines": "IS 456:2000 Clause 26.4 requires mandatory minimum cover of 40-50mm in aggressive conditions. Spalled reinforcement must be restored and re-passivated immediately."
    }
}

# Chatbot Domain-Specific Simulated Responses
MOCK_CHAT_RESPONSES = {
    "slump": """**Engineering Advisory: Permissible Slump Loss in Hot Weather Concreting (IS 7861 Part 1 & IS 456)**

Under high ambient temperatures (>40°C), concrete undergoes rapid moisture evaporation and accelerated cement hydration, typically causing a slump loss of **40mm to 80mm within 45 minutes** of batching.

**Key Mitigation Protocols:**
1. **Initial Slump Adjustment**: Design the mix with a higher initial slump of **150–180 mm** utilizing polycarboxylate ether (PCE) based hyper-plasticizers with extended slump retention (up to 90 mins).
2. **Batching Water Chilling**: Replace 25–40% of mixing water with flake ice to maintain fresh concrete temperature below **32°C** at point of discharge.
3. **Do NOT Re-temper with Raw Water**: Strictly prohibit adding raw water at site. Only use calibrated supplementary superplasticizer dosing under site QA engineer supervision.
4. **Placement Window**: Limit transit time to < 45 minutes; schedule large structural pours between 19:00 hrs and 05:00 hrs.""",

    "cover": """**IS 456:2000 Clause 26.4: Mandatory Minimum Concrete Cover Requirements**

For severe coastal / marine environments (within 5 km of sea coast or saline air):
- **Beams**: Minimum nominal cover = **40 mm** (increased to 50 mm for severe sea-spray splash zone).
- **Columns**: Minimum nominal cover = **45 mm** (or longitudinal bar diameter, whichever is greater).
- **Footings / Raft Foundation**: Minimum cover = **50 mm** (often 75 mm against lean concrete).
- **Slabs**: Minimum nominal cover = **25 mm to 30 mm**.

*Engineering Note:* Use Grade M35 or higher with minimum cement content of **340 kg/m³** and maximum water-cement ratio of **0.45** per IS 456 Table 5 to prevent chloride-induced corrosion.""",

    "wind": """**Tower Crane Wind Speed Limits & Safety Shutdown (IS 13367 / OSHA 1926.1431)**

1. **Standard Maximum Operational Limit**: **38 km/h (10.5 m/s or ~20 knots)**.
   - When sustained wind speeds reach 38 km/h, all lifting of large surface area materials (formwork panels, curtain wall glass, cladding sheets) must be suspended immediately.
2. **Complete Operation Shutdown**: **50 km/h (14 m/s)**.
   - All crane operations must cease immediately.
   - Boom must be parked in approved park radius.
3. **Weathervaning Protocol**:
   - The slewing brake must be **disengaged / released** so the crane jib can freely turn (weathervane) with the wind, minimizing wind drag torque against the tower mast structure.
   - Verify anemometer calibration on the crane jib tip weekly.""",

    "curing": """**IS 456:2000 Clause 13.5: Curing Durations & Regimes**

1. **Ordinary Portland Cement (OPC 43 / 53 Grade)**:
   - Minimum **7 days** of moist/wet curing in normal conditions.
   - Minimum **10 days** when exposed to hot, dry, or windy conditions.
2. **Blended Cements (PPC with Fly Ash, PSC with Slag, or GGBS mixes)**:
   - Minimum **10 days** standard moist curing.
   - Minimum **14 days** under hot/dry weather conditions (due to slower pozzolanic reaction kinetics).
3. **Methods Mandated**:
   - Horizontal Slabs: Ponding with water depth ≥ 25 mm.
   - Columns & Vertical Walls: Continuous wet hessian/burlap wrapping encased in 100-micron polythene sheet or certified liquid membrane-forming curing compound complying with ASTM C309.""",

    "default": """**Multimodal Construction Site Engineering Assistant**

I am ready to assist with your construction engineering, QA/QC, structural integrity, and site safety management needs.

I can guide you on:
- **IS Codes**: IS 456:2000 (RCC), IS 1893 (Seismic), IS 875 (Wind/Dead loads), IS 13920 (Ductile Detailing), IS 1200 (Measurement).
- **OSHA 1926 Standards**: Scaffolding, Fall Protection, Trench Shoring, Crane Safety.
- **Concrete Technology**: Mix design, slump loss, hot/cold weather concreting, non-destructive testing (UPV, Rebound).
- **Quantity & Rate Analysis**: Steel rebar, cement, formwork ratios, and CPWD rate benchmarks.

Please enter your specific site query or select one of the quick inquiry templates!"""
}
