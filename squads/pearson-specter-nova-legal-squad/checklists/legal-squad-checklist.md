# Checklist de Validação do Pearson Specter Nova Legal AGI Squad

Esta checklist ajuda a garantir que todos os componentes do squad jurídico estejam completos e consistentes antes da implantação. O foco é validar que o pipeline de litígio opera sem lacunas e que cada arquivo segue o padrão definido pelo construtor.

## Manifesto e Estrutura
- [ ] `squad.yaml` existe e define corretamente nome, versão, componentes e tags.
- [ ] Todos os agentes listados em `squad.yaml` têm perfis correspondentes na pasta `agents/`.
- [ ] Todas as tarefas referenciadas em `squad.yaml` estão definidas na pasta `tasks/` com entradas, saídas e checklists.
- [ ] O diretório `workflows/` contém o fluxo principal com a sequência de agentes e transições definidas.

## Agentes
- [ ] Cada arquivo de agente contém as seções `agent`, `persona_profile`, `greeting_levels`, `persona`, `commands`, `dependencies`, `Quick Commands`, `Agent Collaboration` e `Usage Guide`.
- [ ] Os `ids` dos agentes são únicos e coincidem com os nomes usados nas tarefas e workflows.
- [ ] As dependências listadas em cada agente apontam para as tarefas corretas.

## Tarefas
- [ ] Cada tarefa especifica `task`, `responsavel`, `responsavel_type` e `atomic_layer`.
- [ ] As entradas e saídas estão claramente definidas, com tipos e descrições detalhadas.
- [ ] O checklist de cada tarefa contém pré e pós‑condições verificáveis.

## Fluxo de Trabalho
- [ ] O arquivo `litigation-pipeline-loop.yaml` define `agent_sequence`, `key_commands`, `success_indicators` e `transitions` coerentes com o pipeline.
- [ ] Cada transição possui um `trigger`, `confidence`, `greeting_message` e `next_steps` que façam sentido na prática.

## Configurações
- [ ] Os arquivos em `config/` estão presentes e atualizados (padrões de codificação, tech stack e estrutura de diretórios).
- [ ] As convenções de codificação são seguidas em todos os arquivos YAML/Markdown (indentação, nomes, etc.).

## Consistência e Ortografia
- [ ] Todos os textos estão em português claro e correto.
- [ ] Não existem campos vazios em arquivos obrigatórios.
- [ ] As tags no manifesto refletem adequadamente o escopo e a finalidade do squad.