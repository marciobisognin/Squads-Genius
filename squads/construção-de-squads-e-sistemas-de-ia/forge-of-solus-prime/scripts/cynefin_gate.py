#!/usr/bin/env python3
"""Portão de Cynefin (estrato TÉLOS → LÓGOS).

Implementa a **Lei do Portão de Cynefin**: nenhuma intenção é executada antes
de ser classificada em *clear / complicated / complex / chaotic*. A proposta de
classe pode vir do LLM (JSON), mas a **decisão de roteamento** (autonomia e
topologia) é determinística — Python puro e auditável.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forge_common import briefing_keywords, load_briefing, write_json  # noqa: E402

# Sinais lexicais determinísticos por domínio Cynefin (auditáveis e versionados).
SINAIS: dict[str, list[str]] = {
    "clear": [
        "rotina", "padrão", "padronizado", "simples", "checklist", "conhecido",
        "repetitiv", "boilerplate", "template", "formatar", "renomear",
    ],
    "complicated": [
        "integrar", "arquitetura", "pipeline", "analisar", "especialista",
        "engenharia", "otimizar", "schema", "api", "refator", "migrar",
    ],
    "complex": [
        "descobrir", "experiment", "incerto", "pesquisa", "hipótese",
        "emergente", "explorar", "prototipar", "ambíguo", "novo mercado",
    ],
    "chaotic": [
        "crise", "incidente", "urgente", "instável", "caos", "vazamento",
        "queda", "emergência", "pânico", "sem padrão",
    ],
}

# Roteamento determinístico derivado da classe (PRD §10 e §3.5).
ROTEAMENTO: dict[str, dict[str, Any]] = {
    "clear": {
        "autonomia": "L3",
        "pesquisa": "mínima",
        "topologia": "single-agent",
        "modo": "Modo 1 — Forja determinística",
        "justificativa_base": "objetivo fechado, solução conhecida, baixo risco",
    },
    "complicated": {
        "autonomia": "L2",
        "pesquisa": "instrumentos + arquitetura",
        "topologia": "multiagente sob demanda",
        "modo": "Modo 4 — Multiagente controlado",
        "justificativa_base": "requer análise/expertise, mas há resposta certa",
    },
    "complex": {
        "autonomia": "L1",
        "pesquisa": "spikes isolados + ciclos curtos",
        "topologia": "ciclos curtos com refutação reforçada",
        "modo": "Modo 2 — Forja assistida por pesquisa",
        "justificativa_base": "resposta só emerge por experimentação",
    },
    "chaotic": {
        "autonomia": "L1",
        "pesquisa": "estabilizar antes (diagnóstico)",
        "topologia": "single-agent, sem automação",
        "modo": "Modo 0 — Blueprint",
        "justificativa_base": "instável, sem padrão claro — estabilizar primeiro",
    },
}

ORDEM_AUTONOMIA = {"L1": 1, "L2": 2, "L3": 3}


def classificar(briefing: dict[str, Any]) -> dict[str, Any]:
    """Classifica o briefing por Cynefin com pontuação lexical determinística."""
    blob = " ".join(briefing_keywords(briefing))
    texto = " ".join(
        str(briefing.get(k, "")) for k in ("objective", "problem", "constraints")
    ).lower() + " " + blob
    scores = {dominio: 0 for dominio in SINAIS}
    for dominio, termos in SINAIS.items():
        for termo in termos:
            if termo in texto:
                scores[dominio] += 1
    # Dica explícita do briefing tem peso, mas não decide sozinha.
    dica = str(briefing.get("cynefin_hint", "") or "").strip().lower()
    if dica in SINAIS:
        scores[dica] += 1
    melhor = max(scores, key=lambda d: (scores[d], -list(SINAIS).index(d)))
    if all(v == 0 for v in scores.values()):
        melhor = "complicated"  # default conservador: pesquisa + L2
    rota = dict(ROTEAMENTO[melhor])

    # Lei: Chaotic nunca passa de L1; aplica-se o teto à dica do operador.
    proposto = str(briefing.get("autonomy_level", "") or "").strip().upper()
    autonomia = rota["autonomia"]
    if proposto in ORDEM_AUTONOMIA:
        # O Portão pode apenas REBAIXAR a autonomia proposta, nunca elevá-la.
        if ORDEM_AUTONOMIA[proposto] < ORDEM_AUTONOMIA[autonomia]:
            autonomia = proposto
    if melhor == "chaotic":
        autonomia = "L1"

    return {
        "cynefin": melhor,
        "scores": scores,
        "autonomy_level": autonomia,
        "pesquisa": rota["pesquisa"],
        "topologia": rota["topologia"],
        "modo": rota["modo"],
        "justificativa": rota["justificativa_base"],
        "lei": "Lei do Portão de Cynefin — classe decidida antes de qualquer ato.",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Portão de Cynefin (roteamento determinístico).")
    ap.add_argument("--briefing", required=True)
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    resultado = classificar(load_briefing(args.briefing))
    if args.out:
        write_json(args.out, resultado)
    import json

    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
