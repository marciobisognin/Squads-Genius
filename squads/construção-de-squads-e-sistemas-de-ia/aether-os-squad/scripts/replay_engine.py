#!/usr/bin/env python3
"""Decision-replay do AETHER OS (aether.replay-report/v1).

Reexecuta um motor determinístico com a entrada registrada e compara a saída
byte a byte com a decisão original. Divergência = quebra de invariante.
PRD AETHER OS v1.2, Seção 25.7.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ENGINE_ID = "aether-replayer@1.0.0"


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def replay_decision(engine: str, recorded_input: dict, recorded_output: dict) -> dict:
    """Reexecuta o motor indicado e compara byte a byte."""
    if engine == "selection":
        import selection_engine
        fresh = selection_engine.decide(recorded_input)
    elif engine == "risk":
        import risk_engine
        fresh = risk_engine.assess(recorded_input)
    elif engine == "dispatch":
        import dispatch_engine
        fresh = dispatch_engine.order(recorded_input)
    elif engine == "budget":
        import budget_engine
        fresh = budget_engine.evaluate(recorded_input)
    elif engine == "error":
        import error_policy_engine
        fresh = error_policy_engine.classify(recorded_input)
    else:
        raise ValueError(f"motor desconhecido: {engine}")
    original_bytes = canonical(recorded_output)
    fresh_bytes = canonical(fresh)
    identical = original_bytes == fresh_bytes
    divergences = []
    if not identical:
        orig, new = recorded_output, fresh
        keys = sorted(set(orig) | set(new))
        for key in keys:
            if canonical(orig.get(key)) != canonical(new.get(key)):
                divergences.append({"field": key,
                                    "recorded": orig.get(key),
                                    "replayed": new.get(key)})
    return {
        "schema_version": "aether.replay-report/v1",
        "mode": "decision-replay",
        "engine": engine,
        "compared": 1,
        "identical": 1 if identical else 0,
        "divergences": divergences,
        "verdict": "pass" if identical else "fail",
        "alert": None if identical else "critical: quebra de invariante de determinismo",
        "replayed_by": ENGINE_ID,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Decision-replay AETHER")
    ap.add_argument("--engine", required=True,
                    choices=["selection", "risk", "dispatch", "budget", "error"])
    ap.add_argument("--input", required=True, help="entrada registrada (JSON)")
    ap.add_argument("--output", required=True, help="decisão registrada (JSON)")
    args = ap.parse_args()
    recorded_input = json.loads(Path(args.input).read_text(encoding="utf-8"))
    recorded_output = json.loads(Path(args.output).read_text(encoding="utf-8"))
    report = replay_decision(args.engine, recorded_input, recorded_output)
    print(canonical(report))
    return 0 if report["verdict"] == "pass" else 8  # 8 = divergência crítica


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
