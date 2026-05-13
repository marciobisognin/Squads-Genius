---
task: ideationAndValidation()
responsavel: "market-analyst"
responsavel_type: Agente
atomic_layer: Molecule
Entrada:
  - campo: nicheDescription
    tipo: string
    origen: "user_input"
    obrigatorio: true
  - campo: marketTrendsData
    tipo: object
    origen: "market-analyst"
    obrigatorio: true
Saida:
  - campo: validatedBusinessConcept
    tipo: object
    destino: "brand-identity-creation.md"
    persistido: true
  - campo: validationReport
    tipo: file
    destino: "strategic-mentor.md"
    persistido: true
Checklist:
  pre-conditions:
    - "[ ] Target niche or industry is defined"
    - "[ ] Real-time market trend data is accessible"
  post-conditions:
    - "[ ] Business idea is scored against feasibility and demand"
    - "[ ] Validation report includes SWOT analysis"
Performance:
  duration_expected: "10-20 minutes"
Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: "10s"
---
# ideationAndValidation()
## Pipeline Diagram
nicheDescription + marketTrendsData ──→ [ideationAndValidation()] ──→ validatedBusinessConcept ──→ [brandIdentityCreation()]