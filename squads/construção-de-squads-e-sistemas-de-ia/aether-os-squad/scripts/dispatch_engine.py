#!/usr/bin/env python3
"""Motor de Despacho determinístico do AETHER OS.

Ordena tarefas prontas por: elegibilidade -> prioridade -> justiça entre
tenants (round-robin ponderado) -> caminho crítico -> desempate lexicográfico
(created_at, run_id, task_id). Sem preempção. PRD AETHER OS v1.2, Seção 14.6.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ENGINE_ID = "deterministic-dispatch-engine@1.0.0"
PRIORITY_RANK = {"critical": 0, "high": 1, "normal": 2, "low": 3}


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def eligible(task: dict) -> tuple[bool, str | None]:
    """Elegibilidade: dependências, aprovação, quota, disjuntor."""
    if not task.get("dependencies_satisfied", True):
        return False, "dependencies_unsatisfied"
    if task.get("approval_pending", False):
        return False, "approval_pending"
    if not task.get("quota_available", True):
        return False, "quota_unavailable"
    if task.get("circuit_breaker_open", False):
        return False, "circuit_breaker_open"
    return True, None


def order(tasks: list[dict]) -> dict:
    """Produz a fila ordenada + decisão auditável por tarefa."""
    ready, blocked = [], []
    for t in tasks:
        ok, reason = eligible(t)
        (ready if ok else blocked).append(
            {**t, "blocked_reason": None if ok else reason})

    # Justiça entre tenants: intercalação round-robin ponderada e estável.
    by_tenant: dict[str, list[dict]] = {}
    for t in ready:
        by_tenant.setdefault(t.get("tenant_id", "tenant_default"), []).append(t)
    for tenant, group in by_tenant.items():
        group.sort(key=lambda t: (
            PRIORITY_RANK.get(t.get("priority", "normal"), 2),
            -int(t.get("unlocks_dependents", 0)),        # caminho crítico
            t.get("created_at", ""), t.get("run_id", ""), t.get("task_id", "")))
    queue = []
    tenants = sorted(by_tenant)  # ordem estável de tenants
    cursors = {tn: 0 for tn in tenants}
    weights = {tn: max(int(by_tenant[tn][0].get("tenant_weight", 1)), 1)
               for tn in tenants}
    while any(cursors[tn] < len(by_tenant[tn]) for tn in tenants):
        for tn in tenants:
            for _ in range(weights[tn]):
                if cursors[tn] < len(by_tenant[tn]):
                    queue.append(by_tenant[tn][cursors[tn]])
                    cursors[tn] += 1

    return {
        "schema_version": "aether.dispatch-decision/v1",
        "queue": [{"position": i,
                   "task_id": t.get("task_id"), "run_id": t.get("run_id"),
                   "tenant_id": t.get("tenant_id", "tenant_default"),
                   "priority": t.get("priority", "normal"),
                   "unlocks_dependents": int(t.get("unlocks_dependents", 0))}
                  for i, t in enumerate(queue)],
        "blocked": [{"task_id": t.get("task_id"), "run_id": t.get("run_id"),
                     "reason": t["blocked_reason"]} for t in blocked],
        "properties": {"preemption": False, "backpressure_explicit": True},
        "decided_by": ENGINE_ID,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Motor de Despacho AETHER")
    ap.add_argument("--tasks", required=True,
                    help="JSON com lista de tarefas prontas/candidatas")
    args = ap.parse_args()
    tasks = json.loads(Path(args.tasks).read_text(encoding="utf-8"))
    print(canonical(order(tasks)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
