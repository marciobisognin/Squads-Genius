task: craftStrategy()
responsavel: "Harvey"
responsavel_type: Agente
atomic_layer: Page

Campos:
  - campo: caseParameters
    tipo: object
    origen: legal-orchestrator
    destino: harvey
    persistido: true
  - campo: judgeProfile
    tipo: object
    origen: donna
    destino: harvey
    persistido: true
  - campo: researchFindings
    tipo: object
    origen: mike
    destino: harvey
    persistido: true
  - campo: financialAssessment
    tipo: object
    origen: louis
    destino: harvey
    persistido: true
  - campo: macroStrategyBoard
    tipo: object
    origen: jessica
    destino: harvey
    persistido: true

Saida:
  - campo: strategyPlan
    tipo: file
    origen: harvey
    destino: legal-orchestrator
    persistido: true

Checklist:
  pre-condicoes:
    - "[ ] Todos os artefatos das etapas anteriores disponíveis"
    - "[ ] Loophole_Finder_Engine e Bluff_&_Leverage_Calculator configurados"
  post-condicoes:
    - "[ ] Plano estratégico agressivo pronto"
    - "[ ] Nível de risco de julgamento estimado"
    - "[ ] `killshot-strategy.pdf` ou `.md` criado"