#!/usr/bin/env python3
"""ARKHEION — Contratos SACP (PRD §6).

Schemas de handoff entre agentes. Usa Pydantic v2 quando disponível; caso contrário
degrada para dataclasses da stdlib com validação manual equivalente — para que os
testes e a validação determinística rodem em qualquer ambiente (PRD §13).

Generalização sobre o PRD: o contador é `NN / TT` (cena/total), permitindo dossiês de
3, 6 ou 9 cenas conforme o tamanho de vídeo escolhido pelo usuário.
"""
from __future__ import annotations

import re
from typing import List, Optional

CONTADOR_RE = re.compile(r"^\d{2} / \d{2}$")

FUNCOES = {
    "pergunta_tensao", "restricao_contexto", "solucao_metodo",
    "processo", "prova_visual", "conclusao_cta",
}
CYNEFIN = {"obvio", "complicado", "complexo", "caotico"}
PLANOS = {"close", "detalhe", "plano_medio", "macro"}
MOVIMENTOS = {"handheld_sutil", "push_lento", "estatico", "pan_lento"}
DATAVIZ_TIPOS = {"barra", "numero", "comparacao", "timeline"}
ENCERRAMENTOS = {"escuro", "branco"}

try:  # ---- caminho preferencial: Pydantic v2 --------------------------------
    from pydantic import BaseModel, Field, field_validator

    _PYDANTIC = True

    class DataVizHint(BaseModel):
        tipo: str
        rotulo: str
        valor: str

        @field_validator("tipo")
        @classmethod
        def _tipo(cls, v: str) -> str:
            if v not in DATAVIZ_TIPOS:
                raise ValueError(f"dataviz.tipo inválido: {v}")
            return v

    class Briefing(BaseModel):
        tema: str
        marca: str
        protocolo: str = Field(max_length=24)
        cta: str
        duracao_total_s: int = 60
        encerramento: str = "escuro"
        fonte_titulo: str = "Oxanium"
        duracao_por_cena_s: int = Field(default=10, ge=8, le=10)
        ativos_disponiveis: List[str] = Field(default_factory=list)

        @field_validator("encerramento")
        @classmethod
        def _enc(cls, v: str) -> str:
            if v not in ENCERRAMENTOS:
                raise ValueError(f"encerramento inválido: {v}")
            return v

    class Classificacao(BaseModel):
        dominio: str
        completo: bool
        faltantes: List[str] = Field(default_factory=list)
        requer_pesquisa: bool = False

        @field_validator("dominio")
        @classmethod
        def _dom(cls, v: str) -> str:
            if v not in CYNEFIN:
                raise ValueError(f"domínio Cynefin inválido: {v}")
            return v

    class Beat(BaseModel):
        indice: int = Field(ge=1, le=9)
        funcao: str
        contador: str
        titulo: str = Field(max_length=28)
        texto_digitado: List[str] = Field(min_length=1, max_length=4)
        ancoras_visuais: List[str] = Field(min_length=1)
        dataviz: Optional[DataVizHint] = None

        @field_validator("funcao")
        @classmethod
        def _fun(cls, v: str) -> str:
            if v not in FUNCOES:
                raise ValueError(f"função narrativa inválida: {v}")
            return v

        @field_validator("contador")
        @classmethod
        def _cont(cls, v: str) -> str:
            if not CONTADOR_RE.match(v):
                raise ValueError(f"contador fora do padrão 'NN / TT': {v}")
            return v

    class PlanoSequencial(BaseModel):
        titulo_dossie: str
        beats: List[Beat] = Field(min_length=3, max_length=9)

    class FootageSpec(BaseModel):
        cena_idx: int
        assunto: str
        plano: str
        movimento: str
        iluminacao: str
        prompt_positivo: str
        prompt_negativo: str = (
            "cor saturada, neon, 3D, holograma, look corporativo, "
            "branco digital puro, transição TikTok"
        )
        duracao_s: int = 10

        @field_validator("plano")
        @classmethod
        def _plano(cls, v: str) -> str:
            if v not in PLANOS:
                raise ValueError(f"plano inválido: {v}")
            return v

        @field_validator("movimento")
        @classmethod
        def _mov(cls, v: str) -> str:
            if v not in MOVIMENTOS:
                raise ValueError(f"movimento inválido: {v}")
            return v

    class CardInterface(BaseModel):
        cena_idx: int
        contador: str
        titulo: str
        linhas_texto: List[str] = Field(min_length=1, max_length=4)
        rodape: str
        metadados_topo_esq: str
        dataviz: Optional[DataVizHint] = None

        @field_validator("contador")
        @classmethod
        def _cont(cls, v: str) -> str:
            if not CONTADOR_RE.match(v):
                raise ValueError(f"contador fora do padrão 'NN / TT': {v}")
            return v

    class AudioSpec(BaseModel):
        mood_drone: str
        cues_sfx: List[str] = Field(default_factory=list)
        silencios_s: List[float] = Field(default_factory=list)
        script_locucao: Optional[str] = None

    class Cena10(BaseModel):
        idx: int
        path_mp4: str
        duracao_s: float
        checksum: str
        kanon_aprovado: bool

    class DossieMaster(BaseModel):
        path_master_2160: str
        path_entrega_1080: str
        duracao_total_s: float
        cenas: List[Cena10] = Field(min_length=3, max_length=9)
        encerramento: str
        langfuse_trace_id: str

