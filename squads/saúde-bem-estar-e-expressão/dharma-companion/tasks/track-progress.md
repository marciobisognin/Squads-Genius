---
task: trackProgress()
responsavel: "PathNavigator"
responsavel_type: Agente
atomic_layer: Molecule

Entrada:
  - campo: sessionLogs
    tipo: array
    origen: "guideMeditation() output — sessionLog"
    obrigatorio: false
  - campo: preceptLogs
    tipo: array
    origen: "applyPrecepts() output — preceptLog"
    obrigatorio: false
  - campo: emotionReports
    tipo: array
    origen: "observeEmotions() output — bodyMindReport"
    obrigatorio: false
  - campo: cycleLogs
    tipo: array
    origen: "orchestrateDailyCycle() output — dailyCycleLog"
    obrigatorio: false
  - campo: repentanceRecords
    tipo: array
    origen: "performRepentance() output — repentanceRecord"
    obrigatorio: false
  - campo: compassionRecords
    tipo: array
    origen: "activateCompassion() output — compassionActions"
    obrigatorio: false

Saida:
  - campo: progressReport
    tipo: object
    destino: "Praticante (relatório de progressão)"
    persistido: true
  - campo: practiceHistory
    tipo: object
    destino: "assessStage() task — input para avaliação de estágio"
    persistido: true
  - campo: consistencyMetrics
    tipo: object
    destino: "Praticante, orchestrateDailyCycle() — métricas de constância"
    persistido: true

Checklist:
  pre-conditions:
    - "[ ] Pelo menos 1 tipo de log disponível para análise"
  post-conditions:
    - "[ ] Relatório de progressão gerado"
    - "[ ] Métricas de constância calculadas (dias consecutivos, total de sessões)"
    - "[ ] Histórico atualizado"
  acceptance-criteria:
    - blocker: true
      criteria: "Progressão tratada sem julgamento — não há 'nota' ou 'falha'"
    - blocker: false
      criteria: "Padrões de constância identificados"
    - blocker: false
      criteria: "Sugestões de ajuste incluídas se métricas indicam queda"

Performance:
  duration_expected: "1-3 minutos"
  cost_estimated: "~200 tokens"
  cacheable: true
  parallelizable: true
  skippable_when: "Nenhum log novo desde última análise"
---

# Pipeline Diagram

```
[sessionLogs] ────────────────┐
[preceptLogs] ────────────────┤
[emotionReports] ─────────────┤
[cycleLogs] ──────────────────┤
[repentanceRecords] ──────────┤
[compassionRecords] ──────────┤
                              ▼
                    ┌─────────────────────┐
                    │  trackProgress()    │
                    │  (PathNavigator)    │
                    └──────┬──────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
    [progressReport] [practiceHistory] [consistencyMetrics]
      (Praticante)    (assessStage)    (Praticante/DailyCycle)
```
