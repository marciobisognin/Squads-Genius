# PRD — Squad SCRIPTORIUM v1.0
### Sistema multiagente de produção acadêmica fim-a-fim com integridade verificável
**Arquitetura-base:** OMNISCIENT v7.0 · **Padrão de orquestração:** LangGraph StateGraph · **Idioma de operação:** PT-BR / EN / bilíngue

---

## 0. Nota de propriedade intelectual

Este PRD é uma **re-arquitetura independente** de uma categoria de problema pública (pipeline acadêmico assistido por IA com *gates* de integridade e *human-in-the-loop*). Nenhum nome de agente, nome de modo, esquema de contrato, texto de prompt ou nomenclatura interna de qualquer suíte de terceiros foi reutilizado. Os mecanismos descritos a seguir são reformulados a partir de primeiros princípios e dos seus próprios padrões OMNISCIENT v7.0 (Cynefin Classifier, contratos SACP, Turing Guild, observabilidade Langfuse). As referências acadêmicas citadas (modos de falha de pipelines autônomos, alucinação de citações em escala de corpus, profundidade de colaboração pedagógica) são fontes científicas públicas e podem ser citadas livremente. Ferramentas open-source são usadas sob suas próprias licenças permissivas.

---

## 1. Sumário executivo

**SCRIPTORIUM** é um squad de 5 guildas (29 agentes) que conduz um manuscrito acadêmico do enquadramento da pergunta de pesquisa até o artefato publicável (Markdown / DOCX / PDF tipografado), passando por revisão por pares simulada multi-perspectiva e dois *gates* de integridade não-puláveis.

O princípio fundador é deliberadamente **não-autônomo**: o pesquisador humano permanece como piloto; o squad executa o trabalho braçal verificável (rastrear referências, formatar citações, checar consistência lógica, validar existência de fontes contra índices bibliográficos reais) e **se recusa a preencher lacunas com memória paramétrica**. Toda alegação não-fundamentada vira uma etiqueta `[LACUNA DE MATERIAL]`, nunca prosa inventada.

**Diferenciais sobre automação ingênua:**
- Verificação determinística de existência de citação contra 4 índices (Semantic Scholar + OpenAlex + Crossref + arXiv) antes de qualquer revisão por LLM.
- Auditoria de fidelidade alegação↔fonte (a citação realmente sustenta a frase?).
- Protocolo anti-bajulação no contraditório (concessão só acima de um limiar de evidência).
- Dossiê de Proveniência versionado que permite retomar a execução em sessão nova.
- Cross-model: um segundo modelo (local, via Ollama) audita o primeiro sem custo de API.

---

## 2. Problema e justificativa

### 2.1 O custo da automação total
Pipelines de pesquisa totalmente autônomos herdam um conjunto recorrente de modos de falha documentados na literatura (Lu et al., 2026, *Nature* 651:914–919, sobre sistemas autônomos de pesquisa): bugs de implementação que passam pela auto-revisão, resultados alucinados, dependência de atalhos, bug reenquadrado como “insight”, fabricação de metodologia, alucinação de citações e **trava de enquadramento** (o sistema só ataca argumentos dentro do frame que ele mesmo fixou, nunca questiona as premissas).

### 2.2 A escala do problema de citação
Auditorias recentes em corpus (Zhao et al., 2026, arXiv:2605.07723) estimam dezenas de milhares de citações alucinadas por ano em pré-prints, incluindo o caso mais perigoso: **referências reais usadas para sustentar afirmações que a fonte não faz**. Verificar que o DOI existe não basta; é preciso verificar que a fonte *diz o que a frase afirma*.

### 2.3 Tese do SCRIPTORIUM
*Um pesquisador humano aumentado por IA evita esses modos de falha melhor do que humano ou IA isolados.* O squad torna os limites estruturais da IA **visíveis e gerenciáveis** por meio de *checkpoints* explícitos, em vez de fingir que não existem.

---

## 3. Arquitetura geral (mapeada ao OMNISCIENT v7.0)

