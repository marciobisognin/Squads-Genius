#!/usr/bin/env python3
"""Cálculo determinístico de limites de alteração contratual (termos aditivos).

Compara o somatório de acréscimos/supressões com os limites legais:
- Regime Lei 14.133/2021 (art. 125): até 25% do valor inicial atualizado;
  até 50% para reforma de edifício ou de equipamento (acréscimos).
- Regime Lei 8.666/1993 (art. 65, §§1º-2º): mesmos percentuais; supressões
  acima de 25% apenas por acordo entre as partes.

O script faz aritmética e enquadramento percentual. A avaliação jurídica da
justificativa, da natureza da alteração e do equilíbrio econômico-financeiro
é do agente riscos-sobrepreco-auditor, com revisão humana.

Uso:
    python3 scripts/validar_limites_aditivos.py --valor-inicial 1000000 \
        --aditivos 150000 120000 --regime 14133 [--tipo reforma]

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys

LIMITES = {"padrao": 25.0, "reforma": 50.0}


def avaliar(valor_inicial: float, aditivos: list[float], regime: str, tipo: str) -> dict:
    if valor_inicial <= 0:
        return {"erro": "valor inicial deve ser positivo"}
    acrescimos = sum(a for a in aditivos if a > 0)
    supressoes = sum(-a for a in aditivos if a < 0)
    pct_acrescimo = round(acrescimos / valor_inicial * 100, 4)
    pct_supressao = round(supressoes / valor_inicial * 100, 4)
    limite_acrescimo = LIMITES["reforma" if tipo == "reforma" else "padrao"]
    limite_supressao = LIMITES["padrao"]

    base_legal = (
        "Lei 14.133/2021, art. 125"
        if regime == "14133"
        else "Lei 8.666/1993, art. 65, §§1º e 2º"
    )
    resultado = {
        "regime": regime,
        "base_legal": base_legal,
        "tipo_objeto": tipo,
        "valor_inicial": valor_inicial,
        "acrescimos_total": acrescimos,
        "supressoes_total": supressoes,
        "percentual_acrescimo": pct_acrescimo,
        "percentual_supressao": pct_supressao,
        "limite_acrescimo_pct": limite_acrescimo,
        "limite_supressao_pct": limite_supressao,
        "acrescimo_dentro_do_limite": pct_acrescimo <= limite_acrescimo,
        "supressao_dentro_do_limite": pct_supressao <= limite_supressao,
        "observacoes": [
            "Percentuais calculados sobre o valor inicial informado; usar o valor inicial ATUALIZADO do contrato.",
            "O enquadramento percentual não esgota a análise: verificar justificativa, motivação (LINDB art. 20), natureza da alteração e vedação ao jogo de planilha.",
            "Supressão acima do limite pode ser admitida por acordo entre as partes, conforme o regime — avaliação jurídica necessária.",
            "Resultado sujeito a revisão humana qualificada.",
        ],
    }
    return resultado


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--valor-inicial", type=float, required=True, help="valor inicial atualizado do contrato")
    ap.add_argument("--aditivos", type=float, nargs="+", required=True, help="valores dos aditivos (negativos = supressão)")
    ap.add_argument("--regime", choices=["14133", "8666"], default="14133", help="regime legal do contrato")
    ap.add_argument("--tipo", choices=["padrao", "reforma"], default="padrao", help="reforma de edifício/equipamento eleva o limite de acréscimo a 50%%")
    args = ap.parse_args()

    resultado = avaliar(args.valor_inicial, args.aditivos, args.regime, args.tipo)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0 if "erro" not in resultado else 2


if __name__ == "__main__":
    sys.exit(main())
