#!/usr/bin/env python3
"""Dicionário de cláusulas reutilizáveis: agrupa por categoria e amostra textos.

Uso: python scripts/build_dictionary.py --clausulas ./saida/clausulas.json \
        --out ./saida/dicionario_clausulas.json
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from projur_common import read_json, write_json


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clausulas", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    itens = read_json(args.clausulas, {"itens": []}).get("itens", [])
    dic: dict[str, dict] = {}
    for c in itens:
        cat = c["categoria"]
        d = dic.setdefault(cat, {"categoria": cat, "ocorrencias": 0, "amostras": []})
        d["ocorrencias"] += 1
        if len(d["amostras"]) < 3 and c.get("texto"):
            d["amostras"].append({"instrumento_id": c["instrumento_id"], "rotulo": c["rotulo"],
                                  "trecho": c["texto"][:300]})

    write_json(args.out, {"categorias": sorted(dic.values(), key=lambda x: -x["ocorrencias"])})
    print(f"Dicionário gerado com {len(dic)} categorias de cláusula -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
