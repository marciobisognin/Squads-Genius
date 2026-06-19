#!/usr/bin/env python3
"""Indexador determinístico do vault Obsidian.

Varre notas Markdown, extrai metadados/links, faz chunking por heading e
grava o índice em SQLite (FTS5) + JSON. Não usa LLM. Read-only no vault.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import obsidian_core as core


def build_index(config_path: str | None, cli_vault: str | None) -> dict:
    config = core.load_config(config_path)
    vault = core.resolve_vault_path(config, cli_vault)
    vcfg = config.get("vault") or {}
    include = vcfg.get("include_patterns") or ["**/*.md"]
    exclude = vcfg.get("exclude_patterns") or [".obsidian/**"]
    default_lang = (config.get("user_profile") or {}).get("language", "und")
    index_dir = core.index_dir_for(vault, config)

    conn = core.open_index(index_dir)
    conn.execute("DELETE FROM chunks")
    notes: list[core.Note] = []
    all_chunks: list[core.Chunk] = []
    title_to_path: dict[str, str] = {}
    secret_hits: list[str] = []

    for path in core.iter_markdown_files(vault, include, exclude):
        raw = path.read_text(encoding="utf-8", errors="ignore")
        hits = core.scan_secrets(raw)
        if hits:
            secret_hits.append(path.relative_to(vault).as_posix())
            continue  # nunca indexar conteúdo com segredo aparente
        rel = path.relative_to(vault).as_posix()
        fm = core.parse_frontmatter(raw)
        body = core.strip_frontmatter(raw)
        content_sha = core._sha256(raw)
        note_id, prev = core.stable_note_id(conn, fm, rel, content_sha)
        tags = core.extract_tags(body, fm)
        headings = core.extract_headings(body)
        links_out = core.extract_wikilinks(body)
        title = core.title_from(path, fm, body)
        title_to_path[title] = rel
        note = core.Note(
            note_id=note_id, current_path=rel, previous_paths=prev,
            title=title, frontmatter=fm, tags=tags, headings=headings,
            links_out=links_out, links_in=[],
            modified_at=core.datetime.fromtimestamp(
                path.stat().st_mtime, core.timezone.utc).replace(
                microsecond=0).isoformat(),
            content_sha256=content_sha, word_count=len(body.split()),
            language=core.detect_language(fm, default_lang),
        )
        notes.append(note)
        all_chunks.extend(core.chunk_by_headings(note_id, rel, body, tags))
        conn.execute("INSERT OR REPLACE INTO registry VALUES (?,?)",
                     (content_sha, note_id))
        conn.execute("INSERT OR REPLACE INTO path_registry VALUES (?,?)",
                     (rel, note_id))

    # Resolve backlinks (links_in) por título.
    for note in notes:
        for other in notes:
            if note.current_path == other.current_path:
                continue
            for link in other.links_out:
                if title_to_path.get(link) == note.current_path \
                        or link == note.title:
                    if other.current_path not in note.links_in:
                        note.links_in.append(other.current_path)

    # Persiste notas e chunks.
    conn.execute("DELETE FROM notes")
    for n in notes:
        conn.execute(
            "INSERT OR REPLACE INTO notes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (n.note_id, n.current_path, json.dumps(n.previous_paths),
             n.title, json.dumps(n.frontmatter, ensure_ascii=False),
             json.dumps(n.tags, ensure_ascii=False),
             json.dumps(n.headings, ensure_ascii=False),
             json.dumps(n.links_out, ensure_ascii=False),
             json.dumps(n.links_in, ensure_ascii=False),
             n.modified_at, n.content_sha256, n.word_count, n.language))
    for c in all_chunks:
        conn.execute(
            "INSERT INTO chunks VALUES (?,?,?,?,?,?,?,?,?)",
            (c.chunk_id, c.note_id, c.path, c.heading, c.text,
             c.anchor_quote, c.start_line, c.end_line,
             " ".join(c.tags)))
    conn.commit()
    conn.close()
    core.dump_json_indexes(index_dir, notes, all_chunks)

    return {
        "vault": str(vault),
        "index_dir": str(index_dir),
        "notes_indexed": len(notes),
        "chunks_indexed": len(all_chunks),
        "skipped_secrets": secret_hits,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Indexa um vault Obsidian.")
    ap.add_argument("--config")
    ap.add_argument("--vault")
    args = ap.parse_args()
    try:
        result = build_index(args.config, args.vault)
    except Exception as exc:  # noqa: BLE001
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
