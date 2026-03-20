---
task: writeFailingTests()
responsavel: TestEngineer
responsavel_type: Agente
atomic_layer: Organism
Entrada:
  - campo: "accusationsList"
    tipo: "Markdown Document"
    origem: "generateAccusations()"
    obrigatorio: true
Saida:
  - campo: "failingTestSuite"
    tipo: "Test Suite File (e.g., .test.js, .test.py)"
    destino: "implementTrialCode()"
    persistido: true
Checklist:
  pre_condicoes:
    - "Lista de acusações (Fase 1) foi devidamente entregue."
  post_condicoes:
    - "Testes gerados DEVEM FALHAR quando executados sem o código da Fase 3."
    - "Cada acusação da Fase 1 possui pelo menos um teste correspondente."
    - "A suíte de testes deve compilar/ser sintaticamente válida."
---

## Pipeline Diagram

```
[generateAccusations()] ──accusationsList──> [writeFailingTests()] ──failingTestSuite──> [implementTrialCode()]
```

## Descrição da Tarefa

A tarefa técnica da Fase 2. O agente traduz as acusações abstratas da Fase 1 em testes automatizados concretos. O objetivo é criar a "Red Phase" do TDD. Os testes servem como a especificação executável que o código da Fase 3 deve satisfazer. Se um teste passar antes da Fase 3, ele é considerado inválido e deve ser ajustado para provar a falha prevista.
