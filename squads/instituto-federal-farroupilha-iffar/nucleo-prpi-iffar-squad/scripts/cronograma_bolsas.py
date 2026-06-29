#!/usr/bin/env python3
"""Acompanhamento determinístico do cronograma de bolsas concedidas.

Lê uma lista de bolsas ativas com seus prazos de mensalidades, relatórios
parciais/finais e TCR (JSON) e compara cada prazo com uma data de
referência, classificando cada bolsa como em dia, relatório próximo do
vencimento (até N dias) ou relatório em atraso.

Uso:
    python3 scripts/cronograma_bolsas.py --bolsas caminho/bolsas.json --data-referencia 2026-06-17

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

DIAS_ALERTA_VENCIMENTO = 15


def parse_data(valor: str) -> date:
    return date.fromisoformat(valor)


def classificar_bolsa(bolsa: dict, data_referencia: date) -> dict:
    pendencias_em_atraso = []
    pendencias_proximas = []

    for entrega in bolsa.get("entregas", []):
        prazo = parse_data(entrega["prazo"])
        entregue = entrega.get("entregue", False)
        if entregue:
            continue
        dias_para_prazo = (prazo - data_referencia).days
        item = {
            "tipo": entrega["tipo"],
            "prazo": entrega["prazo"],
            "dias_para_prazo": dias_para_prazo,
        }
        if dias_para_prazo < 0:
            pendencias_em_atraso.append(item)
        elif dias_para_prazo <= DIAS_ALERTA_VENCIMENTO:
            pendencias_proximas.append(item)

    if pendencias_em_atraso:
        situacao = "relatório em atraso"
    elif pendencias_proximas:
        situacao = "relatório próximo do vencimento"
    else:
        situacao = "em dia"

    return {
        "bolsa_id": bolsa.get("bolsa_id"),
        "situacao": situacao,
        "pendencias_em_atraso": pendencias_em_atraso,
        "pendencias_proximas": pendencias_proximas,
    }


def analisar(dados: dict, data_referencia: date) -> dict:
    bolsas = dados.get("bolsas", [])
    resultados = [classificar_bolsa(b, data_referencia) for b in bolsas]
    em_atraso = [r for r in resultados if r["situacao"] == "relatório em atraso"]

    return {
        "data_referencia": data_referencia.isoformat(),
        "total_bolsas": len(bolsas),
        "resultados": resultados,
        "total_em_atraso": len(em_atraso),
        "gate_cronograma_bolsas_monitorado": "liberado" if not em_atraso else "bloqueado",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bolsas", required=True, help="arquivo JSON com a lista de bolsas e seus cronogramas")
    ap.add_argument("--data-referencia", required=True, help="data de referência no formato AAAA-MM-DD")
    ap.add_argument("--saida", default=None, help="arquivo JSON de saída (padrão: stdout)")
    args = ap.parse_args()

    caminho = Path(args.bolsas)
    if not caminho.is_file():
        print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False))
        return 2
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        data_referencia = parse_data(args.data_referencia)
    except json.JSONDecodeError as e:
        print(json.dumps({"erro": f"JSON inválido: {e}"}, ensure_ascii=False))
        return 2
    except ValueError as e:
        print(json.dumps({"erro": f"data inválida: {e}"}, ensure_ascii=False))
        return 2

    resultado = analisar(dados, data_referencia)
    saida = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(saida, encoding="utf-8")
        print(f"resultado gravado em {args.saida}")
    else:
        print(saida)
    return 0 if resultado["gate_cronograma_bolsas_monitorado"] == "liberado" else 1


if __name__ == "__main__":
    sys.exit(main())
