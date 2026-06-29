#!/usr/bin/env python3
"""Auditoria de qualidade e segurança do índice.

Verifica presença do índice, integridade de citações (anchor existe na
fonte), varredura de segredos e contagens. Gera quality_report.json.
Sem LLM.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import obsidian_core as core


def audit(config_path: str | None, cli_vault: str | None) -> dict:
    config = core.load_config(config_path)
    vault = core.resolve_vault_path(config, cli_vault)
    index_dir = core.index_dir_for(vault, config)
    issues: list[str] = []

    notes_f = index_dir / "notes_index.json"
    chunks_f = index_dir / "chunks_index.json"
    if not notes_f.is_file() or not chunks_f.is_file():
        return {"go_no_go": "no-go", "issues": ["índice ausente"],
                "checked_at": core.now_iso()}

    notes = json.loads(notes_f.read_text(encoding="utf-8"))
    chunks = json.loads(chunks_f.read_text(encoding="utf-8"))

    # Amostra de verificação de âncoras de citação.
    bad_anchors = 0
    for c in chunks[:500]:
        note = vault / c["path"]
        if not note.is_file():
            issues.append(f"chunk aponta para nota inexistente: {c['path']}")
            bad_anchors += 1
            continue
        body = " ".join(note.read_text(encoding="utf-8",
                                       errors="ignore").split())
        if " ".join(c["anchor_quote"].split())[:60] not in body:
            bad_anchors += 1

    # Varredura de segredos no índice persistido.
    secret_hits = []
    for f in index_dir.glob("*.json"):
        if core.scan_secrets(f.read_text(encoding="utf-8", errors="ignore")):
            secret_hits.append(f.name)
    if secret_hits:
        issues.append(f"possível segredo em índice: {secret_hits}")

    orphans = [n["current_path"] for n in notes
               if not n["links_in"] and not n["links_out"]]
    report = {
        "checked_at": core.now_iso(),
        "vault": str(vault),
        "note_count": len(notes),
        "chunk_count": len(chunks),
        "orphans": len(orphans),
        "citation_anchor_failures": bad_anchors,
        "secret_hits": secret_hits,
        "issues": issues,
        "go_no_go": "go" if not issues and bad_anchors == 0 else "review",
    }
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="Auditoria de qualidade.")
    ap.add_argument("--config")
    ap.add_argument("--vault")
    ap.add_argument("--output")
    args = ap.parse_args()
    try:
        report = audit(args.config, args.vault)
    except Exception as exc:  # noqa: BLE001
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if report.get("go_no_go") != "no-go" else 1


if __name__ == "__main__":
    raise SystemExit(main())
