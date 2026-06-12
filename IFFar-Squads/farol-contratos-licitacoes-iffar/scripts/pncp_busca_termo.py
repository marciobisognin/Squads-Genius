#!/usr/bin/env python3
"""Busca PNCP por termo usando a API Compras.gov Dados Abertos.

Consulta contratações PNCP por período/modalidade/UF e filtra localmente pelo termo
no objeto da compra e campos textuais principais.
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
COMPRAS = ROOT / "scripts" / "compras_gov.py"


def run_json(cmd: List[str]) -> Dict[str, Any]:
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(proc.stdout)


def flatten(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def main() -> int:
    ap = argparse.ArgumentParser(description="Busca contratações PNCP por termo no objeto/campos textuais.")
    ap.add_argument("termo", help="termo de busca, ex.: copa cozinha, caneca, material permanente")
    ap.add_argument("--inicio", required=True)
    ap.add_argument("--fim", required=True)
    ap.add_argument("--modalidade", type=int, default=6, help="código de modalidade exigido pela API; default 6")
    ap.add_argument("--uf", default="RS")
    ap.add_argument("--paginas", type=int, default=3)
    ap.add_argument("--tamanho-pagina", type=int, default=10)
    ap.add_argument("--out", default="output/pncp-termo")
    args = ap.parse_args()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(COMPRAS), "contratacoes", "--inicio", args.inicio, "--fim", args.fim, "--modalidade", str(args.modalidade), "--uf", args.uf, "--paginas", str(args.paginas), "--tamanho-pagina", str(args.tamanho_pagina), "--format", "json"]
    payload = run_json(cmd)
    rows = payload.get("resultado", []) if isinstance(payload, dict) else []
    terms = [t.casefold() for t in args.termo.split() if t.strip()]
    matches = []
    for row in rows:
        hay = " ".join(flatten(row.get(k)) for k in row.keys()).casefold()
        if all(t in hay for t in terms):
            matches.append(row)
    json_path = outdir / "pncp_busca_termo.json"
    csv_path = outdir / "pncp_busca_termo.csv"
    json_path.write_text(json.dumps({"termo": args.termo, "total_consultado": len(rows), "matches": matches}, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = ["numeroControlePNCP", "modalidadeNome", "objetoCompra", "dataPublicacaoPncp", "unidadeOrgaoNomeUnidade", "unidadeOrgaoUfSigla", "valorTotalEstimado"]
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in matches:
            w.writerow({k: flatten(row.get(k)) for k in fields})
    print(json.dumps({"termo": args.termo, "total_consultado": len(rows), "matches": len(matches), "json": str(json_path), "csv": str(csv_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
