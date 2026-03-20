---
task: applyPrecepts()
responsavel: "PreceptKeeper"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - campo: practitionerStage
    tipo: string
    origen: "assessStage() output via PathNavigator"
    obrigatorio: false
  - campo: selectedPrecept
    tipo: number
    origen: "Praticante (input direto) ou orchestrateDailyCycle() args"
    obrigatorio: false
  - campo: dailySituation
    tipo: string
    origen: "Praticante (input direto)"
    obrigatorio: false
  - campo: emotionalTriggers
    tipo: array
    origen: "observeEmotions() output via MirrorObserver"
    obrigatorio: false

Saida:
  - campo: dailyPrecepts
    tipo: object
    destino: "orchestrateDailyCycle() registro, Praticante"
    persistido: true
  - campo: ethicalReflection
    tipo: string
    destino: "activateCompassion() task via CompassionCatalyst"
    persistido: true
  - campo: preceptLog
    tipo: object
    destino: "trackProgress() task via PathNavigator"
    persistido: true

Checklist:
  pre-conditions:
    - "[ ] Os 10 Preceitos Mahayana disponíveis como referência"
    - "[ ] Contexto do praticante conhecido (estágio, situação)"
  post-conditions:
    - "[ ] 1-2 preceitos selecionados para o dia"
    - "[ ] Reflexão contextualizada fornecida"
    - "[ ] Pergunta de observação definida para o dia"
    - "[ ] Log de preceitos atualizado"
  acceptance-criteria:
    - blocker: true
      criteria: "Preceito selecionado existe nos 10 Preceitos Mahayana"
    - blocker: true
      criteria: "Reflexão inclui pelo menos 1 das 3 camadas (literal, relacional, universal)"

Performance:
  duration_expected: "2-5 minutos"
  cost_estimated: "~300 tokens"
  cacheable: false
  parallelizable: true
  skippable_when: "Praticante já selecionou preceito manualmente"
---

# Pipeline Diagram

```
[practitionerStage] ──────────┐
[selectedPrecept] ────────────┤
[dailySituation] ─────────────┤
[emotionalTriggers] ──────────┤
                              ▼
                    ┌─────────────────────┐
                    │  applyPrecepts()    │
                    │  (PreceptKeeper)    │
                    └──────┬──────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
     [dailyPrecepts]  [ethicalReflection] [preceptLog]
    (DailyCycle/User)  (activateCompassion) (trackProgress)
```
