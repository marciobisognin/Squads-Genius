# Coding Standards — dharma-companion

## Languages
- Primary: Markdown (agentes, tasks, config, READMEs)
- Secondary: YAML (workflows, squad.yaml)

## Naming Conventions
- Agent IDs: kebab-case (`zazen-guide`)
- Agent filenames: kebab-case.md (`zazen-guide.md`)
- Task identifiers: camelCase() (`guideMeditation()`)
- Task filenames: kebab-case.md (`guide-meditation.md`)
- Workflow names: snake_case (`daily_practice_cycle`)
- Workflow filenames: kebab-case.yaml (`daily-practice-cycle.yaml`)
- Command names: *kebab-case (`*guide-meditation`)
- Squad name: kebab-case (`dharma-companion`)
- Variables em código: inglês, camelCase

## Formatting Rules
- Indentação YAML: 2 espaços
- Indentação Markdown: sem requisito (consistente por arquivo)
- Line length: máximo 120 caracteres em YAML
- Strings YAML com caracteres especiais: sempre entre aspas

## Content Language
- Conteúdo textual: PT-BR com acentuação correta (UTF-8)
- Nomes de variáveis e código: inglês (padrão internacional)
- Termos técnicos: manter em inglês (IDs, paths, commands)
- Termos budistas: manter em romanização consagrada (zazen, samadhi, samu, Darma, Sanga)

## Documentation Standards
- Cada agente: YAML config + Quick Commands + Agent Collaboration + Usage Guide
- Cada task: YAML config + Pipeline Diagram
- README: estrutura padronizada

## Tone & Voice
- Tom contemplativo mas acessível — nunca acadêmico demais
- Sem julgamento — observação, não avaliação
- Inclusivo — todas as tradições contemplativas são respeitadas
- Prático — insights devem chegar ao cotidiano
