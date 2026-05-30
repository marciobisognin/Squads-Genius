---
task: generateSections()
responsavel: "Serif"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: projectAnalysis
    tipo: file
    descricao: "Dados do scan do codebase (de scanProject())"
    obrigatorio: true
  - nome: templateConfig
    tipo: file
    descricao: "Template selecionado com seções e features (de selectTemplate())"
    obrigatorio: true

Saida:
  - nome: readmeDraft
    tipo: file
    descricao: "README.md completo em draft (destino: validateReadme() task)"
    obrigatorio: true

Checklist:
  pre-conditions:
    - "[ ] Análise do codebase disponível"
    - "[ ] Template selecionado"
    - "[ ] Lista de seções definida"
  post-conditions:
    - "[ ] Todas as seções da lista foram geradas"
    - "[ ] Mínimo 8 features distintas do GitHub utilizadas"
    - "[ ] Todos os code blocks têm linguagem especificada"
    - "[ ] Mermaid diagram presente na seção Architecture"
    - "[ ] Mínimo 3 alerts distintos utilizados"
    - "[ ] TOC gerado com links âncora"

Performance:
  duration_expected: "5 minutos"
  cost_estimated: "~5000 tokens"
  cacheable: false
  parallelizable: false
  skippable_when: "Nunca — é o core da geração de conteúdo"

Error Handling:
  strategy: retry
  retry:
    max_attempts: 3
    delay: "5s"
  fallback: "Retry com template Library como fallback"
  notification: "orchestrator"

Metadata:
  story: "Como usuário, quero que cada seção do README contenha conteúdo real e acionável baseado no meu projeto"
  version: "1.0.0"
  dependencies:
    - "scanProject()"
    - "selectTemplate()"
---

# generateSections() — Gerar Conteúdo das Seções

## Pipeline Diagram

```
[scanProject()]     [selectTemplate()]
    |                       |
    | projectAnalysis       | templateConfig
    +-----------+-----------+
                |
                v
+-----------------------------+
| generateSections()          |  <-- Serif (Content Architect)
|         (Organism)          |
+-----------------------------+
                |
                | readmeDraft (file)
                v
       [validateReadme()]
```

## Descrição

Gerar conteúdo real e acionável para CADA seção do README, utilizando os dados do scan do codebase e as features do GitHub mapeadas.

## Regras de Geração

### Para CADA seção:
1. Usar dados REAIS do scan (nunca inventar)
2. Aplicar features do GitHub mapeadas para aquela seção
3. Code blocks SEMPRE com linguagem (```bash, ```typescript, etc.)
4. Comandos de instalação devem ser copy-paste funcionais
5. Exemplos devem refletir o projeto real

### Features Obrigatórias (mínimo 8 de 15):
- [ ] Headings com âncoras (automático)
- [ ] Bold/Italic para ênfase
- [ ] Code blocks com syntax highlighting
- [ ] Tables com header
- [ ] Task lists
- [ ] Alerts (NOTE, TIP, WARNING, IMPORTANT, CAUTION)
- [ ] Mermaid diagrams
- [ ] Collapsed sections (`<details>`)
- [ ] Badges shields.io
- [ ] Emojis
- [ ] Footnotes
- [ ] kbd tags
- [ ] Diff blocks
- [ ] Relative links
- [ ] Reference-style links

### Conteúdo Proibido:
- Placeholders genéricos como "Lorem ipsum" ou "TODO"
- Links para `example.com`
- Dados inventados que não existem no projeto
- Code blocks sem linguagem especificada
