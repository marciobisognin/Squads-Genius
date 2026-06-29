#!/usr/bin/env python3
"""Consolidação da matriz de instrumentos em CSV e JSON.

Uso: python scripts/build_matrix.py --metadados ./saida/metadados.json \
        --partes ./saida/partes.json --alertas ./saida/alertas.json \
        --out ./saida/matriz_contratos.csv
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from projur_common import read_json, write_json

COLUNAS = ["id", "tipo", "numero", "objeto", "valor", "vigencia_inicio",
           "vigencia_fim", "status_vigencia", "n_partes", "partes_validas",
           "base_legal", "origem"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadados", required=True)
    ap.add_argument("--partes", default=None)
    ap.add_argument("--alertas", default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    itens = read_json(args.metadados, {"itens": []}).get("itens", [])
    partes = {i["id"]: i for i in read_json(args.partes, {"itens": []}).get("itens", [])} if args.partes else {}
    alertas = {i["instrumento_id"]: i for i in read_json(args.alertas, {"itens": []}).get("itens", [])} if args.alertas else {}

    linhas = []
    for md in itens:
        p = partes.get(md["id"], {}).get("partes", [])
        linhas.append({
            "id": md["id"],
            "tipo": md.get("tipo"),
            "numero": md.get("numero"),
            "objeto": md.get("objeto"),
            "valor": md.get("valor"),
            "vigencia_inicio": md.get("vigencia_inicio"),
            "vigencia_fim": md.get("vigencia_fim"),
            "status_vigencia": alertas.get(md["id"], {}).get("status"),
            "n_partes": len(p),
            "partes_validas": sum(1 for x in p if x.get("valido")),
            "base_legal": "; ".join(md.get("base_legal", [])),
            "origem": md.get("origem"),
        })

    out_csv = Path(args.out)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUNAS)
        w.writeheader()
        w.writerows(linhas)
    write_json(out_csv.with_suffix(".json"), {"colunas": COLUNAS, "linhas": linhas})
    print(f"Matriz gerada com {len(linhas)} instrumentos -> {out_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