except Exception:  # ---- fallback: dataclasses da stdlib ---------------------
    _PYDANTIC = False
    from dataclasses import dataclass, field

    def _check(cond: bool, msg: str) -> None:
        if not cond:
            raise ValueError(msg)

    @dataclass
    class DataVizHint:  # type: ignore[no-redef]
        tipo: str
        rotulo: str
        valor: str

        def __post_init__(self) -> None:
            _check(self.tipo in DATAVIZ_TIPOS, f"dataviz.tipo inválido: {self.tipo}")

    @dataclass
    class Briefing:  # type: ignore[no-redef]
        tema: str
        marca: str
        protocolo: str
        cta: str
        duracao_total_s: int = 60
        encerramento: str = "escuro"
        fonte_titulo: str = "Oxanium"
        duracao_por_cena_s: int = 10
        ativos_disponiveis: List[str] = field(default_factory=list)

        def __post_init__(self) -> None:
            _check(len(self.protocolo) <= 24, "protocolo > 24 chars")
            _check(self.encerramento in ENCERRAMENTOS, f"encerramento inválido: {self.encerramento}")
            _check(8 <= self.duracao_por_cena_s <= 10, "duracao_por_cena_s fora de 8..10")

    @dataclass
    class Classificacao:  # type: ignore[no-redef]
        dominio: str
        completo: bool
        faltantes: List[str] = field(default_factory=list)
        requer_pesquisa: bool = False

        def __post_init__(self) -> None:
            _check(self.dominio in CYNEFIN, f"domínio Cynefin inválido: {self.dominio}")

    @dataclass
    class Beat:  # type: ignore[no-redef]
        indice: int
        funcao: str
        contador: str
        titulo: str
        texto_digitado: List[str]
        ancoras_visuais: List[str]
        dataviz: Optional[DataVizHint] = None

        def __post_init__(self) -> None:
            _check(1 <= self.indice <= 9, "indice fora de 1..9")
            _check(self.funcao in FUNCOES, f"função inválida: {self.funcao}")
            _check(bool(CONTADOR_RE.match(self.contador)), f"contador fora do padrão: {self.contador}")
            _check(len(self.titulo) <= 28, "titulo > 28 chars")
            _check(1 <= len(self.texto_digitado) <= 4, "texto_digitado deve ter 1..4 linhas")
            _check(len(self.ancoras_visuais) >= 1, "ancoras_visuais vazio")

    @dataclass
    class PlanoSequencial:  # type: ignore[no-redef]
        titulo_dossie: str
        beats: List[Beat]

        def __post_init__(self) -> None:
            _check(3 <= len(self.beats) <= 9, "beats deve ter 3..9 itens")

    @dataclass
    class FootageSpec:  # type: ignore[no-redef]
        cena_idx: int
        assunto: str
        plano: str
        movimento: str
        iluminacao: str
        prompt_positivo: str
        prompt_negativo: str = (
            "cor saturada, neon, 3D, holograma, look corporativo, "
            "branco digital puro, transição TikTok"
        )
        duracao_s: int = 10

        def __post_init__(self) -> None:
            _check(self.plano in PLANOS, f"plano inválido: {self.plano}")
            _check(self.movimento in MOVIMENTOS, f"movimento inválido: {self.movimento}")

    @dataclass
    class CardInterface:  # type: ignore[no-redef]
        cena_idx: int
        contador: str
        titulo: str
        linhas_texto: List[str]
        rodape: str
        metadados_topo_esq: str
        dataviz: Optional[DataVizHint] = None

        def __post_init__(self) -> None:
            _check(bool(CONTADOR_RE.match(self.contador)), f"contador fora do padrão: {self.contador}")
            _check(1 <= len(self.linhas_texto) <= 4, "linhas_texto deve ter 1..4")

    @dataclass
    class AudioSpec:  # type: ignore[no-redef]
        mood_drone: str
        cues_sfx: List[str] = field(default_factory=list)
        silencios_s: List[float] = field(default_factory=list)
        script_locucao: Optional[str] = None

    @dataclass
    class Cena10:  # type: ignore[no-redef]
        idx: int
        path_mp4: str
        duracao_s: float
        checksum: str
        kanon_aprovado: bool

    @dataclass
    class DossieMaster:  # type: ignore[no-redef]
        path_master_2160: str
        path_entrega_1080: str
        duracao_total_s: float
        cenas: List[Cena10]
        encerramento: str
        langfuse_trace_id: str

        def __post_init__(self) -> None:
            _check(3 <= len(self.cenas) <= 9, "cenas deve ter 3..9 itens")


def usando_pydantic() -> bool:
    """True se os contratos estão validando via Pydantic v2."""
    return _PYDANTIC


__all__ = [
    "Briefing", "Classificacao", "DataVizHint", "Beat", "PlanoSequencial",
    "FootageSpec", "CardInterface", "AudioSpec", "Cena10", "DossieMaster",
    "usando_pydantic", "CONTADOR_RE", "FUNCOES", "CYNEFIN",
]

if __name__ == "__main__":
    print("Pydantic ativo:" if usando_pydantic() else "Fallback dataclasses ativo:", usando_pydantic())
    b = Beat(indice=1, funcao="pergunta_tensao", contador="01 / 06", titulo="O PROBLEMA",
             texto_digitado=["linha de teste"], ancoras_visuais=["documentos"])
    print("Beat válido:", b.titulo, b.contador)

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
