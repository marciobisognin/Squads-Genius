#!/usr/bin/env python3
"""Verificação determinística de existência de citação (camada offline).

Implementa o ESQUELETO determinístico da primitiva 6.1 do PRD: cruza cada
referência contra um *cache* local (que, em produção, é alimentado por
Semantic Scholar + OpenAlex + Crossref + arXiv com TTL de 90 dias). Aqui o
cache é um JSON local, de modo que a verificação roda sem rede e sem chave de
API — ideal para CI e para reproduzir o comportamento do gate.

Regras de status (precisão sobre recall):
  - "verificada"    -> casou em >=1 índice (por DOI/arXiv exato ou título fuzzy).
  - "inexistente"   -> APENAS quando um DOI/arXiv-ID EXATO foi informado e
                       falhou em todos os índices.
  - "nao-resolvida" -> sem identificador forte e sem match de título; NÃO bloqueia
                       (caso típico de citação regional/PT-BR não-indexada).

Casamento de título: similaridade por tokens (Jaccard) como *fallback* sem
dependências; em produção, troque por RapidFuzz/sentence-transformers.

Uso:
    python3 scripts/verify_citations.py \
        --citations examples/fixtures/citations_input.json \
        --cache examples/fixtures/index_cache.json \
        [--fuzzy 0.6] [--out output/verificacao.json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

INDICES = ["semantic_scholar", "openalex", "crossref", "arxiv"]


def _norm(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", (s or "").lower()))


def _jaccard(a: str, b: str) -> float:
    ta, tb = _norm(a), _norm(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def verify_one(cit: dict, cache: list[dict], fuzzy: float) -> dict:
    doi = (cit.get("doi") or "").strip().lower()
    arxiv = (cit.get("arxiv_id") or "").strip().lower()
    titulo = cit.get("titulo", "")
    matched: list[str] = []
    best_score = 0.0

    for rec in cache:
        rec_doi = (rec.get("doi") or "").strip().lower()
        rec_arxiv = (rec.get("arxiv_id") or "").strip().lower()
        idx = rec.get("indice")
        if doi and rec_doi and doi == rec_doi:
            if idx and idx not in matched:
                matched.append(idx)
            best_score = max(best_score, 1.0)
            continue
        if arxiv and rec_arxiv and arxiv == rec_arxiv:
            if idx and idx not in matched:
                matched.append(idx)
            best_score = max(best_score, 1.0)
            continue
        score = _jaccard(titulo, rec.get("titulo", ""))
        if score >= fuzzy:
            if idx and idx not in matched:
                matched.append(idx)
            best_score = max(best_score, score)

    has_strong_id = bool(doi or arxiv)
    if matched:
        status = "verificada"
    elif has_strong_id:
        status = "inexistente"
    else:
        status = "nao-resolvida"

    return {
        "chave_citacao": cit.get("chave_citacao"),
        "titulo": titulo,
        "doi": cit.get("doi"),
        "arxiv_id": cit.get("arxiv_id"),
        "status_existencia": status,
        "indices_consultados": INDICES,
        "indices_com_match": matched,
        "fuzzy_score_titulo": round(best_score * 100, 1),
        "cache_hit": bool(matched),
        "override_humano": None,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--citations", required=True)
    ap.add_argument("--cache", required=True)
    ap.add_argument("--fuzzy", type=float, default=0.6)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    citations = json.loads(Path(args.citations).read_text(encoding="utf-8"))
    cache = json.loads(Path(args.cache).read_text(encoding="utf-8"))

    results = [verify_one(c, cache, args.fuzzy) for c in citations]
    resumo = {
        "total": len(results),
        "verificada": sum(r["status_existencia"] == "verificada" for r in results),
        "nao_resolvida": sum(r["status_existencia"] == "nao-resolvida" for r in results),
        "inexistente": sum(r["status_existencia"] == "inexistente" for r in results),
    }
    out = {"resumo": resumo, "resultados": results}

    if args.out:
        outp = Path(args.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(out, ensure_ascii=False, indent=2))
    # Gate: a presença de 'inexistente' sinaliza bloqueio (exit 1) até override humano.
    return 1 if resumo["inexistente"] else 0


if __name__ == "__main__":
    sys.exit(main())
