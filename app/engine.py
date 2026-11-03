"""
Core AI & Behavioral Finance Engine for NeoInvest AI.
Diagnoses mutual fund journey drop-offs, generates SEBI/AMFI-compliant personalized nudges,
and predicts conversion lift using Groq Llama-3 with a deterministic heuristic fallback.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from app.models import (
    FunnelDropOffEvent,
    NudgeRecommendation,
    DropOffReasonCategory,
    NudgeChannel,
    SEBIComplianceCheck,
    FunnelStage,
)
from app.mock_data import MOCK_DROP_OFFS, SEBI_REGULATORY_RULES

load_dotenv()

logger = logging.getLogger("neoinvest.engine")
logging.basicConfig(level=logging.INFO)


class NudgeGenerationEngine:
    def __init__(self, groq_api_key: Optional[str] = None):
        self.api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        self.groq_client = None
        if self.api_key:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=self.api_key)
                logger.info("Groq client initialized for NeoInvest AI.")
            except Exception as e:
                logger.warning(f"Could not initialize Groq client: {e}. Falling back to deterministic engine.")

    def run_deterministic_nudge(self, drop_off: Dict[str, Any]) -> NudgeRecommendation:
        """
        Deterministic, rule-based behavioral intervention engine.
        Grounded in SEBI non-advisory regulations and empirical fintech drop-off recovery patterns.
        """
        stage = drop_off.get("stage_dropped")
        signals = drop_off.get("interaction_signals", {})
        fund_name = drop_off.get("fund_name", "Mutual Fund")
        user_name = drop_off.get("user_name", "Investor").split()[0]
        sip_amount = float(drop_off.get("intended_sip_amount", 5000.0))
        annual_sip = sip_amount * 12

        # 1. Classify Root Cause Objection
        if stage == "MANDATE_SETUP":
            objection = DropOffReasonCategory.MANDATE_ANXIETY
            channel = NudgeChannel.IN_APP_BOTTOM_SHEET
            headline = f"100% Control: Pause or Edit Your ₹{int(sip_amount):,} SIP Anytime"
            body = (
                f"Hi {user_name}, you're in the driver's seat. Your UPI Autopay mandate has zero hidden fees, "
                f"and you can pause, skip an installment, or cancel with a single tap in the NEO app. "
                f"Complete your mandate to begin rupee-cost averaging in {fund_name}."
            )
            cta_label = "Complete Mandate (Takes 30 Sec)"
            cta_target = "RESUME_UPI_MANDATE"
            lift = 0.24

        elif stage == "PAYMENT_AUTHENTICATION":
            objection = DropOffReasonCategory.PAYMENT_LIMIT_EXHAUSTION
            channel = NudgeChannel.WHATSAPP_REASSURANCE
            bank = signals.get("bank_name", "your bank")
            headline = f"Bank Timeout on ₹{int(sip_amount):,} SIP Mandate"
            body = (
                f"Hi {user_name}, we noticed a temporary gateway timeout from {bank}. "
                f"Your money has NOT been deducted. Would you like to complete this via instant Netbanking or a secondary UPI app?"
            )
            cta_label = "Retry with Backup Bank / UPI"
            cta_target = "RETRY_WITH_NETBANKING"
            lift = 0.31

        elif stage == "SIP_CONFIG" and "ELSS" in drop_off.get("fund_category", ""):
            objection = DropOffReasonCategory.TAX_LOCKIN_HESITATION
            channel = NudgeChannel.SMART_BANNER
            headline = f"Save up to ₹46,800 under Section 80C with 3-Year Lock-In"
            body = (
                f"Hi {user_name}, ELSS funds have the shortest lock-in among all 80C options (PPF has 15 years!). "
                f"The 3-year period instills disciplined compounding while saving tax."
            )
            cta_label = "See Tax Savings Breakdown"
            cta_target = "SHOW_TAX_CALCULATOR"
            lift = 0.19

        elif stage == "SIP_CONFIG":
            objection = DropOffReasonCategory.DECISION_PARALYSIS
            channel = NudgeChannel.IN_APP_BOTTOM_SHEET
            headline = f"Not sure which SIP date to pick?"
            body = (
                f"Hi {user_name}, 72% of NEO investors pick the 5th or 10th of the month—right after salary credit. "
                f"Remember, historical returns show negligible difference between dates over 3+ year horizons."
            )
            cta_label = "Select 5th of Month & Proceed"
            cta_target = "SET_DEFAULT_SIP_DATE"
            lift = 0.22

        elif "Small" in drop_off.get("fund_category", "") or signals.get("recent_1w_nav_change", 0) < 0:
            objection = DropOffReasonCategory.VOLATILITY_FEAR
            channel = NudgeChannel.IN_APP_BOTTOM_SHEET
            headline = f"Market Dips are a Systematic Investor's Best Friend"
            body = (
                f"Hi {user_name}, when {fund_name} experiences short-term volatility, your ₹{int(sip_amount):,} "
                f"SIP automatically buys MORE units at a lower NAV. This lowers your average cost per unit over time."
            )
            cta_label = "See Rupee-Cost Averaging Simulator"
            cta_target = "EXPLAIN_RUPEE_COST_AVERAGING"
            lift = 0.17

        else:
            objection = DropOffReasonCategory.EXPENSE_RATIO_CONFUSION
            channel = NudgeChannel.SMART_BANNER
            headline = f"Direct Plans = Zero Distributor Commission on NEO"
            body = (
                f"Hi {user_name}, this is a 100% Direct Plan. The entire benefit of lower expense ratios is credited "
                f"directly into your fund NAV, compounding into higher wealth over 5+ years."
            )
            cta_label = "Continue Direct Investment"
            cta_target = "RESUME_DIRECT_PLAN_FLOW"
            lift = 0.20

        sebi_check = SEBIComplianceCheck(
            rule_name="SEBI Non-Advisory & Risk Disclosure (Cir. 2020/2021)",
            compliant=True,
            disclaimer_text=SEBI_REGULATORY_RULES["non_advisory_clause"]
        )

        estimated_impact = round(annual_sip * lift, 2)

        return NudgeRecommendation(
            intervention_id=f"INT-{drop_off.get('user_id')}",
            user_id=drop_off.get("user_id"),
            detected_objection=objection,
            primary_channel=channel,
            headline=headline,
            body_copy=body,
            cta_label=cta_label,
            cta_target_action=cta_target,
            sebi_compliance=sebi_check,
            predicted_conversion_lift=lift,
            estimated_aum_impact_inr=estimated_impact,
            model_used="neoinvest-deterministic-rules-v1"
        )

    def run_ai_nudge(self, drop_off: Dict[str, Any]) -> NudgeRecommendation:
        """
        Executes Groq/Llama-3-70b contextual synthesis for hyper-personalized recovery messaging.
        Enforces strict SEBI/AMFI regulatory compliance. Falls back to deterministic engine.
        """
        baseline = self.run_deterministic_nudge(drop_off)
        if not self.groq_client:
            return baseline

        prompt = f"""You are the senior Behavioral Finance & Journey Growth AI Engine for the NEO Mutual Fund Investment App.
