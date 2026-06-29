#!/usr/bin/env python3
"""Orquestrador CLI de demonstração do Squad SCRIBA (pipeline determinístico).

Encadeia: Instrument Router -> Deterministic Engine (cálculo aplicável) ->
Validator -> saídas (JSON + memória .md). Não chama LLM: é o "esqueleto
executável" que prova o fluxo do PRD ponta a ponta para os caminhos
determinísticos (cálculo e roteamento); Drafter/Doc Generator (texto da
minuta) ficam para a Fase 2+ do roadmap (ver docs/arquitetura.md).

Uso:
  python3 run_scriba.py --input examples/sample_input_reajuste.json --outdir output
  python3 run_scriba.py --input examples/sample_input_aditivo.json --outdir output
  python3 run_scriba.py --input examples/sample_input_repactuacao.json --outdir output
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from scriba_router import ContractFacts, rotear_instrumento  # noqa: E402
from scriba_engine import (  # noqa: E402
    avaliar_limites_aditivo,
    avaliar_repactuacao,
    avaliar_prorrogacao,
    calcular_provisao_mensal,
    calcular_reajuste,
    ComponenteRepactuacao,
)
from scriba_validator import validar, relatorio_markdown  # noqa: E402


def carregar_input(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _parse_data(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--outdir", default="output")
    args = ap.parse_args()

    data = carregar_input(args.input)
    facts = ContractFacts(**data.get("contract_facts", {}))
    decisao = rotear_instrumento(facts)

    calc: dict = {}
    reajuste_result = None
    limites_result = None
    repactuacao_result = None

    if "reajuste" in data:
        r = data["reajuste"]
        reajuste_result = calcular_reajuste(
            r["valor_base"], r["indice_inicial"], r["indice_final"], r.get("indice_nome", "IPCA"))
        calc["reajuste"] = reajuste_result

    if "aditivo" in data:
        a = data["aditivo"]
        limites_result = avaliar_limites_aditivo(
            a["valor_inicial_atualizado"], acrescimo=a.get("acrescimo", 0.0),
            supressao=a.get("supressao", 0.0),
            reforma_edificio_equipamento=a.get("reforma_edificio_equipamento", False))
        calc["limites_aditivo"] = limites_result

    if "repactuacao" in data:
        rp = data["repactuacao"]
        componentes = [
            ComponenteRepactuacao(
                nome=c["nome"], data_base_anterior=_parse_data(c["data_base_anterior"]),
                valor_atual=c["valor_atual"], valor_negociado=c.get("valor_negociado"))
            for c in rp.get("componentes", [])
        ]
        repactuacao_result = avaliar_repactuacao(
            componentes, _parse_data(rp["data_referencia"]),
            data_fim_vigencia=_parse_data(rp["data_fim_vigencia"]) if rp.get("data_fim_vigencia") else None,
            solicitada=rp.get("solicitada", False))
        calc["repactuacao"] = repactuacao_result

    if "conta_vinculada" in data:
        cv = data["conta_vinculada"]
        calc["conta_vinculada"] = calcular_provisao_mensal(cv["salario_base"], cv.get("modo", "conta_vinculada"))

    if "prorrogacao" in data:
        pr = data["prorrogacao"]
        calc["prorrogacao"] = avaliar_prorrogacao(pr["meses_ja_executados"], pr["meses_prorrogacao"])

    rel = validar(
        limites_result=limites_result, facts=facts, decisao=decisao,
        reajuste_result=reajuste_result, justificativa_indice=data.get("justificativa_indice"),
        repactuacao_result=repactuacao_result)

    os.makedirs(args.outdir, exist_ok=True)
    with open(os.path.join(args.outdir, "instrument_decision.json"), "w", encoding="utf-8") as fh:
        json.dump(decisao.to_dict(), fh, ensure_ascii=False, indent=2)
    with open(os.path.join(args.outdir, "calc_results.json"), "w", encoding="utf-8") as fh:
        json.dump(calc, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(args.outdir, "relatorio_validacao.json"), "w", encoding="utf-8") as fh:
        json.dump(rel, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(args.outdir, "relatorio_validacao.md"), "w", encoding="utf-8") as fh:
        fh.write(relatorio_markdown(rel))

    print(f"Instrumento: {decisao.instrument_type} — {decisao.rationale}")
    print(f"HITL Gate A necessário: {decisao.needs_hitl}")
    print(f"Validação: {rel['status_geral']} ({rel['go_no_go']}) — "
          f"{rel['bloqueios']} bloqueio(s), {rel['alertas']} alerta(s)")
    print(f"Saídas em: {args.outdir}/")
    return 0 if rel["bloqueios"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
