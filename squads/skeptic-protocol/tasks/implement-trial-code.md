---
task: implementTrialCode()
responsavel: "SolutionImplementer"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - campo: failingTestSuite
    tipo: "Test Suite File"
    origen: "writeFailingTests() output — failingTestSuite"
    obrigatorio: true

Saida:
  - campo: productiveSourceCode
    tipo: "Source Code File"
    destino: "executeAppeal() task — input para revisão adversarial"
    persistido: true

Checklist:
  pre-conditions:
    - "[ ] Existe uma suíte de testes falhando que cobre as acusações iniciais."
  post-conditions:
    - "[ ] A suíte de testes da Fase 2 agora PASSA integralmente."
    - "[ ] O código implementado segue os padrões de tecnologia definidos no squad."
    - "[ ] Nenhum código extra (over-engineering) foi adicionado além do necessário para passar nos testes."
---

## Pipeline Diagram

```
[writeFailingTests()] ──failingTestSuite──> [implementTrialCode()] ──productiveSourceCode──> [executeAppeal()]
```

## Descrição da Tarefa

O "Julgamento" (Fase 3). O agente recebe a suíte de testes que falha e escreve o código de implementação necessário para fazê-la passar. É a fase produtiva onde a solução ganha vida. O sucesso é binário: o código ou satisfaz a "Acusação" (passando nos testes da Fase 2) ou o julgamento continua.
