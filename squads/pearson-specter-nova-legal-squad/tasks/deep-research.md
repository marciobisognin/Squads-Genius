task: deepResearch()
responsavel: "Mike"
responsavel_type: Agente
atomic_layer: Strategy

Campos:
  - campo: caseParameters
    tipo: object
    origen: legal-orchestrator
    destino: mike
    persistido: true
  - campo: backgroundInfo
    tipo: object
    origen: donna
    destino: mike
    persistido: true

Saida:
  - campo: researchFindings
    tipo: object
    origen: mike
    destino: louis,jessica,harvey,legal-orchestrator
    persistido: true

Checklist:
  pre-condicoes:
    - "[ ] Parâmetros do caso e background disponíveis"
    - "[ ] Acesso a bancos de jurisprudência configurado"
  post-condicoes:
    - "[ ] Tese jurídica construída e precedentes relevantes mapeados"
    - "[ ] Inconsistências adversárias destacadas"
    - "[ ] Documento `legal-thesis-defense.md` gerado"