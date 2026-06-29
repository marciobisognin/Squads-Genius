# PRD — Squad THEORÍA v1.0
### Pipeline multiagente para geração cinematográfica de vídeos educacionais em Manim (padrão estético 3Blue1Brown)

> **Idioma de operação:** Português do Brasil (pt-BR).
> **Repositório alvo:** `marciobisognin/Squads-Genius`.

---

## 1. Sumário executivo

THEORÍA (do grego *θεωρία* — "contemplar um espetáculo", raiz de *teoria* e de *espectador*) é um squad que transforma **uma ideia** em um **vídeo educacional de nível cinematográfico**, renderizado em Manim com a gramática visual consagrada pelo canal 3Blue1Brown: intuição construída visualmente, hierarquia limpa, transformações suaves, cor com semântica e narração sincronizada ao milissegundo.

A partir de um *brief* mínimo (ideia + formato + nível de audiência), o squad concebe o conceito, define o arco didático, escreve o roteiro, projeta cada cena, calcula o tempo necessário para explicar tudo, compila o código Manim, renderiza, valida e entrega um **MP4 em 1080p no formato informado pelo usuário** (16:9, 9:16 ou 1:1).

### Invariante central (não negociável)
> **LLMs geram apenas conteúdo estruturado (JSON).** Todo cálculo de tempo, toda compilação de código e toda renderização são **Python determinístico** — auditável, reproduzível e versionado. O mesmo *scene-graph* JSON sempre produz o mesmo vídeo.

Isso é alcançado por uma arquitetura **DSL-first**: os agentes não escrevem Manim "no escuro". Eles emitem um **grafo de cena** que referencia uma **biblioteca de primitivas Manim vetadas e testadas**; um compilador determinístico (Motor MANIM) traduz o grafo em código renderizável. Geração de código livre existe apenas como *escape hatch* controlado (agente HEFESTO), sempre sob *sandbox* + render-validate-heal.

---

## 2. Problema e objetivos

### 2.1 Problema
Produzir um vídeo estilo 3b1b manualmente exige domínio simultâneo de pedagogia, roteiro, design de movimento, cor, *timing* e programação Manim. O gargalo não é a renderização (Manim já é determinístico) — é a **composição da cena** e a **sincronia narração↔animação**. Geração ingênua de código Manim por LLM falha em renderizar, sobrepõe objetos, estoura a tela e dessincroniza áudio e vídeo.

### 2.2 Objetivos
- **O1.** Da ideia ao vídeo entregue, com intervenção humana apenas em gates de decisão (classificação e homologação).
- **O2.** Qualidade cinematográfica reproduzível: composição limpa, paleta semântica, câmera intencional, *pacing* que respeita o tempo de absorção do espectador.
- **O3.** Sincronia narração↔animação calculada deterministicamente (erro alvo < 150 ms por segmento).
- **O4.** Saída em **1080p** no formato escolhido (16:9 / 9:16 / 1:1), com todos os artefatos intermediários persistidos para auditoria.
- **O5.** Reprodutibilidade total: versão do Manim fixada + DSL versionada + seed → output idêntico bit-a-bit (frames) ou perceptualmente idêntico (com TTS).

### 2.3 Não-objetivos (v1.0)
- Animação 3D complexa fora do escopo do `ThreeDScene` básico.
- Edição de áudio musical/trilha (apenas narração TTS + silêncios calculados; trilha é *post-hook* opcional).
- Tradução multilíngue (v1.0 é pt-BR nativo).

---

## 3. Princípios de design

| Princípio | Aplicação em THEORÍA |
|---|---|
| **Máquina de estados** | Pipeline de 13 estágios com roteamento condicional e loops de reconciliação (LangGraph StateGraph). |
| **Classificador de entrada** | Classifica a requisição por domínio (matemática, física, linguística, CS…) e complexidade, definindo profundidade e estratégia. Gate humano obrigatório neste estágio. |
| **Handoffs validados** | Todo *handoff* entre agentes é um envelope JSON validado por Pydantic (schema + proveniência + checagem). |
| **Gates humanos (HITL)** | Gate A (pós-classificação) e Gate C (homologação estética). Gate B (storyboard) opcional/configurável. |
| **Self-healing** | Loop de auto-cura para falhas de compilação/render/QA. |
| **Observabilidade** | *Trace* por agente, por estágio e por *job* de render; custo e latência por nó (Langfuse). |
| **Determinismo** | LLM → JSON; cálculo de tempo, compilação e render → Python. |
| **Nomes greco-latinos** | Agentes nomeados por função epistêmica. |

---

## 4. Personas e casos de uso

