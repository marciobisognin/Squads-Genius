# PRD — Squad ARKHEION v1.0
### Pipeline de Dossiês Visuais em Vídeo · Estética "Arquivo Confidencial" (ref. Hermes / Nous Research)
**Família:** Produção Audiovisual (irmã de THEORÍA e KÊRYX)
**Status:** Draft para homologação · **Idioma operacional:** PT-BR · **Auditabilidade:** TCU-grade (determinismo em Python)

---

## 0. Tese em uma frase

> Um **dossiê visual de alta tecnologia**, com estética analógica investigativa, que transforma qualquer assunto em algo que *merece ser investigado* — produzido como **6 cenas de 10 segundos** que se montam em **1 minuto narrativo**, onde o contador `NN / 06` da interface **é** a própria espinha dorsal do roteiro.

ARKHEION (gr. *ἀρχεῖον*, "a casa dos arquivos/registros") existe porque há um isomorfismo exato entre a duração-alvo e a estrutura narrativa de referência:

```
60 s  =  6 × 10 s  =  6 etapas do dossiê  =  contador 01/06 … 06/06
```

A CENA-10 é a unidade atômica. Cada CENA-10 é um beat narrativo completo, renderizado de forma independente e montado deterministicamente. Isso permite paralelizar geração, validar fidelidade por cena, e reaproveitar/regerar uma única cena sem refazer o vídeo inteiro.

---

## 1. Posicionamento

ARKHEION é um squad de **produção audiovisual**. Vizinho-de-prateleira de outros squads de mídia, distingue-se pela *intenção* e pelo *render*:

| Squad | Domínio | Render | Diferença para ARKHEION |
|---|---|---|---|
| **THEORÍA** | Vídeo educacional cinematográfico (Manim, estilo 3B1B) | Vetorial matemático determinístico | THEORÍA *explica*; ARKHEION *revela/investiga* |
| **KÊRYX** | Conteúdo Instagram (infográfico + HQ) | Dual-render (Trilho A determinístico / B generativo) | ARKHEION herda o padrão dual-render de KÊRYX, mas em **vídeo** |
| **ARKHEION** | Dossiê audiovisual "arquivo confidencial" | **Dual-render em vídeo** (HUD determinístico + footage generativo) | — |

ARKHEION adota integralmente os **invariantes arquiteturais** que você aplica em todos os squads:

- **LLMs emitem APENAS JSON estruturado.** Todo cálculo determinístico (tipografia, geometria, timing, color grading, montagem, áudio) roda em **Python**, nunca no LLM. A identidade da marca é *código*, não *prompt*.
- Orquestração **LangGraph StateGraph**.
- **Gate de entrada Cynefin** (classificação de domínio do briefing).
- Contratos de handoff **SACP** com **schemas Pydantic**.
- **Gates HITL** obrigatórios em classificação e homologação.
- Validação **anti-sycophancy** (ELENCHUS).
- Observabilidade **Langfuse**.
- **Turing Guild** com loops de self-healing.
- Nomenclatura **greco-latina epistêmica** dos agentes.

---

## 2. O Cânone Estético (a identidade como contrato imutável)

Esta é a seção mais importante do PRD. Todo o "look" da referência é **codificado como constantes**, não interpretado pelo LLM. O agente **KÁNŌN** valida cada artefato numericamente contra estas constantes. Nenhuma cena passa se violar o Cânone.

### 2.1 Formato
- Aspecto **1:1** (quadrado).
- Master **2160 × 2160 px** · entrega **1080 × 1080 px**.
- **24 fps**.
- Duração-alvo: **60 s** (6 × 10 s). *Corte estendido opcional: 8–10 s/cena ≈ 66 s, conforme referência.*

### 2.2 Paleta — Camada Cinematográfica (footage)
| Token | Hex | Uso |
|---|---|---|
| `cine.black` | `#020406` | Preto profundo dominante |
| `cine.black_blue` | `#050A0C` | Preto azulado das sombras |
| `cine.gray_metal` | `#7B8383` | Cinza metálico (reflexos) |
| `cine.white_dirty` | `#E8ECEA` | Branco sujo (nunca branco digital puro) |
| `cine.cold_reflect` | `#A7D8E3` | Reflexo frio pontual |

