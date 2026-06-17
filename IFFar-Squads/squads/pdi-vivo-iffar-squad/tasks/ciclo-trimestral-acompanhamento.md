# Task — Ciclo trimestral de acompanhamento

## Objetivo
Atualizar status, risco e atraso das metas, identificar metas críticas e produzir relatório executivo, painel e ata de decisão corretiva.

## Entradas
- Matriz operacional consolidada.
- Atualizações mensais/trimestrais de indicadores e status.

## Passos
1. Importar e validar as atualizações.
2. Executar `scripts/risk_matrix.py` para recalcular risco e ações corretivas.
3. Executar `scripts/generate_quarterly_report.py` para o relatório executivo de duas páginas.
4. Executar `scripts/render_dashboard.py` para o painel HTML de status e risco.
5. Registrar ata de decisão corretiva (template `templates/ata_decisao_corretiva.md`).
6. Atualizar histórico e trilha de evidência.

## Saídas
- Matriz de riscos atualizada (CSV/Markdown).
- Relatório executivo trimestral (Markdown).
- Painel HTML.
- Ata de decisão corretiva.

## Regras
- Recalcular de forma determinística (mesma entrada → mesma saída).
- Toda meta crítica precisa de justificativa e ação corretiva.
- Relatório informa limitações e exige revisão humana institucional.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
