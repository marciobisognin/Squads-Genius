#!/usr/bin/env python3
"""THEORÍA — Contratos de handoff (envelopes SACP).

Todos os handoffs entre agentes são envelopes JSON validados. Estes schemas
formalizam o que a Seção 7 do PRD descreve. Funcionam com Pydantic v2 quando
disponível; caso contrário, degradam para dataclasses da stdlib (mesma forma,
sem dependência externa) — preservando o princípio de zero-dependência dos
scripts determinísticos do repositório.

Princípio-mestre: o LLM emite apenas JSON estruturado conforme estes contratos;
tempo, compilação e render são Python determinístico.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

try:  # Caminho preferencial — Pydantic v2.
    from pydantic import BaseModel, Field

    _PYDANTIC = True
except Exception:  # pragma: no cover - fallback sem dependências externas.
    _PYDANTIC = False
    from dataclasses import dataclass, field

    def Field(default=None, **_kwargs):  # type: ignore
        return default

    class BaseModel:  # type: ignore
        """Fallback mínimo: aceita kwargs e expõe .dict()/.to_dict()."""

        def __init__(self, **data: Any) -> None:
            for key, value in data.items():
                setattr(self, key, value)

        def dict(self) -> Dict[str, Any]:
            return {k: v for k, v in self.__dict__.items()}

        def to_dict(self) -> Dict[str, Any]:
            return self.dict()


# ---------------------------------------------------------------------------
# Constantes de domínio (catálogo fechado — evita scope creep).
# ---------------------------------------------------------------------------
FORMATOS = ("16:9", "9:16", "1:1")
NIVEIS = ("fundamental", "medio", "medio_avancado", "superior")
FUNCOES_DIDATICAS = ("gancho", "intuicao", "formalizacao", "recompensa")
COMPLEXIDADES = ("simples", "complicado", "complexo")

RESOLUCOES: Dict[str, Tuple[int, int]] = {
    "16:9": (1920, 1080),
    "9:16": (1080, 1920),
    "1:1": (1080, 1080),
}


# ---------------------------------------------------------------------------
# Contratos (espelham PRD §7).
# ---------------------------------------------------------------------------
class VideoBrief(BaseModel):
    ideia: str
    formato: str = Field("16:9")
    nivel_audiencia: str = Field("medio")
    banda_duracao_s: Tuple[int, int] = Field((120, 360))
    tts_habilitado: bool = Field(True)
    idioma: str = Field("pt-BR")


class Classificacao(BaseModel):
    dominio: str                       # matematica, fisica, linguistica, cs...
    complexidade: str                  # simples | complicado | complexo
    profundidade: int                  # 1..5
    banda_duracao_s: Tuple[int, int]
    gate_b_recomendado: bool = Field(False)


class CoreInsight(BaseModel):
    objetivo_aprendizagem: str
    ideia_nucleo: str
    momento_aha: str
    pre_requisitos: List[str] = Field(default_factory=list) if _PYDANTIC else []


class Beat(BaseModel):
    id: str
    funcao_didatica: str               # gancho | intuicao | formalizacao | recompensa
    narracao: str
    palavras: int
    duracao_narracao_s: float = Field(0.0)   # CHRONOS (determinístico)
    pausa_absorcao_s: float = Field(0.0)      # CHRONOS (determinístico)
    run_time_anim_s: float = Field(0.0)       # CHRONOS (determinístico)


class PrimitiveCall(BaseModel):
    primitiva: str                     # ex.: "FunctionGraphReveal"
    params: Dict[str, Any] = Field(default_factory=dict) if _PYDANTIC else {}
    run_time_s: float = Field(1.0)


class CameraSpec(BaseModel):
    movimento: str = Field("static")   # static | pan | zoom_in | zoom_out
    alvo: Optional[List[float]] = Field(None)
    run_time_s: float = Field(0.0)


class SceneGraph(BaseModel):
    beat_id: str
    primitivas: List[PrimitiveCall] = Field(default_factory=list) if _PYDANTIC else []
    camera: Optional[CameraSpec] = Field(None)
    paleta_ref: str = Field("semantica_padrao")


class RenderJob(BaseModel):
    formato: str = Field("16:9")
    resolucao: Tuple[int, int] = Field((1920, 1080))
    fps: int = Field(60)
    qualidade: str = Field("-qh")
    seed: int = Field(42)
    manim_version_lock: str = Field("0.18.1")
    crf: int = Field(18)


class Defeito(BaseModel):
    tipo: str                          # sobreposicao | off_canvas | contraste | jitter | sync
    severidade: str = Field("media")   # baixa | media | alta
    beat_id: Optional[str] = Field(None)
    detalhe: str = Field("")
    estagio_responsavel: str = Field("SYNTHESIS")


class QAReport(BaseModel):
    aprovado: bool = Field(False)
    defeitos: List[Defeito] = Field(default_factory=list) if _PYDANTIC else []
    frames_amostrados: int = Field(0)


class Envelope(BaseModel):
    versao: str = Field("1.0")
    origem: str = Field("")
    destino: str = Field("")
    schema: str = Field("")
    payload: Dict[str, Any] = Field(default_factory=dict) if _PYDANTIC else {}
    proveniencia: Dict[str, Any] = Field(default_factory=dict) if _PYDANTIC else {}
    checagem: Dict[str, Any] = Field(default_factory=dict) if _PYDANTIC else {}


__all__ = [
    "FORMATOS", "NIVEIS", "FUNCOES_DIDATICAS", "COMPLEXIDADES", "RESOLUCOES",
    "VideoBrief", "Classificacao", "CoreInsight", "Beat", "PrimitiveCall",
    "CameraSpec", "SceneGraph", "RenderJob", "Defeito", "QAReport", "Envelope",
]

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
