# SCRIPTORIUM Squad

> Sistema multiagente de **produção acadêmica fim-a-fim com integridade verificável**.
> A IA é seu copiloto, não o piloto.

**`scriptorium-squad`** · versão `1.0.0` · status `production-ready` · idioma `pt-BR / EN / bilíngue`
**Arquitetura-base:** OMNISCIENT v7.0 (Cynefin Classifier, contratos SACP, Turing Guild, observabilidade Langfuse) · **Orquestração:** LangGraph StateGraph

---

## O que é

O SCRIPTORIUM conduz um manuscrito acadêmico **da pergunta de pesquisa ao
artefato publicável** (Markdown / DOCX / PDF tipografado), passando por revisão
por pares simulada multi-perspectiva e **dois gates de integridade não-puláveis**.

O princípio fundador é **não-autônomo**: o pesquisador humano permanece como
piloto; o squad executa o trabalho braçal verificável (rastrear referências,
formatar citações, checar consistência lógica, validar a existência de fontes
contra índices bibliográficos reais) e **se recusa a preencher lacunas com
memória paramétrica**. Toda alegação não-fundamentada vira a etiqueta
`[LACUNA DE MATERIAL]` — nunca prosa inventada.

### Diferenciais
- Verificação **determinística** de existência de citação contra 4 índices
  (Semantic Scholar + OpenAlex + Crossref + arXiv) antes de qualquer revisão por LLM.
- Auditoria de **fidelidade alegação↔fonte** (a citação realmente sustenta a frase?).
- **Protocolo anti-bajulação** no contraditório (concessão só acima de um limiar de evidência).
- **Dossiê de Proveniência** versionado que permite retomar a execução em sessão nova.
- **Cross-model**: um segundo modelo local (via Ollama) audita o primeiro sem custo de API.

---

## Topologia (5 guildas / 29 agentes + 2 papéis de gate)

```
   Entrada ─▶ TRIADOR-CYNEFIN (gate)
                 │
   G1 INVESTIGA ─▶ G2 ESCRITA ─[✓ 2.5]─▶ G3 PARECER ─▶ G2 REVISÃO
       ▲                                      │ decisão       │
       │   Dossiê de Proveniência (estado)    ▼               ▼
       └──────────────────────  [✓ 4.5] integridade final ─▶ FINALIZAÇÃO ─▶ DOSSIÊ-PROCESSO
```

- **G0 — Maestria** (5): `maestro`, `rastreador-de-estado`, `guarda-de-auto-cura`, `observador-de-colaboracao`, `sentinela-de-conformidade`.
- **Gate de entrada**: `triador-cynefin`.
- **G1 — Investigação** (8): `arquiteto-da-questao`, `cartografo-metodologico`, `curador-bibliografico`, `verificador-de-fontes`, `sintetizador`, `meta-analista`, `critico-adversarial`, `auditor-de-vieses`.
- **G2 — Escrita** (9): `triador-de-entrada`, `arquiteto-de-estrutura`, `construtor-de-argumentos`, `redator`, `conformador-de-citacoes`, `resumista-bilingue`, `ilustrador-de-dados`, `calibrador-de-estilo`, `treinador-de-revisao`.
- **G3 — Parecer** (7): `analista-de-dominio`, `editor-chefe`, `parecerista-metodologico`, `parecerista-de-dominio`, `parecerista-interdisciplinar`, `contraditor-editorial`, `sintetizador-editorial`.
- **Integridade** (compartilhada G0/G3): `auditor-de-integridade` — gates 2.5 e 4.5.

> A guilda transversal G0 envolve todas as demais; o `observador-de-colaboracao`
> é **deliberadamente silenciado nos gates 2.5 e 4.5** para não diluir a checagem de integridade.

---

## Máquina de estados (10 estágios)

