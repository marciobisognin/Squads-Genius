---
task: selectTemplate()
responsavel: "Serif"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: projectType
    tipo: string
    descricao: "Tipo do projeto (Library, CLI, Web App, API, Monorepo, Mobile, Squad AIOS)"
    obrigatorio: true
  - nome: scope
    tipo: string
    descricao: "Escopo: full ou quick"
    obrigatorio: true

Saida:
  - nome: templateConfig
    tipo: file
    descricao: "Configuração do template com seções e features mapeadas (destino: generateSections() task)"
    obrigatorio: true

Checklist:
  pre-conditions:
    - "[ ] Tipo de projeto definido"
    - "[ ] Escopo definido"
  post-conditions:
    - "[ ] Template selecionado compatível com tipo de projeto"
    - "[ ] Lista de seções gerada (12+ para full, 6 para quick)"
    - "[ ] Features do GitHub mapeadas para cada seção"

Performance:
  duration_expected: "1 minuto"
  cost_estimated: "~500 tokens"
  cacheable: true
  parallelizable: false
  skippable_when: "Nunca — template define estrutura do README"

Error Handling:
  strategy: retry
  retry:
    max_attempts: 3
    delay: "5s"
  fallback: "Usar template Library como fallback universal"
  notification: "orchestrator"

Metadata:
  story: "Como usuário, quero que o template do README seja selecionado automaticamente com base no tipo do meu projeto"
  version: "1.0.0"
  dependencies:
    - "scanProject()"
---

# selectTemplate() — Selecionar Template por Tipo de Projeto

## Pipeline Diagram

```
[scanProject()]
    |
    | projectType, scope
    v
+------------------------+
| selectTemplate()       |  <-- Serif (Content Architect)
|      (Organism)        |
+------------------------+
    |
    | templateConfig (file)
    v
[generateSections()]
```

## Descrição

Escolher o template mais adequado baseado no tipo de projeto e escopo solicitado.

## Mapeamento de Seções por Escopo

### Full (12+ seções)
1. Header (badges + descrição)
2. Overview
3. Tech Stack
4. Prerequisites
5. Getting Started
6. Architecture
7. Environment Variables
8. Available Scripts
9. Testing
10. Deployment
11. Troubleshooting
12. Contributing + License

### Quick (6 seções)
1. Header (badges + descrição)
2. Overview + Tech Stack
3. Getting Started
4. Usage
5. Scripts + Testing
6. License

## Mapeamento de Features GitHub por Seção

| Seção | Features Obrigatórias |
|-------|----------------------|
| Header | Badges, emojis |
| Overview | Bold, italic, alerts (TIP) |
| Tech Stack | Table |
| Prerequisites | Task list, alerts (WARNING) |
| Getting Started | Code blocks, task list, alerts (NOTE) |
| Architecture | Mermaid diagram, collapsed section |
| Env Variables | Table, alerts (IMPORTANT) |
| Scripts | Table, code blocks |
| Testing | Code blocks, alerts (TIP) |
| Deployment | Code blocks, alerts (CAUTION) |
| Troubleshooting | Table, collapsed sections |
| Contributing | Footnotes, relative links |
