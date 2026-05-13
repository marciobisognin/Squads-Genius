task: intakeOracle()
responsavel: "Donna"
responsavel_type: Agente
atomic_layer: Analysis

Campos:
  - campo: caseParameters
    tipo: object
    origen: legal-orchestrator
    destino: donna
    persistido: true

Saida:
  - campo: judgeProfile
    tipo: object
    origen: donna
    destino: mike,louis,jessica,harvey,legal-orchestrator
    persistido: true
  - campo: backgroundInfo
    tipo: object
    origen: donna
    destino: mike,louis,jessica,harvey,legal-orchestrator
    persistido: true

Checklist:
  pre-condicoes:
    - "[ ] Parâmetros do caso disponíveis"
    - "[ ] Jurimetrics_Oracle e E-Discovery tools configuradas"
  post-condicoes:
    - "[ ] Perfil do magistrado e background da parte contrária coletados"
    - "[ ] Artefatos disponibilizados para pesquisa, auditoria e macro-alinhamento"