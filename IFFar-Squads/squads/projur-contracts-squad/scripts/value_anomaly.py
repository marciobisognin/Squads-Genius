#!/usr/bin/env python3
"""Detecção de anomalias de valor por mediana/IQR.

Uso: python scripts/value_anomaly.py --metadados ./saida/metadados.json --output ./saida
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import statistics
from pathlib import Path

from projur_common import read_json, write_json


def quartis(valores: list[float]) -> tuple[float, float]:
    s = sorted(valores)
    n = len(s)
    mid = n // 2
    lower = s[:mid]
    upper = s[mid + 1:] if n % 2 else s[mid:]
    q1 = statistics.median(lower) if lower else s[0]
    q3 = statistics.median(upper) if upper else s[-1]
    return q1, q3


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadados", required=True)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    out = Path(args.output) if args.output else Path(args.metadados).parent
    itens = read_json(args.metadados, {"itens": []}).get("itens", [])
    valores = [(md["id"], md["valor"]) for md in itens if md.get("valor")]

    anomalias = []
    if len(valores) >= 4:
        vals = [v for _, v in valores]
        q1, q3 = quartis(vals)
        iqr = q3 - q1
        sup = q3 + 1.5 * iqr
        inf = q1 - 1.5 * iqr
        for vid, v in valores:
            if v > sup or v < inf:
                anomalias.append({"instrumento_id": vid, "valor": v,
                                  "faixa_normal": [round(inf, 2), round(sup, 2)]})

    write_json(out / "anomalias_valor.json", {"total": len(anomalias), "itens": anomalias,
               "amostra": len(valores)})
    print(f"Anomalias de valor: {len(anomalias)} em {len(valores)} valores.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
