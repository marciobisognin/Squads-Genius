#!/usr/bin/env python3
"""Esqueleto do StateGraph do Anel da Forja (estrato KÝKLOS).

Define o estado global ``ForjaState`` e a topologia lógica dos sete atos. Quando
LangGraph está instalado, monta um `StateGraph` real; caso contrário, expõe a
topologia como dados (nós + arestas condicionais) para inspeção/teste — sem
quebrar a portabilidade do squad.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict


class ForjaState(TypedDict, total=False):
    # TÉLOS
    briefing_bruto: str
    briefing_normalizado: dict[str, Any]
    classificacao_cynefin: str
    nivel_autonomia: str
    # LÓGOS
    grafo_requisitos: dict[str, Any]
    contratos: Annotated[list[dict], operator.add]
    # ÓRGANON
    ferramentas_avaliadas: list[dict[str, Any]]
    arquitetura: dict[str, Any]
    artefatos: dict[str, Any]
    # KÝKLOS
    run_state: dict[str, Any]
    relatorio_qualidade: dict[str, Any]
    orcamento: dict[str, Any]
    iteracao: int
    falhas: Annotated[list[dict], operator.add]
    # MNÉMĒ
    aprendizados: Annotated[list[dict], operator.add]


# Topologia lógica dos atos do Anel (nós) e arestas condicionais (gates).
NOS = [
    "noesis", "boule", "diairesis", "jazz", "perceptor", "grapple",
    "praxis", "elenchos", "krisis", "bumblebee", "anamnesis",
]

ARESTAS = [
    ("noesis", "boule"),
    ("boule", "diairesis"),
    ("diairesis", "jazz"),
    ("jazz", "perceptor"),
    ("perceptor", "grapple"),
    ("grapple", "praxis"),
    ("praxis", "elenchos"),
    ("elenchos", "krisis"),
]

# Aresta condicional de self-healing/escalonamento após KRÍSIS.
ARESTAS_CONDICIONAIS = {
    "krisis": {
        "aprovado": "bumblebee",
        "reparavel": "diairesis",       # reparo guiado por diagnóstico
        "falha_2x": "__escalar_humano__",  # HITL
    },
    "bumblebee": {"ok": "anamnesis"},
}

MAX_RETRIES = 2


def topologia() -> dict[str, Any]:
    """Devolve a topologia do Anel como dados auditáveis."""
    return {
        "nos": NOS,
        "arestas": ARESTAS,
        "arestas_condicionais": ARESTAS_CONDICIONAIS,
        "max_retries": MAX_RETRIES,
        "regra": "falha idêntica 2x consecutivas → escala para humano (HITL)",
    }


def construir_grafo():  # pragma: no cover - depende de langgraph
    """Monta um StateGraph real se LangGraph estiver disponível."""
    try:
        from langgraph.graph import END, START, StateGraph  # type: ignore
    except Exception:
        return None
    g = StateGraph(ForjaState)
    for no in NOS:
        g.add_node(no, lambda state, _n=no: state)
    g.add_edge(START, "noesis")
    for origem, destino in ARESTAS:
        g.add_edge(origem, destino)
    g.add_edge("anamnesis", END)
    return g


if __name__ == "__main__":  # pragma: no cover
    import json

    print(json.dumps(topologia(), ensure_ascii=False, indent=2))
