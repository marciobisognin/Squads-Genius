#!/usr/bin/env python3
"""Normalização e validação das partes (CNPJ/CPF por dígito verificador).

Uso: python scripts/normalize_parties.py --in ./saida/metadados.json --output ./saida
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from projur_common import classify_document, read_json, write_json


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", required=True)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    data = read_json(args.infile, {"itens": []})
    out = Path(args.output) if args.output else Path(args.infile).parent

    itens = []
    invalidos = 0
    for md in data.get("itens", []):
        partes = []
        for doc in md.get("documentos_partes", []):
            tipo, valido = classify_document(doc)
            if not valido:
                invalidos += 1
            partes.append({
                "nome_razao_social": "(extrair na revisão)",
                "documento": doc,
                "tipo_documento": tipo,
                "papel": "parte",
                "valido": valido,
            })
        itens.append({"id": md["id"], "partes": partes})

    write_json(out / "partes.json", {"itens": itens, "documentos_invalidos": invalidos})
    print(f"Partes normalizadas; {invalidos} documento(s) inválido(s) sinalizado(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
