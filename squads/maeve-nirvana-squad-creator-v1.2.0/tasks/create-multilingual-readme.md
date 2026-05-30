---
task: createMultilingualReadme()
responsavel: "ReadmeCreator"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: analysisMd
    tipo: file
    descricao: "analyzeRequirements() task output"
    obrigatorio: true
  - nome: squadYaml
    tipo: file
    descricao: "createWorkflows() task output"
    obrigatorio: true
  - nome: agentFiles
    tipo: array<file>
    descricao: "createAgents() task output (pós-otimização)"
    obrigatorio: true
  - nome: taskFiles
    tipo: array<file>
    descricao: "createTasks() task output (pós-otimização)"
    obrigatorio: true
  - nome: workflowFiles
    tipo: array<file>
    descricao: "createWorkflows() task output (pós-otimização)"
    obrigatorio: true

Saida:
  - nome: readmePtBr
    tipo: file
    descricao: "deploy workspace (README.md)"
    obrigatorio: true
  - nome: readmeEn
    tipo: file
    descricao: "deploy workspace (README.en.md)"
    obrigatorio: true
  - nome: readmeZh
    tipo: file
    descricao: "deploy workspace (README.zh.md)"
    obrigatorio: true
  - nome: readmeHi
    tipo: file
    descricao: "deploy workspace (README.hi.md)"
    obrigatorio: true
  - nome: readmeEs
    tipo: file
    descricao: "deploy workspace (README.es.md)"
    obrigatorio: true
  - nome: readmeAr
    tipo: file
    descricao: "deploy workspace (README.ar.md)"
    obrigatorio: true

Checklist:
  pre-conditions:
    - "[ ] Validação PASSED (fase 6 aprovada com 6 categorias OK)"
    - "[ ] squad.yaml existe com name, version, description"
    - "[ ] Agentes, tasks e workflows existem e estão otimizados"
    - "[ ] analysis.md disponível para contexto de domínio"
  post-conditions:
    - "[ ] 6 READMEs gerados: PT-BR, EN, ZH, HI, ES, AR"
    - "[ ] Estrutura idêntica em todos os idiomas (mesmas seções, mesma ordem)"
    - "[ ] Code blocks idênticos em todos os idiomas (não traduzidos)"
    - "[ ] Tabelas de agentes e tasks consistentes"
    - "[ ] Links internos corretos em todos os arquivos"
    - "[ ] Badges de idioma no topo de cada README"

Performance:
  duration_expected: "3-6 minutos"
  cost_estimated: "~6000 tokens (Opus)"
  cacheable: false
  parallelizable: true
  skippable_when: "Usuário solicitar explicitamente skip de README multilíngue"

Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: "5s"
  fallback: "Gerar apenas README em PT-BR e EN, marcar demais idiomas como pendentes"
  notification: "orchestrator"

Metadata:
  story: "Como squad publicável, preciso de documentação em 6 idiomas para alcance global"
  version: "1.0.0"
  dependencies:
    - validateSquad()
  author: "Squad Creator"
  created_at: "2026-02-22T00:00:00Z"
  updated_at: "2026-02-22T00:00:00Z"
---

# createMultilingualReadme()

## Pipeline Diagram

```
┌──────────────┐  ┌──────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ analysis.md  │  │ squad    │  │ agents/*.md  │  │ tasks/*.md   │  │ workflows/   │
│              │  │ .yaml    │  │              │  │              │  │ *.yaml       │
└──────┬───────┘  └────┬─────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │               │               │                 │                 │
       └───────┬───────┴───────────────┴─────────────────┴─────────────────┘
               │
               ▼
      ┌──────────────────┐
      │  ReadmeCreator    │
      │  (squad-readme-   │
      │   creator)        │
      └────────┬──────────┘
               │
    ┌──────────┼──────────┬──────────┬──────────┬──────────┐
    │          │          │          │          │          │
    ▼          ▼          ▼          ▼          ▼          ▼
┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
│README  ││README  ││README  ││README  ││README  ││README  │
│.md     ││.en.md  ││.zh.md  ││.hi.md  ││.es.md  ││.ar.md  │
│(PT-BR) ││(EN)    ││(ZH)    ││(HI)    ││(ES)    ││(AR)    │
└────────┘└────────┘└────────┘└────────┘└────────┘└────────┘
```

## Descrição

A task `createMultilingualReadme()` é a **sétima fase** do pipeline. Gera documentação completa do squad em 6 idiomas para maximizar o alcance global.

### Responsabilidades

1. **Geração do README Base (PT-BR)** — Criar README.md completo com:
   - Nome do squad, versão e descrição
   - Badges de idioma com links para as versões traduzidas
   - Visão geral do squad e domínio
   - Tabela de agentes com nome, role, archetype
   - Tabela de tasks com identifier, responsável, atomic_layer
   - Descrição dos workflows com agent_sequence
   - Instruções de instalação e uso
   - Estrutura de diretórios
   - Licença e créditos

2. **Tradução para 5 Idiomas** — A partir do README base, gerar versões em:
   - **EN** (Inglês) — README.en.md
   - **ZH** (Chinês Simplificado) — README.zh.md
   - **HI** (Hindi) — README.hi.md
   - **ES** (Espanhol) — README.es.md
   - **AR** (Árabe) — README.ar.md

3. **Consistência entre Idiomas** — Garantir que:
   - Todas as versões têm exatamente as mesmas seções na mesma ordem
   - Code blocks não são traduzidos (preservar exatamente como no original)
   - Nomes técnicos (agent IDs, task identifiers, workflow names) não são traduzidos
   - Tabelas têm o mesmo número de linhas e colunas
   - Links internos apontam para os arquivos corretos do idioma

### Badges de Idioma

Cada README inclui no topo:
```markdown
[Português](README.md) | [English](README.en.md) | [中文](README.zh.md) | [हिन्दी](README.hi.md) | [Español](README.es.md) | [العربية](README.ar.md)
```

### Regras de Geração

- README.md (PT-BR) é o arquivo principal — sempre gerado primeiro
- Selecionar preset visual antes de escrever: `parchment-goal-flow` para pedagogia/aprendizado/investigação; `dark-neon-layered-architecture` para negócios/operação/produto/tecnologia
- Termos técnicos AIOS não são traduzidos (squad, agent, task, workflow, etc.)
- Code blocks são copiados verbatim entre idiomas
- Estrutura de seções é idêntica — apenas texto narrativo é traduzido
- UTF-8 obrigatório com acentuação correta em todos os idiomas
