# PALIMPSESTO Squad

### Sistema multiagente de reconstrução contextual imersiva (Filosofia × História × Geografia × Política)

> *Palimpsesto* (gr. *palímpsēstos*, "raspado de novo"): pergaminho reaproveitado em que, sob a escrita nova, as camadas antigas ainda transparecem. Este squad raspa e revela essas camadas, uma a uma, e as recompõe numa experiência de imersão total.

**Versão:** 1.1.0 · **Licença:** MIT · **Criador:** Marcio Bisognin (@marciobisognin)
**Baseline arquitetural:** OMNISCIENT v7.0 (contratos SACP, HITL gate, Cynefin entry-gate, observabilidade Langfuse)

---

## Ideia central

PALIMPSESTO recebe **qualquer objeto de conhecimento histórico-cultural** (um trecho da Bíblia, um evento, uma personalidade, um conceito, um lugar) e devolve não uma explicação, mas uma **reconstrução verificada do mundo ao redor do objeto** — datado, situado geograficamente, traduzido na semântica original da língua falada, encharcado da política, da religião e das ideias da época — e finalmente **narrado em segunda pessoa, no presente histórico**.

Dois compromissos inegociáveis:
1. **Imersão máxima** — a saída transporta, não lista.
2. **Rigor epistemológico máximo** — nada de anacronismo, nada de detalhe inventado disfarçado de fato. Toda afirmação carrega grau de certeza explícito.

## Arquitetura em 4 camadas

```
CAMADA 0 — Triador (classifica, define profundidade e trilhas)
        ↓
CAMADA 1 — CHRONOS · TERRA · VERBUM · ETHOS · KRATOS · NUMEN · NOÛS (paralelo)
        ↓
CAMADA 2 — ÁGON (contra-perspectiva) → ELENCHUS (verificação) → O Tecelão (curadoria)
        ↓ (HITL gate opcional para temas sensíveis)
CAMADA 3 — AEDO (imersão) + PONTE (conexão com o presente)
```

Fluxo: **Camada 1 reconstrói → ÁGON pluraliza → ELENCHUS verifica e poda → Camada 3 só então narra.** A imersão jamais ocorre sobre material não verificado, e a reconstrução nunca repousa numa única perspectiva.

## Agentes

| Agente | Camada | Papel |
|---|---|---|
| `triador` | 0 | Classifica o objeto e monta o plano de escavação (`SACP-IN`) |
| `chronos` | 1 | Estratígrafo do tempo — separa evento / registro / recepção |
| `terra` | 1 | Cartógrafo — geografia física e humana como vetor de causalidade |
| `verbum` | 1 | Filólogo — língua original, campo semântico, o que a tradução apaga |
| `ethos` | 1 | Etnógrafo do cotidiano — mentalidades e vida material |
| `kratos` | 1 | Analista de poder — instituições, economia, interesses |
| `numen` | 1 | Historiador das religiões — crença, ritual, sagrado |
| `nous` | 1 | Historiador das ideias — episteme e cosmovisão da época |
| `agon` | 2 | Advogado dos vencidos — contra-perspectiva, contrafactuais, viés de fonte |
| `elenchus` | 2 | Guardião das fontes — atribui certeza, poda anacronismo e alucinação |
| `tecelao` | 2 | Curador-editor/orquestrador — monta o dossiê verificado |
| `aedo` | 3 | Imersor — narra em 2ª pessoa, presente histórico, só com material verificado |
| `ponte` | 3 | Conexão com o presente — ressonâncias sem anacronismo retroativo |

## Níveis de profundidade

- **Nível 1 — Vislumbre:** 3 camadas-chave (CHRONOS+TERRA+VERBUM) + abertura imersiva curta (Reels/Manim).
- **Nível 2 — Imersão (default):** todas as trilhas pertinentes + narração completa + ponte.
- **Nível 3 — Escavação:** todas as camadas, divergências de escolas, aparato de fontes, notas filológicas extensas.

## Formato da entrega (Nível 2)

1. A Travessia (AEDO) · 2. Os Três Tempos (CHRONOS) · 3. A Terra (TERRA) · 4. As Palavras (VERBUM) · 5. A Vida (ETHOS) · 6. O Poder e o Sagrado (KRATOS+NUMEN+ÁGON) · 7. O Pensável (NOÛS) · 8. A Ponte (PONTE) · 9. Aparato (opcional, Nível 3).

Marcadores de certeza inline (`[consenso]`, `[hipótese]`, `[recriação atmosférica]`) acompanham afirmações de risco. Ver `templates/formato-entrega.md`.

## Contratos de dados

- `templates/sacp-in.schema.json` — Triador → Camada 1
- `templates/claim.schema.json` — Camada 1 / ÁGON → ELENCHUS
- `templates/verified-claim.schema.json` — ELENCHUS → O Tecelão
- `templates/dossier.schema.json` — O Tecelão → AEDO/PONTE

## Guardrails

- **Anti-alucinação:** AEDO só usa material verificado por ELENCHUS.
- **Anti-anacronismo:** todo termo/conceito moderno passa pelo filtro de ELENCHUS.
- **Honestidade sobre lacunas:** "não se sabe" é saída válida.
- **Temas sensíveis:** HITL gate disponível para religião viva, genocídios, disputas identitárias, política contemporânea.
- **Multiperspectiva:** ÁGON garante o olhar do governado/marginal como etapa estrutural.
- **Disputa preservada:** divergência de escolas aparece como tal, nunca achatada em falso consenso.

## Estrutura de pastas

```
palimpsesto-squad/
├── squad.yaml
├── agents/          (13 agentes)
├── tasks/           (8 tasks do pipeline)
├── workflows/       (palimpsesto-pipeline.yaml)
├── templates/       (4 schemas JSON + formato de entrega)
├── examples/        (exemplo trabalhado Mt 5,5)
└── references/      (PRD original)
```

## Métricas de sucesso (v1)

| Objetivo | Métrica | Meta |
|---|---|---|
| Imersão | avaliação humana "senti-me transportado" | ≥ 4,3 |
| Rigor | % afirmações com certeza explícita | 100% |
| Anti-anacronismo | anacronismos por amostragem | < 1 a cada 20 respostas |
| Cobertura multidisciplinar | camadas ativadas em objetos ricos | ≥ 4/5 |
| Rastreabilidade | afirmações de alto risco com fonte | ≥ 90% |

## Roadmap

- **Fase 0 — PoC:** Triador + 4 trilhas (CHRONOS, VERBUM, KRATOS, NUMEN) + ELENCHUS + AEDO, sem RAG.
- **Fase 1 — Completo sem RAG:** 7 trilhas + Tecelão + PONTE + 3 níveis de profundidade + observabilidade.
- **Fase 2 — RAG ancorado:** base de fontes curada para ELENCHUS.
- **Fase 3 — HITL + variantes de saída:** export roteiro Manim/RPG.
- **Fase 4 — Auto-avaliação:** loop de auditoria de anacronismo e calibração de certeza.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
