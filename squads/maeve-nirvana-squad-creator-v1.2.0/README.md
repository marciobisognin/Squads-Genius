# Nirvana Squad Creator

> Versão hardened v1.2.0 (Maeve) com scripts operacionais e consistência de checklist.

> Gera squads AIOS otimizados a partir de linguagem natural — pipeline de 9 fases com análise, geração, otimização, validação, README multi-idioma, deploy e publicação no squads.sh.

## Instalação

```bash
npx squads add gutomec/squads-sh-aios/nirvana-squad-creator
```

## O que Faz

O Nirvana Squad Creator é uma **meta-ferramenta**: um squad AIOS que gera outros squads AIOS. A partir de um objetivo em linguagem natural, ele produz um squad completo e otimizado com:

- **Agentes** com personalidade, archetype e commands (AGENT-PERSONALIZATION-STANDARD-V1)
- **Tasks** com contratos explícitos de Entrada/Saída (TASK-FORMAT-SPECIFICATION-V1)
- **Workflows** com seleção automática de pattern e transitions
- **Config** adaptado ao domínio (coding-standards, tech-stack, source-tree)
- **READMEs** em 6 idiomas (PT-BR, en, zh, hi, es, ar)
- **README visual inteligente** com presets: `parchment-goal-flow` para pedagogia/aprendizado/investigação e `dark-neon-layered-architecture` para negócios/operação/produto/tecnologia
- **Publicação** no marketplace squads.sh

Zero agentes redundantes. Validação em 6 categorias. Deploy automático com habilitação de slash commands.

## Pipeline — 9 Fases

| Fase | Agente | Papel | Modelo |
|------|--------|-------|--------|
| 0 | Orquestrador | Coleta input, inicializa sessão | — |
| 1 | 🔍 Analyzer | Analisa requisitos, gera component-registry | Sonnet |
| 2 | 🏗️ AgentCreator | Gera definições de agents AIOS | Opus |
| 3 | 📋 TaskCreator | Gera tasks com contratos Entrada/Saída | Opus |
| 4 | 🔄 WorkflowCreator | Gera workflows, squad.yaml, config | Opus |
| 5 | ⚡ Optimizer | AgentDropout, cross-references, naming | Opus |
| 6 | ✅ Validator | Validação 6 categorias AIOS | Sonnet |
| 7 | 🌐 ReadmeCreator | READMEs em 6 idiomas | Opus |
| 8 | — Deploy | Deploya em projeto AIOS, habilita commands | Orquestrador |
| 9 | 🚀 Publisher | Publica no squads.sh (opcional) | Orquestrador |

## Agentes

| Icon | Nome | Archetype | Responsabilidade |
|------|------|-----------|------------------|
| 🔍 | Analyzer | Guardian | Decompõe objetivo em domínio, capacidades e roles |
| 🏗️ | AgentCreator | Builder | Gera definições de agentes com persona_profile |
| 📋 | TaskCreator | Builder | Gera tasks com contratos Entrada/Saída encadeados |
| 🔄 | WorkflowCreator | Flow_Master | Gera workflows, squad.yaml, config e README |
| ⚡ | Optimizer | Balancer | Elimina redundâncias, corrige cross-references |
| ✅ | Validator | Guardian | Valida contra 6 categorias de especificação AIOS |
| 🌐 | ReadmeCreator | Builder | Gera READMEs em PT-BR + 5 traduções |
| 🚀 | Publisher | Flow_Master | Guia publicação no squads.sh marketplace |

## Tasks

| Task | Responsável | Atomic Layer |
|------|-------------|-------------|
| `analyzeRequirements()` | Analyzer | Organism |
| `createAgents()` | AgentCreator | Organism |
| `createTasks()` | TaskCreator | Organism |
| `createWorkflows()` | WorkflowCreator | Organism |
| `optimizeSquad()` | Optimizer | Organism |
| `validateSquad()` | Validator | Organism |
| `createMultilingualReadme()` | ReadmeCreator | Organism |
| `deploySquad()` | Orquestrador | Organism |
| `publishSquad()` | Publisher | Molecule |
| `manageState()` | Orquestrador | Molecule |

## Workflows

### squad_generation_pipeline
Pipeline principal de 9 fases — da análise de requisitos à publicação.
```
[Analyzer] → [AgentCreator] → [TaskCreator] → [WorkflowCreator] → [Optimizer] → [Validator] → [ReadmeCreator] → Deploy → [Publisher]
```

### squad_publish_flow
Fluxo standalone para publicar um squad existente no squads.sh.
```
[Validator] → [Publisher]
```

