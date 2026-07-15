# Mapear comportamento e detecção

## Objetivo
Relacionar comportamento a ATT&CK, telemetria, contenção, regra candidata, falso positivo e teste de regressão.

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
