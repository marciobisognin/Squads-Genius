---
task: performRepentance()
responsavel: "PracticeWeaver"
responsavel_type: Agente
atomic_layer: Atom

Entrada:
  - campo: lunarPhase
    tipo: string
    origen: "orchestrateDailyCycle() input — new_moon, full_moon, other"
    obrigatorio: false
  - campo: dailyObservations
    tipo: object
    origen: "observeEmotions() output — bodyMindReport"
    obrigatorio: false

Saida:
  - campo: repentanceRecord
    tipo: object
    destino: "trackProgress() task, orchestrateDailyCycle() registro"
    persistido: true
  - campo: renewalIntention
    tipo: string
    destino: "Praticante (intenção de recomeço)"
    persistido: false

Checklist:
  pre-conditions:
    - "[ ] Texto do ritual de arrependimento disponível"
    - "[ ] Praticante disponível para momento de reflexão"
  post-conditions:
    - "[ ] Recitação do arrependimento realizada ou guiada"
    - "[ ] Intenção de recomeço formulada"
    - "[ ] Registro persistido"
  acceptance-criteria:
    - blocker: true
      criteria: "Arrependimento tratado como limpeza/recomeço, NUNCA como culpa"
    - blocker: false
      criteria: "Se lua nova/cheia, versão completa utilizada"

Performance:
  duration_expected: "1-3 minutos"
  cost_estimated: "~100 tokens"
  cacheable: false
  parallelizable: false
  skippable_when: "Praticante optou por versão silenciosa interna"
---

# Pipeline Diagram

```
[lunarPhase] ─────────────────┐
[dailyObservations] ──────────┤
                              ▼
                    ┌──────────────────────────┐
                    │  performRepentance()     │
                    │  (PracticeWeaver)        │
                    └──────┬───────────────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
          [repentanceRecord] [renewalIntention]
           (trackProgress)    (Praticante)
```

# Texto do Ritual

> "Todo karma prejudicial cometido por mim, desde tempos imemoriais, por ganância, raiva e ignorância, nascido de corpo, fala e mente, agora, de tudo, eu me arrependo."
