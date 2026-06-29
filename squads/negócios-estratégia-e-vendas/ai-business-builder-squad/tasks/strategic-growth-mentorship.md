---
task: strategicGrowthMentorship()
responsavel: "strategic-mentor"
responsavel_type: Agente
atomic_layer: Organism
Entrada:
  - campo: businessPerformanceData
    tipo: object
    origen: "input.md"
    obrigatorio: true
  - campo: growthObjectives
    tipo: array
    origen: "input.md"
    obrigatorio: true
  - campo: marketTrends
    tipo: object
    origen: "market-analyst.md"
    obrigatorio: true
Saida:
  - campo: strategicGrowthReport
    tipo: file
    destino: "dashboard"
    persistido: true
  - campo: mentorshipSessionTranscript
    tipo: file
    destino: "archive"
    persistido: true
  - campo: actionPlan
    tipo: object
    destino: "business-strategist.md"
    persistido: true
Checklist:
  pre-conditions:
    - "[ ] Business performance data is current and validated"
    - "[ ] Growth objectives are clearly defined and measurable"
    - "[ ] Market trend analysis is available from market-analyst"
  post-conditions:
    - "[ ] Strategic growth report is generated and stored"
    - "[ ] Mentorship session transcript is archived"
    - "[ ] Action plan is updated with specific scaling steps"
Performance:
  duration_expected: "30-60 minutes"
Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: "1m"
---
# strategicGrowthMentorship()
## Pipeline Diagram
[input.md, market-analyst.md] ──→ [strategicGrowthMentorship()] ──→ [dashboard, archive, business-strategist.md]