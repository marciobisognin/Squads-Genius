#!/usr/bin/env python3
"""JAZZ — descoberta de instrumentos (estrato ÓRGANON).

Gera candidatas de instrumentos a partir dos termos do briefing, consultando
um catálogo curado offline (determinístico, sem rede) e, quando conectores de
rede estiverem habilitados, índices públicos. No MVP opera em modo offline:
zero rede, zero credenciais, 100% reproduzível.

A pontuação NÃO acontece aqui (Lei da Fronteira Determinística): JAZZ apenas
propõe candidatas com métricas estimadas; PERCEPTOR (`evaluate_tool.py`) calcula
o score final com `Decimal`.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forge_common import briefing_keywords, load_briefing, write_json  # noqa: E402

# Catálogo curado offline: cada entrada cita métricas qualitativas em [0,1].
# Tags casam com os termos do briefing; metrics são propostas (não-autoritativas).
CATALOGO: list[dict[str, Any]] = [
    {
        "tool": "LangGraph",
        "url": "https://github.com/langchain-ai/langgraph",
        "license": "MIT",
        "use_case": "orquestração de StateGraph para o Anel da Forja",
        "tags": ["orquestrar", "grafo", "stategraph", "agente", "pipeline", "loop", "estado"],
        "integration_mode": "library",
        "risk_level": "low",
        "metrics": {"fit": 0.95, "licenca": 1.0, "manutencao": 0.9, "seguranca": 0.85,
                     "instalacao": 0.8, "testabilidade": 0.8, "interop_agente": 0.9},
    },
    {
        "tool": "Pydantic v2",
        "url": "https://github.com/pydantic/pydantic",
        "license": "MIT",
        "use_case": "contratos SACP tipados com extra=forbid (anti-DERIVA)",
        "tags": ["contrato", "schema", "validar", "tipado", "handoff", "modelo", "dados"],
        "integration_mode": "library",
        "risk_level": "low",
        "metrics": {"fit": 0.9, "licenca": 1.0, "manutencao": 0.95, "seguranca": 0.9,
                     "instalacao": 0.9, "testabilidade": 0.9, "interop_agente": 0.7},
    },
    {
        "tool": "Langfuse",
        "url": "https://github.com/langfuse/langfuse",
        "license": "MIT",
        "use_case": "observabilidade por span do Anel (custo/veredito por ato)",
        "tags": ["observabilidade", "tracing", "custo", "span", "métrica", "monitorar"],
        "integration_mode": "api",
        "risk_level": "medium",
        "metrics": {"fit": 0.8, "licenca": 1.0, "manutencao": 0.85, "seguranca": 0.7,
                     "instalacao": 0.7, "testabilidade": 0.7, "interop_agente": 0.8},
    },
    {
        "tool": "pytest",
        "url": "https://github.com/pytest-dev/pytest",
        "license": "MIT",
        "use_case": "Lei do Élenchos: testes verdes como evidência verificável",
        "tags": ["teste", "verificar", "refutar", "evidência", "qa", "validar"],
        "integration_mode": "cli",
        "risk_level": "low",
        "metrics": {"fit": 0.85, "licenca": 1.0, "manutencao": 0.9, "seguranca": 0.95,
                     "instalacao": 0.95, "testabilidade": 1.0, "interop_agente": 0.6},
    },
    {
        "tool": "Playwright",
        "url": "https://github.com/microsoft/playwright",
        "license": "Apache-2.0",
        "use_case": "render determinístico HTML/CSS → PNG/PDF quando há saída visual",
        "tags": ["render", "html", "png", "pdf", "visual", "screenshot", "imagem"],
        "integration_mode": "cli",
        "risk_level": "medium",
        "metrics": {"fit": 0.7, "licenca": 0.9, "manutencao": 0.85, "seguranca": 0.7,
                     "instalacao": 0.6, "testabilidade": 0.7, "interop_agente": 0.6},
    },
    {
        "tool": "ripgrep",
        "url": "https://github.com/BurntSushi/ripgrep",
        "license": "MIT",
        "use_case": "varredura rápida de código/fontes para HOUND (contexto mínimo)",
        "tags": ["buscar", "grep", "código", "varredura", "contexto", "fonte"],
        "integration_mode": "cli",
        "risk_level": "low",
        "metrics": {"fit": 0.65, "licenca": 1.0, "manutencao": 0.85, "seguranca": 0.95,
                     "instalacao": 0.9, "testabilidade": 0.8, "interop_agente": 0.7},
    },
    {
        "tool": "jsonschema",
        "url": "https://github.com/python-jsonschema/jsonschema",
        "license": "MIT",
        "use_case": "validação de payloads SACP contra JSON Schema",
        "tags": ["schema", "json", "validar", "contrato", "payload"],
        "integration_mode": "library",
        "risk_level": "low",
        "metrics": {"fit": 0.75, "licenca": 1.0, "manutencao": 0.8, "seguranca": 0.9,
                     "instalacao": 0.9, "testabilidade": 0.85, "interop_agente": 0.6},
    },
    {
        "tool": "MCP (Model Context Protocol)",
        "url": "https://github.com/modelcontextprotocol",
        "license": "MIT",
        "use_case": "exposição de conectores como ferramentas neutras para runtimes",
        "tags": ["mcp", "conector", "ferramenta", "runtime", "integrar", "portável"],
        "integration_mode": "mcp",
        "risk_level": "medium",
        "metrics": {"fit": 0.7, "licenca": 1.0, "manutencao": 0.8, "seguranca": 0.75,
                     "instalacao": 0.7, "testabilidade": 0.6, "interop_agente": 1.0},
    },
]


def descobrir(briefing: dict[str, Any], limite: int = 10) -> list[dict[str, Any]]:
    """Casa termos do briefing com o catálogo e ordena por relevância lexical."""
    termos = set(briefing_keywords(briefing))
    # Acrescenta termos estruturais sempre presentes num squad FORJA.
    termos |= {"orquestrar", "contrato", "teste", "schema", "observabilidade"}
    pontuadas: list[tuple[int, dict[str, Any]]] = []
    for entrada in CATALOGO:
        relevancia = sum(
            1 for tag in entrada["tags"]
            if any(tag in t or t in tag for t in termos)
        )
        if relevancia == 0:
            continue
        cand = {k: v for k, v in entrada.items() if k != "tags"}
        cand["relevancia_lexical"] = relevancia
        cand["fit_score"] = 0.0  # preenchido por PERCEPTOR
        cand["decision"] = "pending"
        cand["evidence"] = [f"catálogo offline; relevância={relevancia}"]
        pontuadas.append((relevancia, cand))
    pontuadas.sort(key=lambda x: (-x[0], x[1]["tool"]))
    return [c for _, c in pontuadas[:limite]]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="JAZZ — descoberta offline de instrumentos.")
    ap.add_argument("--briefing", required=True)
    ap.add_argument("--out")
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args(argv)
    candidatas = descobrir(load_briefing(args.briefing), limite=args.limit)
    resultado = {
        "source": "catalogo_offline_v1",
        "count": len(candidatas),
        "candidates": candidatas,
    }
    if args.out:
        write_json(args.out, resultado)
    import json

    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
