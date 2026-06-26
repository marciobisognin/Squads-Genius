#!/usr/bin/env python3
"""GlobalState do DÉDALO — estado único compartilhado do StateGraph.

Validado por Pydantic quando disponível; degrada para dataclasses (stdlib) sem perder
a forma. Cada agente lê o estado e escreve apenas em sua fatia.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

try:  # Pydantic é preferido; fallback determinístico para ambientes sem dependências.
    from pydantic import BaseModel, Field

    _HAS_PYDANTIC = True
except Exception:  # pragma: no cover
    from dataclasses import dataclass, field

    _HAS_PYDANTIC = False


if _HAS_PYDANTIC:

    class Provenance(BaseModel):
        agent: str
        source_refs: list[str] = []
        evidence_type: str = "evidencia"  # evidencia | hipotese | estimativa
        timestamp: Optional[datetime] = None
        confidence: float = Field(default=0.0, ge=0.0, le=1.0)

    class IntakeSpec(BaseModel):
        primary_source: str
        objective: str
        niche_sector: Optional[str] = None
        end_user: Optional[str] = None
        output_mode: str = "prd_only"  # prd_only | prd_plus_mvp
        explicit_assumptions: list[str] = []

    class GlobalState(BaseModel):
        run_id: str
        seed: int = 42
        intake: IntakeSpec
        cynefin_domain: Optional[str] = None  # obvio | complicado | complexo | caotico
        sources: Optional[dict[str, Any]] = None
        opportunities: Optional[dict[str, Any]] = None
        scored_opportunities: Optional[dict[str, Any]] = None
        process_model: Optional[dict[str, Any]] = None
        knowledge_model: Optional[dict[str, Any]] = None
        data_map: Optional[dict[str, Any]] = None
        prd: Optional[dict[str, Any]] = None
        architecture: Optional[dict[str, Any]] = None
        redteam: Optional[dict[str, Any]] = None
        validation: Optional[dict[str, Any]] = None
        prototype: Optional[dict[str, Any]] = None
        delivery: Optional[dict[str, Any]] = None
        hitl_gates: dict[str, str] = {}  # gate -> pending | approved | rejected
        healing_log: list[str] = []
        langfuse_trace_id: Optional[str] = None

else:  # pragma: no cover

    @dataclass
    class Provenance:
        agent: str
        source_refs: list = field(default_factory=list)
        evidence_type: str = "evidencia"
        timestamp: Optional[datetime] = None
        confidence: float = 0.0

    @dataclass
    class IntakeSpec:
        primary_source: str
        objective: str
        niche_sector: Optional[str] = None
        end_user: Optional[str] = None
        output_mode: str = "prd_only"
        explicit_assumptions: list = field(default_factory=list)

    @dataclass
    class GlobalState:
        run_id: str
        intake: IntakeSpec
        seed: int = 42
        cynefin_domain: Optional[str] = None
        sources: Optional[dict] = None
        opportunities: Optional[dict] = None
        scored_opportunities: Optional[dict] = None
        process_model: Optional[dict] = None
        knowledge_model: Optional[dict] = None
        data_map: Optional[dict] = None
        prd: Optional[dict] = None
        architecture: Optional[dict] = None
        redteam: Optional[dict] = None
        validation: Optional[dict] = None
        prototype: Optional[dict] = None
        delivery: Optional[dict] = None
        hitl_gates: dict = field(default_factory=dict)
        healing_log: list = field(default_factory=list)
        langfuse_trace_id: Optional[str] = None


HITL_GATES = ("intake", "scope_approval", "final_homologation")
CYNEFIN_DOMAINS = ("obvio", "complicado", "complexo", "caotico")


if __name__ == "__main__":
    state = GlobalState(run_id="forge-demo", intake=IntakeSpec(primary_source="exemplo.mp4", objective="demo"))
    print("Pydantic ativo:", _HAS_PYDANTIC, "| run:", state.run_id, "| seed:", state.seed)
