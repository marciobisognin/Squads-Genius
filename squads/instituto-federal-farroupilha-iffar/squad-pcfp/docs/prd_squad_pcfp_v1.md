# PRD — Squad PCFP v1.0 (documento de origem)

> Transcrição estruturada do PRD anexado pelo autor (Marcio, junho/2026, status: draft para revisão), fonte primária da arquitetura deste squad. Conteúdo normativo detalhado em `base_normativa.md`.

## 1. Visão geral
- **Problema:** a elaboração da Planilha de Custos e Formação de Preços (PCFP) para contratos com dedicação exclusiva de mão de obra exige domínio simultâneo de licitações (Lei 14.133/2021), normativos infralegais em mudança constante (IN 05/2017, 98/2022, 176/2024, 147/2026), direito trabalhista e CCTs por categoria/território, tributação em transição (CBS/IBS, reoneração) e jurisprudência do TCU. Erros geram dano ao erário recorrente (contratos de até 10 anos), apontamentos de CGU/TCU e repactuações mal instruídas.
- **Solução:** squad de agentes de IA cobrindo o ciclo completo: intake → pesquisa normativa → cálculo → conformidade → exequibilidade → artefatos → gestão contratual (repactuação/reajuste), com HITL obrigatório nos pontos de decisão jurídica.
- **Usuários-alvo:** equipes de planejamento (ETP/TR) em IFEs e órgãos federais; agentes de contratação e pregoeiros; fiscais e gestores de contrato; auditoria interna e controle.

### Métricas de sucesso (North Star)
| Métrica | Baseline | Meta v1 |
|---|---|---|
| Tempo de elaboração de PCFP completa | 2–5 dias | < 2 horas |
| Erros de conformidade detectados em auditoria interna | — | redução de 80% |
| Cobertura de checklist normativo automatizado | 0% | ≥ 95% dos itens auditáveis |
| Rastreabilidade (célula → fundamento legal) | manual | 100% das rubricas com citação |

## 2. Base normativa
Ver `base_normativa.md` (camadas legal, infralegal, controle e fontes dinâmicas).

## 3. Arquitetura
### Princípios de design
1. **Cálculo determinístico, raciocínio por LLM** — nenhum valor monetário é gerado por LLM; a engine é Python puro e testável.
2. **Rastreabilidade total** — cada rubrica carrega `{valor, formula, fundamento_legal, fonte, timestamp}`.
3. **HITL nos pontos jurídicos** — enquadramento sindical, regime tributário e percentuais discricionários exigem aprovação humana.
4. **Schema-first** — handoffs via JSON validado (Pydantic), padrão SACP (OMNISCIENT).

### Os 8 agentes
A1 Orquestrador (classificação da demanda, grafo, estado) · A2 Intake & Classificação (ServiceProfile; parser de propostas) · A3 Normativo/RAG jurídico (checklist, índice temporal de vigência) · A4 CCT & Sindical (CCTProfile; HITL Gate 1) · A5 Engine de Cálculo (módulos 1–6 do Anexo VII-D; `pcfp-core`) · A6 Auditor de Conformidade (checklist + exequibilidade verde/amarelo/vermelho) · A7 Gestão Contratual (repactuação × reajuste × reequilíbrio; preclusão; HITL Gate 2) · A8 Gerador de Artefatos (planilha, relatório, checklist assinável, dashboard).

### Fluxos
- **Principal (elaboração nova):** A2 → A3 → A4 [HITL 1] → A5 → A6 (se vermelho: loop A5, máx. 3) → A8 [HITL 2].
- **Secundário (análise de proposta):** A2 parser → A5 recálculo paralelo → A6 diff célula a célula + exequibilidade → A8 relatório ao pregoeiro.

## 4. Stack técnico (produção)
LangGraph (StateGraph + checkpoints, HITL nativo) · Claude (API Anthropic, tiers por agente: jurídico A3/A6 em modelo top; extração A2 em modelo rápido) · engine Python puro + Pydantic + pytest · RAG com pgvector + reranker (corpus pequeno versionado) · corpus normativo em Git (markdown com frontmatter de vigência, diff por PR) · parsing com openpyxl/pdfplumber/docling · XLSX via openpyxl com fórmulas vivas · observabilidade LangSmith/Langfuse · frontend Next.js com tabela editável (revisão HITL célula a célula) · Postgres (TimescaleDB opcional para séries de índices).

## 5. Schemas principais
Ver `templates/schemas.md` (ServiceProfile, CCTProfile, Rubrica, ComplianceFinding, Aprovação HITL).

## 6. Roadmap
| Fase | Escopo | Duração |
|---|---|---|
| F0 Fundação | Corpus normativo versionado + pcfp-core (módulos 1–3) com golden tests dos Cadernos Técnicos | 3 semanas |
| F1 MVP | Fluxo completo p/ limpeza 44h: A1, A2, A5, A8 + XLSX | 4 semanas |
| F2 Conformidade | A3 (RAG) + A6 (auditor) + checklist TCU/CGU + HITL gates | 4 semanas |
| F3 CCT & multi-serviço | A4 + vigilância 12x36 + insalubridade/periculosidade + Simples Nacional | 4 semanas |
| F4 Ciclo de vida | A7 (repactuação/reajuste) + parser de propostas + diff de exequibilidade | 4 semanas |
| F5 Reforma Tributária | Motor CBS/IBS com cronograma de transição parametrizado | 3 semanas |

## 7. Riscos e mitigações
| Risco | Impacto | Mitigação |
|---|---|---|
| LLM "alucinar" norma ou percentual | Crítico | Engine determinística; LLM nunca produz números; citação validada contra corpus |
| Norma alterada sem atualização do corpus | Alto | Job semanal DOU/Portal de Compras + alerta de divergência; frontmatter de vigência |
| Enquadramento sindical incorreto | Alto | HITL Gate 1 obrigatório; A4 apresenta alternativas com prós/contras, nunca decide sozinho |
| Transição CBS/IBS instável | Médio | Motor tributário plugável, alíquotas em configuração versionada |
| Excesso de confiança do usuário (automação ≠ parecer jurídico) | Médio | Disclaimers nos relatórios; campo "responsável pela validação" obrigatório |
| Parsing de propostas caóticas | Médio | Fallback: revisão manual assistida com mapeamento de colunas |

## 8. Fora de escopo (v1)
Obras/engenharia (SINAPI/SICRO); contratações estaduais/municipais; integração transacional SIPAC/Compras.gov (v2: export; v3: API); assinatura digital e tramitação.

## 9. Questões em aberto
1. Custos unitários mínimos da IN 176/2024: estrutura paralela ao Anexo VII-D ou camada de validação? (recomendação inicial: camada de validação no A6 — **adotada nesta implementação**).
2. Hospedagem da knowledge base com CCTs: infraestrutura institucional ou ambiente próprio?
3. Incluir agente de pesquisa de preços (IN 65/2021) como A9 na v2? (sinergia: ver `hefesto-forja-licitatoria-squad/agents/pesquisa-precos-planilhista.md` neste repositório).

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
