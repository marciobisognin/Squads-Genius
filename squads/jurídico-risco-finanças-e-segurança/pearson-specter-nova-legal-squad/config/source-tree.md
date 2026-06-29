# Estrutura de Diretórios do Pearson Specter Nova Legal AGI Squad

Esta estrutura apresenta os principais componentes do projeto **Pearson Specter Nova Legal AGI Squad**. Ela segue o padrão de squads multiagente apresentado pelo construtor original, separando perfis de agentes, definições de tarefas, workflows, configurações e documentação.

```
pearson-specter-nova-legal-squad/
├── squad.yaml                   # Manifesto principal do squad
├── agents/                      # Perfis de agentes e suas instruções
│   ├── harvey.md                # Perfil do agente de M&A e litígio estratégico
│   ├── mike.md                  # Perfil do agente constitucional/penal e RAG eidético
│   ├── louis.md                 # Perfil do agente tributário e financeiro
│   ├── jessica.md               # Perfil do agente de antitruste e governança
│   ├── donna.md                 # Perfil do agente de jurimetria e e‑discovery
│   └── legal-orchestrator.md    # Perfil do orquestrador do fluxo
├── tasks/                       # Definições formais de tarefas do pipeline de litígio
│   ├── define-case.md           # Coleta de informações iniciais sobre o caso
│   ├── intake-oracle.md         # Análise de magistrados e background check (Donna)
│   ├── deep-research.md         # Pesquisa de precedentes e doutrina (Mike)
│   ├── financial-audit.md       # Auditoria financeira e tributária (Louis)
│   ├── macro-alignment.md       # Avaliação concorrencial e compliance (Jessica)
│   ├── craft-strategy.md        # Montagem da estratégia final (Harvey)
│   └── compile-case-report.md   # Consolidação do relatório final
├── workflows/                   # Descrição dos fluxos de trabalho do squad
│   └── litigation-pipeline-loop.yaml
├── checklists/                  # Listas de verificação e validação do squad
│   └── legal-squad-checklist.md
├── config/                      # Padrões de codificação, pilha tecnológica e estrutura
│   ├── coding-standards.md
│   ├── tech-stack.md
│   └── source-tree.md
└── README.md                    # Documentação de uso do squad
```

Mantenha esta estrutura ao adicionar novos arquivos ou submódulos. Responsabilidades bem delimitadas facilitam a manutenção, a extensão e a auditoria do sistema legal.