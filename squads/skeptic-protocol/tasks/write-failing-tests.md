---
task: writeFailingTests()
responsavel: "TestEngineer"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: accusationsList
    tipo: file
    obrigatorio: true
    descricao: "Lista de acusações gerada na Fase 1 (generateAccusations())."

Saida:
  - nome: failingTestSuite
    tipo: file
    obrigatorio: true
    descricao: "Suíte de testes automatizados que falham (destino: implementTrialCode())."

Checklist:
  pre-conditions:
    - "[ ] Lista de acusações (Fase 1) foi devidamente entregue."
  post-conditions:
    - "[ ] Testes gerados DEVEM FALHAR quando executados sem o código da Fase 3."
    - "[ ] Cada acusação da Fase 1 possui pelo menos um teste correspondente."
    - "[ ] A suíte de testes deve compilar/ser sintaticamente válida."
---

## Pipeline Diagram

```
[generateAccusations()] ──accusationsList──> [writeFailingTests()] ──failingTestSuite──> [implementTrialCode()]
```

## Descrição da Tarefa

A tarefa técnica da Fase 2. O agente traduz as acusações abstratas da Fase 1 em testes automatizados concretos. O objetivo é criar a "Red Phase" do TDD. Os testes servem como a especificação executável que o código da Fase 3 deve satisfazer. Se um teste passar antes da Fase 3, ele é considerado inválido e deve ser ajustado para provar a falha prevista.
