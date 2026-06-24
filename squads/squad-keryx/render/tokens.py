#!/usr/bin/env python3
"""KÊRYX — Design system tokens (fonte única da verdade visual).

Calibrado a partir do padrão de referência (PRD seção 8). Centraliza canvas,
grid, tipografia, cores, ritmo vertical e acentos por tema. HEPHAISTOS e KANON
consomem estes tokens; o estilo baoyu modula a ESTÉTICA, nunca quebra a IDENTIDADE.

Determinístico, sem dependências externas. Pode ser importado ou executado:

    python3 render/tokens.py            # imprime os tokens em JSON
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class Canvas:
    width: int = 1080
    height: int = 1350          # 4:5
    margin: int = 72
    columns: int = 2
    gutter: int = 64
    divider_px: float = 1.5
    divider_color: str = "#1A1A1A"
    divider_opacity: float = 0.18
    branding_corner: str = "top-right"
    branding_size: int = 96


@dataclass(frozen=True)
class TypeRole:
    family: str
    weight: int
    size_min: int
    size_max: int
    case: str
    color: str


@dataclass(frozen=True)
class Typography:
    title: TypeRole = field(default_factory=lambda: TypeRole("Poppins", 800, 40, 46, "uppercase", "#111111"))
    header: TypeRole = field(default_factory=lambda: TypeRole("Poppins", 700, 24, 28, "uppercase", "#111111"))
    bullet: TypeRole = field(default_factory=lambda: TypeRole("Inter", 400, 19, 23, "sentence", "#2B2B2B"))
    bullet_marker_color: str = "#BDBDBD"
    bullet_marker_size: int = 8


@dataclass(frozen=True)
class Colors:
    bg: str = "#FFFFFF"
    bg_offwhite: str = "#FAFAF8"
    ink: str = "#111111"
    body: str = "#2B2B2B"
    muted: str = "#BDBDBD"


@dataclass(frozen=True)
class VerticalRhythm:
    space_title_to_first_header: int = 40
    space_between_sections: int = 36
    space_header_to_bullets: int = 16
    bullet_line_height: float = 1.35
    space_between_bullets: int = 12


# Acentos sugeridos por tema (APELLES escolhe; default por domínio).
ACCENTS_BY_THEME: Dict[str, str] = {
    "bateria": "#3FB950",
    "sapo": "#34A853",
    "calendario": "#E5484D",
    "tecnologia": "#2D6BDA",
    "produtividade": "#3FB950",
    "gestao_vida": "#F2C14E",
    "livros": "#8B5CF6",
}

# Faixa permitida de auto-fit para bullets (KANON).
BULLET_FONT_RANGE: List[int] = [19, 20, 21, 22, 23]

# Fontes embutidas no build (sem rede em runtime -> determinismo).
EMBEDDED_FONTS: List[str] = ["Poppins-Bold", "Poppins-SemiBold", "Inter-Regular", "NotoEmoji"]


@dataclass(frozen=True)
class Tokens:
    canvas: Canvas = field(default_factory=Canvas)
    typography: Typography = field(default_factory=Typography)
    colors: Colors = field(default_factory=Colors)
    rhythm: VerticalRhythm = field(default_factory=VerticalRhythm)
    accents: Dict[str, str] = field(default_factory=lambda: dict(ACCENTS_BY_THEME))
    bullet_font_range: List[int] = field(default_factory=lambda: list(BULLET_FONT_RANGE))
    embedded_fonts: List[str] = field(default_factory=lambda: list(EMBEDDED_FONTS))


def default_tokens() -> Tokens:
    return Tokens()


def accent_for(theme_or_domain: str) -> str:
    """Retorna o acento do tema/domínio, com fallback para o acento de tecnologia."""
    return ACCENTS_BY_THEME.get(theme_or_domain, ACCENTS_BY_THEME["tecnologia"])


def to_dict() -> dict:
    return asdict(default_tokens())


if __name__ == "__main__":
    print(json.dumps(to_dict(), ensure_ascii=False, indent=2))
