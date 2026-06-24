#!/usr/bin/env python3
"""Testes do validador de CarouselSpec (regras editoriais do design system).

Executável com pytest OU diretamente: `python3 tests/test_spec_validation.py`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_carousel_spec as v  # noqa: E402


def _exemplo():
    return json.loads((ROOT / "examples" / "exemplo_carousel_spec.json").read_text(encoding="utf-8"))


def test_exemplo_valido():
    report = v.validate_spec(_exemplo())
    assert report["valid"], report["issues"]


def test_titulo_sem_uppercase_reprova():
    spec = _exemplo()
    spec["slides"][0]["title"] = "como evitar o burnout"
    report = v.validate_spec(spec)
    assert not report["valid"]


def test_emoji_no_bullet_reprova():
    spec = _exemplo()
    spec["slides"][0]["columns"][0]["sections"][0]["bullets"][0] = "faça agora 🔥"
    report = v.validate_spec(spec)
    assert not report["valid"]


def test_titulo_precisa_de_um_emoji():
    spec = _exemplo()
    spec["slides"][0]["title_emoji"] = ""
    report = v.validate_spec(spec)
    assert not report["valid"]


if __name__ == "__main__":
    fns = [val for n, val in sorted(globals().items()) if n.startswith("test_") and callable(val)]
    for fn in fns:
        fn()
        print(f"ok: {fn.__name__}")
    print(f"\n{len(fns)} testes passaram.")