| Componente OMNISCIENT v7.0 | Realização no SCRIPTORIUM |
|---|---|
| **Cynefin Classifier (gate de entrada)** | `TRIADOR-CYNEFIN` classifica a demanda em *Clear / Complicated / Complex / Chaotic* e roteia o modo de operação (ex.: revisão sistemática PRISMA → Complicated; exploração de tese aberta → Complex). |
| **Contratos de handoff SACP (JSON)** | Esquemas `pydantic` versionados (`PassaporteDossiê`, `BriefingDeQuestão`, `MatrizDeRastreabilidade`, `ContratoDeParecer`). Todo handoff entre guildas é um JSON validado em runtime. |
| **LangGraph StateGraph** | Máquina de estados de 10 estágios com *conditional edges* (decisões Aceitar/Revisão Menor/Maior/Rejeitar) e *cycles* limitados (cap de 2 loops de revisão). |
| **Turing Guild (loop de auto-cura)** | `Guilda de Auto-Cura`: ao detectar falha em *gate* de integridade, regenera o artefato com diagnóstico estruturado (máx. 3 tentativas) antes de escalar ao humano. |
| **HITL gates** | 10 *checkpoints* humanos (8 decisão + 2 *ack* de integridade), nenhum pulável nos estágios 2.5 e 4.5. |
| **Observabilidade LangSmith/Langfuse** | Tracing por nó, custo por token/estágio, métricas de concessão e bajulação, trajetória de pontuação. |

### 3.1 Topologia de guildas

```
                         ┌─────────────────────────┐
   Entrada do usuário ──▶│  TRIADOR-CYNEFIN (gate)  │
                         └────────────┬─────────────┘
                                      ▼
  ┌──────────────┐   ┌──────────────┐  G2.5  ┌──────────────┐   ┌──────────────┐
  │ G1 INVESTIGA │──▶│ G2 ESCRITA   │──[✓]──▶│ G3 PARECER   │──▶│ G4 REVISÃO   │
  │ (8 agentes)  │   │ (9 agentes)  │ integr.│ (7 agentes)  │◀──│ (re-entrada) │
  └──────────────┘   └──────────────┘        └──────┬───────┘   └──────┬───────┘
         ▲                                          │ decisão          │
         │  Dossiê de Proveniência (estado global)  ▼                  ▼
         └──────────────────────────────────  G4.5 [✓] integridade final ──▶ FINALIZAÇÃO ──▶ DOSSIÊ-PROCESSO
```

Guilda transversal **G0 — MAESTRIA** (orquestração + observabilidade + auto-cura) envolve todas as demais e nunca é pulada, exceto que o *Observador de Colaboração* é deliberadamente **silenciado nos gates obrigatórios 2.5 e 4.5** para não diluir a checagem de integridade.

---

## 4. Roster de agentes (29 agentes, nomenclatura própria)

### G0 — Guilda de Maestria (transversal, 5 agentes)
| Agente | Responsabilidade |
|---|---|
| `MAESTRO` | Orquestrador LangGraph; resolve *conditional edges*; aplica caps de loop. |
| `RASTREADOR-DE-ESTADO` | Mantém o Dossiê de Proveniência; serializa/desserializa estado entre sessões. |
| `GUARDA-DE-AUTO-CURA` | Loop Turing: diagnostica falha de gate e regenera artefato (máx. 3 tentativas). |
| `OBSERVADOR-DE-COLABORAÇÃO` | Pontua a profundidade da colaboração humano-IA em 4 dimensões; **apenas consultivo, nunca bloqueia**. Baseado em Wang & Zhang (2026), IJETHE 23:11. |
| `SENTINELA-DE-CONFORMIDADE` | Roda checklists de conformidade (ex.: PRISMA para revisão sistemática; diretrizes de divulgação de uso de IA por *venue*). |

### G1 — Guilda de Investigação (8 agentes) · acesso a dados: `bruto`
| Agente | Responsabilidade |
|---|---|
| `ARQUITETO-DA-QUESTÃO` | Refina pergunta de pesquisa por diálogo maiêutico; produz Briefing de Questão. |
| `CARTÓGRAFO-METODOLÓGICO` | Desenha o blueprint metodológico e a hierarquia de evidência. |
| `CURADOR-BIBLIOGRÁFICO` | Busca/triagem da literatura; lê corpus pré-curado do usuário (fluxo *corpus-primeiro, busca-preenche-lacuna*). |
| `VERIFICADOR-DE-FONTES` | Verificação determinística de existência de citação (4 índices). |
| `SINTETIZADOR` | Síntese narrativa anti-vazamento; etiqueta `[LACUNA DE MATERIAL]`. |
| `META-ANALISTA` | Análise quantitativa/qualitativa agregada quando aplicável. |
| `CRÍTICO-ADVERSARIAL` | Contraditório com Protocolo de Limiar de Concessão (anti-bajulação). |
| `AUDITOR-DE-VIESES` | Avalia risco de viés e lacunas éticas das fontes. |

