#!/usr/bin/env python3
"""Motor de Orçamento determinístico do AETHER OS (aether.budget/v1).

Enforcement soft/hard por run/tenant/capability, em Decimal.
PRD AETHER OS v1.2, Seção 26.
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path

ENGINE_ID = "deterministic-budget-engine@1.0.0"
SOFT_RATIO = Decimal("0.8")


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def evaluate(ledger: dict) -> dict:
    """Avalia o estado do orçamento: ok | soft_warning | hard_stop."""
    limit = Decimal(str(ledger["limit_usd"]))
    spent = Decimal(str(ledger.get("spent_usd", "0")))
    estimated = Decimal(str(ledger.get("estimated_usd", "0")))
    if limit <= 0:
        raise ValueError("limit_usd deve ser positivo")
    if spent >= limit:
        state, enforcement = "hard_stop", "interromper novas tarefas custosas; exigir decisão"
    elif spent >= limit * SOFT_RATIO:
        state, enforcement = "soft_warning", "registrar evento e seguir"
    else:
        state, enforcement = "ok", "nenhum"
    return {
        "schema_version": "aether.budget/v1",
        "run_id": ledger.get("run_id", ""),
        "scope": ledger.get("scope", "run"),
        "limit_usd": str(limit),
        "estimated_usd": str(estimated),
        "spent_usd": str(spent),
        "remaining_usd": str(max(limit - spent, Decimal("0"))),
        "state": state,
        "enforcement": enforcement,
        "enforced_by": ENGINE_ID,
    }


def charge(ledger: dict, amount: str) -> dict:
    """Debita um custo e reavalia — recusa se o hard stop já estiver ativo."""
    current = evaluate(ledger)
    if current["state"] == "hard_stop":
        return {**current, "charge_accepted": False,
                "error_class": "budget_exceeded"}
    ledger = dict(ledger)
    ledger["spent_usd"] = str(Decimal(str(ledger.get("spent_usd", "0")))
                              + Decimal(str(amount)))
    result = evaluate(ledger)
    result["charge_accepted"] = True
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Motor de Orçamento AETHER")
    ap.add_argument("--ledger", required=True, help="JSON do BudgetLedger")
    ap.add_argument("--charge", help="valor a debitar (Decimal)")
    args = ap.parse_args()
    ledger = json.loads(Path(args.ledger).read_text(encoding="utf-8"))
    result = charge(ledger, args.charge) if args.charge else evaluate(ledger)
    print(canonical(result))
    return 0 if result.get("charge_accepted", True) else 4  # 4 = budget_exceeded


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
