#!/usr/bin/env python3
"""Orquestrador CLI de demonstração do Squad PCFP (pipeline determinístico).

Encadeia: RuleSet -> Calculator (engine) -> Validator -> saídas (JSON/MD/CSV-XLSX).
Não chama LLM: é o "esqueleto executável" que prova o fluxo do PRD ponta a ponta.

Uso:
  python3 run_pcfp.py --input examples/sample_input.json --outdir output
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from pcfp_rules import default_ruleset  # noqa: E402
from pcfp_engine import PostoInput, calcular_planilha  # noqa: E402
from pcfp_validator import validar, relatorio_markdown  # noqa: E402


def carregar_input(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def build_postos(data: dict) -> list:
    postos = []
    meses = int(data.get("parametros", {}).get("meses_execucao", 12))
    for p in data.get("postos", []):
        postos.append(PostoInput(
            nome=p["nome"], cbo=p.get("cbo", "0000-00"),
            quantidade=int(p.get("quantidade", 1)),
            salario_base=float(p["salario_base"]), meses_execucao=meses,
            periculosidade=bool(p.get("periculosidade", False)),
            insalubridade_grau=float(p.get("insalubridade_grau", 0.0)),
            adicional_noturno=float(p.get("adicional_noturno", 0.0)),
            vale_transporte_custo=float(p.get("vale_transporte_custo", 0.0)),
            auxilio_alimentacao=float(p.get("auxilio_alimentacao", 0.0)),
            uniformes=float(p.get("uniformes", 0.0)),
            epis=float(p.get("epis", 0.0))))
    return postos


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--outdir", default="output")
    args = ap.parse_args()

    data = carregar_input(args.input)
    params = data.get("parametros", {})
    rs = default_ruleset(
        regime=params.get("regime", "lei14133_in98"),
        municipio_uf=params.get("municipio_uf", "A_CONFIRMAR"),
        cct_id=params.get("cct_id", "A_CONFIRMAR"),
        desoneracao_folha=bool(params.get("desoneracao_folha", False)))

    postos = build_postos(data)
    planilha = calcular_planilha(postos, rs)
    rel = validar(planilha, rs,
                  piso_cct=float(params.get("piso_cct", 0.0)),
                  custo_minimo_in176=float(params.get("custo_minimo_in176", 0.0)))

    os.makedirs(args.outdir, exist_ok=True)
    with open(os.path.join(args.outdir, "planilha.json"), "w", encoding="utf-8") as fh:
        json.dump(planilha, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(args.outdir, "relatorio_validacao.json"), "w", encoding="utf-8") as fh:
        json.dump(rel, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(args.outdir, "relatorio_validacao.md"), "w", encoding="utf-8") as fh:
        fh.write(relatorio_markdown(rel))

    print(f"Valor global do contrato: R$ {planilha['valor_global_contrato']}")
    print(f"Validação: {rel['status_geral']} ({rel['go_no_go']}) — "
          f"{rel['bloqueios']} bloqueio(s), {rel['alertas']} alerta(s)")
    print(f"Saídas em: {args.outdir}/")
    return 0 if rel["bloqueios"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
