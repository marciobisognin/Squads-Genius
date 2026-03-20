---
task: writeFailingTests()
responsavel: TestEngineer
responsavel_type: Agente
atomic_layer: Organism
contrato:
  Entrada:
    - campo: "accusationsList"
      tipo: "Markdown Document"
      origem: "generateAccusations()"
      obrigatorio: true
  Saida:
    - campo: "failingTestSuite"
      tipo: "Source Code"
      destino: "implementTrialCode()"
      persistido: true
  Checklist:
    pre_condicoes:
      - "Lista de acusações estruturada deve estar disponível."
    post_condicoes:
      - "Todos os testes gerados falham contra a codebase atual (vazia ou vulnerável)."
      - "Cada acusação grave mapeia para no mínimo um teste específico."
---

## Pipeline Diagram

```
[generateAccusations()] ──accusationsList──> [writeFailingTests()] ──failingTestSuite──> [implementTrialCode()]
```

## Descrição da Tarefa

Na Fase 2 do SKEPTIC (Defense), o TestEngineer deve decodificar as "Acusações" concebidas na fase anterior para código-fonte de teste automatizado (Unitário, Integração ou E2E, dependendo da plataforma-alvo). O objetivo é garantir que as vulnerabilidades previstas não sejam apenas teóricas; a suíte deve estar vermelha (failing) antes de qualquer implementação ser feita.