| Estágio | Guilda | Gate / Checkpoint |
|---|---|---|
| 1. Investigar | G1 | 🧑 confirma pergunta+método · 🤖 verificação 4-índices, anti-bajulação |
| 2. Escrever | G2 | 🧑 aprova esqueleto · 🤖 anti-vazamento, VLM, estilo |
| **2.5 Integridade** | Auditoria | ✓ Checklist 7 Modos + ack humano · FALHA → auto-cura (máx. 3) |
| 3. Parecer | G3 | 🧑 revê decisão · 🤖 limiar de concessão, sprint contract cego |
| 3→4 Coaching | Editor-Chefe | 🧑 pode "só conserte" e pular (máx. 8) |
| 4. Revisar | G2 | 🧑 confirma mudanças · 🤖 trajetória de pontuação |
| 3'. Re-parecer | G3 | cap rígido: máx. 1 re-revisão, 2 loops |
| 4'. Re-revisar | G2 | 🧑 confirma congelamento |
| **4.5 Integridade final** | Auditoria | ✓ tolerância zero; 7 modos + alegações 100% |
| 5. Finalizar | G2 | 🧑 escolhe formato · *gate* terminal recusa alegação não-sustentada |
| 6. Dossiê-Processo | G0 | 🧑 confirma idioma e revê colaboração |

---

## Primitivas de honestidade

1. **Verificação determinística de citação** (4 índices, cache 90d) — `scripts/verify_citations.py`.
2. **Auditoria de fidelidade alegação↔fonte** (âncora de 3 camadas + LLM-como-juiz).
3. **Protocolo de Limiar de Concessão** (anti-bajulação) — `scripts/concession_audit.py`.
4. **Protocolo anti-vazamento** (`[LACUNA DE MATERIAL]`).
5. **Checklist de 7 Modos de Falha** (gates 2.5 / 4.5).
6. **Cross-model gratuito** (`SCR_CROSS_MODEL=1`, via Ollama).

---

## Como usar

### Ativação como squad (LLM)
1. Leia `squad.yaml` e assuma a persona do `maestro` (orquestrador).
2. Siga `workflows/scriptorium-pipeline.yaml` (10 estágios, gates 2.5/4.5 não-puláveis).
3. Cada handoff entre guildas é um JSON validado contra os contratos em `templates/`.

### Scripts determinísticos (Python 3.11+, sem dependências externas)
```bash
# Validar as fixtures de contrato contra os schemas
python3 scripts/validate_contracts.py

# Verificação determinística de existência de citação (offline, via cache local)
python3 scripts/verify_citations.py \
    --citations examples/fixtures/citations_input.json \
    --cache examples/fixtures/index_cache.json

# Auditoria anti-bajulação do contraditório
python3 scripts/concession_audit.py --log examples/fixtures/contraditorio_log.json
```

> Os scripts rodam **offline**: o `verify_citations.py` consulta um *cache* local
> que, em produção, é alimentado pelos 4 índices reais (Semantic Scholar +
> OpenAlex + Crossref + arXiv) com TTL de 90 dias.

---

## Contratos (estilo SACP, em `templates/`)
`PassaporteDossie` · `BriefingDeQuestao` · `VerificacaoCitacao` · `RelatorioIntegridade` · `ContratoDeParecer` · `MatrizDeRastreabilidade`.

## Critérios de aceite (resumo)
- 100% das referências passam pela checagem 4-índices; nenhuma `inexistente` na saída sem override humano.
- Auditoria de fidelidade (quando ligada): FNR < 0,15 e FPR < 0,10.
- Anti-bajulação: nenhuma concessão com pontuação < 4.
- Gates 2.5 e 4.5 não-puláveis; tolerância zero em 4.5.
- Custo-alvo: ~US$ 4–6 por artigo de ~15k palavras (calibrar com Langfuse).

## Stack open-source
Semantic Scholar / OpenAlex / Crossref / arXiv · Pandoc · Tectonic · Typst · CSL/citeproc · GROBID · Unpaywall · Zotero translation-server · PyMuPDF / Marker / Nougat · sentence-transformers / RapidFuzz · Chroma / Qdrant / FAISS · LangGraph · Langfuse · Ollama · Ragas / DeepEval · LanguageTool · Manim · gitleaks · OpenReview API.

---

Ver detalhes operacionais em [`docs/guia-de-uso.md`](docs/guia-de-uso.md) e o PRD completo em [`references/PRD_Squad_SCRIPTORIUM_v1.0.md`](references/PRD_Squad_SCRIPTORIUM_v1.0.md).

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
