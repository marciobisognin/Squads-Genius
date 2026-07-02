#!/usr/bin/env python3
"""Motor de Seleção determinístico do AETHER OS (aether.selection-decision/v1).

Gates rígidos eliminatórios + score ponderado em Decimal + desempate estável.
Mentes propõem semantic_fit; este motor decide. Sem chamada a modelo.
PRD AETHER OS v1.2, Seção 12.
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path

ENGINE_ID = "deterministic-selection-engine@1.0.0"

DEFAULT_WEIGHTS = {
    "fit": "0.35", "quality": "0.20", "freshness": "0.05",
    "risk": "0.20", "cost": "0.10", "latency": "0.10",
}
GATES = ("contract_compatibility", "trust_state", "permissions_subset",
         "data_residency", "health")
TRUST_RANK = {"trusted": 3, "validated": 2, "parsed": 1,
              "discovered": 0, "deprecated": -1, "quarantined": -2}


def canonical(obj) -> str:
    """Serialização canônica: chaves ordenadas, Decimal textual (PRD §7.7)."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def check_gates(candidate: dict, request: dict) -> str | None:
    """Retorna o nome do gate reprovado, ou None se todos passam."""
    if candidate.get("output_contract") and request.get("required_output_contract"):
        if candidate["output_contract"] != request["required_output_contract"]:
            return "contract_compatibility"
    trust = candidate.get("trust_state", "discovered")
    planning_only = request.get("planning_only", False)
    if trust != "trusted" and not (planning_only and trust == "validated"):
        return "trust_state"
    required = set(candidate.get("required_permissions", []))
    granted = set(request.get("granted_permissions", []))
    if not required.issubset(granted):
        return "permissions_subset"
    allowed_classes = candidate.get("data_classes", ["public", "internal"])
    if request.get("data_classification", "internal") not in allowed_classes:
        return "data_residency"
    if not candidate.get("healthy", True):
        return "health"
    return None


def score(candidate: dict, weights: dict[str, Decimal]) -> Decimal:
    s = candidate.get("sub_scores", {})
    d = lambda k: Decimal(str(s.get(k, "0")))
    return (weights["fit"] * d("semantic_fit")
            + weights["quality"] * d("historical_quality")
            + weights["freshness"] * d("version_freshness")
            - weights["risk"] * d("risk_penalty")
            - weights["cost"] * d("cost_penalty")
            - weights["latency"] * d("latency_penalty"))


def tie_break_key(candidate: dict):
    """Desempate estável: confiança desc, custo asc, latência asc, id lex."""
    s = candidate.get("sub_scores", {})
    return (-TRUST_RANK.get(candidate.get("trust_state", "discovered"), 0),
            Decimal(str(s.get("cost_penalty", "0"))),
            Decimal(str(s.get("latency_penalty", "0"))),
            candidate["id"])


def decide(request: dict, weights_cfg: dict | None = None) -> dict:
    weights = {k: Decimal(v) for k, v in (weights_cfg or DEFAULT_WEIGHTS).items()}
    results, eligible = [], []
    for cand in sorted(request.get("candidates", []), key=lambda c: c["id"]):
        failed = check_gates(cand, request)
        if failed is not None:
            results.append({"id": cand["id"], "passed_gates": False,
                            "gate_failed": failed, "final_score": None})
            continue
        final = score(cand, weights)
        entry = {"id": cand["id"], "passed_gates": True,
                 "sub_scores": cand.get("sub_scores", {}),
                 "final_score": str(final),
                 "rationale": cand.get("rationale", "")}
        results.append(entry)
        eligible.append((final, tie_break_key(cand), cand["id"]))
    eligible.sort(key=lambda t: (-t[0], t[1]))
    selected = eligible[0][2] if eligible else None
    decision = {
        "schema_version": "aether.selection-decision/v1",
        "run_id": request.get("run_id", ""),
        "task_id": request.get("task_id", ""),
        "selected": selected,
        "capability_gap": selected is None,
        "weights": {k: str(v) for k, v in weights.items()},
        "gates_applied": list(GATES),
        "candidates": results,
        "decided_by": ENGINE_ID,
    }
    return decision


def main() -> int:
    ap = argparse.ArgumentParser(description="Motor de Seleção AETHER")
    ap.add_argument("--request", required=True, help="JSON do SelectionRequest")
    ap.add_argument("--weights", help="JSON opcional com pesos versionados")
    args = ap.parse_args()
    request = json.loads(Path(args.request).read_text(encoding="utf-8"))
    weights = None
    if args.weights:
        weights = json.loads(Path(args.weights).read_text(encoding="utf-8"))
    decision = decide(request, weights)
    print(canonical(decision))
    return 0 if not decision["capability_gap"] else 3  # 3 = capability_gap


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