- **Criador de conteúdo educacional** — pipeline para Reels/Instagram e YouTube em pt-BR (filosofia, física, matemática, linguística, sci-fi).
- **Educador/professor** — gera material visual para aula a partir de um conceito.
- **Integração com outros squads** — THEORÍA expõe interface padronizada para ser orquestrado junto a pipelines Manim existentes e squads de carrosséis; ambos compartilham a camada de identidade visual.

**Caso de uso canônico**
> *"Explique por que e^(iπ) = −1 de forma intuitiva, formato 9:16, audiência ensino médio avançado."*
> → THEORÍA entrega um MP4 1080×1920, ~3–4 min, com a espiral no plano complexo, narração pt-BR sincronizada e a revelação final cronometrada.

---

## 5. Arquitetura do squad

Orquestrador: **DEMIURGO** (*δημιουργός* — o artífice que ordena o cosmos a partir do plano). Liga o StateGraph, mantém o estado e despacha os guildas.

### Gate de entrada
- **Classificador de Domínio** — classifica a requisição por domínio e complexidade; define profundidade e banda de duração. **HITL Gate A.**

### Guilda da Concepção
| Agente | Étimo | Função |
|---|---|---|
| **NOÉSIS** | *νόησις*, insight intelectual | Extrai a **ideia-núcleo** e o "momento aha". Define o objetivo de aprendizagem único. |
| **PAIDEIA** | *παιδεία*, formação | Constrói o **arco didático**: gancho → intuição → formalização → recompensa. Mapeia pré-requisitos e *misconceptions*. |
| **ELENCHUS** | *ἔλεγχος*, refutação socrática | **Verificação factual/matemática** do insight e do roteiro (anti-alucinação). Bloqueia conteúdo incorreto antes do custo de render. |

### Guilda do Roteiro
| Agente | Étimo | Função |
|---|---|---|
| **RAPSODO** | *ραψῳδός*, o recitador | Escreve a **narração pt-BR** segmentada em *beats*, na voz "conversacional-mas-precisa" do estilo 3b1b. |
| **CHRONOS** | *χρόνος*, tempo | **Diretor de *pacing* (determinístico-assistido).** Estima a duração de cada *beat*, aloca `run_time` de animação, insere pausas de absorção e produz a **linha do tempo mestra**. |

### Guilda Visual
| Agente | Étimo | Função |
|---|---|---|
| **SCENOGRAPHO** | *σκηνογράφος*, cenógrafo | Produz o **scene-graph JSON** por *beat*: objetos, layout, transformações — sempre referenciando **primitivas da DSL**. |
| **CHROMA** | *χρῶμα*, cor | **Cinematografia/colorimetria.** Paleta semântica (azul=neutro, amarelo=foco, vermelho=alerta…), movimentos de câmera, hierarquia e estética do movimento. |

### Guilda da Forja
| Componente | Tipo | Função |
|---|---|---|
| **Motor MANIM** | **Determinístico (não-LLM)** | Compila o scene-graph JSON → código Manim usando a biblioteca de primitivas vetadas. **Núcleo auditável/reproduzível.** |
| **HEFESTO** | LLM (codegen controlada) | *Escape hatch* — só para primitivas inexistentes. Saída passa por *lint* + *sandbox* + render-validate-heal; primitivas aprovadas são **promovidas** à biblioteca. |
| **EChÓ** | Determinístico (orquestra TTS) | Sintetiza a narração pt-BR e devolve **durações reais** para reconciliar com CHRONOS. |

### Guilda da Renderização & QA
| Componente | Tipo | Função |
|---|---|---|
| **ÁRGOS** | Determinístico + LLM-QA | Render via Manim CLI + **QA por frame**: sobreposições, objetos fora do *canvas*, contraste, legibilidade, *jitter*. Emite relatório de defeitos. |
| **Loop de Self-Healing** | Determinístico | Conserta falhas de compilação/render/QA; reabre o estágio responsável. |
| **HARMONIA** | Determinístico | **Mux** vídeo+áudio (FFmpeg), aplica formato/aspecto e **1080p**, exporta o contêiner final. |

### Validação final
- **AISTHÉSIS** (*αἴσθησις*, percepção estética) — Validador de qualidade **anti-sycophancy**. Julga contra a rubrica "qualidade 3b1b"; pode **reprovar e devolver**. **HITL Gate C (homologação).**

---

## 6. Máquina de estados (StateGraph)

