# THEORÍA — Arquitetura

## Visão geral
THEORÍA é um pipeline multiagente de 13 estágios (S0→S13) orquestrado por um
**StateGraph** (LangGraph). O orquestrador **DEMIURGO** mantém o estado do job e
despacha as guildas, dispara os gates humanos (A, B, C) e comanda os dois loops
determinísticos: **reconciliação de tempo** (S5↔S9) e **self-healing de render** (S10).

## Invariante central
> **LLMs geram apenas conteúdo estruturado (JSON).** Todo cálculo de tempo, toda
> compilação de código e toda renderização são **Python determinístico** — auditável,
> reproduzível e versionado. O mesmo scene-graph JSON sempre produz o mesmo vídeo.

## Guildas e agentes
| Guilda | Agentes | Natureza |
|---|---|---|
| Orquestração | DEMIURGO | StateGraph |
| Gate de entrada | KRITES | LLM→JSON (Gate A) |
| Concepção | NOÉSIS, PAIDEIA, ELENCHUS | LLM→JSON + QA epistêmico |
| Roteiro | RAPSODO, CHRONOS | LLM→JSON + determinístico |
| Visual | SCENOGRAPHO, CHROMA | LLM→JSON |
| Forja | MOTOR MANIM, HEFESTO, EChÓ | determinístico + codegen controlada |
| Render & QA | ÁRGOS, HARMONIA | determinístico + LLM-QA |
| Validação | AISTHÉSIS | LLM-juiz (Gate C) |

## Fronteira LLM ↔ determinístico
```
LLM (JSON)                         | Determinístico (Python)
-----------------------------------|--------------------------------------------
KRITES   -> Classificacao          | CHRONOS  -> chronos_timing.py (timeline)
NOÉSIS   -> CoreInsight            | MOTOR    -> manim_compiler.py (código)
PAIDEIA  -> Beat[] (arco)          | ÁRGOS    -> qa_frame_checks.py (QA)
RAPSODO  -> narração               | HARMONIA -> assemble_av.py (mux + manifesto)
SCENOGRAPHO -> SceneGraph[]        | render config -> render_config.py
CHROMA   -> câmera/paleta          | validação -> validate_scene_graph.py
ELENCHUS/AISTHÉSIS -> veredictos   | catálogo  -> primitive_library.py
```

## Handoffs
Todo handoff entre agentes é um **envelope JSON** validado por Pydantic
(`schemas/theoria_schemas.py`): `{versao, origem, destino, schema, payload,
proveniencia, checagem}`. A checagem garante `pydantic_ok` e, no caso visual,
`primitivas_existentes`.

## Loops
- **S5↔S9 (reconciliação):** CHRONOS planeja → EChÓ mede durações reais → se
  |Δ| > 200 ms/beat, CHRONOS reajusta. Converge para erro de sync < 150 ms.
- **S10 (self-healing):** ÁRGOS detecta defeito tipado → DEMIURGO reabre o estágio
  responsável (STORYBOARD/CINEMATOGRAPHY/SYNTHESIS/TIMING) com `max_retries` +
  circuit breaker → re-render (preview barato → full 1080p).

## Reprodutibilidade (RNF1)
Manim **pinado** + DSL **versionada** (`DSL_VERSION`) + **seed** → output idêntico
bit-a-bit (frames) ou perceptualmente idêntico (com TTS). O manifesto liga input→output
por hashes (timeline, mux).

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
