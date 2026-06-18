#!/usr/bin/env python3
"""Detecção e mascaramento de PII (LGPD): CPF, CNPJ, e-mail, telefone, conta.

Gera pii.json (achados) e textos mascarados. Nenhum PII em claro nos artefatos.
Uso: python scripts/detect_pii.py --in ./saida/evidencias/textos --output ./saida [--redact]
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from projur_common import write_json

PATTERNS = {
    "cpf": re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"),
    "cnpj": re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b"),
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "telefone": re.compile(r"\(?\d{2}\)?\s?9?\d{4}-?\d{4}\b"),
    "conta_bancaria": re.compile(r"\bag(?:[êe]ncia)?\.?\s*\d{3,5}\b.*?\bc(?:onta)?\.?\s*\d{4,12}\b", re.IGNORECASE),
}
BASE_LGPD = "Lei 13.709/2018 (LGPD) — minimização e necessidade de base legal"


def mask(s: str) -> str:
    return s[:2] + "***" if len(s) > 2 else "***"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="indir", required=True)
    ap.add_argument("--output", default=None)
    ap.add_argument("--redact", action="store_true", help="grava cópias mascaradas dos textos")
    args = ap.parse_args()

    indir = Path(args.indir)
    out = Path(args.output) if args.output else indir.parents[1]
    achados = []
    red_dir = out / "evidencias" / "textos_mascarados"
    if args.redact:
        red_dir.mkdir(parents=True, exist_ok=True)

    for f in sorted(indir.glob("*.txt")):
        texto = f.read_text(encoding="utf-8", errors="ignore")
        masked = texto
        for tipo, rx in PATTERNS.items():
            for m in rx.finditer(texto):
                achados.append({
                    "instrumento_id": f.stem,
                    "tipo_pii": tipo,
                    "trecho_mascarado": mask(m.group(0)),
                    "posicao": m.start(),
                    "base_legal_lgpd": BASE_LGPD,
                })
            masked = rx.sub(lambda mm: mask(mm.group(0)), masked)
        if args.redact:
            (red_dir / f.name).write_text(masked, encoding="utf-8")

    write_json(out / "pii.json", {"total": len(achados), "achados": achados})
    print(f"PII: {len(achados)} achado(s){' (textos mascarados gravados)' if args.redact else ''}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
