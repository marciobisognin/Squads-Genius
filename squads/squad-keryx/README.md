# KÊRYX — O Arauto (Κῆρυξ)

> **Gerador autônomo de carrosséis educativos para Instagram.**
> Versão 1.1.0 · Ecossistema OMNISCIENT v7.0 · Licença MIT.

Squad multi-agente (LangGraph StateGraph) que transforma um **pedido mínimo** —
_"quero um carrossel com N posts"_ — em um **carrossel pronto-para-publicar**, visualmente fiel
ao padrão de referência, factualmente checado e homologável. O squad decide o resto: sorteia
tema(s), pesquisa/ideia o conteúdo, estrutura em cards, redige os bullets, dirige a arte e
**renderiza os slides finais** (PNG + PDF), passando por gates de QA e homologação humana.

**Princípio-mestre:** o LLM gera **conteúdo estruturado (JSON)**; **design, layout e texto final
são determinísticos** — auditáveis e reprodutíveis. A única etapa não-determinística (ilustração
do Trilho B) é **isolada, com seed e validada por gate humano**; o texto educativo **nunca** é
renderizado pela IA de imagem.

## Dois trilhos de saída
- **Trilho A — Cards/Infográfico** (`baoyu-infographic`): alta densidade, `layout × estilo`
  combináveis, **100% determinístico** (HTML+CSS → Playwright → PNG 1080×1350 + PDF).
- **Trilho B — Quadrinho de conhecimento** (`baoyu-comic`): mini-HQ educativa estilo _Logicomix_
  (storyboard determinístico + ilustração generativa _gated_ + letterização vetorial).

## Domínios
Tecnologia · Produtividade · Gestão da vida · Livros & Clássicos (literatura, ficção científica,
filosofia, matemática, física) — isolados, combinados ou em mix aleatório.

## Elenco de agentes
| Agente | Papel | Trilho |
|---|---|---|
| **HEGEMON** | Orquestrador + Cynefin entry gate + HITL final | A/B |
| **KLEROS** | Curadoria aleatória (tema/formato/estilo) com seed e anti-repetição | A/B |
| **HISTOR** | Pesquisa/ideação de conteúdo ancorada no cotidiano_hook | A |
| **TAXIS** | Estruturação em cards (colunas/seções/bullets) | A |
| **LACONICUS** | Copy em imperativo curto + emoji do título | A |
| **APELLES** | Direção de arte + seleção de estilo baoyu | A/B |
| **HEPHAISTOS** | Render determinístico + letterização vetorial (sem LLM) | A/B |
| **KANON** | QA visual (overflow, contraste, grid) + auto-fit (sem LLM) | A/B |
| **MOMUS** | QA factual + anti-sycophancy | A/B |
| **RHAPSODOS** ⬡ | Roteirista/storyboard (princípio ohmsha) | B |
| **EIDOLON** ⬡ | Character sheet + style bible (consistência) | B |
| **ZEUXIS** ⬡ | Ilustrador (IA de imagem, sem texto embutido) | B |

⬡ = ativados somente no Trilho B.

## Fluxo "feliz"
1. Input: `/keryx gerar carrossel, 5 slides` (opcional: domínio, tom, seed, formato).
2. KÊRYX classifica (Cynefin), sorteia tema(s), produz e renderiza.
3. **Gate HITL** apresenta preview (PNGs + textos + flags) → aprova / ajusta / regenera.
4. Entrega: `slide_01.png … slide_NN.png` + `carrossel.pdf` + `manifest.json`.

## Uso rápido (scripts determinísticos)
```bash
cd squads/squad-keryx
python3 scripts/kleros_curation.py --n-slides 5 --seed 42 --mode single_theme
python3 render/tokens.py
python3 scripts/validate_carousel_spec.py --spec examples/exemplo_carousel_spec.json
python3 tests/test_kleros_determinism.py && python3 tests/test_spec_validation.py
```

## Estrutura
```
squad-keryx/
├── squad.yaml                 # manifesto
├── agents/                    # HEGEMON, KLEROS, HEPHAISTOS, KANON, MOMUS + infographic/ + comic/
├── tasks/                     # 13 tasks atômicas por etapa
├── workflows/                 # full_keryx_pipeline + infographic_track + comic_track
├── schemas/sacp_schemas.py    # contratos SACP (Pydantic + fallback)
├── render/                    # tokens.py (verdade visual), engine.py, letterer.py, templates/, styles/
├── scripts/                   # kleros_curation.py, validate_carousel_spec.py
├── config/                    # defaults, domain_weights, baoyu_presets
├── examples/ · docs/ · tests/ · outputs/
```

## Critérios de aceite (DoD) — resumo
- Input `n_slides` + opcionais gera carrossel sem rodada extra.
- PNGs 1080×1350 + `carrossel.pdf` + `manifest.json`.
- Aderência ≥95% (KANON); overflow = 0.
- Mesma `seed`+`spec` ⇒ mesmo `render_hash` (determinismo verde).
- MOMUS sem flags críticas; HITL com preview funcional.
- Trilho B: roteiro → character sheet → arte → letterização → PDF, com dois gates HITL e
  texto dos balões 100% nítido/correto.

## Roadmap
F0 esqueleto determinístico · F1 conteúdo+curadoria · F2 QA+self-healing · F3 confiabilidade+HITL ·
F4 biblioteca de estilos baoyu · F5 Trilho B (quadrinho) · F6 caption + publicação (futuro).

## Limitações & IP
Veja `docs/limitacoes.md` e `NOTICE.md`. Estilos baoyu (MIT) reimplementados; branding sempre do
usuário; arte original (sem imitar artistas vivos nomeados).

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
