#!/usr/bin/env python3
"""Ingestão de lote: cataloga arquivos, deduplica por hash e gera manifest.

Uso: python scripts/ingest.py --input ./entrada --output ./saida
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from projur_common import sha256_file, write_json

EXTS = {".pdf", ".docx", ".doc", ".md", ".txt"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    out = Path(args.output)
    seen: dict[str, str] = {}
    itens: list[dict] = []
    duplicatas: list[dict] = []

    for f in sorted(Path(args.input).rglob("*")):
        if not f.is_file() or f.suffix.lower() not in EXTS:
            continue
        h = sha256_file(f)
        if h in seen:
            duplicatas.append({"arquivo": str(f), "duplicata_de": seen[h]})
            continue
        seen[h] = str(f)
        itens.append({
            "id": f"INS-{len(itens)+1:04d}",
            "arquivo": str(f),
            "nome": f.name,
            "formato": f.suffix.lower().lstrip("."),
            "hash": h,
            "status": "ingerido",
        })

    manifest = {"total": len(itens), "duplicatas": duplicatas, "itens": itens}
    write_json(out / "manifest.json", manifest)
    print(f"Ingeridos {len(itens)} itens; {len(duplicatas)} duplicatas ignoradas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
