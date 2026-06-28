#!/usr/bin/env python3
"""ALPHA TRION — consolidação de aprendizado (estrato MNÉMĒ, report-only no MVP).

Fecha o Anel pela **Lei da Anámnēsis**: ao final de cada run, registra ≥1
aprendizado reutilizável (padrão, anti-padrão, template, conector ou economia)
ou justifica o descarte. No MVP é *report-only*: propõe os patches de
`knowledge/` sem escrevê-los automaticamente.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forge_common import write_json  # noqa: E402

PERGUNTAS = [
    "o que falhou nesta run?",
    "o que foi resolvido de forma reutilizável?",
    "que checklist/template/script deve nascer?",
    "que skill criar/atualizar?",
    "que padrão evitar (anti-padrão)?",
    "que economia de tokens foi identificada?",
]


def consolidar(run_state: dict[str, Any]) -> dict[str, Any]:
    """Deriva aprendizados determinísticos a partir do estado da run."""
    aprendizados: list[dict[str, Any]] = []
    cynefin = run_state.get("classificacao_cynefin", "complicated")
    autonomia = run_state.get("nivel_autonomia", "L1")

    aprendizados.append({
        "tipo": "pattern",
        "destino": "knowledge/patterns/",
        "titulo": f"Roteamento {cynefin} → {autonomia}",
        "conteudo": (
            f"Briefings classificados como '{cynefin}' roteiam para {autonomia}; "
            "registrar como padrão de decomposição de microtarefas."
        ),
    })

    ferramentas = run_state.get("ferramentas_avaliadas", [])
    incorporadas = [f for f in ferramentas if f.get("decision") in {"incorporate", "adapt"}]
    if incorporadas:
        aprendizados.append({
            "tipo": "connector",
            "destino": "knowledge/connectors/",
            "titulo": "Instrumentos aprovados nesta run",
            "conteudo": ", ".join(f["tool"] for f in incorporadas),
        })

    falhas = run_state.get("falhas", [])
    if falhas:
        aprendizados.append({
            "tipo": "anti_pattern",
            "destino": "knowledge/anti_patterns/",
            "titulo": "Falhas observadas",
            "conteudo": "; ".join(str(f.get("motivo", f)) for f in falhas[:3]),
        })

    if not aprendizados:
        return {
            "mode": "report-only",
            "perguntas": PERGUNTAS,
            "learnings": [],
            "descarte_justificado": "run trivial sem novidade reutilizável",
        }

    return {
        "mode": "report-only",
        "perguntas": PERGUNTAS,
        "learnings": aprendizados,
        "lei": "Lei da Anámnēsis — ≥1 aprendizado consolidado ou descarte explícito.",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="ALPHA TRION — consolidação de aprendizado.")
    ap.add_argument("--run", required=True, help="caminho do run_state.json")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    run_state = json.loads(Path(args.run).read_text(encoding="utf-8"))
    resultado = consolidar(run_state)
    if args.out:
        write_json(args.out, resultado)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
