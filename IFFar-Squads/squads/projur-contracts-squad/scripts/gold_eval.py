#!/usr/bin/env python3
"""Avaliação de métricas contra o gold set (similaridade e acerto de classe).

Espera ./examples/gold/gold.json com itens {id, texto_esperado, tipo_esperado}.
Uso: python scripts/gold_eval.py --gold ./examples/gold/gold.json \
        --textos ./saida/evidencias/textos --classificacao ./saida/classificacao.json
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from projur_common import read_json, similarity, write_json


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--textos", required=True)
    ap.add_argument("--classificacao", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    gold = read_json(args.gold, {"itens": []}).get("itens", [])
    textos_dir = Path(args.textos)
    cls = {i["id"]: i for i in read_json(args.classificacao, {"itens": []}).get("itens", [])} if args.classificacao else {}

    sims, acertos, total_cls = [], 0, 0
    detalhes = []
    for g in gold:
        gid = g["id"]
        tf = textos_dir / f"{gid}.txt"
        sim = None
        if tf.exists() and g.get("texto_esperado"):
            sim = round(similarity(tf.read_text(encoding="utf-8", errors="ignore"), g["texto_esperado"]), 3)
            sims.append(sim)
        acerto = None
        if g.get("tipo_esperado") and gid in cls:
            total_cls += 1
            acerto = cls[gid]["tipo"] == g["tipo_esperado"]
            acertos += 1 if acerto else 0
        detalhes.append({"id": gid, "similaridade": sim, "tipo_ok": acerto})

    resumo = {
        "similaridade_media": round(sum(sims) / len(sims), 3) if sims else None,
        "acerto_classificacao": round(acertos / total_cls, 3) if total_cls else None,
        "n_avaliados": len(gold),
        "detalhes": detalhes,
    }
    out = Path(args.out) if args.out else textos_dir.parents[1] / "gold_eval.json"
    write_json(out, resumo)
    print(f"Gold eval: similaridade={resumo['similaridade_media']}, "
          f"acerto_classificacao={resumo['acerto_classificacao']} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
