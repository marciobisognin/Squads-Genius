---
task: arquitetarContexto()
responsavel: "Maven"
responsavel_type: Agente
atomic_layer: Molecule

Entrada:
  - nome: projectRoot
    tipo: string
    descricao: "Diretório raiz do projeto alvo"
    obrigatorio: true
  - nome: targetPlatforms
    tipo: array
    descricao: "Plataformas para as quais o contexto deve ser otimizado (do squad.yaml)"
    obrigatorio: true

Saida:
  - nome: contextBlueprint
    tipo: file
    descricao: ".apex-context/blueprint.yaml (blueprint estrutural para Spark)"
    obrigatorio: true
  - nome: technicalInventory
    tipo: file
    descricao: ".apex-context/inventory.json (inventário técnico completo)"
    obrigatorio: true

Checklist:
  pre-conditions:
    - "[ ] Diretório raiz do projeto acessível e lido"
    - "[ ] Diretório .apex-context/ existe e é gravável"
    - "[ ] Escaneamento técnico recursivo (ls -R) realizado"
  post-conditions:
    - "[ ] blueprint.yaml contém a lista de arquivos de regras necessários"
    - "[ ] inventory.json lista todas as tecnologias dominantes e ativos de código"
    - "[ ] Nenhuma dependência externa não mapeada no inventário"

Performance:
  duration_expected: "1-3 minutos"
  cost_estimated: "~1000 tokens (Sonnet/Flash)"
  cacheable: true
  parallelizable: false
  skippable_when: "Nenhuma alteração na estrutura de diretórios foi detectada desde a última execução"

Error Handling:
  strategy: fallback
  fallback: "Se o escaneamento recursivo falhar, gerar um inventário básico a partir da raiz do projeto"
  notification: "apex-orquestrista"

Metadata:
  story: "Como orquestrador, preciso de um blueprint técnico da estrutura do projeto para planejar o enriquecimento do contexto"
  version: "1.0.0"
  author: "Nirvana Squad Creator (Refined)"
---

# arquitetarContexto()

## Pipeline Diagram
```
┌─────────────┐     ┌───────────────┐     ┌───────────────────────┐
│ projectRoot  │────▶│    Maven      │────▶│  blueprint.yaml       │
│ (string)     │     │ (maven-arch)  │     │  inventory.json       │
└─────────────┘     └───────────────┘     └───────────────────────┘
                               │                      │
                               │ Phase 1              │ Alimenta Spark
                               ▼                      ▼
                        ┌───────────┐          ┌─────────────┐
                        │ Tech Stack │          │ Files Map   │
                        │ Domínio    │          │ Meta-rules  │
                        └───────────┘          └─────────────┘
```

## Descrição
A task `arquitetarContexto()` analisa a estrutura do projeto e define a base técnica (blueprint) para o enriquecimento subsequente. Ela mapeia linguagens, frameworks e infraestrutura para garantir que as regras de contexto sejam precisas e úteis.

### Responsabilidades
1. **Escaneamento Técnico** — Varredura completa para identificação de padrões (.js, .py, .yaml, etc.).
2. **Desenho Multiplataforma** — Define quais arquivos específicos de cada plataforma (ex: `CLAUDE.md`, `ANTIGRAVITY.md`) devem ser criados ou atualizados.
3. **Mapeamento de Regras** — Propõe o escopo semântico do que deve ser otimizado.
