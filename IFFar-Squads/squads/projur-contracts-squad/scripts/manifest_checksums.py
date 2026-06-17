#!/usr/bin/env python3
"""Gera e confere checksums dos artefatos da saída (reprodutibilidade).

Uso: python scripts/manifest_checksums.py --input ./saida --out ./saida/checksums.json
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from projur_common import sha256_file, write_json


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    base = Path(args.input)
    out = Path(args.out) if args.out else base / "checksums.json"
    sums = {}
    for f in sorted(base.rglob("*")):
        if f.is_file() and f.name != "checksums.json":
            sums[str(f.relative_to(base))] = sha256_file(f)

    write_json(out, {"total": len(sums), "checksums": sums})
    print(f"Checksums calculados para {len(sums)} artefatos -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
