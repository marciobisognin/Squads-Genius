#!/usr/bin/env python3
"""Métricas-base determinísticas do DÉDALO (LOGISTÉS).

Toda aritmética da fábrica vive aqui ou em scoring.py — nunca no LLM. Funções puras,
sem efeitos colaterais, com sanity checks que espelham a Guilda de Turing.
"""
from __future__ import annotations

from typing import Iterable


def safe_div(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Divisão segura: evita ZeroDivisionError e retorna default quando indefinido."""
    if denominator == 0:
        return default
    return numerator / denominator


def impact_effort_ratio(impact_1to5: int, effort_1to5: int) -> float:
    """Razão impacto/esforço (quanto maior, melhor o custo-benefício)."""
    for label, v in (("impact", impact_1to5), ("effort", effort_1to5)):
        if not (1 <= v <= 5):
            raise ValueError(f"Nota '{label}' fora de 1-5: {v}")
    return round(safe_div(impact_1to5, effort_1to5), 4)


def coverage(found: int, expected: int) -> float:
    """Cobertura (0..1): proporção de itens encontrados vs esperados. Útil para rastreabilidade."""
    if found < 0 or expected < 0:
        raise ValueError("found/expected não podem ser negativos")
    return round(min(1.0, safe_div(found, expected, default=0.0)), 4)


def mean(values: Iterable[float]) -> float:
    """Média aritmética determinística (0.0 para sequência vazia)."""
    vals = list(values)
    if not vals:
        return 0.0
    return round(sum(vals) / len(vals), 4)


def traceability_score(features: int, features_with_source: int) -> float:
    """Score de rastreabilidade: fração de features com origem (fonte/processo/evidência)."""
    return coverage(features_with_source, features)


if __name__ == "__main__":
    print("impact/effort 5/3 =", impact_effort_ratio(5, 3))
    print("coverage 7/8 =", coverage(7, 8))
    print("traceability 9/10 =", traceability_score(10, 9))
