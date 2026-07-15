# Mapear técnica para detecção

## Objetivo
Para cada técnica estudada, registrar telemetria, controle preventivo, detecção, remediação e reteste; técnicas plan-only não são executadas.

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
