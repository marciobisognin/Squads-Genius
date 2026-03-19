---
task: sintetizarRelatorio()
responsavel: "Hermes Orquestrador"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: cisnesNegrosMapa
    tipo: file
    obrigatorio: true
    descricao: "Mapa de Cygnus"
  - nome: antifragileBlueprint
    tipo: file
    obrigatorio: true
    descricao: "Blueprint de Hydra"
  - nome: barbellStrategy
    tipo: file
    obrigatorio: true
    descricao: "Estratégia de Sêneca"
  - nome: validationReport
    tipo: file
    obrigatorio: true
    descricao: "Relatório de Medusa"
  - nome: fragilityScorecard
    tipo: file
    obrigatorio: true
    descricao: "Scorecard de Medusa"

Saida:
  - nome: relatorioExecutivoAntifragil
    tipo: file
    obrigatorio: true
    descricao: "Arquivo Final: relatorio-executivo-antifragil.md"

Checklist:
  pre-conditions:
    - "[ ] Todos os 5 artefatos de entrada recebidos e válidos"
    - "[ ] validationReport contém status final (PASSED/FAILED)"
  post-conditions:
    - "[ ] TL;DR de 3 bullets no topo"
    - "[ ] Status global declarado (ANTIFRÁGIL / ROBUSTO / FRÁGIL)"
    - "[ ] Seções de cada agente presentes e sintetizadas"
    - "[ ] Plano de ação com 3 horizontes (24h, 1 semana, 1 mês)"

Performance:
  duration_expected: "5-10 min"
  cacheable: false
  parallelizable: false
  skippable_when: "Nunca — síntese final obrigatória"

Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: "5s"
  fallback: "Solicitar preenchimento manual de lacunas nos artefatos"
  notification: "orchestrator"

Metadata:
  version: 1.0.0
  author: marciobisognin
  story: Genius Athena-Strange — Taleb Pipeline
---

# sintetizarRelatorio()

## Pipeline Diagram

```
[Todos os artefatos] ──→ [sintetizarRelatorio()] ──→ [relatorio-executivo-antifragil.md] ──→ Usuário
```

## Descrição

Consolida todos os artefatos em um relatório executivo acionável que classifica o sistema como Frágil, Robusto ou Antifrágil. O orquestrador garante que a visão de cada especialista seja refletida com clareza técnica e pragmatismo estratégico.
