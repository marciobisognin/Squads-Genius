#!/usr/bin/env python3
"""PERCEPTOR — motor de pontuação determinístico (estrato ÓRGANON).

Materializa a **Lei da Fronteira Determinística**: o LLM (JAZZ) propõe
candidatas e estima métricas qualitativas, mas o **score final é Python puro
com `Decimal`** — auditável e reproduzível. Nenhum número que importa nasce de
um modelo de linguagem.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

getcontext().prec = 12

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forge_common import write_json  # noqa: E402

# Pesos canônicos (somam 1.00) — versionados e auditáveis.
PESOS: dict[str, Decimal] = {
    "fit": Decimal("0.25"),
    "licenca": Decimal("0.20"),
    "manutencao": Decimal("0.15"),
    "seguranca": Decimal("0.15"),
    "instalacao": Decimal("0.10"),
    "testabilidade": Decimal("0.10"),
    "interop_agente": Decimal("0.05"),
}

LIMIAR_INCORPORAR = Decimal("0.70")
LIMIAR_ADAPTAR = Decimal("0.50")


def pontuar(metricas: dict[str, Any]) -> Decimal:
    """Cada métrica em [0,1]. Retorna score determinístico em [0,1]."""
    faltando = set(PESOS) - set(metricas)
    if faltando:
        raise ValueError(f"métricas ausentes: {sorted(faltando)}")
    convertidas: dict[str, Decimal] = {}
    for k in PESOS:
        v = Decimal(str(metricas[k]))
        if not (Decimal(0) <= v <= Decimal(1)):
            raise ValueError(f"métrica fora de [0,1]: {k}={v}")
        convertidas[k] = v
    score = sum((PESOS[k] * convertidas[k] for k in PESOS), Decimal(0))
    return score.quantize(Decimal("0.0001"))


def decidir(score: Decimal, risco: str) -> str:
    """Decisão determinística: risco alto nunca incorpora automaticamente."""
    if risco == "high":
        return "reject"
    if score >= LIMIAR_INCORPORAR:
        return "incorporate"
    if score >= LIMIAR_ADAPTAR:
        return "adapt"
    return "watch"


def avaliar_candidatas(candidatas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Avalia uma lista de candidatas, anexando score e decisão."""
    avaliadas: list[dict[str, Any]] = []
    for cand in candidatas:
        score = pontuar(cand["metrics"])
        risco = str(cand.get("risk_level", "low"))
        decisao = decidir(score, risco)
        out = dict(cand)
        out["fit_score"] = float(score)
        out["decision"] = decisao
        out["evidence"] = list(cand.get("evidence", [])) + [
            f"score={score} (Decimal, pesos canônicos v1); risco={risco}",
        ]
        avaliadas.append(out)
    avaliadas.sort(key=lambda c: (-c["fit_score"], c["tool"]))
    return avaliadas


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="PERCEPTOR — pontuação determinística de instrumentos.")
    ap.add_argument("--candidates", required=True, help="JSON do discover_tools.py")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    data = json.loads(Path(args.candidates).read_text(encoding="utf-8"))
    candidatas = data.get("candidates", data if isinstance(data, list) else [])
    avaliadas = avaliar_candidatas(candidatas)
    incorporadas = [c for c in avaliadas if c["decision"] in {"incorporate", "adapt"}]
    resultado = {
        "engine": "decimal_v1",
        "pesos": {k: str(v) for k, v in PESOS.items()},
        "limiares": {"incorporar": str(LIMIAR_INCORPORAR), "adaptar": str(LIMIAR_ADAPTAR)},
        "count": len(avaliadas),
        "incorporated_or_adapted": len(incorporadas),
        "evaluations": avaliadas,
    }
    if args.out:
        write_json(args.out, resultado)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
