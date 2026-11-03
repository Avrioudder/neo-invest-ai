"""
Strongly-typed Pydantic schemas for NeoInvest AI.
Covers funnel events, drop-off classification, SEBI/AMFI regulatory guardrails,
and automated contextual recovery nudges.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class FunnelStage(str, Enum):
    FUND_DISCOVERY = "FUND_DISCOVERY"
    FUND_DETAILS_VIEW = "FUND_DETAILS_VIEW"
    SIP_CONFIG = "SIP_CONFIG"
    MANDATE_SETUP = "MANDATE_SETUP"
    PAYMENT_AUTHENTICATION = "PAYMENT_AUTHENTICATION"
    ORDER_SUCCESS = "ORDER_SUCCESS"


class DropOffReasonCategory(str, Enum):
    MANDATE_ANXIETY = "MANDATE_ANXIETY"
    EXPENSE_RATIO_CONFUSION = "EXPENSE_RATIO_CONFUSION"
    TAX_LOCKIN_HESITATION = "TAX_LOCKIN_HESITATION"
    PAYMENT_LIMIT_EXHAUSTION = "PAYMENT_LIMIT_EXHAUSTION"
    VOLATILITY_FEAR = "VOLATILITY_FEAR"
    DECISION_PARALYSIS = "DECISION_PARALYSIS"


class UserRiskProfile(str, Enum):
    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE"
    GROWTH_AGGRESSIVE = "GROWTH_AGGRESSIVE"


class NudgeChannel(str, Enum):
    IN_APP_BOTTOM_SHEET = "IN_APP_BOTTOM_SHEET"
    SMART_BANNER = "SMART_BANNER"
    WHATSAPP_REASSURANCE = "WHATSAPP_REASSURANCE"
    PUSH_NOTIFICATION = "PUSH_NOTIFICATION"


class SEBIComplianceCheck(BaseModel):
    rule_name: str = Field(..., description="SEBI / AMFI regulatory standard reference")
    compliant: bool = Field(..., description="Whether message conforms to non-advisory and risk rules")
    disclaimer_text: str = Field(..., description="Mandatory statutory disclosure")


class FunnelDropOffEvent(BaseModel):
    user_id: str
    user_name: str
    risk_profile: UserRiskProfile
    fund_id: str
    fund_name: str
    fund_category: str
    intended_sip_amount: float
    stage_dropped: FunnelStage
    dwell_time_seconds: int
    interaction_signals: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str


class NudgeRecommendation(BaseModel):
    intervention_id: str
    user_id: str
    detected_objection: DropOffReasonCategory
    primary_channel: NudgeChannel
    headline: str
    body_copy: str
    cta_label: str
    cta_target_action: str
    sebi_compliance: SEBIComplianceCheck
    predicted_conversion_lift: float = Field(..., ge=0.0, le=1.0, description="Predicted recovery probability")
    estimated_aum_impact_inr: float = Field(..., description="Projected annualized AUM protected (₹)")
    model_used: str = "neoinvest-ai-engine-v1"


class FunnelConversionMetrics(BaseModel):
    total_visitors: int
    fund_viewers: int
    sip_configured: int
    mandate_initiated: int
    orders_completed: int
    overall_conversion_rate: float
    estimated_monthly_aum_loss_inr: float


class NudgeDispatchRequest(BaseModel):
    intervention_id: str
    user_id: str
    channel: NudgeChannel
    custom_note: Optional[str] = None
    experiment_tag: str = "exp_sip_recovery_v1"