### G2 — Guilda de Escrita (9 agentes) · acesso a dados: `redigido`
| Agente | Responsabilidade |
|---|---|
| `TRIADOR-DE-ENTRADA` | Classifica a demanda de escrita e configura o registro do artigo. |
| `ARQUITETO-DE-ESTRUTURA` | Constrói o esqueleto (IMRaD, revisão temática, estudo de caso, *policy brief* etc.). |
| `CONSTRUTOR-DE-ARGUMENTOS` | Mapa de argumentos; encadeamento lógico. |
| `REDATOR` | Escreve o draft com calibração de estilo na voz do autor. |
| `CONFORMADOR-DE-CITAÇÕES` | Conversão entre formatos (APA 7 / IEEE / Chicago / MLA / Vancouver) via CSL. |
| `RESUMISTA-BILÍNGUE` | Abstract bilíngue (PT-BR + EN). |
| `ILUSTRADOR-DE-DADOS` | Gera figuras; verificação visual (VLM) de fidelidade caption↔dados. |
| `CALIBRADOR-DE-ESTILO` | Aprende a voz do autor de trabalhos anteriores; *Writing Quality Check* (detecta padrões “de máquina”). |
| `TREINADOR-DE-REVISÃO` | Coaching maiêutico para incorporar pareceres. |

### G3 — Guilda de Parecer (7 agentes) · acesso a dados: `somente-verificado`
| Agente | Responsabilidade |
|---|---|
| `ANALISTA-DE-DOMÍNIO` | Autodetecta a área e configura 3 pareceristas adaptativos. |
| `EDITOR-CHEFE` | Conduz a decisão editorial e o coaching de revisão. |
| `PARECERISTA-METODOLÓGICO` | Rigor de método, validade, estatística. |
| `PARECERISTA-DE-DOMÍNIO` | Contribuição e estado da arte da área. |
| `PARECERISTA-INTERDISCIPLINAR` | Perspectiva transversal e generalização. |
| `CONTRADITOR-EDITORIAL` | Ataque adversarial ao manuscrito, com intensidade preservada entre rodadas. |
| `SINTETIZADOR-EDITORIAL` | Protocolo mecânico de 3 passos para consolidar pareceres em decisão. |

### Guilda de Integridade (compartilhada G0/G3) · 2.5 e 4.5
| Agente | Responsabilidade |
|---|---|
| `AUDITOR-DE-INTEGRIDADE` | Executa o Checklist de 7 Modos de Falha + auditoria de fidelidade alegação↔fonte. |

---

## 5. Máquina de estados (10 estágios)

