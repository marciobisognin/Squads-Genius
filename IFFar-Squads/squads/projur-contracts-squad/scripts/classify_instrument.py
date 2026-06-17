#!/usr/bin/env python3
"""Classificação do tipo de instrumento por regras e palavras-chave.

Determinístico. Não substitui análise semântica nem revisão humana.
Uso: python scripts/classify_instrument.py --in ./saida/evidencias/textos --output ./saida
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from projur_common import normalize_text, write_json

# tipo -> (palavras_chave, peso)
TAXONOMIA = {
    "termo_aditivo": ["termo aditivo", "aditivo ao contrato", "primeiro termo aditivo"],
    "ata_registro_precos": ["ata de registro de precos", "registro de precos"],
    "termo_execucao_descentralizada": ["termo de execucao descentralizada", "ted", "descentralizacao de credito"],
    "convenio": ["convenio", "plano de trabalho", "concedente", "convenente"],
    "termo_fomento_colaboracao": ["termo de fomento", "termo de colaboracao", "organizacao da sociedade civil", "mrosc"],
    "acordo_cooperacao": ["acordo de cooperacao", "cooperacao tecnica", "sem repasse de recursos"],
    "contrato_fundacao_apoio": ["fundacao de apoio", "lei 8.958", "lei n 8.958"],
    "contrato": ["contrato", "contratante", "contratada", "clausula primeira", "objeto"],
}
ORDEM = list(TAXONOMIA.keys())  # mais específico primeiro; 'contrato' por último


def classify(texto: str) -> tuple[str, float, list[str]]:
    norm = normalize_text(texto)
    melhor, score, evid = "indefinido", 0, []
    for tipo in ORDEM:
        kws = TAXONOMIA[tipo]
        hits = [k for k in kws if k in norm]
        s = len(hits)
        if s > score:
            melhor, score, evid = tipo, s, hits
    conf = min(1.0, 0.4 + 0.2 * score) if score else 0.0
    return melhor, round(conf, 2), evid


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="indir", required=True)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    indir = Path(args.indir)
    out = Path(args.output) if args.output else indir.parents[1]
    resultados = []
    for f in sorted(indir.glob("*.txt")):
        tipo, conf, evid = classify(f.read_text(encoding="utf-8", errors="ignore"))
        resultados.append({"id": f.stem, "tipo": tipo, "confianca": conf, "evidencia": evid})

    write_json(out / "classificacao.json", {"itens": resultados})
    print(f"Classificados {len(resultados)} instrumentos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
