#!/usr/bin/env python3
"""Máquina de estados do run do AETHER OS + loop de revisão até a entrega.

Implementa o lifecycle (PRD §14.1) e o self-healing limitado (PRD §14.3):
validating -> executing enquanto houver critério de aceite não atendido e
tentativas disponíveis; esgotado o teto, partial/failed — nunca loop infinito.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ENGINE_ID = "aether-run-loop@1.0.0"

TRANSITIONS = {
    "received": {"classified"},
    "classified": {"awaiting_classification", "planned"},
    "awaiting_classification": {"classified", "aborted"},
    "planned": {"awaiting_approval", "executing"},
    "awaiting_approval": {"planned", "aborted"},
    "executing": {"validating", "failed"},
    "validating": {"executing", "completed", "partial"},
    "completed": {"learning"},
    "partial": {"learning"},
    "learning": set(),
    "failed": set(),
    "aborted": set(),
}
ESCALATION_ORDER = ("retry_same", "retry_adjusted", "partial_replan", "human_gate")
DEFAULT_MAX_ATTEMPTS = 3


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def transition(state: str, to: str) -> str:
    if to not in TRANSITIONS.get(state, set()):
        raise ValueError(f"transição inválida: {state} -> {to}")
    return to


def check_acceptance(task: dict) -> list[str]:
    """Critérios de aceite são checks determinísticos declarados por tarefa.

    Cada critério é um dict {"id", "satisfied"} avaliado por neurônios
    lógicos (schema, hash, reconciliação); aqui consumimos o resultado.
    """
    return [c["id"] for c in task.get("acceptance_criteria", [])
            if not c.get("satisfied", False)]


def review_loop(task: dict, max_attempts: int = DEFAULT_MAX_ATTEMPTS) -> dict:
    """Executa o loop de revisão de UMA tarefa até entrega completa ou teto.

    A "execução" real é delegada aos executores selecionados; este motor
    decide as transições e registra cada tentativa (motivo + estratégia).
    """
    attempts_log = []
    attempts = task.get("attempts", [])
    for attempt_no in range(1, max_attempts + 1):
        attempt = attempts[attempt_no - 1] if attempt_no <= len(attempts) else {}
        pending = check_acceptance({**task, **attempt}) if attempt else \
            check_acceptance(task)
        strategy = ESCALATION_ORDER[min(attempt_no - 1, len(ESCALATION_ORDER) - 1)]
        attempts_log.append({
            "attempt": attempt_no,
            "strategy": strategy,
            "unmet_criteria": pending,
            "adversarial_resolved": bool(attempt.get("adversarial_resolved",
                                                     task.get("adversarial_resolved", True))),
        })
        adversarial_ok = attempts_log[-1]["adversarial_resolved"]
        if not pending and adversarial_ok:
            return {
                "schema_version": "aether.review-loop/v1",
                "task_id": task.get("task_id", ""),
                "run_id": task.get("run_id", ""),
                "final_state": "completed",
                "attempts": attempts_log,
                "decided_by": ENGINE_ID,
            }
    partial_ok = any(not log["unmet_criteria"] for log in attempts_log)
    return {
        "schema_version": "aether.review-loop/v1",
        "task_id": task.get("task_id", ""),
        "run_id": task.get("run_id", ""),
        "final_state": "partial" if partial_ok else "failed",
        "escalation": "human_gate",
        "attempts": attempts_log,
        "error": None if partial_ok else {
            "class": "internal" if not task.get("last_error_class")
            else task["last_error_class"],
            "detail": "teto de tentativas esgotado sem cumprir critérios de aceite",
        },
        "decided_by": ENGINE_ID,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Run loop / máquina de estados AETHER")
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("transition")
    t.add_argument("--state", required=True)
    t.add_argument("--to", required=True)
    l = sub.add_parser("review")
    l.add_argument("--task", required=True, help="JSON da tarefa com critérios")
    l.add_argument("--max-attempts", type=int, default=DEFAULT_MAX_ATTEMPTS)
    args = ap.parse_args()
    if args.cmd == "transition":
        try:
            new_state = transition(args.state, args.to)
        except ValueError as exc:
            print(canonical({"error": str(exc), "class": "contract_violation"}))
            return 1
        print(canonical({"state": new_state}))
        return 0
    task = json.loads(Path(args.task).read_text(encoding="utf-8"))
    result = review_loop(task, args.max_attempts)
    print(canonical(result))
    return 0 if result["final_state"] == "completed" else 9


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
