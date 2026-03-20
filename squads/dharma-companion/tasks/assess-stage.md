---
task: assessStage()
responsavel: "PathNavigator"
responsavel_type: Agente
atomic_layer: Molecule

Entrada:
  - campo: practitionerContext
    tipo: string
    origen: "Praticante (input direto) — descrição da situação atual"
    obrigatorio: true
  - campo: practiceHistory
    tipo: object
    origen: "trackProgress() output — histórico acumulado"
    obrigatorio: false
  - campo: dailyCycleLogs
    tipo: array
    origen: "orchestrateDailyCycle() output — logs acumulados"
    obrigatorio: false

Saida:
  - campo: currentStage
    tipo: object
    destino: "orchestrateDailyCycle(), guideMeditation(), applyPrecepts(), activateCompassion()"
    persistido: true
  - campo: stageReflection
    tipo: string
    destino: "Praticante (reflexão sobre estágio atual)"
    persistido: true
  - campo: nextStepSuggestions
    tipo: array
    destino: "Praticante, orchestrateDailyCycle()"
    persistido: true

Checklist:
  pre-conditions:
    - "[ ] Contexto do praticante fornecido (mínimo: descrição de situação)"
    - "[ ] Os 5 estágios disponíveis como referência"
  post-conditions:
    - "[ ] Estágio atual identificado (1-5)"
    - "[ ] Justificativa do estágio fornecida"
    - "[ ] Sugestões de próximos passos definidas"
    - "[ ] Reflexão sobre impermanência adaptada ao estágio"
  acceptance-criteria:
    - blocker: true
      criteria: "Estágio identificado é um dos 5 definidos no framework"
    - blocker: false
      criteria: "Reflexão sobre impermanência incluída"

Performance:
  duration_expected: "2-5 minutos"
  cost_estimated: "~250 tokens"
  cacheable: true
  parallelizable: true
  skippable_when: "Estágio avaliado há menos de 30 dias sem mudanças significativas"
---

# Pipeline Diagram

```
[practitionerContext] ────────┐
[practiceHistory] ────────────┤
[dailyCycleLogs] ─────────────┤
                              ▼
                    ┌─────────────────────┐
                    │  assessStage()      │
                    │  (PathNavigator)    │
                    └──────┬──────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
     [currentStage]  [stageReflection] [nextStepSuggestions]
    (Todos agentes)   (Praticante)     (Praticante/DailyCycle)
```
