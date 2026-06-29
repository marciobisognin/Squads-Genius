#!/usr/bin/env python3
"""Exporta um pacote de contexto citável para outro agente.

A partir de uma consulta, monta um bundle JSON com trechos e citações
verificadas que outro agente pode consumir sem acesso direto ao vault.
Read-only. Sem LLM.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import obsidian_query as query_mod


def export_context(config_path: str | None, cli_vault: str | None,
                   question: str, top_k: int = 12) -> dict:
    result = query_mod.query(config_path, cli_vault, question,
                             top_k=top_k, with_citations=True)
    return {
        "context_for": "external_agent",
        "question": question,
        "citations": result["citations"],
        "evidence": result["evidence"],
        "has_sources": result["has_sources"],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Exporta contexto citável.")
    ap.add_argument("--config")
    ap.add_argument("--vault")
    ap.add_argument("--query", required=True)
    ap.add_argument("--top-k", type=int, default=12)
    ap.add_argument("--output")
    args = ap.parse_args()
    try:
        bundle = export_context(args.config, args.vault, args.query,
                                args.top_k)
    except Exception as exc:  # noqa: BLE001
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(bundle, ensure_ascii=False, indent=2)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
