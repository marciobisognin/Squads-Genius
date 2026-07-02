#!/usr/bin/env python3
"""Error-policy-engine do AETHER OS (aether.error/v1).

Toda falha vira contrato tipado com classe canônica e ação determinística.
Texto livre não é mecanismo de recuperação. PRD AETHER OS v1.2, Seção 14.8.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ENGINE_ID = "error-policy-engine@1.0.0"

# Tabela classe->ação (espelho versionado de config/error_policy.yaml).
CLASS_TABLE = {
    "contract_violation": {"retryable": False, "action": "block_step"},
    "policy_denied": {"retryable": False, "action": "block_and_log"},
    "approval_expired": {"retryable": False, "action": "execute_on_expire"},
    "budget_exceeded": {"retryable": False, "action": "pause_costly_and_escalate"},
    "quota_exceeded": {"retryable": False, "action": "enqueue_soft_or_refuse_hard"},
    "tool_error": {"retryable": True, "action": "retry_backoff_until_limit"},
    "model_unavailable": {"retryable": True, "action": "profile_fallback_or_pause"},
    "timeout": {"retryable": True, "action": "retry_if_idempotent_else_fail"},
    "sandbox_violation": {"retryable": False, "action": "abort_quarantine_alert"},
    "integrity_error": {"retryable": False, "action": "block_handoff_security_event"},
    "injection_suspected": {"retryable": False, "action": "quarantine_human_review"},
    "dependency_failed": {"retryable": False, "action": "propagate_skipped"},
    "compensation_failed": {"retryable": False, "action": "incident_critical_alert_human"},
    "internal": {"retryable": False, "action": "fail_safe_triage"},
}
RETRY_DEFAULTS = {"max_attempts": 3, "backoff_seconds": [2, 4, 8]}


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def classify(failure: dict) -> dict:
    """Materializa uma falha como aether.error/v1 com ação determinística."""
    error_class = failure.get("class", "internal")
    policy = CLASS_TABLE.get(error_class)
    if policy is None:
        error_class, policy = "internal", CLASS_TABLE["internal"]
    attempt = int(failure.get("attempt", 1))
    retryable = policy["retryable"] and attempt < RETRY_DEFAULTS["max_attempts"]
    backoffs = RETRY_DEFAULTS["backoff_seconds"]
    next_backoff = backoffs[min(attempt - 1, len(backoffs) - 1)] if retryable else None
    return {
        "schema_version": "aether.error/v1",
        "error_id": failure.get("error_id", f"err_{failure.get('run_id', 'na')}_{attempt}"),
        "run_id": failure.get("run_id", ""),
        "task_id": failure.get("task_id", ""),
        "class": error_class,
        "retryable": retryable,
        "attempt": attempt,
        "next_backoff_seconds": next_backoff,
        "action": policy["action"],
        "incident": error_class == "compensation_failed",
        "origin": failure.get("origin", ""),
        "message_operator": failure.get("message_operator", ""),
        "evidence": failure.get("evidence", []),
        "handled_by": ENGINE_ID,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Error-policy-engine AETHER")
    ap.add_argument("--failure", required=True, help="JSON da falha bruta")
    args = ap.parse_args()
    failure = json.loads(Path(args.failure).read_text(encoding="utf-8"))
    record = classify(failure)
    print(canonical(record))
    return 0 if record["retryable"] else 1


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
