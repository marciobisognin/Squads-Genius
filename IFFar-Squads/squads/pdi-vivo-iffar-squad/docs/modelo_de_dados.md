# Modelo de dados — PDI Vivo IFFar Squad

## Matriz central de metas
Campos (ver `schemas/goal.schema.json`):

`codigo | ciclo | dimensao | objetivo | meta | acao | campus | unidade_responsavel | responsavel_nome | indicador | linha_base | meta_anual | meta_2034 | fonte_dados | evidencia_obrigatoria | periodicidade | status | risco | restricao_principal | acao_corretiva | ultima_atualizacao | proxima_revisao`

### Campos obrigatórios mínimos
`codigo, ciclo, dimensao, meta, indicador, fonte_dados, responsavel_nome, periodicidade, status, risco`

## Vocabulário controlado

### Status
não iniciada · em planejamento · em execução · parcialmente concluída · concluída · atrasada · suspensa · requer decisão · requer repactuação

### Risco
baixo · médio · alto · crítico

### Periodicidade
mensal · trimestral · semestral · anual · bienal · eventual

## Regra determinística de risco (`derive_risk`)
1. Status `suspensa`, `requer decisão` ou `requer repactuação` → **crítico**.
2. Status `atrasada` ou próxima revisão vencida → **alto**.
3. Falta de indicador, fonte ou responsável → **alto**.
4. Status `não iniciada`/`em planejamento` → **médio**.
5. Caso contrário → **baixo**.
6. Mantém-se sempre o **maior** risco entre o derivado e o declarado.

## Schemas relacionados
- `goal.schema.json` — meta operacional.
- `indicator.schema.json` — indicador (fórmula, unidade, fonte, periodicidade).
- `risk.schema.json` — risco (nível, categoria, ação corretiva).
- `evidence.schema.json` — evidência auditável (hash, classificação LGPD).

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
