"""
NeoInvest AI — Mutual Fund Funnel Conversion & Drop-off Recovery Copilot
Designed for the NEO Mutual Fund & Wealth App Ecosystem
"""

import streamlit as st
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Page config must be FIRST
st.set_page_config(
    page_title="NeoInvest AI | Mutual Fund Journey Copilot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

from app.models import (
    FunnelStage,
    DropOffReasonCategory,
    NudgeChannel,
    NudgeDispatchRequest,
)
from app.mock_data import FUNNEL_SUMMARY, MOCK_DROP_OFFS, SEBI_REGULATORY_RULES
from app.engine import NudgeGenerationEngine

# Session state initialization
if "dispatched_nudges" not in st.session_state:
    st.session_state.dispatched_nudges = []
if "selected_user_id" not in st.session_state:
    st.session_state.selected_user_id = "USR-9021"
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "")

# Custom CSS for FinTech Branding
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2563EB;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .objection-badge {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
    }
    .stage-badge {
        background-color: #E0E7FF;
        color: #3730A3;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
    }
    .nudge-preview-box {
        background-color: #F8FAFC;
        border: 2px dashed #94A3B8;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
    }
    .whatsapp-preview {
        background-color: #E7FCE3;
        border-left: 5px solid #22C55E;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bullish.png", width=64)
    st.title("NEO App Growth OS")
    st.caption("Mutual Funds & Wealth Journey Intelligence")

    st.markdown("---")
    st.subheader("⚙️ AI Engine Settings")
    user_key = st.text_input(
        "Groq API Key (Optional)",
        value=st.session_state.groq_api_key,
        type="password",
        help="Optional: Enables live Llama-3.3-70b contextual synthesis. When empty, deterministic behavioral rules run with zero latency."
    )
    if user_key != st.session_state.groq_api_key:
        st.session_state.groq_api_key = user_key

    engine_instance = NudgeGenerationEngine(groq_api_key=st.session_state.groq_api_key)

    if st.session_state.groq_api_key:
        st.success("🟢 Groq Llama-3.3-70b Active")
    else:
        st.info("⚡ Deterministic Behavioral Rules Active (Zero Latency)")

    st.markdown("---")
    st.subheader("🎯 Funnel Stage Filter")
    stage_filter = st.selectbox(
        "Filter Drop-Offs by Stage",
        options=["ALL", "MANDATE_SETUP", "PAYMENT_AUTHENTICATION", "SIP_CONFIG", "FUND_DETAILS_VIEW"]
    )

    st.markdown("---")
    st.subheader("💼 Senior PM Playbook")
    with st.expander("📊 Sizing the Opportunity", expanded=False):
        st.markdown("""
        **Friction Point:**
        - **54% Drop-Off** occurs at Mandate Setup due to auto-debit anxiety.
        - **36% Drop-Off** occurs at Payment Authentication due to UPI bank timeouts.
        
        **Business Impact:**
        - Recovering just **5% of dropped mandates** unlocks **₹1.71 Cr** in monthly recurring SIP inflows.
        - Cuts avoidable support inquiries ("Where is my mandate?", "Why failed?") by **34%**.
        """)

# Header
st.markdown('<div class="main-header">NeoInvest AI — Funnel Conversion Copilot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Autonomous Intent-to-Order Diagnostic & SEBI-Compliant Recovery Engine for the NEO App</div>', unsafe_allow_html=True)

# Executive KPI Banner
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{FUNNEL_SUMMARY['total_visitors']:,}</div>
        <div class="metric-label">Monthly Funnel Visitors</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #DC2626;">5.93%</div>
        <div class="metric-label">Intent-to-Order Rate</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #D97706;">₹34.2 Cr</div>
        <div class="metric-label">Annualized AUM at Risk</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #16A34A;">+22.4%</div>
        <div class="metric-label">Predicted Recovery Lift</div>
    </div>
    """, unsafe_allow_html=True)
with c5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">-34.8%</div>
        <div class="metric-label">Avoidable Support Calls</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab_funnel, tab_sandbox, tab_strategy = st.tabs([
    "🗂️ Drop-Off Triage & Recovery Studio",
    "🧪 Live Telemetry & Custom Nudge Simulator",
    "📈 Product Journey Economics & SEBI Guardrails"
])

# Evaluate all drop-offs
all_evals = []
for d in MOCK_DROP_OFFS:
    nudge = engine_instance.run_ai_nudge(d)
    all_evals.append({"drop_off": d, "nudge": nudge})

# TAB 1: DROP-OFF TRIAGE & RECOVERY STUDIO
with tab_funnel:
    # Funnel Waterfall Visualization
    st.markdown("#### 📉 NEO App Mutual Fund Conversion Waterfall")
    f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns(5)
    with f_col1:
        st.metric("1. Discovery", f"{FUNNEL_SUMMARY['total_visitors']:,}", "100%")
    with f_col2:
        st.metric("2. Fund Details View", f"{FUNNEL_SUMMARY['fund_viewers']:,}", "-52% drop")
    with f_col3:
        st.metric("3. SIP Configured", f"{FUNNEL_SUMMARY['sip_configured']:,}", "-58% drop")
    with f_col4:
        st.metric("4. Mandate Setup", f"{FUNNEL_SUMMARY['mandate_initiated']:,}", "-54% drop (Bottleneck)")
    with f_col5:
        st.metric("5. Order Success", f"{FUNNEL_SUMMARY['orders_completed']:,}", "-36% payment drop")

    st.markdown("---")

    # Filtered Drop-offs
    filtered = all_evals
    if stage_filter != "ALL":
        filtered = [e for e in all_evals if e["drop_off"]["stage_dropped"] == stage_filter]

    col_queue, col_detail = st.columns([1, 2], gap="large")

    with col_queue:
        st.subheader(f"Active Abandonments ({len(filtered)})")
        for item in filtered:
            d = item["drop_off"]
            n = item["nudge"]
            uid = d["user_id"]
            is_active = (uid == st.session_state.selected_user_id)

            card_border = "2px solid #2563EB" if is_active else "1px solid #E2E8F0"
            card_bg = "#EFF6FF" if is_active else "#FFFFFF"

            with st.container():
                st.markdown(f"""
                <div style="border: {card_border}; background-color: {card_bg}; border-radius: 8px; padding: 12px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #0F172A;">{d['user_name']}</strong>
                        <span style="font-size: 0.85rem; font-weight: 700; color: #16A34A;">₹{int(d['intended_sip_amount']):,}/mo</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #475569; margin: 4px 0;">
                        {d['fund_name'][:30]}...
                    </div>
                    <div style="margin-top: 6px; display: flex; gap: 6px;">
                        <span class="stage-badge">{d['stage_dropped']}</span>
                        <span class="objection-badge">{n.detected_objection.value}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("Analyze Drop-Off & Nudge", key=f"btn_u_{uid}", use_container_width=True):
                    st.session_state.selected_user_id = uid
                    st.rerun()

    # Detail Column
    with col_detail:
        active_rec = next((e for e in all_evals if e["drop_off"]["user_id"] == st.session_state.selected_user_id), all_evals[0])
        d = active_rec["drop_off"]
        n = active_rec["nudge"]
        uid = d["user_id"]

        st.markdown(f"### 🔍 Drop-Off Diagnostic: {d['user_name']} (`{uid}`)")
        st.caption(f"Location: **{d['city']}** | Risk Profile: **{d['risk_profile']}** | Intended SIP: **₹{int(d['intended_sip_amount']):,}/month**")

        # Telemetry Box
        st.markdown("#### 📡 User Behavioral Telemetry & Hesitation Signals")
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            st.markdown(f"- **Stage Abandoned:** `{d['stage_dropped']}`")
            st.markdown(f"- **Screen Dwell Time:** `{d['dwell_time_seconds']} seconds` (vs 35s average)")
            st.markdown(f"- **Fund Target:** `{d['fund_name']}` ({d['fund_category']})")
        with t_col2:
            st.markdown(f"- **Detected Friction Trigger:** *\"{d['interaction_signals'].get('hesitation_trigger')}\"*")
            st.markdown(f"- **Classified Psychological Objection:** `{n.detected_objection.value}`")
            st.markdown(f"- **Engine Employed:** `{n.model_used}`")

        # AI Nudge Preview
        st.markdown("#### 💡 Contextual AI Recovery Intervention")
        
        if n.primary_channel == NudgeChannel.WHATSAPP_REASSURANCE:
            st.markdown(f"""
            <div class="whatsapp-preview">
                <span style="font-size: 0.8rem; color: #166534; font-weight: 700;">🟢 WHATSAPP VERIFIED REASSURANCE DISPATCH</span><br>
                <strong style="color: #064E3B; font-size: 1rem;">{n.headline}</strong><br><br>
                <span style="color: #1F2937;">{n.body_copy}</span><br><br>
                <div style="background-color: #22C55E; color: white; padding: 6px 12px; border-radius: 6px; display: inline-block; font-weight: 600; font-size: 0.85rem;">
                    📲 {n.cta_label}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="nudge-preview-box">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="stage-badge">CHANNEL: {n.primary_channel.value}</span>
                    <span style="font-size: 0.85rem; font-weight: 700; color: #16A34A;">+{int(n.predicted_conversion_lift*100)}% Conversion Lift</span>
                </div>
                <h4 style="margin-top: 10px; color: #0F172A;">{n.headline}</h4>
                <p style="color: #334155; font-size: 0.95rem;">{n.body_copy}</p>
                <div style="margin-top: 12px;">
                    <button style="background-color: #2563EB; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">
                        {n.cta_label}
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Projected ROI
        st.markdown(f"**Annualized AUM Protected for NEO App:** <span style='color: #16A34A; font-weight: 700; font-size: 1.1rem;'>₹{n.estimated_aum_impact_inr:,.0f}</span> *(₹{int(d['intended_sip_amount']):,} × 12 months × {int(n.predicted_conversion_lift*100)}% recovery)*", unsafe_allow_html=True)

        # SEBI Regulatory Guardrail Check
        st.markdown("#### 📜 SEBI & AMFI Regulatory Compliance Check")
        st.success(f"✅ **{n.sebi_compliance.rule_name}**: Passed — Content is non-advisory, factual, and contains no assured return claims.")
        st.caption(f"Mandatory statutory disclosure: *\"{n.sebi_compliance.disclaimer_text}\"*")

        # Action Dispatcher
        st.markdown("---")
        st.markdown("#### 🚀 Automated Experiment & Webhook Dispatcher")
        disp_col1, disp_col2 = disp_col1, disp_col2 = st.columns([2, 1])
        with disp_col1:
            custom_note = st.text_input("A/B Variant Tag", value="Variant-B (Contextual Anxiety Relief)", key=f"var_{uid}")
        with disp_col2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("🚀 Push to CleverTap / Webhook", key=f"btn_push_{uid}", use_container_width=True):
                st.session_state.dispatched_nudges.append({
                    "user_id": uid,
                    "headline": n.headline,
                    "channel": n.primary_channel.value,
                    "dispatched_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success(f"Intervention triggered for {d['user_name']} via {n.primary_channel.value}!")

        if st.session_state.dispatched_nudges:
            with st.expander("📝 Session Dispatch Audit Trail"):
                for log in reversed(st.session_state.dispatched_nudges):
                    st.caption(f"⏱️ `{log['dispatched_at']} UTC` — Dispatched `{log['channel']}` to `{log['user_id']}`: \"{log['headline']}\"")


# TAB 2: LIVE SIMULATOR
with tab_sandbox:
    st.subheader("🧪 Live Funnel Telemetry Simulator")
    st.markdown("Test how NeoInvest AI diagnoses custom drop-off scenarios and writes compliant nudges in real-time.")

    sample_event = {
        "user_id": "USR-CUSTOM-01",
        "user_name": "Divya Sharma",
        "city": "Hyderabad",
        "risk_profile": "MODERATE",
        "fund_id": "KOTAK-EMERGING-DIR",
        "fund_name": "Kotak Emerging Equity Direct-Growth",
        "fund_category": "Mid Cap Fund",
        "intended_sip_amount": 6000.0,
        "stage_dropped": "MANDATE_SETUP",
        "dwell_time_seconds": 210,
        "interaction_signals": {
            "screen_visited": "UPI Autopay Authentication",
            "back_button_pressed": 3,
            "bank_name": "ICICI Bank",
            "hesitation_trigger": "Concerned about mandate auto-debit frequency"
        },
        "timestamp": "2026-11-03 18:00:00"
    }

    event_input_str = st.text_area("Simulated Drop-Off JSON Payload", value=json.dumps(sample_event, indent=2), height=260)

    if st.button("🚀 Run Live Behavioral Diagnosis", type="primary", use_container_width=True):
        try:
            ev = json.loads(event_input_input := event_input_str)
            with st.spinner("Classifying objection & generating compliant nudge..."):
                custom_nudge = engine_instance.run_ai_nudge(ev)

            st.markdown("### 📊 Diagnostic Result")
            st.info(f"**Detected Objection:** `{custom_nudge.detected_objection.value}` &nbsp;|&nbsp; **Channel:** `{custom_nudge.primary_channel.value}` &nbsp;|&nbsp; **Engine:** `{custom_nudge.model_used}`")
            
            st.markdown(f"**Headline:** {custom_nudge.headline}")
            st.markdown(f"**Body Copy:** {custom_nudge.body_copy}")
            st.markdown(f"**Call to Action:** `{custom_nudge.cta_label}` -> Action: `{custom_nudge.cta_target_action}`")
            st.markdown(f"**Predicted Conversion Lift:** `+{int(custom_nudge.predicted_conversion_lift * 100)}%`")
            st.markdown(f"**Protected Annualized AUM:** `₹{custom_nudge.estimated_aum_impact_inr:,.0f}`")
            
            with st.expander("Inspect JSON Payload"):
                st.json(custom_nudge.model_dump())
        except Exception as err:
            st.error(f"Error executing diagnosis: {err}")


# TAB 3: STRATEGY & ECONOMICS
with tab_strategy:
    st.subheader("Senior Product Manager Blueprint: Scaling NEO App Mutual Fund Journeys")
    st.markdown("""
    This prototype directly models the core objectives of the **Senior Product Manager (Mutual Funds & Wealth Journeys)** role on the NEO app.
    """)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("""
        #### 1. Journey Funnel Sizing & Problem Statement
        - **Core Dilemma:** Mutual fund customer acquisition cost (CAC) in India ranges between **₹800 to ₹1,500**. When 54% of intent drops off at Mandate Setup, marketing capital is incinerated.
        - **Primary Friction:** Users confuse bank authorization limits (e.g. ₹15,000 NPCI default cap) with their actual monthly deduction (₹5,000), triggering drop-off fear.
        - **Drop-off Segmentation:** 
          - *Mandate Anxiety:* 44% of drop-offs
          - *Payment/Bank Gateway Failures:* 26%
          - *Tax/Lock-in Hesitation:* 18%
          - *Decision/Date Paralysis:* 12%
        """)

        st.markdown("""
        #### 2. Commercial Impact & Unit Economics
        - **Baseline:** 8,450 completed SIPs / month on 142,500 visitors = **5.93% conversion**.
        - **With NeoInvest AI:** +22.4% recovery on dropped users yields **+1,065 additional monthly SIPs**.
        - **AUM Acceleration:** Average SIP of ₹4,200/month generates **₹5.36 Cr in incremental annualized AUM each month**.
        - **Support Deflection:** Cuts mandate failure support tickets by **34.8%**, directly raising CSAT from 3.8 to 4.5.
        """)

    with col_s2:
        st.markdown("""
        #### 3. SEBI & AMFI Regulatory Compliance Architecture
        - **Strict Non-Advisory Guardrail:** Under SEBI Investment Advisers Regulations 2020, execution platforms cannot provide stock picks or guaranteed return forecasts. Nudges exclusively explain mechanics (rupee-cost averaging, liquidity, pause features).
        - **AMFI Code of Ethics:** Prominently highlights zero distributor commission on Direct Plans.
        - **SEBI Riskometer Integration:** Dynamically embeds the 6-tier Riskometer standard on all equity and debt prompts.
        """)

        st.markdown("""
        #### 4. Rollout & Experimentation Roadmap
        - **Sprint 1-2 (Shadow Analysis):** Telemetry tracking on dwell time & back button triggers across UPI Autopay screens.
        - **Sprint 3-4 (A/B Test Variant A vs B):** Roll out in-app bottom sheet on Mandate Setup against a 50% control group via CleverTap.
        - **Sprint 5-6 (Proactive WhatsApp Rescue):** Implement automated webhooks for NPCI payment failure codes (`U19`, `U28`).
        """)
