#!/usr/bin/env python3
"""Consulta com citações verificadas.

Recupera trechos relevantes (busca lexical) e produz citações ancoradas em
path > heading > anchor_quote, verificando que o trecho ainda existe na
nota-fonte. A SÍNTESE em prosa é responsabilidade do agente LLM
(knowledge-synthesizer); este script entrega evidência citável determinística.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import obsidian_core as core
import obsidian_search as search_mod

NO_SOURCE_MSG = ("Não encontrei fonte suficiente no vault para afirmar isso "
                 "como conhecimento do Obsidian.")


def _verify_anchor(vault: Path, path: str, anchor: str) -> bool:
    note = vault / path
    if not note.is_file() or not anchor:
        return False
    body = " ".join(note.read_text(encoding="utf-8", errors="ignore").split())
    probe = " ".join(anchor.split())[:60]
    return probe in body


def query(config_path: str | None, cli_vault: str | None, question: str,
          top_k: int = 8, with_citations: bool = True) -> dict:
    config = core.load_config(config_path)
    vault = core.resolve_vault_path(config, cli_vault)
    hits = search_mod.search(config_path, cli_vault, question, top_k=top_k)
    citations = []
    for h in hits:
        verified = _verify_anchor(vault, h["path"], h["anchor_quote"])
        citations.append({
            "path": h["path"], "heading": h["heading"],
            "anchor_quote": h["anchor_quote"],
            "start_line": h["start_line"], "end_line": h["end_line"],
            "score": h["score"], "verified": verified,
        })
    verified_citations = [c for c in citations if c["verified"]]
    return {
        "question": question,
        "has_sources": bool(verified_citations),
        "message": None if verified_citations else NO_SOURCE_MSG,
        "evidence": [{"path": h["path"], "heading": h["heading"],
                      "snippet": h["snippet"]} for h in hits],
        "citations": verified_citations if with_citations else [],
        "synthesis_note": ("A síntese textual final deve ser gerada por um "
                           "agente LLM usando apenas estas evidências."),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Consulta com citações.")
    ap.add_argument("--config")
    ap.add_argument("--vault")
    ap.add_argument("--query", required=True)
    ap.add_argument("--top-k", type=int, default=8)
    ap.add_argument("--with-citations", action="store_true", default=True)
    args = ap.parse_args()
    try:
        result = query(args.config, args.vault, args.query, args.top_k,
                       args.with_citations)
    except Exception as exc:  # noqa: BLE001
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
