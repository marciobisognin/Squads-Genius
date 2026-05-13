task: financialAudit()
responsavel: "Louis"
responsavel_type: Agente
atomic_layer: Strategy

Campos:
  - campo: caseParameters
    tipo: object
    origen: legal-orchestrator
    destino: louis
    persistido: true
  - campo: researchFindings
    tipo: object
    origen: mike
    destino: louis
    persistido: true
  - campo: financialDocs
    tipo: object
    origen: usuário
    destino: louis
    persistido: false

Saida:
  - campo: financialAssessment
    tipo: object
    origen: louis
    destino: jessica,harvey,legal-orchestrator
    persistido: true

Checklist:
  pre-condicoes:
    - "[ ] Parâmetros do caso e pesquisa jurídica disponíveis"
    - "[ ] Documentos financeiros fornecidos"
  post-condicoes:
    - "[ ] Análise financeira e tributária realizada"
    - "[ ] Probabilidades de sucesso em contencioso tributário estimadas"
    - "[ ] Artefato `financial-assessment.json` criado"