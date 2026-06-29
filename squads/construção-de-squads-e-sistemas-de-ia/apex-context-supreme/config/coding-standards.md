# Coding Standards: apex-context-supreme

Este documento define as convenções de código e documentação para o squad de Context Engineering.

## Naming Conventions

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Agent ID | kebab-case | `apex-orchestrator` |
| Agent Filename | kebab-case.md | `apex-orchestrator.md` |
| Task Identifier | camelCase() | `architectContext()` |
| Task Filename | kebab-case.md | `architect-context.md` |
| Workflow Name | snake_case | `apex_main_pipeline` |
| Workflow Filename | kebab-case.yaml | `apex-main-pipeline.yaml` |

## Documentation Standards

- Todos os agentes DEVEM ter um bloco YAML frontmatter completo.
- Todas as tasks DEVEM ter contratos de Entrada/Saída explícitos.
- READMEs devem ser mantidos em 6 idiomas.
- Comentários em YAML devem ser em inglês para portabilidade técnica.
- Documentação de uso deve ser em PT-BR (principal) e EN (secundário).

## AIOS Compliance

- Seguir constituição `.aiox-core/constitution.md`.
- Priorizar `CLI First -> Observability Second -> UI Third`.
- Versão mínima do AIOS Core: `2.1.0`.