### 2.3 Paleta — Camada de Interface (HUD editorial)
| Token | Hex | Uso |
|---|---|---|
| `ui.bg` | `#030608` | Fundo quase absoluto |
| `ui.lines` | `#314B55` | Linhas/molduras azul-petróleo |
| `ui.text_secondary` | `#B8D1D6` | Metadados, texto de apoio |
| `ui.text_primary` | `#EDF8F8` | Texto principal |
| `ui.glow` | `#94E4F2` | Halo frio dos títulos |
| `ui.artifact_red` | `#A35B55` | Artefato vermelho sutil (alerta/ênfase rara) |

**Regra dura:** zero cores saturadas, zero neon, zero dourado, zero estética gamer.

### 2.4 Geometria fixa do card (base 1080×1080, escalável ×2 para master)
| Elemento | Posição/Medida |
|---|---|
| Margens laterais | ~80 px |
| Linha superior (régua fina) | ~95 px do topo |
| Título principal | faixa de altura **390–470 px** |
| Texto explicativo | imediatamente abaixo do título |
| Rodapé (assinatura curta) | **985–1010 px** |
| Cantos técnicos em "L" | ~25 px de comprimento, nos 4 cantos |
| Topo-esquerda | nome do projeto / marca / protocolo |
| Topo-direita | contador `NN / 06` |
| Rodapé-esquerda | `marca / projeto` · `empresa / assunto` · `arquivo / protocolo` |

A moldura **permanece fixa** enquanto o conteúdo interno muda entre cenas.

### 2.5 Tipografia
- Família de título: técnica/quadrada, aparência de display digital, leve pixelação, halo frio.
- Referências aceitas (em ordem de preferência): **Oxanium**, **Chakra Petch**, **Tektur**, **Orbitron**, **Share Tech Mono**, **Space Mono**, **IBM Plex Mono**.
- Títulos: **CAIXA ALTA**, 1–4 palavras, cor `ui.text_primary` + `text-shadow` halo `ui.glow`.
- Texto de apoio: **monoespaçado**, menor, alta legibilidade, `ui.text_secondary`.
- Metadados: pequenos, baixa opacidade.
- Números/métricas: grandes, retos, "painel técnico".

### 2.6 Color grading (cadeia FFmpeg determinística)
Parâmetros canônicos (aplicados ao footage E como passe global de continuidade):
- Contraste **alto** (`eq=contrast≈1.4`).
- Saturação **≈0.10–0.12** (quase P&B).
- **Pretos esmagados** sem perder detalhe (curva tipo `curves`).
- Branco **sujo**, clamp abaixo de digital puro.
- **Granulação** forte porém refinada (`noise alls≈16–20`).
- **Scanlines** sutis (overlay/`geq`).
- **Bloom** suave nos highlights (`gblur` em camada de threshold, screen-blend).
- **Aberração cromática** mínima nos highlights (`rgbashift`).
- **Vinheta** escura **15%–25%** (`vignette`).

### 2.7 Timing & animação da interface
| Evento | Valor canônico |
|---|---|
| Fade de entrada (saindo do preto) | curto |
| Entrada do título | 0,4–0,8 s |
| Velocidade de digitação | **20–30 caracteres/s** |
| Cursor retangular branco (piscar) | 0,6–0,9 s |
| Glitch RGB na entrada do título | **1–2 frames** |
| Barras de dados | crescem da esquerda → direita |
| Números | contagem rápida |
| Permanência por card | 8–10 s (default ARKHEION: **10 s**) |

**Proibido:** transições de TikTok, zoom agressivo, explosão gráfica, 3D, hologramas, rotação, qualquer "salto".

### 2.8 Áudio
- Trilha **eletrônica industrial**, minimalista, escura. Graves discretos, pulsos lentos.
- Texturas: ruído de fita, CRT, interferências, impactos secos.
- SFX de teclado/cursor/sistema (sincronizados à digitação).
- **Silêncio estratégico** antes de frases-chave (tipicamente antes do beat 06).
- Locução (opcional): baixa, firme, objetiva. **Nunca** tom de anúncio.
- Proibido: música épica, feliz, pop, corporativa.

### 2.9 Encerramento
Dois formatos canônicos:
- **Escuro:** logo central em fundo preto, brilho frio leve, ruído, fade lento. (marca própria)
- **Branco:** fundo branco limpo, marca principal acima + parceiros abaixo, muito espaço vazio. (institucional)
- Nunca replicar logos de terceiros sem autorização — apenas a *lógica* de composição.