| Estágio | Guilda/Modo | Artefato produzido | Gate / Checkpoint |
|---|---|---|---|
| **1. INVESTIGAR** | G1 (completo/maiêutico/revisão-sistemática/checagem-de-fatos/scan-comparativo/rápido) | Briefing de Questão; Blueprint Metodológico; Bibliografia Anotada (verificada); Relatório de Síntese | 🧑 Humano confirma pergunta + método. 🤖 Verificação 4-índices; hierarquia de evidência; anti-bajulação no contraditório |
| **2. ESCREVER** | G2 (completo/plano/só-esboço/conversão/divulgação) | Esqueleto; Mapa de Argumentos; Draft; Abstract bilíngue; Figuras; Lista de Citações | 🧑 Humano aprova esqueleto antes da redação. 🤖 Anti-vazamento; verificação VLM de figura; calibração de estilo |
| **2.5 INTEGRIDADE** | Auditoria (não-pulável) | Dossiê de Proveniência (obrigatório); Relatório de Verificação de Alegações (amostra 30%, mín. 10) | ✓ Checklist 7 Modos + *ack* humano. FALHA → auto-cura (máx. 3 rodadas) |
| **3. PARECER** | G3 (completo/guiado/rápido/foco-método/calibração) | Pacote de 5 pareceres (Editor + 3 pareceristas + Contraditor) + Decisão Editorial + Roteiro de Revisão | 🧑 Humano revê decisão. 🤖 Limiar de concessão; *sprint contract* (parecer cego antes de ver o manuscrito) |
| **3→4 COACHING** | Editor-Chefe (maiêutico) | Estratégia de revisão (diálogo, máx. 8 rodadas) | 🧑 Humano pode dizer “só conserte” e pular |
| **4. REVISAR** | G2 (revisão) | Resposta ponto-a-ponto; Draft revisado; Relatório de Deltas | 🧑 Humano confirma mudanças. 🤖 Rastreamento de trajetória de pontuação (regressão é sinalizada) |
| **3'. RE-PARECER** | G3 (re-revisão, time enxuto) | Checklist de resposta + Matriz de Rastreabilidade (verifica cada alegação do autor) | 🧑 Humano revê. Cap rígido: máx. 1 re-revisão, 2 loops no total |
| **3'→4' COACHING** | Editor-Chefe | Diálogo sobre trade-offs residuais (máx. 5 rodadas) | 🧑 Humano pode pular |
| **4'. RE-REVISAR** | G2 | Draft final (conteúdo congelado) | 🧑 Humano confirma congelamento; sem novo loop |
| **4.5 INTEGRIDADE FINAL** | Auditoria (não-pulável, tolerância zero) | Dossiê atualizado (`VERIFICADO`); Verificação de Alegações (100%) | ✓ Re-execução profunda dos 7 modos; qualquer suspeita pendente deve ser RESOLVIDA |
| **(opt-in) 4→5 AUDITORIA-DE-FIDELIDADE** | Auditoria | Resultados de auditoria por citação; deriva de alegação; afirmações não-citadas | ✓ LLM-como-juiz por citação contra excerto recuperado; *gate* terminal no formatador |
| **5. FINALIZAR** | G2 (formatação/divulgação) | MD; DOCX (Pandoc); LaTeX/Typst; PDF (Tectonic); Declaração de Uso de IA | 🧑 Humano escolhe formato. *Gate* terminal recusa saída com alegação não-sustentada pendente |
| **6. DOSSIÊ-PROCESSO** | G0 | Registro do Processo; Auto-Reflexão (taxa de concessão, risco de bajulação); trajetória de pontuação; capítulo de Profundidade de Colaboração | 🧑 Humano confirma idioma e revê qualidade da colaboração |

---

## 6. Primitivas de honestidade (núcleo de qualidade)

### 6.1 Verificação determinística de existência de citação
Antes de qualquer revisão por LLM, cada referência é cruzada contra **Semantic Scholar + OpenAlex + Crossref + arXiv**. Status por citação: `verificada` / `não-resolvida` / `inexistente` (apenas quando um DOI/arXiv-ID *exato* falha — citações regionais/não-indexadas ficam `não-resolvida` e não bloqueiam). Cache SQLite com TTL de 90 dias. Casamento de título por *fuzzy matching* (RapidFuzz, limiar configurável) e dedup semântica por `sentence-transformers`.

### 6.2 Auditoria de fidelidade alegação↔fonte
Cada citação carrega uma **âncora de três camadas** (`quote` / `page` / `section`). O `AUDITOR-DE-INTEGRIDADE` recupera o excerto ancorado e julga, por LLM, se a fonte realmente sustenta a frase. Classes de alta severidade (alegação-não-sustentada, referência-fabricada, violação-de-restrição) **recusam a saída** no *gate* terminal do formatador.

### 6.3 Protocolo de Limiar de Concessão (anti-bajulação)
O contraditório pontua cada réplica do autor em escala 1–5 **antes** de responder. Concessão só é permitida com pontuação ≥4 (a réplica endereça diretamente o ataque com evidência). Pontuação ≤3 → mantém a posição e reafirma o ataque original. Regras anti-bajulação: sem concessões consecutivas; rastreamento de taxa de concessão; detector de trava de enquadramento após cada *checkpoint*.

### 6.4 Protocolo anti-vazamento (isolamento de conhecimento)
Materiais da sessão têm prioridade absoluta sobre a memória paramétrica do modelo. Conteúdo ausente vira `[LACUNA DE MATERIAL]`, nunca preenchimento inventado.

