---
task: validateReadme()
responsavel: "Lens"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: readmeDraft
    tipo: file
    descricao: "README em draft para validação (de generateSections())"
    obrigatorio: true
  - nome: projectPath
    tipo: string
    descricao: "Caminho do projeto (para verificar links relativos)"
    obrigatorio: true

Saida:
  - nome: validationReport
    tipo: file
    descricao: "Relatório de validação com score, itens e verdict (destino: enhanceReadme() ou generateSections())"
    obrigatorio: true

Checklist:
  pre-conditions:
    - "[ ] README draft disponível"
    - "[ ] Caminho do projeto acessível"
  post-conditions:
    - "[ ] Score calculado com fórmula documentada"
    - "[ ] Cada item do checklist avaliado individualmente"
    - "[ ] Itens reprovados têm motivo específico"
    - "[ ] Verdict emitido conforme faixas de score"

Performance:
  duration_expected: "2 minutos"
  cost_estimated: "~2000 tokens"
  cacheable: false
  parallelizable: false
  skippable_when: "Nunca — validação é gate obrigatório"

Error Handling:
  strategy: retry
  retry:
    max_attempts: 3
    delay: "5s"
  fallback: "Emitir relatório parcial com itens validados e advisory sobre itens não verificados"
  notification: "orchestrator"

Metadata:
  story: "Como usuário, quero que meu README seja validado com checklist rigoroso antes da entrega"
  version: "1.0.0"
  dependencies:
    - "generateSections()"
---

# validateReadme() — Validar README com Checklist

## Pipeline Diagram

```
[generateSections()]
    |
    | readmeDraft, projectPath
    v
+------------------------+
| validateReadme()       |  <-- Lens (Quality Validator)
|      (Organism)        |
+------------------------+
    |
    | validationReport (file)
    v
[enhanceReadme()] ou [generateSections()] (se retrabalho)
```

## Descrição

Executar validação completa do README draft usando checklist de 25+ pontos e gerar score de qualidade.

## Processo de Validação

1. **Ler** o README draft completo
2. **Avaliar** cada ponto do checklist (ver `checklists/readme-quality.md`)
3. **Calcular** score com pesos (Blocking 2x, Advisory 1x)
4. **Gerar** relatório com passes, falhas e sugestões
5. **Emitir** verdict: APROVADO (>= 90), POLIR (75-89), RETRABALHAR (< 75)

## Validações Técnicas

- **Code blocks**: Regex para verificar se TODOS têm linguagem após ` ``` `
- **Mermaid**: Verificar abertura `mermaid` e fechamento ` ``` `, keywords válidas (graph, flowchart, sequenceDiagram, etc.)
- **Alerts**: Verificar sintaxe `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`
- **Badges**: Verificar padrão `![text](url)` com URL shields.io ou similar
- **TOC links**: Verificar que cada link `#anchor` corresponde a um heading existente
- **Relative links**: Verificar que arquivos referenciados existem no projeto
