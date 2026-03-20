---
task: executeAppeal()
responsavel: RedTeamer
responsavel_type: Agente
atomic_layer: Molecule
contrato:
  Entrada:
    - campo: "productiveSourceCode"
      tipo: "Source Code"
      origem: "implementTrialCode()"
      obrigatorio: true
    - campo: "failingTestSuite"
      tipo: "Source Code"
      origem: "writeFailingTests()"
      obrigatorio: true
  Saida:
    - campo: "appealResult"
      tipo: "Boolean"
      destino: "generateVerdictReport()"
      persistido: false
    - campo: "appealFeedback"
      tipo: "Markdown Text"
      destino: "generateAccusations()"
      persistido: false
  Checklist:
    pre_condicoes:
      - "Código produtivo estável acompanhado da suíte de testes."
    post_condicoes:
      - "A solução foi testada adversariamente em seus edge cases."
      - "Se uma quebra nova foi identificada, appealFeedback é enviado devolvendo à Fase 1."
---

## Pipeline Diagram

```
[implementTrialCode()] ──productiveSourceCode──> [executeAppeal()] ──appealResult──> [generateVerdictReport()]
```

## Descrição da Tarefa

Na Fase 4 (Appeal), entra o RedTeamer. Ele assume que a sua solução implementada (mesmo passando nos testes criados) esconde falhas. O agente varre agressivamente o código buscando race conditions obscuras, type confusions omitidos e estresse operacional. Se a solução quebrar categoricamente, a tarefa emite "appealFeedback" e reinicia o relógio. Se sobreviver ao ataque, emite "appealResult" positivo.
