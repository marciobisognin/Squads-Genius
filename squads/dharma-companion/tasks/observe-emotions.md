---
task: observeEmotions()
responsavel: "MirrorObserver"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - campo: emotionalTrigger
    tipo: string
    origen: "Praticante (input direto) ou orchestrateDailyCycle() Passo 4"
    obrigatorio: false
  - campo: biographicalMemory
    tipo: string
    origen: "Praticante (input direto)"
    obrigatorio: false
  - campo: zazenObservations
    tipo: array
    origen: "guideMeditation() output — emotionalObservations"
    obrigatorio: false
  - campo: challengedPrecepts
    tipo: array
    origen: "applyPrecepts() output — dailyPrecepts"
    obrigatorio: false

Saida:
  - campo: buttonMap
    tipo: object
    destino: "trackProgress() task, activateCompassion() task"
    persistido: true
  - campo: reframedMemory
    tipo: object
    destino: "activateCompassion() task — para conversão em voto"
    persistido: true
  - campo: bodyMindReport
    tipo: object
    destino: "orchestrateDailyCycle() registro, trackProgress() task"
    persistido: true
  - campo: preceptConnections
    tipo: array
    destino: "applyPrecepts() task — feedback de botões para preceitos"
    persistido: false

Checklist:
  pre-conditions:
    - "[ ] Praticante disposto a investigar emoções (não forçar)"
    - "[ ] Contexto de segurança emocional estabelecido"
  post-conditions:
    - "[ ] Gatilho emocional identificado (se havia)"
    - "[ ] Sensação física associada registrada"
    - "[ ] Padrão biográfico investigado (se aplicável)"
    - "[ ] Atitude de 'campo de treino' reforçada"
  acceptance-criteria:
    - blocker: true
      criteria: "Observação trata corpo-mente como unidade inseparável"
    - blocker: true
      criteria: "Nenhum diagnóstico clínico é feito — apenas observação"
    - blocker: false
      criteria: "Conexão entre botão e preceito identificada"

Performance:
  duration_expected: "5-15 minutos"
  cost_estimated: "~400 tokens"
  cacheable: false
  parallelizable: true
  skippable_when: "Praticante não identificou gatilhos no dia"
---

# Pipeline Diagram

```
[emotionalTrigger] ───────────┐
[biographicalMemory] ─────────┤
[zazenObservations] ──────────┤
[challengedPrecepts] ─────────┤
                              ▼
                    ┌─────────────────────┐
                    │  observeEmotions()  │
                    │  (MirrorObserver)   │
                    └──────┬──────────────┘
                           │
          ┌────────────┬───┼───────────────┐
          ▼            ▼   ▼               ▼
    [buttonMap]  [reframedMemory] [bodyMindReport] [preceptConnections]
   (trackProgress) (activateComp.)  (dailyCycle)    (applyPrecepts)
```
