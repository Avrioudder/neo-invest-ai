"""
Realistic enterprise telemetry and mock datasets for the NEO Mutual Fund Investment App.
Mirrors real-world drop-offs, payment mandate obstacles, SEBI risk disclosures,
and cohort conversion metrics.
"""

from typing import Dict, Any, List

FUNNEL_SUMMARY: Dict[str, Any] = {
    "total_visitors": 142500,
    "fund_viewers": 68400,
    "sip_configured": 28700,
    "mandate_initiated": 13200,
    "orders_completed": 8450,
    "overall_conversion_rate": 0.0593,
    "estimated_monthly_aum_loss_inr": 342000000.0,
    "avoidable_support_contacts_pct": 34.8,
    "csat_funnel_rating": 3.8
}

MOCK_DROP_OFFS: List[Dict[str, Any]] = [
    {
        "user_id": "USR-9021",
        "user_name": "Rohan Verma",
        "city": "Bengaluru",
        "risk_profile": "MODERATE",
        "fund_id": "PP-FLEXI-DIR",
        "fund_name": "Parag Parikh Flexi Cap Direct-Growth",
        "fund_category": "Flexi Cap Fund",
        "intended_sip_amount": 5000.0,
        "stage_dropped": "MANDATE_SETUP",
        "dwell_time_seconds": 185,
        "interaction_signals": {
            "screen_visited": "UPI Autopay Mandate",
            "back_button_pressed": 2,
            "clicked_faq": "Can I cancel my SIP anytime?",
            "bank_name": "HDFC Bank",
            "hesitation_trigger": "Autopay Max Limit ₹15,000 text displayed"
        },
        "timestamp": "2026-11-03 14:22:10"
    },
    {
        "user_id": "USR-9022",
        "user_name": "Ananya Iyer",
        "city": "Mumbai",
        "risk_profile": "CONSERVATIVE",
        "fund_id": "MIRAE-ELSS-DIR",
        "fund_name": "Mirae Asset ELSS Tax Saver Direct-Growth",
        "fund_category": "ELSS Tax Saver",
        "intended_sip_amount": 10000.0,
        "stage_dropped": "SIP_CONFIG",
        "dwell_time_seconds": 240,
        "interaction_signals": {
            "screen_visited": "SIP Installment & Tax Benefit",
            "toggled_fund_type": ["ELSS", "Large Cap"],
            "hovered_term": "3-Year Mandatory Lock-In",
            "hesitation_trigger": "Fear of funds locked without liquidity during emergency"
        },
        "timestamp": "2026-11-03 15:05:40"
    },
    {
        "user_id": "USR-9023",
        "user_name": "Vikramaditya Roy",
        "city": "Gurugram",
        "risk_profile": "GROWTH_AGGRESSIVE",
        "fund_id": "NIPPON-SMALL-DIR",
        "fund_name": "Nippon India Small Cap Direct-Growth",
        "fund_category": "Small Cap Fund",
        "intended_sip_amount": 7500.0,
        "stage_dropped": "FUND_DETAILS_VIEW",
        "dwell_time_seconds": 310,
        "interaction_signals": {
            "screen_visited": "Fund Performance & Riskometer",
            "viewed_riskometer": "Very High Risk badge",
            "recent_1w_nav_change": -2.4,
            "hesitation_trigger": "Short-term market dip causing loss aversion"
        },
        "timestamp": "2026-11-03 15:45:12"
    },
    {
        "user_id": "USR-9024",
        "user_name": "Pooja Hegde",
        "city": "Pune",
        "risk_profile": "CONSERVATIVE",
        "fund_id": "UTI-NIFTY50-DIR",
        "fund_name": "UTI Nifty 50 Index Fund Direct-Growth",
        "fund_category": "Index Fund / Large Cap",
        "intended_sip_amount": 3000.0,
        "stage_dropped": "PAYMENT_AUTHENTICATION",
        "dwell_time_seconds": 95,
        "interaction_signals": {
            "screen_visited": "NPCI Bank Mandate Gateway",
            "error_code": "NPCI_U19_LIMIT_EXCEEDED",
            "bank_name": "State Bank of India",
            "hesitation_trigger": "Bank server timeout during UPI Autopay mandate pin entry"
        },
        "timestamp": "2026-11-03 16:10:05"
    },
    {
        "user_id": "USR-9025",
        "user_name": "Aditya Sengupta",
        "city": "Kolkata",
        "risk_profile": "MODERATE",
        "fund_id": "HDFC-MIDCAP-DIR",
        "fund_name": "HDFC Mid-Cap Opportunities Direct-Growth",
        "fund_category": "Mid Cap Fund",
        "intended_sip_amount": 4000.0,
        "stage_dropped": "FUND_DETAILS_VIEW",
        "dwell_time_seconds": 160,
        "interaction_signals": {
            "screen_visited": "Expense Ratio & Fund House Info",
            "searched_help": "Direct Plan vs Regular Plan commission",
            "hesitation_trigger": "Unsure if 0.78% TER is deducted every month or annually"
        },
        "timestamp": "2026-11-03 16:30:20"
    },
    {
        "user_id": "USR-9026",
        "user_name": "Kavita Nair",
        "city": "Chennai",
        "risk_profile": "CONSERVATIVE",
        "fund_id": "ICICI-BLUECHIP-DIR",
        "fund_name": "ICICI Prudential Bluechip Direct-Growth",
        "fund_category": "Large Cap Fund",
        "intended_sip_amount": 2500.0,
        "stage_dropped": "SIP_CONFIG",
        "dwell_time_seconds": 210,
        "interaction_signals": {
            "screen_visited": "SIP Date Selection",
            "toggled_dates": [1, 5, 10, 15],
            "hesitation_trigger": "Unsure which date aligns with salary cycle to avoid bounce charge"
        },
        "timestamp": "2026-11-03 17:15:33"
    }
]

SEBI_REGULATORY_RULES = {
    "non_advisory_clause": "Mutual fund investments are subject to market risks, read all scheme related documents carefully. Past performance is not indicative of future returns.",
    "amfi_code": "AMFI Reg No. 184920. Digital platform facilitates direct execution without charging distributor commissions.",
    "riskometer_guideline": "SEBI Cir/IMD/DF2/99/2020: Product labeling with 6-level riskometer mandatory on all investment journeys."
}
