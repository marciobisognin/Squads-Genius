---
task: marketingFunnelDesign()
responsavel: "funnel-engineer"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - campo: businessModel
    tipo: object
    origen: "input.md"
    obrigatorio: true
  - campo: targetAudience
    tipo: object
    origen: "input.md"
    obrigatorio: true
  - campo: offerDetails
    tipo: object
    origen: "input.md"
    obrigatorio: true
  - campo: funnelComplexity
    tipo: string
    origen: "input.md"
    obrigatorio: true

Saida:
  - campo: funnelArchitecture
    tipo: object
    destino: "content-to-conversion-flow.yaml"
    persistido: true
  - campo: landingPageWireframe
    tipo: file
    destino: "storage/funnels/"
    persistido: true
  - campo: emailSequenceMap
    tipo: file
    destino: "storage/funnels/"
    persistido: true

Checklist:
  pre-conditions:
    - "[ ] Business model and target audience are defined"
    - "[ ] Core offer and pricing are established"
    - "[ ] Marketing goals (leads vs sales) are specified"
  post-conditions:
    - "[ ] Funnel stages (TOFU, MOFU, BOFU) are mapped"
    - "[ ] Conversion triggers and automation logic are defined"
    - "[ ] Open-source tool stack for implementation is recommended"

Performance:
  duration_expected: "15-30 minutes"

Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: "10s"
---
# marketingFunnelDesign()

## Pipeline Diagram
input.md ──→ [marketingFunnelDesign()] ──→ funnelArchitecture ──→ [content-to-conversion-flow.yaml]

## Description
This task designs a comprehensive marketing funnel tailored to the business model and target audience. It utilizes global frameworks like AIDA (Attention, Interest, Desire, Action) or PAS (Problem, Agitation, Solution) to map out the customer journey from initial awareness to final conversion. The output includes the logical architecture, wireframe structures for landing pages, and the mapping of automated email sequences using open-source compatible logic.