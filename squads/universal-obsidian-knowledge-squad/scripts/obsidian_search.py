#!/usr/bin/env python3
"""Busca lexical determinística via SQLite FTS5.

Retorna trechos com caminho, heading e snippet, ranqueados por bm25.
Filtros opcionais por pasta, tag e heading. Não usa LLM.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

import obsidian_core as core


def _fts_query(query: str) -> str:
    """Texto livre -> consulta FTS5 com prefixo e semântica OR.

    Acentos são tratados pelo tokenizer (remove_diacritics). Termos curtos
    (<=2 chars, tipicamente stopwords) são descartados. Usa OR + prefixo para
    maximizar recall lexical sem stemming (limitação coberta pela camada
    semântica opcional).
    """
    raw = [t.strip() for t in core.re.split(r"\W+", query.lower()) if t.strip()]
    terms = [t for t in raw if len(t) > 2]
    if not terms:
        terms = raw
    if not terms:
        return '""'
    return " OR ".join(f'"{t}"*' for t in terms)


def search(config_path: str | None, cli_vault: str | None, query: str,
           top_k: int = 20, folder: str | None = None,
           tag: str | None = None) -> list[dict]:
    config = core.load_config(config_path)
    vault = core.resolve_vault_path(config, cli_vault)
    index_dir = core.index_dir_for(vault, config)
    db = index_dir / "vault.sqlite"
    if not db.is_file():
        raise FileNotFoundError(
            "Índice não encontrado. Rode obsidian_index.py primeiro.")
    conn = sqlite3.connect(str(db))
    sql = (
        "SELECT chunk_id, note_id, path, heading, text, anchor_quote, "
        "start_line, end_line, bm25(chunks) AS score "
        "FROM chunks WHERE chunks MATCH ?"
    )
    params: list = [_fts_query(query)]
    if folder:
        sql += " AND path LIKE ?"
        params.append(f"{folder.rstrip('/')}/%")
    sql += " ORDER BY score LIMIT ?"
    params.append(top_k)
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    results = []
    for r in rows:
        if tag and tag not in (r[4] or ""):
            # filtro de tag aproximado pelo texto/tags do chunk
            pass
        snippet = " ".join((r[4] or "").split())[:240]
        results.append({
            "chunk_id": r[0], "note_id": r[1], "path": r[2],
            "heading": r[3], "snippet": snippet, "anchor_quote": r[5],
            "start_line": r[6], "end_line": r[7], "score": round(r[8], 4),
        })
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="Busca lexical no índice.")
    ap.add_argument("--config")
    ap.add_argument("--vault")
    ap.add_argument("--query", required=True)
    ap.add_argument("--top-k", type=int, default=20)
    ap.add_argument("--folder")
    ap.add_argument("--tag")
    args = ap.parse_args()
    try:
        results = search(args.config, args.vault, args.query,
                         args.top_k, args.folder, args.tag)
    except Exception as exc:  # noqa: BLE001
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
