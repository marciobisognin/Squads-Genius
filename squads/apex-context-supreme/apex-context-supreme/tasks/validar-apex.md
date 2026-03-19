---
task: validarContexto()
responsavel: "Vigil"
responsavel_type: Agente
atomic_layer: Molecule

Entrada:
  - nome: optimizedRuleFiles
    tipo: array
    descricao: "Arquivos processados e otimizados pelo Trim"
    obrigatorio: true

Saida:
  - nome: validationReport
    tipo: file
    descricao: "Relatório de conformidade final (validation-report.md)"
    obrigatorio: true
  - nome: acceptanceStatus
    tipo: boolean
    descricao: "Status final de aceitação (True/False)"
    obrigatorio: true

Checklist:
  pre-conditions:
    - "[ ] Todos os arquivos otimizados existem Fisicamente"
    - "[ ] Checklist de qualidade (apex-quality-gate.md) acessível"
  post-conditions:
    - "[ ] Sintaxe Markdown validada em todos os arquivos de saída"
    - "[ ] Todos os links internos nos arquivos .md são funcionais"
    - "[ ] Conformidade com a stack tecnológica verificada"

Performance:
  duration_expected: "1-2 minutos"
  cost_estimated: "~800 tokens (Sonnet/Flash)"
  cacheable: false
  parallelizable: true
  skippable_when: "Nunca — a última barreira de qualidade é obrigatória"

Error Handling:
  strategy: retry
  retry:
    max_attempts: 1
  fallback: "Em caso de falha crítica na validação, Apex deve suspender a entrega final"
  notification: "apex-orquestrista"

Metadata:
  story: "Como guardiã da qualidade, preciso garantir que o contexto final seja livre de erros e siga os padrões"
  version: "1.0.0"
  author: "Nirvana Squad Creator (Refined)"
---

# validarContexto()

## Pipeline Diagram
```
┌───────────────┐     ┌───────────────┐     ┌───────────────────────┐
│ Regras Otimiz.│────▶│    Vigil      │────▶│  Relatório de Validação│
│ (.md Files)   │     │ (vigil-guard) │     │  validation-report.md  │
└───────────────┘     └───────────────┘     └───────────────────────┘
                               │                      │
                               │ Phase 4              │ Finaliza Apex
                               ▼                      ▼
                        ┌────────────┐         ┌───────────────┐
                        │ Compliance │         │ Approved/Fail │
                        │ Syntax Check│         │ Status        │
                        └────────────┘         └───────────────┘
```

## Descrição
A task `validarContexto()` realiza a inspeção final de todos os artefatos gerados. Ela garante que não houve corrupção de dados durante as fases de alquimia ou escultura e que o resultado final está perfeitamente alinhado com as especificações AIOS e as necessidades técnicas do projeto.
