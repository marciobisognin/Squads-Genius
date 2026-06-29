#!/usr/bin/env python3
"""SACP — Structured Agent Communication Protocol (envelope de handoff do DÉDALO).

Todo handoff entre agentes é um envelope tipado e versionado, com provenance e
confidence. A Guilda de Turing seta schema_valid; confidence < 0.6 aciona auditoria
de ELENCHUS.
"""
from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel, Field

    _HAS_PYDANTIC = True
except Exception:  # pragma: no cover
    from dataclasses import dataclass, field

    _HAS_PYDANTIC = False

SACP_VERSION = "1.0"
AUDIT_CONFIDENCE_THRESHOLD = 0.6


if _HAS_PYDANTIC:

    class SacpProvenance(BaseModel):
        agent: str
        evidence_type: str = "hipotese"
        source_refs: list[str] = []
        timestamp: Optional[str] = None
        confidence: float = Field(default=0.0, ge=0.0, le=1.0)

    class SacpEnvelope(BaseModel):
        sacp_version: str = SACP_VERSION
        run_id: str
        from_agent: str
        to_agent: str
        payload_type: str
        payload: dict[str, Any]
        provenance: SacpProvenance
        schema_valid: bool = False

else:  # pragma: no cover

    @dataclass
    class SacpProvenance:
        agent: str
        evidence_type: str = "hipotese"
        source_refs: list = field(default_factory=list)
        timestamp: Optional[str] = None
        confidence: float = 0.0

    @dataclass
    class SacpEnvelope:
        run_id: str
        from_agent: str
        to_agent: str
        payload_type: str
        payload: dict
        provenance: SacpProvenance
        sacp_version: str = SACP_VERSION
        schema_valid: bool = False


def needs_redteam_audit(envelope: "SacpEnvelope") -> bool:
    """Regra SACP: confidence abaixo do limiar aciona auditoria adversarial (ELENCHUS)."""
    return envelope.provenance.confidence < AUDIT_CONFIDENCE_THRESHOLD


if __name__ == "__main__":
    env = SacpEnvelope(
        run_id="forge-demo",
        from_agent="KAIROS",
        to_agent="LOGISTES",
        payload_type="OpportunityMap",
        payload={"opportunities": []},
        provenance=SacpProvenance(agent="KAIROS", confidence=0.68),
    )
    print("Pydantic:", _HAS_PYDANTIC, "| auditar?", needs_redteam_audit(env))