### 2.10 Estrutura narrativa reutilizável (mapeada às CENA-10)
| Cena | Contador | Função | Exemplos de título |
|---|---|---|---|
| 1 | `01 / 06` | Pergunta / tensão | "O PROBLEMA", "O LIMITE" |
| 2 | `02 / 06` | Restrição / contexto | "ACESSO LIMITADO" |
| 3 | `03 / 06` | Solução / método | "O MÉTODO" |
| 4 | `04 / 06` | Processo / bastidores | "EM MOVIMENTO" |
| 5 | `05 / 06` | Prova visual (barra/nº/comparação) | "DADOS REAIS", "NOVA EVIDÊNCIA" |
| 6 | `06 / 06` | Conclusão / CTA | "EM OPERAÇÃO", "DISPONÍVEL AGORA" |

### 2.11 Mapeamento tema → footage (substituição de cenário)
O tratamento sombrio/investigativo é **constante**; só o *conteúdo* das imagens muda:

| Assunto | Imagens-âncora |
|---|---|
| Educação / História | livros antigos, documentos, mapas, arquivos, manuscritos, quadro |
| Moda | tecidos, costuras, etiquetas, máquina de costura, textura das peças |
| Arquitetura | maquetes, concreto, plantas, luz no ambiente, materiais |
| Direito | documentos, carimbos, processos, corredores, prédios públicos |
| Saúde | equipamentos, exames, prontuários, instrumentos |
| Negócios | estoque, planilhas, operação, entregas, gráficos |
| Tecnologia | servidores, código, cabos, telas, protótipos, circuitos |

> Invariante de sensação: *"estamos vendo algo que normalmente ficaria nos bastidores."*

---

## 3. Arquitetura do sistema

### 3.1 Visão de alto nível (dual-render herdado de KÊRYX, em vídeo)

```
                          ┌──────────────────────────────────────┐
   BRIEFING (tema, marca, │            HÉGEMŌN (orquestrador)     │
   CTA, formato) ───────► │           LangGraph StateGraph        │
                          └───────────────┬──────────────────────┘
                                          │
                    ┌─────────────────────▼─────────────────────┐
                    │  GATE 1 · DIAÍRESIS (Cynefin) ── HITL      │
                    └─────────────────────┬─────────────────────┘
                                          │
                    ┌─────────────────────▼─────────────────────┐
                    │  MŶTHOS → PlanoSequencial (6 beats JSON)   │
                    └─────────────────────┬─────────────────────┘
                                          │
                    ┌─────────────────────▼─────────────────────┐
                    │  GATE 2 · Aprovação de roteiro ── HITL     │
                    └─────────────────────┬─────────────────────┘
                       ┌──────────────────┼──────────────────┐
                       ▼                  ▼                  ▼
              ┌─────────────┐   ┌──────────────┐   ┌──────────────┐
   TRILHO B → │ SKIÁGRAPHOS │   │    TÝPOS      │   │    PHŌNĒ     │ ← ÁUDIO
   (footage)  │ FootageSpec │   │ CardInterface │   │  AudioSpec   │
              └──────┬──────┘   └──────┬───────┘   └──────┬───────┘
                     │ (×6)            │ (×6)             │
                     └────────┬────────┴──────────────────┘
                              ▼
                ┌───────────────────────────────┐
                │  KÁNŌN · validação determinís- │  ← rejeita specs fora do Cânone
                │  tica contra o Cânone (Pydantic│
                │  + regras numéricas)           │
                └───────────────┬───────────────┘
                                ▼
                ┌───────────────────────────────┐
   TRILHO A  →  │  TÉKTŌN · render determinístico│
   (interface)  │  • HUD frames (HTML/CSS+PW)    │
                │  • typed-text/cursor/glitch    │
                │  • invoca API text-to-video    │
                │  • grade FFmpeg (Cânone 2.6)   │
                │  → 6× CENA-10 (.mp4)           │
                └───────────────┬───────────────┘
                                ▼
                ┌───────────────────────────────┐
                │  SÝNTHESIS · montagem master   │
                │  • concat 6× hard-cut + glitch │
                │  • passe global grão/scanline  │
                │  • mix de áudio + silêncios    │
                │  • card de encerramento (logo) │
                │  → DossiêMaster (60 s)         │
                └───────────────┬───────────────┘
                                ▼
                ┌───────────────────────────────┐
                │  ELENCHUS (tom/coerência) +    │
                │  KÁNŌN (fidelidade técnica)    │
                └───────────────┬───────────────┘
                                ▼
                ┌───────────────────────────────┐
                │  GATE 3 · Homologação ── HITL  │
                └───────────────┬───────────────┘
                                ▼
                          ENTREGA + Langfuse trace

         TURING (Turing Guild) envolve todos os nós: retry, repair de JSON,
         backoff em APIs, escalonamento a HITL em falha persistente.
```

