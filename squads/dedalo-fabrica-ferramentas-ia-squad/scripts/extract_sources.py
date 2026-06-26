#!/usr/bin/env python3
"""Esqueleto determinístico de extração de fontes (SKOPÓS) do DÉDALO.

Normaliza referências de fontes (vídeo/print/PDF/texto) em um esboço de SourcePackage,
marcando explicitamente as inacessíveis. A transcrição/OCR reais são plugados por
ferramentas externas (yt-dlp, ffprobe, whisper, OCR) — aqui garantimos a ESTRUTURA e a
regra de ouro: fonte inacessível é marcada, nunca inventada.

Uso:
    python3 scripts/extract_sources.py --sources video.mp4 print.png doc.pdf
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ACCESSIBLE_SUFFIXES = {".mp4", ".m4a", ".wav", ".png", ".jpg", ".jpeg", ".pdf", ".txt", ".md", ".srt", ".vtt"}


def classify_source(ref: str) -> dict:
    """Classifica uma referência como acessível (arquivo local existente) ou a verificar."""
    path = Path(ref)
    is_url = ref.startswith("http://") or ref.startswith("https://")
    if is_url:
        return {"source_ref": ref, "kind": "url", "accessible": "unknown", "note": "requer ferramenta de download/login"}
    accessible = path.is_file() and path.suffix.lower() in ACCESSIBLE_SUFFIXES
    return {
        "source_ref": ref,
        "kind": path.suffix.lower().lstrip(".") or "unknown",
        "accessible": bool(accessible),
        "note": "" if accessible else "arquivo ausente ou formato não suportado",
    }


def build_skeleton(refs: list[str]) -> dict:
    classified = [classify_source(r) for r in refs]
    inaccessible = [c["source_ref"] for c in classified if c["accessible"] is False]
    return {
        "transcripts": [],
        "key_quotes": [],
        "cited_tools": [],
        "inaccessible_sources": inaccessible,
        "classified": classified,
        "rule": "fonte inacessível é marcada, nunca inventada",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Esboça SourcePackage a partir de referências de fontes.")
    ap.add_argument("--sources", nargs="+", required=True, help="Lista de referências (arquivos ou URLs).")
    args = ap.parse_args()
    print(json.dumps(build_skeleton(args.sources), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
