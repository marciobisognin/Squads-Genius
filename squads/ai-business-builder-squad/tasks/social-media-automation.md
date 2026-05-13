---
task: socialMediaAutomation()
responsavel: "ContentStrategist"
responsavel_type: Agente
atomic_layer: Organism
Entrada:
  - campo: contentCalendar
    tipo: object
    origen: "brand-identity-creation.md"
    obrigatorio: true
  - campo: platformCredentials
    tipo: object
    origen: "vault"
    obrigatorio: true
  - campo: brandAssets
    tipo: array
    origen: "brand-identity-creation.md"
    obrigatorio: true
Saida:
  - campo: automationWorkflow
    tipo: file
    destino: "business-launch-pipeline.yaml"
    persistido: true
  - campo: scheduledPosts
    tipo: array
    destino: "social-media-platforms"
    persistido: true
Checklist:
  pre-conditions:
    - "[ ] Content calendar is finalized"
    - "[ ] API keys for social platforms are configured"
  post-conditions:
    - "[ ] Automation scripts are active"
    - "[ ] First batch of posts is scheduled"
Performance:
  duration_expected: "30-60 minutes"
Error Handling:
  strategy: retry
  retry:
    max_attempts: 3
    delay: "10s"
---
# socialMediaAutomation()
## Pipeline Diagram
contentCalendar ──→ [socialMediaAutomation()] ──→ automationWorkflow ──→ [business-launch-pipeline.yaml]