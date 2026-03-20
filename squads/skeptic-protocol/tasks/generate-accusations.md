---
task: generateAccusations()
responsavel: "FailurePredictor"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: projectRequirements
    tipo: string
    obrigatorio: true
    descricao: "Requisitos ou objetivos base do sistema fornecidos pelo usuário ou orquestrador."
  - nome: appealFeedback
    tipo: string
    obrigatorio: false
    descricao: "Feedback adversarial da Fase 4 (executeAppeal) para refinamento de acusações."

Saida:
  - nome: accusationsList
    tipo: file
    obrigatorio: true
    descricao: "Lista documentada de vulnerabilidades e falhas lógicas (destino: writeFailingTests())."

Checklist:
  pre-conditions:
    - "[ ] Requisitos ou objetivos base do sistema foram fornecidos."
  post-conditions:
    - "[ ] Zero linhas de código de implementação foram geradas."
    - "[ ] Todas as acusações contêm: Título, Descrição, Severidade e Probabilidade."
---

## Pipeline Diagram

```
[Requirement Input] ──projectRequirements──> [generateAccusations()] ──accusationsList──> [writeFailingTests()]
```

## Descrição da Tarefa

A tarefa base da Fase 1 do SKEPTIC Protocol. O agente recebe os requisitos do sistema e adota uma postura de "Red Team" estrutural, imaginando cenários extremos, problemas lógicos, falhas de segurança e buracos no design. O agente documenta essas vulnerabilidades estritamente em formato de texto. Sob nenhuma hipótese código produtivo é gerado nesta fase.
