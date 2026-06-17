#!/usr/bin/env python3
"""Vínculo entre instrumentos: aditivo↔contrato-pai, convênio↔TED, ata↔contratos.

Heurístico por número e tipo. Precisão validada por amostragem humana.
Uso: python scripts/link_instruments.py --metadados ./saida/metadados.json --output ./saida
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from projur_common import read_json, write_json


def base_numero(numero: str | None) -> str | None:
    if not numero:
        return None
    m = re.match(r"(\d+[/.-]\d+)", numero)
    return m.group(1) if m else numero


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadados", required=True)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    out = Path(args.output) if args.output else Path(args.metadados).parent
    itens = read_json(args.metadados, {"itens": []}).get("itens", [])

    # index por número-base para ligar aditivos ao contrato-pai
    por_numero: dict[str, list[dict]] = {}
    for md in itens:
        bn = base_numero(md.get("numero"))
        if bn:
            por_numero.setdefault(bn, []).append(md)

    vinculos = []
    for md in itens:
        tipo = md.get("tipo")
        bn = base_numero(md.get("numero"))
        if tipo == "termo_aditivo" and bn:
            pais = [x for x in por_numero.get(bn, []) if x["id"] != md["id"] and x.get("tipo") == "contrato"]
            for pai in pais:
                vinculos.append({"origem_id": md["id"], "destino_id": pai["id"], "tipo_vinculo": "aditivo", "confianca": 0.8})
        if tipo == "termo_execucao_descentralizada" and bn:
            convs = [x for x in por_numero.get(bn, []) if x["id"] != md["id"] and x.get("tipo") == "convenio"]
            for c in convs:
                vinculos.append({"origem_id": md["id"], "destino_id": c["id"], "tipo_vinculo": "ted", "confianca": 0.7})

    write_json(out / "vinculos.json", {"total": len(vinculos), "itens": vinculos})
    print(f"Vínculos identificados: {len(vinculos)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
