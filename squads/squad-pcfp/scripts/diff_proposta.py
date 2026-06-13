#!/usr/bin/env python3
"""Diff célula a célula entre CostSheet de referência e proposta de licitante.

Compara duas CostSheets (JSON do pcfp_core.py ou proposta normalizada pelo A2
no mesmo schema) rubrica a rubrica: diferença absoluta, percentual e
classificação verde/amarelo/vermelho por limiar — insumo do parecer de
exequibilidade do A6 (fluxo secundário do PRD, seção 3.4).

Uso:
    python3 scripts/diff_proposta.py --referencia ref.json --proposta prop.json [--limiar-amarelo 0.10 --limiar-vermelho 0.25]

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
from pathlib import Path


def indexar(cs: dict) -> dict:
    return {f"{r['modulo']}::{r['nome']}": float(r["valor"]) for r in cs.get("rubricas", [])}


def classificar(pct_abs: float, amarelo: float, vermelho: float) -> str:
    if pct_abs >= vermelho:
        return "vermelho"
    if pct_abs >= amarelo:
        return "amarelo"
    return "verde"


def diff(ref: dict, prop: dict, amarelo: float, vermelho: float) -> dict:
    iref, iprop = indexar(ref), indexar(prop)
    linhas, contagem = [], {"verde": 0, "amarelo": 0, "vermelho": 0}
    for chave in sorted(set(iref) | set(iprop)):
        vr, vp = iref.get(chave), iprop.get(chave)
        if vr is None or vp is None:
            status = "vermelho"
            linhas.append({"rubrica": chave, "referencia": vr, "proposta": vp,
                           "diferenca": None, "diferenca_pct": None, "status": status,
                           "nota": "rubrica ausente em um dos lados — verificar mapeamento ou omissão"})
        else:
            delta = round(vp - vr, 2)
            pct = abs(delta) / vr if vr else (0.0 if delta == 0 else 1.0)
            status = classificar(pct, amarelo, vermelho)
            linhas.append({"rubrica": chave, "referencia": vr, "proposta": vp,
                           "diferenca": delta, "diferenca_pct": round(pct, 4), "status": status})
        contagem[status] += 1

    tr = ref.get("totais", {}).get("preco_por_posto_mensal")
    tp = prop.get("totais", {}).get("preco_por_posto_mensal")
    total = None
    if tr and tp:
        pct = abs(tp - tr) / tr
        total = {"referencia": tr, "proposta": tp, "diferenca": round(tp - tr, 2),
                 "diferenca_pct": round(pct, 4), "status": classificar(pct, amarelo, vermelho)}

    resultado_geral = "vermelho" if contagem["vermelho"] else ("amarelo" if contagem["amarelo"] else "verde")
    return {
        "schema": "DiffExequibilidade v1 (PRD Squad PCFP)",
        "limiar_amarelo": amarelo, "limiar_vermelho": vermelho,
        "resultado_geral": resultado_geral,
        "contagem": contagem,
        "total_por_posto": total,
        "celulas": linhas,
        "observacao": "Classificação aritmética por limiar. O parecer de exequibilidade (inclusive proposta abaixo da referência) é do A6 com decisão do pregoeiro — vermelho não implica desclassificação automática.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--referencia", required=True)
    ap.add_argument("--proposta", required=True)
    ap.add_argument("--limiar-amarelo", type=float, default=0.10)
    ap.add_argument("--limiar-vermelho", type=float, default=0.25)
    ap.add_argument("--saida", default=None)
    args = ap.parse_args()
    for c in (args.referencia, args.proposta):
        if not Path(c).is_file():
            print(json.dumps({"erro": f"arquivo não encontrado: {c}"}, ensure_ascii=False)); return 2
    rel = diff(json.loads(Path(args.referencia).read_text(encoding="utf-8")),
               json.loads(Path(args.proposta).read_text(encoding="utf-8")),
               args.limiar_amarelo, args.limiar_vermelho)
    texto = json.dumps(rel, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(texto, encoding="utf-8"); print(f"diff gravado em {args.saida}")
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
