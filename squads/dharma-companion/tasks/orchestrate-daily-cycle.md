---
task: orchestrateDailyCycle()
responsavel: "PracticeWeaver"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - campo: timeAvailable
    tipo: number
    origen: "Praticante (input direto)"
    obrigatorio: false
  - campo: dailyFocus
    tipo: string
    origen: "Praticante (input direto) — zazen, ethics, observation, compassion"
    obrigatorio: false
  - campo: practitionerStage
    tipo: string
    origen: "assessStage() output via PathNavigator"
    obrigatorio: false
  - campo: lunarPhase
    tipo: string
    origen: "Calendário lunar — new_moon, full_moon, other"
    obrigatorio: false

Saida:
  - campo: dailyCycleLog
    tipo: object
    destino: "trackProgress() task via PathNavigator"
    persistido: true
  - campo: stepDelegations
    tipo: array
    destino: "guideMeditation(), applyPrecepts(), observeEmotions(), performRepentance(), activateCompassion()"
    persistido: false
  - campo: weeklyRhythm
    tipo: object
    destino: "Praticante (sugestão de ritmo semanal)"
    persistido: true

Checklist:
  pre-conditions:
    - "[ ] Praticante indicou tempo disponível ou aceita padrão (15min)"
    - "[ ] Estágio do praticante conhecido ou assumido como 'beginner'"
  post-conditions:
    - "[ ] Pelo menos o Passo 1 (Assentar-se) foi delegado ao ZazenGuide"
    - "[ ] Passos adaptados ao tempo disponível"
    - "[ ] Log do ciclo diário registrado"
    - "[ ] Se lua nova/cheia, Passo 5 (Arrependimento) incluído com ênfase"
  acceptance-criteria:
    - blocker: true
      criteria: "Ciclo inclui no mínimo 1 passo (zazen)"
    - blocker: true
      criteria: "Delegações referenciam agentes reais do squad"
    - blocker: false
      criteria: "Todos os 6 passos incluídos quando tempo >= 45min"

Performance:
  duration_expected: "5-60 minutos (conforme tempo disponível)"
  cost_estimated: "~300 tokens (orquestração) + custos das tasks delegadas"
  cacheable: false
  parallelizable: false
  skippable_when: "Praticante executa ciclo autônomo sem assistência"
---

# Pipeline Diagram

```
[timeAvailable] ──────────────┐
[dailyFocus] ─────────────────┤
[practitionerStage] ──────────┤
[lunarPhase] ─────────────────┤
                              ▼
                  ┌───────────────────────────┐
                  │  orchestrateDailyCycle()   │
                  │  (PracticeWeaver)          │
                  └──────────┬────────────────┘
                             │
        ┌──────────┬─────────┼─────────┬──────────┬──────────┐
        ▼          ▼         ▼         ▼          ▼          ▼
  [guideMedit.] [assessSt.] [applyPr.] [observeEm.] [performRep.] [activateC.]
   Passo 1      Passo 2    Passo 3    Passo 4     Passo 5      Passo 6
  (ZazenGuide) (PathNav.) (Precept.) (Mirror.)  (Interno)   (Compassion.)
```
