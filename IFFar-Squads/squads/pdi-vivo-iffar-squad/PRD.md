# PRD — PDI Vivo IFFar Squad

**Versão:** 1.0.0 · **Data:** 2026-06-17 · **Autor:** Marcio Bisognin · **Status:** aprovado para construção

---

## 1. Visão e contexto

O Plano de Desenvolvimento Institucional (PDI) do Instituto Federal Farroupilha é um documento de oito anos, construído de forma participativa, que descreve missão, organização, diretrizes pedagógicas, planejamento estratégico e processos de monitoramento. O ciclo 2019–2026 é robusto como documento, mas a análise comparativa com a proposta de PDI Vivo 2027–2034 mostra que **o desafio do novo ciclo não é redigir outro plano — é operacionalizá-lo como sistema vivo de gestão**.

Evidência da análise textual (incidência de termos de gestão contemporânea):

| Termo | PDI 2019–2026 | PDI Vivo 2027–2034 |
|---|---:|---:|
| indicadores | 10 | 33 |
| riscos | 3 | 20 |
| evidências | 0 | 15 |
| dashboard | 0 | 13 |
| painel | 0 | 17 |
| dados | 9 | 63 |
| territorial | 3 | 31 |

> Contagem textual não substitui leitura qualitativa, mas reforça a tese: o squad deve atuar na **camada operacional** — extrair metas, estruturar indicadores, vincular evidências, criar painéis e apoiar decisões corretivas.

## 2. Problema

O PDI tende a funcionar como documento formal de planejamento, com baixa rastreabilidade entre planejamento, orçamento, execução e resultado. Faltam:
- metas convertidas em registros estruturados e verificáveis;
- indicadores com fonte, periodicidade, responsável e evidência;
- riscos associados a cada meta ou programa;
- status por campus e por dimensão;
- relatórios trimestrais e revisão anual operacionais;
- comunicação clara para gestores, comunidade e sociedade.

## 3. Objetivos e métricas de sucesso

| Objetivo | Métrica de sucesso |
|---|---|
| Estruturar o PDI como dado | 100% das metas em matriz validável (CSV/JSON conforme schema) |
| Garantir rastreabilidade | 100% das metas com `fonte_dados` e `evidencia_obrigatoria` |
| Monitorar risco | Matriz de riscos recalculada a cada ciclo, com ação corretiva para todo risco alto/crítico |
| Acompanhar por campus | Pacto territorial gerado para cada campus com metas |
| Apoiar decisão | Relatório executivo trimestral + painel HTML por ciclo |
| Conformidade e privacidade | 0 publicações com dado pessoal sem base legal; parecer de governança em todo ciclo |

### Não objetivos (out of scope)
- Substituir deliberação colegiada, parecer jurídico ou decisão administrativa.
- Coletar automaticamente dados de sistemas sem conector autorizado.
- Publicar conteúdo sem revisão humana institucional.

## 4. Público-alvo
Pró-Reitoria de Desenvolvimento Institucional, DPDI, Reitoria, direções gerais de campus, gestores de ensino/pesquisa/extensão/administração/pessoas/TI/assistência estudantil, comitês locais do PDI, CPA e instâncias de avaliação, e a comunidade acadêmica em consultas e acompanhamento.

## 5. Arquitetura de agentes (17 SME)

| # | Agente | Especialidade |
|---|---|---|
| 1 | pdi-orchestrator | Orquestração e quality gates |
| 2 | documental-architect | Ingestão e base de conhecimento documental |
| 3 | goal-indicator-extractor | Extração de metas/indicadores |
| 4 | campus-territory-analyst | Campus e territorialidade |
| 5 | evidence-data-curator | Evidências, dicionário de dados e qualidade |
| 6 | data-bi-integration-engineer | Integração de fontes e camada semântica/BI |
| 7 | risk-budget-dependency-analyst | Riscos e dependências |
| 8 | budget-loa-ppa-analyst | Orçamento PPA/LOA/PLOA e execução |
| 9 | retention-success-monitor | Permanência, êxito e assistência estudantil |
| 10 | innovation-extension-radar | Inovação, extensão e impacto territorial |
| 11 | people-staffing-analyst | Gestão de pessoas e dimensionamento |
| 12 | infrastructure-works-analyst | Infraestrutura, obras e patrimônio |
| 13 | institutional-assessment-cpa-sinaes-specialist | Avaliação institucional CPA/SINAES |
| 14 | methodology-mec-compliance-reviewer | Metodologia e conformidade MEC/INEP |
| 15 | dashboard-report-designer | Painéis e relatórios executivos |
| 16 | institutional-diplomacy-consultation | Comunicação e consulta pública |
| 17 | governance-ethics-lgpd-guardian | Governança, ética e LGPD (gatekeeper) |

