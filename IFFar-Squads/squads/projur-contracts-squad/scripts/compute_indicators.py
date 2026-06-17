#!/usr/bin/env python3
"""Indicadores de gestão: valor total, distribuição por tipo, taxa de renovação,
percentual de cláusulas fora do padrão.

Uso: python scripts/compute_indicators.py --metadados ./saida/metadados.json \
        --clausulas-essenciais ./saida/clausulas_essenciais.json \
        --alertas ./saida/alertas.json --out ./saida/indicadores.json
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from projur_common import read_json, write_json


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadados", required=True)
    ap.add_argument("--clausulas-essenciais", default=None)
    ap.add_argument("--alertas", default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    itens = read_json(args.metadados, {"itens": []}).get("itens", [])
    ess = read_json(args.clausulas_essenciais, {"itens": []}).get("itens", []) if args.clausulas_essenciais else []
    alertas = read_json(args.alertas, {"itens": []}).get("itens", []) if args.alertas else []

    total = len(itens)
    valor_total = round(sum(md.get("valor") or 0 for md in itens), 2)
    por_tipo = dict(Counter(md.get("tipo", "indefinido") for md in itens))
    aditivos = sum(1 for md in itens if md.get("tipo") == "termo_aditivo")
    contratos = sum(1 for md in itens if md.get("tipo") == "contrato") or 1
    taxa_renovacao = round(aditivos / contratos, 2)

    fora_padrao = [e for e in ess if e.get("essenciais_ausentes")]
    pct_fora = round(len(fora_padrao) / len(ess), 2) if ess else 0.0

    venc = Counter(a.get("status") for a in alertas)

    indicadores = {
        "total_instrumentos": total,
        "valor_total": valor_total,
        "por_tipo": por_tipo,
        "taxa_renovacao": taxa_renovacao,
        "pct_clausulas_fora_padrao": pct_fora,
        "vigencia": dict(venc),
    }
    write_json(args.out, indicadores)
    print(f"Indicadores: {total} instrumentos, valor total R$ {valor_total:,.2f}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
