# Validar proveniência e privacidade

## Objetivo
Executar gate final de fonte, corroboração, minimização, hipótese alternativa e justificativa de retenção.

## Entradas
- contexto de laboratório/engagement;
- técnica e ferramentas candidatas;
- registro de disponibilidade;
- limites e regras de engajamento.

## Saídas obrigatórias
- decisão `GATED_HANDOFF`, `PLAN_ONLY` ou `DENY`;
- ambiente real e estado da ferramenta;
- artefato/evidência esperado;
- gêmeo defensivo;
- critério de reteste e parada.

## Gate
Falhar se contexto, banda, autorização, privacidade ou ambiente não forem demonstrados.