### 3.2 Separação determinístico × probabilístico (invariante TCU)

| Nó | Tipo | Saída |
|---|---|---|
| DIAÍRESIS | LLM | JSON (classificação Cynefin) |
| MŶTHOS | LLM | JSON (PlanoSequencial: 6 beats) |
| SKIÁGRAPHOS | LLM | JSON (FootageSpec por cena) |
| TÝPOS | LLM | JSON (CardInterface por cena) |
| PHŌNĒ | LLM | JSON (AudioSpec) |
| ELENCHUS | LLM | JSON (veredito narrativo/tom) |
| **KÁNŌN** | **Python** | validação numérica contra o Cânone |
| **TÉKTŌN** | **Python** | render de frames + footage + grade |
| **SÝNTHESIS** | **Python** | montagem, áudio, master |
| **TURING** | **Python** | self-healing/orquestração |
| **HÉGEMŌN** | **Python** | StateGraph/roteamento/HITL |

Tudo que define a **identidade da marca** (cor, geometria, fonte, timing, grão) é executado em código determinístico. O LLM nunca "desenha" — ele apenas *descreve em JSON* o conteúdo a ser desenhado.

---

## 4. Roster de agentes (greco-latino epistêmico)

### Guilda da Triagem
**DIAÍRESIS** (διαίρεσις, "divisão/classificação")
- Responsabilidade única: classificar o briefing no domínio **Cynefin** (Óbvio/Complicado/Complexo/Caótico) e validar completude mínima (tema, marca, CTA, ativos disponíveis).
- Caótico/insuficiente → bounce ao usuário. Complicado → aciona sub-passo de pesquisa em MŶTHOS.
- **Gate HITL 1**: humano confirma classificação e escopo.

### Guilda Narrativa
**MŶTHOS** (μῦθος, "enredo")
- Story → **6 beats** rígidos (§2.10). Por cena produz: `titulo` (1–4 palavras, CAIXA ALTA), `texto_digitado` (linhas curtas), `contador`, `assinatura_rodape`, `dica_dataviz` (quando beat 05), `ancoras_visuais` (mapeadas ao tema §2.11).
- Emite **PlanoSequencial** (JSON). Nunca redige fora do contrato.

### Guilda de Direção Visual
**SKIÁGRAPHOS** (σκιαγράφος, "pintor de sombras")
- Para cada cena, produz **FootageSpec** (Trilho B): assunto/objeto, tipo de plano (close de telas/teclados/cabos/documentos), movimento de câmera (handheld discreto, push lento), iluminação (luzes pontuais, pretos esmagados), prompt positivo + **negativo** (sem cor saturada, sem neon, sem 3D, sem look corporativo).

**TÝPOS** (τύπος, "impressão/molde tipográfico")
- Para cada cena, produz **CardInterface** (Trilho A): variáveis de layout conforme geometria §2.4, conteúdo do título, linhas do texto digitado, config do contador/rodapé/metadados, e (quando beat 05) config de `dataviz` (barra/numero/comparação).
- Saída restrita à geometria/paleta do Cânone — sem liberdade estética.

### Guilda Sonora
**PHŌNĒ** (φωνή, "som/voz")
- Produz **AudioSpec**: mood do drone por beat, cues de SFX (teclado/cursor/impacto), pontos de **silêncio estratégico**, e (opcional) `script_locucao` baixo/firme.

### Guilda da Renderização Determinística (Têktōn)
**TÉKTŌN** (τέκτων, "artífice/construtor") — *Python, não-LLM*
- Renderiza a moldura HUD e a animação de digitação/cursor/glitch frame-a-frame (HTML/CSS + Playwright).
- Invoca a API text-to-video com a FootageSpec; aplica o **grade canônico** (§2.6) sobre o footage.
- Compõe Trilho A sobre Trilho B → **6× CENA-10 (.mp4)**.

**SÝNTHESIS** (σύνθεσις, "composição") — *Python, não-LLM*
- Concatena as 6 cenas com cortes secos + transição glitch de 1–2 frames; passe global de grão/scanline para continuidade temporal; mixa o áudio com silêncios; anexa card de encerramento; exporta master 2160² e entrega 1080².

### Guilda de Validação
**KÁNŌN** (κανών, "régua/cânone") — *Python, não-LLM*
- Guardião de fidelidade. Valida **numericamente** specs e renders contra o Cânone (hex exatos, geometria com tolerância, fonte permitida, parâmetros de grade, timing). **Gate bloqueante.**

