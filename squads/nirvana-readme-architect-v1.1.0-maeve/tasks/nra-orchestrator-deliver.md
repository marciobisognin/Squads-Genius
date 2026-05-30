---
task: deliverReadme()
responsavel: "Quill"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: readmeFinal
    tipo: file
    descricao: "README.md finalizado (de enhanceReadme())"
    obrigatorio: true
  - nome: outputPath
    tipo: string
    descricao: "Caminho de saída para salvar o README"
    obrigatorio: true
  - nome: score
    tipo: number
    descricao: "Score final de qualidade"
    obrigatorio: true
  - nome: featuresUsed
    tipo: list
    descricao: "Features do GitHub utilizadas no README"
    obrigatorio: true

Saida:
  - nome: deliverySummary
    tipo: file
    descricao: "Resumo da entrega com métricas e caminho do arquivo salvo"
    obrigatorio: true

Checklist:
  pre-conditions:
    - "[ ] README finalizado com score >= 90"
    - "[ ] Caminho de saída definido"
  post-conditions:
    - "[ ] README salvo no caminho especificado"
    - "[ ] Resumo da entrega apresentado ao usuário"
    - "[ ] Cleanup de artefatos temporários executado"

Performance:
  duration_expected: "1 minuto"
  cost_estimated: "~500 tokens"
  cacheable: false
  parallelizable: false
  skippable_when: "Nunca — entrega é o passo final obrigatório"

Error Handling:
  strategy: retry
  retry:
    max_attempts: 3
    delay: "5s"
  fallback: "Salvar README no diretório atual com nome README-generated.md"
  notification: "orchestrator"

Metadata:
  story: "Como usuário, quero receber o README final salvo no local correto com resumo de métricas"
  version: "1.0.0"
  dependencies:
    - "enhanceReadme()"
---

# deliverReadme() — Entregar README Final

## Pipeline Diagram

```
[enhanceReadme()]
    |
    | readmeFinal, outputPath, score, featuresUsed
    v
+------------------------+
| deliverReadme()        |  <-- Quill (Orchestrator)
|      (Organism)        |
+------------------------+
    |
    | deliverySummary (file)
    v
[user] (entrega final)
```

## Descrição

Salvar o README finalizado no caminho especificado e apresentar resumo ao usuário.

## Resumo da Entrega

Apresentar ao usuário:
1. Caminho do arquivo salvo
2. Score de qualidade obtido
3. Número de seções geradas
4. Features do GitHub utilizadas
5. Métricas: linhas totais, tabelas, code blocks, diagrams

## Cleanup

- Remover artefatos temporários (drafts, reports intermediários)
- Reportar warnings pendentes (se houver)
