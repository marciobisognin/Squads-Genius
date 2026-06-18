#!/usr/bin/env python3
"""Empacota todos os artefatos da saída em um ZIP reprodutível.

Uso: python scripts/package_zip.py --input ./saida --out ./saida/projur_contracts_squad_pacote.zip
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    base = Path(args.input)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(base.rglob("*")):
            if f.is_file() and f.resolve() != out.resolve():
                z.write(f, f.relative_to(base))
                n += 1
    print(f"Pacote gerado com {n} arquivos -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
