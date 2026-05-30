# Materiais Operacionais — Fluxo Maeve de Construção de Squads

Este pacote inclui todos os materiais necessários para construção de squads no sistema:

## Agentes
- squad-analyzer
- squad-agent-creator
- squad-task-creator
- squad-workflow-creator
- squad-optimizer
- squad-validator
- squad-readme-creator
- squad-orchestrator
- squad-publisher

## Fluxo padrão (9 fases)
1. Análise
2. Criação de agentes
3. Criação de tasks
4. Criação de workflows/manifest/config
5. Otimização
6. Validação
7. README multilíngue
8. Orquestração/deploy
9. Publicação

## Tarefas-chave
- analyzeRequirements()
- createAgents()
- createTasks()
- createWorkflows()
- optimizeSquad()
- validateSquad()
- createMultilingualReadme()
- manageState()
- deploySquad()
- publishSquad()

## CLIs incluídos
- `node scripts/squad-tools.cjs ...`
- `nirvana-squad-tools`
- `nirvana-squad-create`
- `nirvana-squad-init`


## Novos comandos v1.2.0
- `state advance ... --auto-gate=true|false`
- `report final <session> --target=... --marketplace=...`
