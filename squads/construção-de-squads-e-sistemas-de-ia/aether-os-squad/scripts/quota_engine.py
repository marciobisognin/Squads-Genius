#!/usr/bin/env python3
"""Motor de Quotas determinístico do AETHER OS (QuotaLedger).

Orçamento controla dinheiro; quota controla recurso: concorrência, chamadas,
sandboxes, armazenamento e runs filhos. Enforcement soft (enfileira) e hard
(recusa com quota_exceeded). PRD AETHER OS v1.2, Seção 26.4.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ENGINE_ID = "deterministic-quota-engine@1.0.0"

DEFAULT_LIMITS = {
    "concurrent_tasks": {"soft": 4, "hard": 8},
    "model_calls_per_minute": {"soft": 30, "hard": 60},
    "concurrent_sandboxes": {"soft": 2, "hard": 4},
    "artifact_storage_mb": {"soft": 512, "hard": 1024},
    "child_runs_per_run": {"soft": 3, "hard": 5},
    "child_run_max_depth": {"hard": 3},
}


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def check(resource: str, current: int, requested: int = 1,
          limits: dict | None = None, scope: str = "tenant_default") -> dict:
    """Decide admit | enqueue_soft | refuse_hard para um pedido de recurso."""
    table = (limits or DEFAULT_LIMITS).get(resource)
    if table is None:
        raise ValueError(f"recurso desconhecido: {resource}")
    projected = current + requested
    hard = table.get("hard")
    soft = table.get("soft", hard)
    if hard is not None and projected > hard:
        decision, error_class = "refuse_hard", "quota_exceeded"
    elif soft is not None and projected > soft:
        decision, error_class = "enqueue_soft", None
    else:
        decision, error_class = "admit", None
    return {
        "schema_version": "aether.quota-decision/v1",
        "scope": scope,
        "resource": resource,
        "current": current,
        "requested": requested,
        "projected": projected,
        "soft_limit": soft,
        "hard_limit": hard,
        "decision": decision,
        "error_class": error_class,
        "enforced_by": ENGINE_ID,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Motor de Quotas AETHER")
    ap.add_argument("--resource", required=True)
    ap.add_argument("--current", type=int, required=True)
    ap.add_argument("--requested", type=int, default=1)
    ap.add_argument("--limits", help="JSON opcional com limites versionados")
    ap.add_argument("--scope", default="tenant_default")
    args = ap.parse_args()
    limits = None
    if args.limits:
        limits = json.loads(Path(args.limits).read_text(encoding="utf-8"))
    result = check(args.resource, args.current, args.requested, limits, args.scope)
    print(canonical(result))
    return {"admit": 0, "enqueue_soft": 5, "refuse_hard": 6}[result["decision"]]


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
