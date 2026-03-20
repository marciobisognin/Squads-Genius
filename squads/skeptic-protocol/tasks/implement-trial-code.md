---
task: implementTrialCode()
responsavel: SolutionImplementer
responsavel_type: Agente
atomic_layer: Organism
contrato:
  Entrada:
    - campo: "failingTestSuite"
      tipo: "Source Code"
      origem: "writeFailingTests()"
      obrigatorio: true
  Saida:
    - campo: "productiveSourceCode"
      tipo: "Source Code"
      destino: "executeAppeal()"
      persistido: true
  Checklist:
    pre_condicoes:
      - "Suíte de testes de defesa deve estar pronta e (atualmente) falhando."
    post_condicoes:
      - "O código não introduz novas dependências ou lógicas arbitrárias não cobertas pelos testes."
      - "O código compilado faz toda a suíte de testes passar."
---

## Pipeline Diagram

```
[writeFailingTests()] ──failingTestSuite──> [implementTrialCode()] ──productiveSourceCode──> [executeAppeal()]
```

## Descrição da Tarefa

A Fase 3 do SKEPTIC (Trial). Ocorrendo estritamente de fora para dentro, baseando-se no comportamento imposto pela suíte construída anteriormente. O SolutionImplementer tem um único norte: refatorar, escrever e orquestrar código de domínio o suficiente para esverdear (pass) a bateria de defesas e mitigações imposta pelas acusações, sem exceder o escopo dos testes de forma perigosa.
