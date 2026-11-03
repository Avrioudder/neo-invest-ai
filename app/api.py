"""
FastAPI application for NeoInvest AI.
Provides REST endpoints for funnel diagnostics, nudge generation, and automated recovery dispatch.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, Any, List

from app.models import (
    NudgeRecommendation,
    NudgeDispatchRequest,
    FunnelDropOffEvent,
)
from app.mock_data import FUNNEL_SUMMARY, MOCK_DROP_OFFS
from app.engine import engine, get_all_mock_interventions

api_app = FastAPI(
    title="NeoInvest AI - Mutual Fund Journey Growth Engine",
    description="Drop-Off Recovery, Mandate Optimization & SEBI-Compliant Personalization Engine for NEO App",
    version="1.0.0"
)

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DISPATCH_LOGS: List[Dict[str, Any]] = []


@api_app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "NeoInvest AI Journey Copilot",
        "timestamp": datetime.utcnow().isoformat(),
        "compliance_standard": "SEBI Cir/IMD/DF2/99/2020 Compliant"
    }


@api_app.get("/api/funnel/metrics")
def get_funnel_metrics():
    return FUNNEL_SUMMARY


@api_app.get("/api/drop-offs")
def list_drop_offs():
    return get_all_mock_interventions()


@api_app.get("/api/drop-offs/{user_id}")
def get_user_drop_off(user_id: str):
    for item in MOCK_DROP_OFFS:
        if item["user_id"] == user_id:
            nudge = engine.run_ai_nudge(item)
            return {"drop_off": item, "nudge": nudge}
    raise HTTPException(status_code=404, detail=f"User drop-off event {user_id} not found")


@api_app.post("/api/diagnose-and-nudge", response_model=NudgeRecommendation)
def generate_nudge(drop_off_payload: Dict[str, Any]):
    return engine.run_ai_nudge(drop_off_payload)


@api_app.post("/api/dispatch-nudge")
def dispatch_nudge(request: NudgeDispatchRequest):
    record = {
        "intervention_id": request.intervention_id,
        "user_id": request.user_id,
        "channel": request.channel.value,
        "custom_note": request.custom_note,
        "experiment_tag": request.experiment_tag,
        "dispatched_at": datetime.utcnow().isoformat(),
        "status": "DELIVERED"
    }
    DISPATCH_LOGS.append(record)
    return {"status": "success", "dispatch_record": record}


@api_app.get("/api/dispatch-history")
def get_dispatch_history():
    return {"history": DISPATCH_LOGS}
