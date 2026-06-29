task: defineCase()
responsavel: "Legal Orchestrator"
responsavel_type: Agente
atomic_layer: Analysis

Campos:
  - campo: clientName
    tipo: string
    origen: usuário
    destino: legal-orchestrator
    persistido: true
  - campo: caseDescription
    tipo: string
    origen: usuário
    destino: legal-orchestrator
    persistido: true
  - campo: caseType
    tipo: string
    origen: usuário
    destino: legal-orchestrator
    persistido: true
  - campo: analysisDepth
    tipo: string
    origen: usuário
    destino: legal-orchestrator
    persistido: true

Saida:
  - campo: caseParameters
    tipo: object
    origen: legal-orchestrator
    destino: agentes
    persistido: true

Checklist:
  pre-condicoes:
    - "[ ] Informações básicas do cliente e do caso foram fornecidas"
    - "[ ] Tipo de caso (ex.: societário, penal, tributário, concorrencial) definido"
  post-condicoes:
    - "[ ] Parâmetros do caso armazenados e prontos para as próximas etapas"
    - "[ ] Handoff iniciado para Donna"