## Configuração

- `config/coding-standards.md` — Naming conventions, regras de formato, linguagem
- `config/tech-stack.md` — Node.js, AIOS Core, Claude Code, YAML/Markdown
- `config/source-tree.md` — Estrutura de diretórios do squad

## Uso

### Pipeline completo
```bash
/SQUADS:nsc:squad-analyzer
```

### Agentes individuais
```
/SQUADS:nsc:squad-analyzer          — Análise de requisitos
/SQUADS:nsc:squad-agent-creator     — Geração de agentes
/SQUADS:nsc:squad-task-creator      — Geração de tasks
/SQUADS:nsc:squad-workflow-creator  — Workflows e squad.yaml
/SQUADS:nsc:squad-optimizer         — Otimização
/SQUADS:nsc:squad-validator         — Validação
/SQUADS:nsc:squad-readme-creator    — READMEs multi-idioma
/SQUADS:nsc:squad-publisher         — Publicação
```

## Autor

**Luiz Gustavo Vieira Rodrigues** ([@gutomec](https://github.com/gutomec))

## Licença

MIT


## CLI v1.3.0 — geração hardened

A versão local v1.3.0 fortalece o comando `nirvana-squad-create` com os recursos sugeridos no diagnóstico:

- `--mode=scaffold|full` — scaffold mínimo ou squad completo validável.
- `--target=aios|maeve` — metadados para o runtime/convenção de destino.
- `--profile=marcio|generic` — aplica autoria padrão. Para `marcio`, novos squads recebem MIT, Marcio Bisognin e @marciobisognin.
- `--output=<dir>` e `--output <dir>` — ambos os formatos são aceitos.
- `--release` — validação bloqueante contra manifesto vazio em modo `full`.
- `--smoke-test` — executa `scripts/smoke-test.cjs` no squad recém-gerado.
- `--force` — sobrescreve destino existente quando explicitamente solicitado.

Exemplo:

```bash
nirvana-squad-create meu-squad \
  --mode=full \
  --target=maeve \
  --profile=marcio \
  --output ~/squad-factory/workspaces \
  --objective="Criar ativos com IA" \
  --release \
  --smoke-test
```

Novos squads completos passam a incluir `LICENSE`, `NOTICE.md`, `AUTHORS.md`, `.ip/ownership.json`, `.ip/response-footer.md`, agentes, tasks, workflow, checklist, templates, referências, script de smoke test e relatório de geração em `validation/generation-report.md`.


## CLI v1.4.0 — Architect Gate premium

A versão local v1.4.0 integra o **Nirvana README Architect** ao workflow de construção de squads. Agora, todo squad criado em `--mode=full` passa automaticamente por um quality gate premium antes da entrega final.

Fluxo integrado:

1. O construtor gera o squad.
2. O `premium-architect-gate.cjs` audita estrutura, manifesto, agentes, tasks, README, licença/autoria e smoke test.
3. Se o score ficar abaixo de 90/100 ou houver lacunas, o gate aplica uma reconstrução corretiva: melhora README, comandos universais, checklist premium e arquivos IP/licença.
4. O gate reavalia o squad.
5. Só passa como premium quando o relatório `validation/premium-architect-report.md` indicar score mínimo 90/100 sem issues bloqueantes.

Comando padrão recomendado:

```bash
nirvana-squad-create nome-do-squad \
  --mode=full \
  --target=maeve \
  --profile=marcio \
  --output ~/squad-factory/workspaces \
  --objective="Objetivo do squad" \
  --release \
  --smoke-test
```

Para testar manualmente um squad já existente:

```bash
node scripts/premium-architect-gate.cjs --squad /caminho/do/squad --rebuild --min-score=90
```

Para desativar excepcionalmente o gate em uma geração full:

```bash
nirvana-squad-create nome --mode=full --no-premium-gate
```

## Convenção Maeve de nomes e textos de publicação

Novos squads para Marcio devem usar nomes de 3 a 4 palavras: `Maeve` + dois elementos da mitologia grega/nórdica +, quando fizer sentido, um elemento narrativo de Marvel, Westworld ou Transformers. Exemplos: `Maeve Athena Mimir Matrix`, `Maeve Hephaestus Brokkr AllSpark`, `Maeve Ariadne Mimir Maze`.

Todo squad finalizado deve incluir `TEXTO_PUBLICACAO_REDES_BLOG.md` com: nome, o que é, o que faz, problema que resolve, exemplos práticos e função de cada agente. Ver `references/maeve-squad-naming-and-publication-policy.md`.
