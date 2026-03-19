---
task: auditarFragilidade()
responsavel: "Medusa Auditora"
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
  - nome: exposureMap
    tipo: file
    obrigatorio: true
    descricao: "Exposições de Sêneca"

Saida:
  - nome: validationReport
    tipo: file
    obrigatorio: true
    descricao: "Relatório de auditoria (destino: sintetizarRelatorio())"
  - nome: fragilityScorecard
    tipo: file
    obrigatorio: true
    descricao: "Scorecard (destino: sintetizarRelatorio())"
  - nome: acceptanceStatus
    tipo: boolean
    obrigatorio: true
    descricao: "Status de aceitação final"

Checklist:
  pre-conditions:
    - "[ ] Todos os 4 artefatos de entrada recebidos e válidos"
    - "[ ] Nenhum artefato com erros estruturais"
  post-conditions:
    - "[ ] 6 critérios avaliados (Tríade, Barbell, Skin in the Game, Via Negativa, Lindy, Ruína)"
    - "[ ] Scorecard gerado com pontuação por componente"
    - "[ ] Fragilistas identificados (se houver)"
    - "[ ] Status final declarado: PASSED (true) ou FAILED (false)"

Performance:
  duration_expected: "5-8 min"
  cacheable: false
  parallelizable: false
  skippable_when: "Nunca — qualidade final inegociável"

Error Handling:
  strategy: abort
  retry:
    max_attempts: 1
    delay: "0s"
  fallback: "FAIL automático + alerta urgente"
  notification: "orchestrator"

Metadata:
  version: 1.0.0
  author: marciobisognin
  story: Genius Athena-Strange — Taleb Pipeline
---

# auditarFragilidade()

## Pipeline Diagram

```
[cisnesNegrosMapa, antifragileBlueprint, barbellStrategy] ──→ [auditarFragilidade()] ──→ [validation-report.md] ──→ [sintetizarRelatorio()]
```

## Descrição

Audita todos os artefatos contra 6 critérios de fragilidade, verificando skin in the game, Efeito Lindy e risco de ruína. É a última linha de defesa antes da síntese final, petrificando qualquer fragilidade que tenha escapado das fases anteriores.
