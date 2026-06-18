#!/usr/bin/env python3
"""Checklist heurístico das cláusulas necessárias (art. 92, Lei 14.133/2021).

Primeira passada determinística. Não é conclusão jurídica; exige revisão humana.
Uso: python scripts/check_essential_clauses.py --clausulas ./saida/clausulas.json \
        --metadados ./saida/metadados.json --output ./saida
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from projur_common import read_json, write_json

# categorias mínimas esperadas em um contrato administrativo (referencial art. 92)
ESSENCIAIS = ["objeto", "valor", "vigencia", "garantia", "sancoes", "fiscalizacao", "rescisao", "foro"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clausulas", required=True)
    ap.add_argument("--metadados", default=None)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    out = Path(args.output) if args.output else Path(args.clausulas).parent
    clausulas = read_json(args.clausulas, {"itens": []}).get("itens", [])

    por_inst: dict[str, set[str]] = {}
    for c in clausulas:
        por_inst.setdefault(c["instrumento_id"], set()).add(c["categoria"])

    resultado = []
    for inst, cats in sorted(por_inst.items()):
        presentes = [c for c in ESSENCIAIS if c in cats]
        ausentes = [c for c in ESSENCIAIS if c not in cats]
        acerto = round(len(presentes) / len(ESSENCIAIS), 2)
        resultado.append({
            "instrumento_id": inst,
            "essenciais_presentes": presentes,
            "essenciais_ausentes": ausentes,
            "cobertura": acerto,
            "base_legal": "Art. 92, Lei 14.133/2021 (referencial — verificar vigência)",
        })

    write_json(out / "clausulas_essenciais.json", {"itens": resultado})
    print(f"Checklist art. 92 aplicado a {len(resultado)} instrumento(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