**ELENCHUS** (ἔλεγχος, "refutação socrática")
- Anti-sycophancy. Desafia a coerência narrativa e detecta deriva para **tom de propaganda** (o dossiê tem que parecer *prova*, não anúncio). Veredito JSON com objeções acionáveis.

### Guilda Turing
**TURING** — *Python, não-LLM*
- Self-healing: retry com backoff em APIs, reparo de JSON malformado, regeneração de cena isolada, escalonamento a HITL após N falhas.

### Orquestração
**HÉGEMŌN** (ἡγεμών, "guia/condutor") — *Python, não-LLM*
- Supervisor do StateGraph: roteia nós, gerencia o estado SACP, aplica os 3 gates HITL, dispara traces Langfuse.

---

## 5. A unidade atômica — contrato CENA-10

Cada CENA-10 é dois planos sobrepostos + áudio, com 10 s exatos:

```
CENA-10
├── Trilho B (footage)      ← SKIÁGRAPHOS → FootageSpec → API → grade FFmpeg
├── Trilho A (interface)    ← TÝPOS → CardInterface → HTML/CSS+Playwright frames
│     ├── moldura fixa (HUD §2.4)
│     ├── título (entrada 0,4–0,8s, halo §2.5)
│     ├── texto digitado (20–30 cps, cursor 0,6–0,9s)
│     ├── glitch RGB (1–2 frames na entrada)
│     └── dataviz (apenas beat 05)
└── Áudio (segmento)        ← PHŌNĒ → drone + SFX + silêncio
```

Vantagens do átomo de 10s:
- **Paralelizável**: as 6 cenas geram em paralelo.
- **Regenerável**: reprovar a cena 04 não refaz o vídeo.
- **Auditável**: KÁNŌN valida cena a cena com trace individual.

---

## 6. Contratos SACP (Pydantic)

```python
from pydantic import BaseModel, Field, conlist, constr
from typing import Literal, Optional
from enum import Enum

# ---------- Enums do Cânone ----------
class CynefinDomain(str, Enum):
    OBVIO = "obvio"; COMPLICADO = "complicado"
    COMPLEXO = "complexo"; CAOTICO = "caotico"

FonteTitulo = Literal[
    "Oxanium","Chakra Petch","Tektur","Orbitron",
    "Share Tech Mono","Space Mono","IBM Plex Mono"]

BeatFuncao = Literal[
    "pergunta_tensao","restricao_contexto","solucao_metodo",
    "processo","prova_visual","conclusao_cta"]

# ---------- Entrada ----------
class Briefing(BaseModel):
    tema: str
    marca: str
    protocolo: constr(max_length=24)              # topo-esquerda
    cta: str                                       # frase do beat 06
    encerramento: Literal["escuro","branco"] = "escuro"
    fonte_titulo: FonteTitulo = "Oxanium"
    duracao_por_cena_s: int = Field(10, ge=8, le=10)
    ativos_disponiveis: list[str] = []             # b-roll/logos do usuário

class Classificacao(BaseModel):
    dominio: CynefinDomain
    completo: bool
    faltantes: list[str] = []
    requer_pesquisa: bool = False

# ---------- Narrativa ----------
class DataVizHint(BaseModel):
    tipo: Literal["barra","numero","comparacao","timeline"]
    rotulo: str
    valor: str                                     # ex.: "98%", "3x"

class Beat(BaseModel):
    indice: int = Field(ge=1, le=6)
    funcao: BeatFuncao
    contador: constr(pattern=r"^0[1-6] / 06$")
    titulo: constr(max_length=28)                  # 1–4 palavras, CAIXA ALTA
    texto_digitado: conlist(str, min_length=1, max_length=4)
    ancoras_visuais: conlist(str, min_length=1)    # mapeadas ao tema §2.11
    dataviz: Optional[DataVizHint] = None          # obrigatório só no beat 5

class PlanoSequencial(BaseModel):
    titulo_dossie: str
    beats: conlist(Beat, min_length=6, max_length=6)

# ---------- Trilho B (footage) ----------
class FootageSpec(BaseModel):
    cena_idx: int
    assunto: str
    plano: Literal["close","detalhe","plano_medio","macro"]
    movimento: Literal["handheld_sutil","push_lento","estatico","pan_lento"]
    iluminacao: str                                # "luzes pontuais, pretos esmagados"
    prompt_positivo: str
    prompt_negativo: str = ("cor saturada, neon, 3D, holograma, "
        "look corporativo, branco digital puro, transição TikTok")
    duracao_s: int = 10

# ---------- Trilho A (interface) ----------
class CardInterface(BaseModel):
    cena_idx: int
    contador: constr(pattern=r"^0[1-6] / 06$")
    titulo: str
    linhas_texto: conlist(str, min_length=1, max_length=4)
    rodape: str                                    # "marca / projeto"
    metadados_topo_esq: str
    dataviz: Optional[DataVizHint] = None
    # geometria/paleta NÃO são editáveis aqui — vêm do Cânone (constantes)

# ---------- Áudio ----------
class AudioSpec(BaseModel):
    mood_drone: str
    cues_sfx: list[str]                            # ["teclado@beat1","impacto@beat6"]
    silencios_s: list[float] = []                  # offsets de silêncio estratégico
    script_locucao: Optional[str] = None

# ---------- Cena renderizada ----------
class Cena10(BaseModel):
    idx: int
    path_mp4: str
    duracao_s: float
    checksum: str
    kanon_aprovado: bool

# ---------- Master ----------
class DossieMaster(BaseModel):
    path_master_2160: str
    path_entrega_1080: str
    duracao_total_s: float
    cenas: conlist(Cena10, min_length=6, max_length=6)
    encerramento: Literal["escuro","branco"]
    langfuse_trace_id: str
```

