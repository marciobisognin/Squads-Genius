---
task: activateCompassion()
responsavel: "CompassionCatalyst"
responsavel_type: Agente
atomic_layer: Molecule

Entrada:
  - campo: practiceInsights
    tipo: object
    origen: "observeEmotions() output — buttonMap, reframedMemory"
    obrigatorio: false
  - campo: ethicalReflections
    tipo: string
    origen: "applyPrecepts() output — ethicalReflection"
    obrigatorio: false
  - campo: practitionerStage
    tipo: string
    origen: "assessStage() output — currentStage"
    obrigatorio: false
  - campo: practitionerContext
    tipo: string
    origen: "Praticante (input direto) — contexto familiar, profissional, comunitário"
    obrigatorio: false

Saida:
  - campo: compassionActions
    tipo: array
    destino: "Praticante (sugestões de ações concretas)"
    persistido: true
  - campo: dailyServiceSuggestion
    tipo: string
    destino: "orchestrateDailyCycle() registro"
    persistido: true
  - campo: gratitudePractice
    tipo: object
    destino: "Praticante (prática de gratidão)"
    persistido: false

Checklist:
  pre-conditions:
    - "[ ] Pelo menos 1 input disponível (insight, reflexão ou contexto)"
  post-conditions:
    - "[ ] Pelo menos 1 ação concreta sugerida"
    - "[ ] Ação adaptada ao estágio do praticante"
    - "[ ] Ação é realizável no contexto do praticante"
  acceptance-criteria:
    - blocker: true
      criteria: "Ação sugerida é concreta e realizável (não abstrata)"
    - blocker: false
      criteria: "Conexão entre insight e ação é explícita"

Performance:
  duration_expected: "2-5 minutos"
  cost_estimated: "~200 tokens"
  cacheable: false
  parallelizable: true
  skippable_when: "Praticante já definiu ação de serviço para o dia"
---

# Pipeline Diagram

```
[practiceInsights] ───────────┐
[ethicalReflections] ─────────┤
[practitionerStage] ──────────┤
[practitionerContext] ────────┤
                              ▼
                    ┌─────────────────────────┐
                    │  activateCompassion()   │
                    │  (CompassionCatalyst)   │
                    └──────┬──────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
  [compassionActions] [dailyServiceSug.] [gratitudePractice]
     (Praticante)       (DailyCycle)       (Praticante)
```
