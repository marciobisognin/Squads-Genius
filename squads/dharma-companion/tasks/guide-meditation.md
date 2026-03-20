---
task: guideMeditation()
responsavel: "ZazenGuide"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - campo: practitionerLevel
    tipo: string
    origen: "assessStage() output via PathNavigator"
    obrigatorio: false
  - campo: sessionDuration
    tipo: number
    origen: "Praticante (input direto) ou orchestrateDailyCycle() args"
    obrigatorio: false
  - campo: previousSessionNotes
    tipo: object
    origen: "trackProgress() output via PathNavigator"
    obrigatorio: false

Saida:
  - campo: sessionGuidance
    tipo: object
    destino: "Praticante (instrução direta)"
    persistido: false
  - campo: sessionLog
    tipo: object
    destino: "trackProgress() task, orchestrateDailyCycle() registro"
    persistido: true
  - campo: emotionalObservations
    tipo: array
    destino: "observeEmotions() task via MirrorObserver"
    persistido: false

Checklist:
  pre-conditions:
    - "[ ] Praticante disponível para sessão (tempo mínimo de 5 minutos)"
    - "[ ] Ambiente adequado verificado (silêncio, espaço)"
  post-conditions:
    - "[ ] Instrução de postura fornecida"
    - "[ ] Técnica de respiração explicada"
    - "[ ] Duração da sessão definida"
    - "[ ] Sessão registrada no log"
  acceptance-criteria:
    - blocker: true
      criteria: "Instrução inclui postura, respiração e tempo"
    - blocker: false
      criteria: "Nível do praticante considerado na adaptação"

Performance:
  duration_expected: "5-45 minutos (conforme nível)"
  cost_estimated: "~200 tokens"
  cacheable: false
  parallelizable: false
  skippable_when: "Praticante já possui rotina autônoma de zazen"
---

# Pipeline Diagram

```
[practitionerLevel] ──────────┐
[sessionDuration] ────────────┤
[previousSessionNotes] ───────┤
                              ▼
                    ┌─────────────────────┐
                    │  guideMeditation()  │
                    │  (ZazenGuide)       │
                    └──────┬──────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
     [sessionGuidance] [sessionLog] [emotionalObservations]
      (Praticante)    (trackProgress) (observeEmotions)
```
