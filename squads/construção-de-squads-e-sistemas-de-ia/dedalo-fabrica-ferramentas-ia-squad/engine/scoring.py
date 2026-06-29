#!/usr/bin/env python3
"""Motor determinístico de priorização de oportunidades do DÉDALO.

Invariante central do squad: o LLM fornece as notas 1-5 como PREMISSAS; o Python
computa o ranking. Funções puras, versionadas e auditáveis — sem aleatoriedade,
diff zero entre runs idênticos.
"""
from __future__ import annotations

from dataclasses import dataclass

from weights import SCORE_THRESHOLD, WEIGHTS_V1


@dataclass(frozen=True)
class OppScoringAssumptions:
    """Premissas 1-5 fornecidas pelo LLM (KAIRÓS). Validadas antes do cálculo."""

    impact_value_1to5: int
    effort_1to5: int
    risk_1to5: int
    data_availability_1to5: int
    repetition_1to5: int


@dataclass(frozen=True)
class ScoredOpportunity:
    name: str
    score: float
    below_threshold: bool


def _check_range(value: int, label: str) -> None:
    if not isinstance(value, int) or not (1 <= value <= 5):
        raise ValueError(f"Nota '{label}' fora do intervalo 1-5: {value!r}")


def validate_assumptions(a: OppScoringAssumptions) -> None:
    """Sanity gate (espelha a Guilda de Turing): notas precisam estar em 1-5."""
    _check_range(a.impact_value_1to5, "impact_value_1to5")
    _check_range(a.effort_1to5, "effort_1to5")
    _check_range(a.risk_1to5, "risk_1to5")
    _check_range(a.data_availability_1to5, "data_availability_1to5")
    _check_range(a.repetition_1to5, "repetition_1to5")


def score_opportunity(a: OppScoringAssumptions, w: dict[str, float] = WEIGHTS_V1) -> float:
    """Score puro e determinístico de uma oportunidade. Mesma entrada => mesmo número."""
    validate_assumptions(a)
    return round(
        w["impact"] * (a.impact_value_1to5 / 5)
        + w["repetition"] * (a.repetition_1to5 / 5)
        + w["data_availability"] * (a.data_availability_1to5 / 5)
        - w["effort_penalty"] * (a.effort_1to5 / 5)
        - w["risk_penalty"] * (a.risk_1to5 / 5),
        4,
    )


def rank_opportunities(opps: list[tuple[str, OppScoringAssumptions]]) -> list[ScoredOpportunity]:
    """Ordena oportunidades por score decrescente. Determinístico e estável.

    Desempate por nome (ordem lexicográfica) garante reprodutibilidade total.
    """
    scored = [
        ScoredOpportunity(name=name, score=score_opportunity(a), below_threshold=False)
        for name, a in opps
    ]
    scored = [
        ScoredOpportunity(s.name, s.score, s.score < SCORE_THRESHOLD) for s in scored
    ]
    return sorted(scored, key=lambda s: (-s.score, s.name))


if __name__ == "__main__":
    demo = [
        ("Triagem inteligente para clínicas", OppScoringAssumptions(5, 3, 4, 2, 5)),
        ("Radar de preço para distribuidora", OppScoringAssumptions(4, 2, 2, 4, 4)),
        ("Base de conhecimento viva", OppScoringAssumptions(3, 3, 1, 3, 5)),
    ]
    for s in rank_opportunities(demo):
        flag = " (abaixo do limiar)" if s.below_threshold else ""
        print(f"{s.score:+.4f}  {s.name}{flag}")