### 6.5 Checklist de 7 Modos de Falha (gate 2.5 / 4.5)
Taxonomia derivada de Lu et al. (2026), reformulada: **M1** bug que passa pela auto-revisão · **M2** citação alucinada · **M3** resultado experimental fabricado · **M4** dependência de atalho · **M5** bug reenquadrado como insight · **M6** metodologia fabricada · **M7** trava de enquadramento. Qualquer modo SUSPEITO → falha o gate.

### 6.6 Cross-model gratuito
Quando `SCR_CROSS_MODEL=1`, um modelo local (via **Ollama**, ex. Llama/Qwen) re-executa a auditoria de integridade e o contraditório. Divergência >2 pontos é **reportada, não suavizada**.

---

## 7. Stack open-source

### 7.1 Herdadas do conceito original (todas livres)
- **Índices bibliográficos:** Semantic Scholar API, OpenAlex, Crossref, arXiv API (sem chave necessária para o básico).
- **Tipografia/conversão:** Pandoc (DOCX), Tectonic (LaTeX→PDF), CSL/citeproc (estilos de citação).
- **Runtime:** Python, pydantic (validação de contrato), ruamel.yaml, SQLite (cache).

### 7.2 Acréscimos open-source que agregam valor
| Ferramenta | Ganho |
|---|---|
| **GROBID** | Extração estruturada de metadados e referências de PDFs. |
| **Unpaywall API** | Descoberta de PDF *open access* legal para a auditoria de fidelidade. |
| **Zotero translation-server** | Ingestão de corpus do usuário e *round-trip* de bibliografia. |
| **PyMuPDF / Marker / Nougat** | Extração de texto de PDFs (inclusive escaneados/equações). |
| **sentence-transformers + RapidFuzz** | Dedup semântica e casamento de título robustos (além de Levenshtein puro). |
| **Chroma / Qdrant / FAISS** | *Vector store* para o corpus de literatura (busca *corpus-primeiro*). |
| **LangGraph** | Orquestração StateGraph (seu padrão OMNISCIENT). |
| **Langfuse** | Observabilidade auto-hospedável (tracing, custo, métricas de honestidade). |
| **Ollama** | Segundo modelo local para cross-model sem custo de API. |
| **Ragas / DeepEval** | Harness de avaliação dos próprios agentes (FNR/FPR da auditoria). |
| **LanguageTool** | Checagem gramatical open-source. |
| **Typst** | Alternativa moderna ao LaTeX para PDF (mais rápida de compilar). |
| **Manim** | Figuras animadas/explicativas (alinhado ao seu padrão de produção). |
| **gitleaks** | Varredura de segredos no repositório do squad. |
| **OpenReview API** | Dados de *venues* para a declaração de uso de IA. |

---

## 8. Contratos de handoff (esquemas pydantic, estilo SACP)

```python
class PassaporteDossie(BaseModel):           # estado global versionado
    versao_schema: str
    questao_pesquisa: BriefingDeQuestao
    corpus_literatura: list[EntradaCorpus] = []   # input-port opcional
    log_rejeicao: list[EntradaRejeicao] = []
    status_verificacao: Literal["PENDENTE","VERIFICADO"] = "PENDENTE"
    declaracao_experimentos: Literal["sem_experimentos","experimentos_declarados"]
    historico_integridade: list[RelatorioIntegridade] = []
    trajetoria_pontuacao: list[PontoTrajetoria] = []
    ledger_fronteira_reset: list[EntradaReset] = []   # retomar em sessão nova
    repro_lock: ReproLock | None = None               # documentação, não garantia

class MatrizDeRastreabilidade(BaseModel):     # estágio 3'
    alegacao_autor: str
    referencia: str
    verificado: bool
    metodo_recuperacao: Literal["quote","page","section","none"]

class ContratoDeParecer(BaseModel):           # estágio 3 (sprint contract)
    tamanho_painel: int
    dimensoes_aceite: list[str]
    condicoes_falha: list[CondicaoFalha]      # com severidade + quantificador
    procedimento_medicao: str
    # comprometido ANTES de ver o manuscrito (fase cega)
```

Todo handoff entre guildas valida o JSON em runtime; falha de parse → fallback gracioso (ex.: corpus ilegível → `[FALHA DE PARSE DO CORPUS]` e fluxo só-base-externa).