```
S0  INTAKE            → recebe brief (ideia, formato, nível, banda de duração, TTS on/off)
S1  CLASSIFICATION    → Classificador de Domínio           ──▶ [HITL Gate A]
S2  INSIGHT           → NOÉSIS
S3  PEDAGOGY          → PAIDEIA  ──▶ ELENCHUS (verificação)
S4  SCRIPT            → RAPSODO  ──▶ ELENCHUS (verificação)
S5  TIMING            → CHRONOS  ◀────────────┐ (reconciliação)
S6  STORYBOARD        → SCENOGRAPHO            │
S7  CINEMATOGRAPHY    → CHROMA   ──▶ [HITL Gate B opcional]
S8  SYNTHESIS         → Motor MANIM (+ HEFESTO se necessário)
S9  VOICE             → EChÓ  ──────────────► durações reais ─┘ (loop p/ S5 se Δ > tolerância)
S10 RENDER & QA       → ÁRGOS + Self-Healing   (loop até passar)
S11 ASSEMBLY          → HARMONIA (mux + 1080p + formato)
S12 AESTHETIC VALID.  → AISTHÉSIS              ──▶ [HITL Gate C]
                         ├─ aprovado → S13
                         └─ reprovado → roteia p/ estágio responsável
S13 DELIVERY          → MP4 final + manifesto de artefatos (auditoria)
```

**Loops de reconciliação chave**
- **S5 ↔ S9:** o tempo planejado por CHRONOS é confrontado com a duração real do TTS (EChÓ). Se |Δ| > tolerância (default 200 ms/beat), CHRONOS reajusta `run_time` e pausas.
- **S10 (Self-Healing):** falha de render → diagnóstico → correção no estágio de origem (SYNTHESIS, STORYBOARD ou CINEMATOGRAPHY) → re-render.

---

## 7. Esquemas de handoff (Pydantic) — ilustrativos

```python
class VideoBrief(BaseModel):
    ideia: str
    formato: Literal["16:9", "9:16", "1:1"]
    nivel_audiencia: Literal["fundamental", "medio", "medio_avancado", "superior"]
    banda_duracao_s: tuple[int, int] = (120, 360)
    tts_habilitado: bool = True
    idioma: str = "pt-BR"

class CoreInsight(BaseModel):
    objetivo_aprendizagem: str
    ideia_nucleo: str
    momento_aha: str
    pre_requisitos: list[str]

class Beat(BaseModel):
    id: str
    funcao_didatica: Literal["gancho","intuicao","formalizacao","recompensa"]
    narracao: str
    palavras: int
    duracao_narracao_s: float      # CHRONOS (determinístico)
    pausa_absorcao_s: float        # CHRONOS

class PrimitiveCall(BaseModel):
    primitiva: str                 # ex.: "FunctionGraphReveal"
    params: dict[str, Any]
    run_time_s: float

class SceneGraph(BaseModel):
    beat_id: str
    primitivas: list[PrimitiveCall]
    camera: CameraSpec
    paleta: PaletteRef

class RenderJob(BaseModel):
    resolucao: tuple[int,int]
    fps: int = 60
    qualidade: Literal["-qh"] = "-qh"
    seed: int
    manim_version_lock: str

class QAReport(BaseModel):
    aprovado: bool
    defeitos: list[Defeito]        # sobreposicao, off_canvas, contraste, jitter...
```

---

## 8. Exemplo de envelope de handoff

```json
{
  "versao": "1.0",
  "origem": "SCENOGRAPHO",
  "destino": "Motor MANIM",
  "schema": "SceneGraph",
  "payload": { "...": "scene-graph validado" },
  "proveniencia": { "trace_id": "lf-...", "stage": "S6" },
  "checagem": { "pydantic_ok": true, "primitivas_existentes": true }
}
```

---

## 9. O motor determinístico (núcleo auditável)

### 9.1 DSL de cena — biblioteca de primitivas Manim vetadas
A "voz visual" do 3b1b é um vocabulário finito de movimentos. THEORÍA o codifica como **primitivas parametrizadas, testadas e versionadas** (cada uma com *golden frames* de regressão):

| Primitiva (exemplos MVP) | Uso |
|---|---|
| `TitleReveal` | abertura/legenda com *fade* e *underline* |
| `NumberLineReveal` / `NumberPlaneReveal` | introdução de eixos |
| `FunctionGraphReveal` | desenho progressivo de curva |
| `TransformEquation` | morfismo entre fórmulas (LaTeX) |
| `VectorField` / `VectorTransform` | álgebra linear / campos |
| `MatrixMultiplication` | operação matricial passo a passo |
| `GeometricProof` | construção geométrica encadeada |
| `HighlightFocus` | foco semântico (cor amarela) sobre objeto |
| `CameraMove` | *pan/zoom* intencional |
| `ComplexPlaneSpiral` | rotação no plano complexo (ex.: e^(iπ)) |

