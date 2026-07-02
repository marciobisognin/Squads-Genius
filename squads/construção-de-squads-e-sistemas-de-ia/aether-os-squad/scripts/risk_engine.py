#!/usr/bin/env python3
"""Motor de Risco determinístico do AETHER OS (aether.risk-assessment/v1).

Fatores estruturados -> score ponderado (Decimal) -> tier + escalonamento
rígido. Sem chamada a modelo. PRD AETHER OS v1.2, Seção 19.
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path

ENGINE_ID = "deterministic-risk-engine@1.0.0"

FACTOR_SCALES = {
    "data_classification": {"public": 0, "internal": 1, "confidential": 2, "restricted": 3},
    "external_effect": {"none": 0, "read": 1, "write": 2, "irreversible": 3},
    "reversibility": {"reversible": 0, "compensable": 1, "irreversible": 2},
    "blast_radius": {"artifact": 0, "project": 1, "tenant": 2, "cross-tenant": 3},
    "network": {"deny": 0, "allowlist": 1, "open": 2},
    "credentials": {"none": 0, "scoped": 1, "broad": 2},
}
WEIGHTS = {
    "data_classification": Decimal("0.25"), "external_effect": Decimal("0.25"),
    "reversibility": Decimal("0.20"), "blast_radius": Decimal("0.12"),
    "network": Decimal("0.09"), "credentials": Decimal("0.09"),
}
TIERS = ("low", "medium", "high", "critical")
THRESHOLDS = {"low": Decimal("0.25"), "medium": Decimal("0.50"), "high": Decimal("0.75")}
APPROVAL_MATRIX = {
    "low": "auto", "medium": "supervised",
    "high": "human_approval_before_effect", "critical": "blocked_by_default",
}
CRITICAL_ACTIONS = {"payment", "data_deletion", "regulatory_decision",
                    "irreversible_production"}


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def weighted_score(factors: dict) -> Decimal:
    """Soma ponderada normalizada em [0,1]."""
    total = Decimal("0")
    for name, scale in FACTOR_SCALES.items():
        value = factors.get(name)
        if value not in scale:
            raise ValueError(f"fator inválido: {name}={value!r}")
        max_level = max(scale.values())
        normalized = Decimal(scale[value]) / Decimal(max_level)
        total += WEIGHTS[name] * normalized
    return total


def map_score_to_tier(score: Decimal) -> str:
    if score <= THRESHOLDS["low"]:
        return "low"
    if score <= THRESHOLDS["medium"]:
        return "medium"
    if score <= THRESHOLDS["high"]:
        return "high"
    return "critical"


def apply_hard_escalations(tier: str, action: dict) -> tuple[str, str | None]:
    """Regras rígidas elevam o tier independentemente do score (PRD §19.3)."""
    factors = action["factors"]
    rank = {t: i for i, t in enumerate(TIERS)}
    rule = None

    def raise_to(min_tier: str, rule_name: str):
        nonlocal tier, rule
        if rank[tier] < rank[min_tier]:
            tier, rule = min_tier, rule_name

    if action.get("action_kind") in CRITICAL_ACTIONS:
        raise_to("critical", "critical_action_kind -> critical")
    if factors.get("external_effect") == "irreversible":
        raise_to("high", "irreversible_effect -> min(high)")
    effect_rank = FACTOR_SCALES["external_effect"]
    if (factors.get("data_classification") == "restricted"
            and effect_rank.get(factors.get("external_effect", "none"), 0) >= effect_rank["write"]):
        raise_to("high", "restricted_or_write_effect -> min(high)")
    if factors.get("credentials") == "broad" and factors.get("network") == "open":
        raise_to("high", "broad_creds_open_network -> min(high)")
    return tier, rule


def assess(action: dict) -> dict:
    score = weighted_score(action["factors"])
    tier = map_score_to_tier(score)
    tier, rule = apply_hard_escalations(tier, action)
    return {
        "schema_version": "aether.risk-assessment/v1",
        "run_id": action.get("run_id", ""),
        "task_id": action.get("task_id", ""),
        "tier": tier,
        "score": str(score),
        "factors": {k: action["factors"][k] for k in sorted(FACTOR_SCALES)},
        "triggered_rule": rule,
        "approval_policy": APPROVAL_MATRIX[tier],
        "assessed_by": ENGINE_ID,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Motor de Risco AETHER")
    ap.add_argument("--action", required=True, help="JSON do ActionDescriptor")
    args = ap.parse_args()
    action = json.loads(Path(args.action).read_text(encoding="utf-8"))
    print(canonical(assess(action)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
