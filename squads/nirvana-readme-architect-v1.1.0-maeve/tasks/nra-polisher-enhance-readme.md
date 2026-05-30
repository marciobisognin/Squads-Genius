---
task: enhanceReadme()
responsavel: "Gloss"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: readmeDraft
    tipo: file
    descricao: "README validado para polimento (de validateReadme())"
    obrigatorio: true
  - nome: validationReport
    tipo: file
    descricao: "Relatório de validação com sugestões (de validateReadme())"
    obrigatorio: true

Saida:
  - nome: readmeFinal
    tipo: file
    descricao: "README.md finalizado e polido (destino: deliverReadme() task)"
    obrigatorio: true

Checklist:
  pre-conditions:
    - "[ ] README draft com score >= 75"
    - "[ ] Relatório de validação disponível"
  post-conditions:
    - "[ ] TOC reflete exatamente as seções H2 presentes"
    - "[ ] Badges alinhados com estilo consistente"
    - "[ ] Espaçamento uniforme entre seções"
    - "[ ] Collapsed sections para blocos > 30 linhas"
    - "[ ] Nenhum conteúdo removido — apenas apresentação melhorada"

Performance:
  duration_expected: "3 minutos"
  cost_estimated: "~2500 tokens"
  cacheable: false
  parallelizable: false
  skippable_when: "Score já >= 95 e nenhuma sugestão visual pendente"

Error Handling:
  strategy: retry
  retry:
    max_attempts: 3
    delay: "5s"
  fallback: "Entregar README sem polimento com advisory de melhorias visuais pendentes"
  notification: "orchestrator"

Metadata:
  story: "Como usuário, quero que meu README tenha polimento visual perfeito antes da entrega"
  version: "1.0.0"
  dependencies:
    - "validateReadme()"
---

# enhanceReadme() — Polimento Final do README

## Pipeline Diagram

```
[validateReadme()]
    |
    | readmeDraft, validationReport
    v
+------------------------+
| enhanceReadme()        |  <-- Gloss (Polisher)
|      (Organism)        |
+------------------------+
    |
    | readmeFinal (file)
    v
[deliverReadme()]
```

## Descrição

Aplicar polimento visual e estrutural ao README para atingir nível Nirvana de qualidade.

## Etapas de Polimento

1. **Corrigir** itens apontados no relatório de validação
2. **Gerar/Atualizar** TOC com links âncora corretos
3. **Alinhar** badges em layout consistente
4. **Uniformizar** espaçamento (1 linha em branco entre seções)
5. **Envolver** blocos longos em collapsed sections
6. **Converter** URLs longas em reference-style links
7. **Verificar** renderização de mermaid diagrams
8. **Adicionar** badges faltantes (build, version, license)
9. **Revisar** consistência de emojis
10. **Validar** encoding UTF-8

## Regras

- NUNCA alterar conteúdo semântico — apenas formatação
- Manter TODA acentuação PT-BR intacta
- Estilo de badge consistente (mesmo style parameter)
- TOC deve ser a primeira seção após badges/descrição
