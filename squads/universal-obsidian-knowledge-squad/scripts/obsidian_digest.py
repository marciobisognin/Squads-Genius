#!/usr/bin/env python3
"""Digest de notas recentes (determinístico).

Lista notas modificadas nos últimos N dias, agrupadas por tag, para servir de
insumo a um resumo executivo. A redação final é tarefa do agente LLM.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import obsidian_core as core


def digest(config_path: str | None, cli_vault: str | None,
           days: int = 7) -> dict:
    config = core.load_config(config_path)
    vault = core.resolve_vault_path(config, cli_vault)
    index_dir = core.index_dir_for(vault, config)
    notes_f = index_dir / "notes_index.json"
    if not notes_f.is_file():
        raise FileNotFoundError("Índice ausente. Rode obsidian_index.py.")
    notes = json.loads(notes_f.read_text(encoding="utf-8"))
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    recent = []
    for n in notes:
        try:
            mod = datetime.fromisoformat(n["modified_at"])
        except ValueError:
            continue
        if mod >= cutoff:
            recent.append({"path": n["current_path"], "title": n["title"],
                           "tags": n["tags"], "modified_at": n["modified_at"]})
    recent.sort(key=lambda x: x["modified_at"], reverse=True)
    return {"window_days": days, "count": len(recent), "notes": recent}


def main() -> int:
    ap = argparse.ArgumentParser(description="Digest de notas recentes.")
    ap.add_argument("--config")
    ap.add_argument("--vault")
    ap.add_argument("--days", type=int, default=7)
    args = ap.parse_args()
    try:
        result = digest(args.config, args.vault, args.days)
    except Exception as exc:  # noqa: BLE001
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
