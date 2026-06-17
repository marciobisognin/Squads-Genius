#!/usr/bin/env python3
"""Segmentação do texto em cláusulas rotuladas.

Uso: python scripts/extract_clauses.py --in ./saida/evidencias/textos --output ./saida
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from projur_common import normalize_text, write_json

RE_CLAUSULA = re.compile(
    r"(cl[áa]usula\s+[A-Za-zÀ-ÿ]+)\b[\s:.\-]+(.*?)(?=cl[áa]usula\s+[A-Za-zÀ-ÿ]+\b|$)",
    re.IGNORECASE | re.DOTALL,
)

CATEGORIAS = {
    "objeto": ["objeto"],
    "valor": ["valor", "preco", "preço"],
    "vigencia": ["vigencia", "vigência", "prazo"],
    "garantia": ["garantia"],
    "sancoes": ["sancao", "sanção", "penalidade"],
    "fiscalizacao": ["fiscalizacao", "fiscalização", "gestor"],
    "rescisao": ["rescisao", "rescisão", "extincao", "extinção"],
    "foro": ["foro"],
    "lgpd": ["dados pessoais", "lgpd"],
    "anticorrupcao": ["anticorrupcao", "anticorrupção", "integridade"],
}


def categorize(rotulo: str, texto: str) -> str:
    blob = normalize_text(rotulo + " " + texto[:200])
    for cat, kws in CATEGORIAS.items():
        if any(normalize_text(k) in blob for k in kws):
            return cat
    return "outras"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="indir", required=True)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    indir = Path(args.indir)
    out = Path(args.output) if args.output else indir.parents[1]
    clausulas = []
    for f in sorted(indir.glob("*.txt")):
        texto = f.read_text(encoding="utf-8", errors="ignore")
        for i, m in enumerate(RE_CLAUSULA.finditer(texto), 1):
            rotulo = re.sub(r"\s+", " ", m.group(1)).strip()[:80]
            corpo = re.sub(r"\s+", " ", m.group(2)).strip()[:1000]
            clausulas.append({
                "id": f"{f.stem}-C{i:02d}",
                "instrumento_id": f.stem,
                "rotulo": rotulo,
                "texto": corpo,
                "categoria": categorize(rotulo, corpo),
                "essencial": False,
                "presente": True,
            })

    write_json(out / "clausulas.json", {"total": len(clausulas), "itens": clausulas})
    print(f"Segmentadas {len(clausulas)} cláusulas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
