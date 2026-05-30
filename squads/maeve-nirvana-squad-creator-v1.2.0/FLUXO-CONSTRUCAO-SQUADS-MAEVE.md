# Fluxo Maeve — Construção de Squads no Sistema

Este material organiza **todos os agentes** em um fluxo único, com foco em construção de squads de ponta a ponta.

## Mapa Agente → Tarefa principal

1. **squad-analyzer** → `analyzeRequirements()`  
   Saída: análise de domínio, capacidades, registry de componentes.

2. **squad-agent-creator** → `createAgents()`  
   Saída: agentes AIOS com persona_profile, commands e dependências.

3. **squad-task-creator** → `createTasks()`  
   Saída: tasks com contrato Entrada/Saída e checklists.

4. **squad-workflow-creator** → `createWorkflows()`  
   Saída: workflows YAML, manifest `squad.yaml`, config base.

5. **squad-optimizer** → `optimizeSquad()`  
   Saída: redução de redundância, padronização e correção de cross-references.

6. **squad-validator** → `validateSquad()`  
   Saída: relatório de validação por categorias (blocking/recommended).

7. **squad-readme-creator** → `createMultilingualReadme()`  
   Saída: README principal e versões multilíngues.

8. **squad-orchestrator** → `manageState()` + `deploySquad()`  
   Saída: estado de pipeline, deploy em projeto destino, integração operacional.

9. **squad-publisher** → `publishSquad()`  
   Saída: preparação e publicação no marketplace.

## Pipeline operacional (v1.2.0)

1. Análise
2. Criação de agentes
3. Criação de tasks
4. Criação de workflows/manifest/config
5. Otimização
6. Validação
7. README multilíngue
8. Orquestração/deploy
9. Publicação

## Estado e automação

Ferramenta: `scripts/squad-tools.cjs`

### Comandos-chave
- `init`
- `state advance` (**com gate automático por padrão**)
- `state gate`
- `state add-decision`
- `validate`
- `snapshot`
- `report final` (gera `FINAL-PUBLISH-REPORT.md`)

## Artefatos finais esperados

- Pasta do squad completa (`agents/`, `tasks/`, `workflows/`, `config/`, `checklists/`, `templates/`, `references/`)
- `squad.yaml` consistente
- `README.md` + multilíngues
- `FINAL-PUBLISH-REPORT.md`
- pacote compactado para distribuição (`.tar.bz2` e opcional `.zip`)
