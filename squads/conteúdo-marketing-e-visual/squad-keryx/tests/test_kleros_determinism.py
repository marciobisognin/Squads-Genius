#!/usr/bin/env python3
"""Testes de determinismo da curadoria (KLEROS) e do render_hash.

Executável com pytest OU diretamente: `python3 tests/test_kleros_determinism.py`.
Não exige dependências externas.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "render"))

import kleros_curation as k  # noqa: E402
import engine  # noqa: E402


def test_curadoria_reprodutivel_mesma_seed():
    a = k.curar(n_slides=5, seed=42, mode="single_theme", output_format="infographic")
    b = k.curar(n_slides=5, seed=42, mode="single_theme", output_format="infographic")
    assert a == b, "mesma seed deve produzir o mesmo ThemePlan"


def test_curadoria_varia_com_seed():
    a = k.curar(n_slides=5, seed=1, mode="random_mix", output_format="infographic")
    b = k.curar(n_slides=5, seed=2, mode="random_mix", output_format="infographic")
    assert a["slots"] != b["slots"], "seeds diferentes devem variar (com alta probabilidade)"


def test_n_slides_respeitado():
    plan = k.curar(n_slides=7, seed=3)
    assert len(plan["slots"]) == 7


def test_anti_repeticao_exclui_topico():
    plan = k.curar(n_slides=5, seed=42, domains=["produtividade"], excluidos=["evitar_burnout"])
    assert all(s["topico"] != "evitar_burnout" for s in plan["slots"])


def test_render_hash_deterministico():
    spec = {"carousel_id": "t", "slides": [{"slide_index": 1, "title": "TESTE",
            "baoyu": {"layout": "dense-modules", "style": "minimalist"}}]}
    m1 = engine.render_carousel(spec, {}, seed=42)
    m2 = engine.render_carousel(spec, {}, seed=42)
    assert m1["slides"][0]["render_hash"] == m2["slides"][0]["render_hash"]


def test_render_hash_muda_com_seed():
    spec = {"carousel_id": "t", "slides": [{"slide_index": 1, "title": "TESTE",
            "baoyu": {"layout": "dense-modules", "style": "minimalist"}}]}
    assert engine.render_carousel(spec, {}, 1)["slides"][0]["render_hash"] != \
        engine.render_carousel(spec, {}, 2)["slides"][0]["render_hash"]


if __name__ == "__main__":
    fns = [v for n, v in sorted(globals().items()) if n.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok: {fn.__name__}")
    print(f"\n{len(fns)} testes passaram.")
