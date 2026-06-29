#!/usr/bin/env python3
"""Valida um Plano de Ensino contra os campos obrigatórios do schema.

Não usa biblioteca externa de JSON Schema — faz checagem estrutural mínima
equivalente, suficiente para os campos obrigatórios de
`schemas/plano_ensino.schema.json`.

Uso:
    python3 validate_plano_ensino.py --input plano.json --report quality_report.json
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sacp_common import read_json, write_json  # noqa: E402

CAMPOS_OBRIGATORIOS = [
    "componente_id",
    "curso_id",
    "ementa",
    "objetivos",
    "metodologia",
    "conteudo_programatico",
    "avaliacao",
    "referencias",
    "cronograma",
    "status_homologacao",
]

STATUS_VALIDOS = {"rascunho", "em_revisao", "homologado", "devolvido"}


def validate(plano: dict) -> dict:
    achados = []
    for campo in CAMPOS_OBRIGATORIOS:
        if not plano.get(campo):
            achados.append({"severidade": "alta", "campo": campo, "mensagem": "campo obrigatório ausente ou vazio"})

    status = plano.get("status_homologacao")
    if status and status not in STATUS_VALIDOS:
        achados.append({"severidade": "alta", "campo": "status_homologacao", "mensagem": f"valor inválido: {status}"})

    cronograma = plano.get("cronograma") or []
    if isinstance(cronograma, list) and not cronograma:
        achados.append({"severidade": "média", "campo": "cronograma", "mensagem": "cronograma vazio"})

    if status == "homologado" and not plano.get("veredito_curricular") == "conforme":
        achados.append(
            {
                "severidade": "alta",
                "campo": "veredito_curricular",
                "mensagem": "plano marcado como homologado sem veredito 'conforme' do Guardião Curricular",
            }
        )

    severidade_alta = any(a["severidade"] == "alta" for a in achados)
    return {"valido": not severidade_alta, "achados": achados}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="Plano de Ensino (JSON).")
    ap.add_argument("--report", required=True, help="Relatório de validação (JSON).")
    args = ap.parse_args()

    plano = read_json(args.input)
    resultado = validate(plano)
    write_json(args.report, resultado)

    print(f"Validação concluída: {'OK' if resultado['valido'] else 'PENDÊNCIAS'} ({len(resultado['achados'])} achado(s)).")
    return 0 if resultado["valido"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
