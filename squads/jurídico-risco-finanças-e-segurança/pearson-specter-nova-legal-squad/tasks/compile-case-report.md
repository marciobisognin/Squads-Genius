task: compileCaseReport()
responsavel: "Legal Orchestrator"
responsavel_type: Agente
atomic_layer: Page

Campos:
  - campo: caseParameters
    tipo: object
    origen: legal-orchestrator
    destino: legal-orchestrator
    persistido: true
  - campo: judgeProfile
    tipo: object
    origen: donna
    destino: legal-orchestrator
    persistido: true
  - campo: researchFindings
    tipo: object
    origen: mike
    destino: legal-orchestrator
    persistido: true
  - campo: financialAssessment
    tipo: object
    origen: louis
    destino: legal-orchestrator
    persistido: true
  - campo: macroStrategyBoard
    tipo: object
    origen: jessica
    destino: legal-orchestrator
    persistido: true
  - campo: strategyPlan
    tipo: file
    origen: harvey
    destino: legal-orchestrator
    persistido: true

Saida:
  - campo: finalCaseReport
    tipo: file
    origen: legal-orchestrator
    destino: usuário
    persistido: true

Checklist:
  pre-condicoes:
    - "[ ] Todos os artefatos de caso disponíveis"
  post-condicoes:
    - "[ ] Relatório final compilado com teses, auditorias, macro estratégias e plano final"
    - "[ ] Arquivo entregue ao cliente"