---

## 7. O Cânone como código (módulo de constantes)

> Núcleo da auditabilidade: a marca vive aqui, em Python versionado — não em prompts.

```python
# arkheion/canon.py
from dataclasses import dataclass

PALETA_CINE = {
    "black":"#020406","black_blue":"#050A0C","gray_metal":"#7B8383",
    "white_dirty":"#E8ECEA","cold_reflect":"#A7D8E3"}

PALETA_UI = {
    "bg":"#030608","lines":"#314B55","text_secondary":"#B8D1D6",
    "text_primary":"#EDF8F8","glow":"#94E4F2","artifact_red":"#A35B55"}

@dataclass(frozen=True)
class Geometria:        # base 1080; ×2 para master 2160
    margem_lateral: int = 80
    linha_superior_y: int = 95
    titulo_y_min: int = 390
    titulo_y_max: int = 470
    rodape_y_min: int = 985
    rodape_y_max: int = 1010
    canto_l_len: int = 25

@dataclass(frozen=True)
class Timing:
    fps: int = 24
    cena_s: int = 10
    titulo_entrada_s: tuple = (0.4, 0.8)
    cps_min: int = 20
    cps_max: int = 30
    cursor_blink_s: tuple = (0.6, 0.9)
    glitch_frames: tuple = (1, 2)

FONTES_PERMITIDAS = {
    "Oxanium","Chakra Petch","Tektur","Orbitron",
    "Share Tech Mono","Space Mono","IBM Plex Mono"}

# Cadeia de grade canônica (FFmpeg) — parametrizada, não improvisada
GRADE_FFMPEG = (
    "eq=contrast=1.40:saturation=0.11:brightness=-0.04,"
    "curves=all='0/0 0.15/0.05 0.85/0.92 1/0.96',"   # pretos esmagados, branco sujo
    "noise=alls=18:allf=t,"                           # granulação refinada
    "gblur=sigma=0.6,"                                # bloom base
    "rgbashift=rh=2:bh=-2,"                           # aberração cromática mínima
    "vignette=PI/4.5"                                 # ~20% vinheta
)
# scanlines + glitch RGB pontual aplicados como overlays separados por TÉKTŌN

VELOCIDADE_DIGITACAO_CPS = 25      # ponto central da faixa
PROIBIDOS = {"neon","saturado","3D","holograma","tiktok","zoom_agressivo"}
```

KÁNŌN compara cada spec/render com este módulo. Divergência de hex, fonte fora da lista, geometria fora da tolerância ou timing fora da faixa → **reprovação bloqueante** com motivo auditável.

---

## 8. Pipeline de renderização determinística (TÉKTŌN)

### 8.1 Trilho A — HUD e digitação
1. **Template HTML/CSS** com a moldura fixa (cantos "L", régua, contador, rodapé) e fontes web (`@font-face` locais das fontes permitidas). Variáveis CSS = tokens do Cânone.
2. **Geração frame-a-frame** (240 frames / 10 s @ 24fps):
   - frames 0–N: fade do preto + entrada do título (0,4–0,8 s) + glitch RGB 1–2 frames;
   - frames seguintes: texto digitado revelando substring por frame a 25 cps; cursor retangular piscando (0,6–0,9 s);
   - beat 05: barra de dados crescendo E→D e/ou número em contagem rápida.
   - Captura via **Playwright** (screenshot por frame) → sequência PNG com alfa.
