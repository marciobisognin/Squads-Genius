#!/usr/bin/env python3
"""CLI operacional do AETHER OS (PRD §27.5 e §31).

Comandos: doctor, init, discover, search, select, risk, dispatch, budget,
quota, error, replay, review, learn, forge, demo. Stdlib-first; cada motor
também pode ser invocado diretamente pelo seu script.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "aether-os-squad@1.1.0"


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=2,
                      default=str)


def cmd_doctor(_args) -> int:
    """Diagnóstico do ambiente com correções acionáveis (não stack traces)."""
    checks = []
    ok = sys.version_info >= (3, 11)
    checks.append({"check": "python>=3.11", "pass": ok,
                   "fix": None if ok else "instale Python 3.11+"})
    here = Path(__file__).resolve().parent
    for engine in ("selection_engine", "risk_engine", "budget_engine",
                   "quota_engine", "dispatch_engine", "error_policy_engine",
                   "registry_indexer", "sacp_validator", "replay_engine",
                   "run_loop", "memory_engine", "forge_bridge",
                   "oikos_engine", "persona_engine", "host_adapter",
                   "token_economy"):
        present = (here / f"{engine}.py").is_file()
        checks.append({"check": f"engine:{engine}", "pass": present,
                       "fix": None if present else f"restaure scripts/{engine}.py"})
    for cfg in ("selection_weights.yaml", "risk_policy.yaml",
                "error_policy.yaml", "quotas.yaml",
                "host_adapters.yaml", "token_economy.yaml"):
        present = (here.parent / "config" / cfg).is_file()
        checks.append({"check": f"config:{cfg}", "pass": present,
                       "fix": None if present else f"restaure config/{cfg}"})
    verdict = "healthy" if all(c["pass"] for c in checks) else "attention"
    print(canonical({"doctor": verdict, "version": VERSION, "checks": checks}))
    return 0 if verdict == "healthy" else 1


def cmd_init(args) -> int:
    """Cria workspace local com estrutura mínima e memória vazia."""
    ws = Path(args.workspace).resolve()
    for sub in ("runs", "artifacts", "cache", "memory", "forge"):
        (ws / sub).mkdir(parents=True, exist_ok=True)
    lessons = ws / "memory" / "lessons.jsonl"
    if not lessons.exists():
        lessons.write_text("", encoding="utf-8")
    print(canonical({"initialized": str(ws),
                     "dirs": ["runs", "artifacts", "cache", "memory", "forge"],
                     "note": "idempotente e offline (local-first)"}))
    return 0


def cmd_demo(args) -> int:
    """Run guiado: descoberta -> seleção -> risco -> despacho -> replay.

    Narra cada decisão determinística de ponta a ponta, offline.
    """
    import dispatch_engine
    import replay_engine
    import risk_engine
    import selection_engine

    narrative = []
    request = {
        "run_id": "run_demo", "task_id": "t1",
        "granted_permissions": ["read_local"],
        "data_classification": "internal",
        "candidates": [
            {"id": "squad:beta@1.0.0/task:analisar", "trust_state": "trusted",
             "required_permissions": ["read_local"],
             "data_classes": ["public", "internal"],
             "sub_scores": {"semantic_fit": "0.90", "historical_quality": "0.85",
                            "version_freshness": "1.0", "risk_penalty": "0.2",
                            "cost_penalty": "0.1", "latency_penalty": "0.1"},
             "rationale": "capability compatível"},
            {"id": "squad:alfa@0.9.0/task:analisar", "trust_state": "discovered",
             "required_permissions": ["read_local"], "sub_scores": {}},
        ],
    }
    selection = selection_engine.decide(request)
    narrative.append({"stage": "seleção", "selected": selection["selected"],
                      "capability_gap": selection["capability_gap"]})
    action = {"run_id": "run_demo", "task_id": "t1", "factors": {
        "data_classification": "internal", "external_effect": "none",
        "reversibility": "reversible", "blast_radius": "artifact",
        "network": "deny", "credentials": "none"}}
    risk = risk_engine.assess(action)
    narrative.append({"stage": "risco", "tier": risk["tier"],
                      "policy": risk["approval_policy"]})
    dispatch = dispatch_engine.order([
        {"task_id": "t1", "run_id": "run_demo", "priority": "normal",
         "created_at": "2026-07-02T00:00:00Z", "unlocks_dependents": 2},
        {"task_id": "t2", "run_id": "run_demo", "priority": "normal",
         "created_at": "2026-07-02T00:00:01Z", "approval_pending": True},
    ])
    narrative.append({"stage": "despacho",
                      "queue": [q["task_id"] for q in dispatch["queue"]],
                      "blocked": [b["task_id"] for b in dispatch["blocked"]]})
    replay = replay_engine.replay_decision("selection", request, selection)
    narrative.append({"stage": "decision-replay", "verdict": replay["verdict"]})
    print(canonical({"demo": "ok", "narrative": narrative,
                     "invariant": "mesma entrada, mesma decisão — byte a byte"}))
    return 0


def forward(module: str, argv: list[str]) -> int:
    """Encaminha para o main() do motor correspondente."""
    import importlib
    mod = importlib.import_module(module)
    sys.argv = [module] + argv
    return mod.main()


def main() -> int:
    ap = argparse.ArgumentParser(prog="aether", description="AETHER OS CLI")
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    p_init = sub.add_parser("init")
    p_init.add_argument("--workspace", default="workspace")
    sub.add_parser("demo")
    for name, module in (
        ("discover", "registry_indexer"), ("search", "registry_indexer"),
        ("select", "selection_engine"), ("risk", "risk_engine"),
        ("dispatch", "dispatch_engine"), ("budget", "budget_engine"),
        ("quota", "quota_engine"), ("error", "error_policy_engine"),
        ("replay", "replay_engine"), ("review", "run_loop"),
        ("learn", "memory_engine"), ("forge", "forge_bridge"),
        ("handoff", "sacp_validator"), ("oikos", "oikos_engine"),
        ("persona", "persona_engine"), ("hosts", "host_adapter"),
        ("economy", "token_economy"),
    ):
        p = sub.add_parser(name, add_help=False)
        p.set_defaults(module=module)
    args, rest = ap.parse_known_args()
    if args.cmd == "doctor":
        return cmd_doctor(args)
    if args.cmd == "init":
        return cmd_init(args)
    if args.cmd == "demo":
        return cmd_demo(args)
    if args.cmd in ("discover", "search"):
        rest = [args.cmd] + rest
    if args.cmd in ("review",):
        rest = ["review"] + rest if rest and rest[0].startswith("--") else rest
    return forward(args.module, rest)


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
