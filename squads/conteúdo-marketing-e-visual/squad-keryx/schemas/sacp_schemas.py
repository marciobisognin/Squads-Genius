#!/usr/bin/env python3
"""KÊRYX — Contratos de dados SACP (handoffs entre agentes).

Todos os handoffs são JSON validado. Quando Pydantic está disponível, usa BaseModel;
caso contrário, cai para dataclasses (mantém o arquivo importável/auditável sem deps).

Artefatos: CarouselBrief, ThemePlan, ContentDraft, CarouselSpec, RenderManifest,
QAVisual, QAContent, ComicScript, CharacterSheet, ComicAssets.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

try:  # caminho preferido
    from pydantic import BaseModel, Field

    _PYDANTIC = True
except Exception:  # fallback determinístico sem dependências
    _PYDANTIC = False
    from dataclasses import dataclass, field

    def Field(default=None, **_kwargs):  # type: ignore
        return default


if _PYDANTIC:

    class BaoyuInfographic(BaseModel):
        layout: str = "dense-modules"
        style: str = "minimalist"
        palette: Optional[List[str]] = None

    class BaoyuComic(BaseModel):
        art: str = "ligne-claire"
        tone: str = "warm"
        layout: str = "standard"
        preset: Optional[str] = "ohmsha"

    class BaoyuStyle(BaseModel):
        infographic: Optional[BaoyuInfographic] = None
        comic: Optional[BaoyuComic] = None

    class CarouselBrief(BaseModel):
        request_id: str
        n_slides: int = Field(..., ge=1)
        output_format: str = "auto"          # infographic | comic | auto
        mode: str = "single_theme"           # single_theme | combined | random_mix
        domains: List[str] = Field(default_factory=lambda: ["tecnologia", "produtividade", "gestao_vida", "livros"])
        seed: int = 42
        tom: str = "default"
        branding_slot: str = "user_logo_v1"
        cynefin_class: str = "clear"
        baoyu_style: Optional[BaoyuStyle] = None

    class ThemeSlot(BaseModel):
        slide_index: int
        dominio: str
        topico: str
        cotidiano_hook: str
        subdominio: Optional[str] = None

    class ThemePlan(BaseModel):
        request_id: str
        output_format: str = "infographic"
        slots: List[ThemeSlot]
        anti_repeticao: Dict[str, Any] = Field(default_factory=dict)

    class Section(BaseModel):
        header: str
        bullets: List[str]

    class Column(BaseModel):
        sections: List[Section]

    class Slide(BaseModel):
        slide_index: int
        title: str
        title_emoji: Optional[str] = None
        layout: str = "two_column"
        baoyu: Optional[BaoyuInfographic] = None
        accent_color: Optional[str] = None
        branding_slot: Optional[str] = None
        columns: List[Column] = Field(default_factory=list)

    class CarouselSpec(BaseModel):
        carousel_id: str
        n_slides: int
        slides: List[Slide]

    class RenderSlide(BaseModel):
        slide_index: int
        png_path: str
        width: int = 1080
        height: int = 1350
        render_hash: str

    class RenderManifest(BaseModel):
        carousel_id: str
        slides: List[RenderSlide]
        pdf_path: str
        fonts_used: List[str] = Field(default_factory=list)
        deterministic: bool = True

    class QAVisual(BaseModel):
        slide_index: int
        overflow: bool = False
        min_contrast_ratio: float = 0.0
        grid_ok: bool = True
        issues: List[str] = Field(default_factory=list)
        fix_request: Optional[Dict[str, Any]] = None

    class QAContent(BaseModel):
        slide_index: int
        factual_flags: List[str] = Field(default_factory=list)
        cliche_flags: List[str] = Field(default_factory=list)
        sycophancy_flags: List[str] = Field(default_factory=list)
        verdict: str = "pass"  # pass | revise
        fix_request: Optional[Dict[str, Any]] = None

    class Panel(BaseModel):
        panel_index: int
        shot: str = "wide"
        scene_description: str
        metaphor: Optional[str] = None
        dialogue: List[Dict[str, str]] = Field(default_factory=list)
        caption: Optional[str] = None

    class ComicPage(BaseModel):
        page_index: int
        visual_thesis: str
        panels: List[Panel]

    class ComicScript(BaseModel):
        comic_id: str
        topic: str
        premise: str
        pages: List[ComicPage]
        text_layer_only: bool = True

    class Character(BaseModel):
        id: str
        name: str
        visual_identity: str
        consistency_tokens: List[str]

    class CharacterSheet(BaseModel):
        comic_id: str
        art_style: str = "ligne-claire"
        characters: List[Character]
        style_bible: Dict[str, Any] = Field(default_factory=dict)
        character_sheet_png: Optional[str] = None

    class PanelBox(BaseModel):
        panel_index: int
        x: int
        y: int
        w: int
        h: int

    class ComicAssetPage(BaseModel):
        page_index: int
        art_png: str
        image_backend: Optional[str] = None
        seed: Optional[int] = None
        deterministic_pixels: bool = False
        panel_boxes: List[PanelBox] = Field(default_factory=list)

    class ComicAssets(BaseModel):
        comic_id: str
        pages: List[ComicAssetPage]
        needs_letterizing: bool = True

else:  # ----- Fallback dataclasses (sem validação rica, mas importável) -----

    @dataclass
    class CarouselBrief:  # type: ignore
        request_id: str
        n_slides: int
        output_format: str = "auto"
        mode: str = "single_theme"
        domains: List[str] = field(default_factory=lambda: ["tecnologia", "produtividade", "gestao_vida", "livros"])
        seed: int = 42
        tom: str = "default"
        branding_slot: str = "user_logo_v1"
        cynefin_class: str = "clear"
        baoyu_style: Optional[Dict[str, Any]] = None

    @dataclass
    class ThemePlan:  # type: ignore
        request_id: str
        slots: List[Dict[str, Any]]
        output_format: str = "infographic"
        anti_repeticao: Dict[str, Any] = field(default_factory=dict)

    @dataclass
    class CarouselSpec:  # type: ignore
        carousel_id: str
        n_slides: int
        slides: List[Dict[str, Any]]

    @dataclass
    class RenderManifest:  # type: ignore
        carousel_id: str
        slides: List[Dict[str, Any]]
        pdf_path: str
        fonts_used: List[str] = field(default_factory=list)
        deterministic: bool = True

    @dataclass
    class ComicScript:  # type: ignore
        comic_id: str
        topic: str
        premise: str
        pages: List[Dict[str, Any]]
        text_layer_only: bool = True

    @dataclass
    class CharacterSheet:  # type: ignore
        comic_id: str
        characters: List[Dict[str, Any]]
        art_style: str = "ligne-claire"
        style_bible: Dict[str, Any] = field(default_factory=dict)
        character_sheet_png: Optional[str] = None

    @dataclass
    class ComicAssets:  # type: ignore
        comic_id: str
        pages: List[Dict[str, Any]]
        needs_letterizing: bool = True


__all__ = [
    "CarouselBrief", "ThemePlan", "CarouselSpec", "RenderManifest",
    "ComicScript", "CharacterSheet", "ComicAssets",
]

if __name__ == "__main__":
    print("Pydantic disponível:" , _PYDANTIC)
    print("Schemas SACP carregados:", ", ".join(__all__))
