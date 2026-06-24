#!/usr/bin/env python3
"""KÊRYX — Validador determinístico do CarouselSpec (regras editoriais + design system).

Confere as regras do "molho" do padrão (PRD seções 7.3 e 8.5) sem LLM:
- título UPPERCASE e exatamente 1 emoji no título; 0 emoji nos bullets;
- header de seção UPPERCASE;
- bullet em imperativo curto (<= 12 palavras como teto de segurança);
- presença de seções/bullets.

Uso:
    python3 scripts/validate_carousel_spec.py --spec caminho/spec.json
    cat spec.json | python3 scripts/validate_carousel_spec.py
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List

# Faixa de emoji simplificada (cobre os blocos mais comuns).
EMOJI_RANGES = [
    (0x1F300, 0x1FAFF),
    (0x2600, 0x27BF),
    (0x1F000, 0x1F0FF),
    (0x2B00, 0x2BFF),
]
MAX_BULLET_WORDS = 12


def count_emoji(text: str) -> int:
    n = 0
    for ch in text:
        cp = ord(ch)
        if any(lo <= cp <= hi for lo, hi in EMOJI_RANGES):
            n += 1
    return n


def validate_slide(slide: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    idx = slide.get("slide_index", "?")
    title = slide.get("title", "")
    if not title:
        issues.append(f"slide {idx}: título ausente")
    elif title != title.upper():
        issues.append(f"slide {idx}: título não está em UPPERCASE")

    emoji_field = slide.get("title_emoji", "")
    title_emojis = count_emoji(title) + count_emoji(emoji_field)
    if title_emojis != 1:
        issues.append(f"slide {idx}: título deve ter exatamente 1 emoji (encontrado {title_emojis})")

    cols = slide.get("columns", [])
    if not cols:
        issues.append(f"slide {idx}: sem colunas")
    for col in cols:
        for sec in col.get("sections", []):
            header = sec.get("header", "")
            if not header:
                issues.append(f"slide {idx}: seção sem header")
            elif header != header.upper():
                issues.append(f"slide {idx}: header '{header}' não está em UPPERCASE")
            bullets = sec.get("bullets", [])
            if not bullets:
                issues.append(f"slide {idx}: seção '{header}' sem bullets")
            for b in bullets:
                if count_emoji(b) > 0:
                    issues.append(f"slide {idx}: bullet com emoji ('{b[:30]}...')")
                if len(b.split()) > MAX_BULLET_WORDS:
                    issues.append(f"slide {idx}: bullet longo (> {MAX_BULLET_WORDS} palavras): '{b[:30]}...'")
    return issues


def validate_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[str] = []
    if "slides" not in spec or not spec["slides"]:
        issues.append("spec sem slides")
    n = spec.get("n_slides")
    slides = spec.get("slides", [])
    if n is not None and n != len(slides):
        issues.append(f"n_slides={n} difere do número de slides ({len(slides)})")
    for slide in slides:
        issues.extend(validate_slide(slide))
    return {"valid": not issues, "issue_count": len(issues), "issues": issues}


def main() -> int:
    ap = argparse.ArgumentParser(description="Valida um CarouselSpec contra as regras editoriais.")
    ap.add_argument("--spec", help="Arquivo JSON do CarouselSpec. Se ausente, lê de stdin.")
    args = ap.parse_args()
    raw = open(args.spec, encoding="utf-8").read() if args.spec else sys.stdin.read()
    spec = json.loads(raw)
    report = validate_spec(spec)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
