# Task — Matriz operacional de metas

## Objetivo
Converter dimensões, objetivos, metas e ações do PDI em uma matriz operacional estruturada, validada e com indicadores, fontes, responsáveis e evidências.

## Entradas
- Texto extraído do PDI (saída do workflow A).
- Dicionário de indicadores e fontes institucionais (SUAP, SISTEC, PNP, e-MEC, SIAFI).

## Passos
1. Executar `scripts/build_goal_matrix.py` para gerar a matriz preliminar.
2. Preencher (com revisão humana) indicador, linha de base, meta anual, meta final, fonte, evidência, responsável, periodicidade e prazo.
3. Validar com `scripts/validate_indicator_matrix.py` (campos obrigatórios, vocabulário, duplicidade, lacunas).
4. Sanear achados de severidade alta (sem indicador, sem fonte, sem responsável, sem evidência, prazo vencido).
5. Consolidar a matriz conforme `schemas/goal.schema.json`.

## Saídas
- Matriz operacional de metas (CSV/JSON).
- Dicionário de indicadores (CSV/Markdown).
- Quality report de validação (JSON).

## Regras
- O script nunca preenche indicador, fonte ou responsável automaticamente.
- Toda meta deve ter `fonte_dados` e `evidencia_obrigatoria`.
- Status e risco seguem o vocabulário controlado dos schemas.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