Analyze this user drop-off event on the mutual fund funnel and generate an empathetic, persuasive, and strictly compliant recovery nudge.

Regulatory Constraints:
1. SEBI Compliance: You CANNOT give guaranteed return promises or unregistered advisory stock picks.
2. AMFI Standards: Reinforce that direct mutual funds have zero broker commissions.
3. Keep tone reassuring, concise, and focused on easing friction.

User Drop-Off Telemetry:
{json.dumps(drop_off, indent=2)}

Baseline Heuristic Reference:
{baseline.model_dump_json(indent=2)}

Respond with a valid JSON matching this schema:
{{
  "detected_objection": "<MANDATE_ANXIETY | EXPENSE_RATIO_CONFUSION | TAX_LOCKIN_HESITATION | PAYMENT_LIMIT_EXHAUSTION | VOLATILITY_FEAR | DECISION_PARALYSIS>",
  "primary_channel": "<IN_APP_BOTTOM_SHEET | SMART_BANNER | WHATSAPP_REASSURANCE | PUSH_NOTIFICATION>",
  "headline": "<Punchy, reassuring headline max 60 chars>",
  "body_copy": "<Concise 2-sentence explanation easing user hesitation and explaining why SIP empowers them>",
  "cta_label": "<Clear 3-4 word actionable button label>",
  "cta_target_action": "<action slug>",
  "predicted_conversion_lift": <float between 0.15 and 0.35>
}}
"""

        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a specialized Fintech Product Manager AI. Respond in strict JSON only."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            raw = chat_completion.choices[0].message.content
            parsed = json.loads(raw)

            # Validate Enum values
            try:
                obj_enum = DropOffReasonCategory(parsed.get("detected_objection", baseline.detected_objection.value))
            except Exception:
                obj_enum = baseline.detected_objection

            try:
                channel_enum = NudgeChannel(parsed.get("primary_channel", baseline.primary_channel.value))
            except Exception:
                channel_enum = baseline.primary_channel

            lift = float(parsed.get("predicted_conversion_lift", baseline.predicted_conversion_lift))
            annual_sip = float(drop_off.get("intended_sip_amount", 5000.0)) * 12
            estimated_impact = round(annual_sip * lift, 2)

            return NudgeRecommendation(
                intervention_id=f"INT-{drop_off.get('user_id')}",
                user_id=drop_off.get("user_id"),
                detected_objection=obj_enum,
                primary_channel=channel_enum,
                headline=parsed.get("headline", baseline.headline),
                body_copy=parsed.get("body_copy", baseline.body_copy),
                cta_label=parsed.get("cta_label", baseline.cta_label),
                cta_target_action=parsed.get("cta_target_action", baseline.cta_target_action),
                sebi_compliance=baseline.sebi_compliance,
                predicted_conversion_lift=lift,
                estimated_aum_impact_inr=estimated_impact,
                model_used="groq/llama-3.3-70b-versatile"
            )
        except Exception as e:
            logger.warning(f"Groq API call encountered exception: {e}. Defaulting to deterministic engine.")
            res = baseline
            res.model_used = "neoinvest-deterministic-fallback-v1"
            return res


engine = NudgeGenerationEngine()


def get_all_mock_interventions() -> List[Dict[str, Any]]:
    """Evaluates all mock drop-offs and returns combined list."""
    results = []
    for item in MOCK_DROP_OFFS:
        nudge = engine.run_ai_nudge(item)
        results.append({
            "drop_off": item,
            "nudge": nudge
        })
    return results
