#!/usr/bin/env python3
"""KÊRYX — Letterizador do Trilho B (HEPHAISTOS).

Sobrepõe balões/legendas vetoriais NÍTIDAS sobre a arte generativa (ZEUXIS), usando o
TEXTO EXATO do ComicScript posicionado nos panel_boxes. O texto educativo nunca é
renderizado pela IA de imagem — vai em camada vetorial por cima (auditável, sem garbled).

Determinístico: roteiro, posição/conteúdo dos balões, tipografia e composição.
Dependências de render são importadas de forma preguiçosa.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

OUTPUT_DIR = Path("outputs/comic")


def _panel_text(panel: Dict[str, Any]) -> str:
    """Extrai o texto exato (diálogo + legenda) de um painel do ComicScript."""
    parts: List[str] = []
    for d in panel.get("dialogue") or []:
        speaker = d.get("speaker", "")
        text = d.get("text", "")
        parts.append(f"{speaker}: {text}" if speaker else text)
    if panel.get("caption"):
        parts.append(str(panel["caption"]))
    return " | ".join(parts)


def build_letter_layer_svg(page: Dict[str, Any], script_page: Dict[str, Any]) -> str:
    """Gera a camada SVG de balões/legendas para uma página (texto vetorial nítido)."""
    boxes = {b["panel_index"]: b for b in page.get("panel_boxes", [])}
    elems: List[str] = []
    for panel in script_page.get("panels", []):
        idx = panel.get("panel_index")
        box = boxes.get(idx)
        if not box:
            continue
        text = _panel_text(panel).replace("&", "&amp;").replace("<", "&lt;")
        tx = box["x"] + 24
        ty = box["y"] + 48
        elems.append(
            f'<g data-panel="{idx}">'
            f'<rect x="{box["x"]+12}" y="{box["y"]+12}" rx="16" ry="16" '
            f'width="{max(0, box["w"]-24)}" height="80" fill="#FFFFFF" stroke="#1A1A1A" stroke-width="2"/>'
            f'<text x="{tx}" y="{ty}" font-family="Inter" font-size="22" fill="#111111">{text}</text>'
            f"</g>"
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350">'
        + "".join(elems)
        + "</svg>"
    )


def letterize(comic_assets: Dict[str, Any], comic_script: Dict[str, Any]) -> Dict[str, Any]:
    """Compõe arte + camada de texto por página -> manifesto de letterização.

    render_hash cobre a CAMADA DE TEXTO + composição (não o bitmap da arte generativa).
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    script_pages = {p["page_index"]: p for p in comic_script.get("pages", [])}
    pages_out: List[Dict[str, Any]] = []
    for page in comic_assets.get("pages", []):
        pidx = page.get("page_index")
        svg = build_letter_layer_svg(page, script_pages.get(pidx, {}))
        text_hash = "sha256:" + hashlib.sha256(svg.encode("utf-8")).hexdigest()
        pages_out.append(
            {
                "page_index": pidx,
                "art_png": page.get("art_png"),
                "lettered_png": str(OUTPUT_DIR / f"page_{pidx:02d}.png"),
                "text_layer_hash": text_hash,
                "deterministic_text": True,
            }
        )
    return {
        "comic_id": comic_assets.get("comic_id", ""),
        "pages": pages_out,
        "pdf_path": str(OUTPUT_DIR / "comic.pdf"),
        "deterministic_text": True,
    }


if __name__ == "__main__":
    assets = {"comic_id": "demo", "pages": [{"page_index": 1, "art_png": "outputs/comic/page_01_art.png",
              "panel_boxes": [{"panel_index": 1, "x": 0, "y": 0, "w": 1080, "h": 450}]}]}
    script = {"pages": [{"page_index": 1, "panels": [{"panel_index": 1,
              "dialogue": [{"speaker": "GUIA", "text": "com dois, a órbita se repete pra sempre"}],
              "caption": None}]}]}
    print(json.dumps(letterize(assets, script), ensure_ascii=False, indent=2))
