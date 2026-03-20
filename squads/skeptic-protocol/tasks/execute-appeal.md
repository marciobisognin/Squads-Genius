---
task: executeAppeal()
responsavel: RedTeamer
responsavel_type: Agente
atomic_layer: Molecule
Entrada:
  - campo: "productiveSourceCode"
    tipo: "Source Code File"
    origem: "implementTrialCode()"
    obrigatorio: true
Saida:
  - campo: "appealResult"
    tipo: "Boolean"
    destino: "skeptic-orchestrator"
    persistido: true
  - campo: "appealFeedback"
    tipo: "Markdown Text"
    destino: "generateAccusations()"
    persistido: false
Checklist:
  pre_condicoes:
    - "O código da solução passou em todos os testes da Fase 2."
  post_condicoes:
    - "Tentativas de quebra de código (edge cases, overflow, injeção) foram realizadas."
    - "Se o código quebrar, appealResult é FALSE e feedback é enviado para a Fase 1."
    - "Se o código resistir, appealResult é TRUE."
---

## Pipeline Diagram

```
[implementTrialCode()] ──productiveSourceCode──> [executeAppeal()] ──appealResult──> [skeptic-orchestrator]
```

## Descrição da Tarefa

A "Apelação" (Fase 4). O agente assume o papel de um adversário agressivo que tenta quebrar a solução aprovada na fase anterior. Ele não usa os mesmos testes da Fase 2; em vez disso, ele cria novos cenários não previstos originalmente. Se encontrar uma falha, o protocolo é reiniciado ou o feedback é enviado para correção.
