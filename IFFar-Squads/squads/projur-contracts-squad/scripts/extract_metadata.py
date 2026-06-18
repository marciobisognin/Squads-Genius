#!/usr/bin/env python3
"""Extração de metadados: número, partes, objeto, valor, vigência, base legal.

Heurístico e determinístico (regex). Separa observado de inferido.
Uso: python scripts/extract_metadata.py --in ./saida/evidencias/textos \
        --classificacao ./saida/classificacao.json --output ./saida
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from projur_common import parse_date_br, parse_money_br, read_json, write_json

RE_NUMERO = re.compile(r"n[ºo°.]?\s*([0-9]{1,5}[/.-][0-9]{2,4})", re.IGNORECASE)
RE_CNPJ = re.compile(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}")
RE_CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
RE_VALOR = re.compile(r"R\$\s*[\d.]+,\d{2}")
RE_DATA = re.compile(r"\d{2}/\d{2}/\d{4}")
RE_LEI = re.compile(r"lei\s*(?:n[ºo°.]?\s*)?\d{1,2}\.?\d{3}(?:/\d{4})?", re.IGNORECASE)
RE_OBJETO = re.compile(r"objeto[:\s]+(.{20,240}?)(?:\.|cl[áa]usula)", re.IGNORECASE | re.DOTALL)


def extract(texto: str) -> dict:
    numero = RE_NUMERO.search(texto)
    valores = [parse_money_br(v) for v in RE_VALOR.findall(texto)]
    valores = [v for v in valores if v]
    datas = [parse_date_br(d) for d in RE_DATA.findall(texto)]
    datas = sorted(d for d in datas if d)
    objeto = RE_OBJETO.search(texto)
    base_legal = sorted({m.group(0).strip() for m in RE_LEI.finditer(texto)})
    docs = RE_CNPJ.findall(texto) + RE_CPF.findall(texto)
    return {
        "numero": numero.group(1) if numero else None,
        "objeto": re.sub(r"\s+", " ", objeto.group(1)).strip() if objeto else None,
        "valor": max(valores) if valores else None,
        "vigencia_inicio": datas[0] if datas else None,
        "vigencia_fim": datas[-1] if len(datas) > 1 else None,
        "base_legal": base_legal,
        "documentos_partes": sorted(set(docs)),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="indir", required=True)
    ap.add_argument("--classificacao", default=None)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    indir = Path(args.indir)
    out = Path(args.output) if args.output else indir.parents[1]
    cls = {i["id"]: i for i in read_json(args.classificacao, {"itens": []}).get("itens", [])} if args.classificacao else {}

    itens = []
    for f in sorted(indir.glob("*.txt")):
        md = extract(f.read_text(encoding="utf-8", errors="ignore"))
        md["id"] = f.stem
        md["tipo"] = cls.get(f.stem, {}).get("tipo", "indefinido")
        md["origem"] = f.name
        itens.append(md)

    write_json(out / "metadados.json", {"itens": itens})
    print(f"Metadados extraídos de {len(itens)} instrumentos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
