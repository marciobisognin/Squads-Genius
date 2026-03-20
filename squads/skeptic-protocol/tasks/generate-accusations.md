---
task: generateAccusations()
responsavel: "FailurePredictor"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - campo: projectRequirements
    tipo: "Markdown Text"
    origen: "User / Orchestrator"
    obrigatorio: true
  - campo: appealFeedback
    tipo: "Markdown Text"
    origen: "executeAppeal() output — appealFeedback"
    obrigatorio: false

Saida:
  - campo: accusationsList
    tipo: "Markdown Document"
    destino: "writeFailingTests() task — input para criação de testes"
    persistido: true

Checklist:
  pre-conditions:
    - "[ ] Requisitos ou objetivos base do sistema foram fornecidos."
  post-conditions:
    - "[ ] Zero linhas de código de implementação (linguagens de programação) foram geradas."
    - "[ ] Todas as acusações contêm: Título, Descrição, Severidade, Probabilidade."
---

## Pipeline Diagram

```
[Requirement Input] ──projectRequirements──> [generateAccusations()] ──accusationsList──> [writeFailingTests()]
```

## Descrição da Tarefa

A tarefa base da Fase 1 do SKEPTIC Protocol. O agente recebe os requisitos do sistema e adota uma postura de "Red Team" estrutural, imaginando cenários extremos, problemas lógicos, falhas de segurança e buracos no design. O agente documenta essas vulnerabilidades estritamente em formato de texto. Sob nenhuma hipótese código produtivo é gerado nesta fase.
