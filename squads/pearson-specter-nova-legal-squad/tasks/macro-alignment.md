task: macroAlignment()
responsavel: "Jessica"
responsavel_type: Agente
atomic_layer: Strategy

Campos:
  - campo: caseParameters
    tipo: object
    origen: legal-orchestrator
    destino: jessica
    persistido: true
  - campo: researchFindings
    tipo: object
    origen: mike
    destino: jessica
    persistido: true
  - campo: financialAssessment
    tipo: object
    origen: louis
    destino: jessica
    persistido: true

Saida:
  - campo: macroStrategyBoard
    tipo: object
    origen: jessica
    destino: harvey,legal-orchestrator
    persistido: true

Checklist:
  pre-condicoes:
    - "[ ] Parâmetros do caso, pesquisa e avaliação financeira disponíveis"
    - "[ ] Modelos de impacto regulatório e antitruste acessíveis"
  post-condicoes:
    - "[ ] Avaliação de risco regulatório e macro estratégia finalizada"
    - "[ ] `macro-strategy-board.md` criado"