3. Resultado: overlay de interface com transparência, pronto para compor.

### 8.2 Trilho B — footage
1. Envia FootageSpec à **API text-to-video** (Kling / Runway Gen-3 / Veo / Luma — *configurável por provider*), 1:1, 10 s.
2. Aplica **GRADE_FFMPEG** (§7) + overlay de **scanlines** → footage canônico, independentemente da variância do gerador.

### 8.3 Composição da CENA-10
- Compõe Trilho A (alfa) sobre Trilho B (`overlay`), corta em 10 s, calcula `checksum`, submete ao KÁNŌN. Saída: `Cena10`.

### 8.4 Montagem (SÝNTHESIS)
- `concat` das 6 cenas com **corte seco** + transição **glitch** de 1–2 frames.
- **Passe global** de grão/scanline sobre a timeline montada (continuidade temporal do grão entre cortes).
- **Áudio**: bed de drone industrial contínuo + SFX por cue + silêncios (AudioSpec) + locução opcional (TTS baixo/firme).
- Anexa **card de encerramento** (escuro/branco) com fade lento.
- Exporta master **2160²** e entrega **1080²**, 24fps, H.264/HEVC.

> **Stack de áudio:** bed via biblioteca licenciada/loop ou API de áudio generativo; SFX de sistema versionados no repo; TTS opcional (provider configurável). Default: **sem locução** (o silêncio é parte da estética).

---

## 9. Máquina de estados (LangGraph)

```
[ingest] → [diairesis] → ⟨GATE_1 HITL⟩
        → [mythos] → ⟨GATE_2 HITL: aprova roteiro/6 beats⟩
        → fan-out: [skiagraphos ×6] ∥ [typos ×6] ∥ [phone]
        → [kanon_specs]  (reprova → volta ao agente correspondente)
        → [tekton ×6]    (render cenas; falha → TURING)
        → [kanon_cenas]  (reprova cena → regenera só a cena)
        → [synthesis]    (master)
        → [elenchus] ∥ [kanon_master]
        → ⟨GATE_3 HITL: homologação⟩
        → [entrega + langfuse_flush]
```

Política de roteamento de falha (TURING): malformação JSON → repair+retry (máx 2); erro de API → backoff exponencial (máx 3); reprovação KÁNŌN persistente (≥2) → escalona a HITL com diagnóstico.

---

## 10. Gates HITL

| Gate | Quando | Decisão humana |
|---|---|---|
| **1 · Triagem** | após DIAÍRESIS | confirma domínio Cynefin, tema, marca, CTA; injeta ativos |
| **2 · Roteiro** | após MŶTHOS | aprova/edita os 6 títulos + textos digitados antes de gastar render |
| **3 · Homologação** | após master | aprova entrega final ou solicita regeneração de cena(s) |

Gate 2 é o de maior ROI: aprova-se o roteiro *antes* de consumir créditos de geração de vídeo.

---

## 11. Validação & anti-sycophancy

- **KÁNŌN (determinístico):** fidelidade técnica — hex, fonte, geometria, grade, timing, duração 10s ± tolerância. Falha = bloqueio com `motivo` auditável.
- **ELENCHUS (LLM, adversarial):** os 6 beats contam *uma história* (tensão → resolução)? O tom é de **dossiê/prova** ou escorregou para **propaganda**? O CTA fecha sem entusiasmo de anúncio? Emite objeções acionáveis; não elogia por elogiar.

---

## 12. Observabilidade (Langfuse)

- Trace por execução; spans por agente e por CENA-10.
- Atributos: tokens, latência, provider de vídeo, custo estimado, verdict de KÁNŌN/ELENCHUS, decisões HITL.
- Cada `Cena10.checksum` + spec correspondente ficam linkados → reconstrução completa do "por que esta cena ficou assim" (auditabilidade TCU-grade).

---

## 13. Stack tecnológico

| Camada | Tecnologia |
|---|---|
| Orquestração | LangGraph (StateGraph) + Python 3.12 |
| Contratos | Pydantic v2 |
| HUD/tipografia | HTML + CSS + Playwright (captura frame-a-frame) |
| Vídeo generativo | API text-to-video (provider plugável: Kling/Runway/Veo/Luma) |
| Grade/compositing/montagem | FFmpeg + MoviePy |
| Áudio | FFmpeg + biblioteca de loops/SFX + TTS opcional |
| Observabilidade | Langfuse |
| Empacotamento | Docker (render workers) |

