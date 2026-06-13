# ⚡ AllSpark Talent Intelligence Squad

## Visão Geral

O AllSpark Talent Intelligence Squad é um sistema multiagente de inteligência de pessoas projetado para transformar dados brutos de RH em insights estratégicos acionáveis. Ele mapeia competências, detecta riscos de retenção, projeta sucessão, audita DEI, personaliza jornadas de onboarding e realiza benchmarking salarial — tudo em um pipeline orquestrado com quality gates e humano no loop nos momentos críticos.

O squad opera em modo de grafo multiagente dinâmico: cada agente é especialista em seu domínio e entrega outputs estruturados para os nós adjacentes, permitindo tanto a execução do pipeline completo quanto análises pontuais por módulo.

## Artefato de Inspiração

**AllSpark (Transformers)** — a fonte primordial de energia e inteligência que dá vida aos Autobots. Neste squad, o AllSpark representa a inteligência de pessoas: a força oculta que, quando bem mapeada e ativada, dá vida à organização. Dados de RH são apenas metais brutos; este squad é o AllSpark que os transforma em potencial humano acionável.

## Domínio

Inteligência de talentos, aquisição e mapeamento de competências, planejamento de sucessão, DEI (Diversidade, Equidade e Inclusão), benchmarking salarial, saúde organizacional, onboarding e retenção de talentos.

---

## Agentes

O squad é composto por 9 agentes especializados que atuam em pipeline ou de forma modular:

| Agente | Papel |
|---|---|
| **talent-orchestrator** | Coordenador central: roteia inputs, gerencia o pipeline, aciona quality gates e consolida os outputs finais em um People Intelligence Report coeso. |
| **talent-mapper** | Mapeia o inventário de competências organizacionais, identifica gaps críticos por área e nível, e produz a lista de colaboradores de alto potencial (HiPo). |
| **psychometric-profiler** | Sintetiza avaliações comportamentais (DISC, Big Five, CliftonStrengths) em perfis acionáveis por colaborador e mapas de dinâmica de time. |
| **market-salary-intel** | Benchmarking salarial (FGV, Catho, Glassdoor, LinkedIn Salary), análise de competitividade de remuneração total, inteligência de employer branding e alertas de risco por gap salarial. |
| **culture-fit-analyst** | Avalia alinhamento de valores individuais com a cultura organizacional, diagnostica clima por área e mapeia subculturas e focos de conflito. |
| **succession-architect** | Identifica posições críticas, avalia prontidão de sucessores, constrói trilhas de carreira mensuráveis e cria planos de aceleração individualizados. |
| **dei-metrics-auditor** | Audita métricas de Diversidade, Equidade e Inclusão com KPIs verificáveis, análise de equidade salarial e conformidade LGPD. |
| **onboarding-designer** | Desenha jornadas de onboarding personalizadas 30-60-90 dias por perfil comportamental, cargo e área, com métricas de sucesso instrumentadas. |
| **retention-risk-sentinel** | Calcula Risk Scores de turnover por colaborador, emite alertas precoces com intervenções recomendadas e monitora tendências de rotatividade. |

---

## Pipeline

O pipeline completo executa 10 fases sequenciais com quality gates entre etapas críticas:

```
1. Intake e Validação de Dados            → talent-orchestrator
2. Mapeamento de Competências             → talent-mapper
3. Perfilamento Comportamental            → psychometric-profiler       [GATE HITL]
4. Inteligência de Mercado Salarial       → market-salary-intel
5. Análise de Fit Cultural e Clima        → culture-fit-analyst
6. Planejamento de Sucessão               → succession-architect         [GATE HITL]
7. Auditoria de Métricas DEI              → dei-metrics-auditor          [GATE LGPD]
8. Design de Jornada de Onboarding        → onboarding-designer
9. Monitoramento e Sentinela de Retenção  → retention-risk-sentinel
10. Consolidação e Entrega Final          → talent-orchestrator          [GATE HITL]
```

Gates HITL obrigatórios: perfis comportamentais (revisão por especialista), mapa de sucessão (aprovação CHRO + liderança), auditoria DEI (revisão DPO/jurídico) e entrega final (aprovação RH sênior).

---

## Como Usar

### Execução do pipeline completo

Para rodar o ciclo de People Intelligence completo, forneça ao talent-orchestrator:
1. Base de dados de colaboradores (cargo, área, nível, data de admissão, faixa salarial)
2. Resultados de avaliações de desempenho dos últimos 12 meses
3. Dados de pesquisa de clima organizacional (últimos 6-12 meses)
4. Histórico de turnover dos últimos 24 meses
5. Benchmarks salariais de mercado por cargo e região
6. Dados demográficos com consentimento LGPD documentado
7. Resultados de avaliações comportamentais (quando disponíveis)
8. Contexto estratégico da organização para os próximos 12-36 meses

### Execução modular

Cada agente pode ser acionado de forma independente para análises pontuais:
- Somente benchmarking salarial: ative `market-salary-intel` diretamente.
- Somente risco de retenção: ative `retention-risk-sentinel` com os dados de colaboradores.
- Somente sucessão: use a task `succession-planning.md` ativando o `succession-architect`.
- Análise completa de talentos: use a task `talent-analysis.md` com o pipeline completo.

### Comando rápido
```
*run pipeline completo — [fornecer dados de entrada conforme lista acima]
*run succession-planning — [fornecer organograma + dados de colaboradores]
*run salary-benchmark — [fornecer cargos + região de referência]
```

---

## Outputs Esperados

Ao final do pipeline completo, o squad entrega:

- **People Intelligence Report** (versão executiva e técnica): sumário com 5-10 recomendações priorizadas por impacto e urgência.
- **Matriz de Competências Organizacional**: mapa de skills com gaps críticos e lista HiPo.
- **Perfis Comportamentais Consolidados** por time (após revisão humana obrigatória).
- **Relatório de Benchmark Salarial**: posicionamento competitivo e lista de risco por remuneração.
- **Diagnóstico de Clima e Fit Cultural**: NPS interno por área e mapa de subculturas.
- **Mapa de Sucessão Visual**: Succession Readiness Scores e planos de aceleração por sucessor.
- **Dashboard de Métricas DEI**: KPIs auditáveis com plano de ação e conformidade LGPD.
- **Jornadas de Onboarding Personalizadas**: trilhas 30-60-90 dias por cargo e perfil.
- **Dashboard de Risk Scores de Retenção**: alertas ativos com intervenções recomendadas.
- **Log de Quality Gates**: apêndice de auditoria com todas as decisões e aprovações registradas.

---

## Aviso Legal

Este squad utiliza dados de pessoas e, portanto, exige conformidade estrita com a Lei Geral de Proteção de Dados (LGPD — Lei nº 13.709/2018). Dados demográficos devem ser coletados com consentimento documentado. Perfis psicométricos devem ser revisados por profissional habilitado antes de qualquer circulação. Nenhum dado pessoal identificável deve constar em relatórios de distribuição ampla. O uso deste squad não substitui a avaliação clínica, o diagnóstico psicológico formal nem a consultoria jurídica trabalhista. Resultados devem ser contextualizados por profissionais de RH antes de embasar decisões de promoção, demissão ou remuneração.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