> **Contrato:** SCENOGRAPHO **só** referencia primitivas existentes. Se precisar de algo novo, abre *ticket* para HEFESTO. Isso mantém a saída **determinística e reproduzível**.

### 9.2 Cálculo determinístico de tempo (CHRONOS)
```
taxa_fala_ppm   = 150            # palavras/min, pt-BR narração didática (configurável)
dur_narracao_s  = palavras / (taxa_fala_ppm / 60)
pausa_absorcao  = f(funcao_didatica)   # ex.: recompensa = 1.5s, intuicao = 0.8s
run_time_anim   = max(dur_narracao_s, soma(run_time primitivas)) + pausa_absorcao
duracao_total   = Σ run_time_anim  (validada contra banda_duracao_s do brief)
```
A duração do vídeo é **derivada do conteúdo** (tempo necessário para explicar tudo), limitada pela banda informada. Sem números mágicos: tudo rastreável.

### 9.3 Render config — formato e 1080p
| Formato | Resolução (1080p) | FPS |
|---|---|---|
| 16:9 (YouTube) | 1920 × 1080 | 60 |
| 9:16 (Reels/Shorts) | 1080 × 1920 | 60 |
| 1:1 (feed) | 1080 × 1080 | 60 |

Render: `manim -qh --resolution {W},{H} --fps 60`. Encode final via FFmpeg (H.264, `yuv420p`, CRF configurável). Tudo parametrizado por `RenderJob` — reproduzível.

### 9.4 Pipeline de assembly (HARMONIA)
Mux determinístico vídeo (Manim) + áudio (EChÓ), normalização de áudio, alinhamento por *timestamps* da linha do tempo mestra, exportação no contêiner alvo.

---

## 10. Gates HITL

- **Gate A — Classificação (S1):** o humano confirma domínio, profundidade e banda de duração antes de gastar tokens/render.
- **Gate B — Storyboard (S7, opcional):** preview textual/esquemático das cenas antes da síntese de código. Configurável (default: ligado para domínios de maior complexidade).
- **Gate C — Homologação estética (S12):** AISTHÉSIS apresenta o vídeo + rubrica; humano aprova, reprova com motivo (roteia de volta) ou aprova com ressalvas.

---

## 11. Self-healing e QA

ÁRGOS roda checagens determinísticas por frame amostrado:
- **Off-canvas:** *bounding box* fora dos limites → corrigir layout (STORYBOARD).
- **Sobreposição:** colisão de *mobjects* → reposicionar (CHROMA/STORYBOARD).
- **Contraste/legibilidade:** razão de contraste mínima (texto vs. fundo).
- **Jitter/erro de transform:** descontinuidade entre frames.
- **Sync:** *drift* narração↔animação > tolerância → CHRONOS.

Falha de **compilação** (HEFESTO) → Self-Healing aplica correção guiada por *traceback* em *sandbox*, com número máximo de tentativas antes de escalar ao humano.

---

## 12. Observabilidade (Langfuse)

- *Trace* hierárquico: `job → estágio → agente → chamada LLM/ferramenta`.
- Métricas por nó: tokens, custo, latência, número de retries do self-healing.
- *Span* dedicado ao render (tempo de render, número de frames, resolução).
- Persistência de **todos os artefatos intermediários** (brief, insight, arco, roteiro, timeline, scene-graphs, código gerado, logs de QA, manifesto) — auditoria rastreável e reproduzível.

---

## 13. Requisitos

### 13.1 Funcionais
- RF1. Aceitar *brief* com formato, nível e (opcional) banda de duração.
- RF2. Derivar duração do conteúdo, respeitando a banda.
- RF3. Gerar narração pt-BR segmentada e sincronizada.
- RF4. Compor cenas exclusivamente via DSL (codegen custom só sob *guardrails*).
- RF5. Renderizar em 1080p no formato escolhido.
- RF6. Sincronizar áudio (se TTS on) ou embutir legendas/cartelas (se TTS off).
- RF7. Entregar MP4 + manifesto de artefatos.

### 13.2 Não-funcionais
- RNF1. **Reprodutibilidade:** Manim fixado + DSL versionada + seed → output idêntico (frames) / perceptualmente idêntico (com TTS).
- RNF2. **Auditabilidade:** 100% dos *handoffs* persistidos como JSON validado.
- RNF3. **Idempotência:** re-execução de um estágio não corrompe o estado.
- RNF4. **Guardrails de custo:** orçamento de tokens por estágio; *circuit breaker* no self-healing.
- RNF5. **Isolamento:** render e codegen custom em *sandbox* Docker.

