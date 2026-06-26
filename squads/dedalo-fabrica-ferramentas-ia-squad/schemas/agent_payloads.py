#!/usr/bin/env python3
"""Payloads tipados por agente do DÉDALO (contratos SACP de domínio).

Cada agente escreve uma fatia do GlobalState com um payload aqui declarado. Pydantic
quando disponível; fallback dataclasses. As notas de scoring são SEMPRE premissas:
o ranking final é Python (engine/scoring.py).
"""
from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel, Field

    _HAS_PYDANTIC = True
except Exception:  # pragma: no cover
    from dataclasses import dataclass, field

    _HAS_PYDANTIC = False


if _HAS_PYDANTIC:

    class Evidence(BaseModel):
        text: str
        source_ref: str
        timestamp: Optional[str] = None
        confidence: float = Field(default=0.0, ge=0.0, le=1.0)

    class SourcePackage(BaseModel):
        transcripts: list[dict[str, Any]] = []
        key_quotes: list[Evidence] = []
        cited_tools: list[str] = []
        inaccessible_sources: list[str] = []

    class OppScoringAssumptions(BaseModel):
        impact_value_1to5: int = Field(ge=1, le=5)
        effort_1to5: int = Field(ge=1, le=5)
        risk_1to5: int = Field(ge=1, le=5)
        data_availability_1to5: int = Field(ge=1, le=5)
        repetition_1to5: int = Field(ge=1, le=5)

    class Opportunity(BaseModel):
        name: str
        niche: str
        pain: str
        user: str
        archetype: str
        data_needed: list[str] = []
        automations: list[str] = []
        agents: list[str] = []
        integrations: list[str] = []
        mvp_sketch: str = ""
        scoring_assumptions: OppScoringAssumptions
        maps_to_evidence: list[str] = []

    class OpportunityMap(BaseModel):
        opportunities: list[Opportunity] = []

    class RedTeamReport(BaseModel):
        verdict: str = "aprovado_com_ressalvas"  # aprovado | aprovado_com_ressalvas | bloqueado
        attacks: list[dict[str, Any]] = []
        hallucinated_requirements: list[str] = []
        weakest_assumption: str = ""
        kill_shot: Optional[str] = None
        required_fixes: list[str] = []

    class ValidationReport(BaseModel):
        quality_checks: list[str] = []
        security_flags: list[str] = []
        lgpd: dict[str, str] = {}
        human_in_loop_required: bool = False
        regulated_sector_notes: str = ""
        blocking: bool = False
        disclaimer: str = ""

else:  # pragma: no cover

    @dataclass
    class Evidence:
        text: str
        source_ref: str
        timestamp: Optional[str] = None
        confidence: float = 0.0

    @dataclass
    class SourcePackage:
        transcripts: list = field(default_factory=list)
        key_quotes: list = field(default_factory=list)
        cited_tools: list = field(default_factory=list)
        inaccessible_sources: list = field(default_factory=list)

    @dataclass
    class OppScoringAssumptions:
        impact_value_1to5: int
        effort_1to5: int
        risk_1to5: int
        data_availability_1to5: int
        repetition_1to5: int

    @dataclass
    class Opportunity:
        name: str
        niche: str
        pain: str
        user: str
        archetype: str
        scoring_assumptions: OppScoringAssumptions
        data_needed: list = field(default_factory=list)
        automations: list = field(default_factory=list)
        agents: list = field(default_factory=list)
        integrations: list = field(default_factory=list)
        mvp_sketch: str = ""
        maps_to_evidence: list = field(default_factory=list)

    @dataclass
    class OpportunityMap:
        opportunities: list = field(default_factory=list)

    @dataclass
    class RedTeamReport:
        verdict: str = "aprovado_com_ressalvas"
        attacks: list = field(default_factory=list)
        hallucinated_requirements: list = field(default_factory=list)
        weakest_assumption: str = ""
        kill_shot: Optional[str] = None
        required_fixes: list = field(default_factory=list)

    @dataclass
    class ValidationReport:
        quality_checks: list = field(default_factory=list)
        security_flags: list = field(default_factory=list)
        lgpd: dict = field(default_factory=dict)
        human_in_loop_required: bool = False
        regulated_sector_notes: str = ""
        blocking: bool = False
        disclaimer: str = ""


VALID_ARCHETYPES = (
    "market_intel", "content_analyzer", "knowledge_base", "crm_churn",
    "legal_rag", "clinic_triage", "construction_control", "distributor_sales", "micro_saas",
)


if __name__ == "__main__":
    print("Pydantic ativo:", _HAS_PYDANTIC, "| arquétipos:", len(VALID_ARCHETYPES))
