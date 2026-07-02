#!/usr/bin/env python3
"""Motor de Economia de Tokens do AETHER OS — PRD v1.3, §26.5.

Cinco alavancas determinísticas, medidas e NEUTRAS em relação às decisões:
carga preguiçosa, carga dirigida, layout cacheável, derivação com herança e
handoff por referência. Nenhuma alavanca pode alterar o resultado de uma
decisão (neutralidade verificada por replay, NFR-32). Stdlib puro.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ENGINE_ID = "aether-token-economy@1.0.0"

DATA_CLASS_RANK = {"public": 0, "internal": 1, "confidential": 2, "restricted": 3}
DEFAULT_INHERIT_THRESHOLD_TOKENS = 24000
DEFAULT_ENVELOPE_CEILING_TOKENS = 2000
LEVERS = ("lazy_loading", "directed_loading", "cacheable_prompt_layout",
          "fork_with_inheritance", "handoff_by_reference")


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def estimate_tokens(text: str) -> int:
    """Estimativa determinística (~4 chars/token) — para limiares, não cobrança."""
    return max(1, len(text) // 4)


def derivation_decide(request: dict) -> dict:
    """Regras determinísticas de derivação, NESTA ordem (PRD §26.5):

    1. host sem subagent_fork -> instanciação limpa;
    2. conteúdo não confiável no pai OU classe de dado do filho inferior à do
       pai -> limpa, SEMPRE (segurança precede economia);
    3. contexto herdado acima do limiar -> limpa (herdar sai mais caro);
    4. caso contrário -> derivação com herança, registrada como evento.
    """
    threshold = int(request.get("inherit_threshold_tokens",
                                DEFAULT_INHERIT_THRESHOLD_TOKENS))
    rule, decision = None, None
    if not request.get("host_subagent_fork", False):
        rule, decision = 1, "clean_instantiation"
    elif (request.get("parent_has_untrusted_content", False)
          or DATA_CLASS_RANK.get(request.get("child_data_class", "internal"), 1)
          < DATA_CLASS_RANK.get(request.get("parent_data_class", "internal"), 1)):
        rule, decision = 2, "clean_instantiation"
    elif int(request.get("parent_context_tokens", 0)) > threshold:
        rule, decision = 3, "clean_instantiation"
    else:
        rule, decision = 4, "fork_with_inheritance"
    return {"schema_version": "aether.derivation-decision/v1",
            "run_id": request.get("run_id", ""),
            "task_id": request.get("task_id", ""),
            "decision": decision,
            "rule_applied": rule,
            "security_precedes_economy": rule == 2,
            "event": "derivation.decided",
            "decided_by": ENGINE_ID}


def envelope_check(payload_text: str,
                   ceiling: int = DEFAULT_ENVELOPE_CEILING_TOKENS) -> dict:
    """Handoff por referência: teto de tokens por envelope SACP (NFR-31)."""
    tokens = estimate_tokens(payload_text)
    ok = tokens <= ceiling
    return {"schema_version": "aether.envelope-budget/v1",
            "estimated_tokens": tokens, "ceiling": ceiling,
            "verdict": "pass" if ok else "exceed",
            "action": None if ok else
            "transportar por artifact:// (referência), nunca conteúdo bruto extenso",
            "checked_by": ENGINE_ID}


def layout(sections: list[dict]) -> dict:
    """Layout cacheável: estável no início, variável no fim — ordem estável."""
    stable = [s for s in sections if s.get("stability") == "stable"]
    variable = [s for s in sections if s.get("stability") != "stable"]
    ordered = ([s["id"] for s in sorted(stable, key=lambda s: s["id"])]
               + [s["id"] for s in variable])
    return {"schema_version": "aether.prompt-layout/v1",
            "order": ordered,
            "cache_prefix": [s["id"] for s in sorted(stable, key=lambda s: s["id"])],
            "note": "conteúdo estável primeiro (manifesto, sistema, prósopon); "
                    "variável no fim (briefing, memória, handoff)",
            "arranged_by": ENGINE_ID}


def report(metrics: dict) -> dict:
    """Telemetria de economia por alavanca — sustenta custo por artefato."""
    per_lever = {lever: metrics.get(lever, {"saved_tokens": 0})
                 for lever in LEVERS}
    total = sum(int(v.get("saved_tokens", 0)) for v in per_lever.values())
    return {"schema_version": "aether.token-economy-report/v1",
            "per_lever": per_lever, "total_saved_tokens": total,
            "neutrality": "verificada por decision-replay em pares com/sem "
                          "cache e com/sem herança; divergência é incidente",
            "reported_by": ENGINE_ID}


def main() -> int:
    ap = argparse.ArgumentParser(description="Economia de Tokens AETHER")
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("derive"); d.add_argument("--request", required=True)
    e = sub.add_parser("envelope-check"); e.add_argument("--payload", required=True)
    e.add_argument("--ceiling", type=int, default=DEFAULT_ENVELOPE_CEILING_TOKENS)
    l = sub.add_parser("layout"); l.add_argument("--sections", required=True)
    r = sub.add_parser("report"); r.add_argument("--metrics", required=True)
    args = ap.parse_args()
    if args.cmd == "derive":
        request = json.loads(Path(args.request).read_text(encoding="utf-8"))
        print(canonical(derivation_decide(request)))
        return 0
    if args.cmd == "envelope-check":
        text = Path(args.payload).read_text(encoding="utf-8", errors="ignore")
        result = envelope_check(text, args.ceiling)
        print(canonical(result))
        return 0 if result["verdict"] == "pass" else 11  # 11 = envelope excede teto
    if args.cmd == "layout":
        sections = json.loads(Path(args.sections).read_text(encoding="utf-8"))
        print(canonical(layout(sections)))
        return 0
    metrics = json.loads(Path(args.metrics).read_text(encoding="utf-8"))
    print(canonical(report(metrics)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
