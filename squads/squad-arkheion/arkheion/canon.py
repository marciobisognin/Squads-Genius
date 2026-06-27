#!/usr/bin/env python3
"""ARKHEION — O Cânone como código (PRD §7).

> Núcleo da auditabilidade: a marca vive aqui, em Python versionado — não em prompts.

Tudo que define a identidade da marca (cor, geometria, fonte, timing, grade) é uma
constante determinística. O agente KÁNŌN compara cada spec/render com este módulo;
divergência de hex, fonte fora da lista, geometria fora da tolerância ou timing fora
da faixa é uma reprovação bloqueante com motivo auditável.

Extensão sobre o PRD: o usuário informa o **tema** e o **tamanho do vídeo**. O tamanho
é resolvido por `DURACAO_PRESETS` em um número inteiro de CENA-10 (átomos de 10s) e na
sequência de funções narrativas correspondente — mantendo 60s/6 beats como default.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# --------------------------------------------------------------------------- #
# Paletas (PRD §2.2 / §2.3) — hex exatos, validados por KÁNŌN                  #
# --------------------------------------------------------------------------- #
PALETA_CINE: Dict[str, str] = {
    "black": "#020406",
    "black_blue": "#050A0C",
    "gray_metal": "#7B8383",
    "white_dirty": "#E8ECEA",
    "cold_reflect": "#A7D8E3",
}

PALETA_UI: Dict[str, str] = {
    "bg": "#030608",
    "lines": "#314B55",
    "text_secondary": "#B8D1D6",
    "text_primary": "#EDF8F8",
    "glow": "#94E4F2",
    "artifact_red": "#A35B55",
}

HEX_PERMITIDOS = set(PALETA_CINE.values()) | set(PALETA_UI.values())


# --------------------------------------------------------------------------- #
# Geometria fixa do card (PRD §2.4) — base 1080; ×2 para master 2160          #
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Geometria:
    base: int = 1080
    margem_lateral: int = 80
    linha_superior_y: int = 95
    titulo_y_min: int = 390
    titulo_y_max: int = 470
    rodape_y_min: int = 985
    rodape_y_max: int = 1010
    canto_l_len: int = 25

    def escala(self, fator: int = 2) -> "Geometria":
        """Retorna a geometria escalada (ex.: master 2160 = ×2)."""
        return Geometria(
            base=self.base * fator,
            margem_lateral=self.margem_lateral * fator,
            linha_superior_y=self.linha_superior_y * fator,
            titulo_y_min=self.titulo_y_min * fator,
            titulo_y_max=self.titulo_y_max * fator,
            rodape_y_min=self.rodape_y_min * fator,
            rodape_y_max=self.rodape_y_max * fator,
            canto_l_len=self.canto_l_len * fator,
        )


GEOMETRIA = Geometria()
GEOMETRIA_TOLERANCIA_PX = 6  # tolerância de KÁNŌN para posições/medidas


# --------------------------------------------------------------------------- #
# Timing & animação (PRD §2.7)                                                 #
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Timing:
    fps: int = 24
    cena_s: int = 10
    titulo_entrada_s: Tuple[float, float] = (0.4, 0.8)
    cps_min: int = 20
    cps_max: int = 30
    cursor_blink_s: Tuple[float, float] = (0.6, 0.9)
    glitch_frames: Tuple[int, int] = (1, 2)
    permanencia_card_s: Tuple[int, int] = (8, 10)

    @property
    def frames_por_cena(self) -> int:
        return self.fps * self.cena_s


TIMING = Timing()
VELOCIDADE_DIGITACAO_CPS = 25  # ponto central da faixa 20–30


# --------------------------------------------------------------------------- #
# Tipografia (PRD §2.5)                                                        #
# --------------------------------------------------------------------------- #
FONTES_PERMITIDAS = {
    "Oxanium",
    "Chakra Petch",
    "Tektur",
    "Orbitron",
    "Share Tech Mono",
    "Space Mono",
    "IBM Plex Mono",
}
FONTE_TITULO_DEFAULT = "Oxanium"
TITULO_MAX_PALAVRAS = 4


# --------------------------------------------------------------------------- #
# Formato (PRD §2.1)                                                           #
# --------------------------------------------------------------------------- #
ASPECTO = "1:1"
RES_MASTER = (2160, 2160)
RES_ENTREGA = (1080, 1080)


# --------------------------------------------------------------------------- #
# Color grading — cadeia FFmpeg determinística (PRD §2.6 / §7)                 #
# --------------------------------------------------------------------------- #
GRADE_FFMPEG = (
    "eq=contrast=1.40:saturation=0.11:brightness=-0.04,"
    "curves=all='0/0 0.15/0.05 0.85/0.92 1/0.96',"  # pretos esmagados, branco sujo
    "noise=alls=18:allf=t,"                          # granulação refinada
    "gblur=sigma=0.6,"                               # bloom base
    "rgbashift=rh=2:bh=-2,"                          # aberração cromática mínima
    "vignette=PI/4.5"                                # ~20% vinheta
)

# Faixas de tolerância numérica que KÁNŌN aceita na cadeia de grade.
GRADE_FAIXAS: Dict[str, Tuple[float, float]] = {
    "contrast": (1.30, 1.50),
    "saturation": (0.10, 0.12),
    "noise_alls": (16, 20),
    "vignette_frac": (0.15, 0.25),
}


# --------------------------------------------------------------------------- #
# Estrutura narrativa reutilizável (PRD §2.10) + tamanho variável             #
# --------------------------------------------------------------------------- #
# Sequência canônica de funções narrativas para o dossiê de 60s (6 beats).
FUNCOES_NARRATIVAS_6 = [
    "pergunta_tensao",     # 01 — O PROBLEMA / O LIMITE
    "restricao_contexto",  # 02 — ACESSO LIMITADO
    "solucao_metodo",      # 03 — O MÉTODO
    "processo",            # 04 — EM MOVIMENTO
    "prova_visual",        # 05 — DADOS REAIS / NOVA EVIDÊNCIA (dataviz)
    "conclusao_cta",       # 06 — EM OPERAÇÃO / DISPONÍVEL AGORA
]

# Reduções coerentes para tamanhos menores e expansão para maiores. Toda
# sequência preserva tensão → resolução e mantém prova_visual + conclusao_cta.
FUNCOES_NARRATIVAS_3 = ["pergunta_tensao", "solucao_metodo", "conclusao_cta"]
FUNCOES_NARRATIVAS_9 = [
    "pergunta_tensao", "restricao_contexto", "solucao_metodo",
    "processo", "processo", "prova_visual",
    "prova_visual", "restricao_contexto", "conclusao_cta",
]

# tamanho-alvo (s) -> (n_cenas, sequência de funções). CENA-10 = 10s é atômico.
DURACAO_PRESETS: Dict[int, Tuple[int, List[str]]] = {
    30: (3, FUNCOES_NARRATIVAS_3),
    60: (6, FUNCOES_NARRATIVAS_6),
    90: (9, FUNCOES_NARRATIVAS_9),
}
DURACAO_DEFAULT_S = 60


@dataclass(frozen=True)
class PlanoDuracao:
    """Resolução determinística do tamanho do vídeo escolhido pelo usuário."""
    duracao_total_s: int
    n_cenas: int
    funcoes: Tuple[str, ...]
    contadores: Tuple[str, ...]


def resolver_duracao(duracao_total_s: int = DURACAO_DEFAULT_S) -> PlanoDuracao:
    """Converte o tamanho-alvo (s) em nº de CENA-10, funções e contadores NN/TT.

    Aceita os presets de `DURACAO_PRESETS` ou qualquer múltiplo de 10 (3..9 cenas),
    repetindo `processo`/`prova_visual` no miolo quando não há preset exato.
    """
    if duracao_total_s in DURACAO_PRESETS:
        n, funcoes = DURACAO_PRESETS[duracao_total_s]
    else:
        if duracao_total_s % TIMING.cena_s != 0:
            raise ValueError(
                f"tamanho {duracao_total_s}s não é múltiplo de {TIMING.cena_s}s "
                f"(CENA-10 é atômica); use {sorted(DURACAO_PRESETS)} ou múltiplo de 10"
            )
        n = duracao_total_s // TIMING.cena_s
        if not 3 <= n <= 9:
            raise ValueError("ARKHEION suporta de 3 a 9 cenas (30s a 90s)")
        funcoes = _funcoes_para_n(n)
    total = n * TIMING.cena_s
    contadores = tuple(f"{i:02d} / {n:02d}" for i in range(1, n + 1))
    return PlanoDuracao(total, n, tuple(funcoes), contadores)


def _funcoes_para_n(n: int) -> List[str]:
    """Gera uma sequência narrativa de tamanho n preservando abertura/prova/CTA."""
    base = ["pergunta_tensao", "restricao_contexto", "solucao_metodo",
            "processo", "prova_visual", "conclusao_cta"]
    if n <= 6:
        # mantém início e fim; remove do miolo (índices 1 e 3) conforme necessário
        descartaveis = [1, 3, 2]
        funcoes = base[:]
        for idx in descartaveis:
            if len(funcoes) <= n:
                break
            funcoes.pop(idx if idx < len(funcoes) - 1 else len(funcoes) - 2)
        return funcoes[:n]
    extra = n - 6
    miolo = ["processo", "prova_visual"]
    expandido = base[:5] + [miolo[i % 2] for i in range(extra)] + [base[5]]
    return expandido


# --------------------------------------------------------------------------- #
# Encerramento (PRD §2.9)                                                      #
# --------------------------------------------------------------------------- #
ENCERRAMENTOS = {"escuro", "branco"}


# --------------------------------------------------------------------------- #
# Proibições duras (PRD §2.3 / §2.7)                                           #
# --------------------------------------------------------------------------- #
PROIBIDOS = {
    "neon", "saturado", "saturada", "3d", "holograma", "tiktok",
    "zoom_agressivo", "dourado", "gamer", "branco_digital_puro",
    "explosao", "rotacao",
}

# Mapa tema → imagens-âncora (PRD §2.11). O tratamento é constante; só o
# conteúdo das imagens muda.
ANCORAS_POR_TEMA: Dict[str, List[str]] = {
    "educacao": ["livros antigos", "documentos", "mapas", "arquivos", "manuscritos", "quadro"],
    "moda": ["tecidos", "costuras", "etiquetas", "máquina de costura", "textura das peças"],
    "arquitetura": ["maquetes", "concreto", "plantas", "luz no ambiente", "materiais"],
    "direito": ["documentos", "carimbos", "processos", "corredores", "prédios públicos"],
    "saude": ["equipamentos", "exames", "prontuários", "instrumentos"],
    "negocios": ["estoque", "planilhas", "operação", "entregas", "gráficos"],
    "tecnologia": ["servidores", "código", "cabos", "telas", "protótipos", "circuitos"],
}


def _sem_acento(texto: str) -> str:
    import unicodedata
    return "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )


def ancoras_para_tema(tema: str) -> List[str]:
    """Retorna imagens-âncora para um tema; fallback investigativo genérico."""
    chave = _sem_acento(tema.strip().lower())
    for k, v in ANCORAS_POR_TEMA.items():
        if _sem_acento(k) in chave:
            return list(v)
    return ["documentos", "arquivos", "telas", "bastidores"]


# Frase-cânone para colar no topo de cada PR (PRD final).
CANONE_RESUMO = "A imagem é a prova. O LLM descreve; o código desenha; o silêncio acusa."


if __name__ == "__main__":  # demonstração determinística
    import json

    for alvo in (30, 60, 90):
        p = resolver_duracao(alvo)
        print(json.dumps({
            "tamanho_s": p.duracao_total_s,
            "n_cenas": p.n_cenas,
            "funcoes": list(p.funcoes),
            "contadores": list(p.contadores),
        }, ensure_ascii=False))

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
