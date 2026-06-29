#!/usr/bin/env python3
"""Hooks de observabilidade (Langfuse) do DÉDALO.

Registra span por nó (input/output/modelo/tokens/custo/latência) e score por nó
(schema_valid, confidence, veredito de red-team, taxa de reparo de Turing). Degrada
para um logger local determinístico quando o SDK do Langfuse não está instalado —
nenhuma credencial é lida ou exigida aqui.
"""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Optional


@dataclass
class NodeSpan:
    node: str
    run_id: str
    model: str = ""
    input_summary: str = ""
    output_summary: str = ""
    tokens: int = 0
    cost_brl: float = 0.0
    latency_ms: float = 0.0
    schema_valid: bool = True
    confidence: float = 0.0
    redteam_verdict: Optional[str] = None
    repair_rate: float = 0.0
    started_at: float = field(default_factory=time.time)


class ObservabilityClient:
    """Cliente de observabilidade com fallback local (sem dependências externas)."""

    def __init__(self, provider: str = "langfuse") -> None:
        self.provider = provider
        self._sink: list[dict[str, Any]] = []
        self._backend = self._try_load_backend()

    @staticmethod
    def _try_load_backend() -> Optional[Any]:
        try:  # pragma: no cover - depende de ambiente
            import langfuse  # type: ignore

            return langfuse
        except Exception:
            return None

    def record_span(self, span: NodeSpan) -> dict[str, Any]:
        span.latency_ms = round((time.time() - span.started_at) * 1000, 2)
        event = asdict(span)
        self._sink.append(event)
        return event

    def alerts(self, cost_ceiling_brl: float = 0.0, repair_ceiling: float = 0.3) -> list[str]:
        """Regras de alerta: custo acima do teto e reparo de Turing acima do limiar."""
        out: list[str] = []
        for ev in self._sink:
            if cost_ceiling_brl and ev["cost_brl"] > cost_ceiling_brl:
                out.append(f"custo acima do teto no nó {ev['node']}: R$ {ev['cost_brl']:.2f}")
            if ev["repair_rate"] > repair_ceiling:
                out.append(f"reparo de Turing alto no nó {ev['node']}: {ev['repair_rate']:.0%}")
        return out

    def dump(self) -> str:
        return json.dumps(self._sink, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    client = ObservabilityClient()
    client.record_span(NodeSpan(node="KAIROS", run_id="forge-demo", model="opus", confidence=0.68))
    print("backend langfuse disponível:", client._backend is not None)
    print(client.dump())