---

## 14. Stack tecnológico

- **Orquestração:** Python 3.12, LangGraph, Pydantic v2.
- **LLM dos agentes:** Anthropic Claude (saída JSON estruturada).
- **Render:** Manim Community (versão *pinned*), FFmpeg.
- **TTS pt-BR:** provedor plugável (ex.: ElevenLabs / Azure Neural / Coqui) — interface abstrata em EChÓ.
- **Observabilidade:** Langfuse.
- **Execução isolada:** Docker (sandbox de render e de codegen).
- **Persistência de artefatos:** armazenamento versionado (filesystem/objeto) + índice por `job_id`.

---

## 15. Métricas de sucesso (KPIs)

| KPI | Alvo v1.0 |
|---|---|
| Renders que passam QA na 1ª tentativa | ≥ 70% |
| Taxa de sucesso do self-healing | ≥ 85% |
| Edições humanas por vídeo (Gate C) | ≤ 2 |
| Erro de sincronia narração↔animação | < 150 ms/segmento |
| Reprodutibilidade (output idêntico) | 100% (sem TTS) |
| Score na rubrica AISTHÉSIS | ≥ 8/10 |
| Tempo médio ideia→entrega (sem HITL) | < 25 min (vídeo de ~3 min) |

---

## 16. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Codegen Manim frágil | **DSL-first**; codegen custom só sob sandbox + render-validate-heal. |
| Alucinação matemática/conceitual | **ELENCHUS** verifica antes do custo de render. |
| Custo/tempo de render alto | *Preview* em baixa qualidade no QA; full 1080p só após aprovação. |
| TTS pt-BR não-natural | Provedor plugável + reconciliação de duração; *fallback* para legendas. |
| *Scope creep* de efeitos cinematográficos | Catálogo fechado de primitivas/câmera por fase. |
| Dessincronia áudio↔vídeo | Loop determinístico S5↔S9 com tolerância configurável. |

---

## 17. Roadmap por fases

- **Fase 0 — Fundação:** biblioteca DSL (MVP de ~10 primitivas + *golden frames*), pipeline de render, schemas Pydantic, esqueleto do StateGraph, Classificador de Domínio.
- **Fase 1 — Núcleo:** concept → script → storyboard → render para 16:9, **sem TTS** (legendas). Gates A e C.
- **Fase 2 — Tempo & voz:** CHRONOS completo, EChÓ (TTS), loop de sincronia, multi-formato (9:16, 1:1).
- **Fase 3 — Cinematografia & QA:** CHROMA (câmera/paleta), ÁRGOS QA por frame, Self-Healing.
- **Fase 4 — Forja custom:** HEFESTO + ciclo de promoção de primitivas à biblioteca.
- **Fase 5 — Hardening:** Langfuse completo, guardrails de custo, batch, integração com squads parceiros.

---

## 18. Anexo — fluxo do caso canônico

> **Brief:** "Intuição de e^(iπ) = −1; formato 9:16; médio avançado."

1. **Classificador:** domínio=matemática, complexidade=Complicado, banda=180–300 s → *Gate A ok*.
2. **NOÉSIS:** ideia-núcleo = "multiplicar por e^(iθ) é girar no plano complexo"; aha = "andar π radianos = meia volta = −1".
3. **PAIDEIA:** gancho (o que significa elevar à potência imaginária?) → intuição (rotação) → formalização (espiral/círculo unitário) → recompensa (π chega em −1). **ELENCHUS** valida.
4. **RAPSODO:** narração pt-BR por *beat*.
5. **CHRONOS:** durações por *beat*, pausa de 1,5 s na recompensa, total ≈ 230 s.
6. **SCENOGRAPHO:** `ComplexPlaneReveal` → `ComplexPlaneSpiral(theta=π)` → `HighlightFocus(point=-1)`.
7. **CHROMA:** azul (plano), amarelo (vetor girante), zoom suave no ponto −1.
8. **Motor MANIM:** compila para código a partir das primitivas.
9. **EChÓ:** TTS; reconcilia durações (Δ < tolerância).
10. **ÁRGOS + Self-Healing:** render 1080×1920, QA, autocorreção.
11. **HARMONIA:** mux + encode 1080p 9:16.
12. **AISTHÉSIS:** rubrica ≥ 8 → *Gate C* → **entrega do MP4 + manifesto**.

---

*Documento sujeito a refinamento por escopo (gates A/B/C) e calibração de parâmetros (taxa de fala, tolerâncias de sync, paleta).*

---

*Adaptado para o squad THEORÍA. Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.*