---

## 9. Modos de operação

| Guilda | Modos |
|---|---|
| Investigação | completo, rápido, maiêutico, revisão, revisão-de-literatura, scan-comparativo (POR-QUE/COMO/O-QUE), checagem-de-fatos, revisão-sistemática (PRISMA) |
| Escrita | completo, plano, só-esboço, revisão, coach-de-revisão, só-abstract, revisão-de-literatura, conversão-de-formato, checagem-de-citação, declaração-de-IA, auditoria-de-réplica |
| Parecer | completo, re-revisão, rápido, foco-método, guiado, calibração |
| Pipeline | orquestrador + `retomar_de_passaporte=<hash>` + `SCR_CLAIM_AUDIT=1` (auditoria de fidelidade) + camada de verificação temporal |

---

## 10. Critérios de aceite e métricas

- **Verificação de citação:** 100% das referências passam pela checagem 4-índices; nenhuma `inexistente` na saída final sem *override* humano registrado.
- **Auditoria de fidelidade (quando ligada):** FNR < 0,15 e FPR < 0,10 contra um *gold set* de 20 tuplas fornecido pelo humano.
- **Anti-bajulação:** taxa de concessão do contraditório reportada; nenhuma concessão com pontuação <4.
- **Integridade:** gates 2.5 e 4.5 não-puláveis; qualquer modo SUSPEITO em 2.5 deve estar RESOLVIDO em 4.5 (tolerância zero).
- **Reprodutibilidade de processo:** Dossiê permite retomar a execução em sessão nova a partir do *ledger*.
- **Custo-alvo:** ~US$4–6 por artigo de ~15k palavras no pipeline completo (referência do conceito original; calibrar com observabilidade Langfuse).

---

## 11. Roadmap de implementação

| Fase | Entregas |
|---|---|
| **F0 — Fundação** | Esquemas pydantic (Dossiê + contratos); StateGraph LangGraph esqueleto; cache SQLite; cliente 4-índices. |
| **F1 — Investigação** | G1 completa; fluxo corpus-primeiro; verificação de fontes; contraditório com limiar de concessão. |
| **F2 — Escrita + Integridade** | G2 completa; gate 2.5 (7 modos); anti-vazamento; calibração de estilo; figuras VLM. |
| **F3 — Parecer + Revisão** | G3 completa; *sprint contract* cego; matriz de rastreabilidade; caps de loop; gate 4.5. |
| **F4 — Finalização + Observabilidade** | Pandoc/Tectonic/Typst; declaração de IA por *venue*; Langfuse; Dossiê-Processo; auto-reflexão. |
| **F5 — Hardening** | Auditoria de fidelidade opt-in; cross-model via Ollama; harness Ragas/DeepEval; gitleaks; CI. |

---

## 12. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Alucinação de fidelidade (DOI existe mas não sustenta a frase) | Âncora de 3 camadas + LLM-como-juiz + *gate* terminal de recusa. |
| Bajulação sob pressão do usuário | Limiar de concessão + detector de trava de enquadramento + cross-model. |
| Vazamento de memória paramétrica | Protocolo anti-vazamento + etiqueta `[LACUNA DE MATERIAL]`. |
| Falsa sensação de reprodutibilidade | `repro_lock` é documentação pós-hoc, explicitamente **não** garantia de replay byte-a-byte. |
| Citações regionais/PT-BR não-indexadas | Status `não-resolvida` (não `inexistente`); precisão sobre recall, nunca bloqueia. |
| Over-reliance do pesquisador na IA | Observador de Colaboração + checkpoints humanos não-puláveis nos gates de integridade. |

---

## 13. Princípio orientador

> A IA é seu copiloto, não o piloto. O SCRIPTORIUM não escreve o artigo *por você* e não esconde que a IA foi usada — ele faz o trabalho braçal verificável para você focar no que exige cérebro humano: definir a pergunta, escolher o método, interpretar o que os dados significam e escrever a frase depois de “eu defendo que…”.

---

*Squad SCRIPTORIUM v1.0 — re-arquitetura independente sob OMNISCIENT v7.0. Documento de produto; não reutiliza nomenclatura, prompts ou esquemas de terceiros.*
