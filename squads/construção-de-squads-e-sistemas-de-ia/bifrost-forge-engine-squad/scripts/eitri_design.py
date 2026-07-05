#!/usr/bin/env python3
"""Eitri Design Forge — design system original e determinístico.

O ferreiro anão Eitri forjou tesouros na fornalha de Niðavellir. Aqui forjamos um
design system ORIGINAL (paleta, tipografia, tokens) derivado de forma
determinística do nome do projeto — sem copiar marcas de terceiros: as cores
saem de um hash estável, não de qualquer identidade proprietária.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import colorsys
import hashlib
import json
from typing import Any, Dict

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."


def _hue_from(text: str) -> float:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return (int(digest[:8], 16) % 360) / 360.0


def _hex(h: float, s: float, l: float) -> str:
    r, g, b = colorsys.hls_to_rgb(h % 1.0, l, s)
    return "#{:02x}{:02x}{:02x}".format(round(r * 255), round(g * 255), round(b * 255))


def build_palette(project_name: str) -> Dict[str, str]:
    base = _hue_from(project_name)
    return {
        "primary": _hex(base, 0.62, 0.48),
        "secondary": _hex(base + 0.5, 0.55, 0.52),
        "accent": _hex(base + 0.083, 0.72, 0.55),
        "neutral_ink": "#101317",
        "neutral_paper": "#f7f8fa",
        "success": "#1f9d63",
        "warning": "#c8871a",
        "danger": "#c0392b",
    }


def design_tokens(project_name: str) -> Dict[str, Any]:
    return {
        "color": build_palette(project_name),
        "typography": {
            "font_display": "system-ui var (recomendação: Inter/Source Sans — fontes livres)",
            "font_body": "system-ui var (recomendação: Inter/Source Sans — fontes livres)",
            "scale": [0.75, 0.875, 1.0, 1.25, 1.5, 2.0, 3.0],
        },
        "radius": {"sm": 6, "md": 10, "lg": 16, "pill": 999},
        "space": [0, 4, 8, 12, 16, 24, 32, 48, 64],
        "elevation": ["none", "0 1px 2px rgba(0,0,0,.08)", "0 6px 20px rgba(0,0,0,.12)"],
    }


def generate_design_system(project_name: str) -> Dict[str, str]:
    tokens = design_tokens(project_name)
    palette = tokens["color"]
    rows = "\n".join(f"| {name} | `{value}` |" for name, value in palette.items())
    md = f"""# Design System — {project_name}

> Identidade **original**, derivada deterministicamente do nome do projeto.
> Nenhuma marca, cor de marca ou ativo de terceiros é copiado.

## Paleta
| Token | Valor |
|---|---|
{rows}

## Tipografia
- Display: {tokens['typography']['font_display']}
- Texto: {tokens['typography']['font_body']}
- Escala modular: {tokens['typography']['scale']}

## Raios, espaçamento e elevação
- Raio: {tokens['radius']}
- Espaçamento: {tokens['space']}
- Elevação: {tokens['elevation']}

---
{FOOTER}
"""
    return {
        "docs/design_system.md": md,
        "docs/design_tokens.json": json.dumps(tokens, ensure_ascii=False, indent=2) + "\n",
    }


if __name__ == "__main__":  # pragma: no cover
    import sys
    print(json.dumps(design_tokens(sys.argv[1] if len(sys.argv) > 1 else "Demo"), ensure_ascii=False, indent=2))