---

## 14. Estrutura de repositório (proposta `marciobisognin/Squads-Genius`)

```
squad-arkheion/
├── arkheion/
│   ├── canon.py                 # Cânone como código (§7)
│   ├── schemas.py               # contratos SACP (§6)
│   ├── graph.py                 # LangGraph StateGraph
│   ├── agents/
│   │   ├── diairesis.py  mythos.py  skiagraphos.py
│   │   ├── typos.py  phone.py  elenchus.py
│   ├── deterministic/
│   │   ├── kanon.py             # validador numérico
│   │   ├── tekton/              # render HUD + footage + grade
│   │   │   ├── hud_template/    # html/css + fontes
│   │   │   ├── typing.py        # digitação/cursor/glitch
│   │   │   ├── footage.py       # client text-to-video
│   │   │   └── grade.py         # cadeia FFmpeg
│   │   ├── synthesis.py         # montagem/áudio/master
│   │   └── turing.py            # self-healing
│   ├── hegemon.py               # orquestrador + gates HITL
│   └── observability.py         # Langfuse
├── assets/sfx/                  # impactos, teclado, cursor (versionados)
├── tests/
│   ├── test_canon.py            # garante hex/geometria/timing
│   ├── test_schemas.py
│   └── test_kanon_rejection.py  # specs fora do Cânone DEVEM falhar
├── examples/                    # briefings de demonstração por tema
└── PRD_Squad_ARKHEION_v1.0.md
```

---

## 15. Roadmap de implementação

| Fase | Entregável | Critério de saída |
|---|---|---|
| **F0 · Cânone** | `canon.py` + `schemas.py` + testes | KÁNŌN reprova specs sintéticas fora do padrão |
| **F1 · Trilho A** | HUD + digitação/cursor/glitch (1 card estático→animado) | 1 CENA-10 só-interface renderiza fiel ao Cânone |
| **F2 · Trilho B + grade** | client de vídeo + cadeia FFmpeg | footage qualquer → look canônico |
| **F3 · CENA-10** | composição A∘B + KÁNŌN por cena | 6 cenas independentes válidas |
| **F4 · SÝNTHESIS** | montagem + áudio + encerramento | master 60s 1:1 24fps exportado |
| **F5 · Agentes LLM** | MŶTHOS/SKIÁGRAPHOS/TÝPOS/PHŌNĒ (JSON-only) | briefing → PlanoSequencial → specs válidas |
| **F6 · Orquestração** | HÉGEMŌN + 3 gates HITL + TURING | execução E2E de um tema |
| **F7 · Validação** | ELENCHUS + Langfuse | trace auditável + veredito narrativo |

MVP útil = **F0–F4** (render determinístico funcionando com specs mockadas). Os agentes LLM entram depois, já contra contratos estáveis.

---

## 16. Riscos & mitigações

| Risco | Mitigação |
|---|---|
| Footage generativo "vaza" cor/estética | Grade FFmpeg é **soberana**: marca é code-enforced, não model-enforced |
| Custo de créditos de vídeo | Gate 2 aprova roteiro antes de gerar; regeneração é por-cena, não por-vídeo |
| Variância entre providers de vídeo | Client plugável + grade idêntica neutraliza diferença de look |
| Fontes não licenciadas | Lista restrita a famílias de licença aberta (Oxanium/Chakra Petch/etc. via OFL) |
| Logos de terceiros no encerramento | Apenas a *lógica* de composição; ativos vêm do usuário no Gate 1 |
| Deriva para "propaganda" | ELENCHUS bloqueia tom de anúncio; Cânone proíbe estética corporativa |

---

## 17. Definition of Done (v1.0)

Um dossiê está pronto quando:
1. 6× CENA-10 aprovadas individualmente por KÁNŌN (hex/fonte/geometria/grade/timing dentro da tolerância);
2. master de **60 s**, **1:1**, **24 fps**, com contador `01/06…06/06` coerente e moldura fixa;
3. áudio industrial com silêncio estratégico antes do beat 06 e SFX sincronizados à digitação;
4. encerramento (escuro ou branco) conforme briefing;
5. veredito ELENCHUS sem objeção de tom "propaganda";
6. trace Langfuse completo, com specs ↔ checksums linkados;
7. homologação humana registrada no Gate 3.

---

*Cânone resumido em uma frase, para colar no topo de cada PR:*
> **A imagem é a prova. O LLM descreve; o código desenha; o silêncio acusa.**
