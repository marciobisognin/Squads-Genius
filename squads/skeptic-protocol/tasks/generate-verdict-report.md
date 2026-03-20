---
task: generateVerdictReport()
responsavel: SkepticOrchestrator
responsavel_type: Agente
atomic_layer: Molecule
contrato:
  Entrada:
    - campo: "appealResult"
      tipo: "Boolean"
      origem: "executeAppeal()"
      obrigatorio: true
    - campo: "accusationsList"
      tipo: "Markdown Document"
      origem: "generateAccusations()"
      obrigatorio: true
  Saida:
    - campo: "skepticReport"
      tipo: "Markdown Document"
      destino: "User / System"
      persistido: true
  Checklist:
    pre_condicoes:
      - "O resultado da Fase de Apelação (Appeal) deve ser positivo (True)."
    post_condicoes:
      - "Documento SKEPTIC_REPORT.md gerado, sumarizando as acusações superadas."
      - "Limitações incorrigíveis ou pontuais catalogadas na seção Oficial do Veredito."
---

## Pipeline Diagram

```
[executeAppeal()] ──appealResult──> [generateVerdictReport()] ──skepticReport──> [User]
```

## Descrição da Tarefa

A última etapa (Verdict) encerra o workflow SKEPTIC Protocol. O Orchestrator exige que a prova de robustez do sistema esteja contínua. Ele contabiliza quantas acusações da Fase 1 foram convertidas em Red Tests (Fase 2) e resolvidas pelo código produtivo (Fase 3), chanceladas pelo Apelo (Fase 4). O produto final é um documento chamado SKEPTIC_REPORT.md contendo todo o compliance alcançado.
