#!/usr/bin/env python3
"""Triagem formal determinística de propostas submetidas a edital de fomento.

Lê o edital (regras, documentação exigida, limite de bolsas por orientador) e
as propostas submetidas (JSON) e classifica cada proposta como apta, inapta
por documentação ou conflito a resolver (ex.: orientador acima do limite de
bolsas do edital). Nunca avalia mérito científico/técnico.

Uso:
    python3 scripts/triagem_propostas.py --edital caminho/edital.json --propostas caminho/propostas.json

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def triar(edital: dict, propostas: list[dict]) -> dict:
    documentacao_exigida = set(edital.get("documentacao_exigida", []))
    limite_bolsas_por_orientador = edital.get("limite_bolsas_por_orientador")

    contagem_por_orientador = Counter(p.get("orientador") for p in propostas)

    resultados = []
    for proposta in propostas:
        proposta_id = proposta.get("id")
        orientador = proposta.get("orientador")
        documentos_entregues = set(proposta.get("documentos_entregues", []))
        documentos_ausentes = sorted(documentacao_exigida - documentos_entregues)

        conflitos = []
        if limite_bolsas_por_orientador is not None and contagem_por_orientador[orientador] > limite_bolsas_por_orientador:
            conflitos.append({
                "motivo": "orientador_acima_do_limite_de_bolsas",
                "propostas_do_orientador": contagem_por_orientador[orientador],
                "limite_do_edital": limite_bolsas_por_orientador,
            })

        if documentos_ausentes:
            classificacao = "inapta por documentação"
        elif conflitos:
            classificacao = "conflito a resolver"
        else:
            classificacao = "apta"

        resultados.append({
            "id": proposta_id,
            "orientador": orientador,
            "documentos_ausentes": documentos_ausentes,
            "conflitos": conflitos,
            "classificacao": classificacao,
        })

    bloqueante = any(r["classificacao"] != "apta" for r in resultados)

    return {
        "total_propostas": len(propostas),
        "resultados": resultados,
        "gate_triagem_documental_completa": "liberado" if not bloqueante else "bloqueado",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--edital", required=True, help="arquivo JSON com regras do edital")
    ap.add_argument("--propostas", required=True, help="arquivo JSON com a lista de propostas submetidas")
    ap.add_argument("--saida", default=None, help="arquivo JSON de saída (padrão: stdout)")
    args = ap.parse_args()

    caminho_edital = Path(args.edital)
    caminho_propostas = Path(args.propostas)
    for caminho in (caminho_edital, caminho_propostas):
        if not caminho.is_file():
            print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False))
            return 2

    try:
        edital = json.loads(caminho_edital.read_text(encoding="utf-8"))
        propostas = json.loads(caminho_propostas.read_text(encoding="utf-8")).get("propostas", [])
    except json.JSONDecodeError as e:
        print(json.dumps({"erro": f"JSON inválido: {e}"}, ensure_ascii=False))
        return 2

    resultado = triar(edital, propostas)
    saida = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(saida, encoding="utf-8")
        print(f"resultado gravado em {args.saida}")
    else:
        print(saida)
    return 0 if resultado["gate_triagem_documental_completa"] == "liberado" else 1


if __name__ == "__main__":
    sys.exit(main())