> Frente à proposta original (11 agentes), foram adicionados 6 SME — BI/integração, orçamento LOA/PPA, gestão de pessoas, infraestrutura/obras, avaliação CPA/SINAES e conformidade MEC — cobrindo as dimensões do PDI que ficavam sem dono técnico.

## 6. Workflows

- **A — Ingestão e comparação documental:** extrai e classifica fontes, compara ciclos, relatório de lacunas.
- **B — Matriz operacional de metas:** estrutura metas, indicadores, fontes e validação.
- **C — Pacto por campus:** filtra metas por campus, mapeia restrições e gera pacto territorial.
- **D — Ciclo trimestral:** recalcula status/risco, gera relatório executivo, painel e ata de decisão.
- **E — Revisão anual e conferência bienal:** consolida indicadores, compara meta×execução, prepara consulta pública.

## 7. Modelo de dados
Matriz central com 22 campos (ver `docs/modelo_de_dados.md` e `schemas/goal.schema.json`). Vocabulário controlado para status (9 valores), risco (4 níveis) e periodicidade (6 valores). Schemas adicionais para indicador, risco e evidência.

## 8. Scripts determinísticos (10)
`pdi_common` (núcleo) · `extract_pdi_text` · `build_goal_matrix` · `validate_indicator_matrix` · `compare_pdi_cycles` · `build_campus_pact` · `risk_matrix` · `generate_quarterly_report` · `render_dashboard` · `smoke_test`.

Regra de ouro: **scripts nunca inventam** indicador, fonte, responsável, prazo ou número — apenas estruturam, validam e sinalizam lacunas.

## 9. Entregáveis

| Entregável | Formato |
|---|---|
| Base de conhecimento do PDI | Texto extraído + métricas + hash |
| Matriz operacional de metas | CSV/JSON |
| Dicionário de indicadores | CSV/Markdown |
| Matriz de riscos | CSV/Markdown |
| Relatório executivo trimestral | Markdown (→ PDF/DOCX) |
| Painel | HTML local |
| Pactos por campus | CSV/Markdown |
| Pacote de consulta pública | Markdown/PDF |
| Quality report | JSON |

## 10. Requisitos não funcionais (NFR)
- **Determinismo:** mesma entrada → mesma saída; sem dependência de rede no núcleo.
- **Portabilidade:** Python 3.11+ com biblioteca padrão; dependências externas opcionais.
- **Auditabilidade:** hash SHA-256 de fontes/evidências; trilha de decisões.
- **Testabilidade:** suíte `pytest` + `smoke_test.py` cobrindo o pipeline.
- **Acessibilidade:** relatórios e consulta pública em linguagem clara.
- **Idempotência:** geração de artefatos repetível.

## 11. Governança de dados e LGPD
Classificação por sensibilidade; minimização e mascaramento de dado pessoal; retenção configurável; proibição de envio de dados institucionais a modelos externos sem autorização; parecer do `governance-ethics-lgpd-guardian` (com poder de bloqueio) antes de qualquer publicação.

## 12. Plano de testes e critérios de aceite
O squad é considerado pronto quando:
- [x] lê PDF/DOCX/Markdown e registra extração com hash;
- [x] gera matriz de metas em CSV/JSON;
- [x] identifica metas sem indicador, responsável, prazo ou evidência;
- [x] gera relatório executivo com status e riscos;
- [x] produz painel HTML local simples;
- [x] inclui exemplos de entrada e saída;
- [x] possui testes automatizados (pytest) para utilidades e validação;
- [x] possui smoke test do pipeline com evidência real de execução;
- [x] passa no `validate_squad.py` do construtor (go).

## 13. Riscos e mitigação

| Risco | Impacto | Mitigação |
|---|---|---|
| Virar mero gerador de texto | Alto | Scripts determinísticos + matriz validável |
| Dados sensíveis sem governança | Alto | Guardião LGPD, anonimização e revisão prévia |
| Metas sem fonte de evidência | Alto | Campo obrigatório + validador |
| Baixa adesão dos campi | Médio/alto | Pacto por campus + devolutivas visuais |
| Excesso de indicadores | Médio | Câmara de Indicadores + criticidade |
| Relatório formalista sem decisão | Alto | Ata de decisão corretiva + ciclo trimestral |

## 14. Roadmap
Ver `docs/roadmap.md` (7 fases, da estrutura inicial à publicação institucional).

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
