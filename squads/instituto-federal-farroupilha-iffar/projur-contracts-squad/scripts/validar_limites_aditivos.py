#!/usr/bin/env python3
"""Cálculo do percentual de alteração contratual vs. limites legais (25%/50%).

Aritmética e enquadramento de limite apenas. A avaliação de justificativa,
natureza e equilíbrio econômico-financeiro é do agente, com revisão humana.
Referencial: art. 125, Lei 14.133/2021 (verificar vigência).

Uso: python scripts/validar_limites_aditivos.py --valor-original 100000 --acrescimo 30000
  ou: python scripts/validar_limites_aditivos.py --vinculos ./saida/vinculos.json --output ./saida
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from projur_common import write_json

LIMITE_PADRAO = 0.25
LIMITE_REFORMA = 0.50


def avaliar(valor_original: float, alteracao: float, reforma: bool = False) -> dict:
    limite = LIMITE_REFORMA if reforma else LIMITE_PADRAO
    pct = (alteracao / valor_original) if valor_original else 0.0
    return {
        "valor_original": valor_original,
        "alteracao": alteracao,
        "percentual": round(pct * 100, 2),
        "limite_aplicado_pct": round(limite * 100, 2),
        "dentro_do_limite": pct <= limite + 1e-9,
        "base_legal": "Art. 125, Lei 14.133/2021 (referencial — verificar vigência)",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--valor-original", type=float)
    ap.add_argument("--acrescimo", type=float)
    ap.add_argument("--reforma", action="store_true")
    ap.add_argument("--vinculos", default=None)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    if args.valor_original is not None and args.acrescimo is not None:
        res = avaliar(args.valor_original, args.acrescimo, args.reforma)
        print(res)
        return 0

    # modo lote opcional: lê vínculos de aditivos
    if args.vinculos:
        out = Path(args.output) if args.output else Path(args.vinculos).parent
        write_json(out / "aditivos_avaliacao.json", {"itens": [], "nota": "fornecer valores por aditivo para cálculo"})
        print("Modo lote: forneça valores por aditivo nos vínculos para cálculo.")
        return 0

    ap.error("informe --valor-original e --acrescimo, ou --vinculos")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
