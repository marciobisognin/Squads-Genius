# Relatório Demo — Auditoria Visual Premium

## Sumário Executivo
A organização precisa transformar relatórios densos em um material executivo com rastreabilidade de evidência, auditoria de controles, scorecard de compliance e plano de remediação.

## KPIs
- 82% dos achados possuem evidência suficiente.
- 12 controles-chave mapeados.
- 5 riscos materiais priorizados.
- 4 gaps de compliance pendentes.

## Findings
- [HIGH][INFERRED] Backup sem teste formal de restauração nos últimos 12 meses.
- [HIGH][SPECULATED] Ausência de matriz de controles documentada para processo financeiro crítico.
- [MEDIUM][CONFIRMED] Política de privacidade existe, mas não há evidência de revisão recente.
- [MEDIUM][INFERRED] Dependência excessiva de uma pessoa-chave no processo de fechamento.

## Controles
- Financeiro | Pagamento indevido | Dupla aprovação | Extrato e workflow | Parcial.
- TI | Perda de dados | Backup 3-2-1 | Log de restauração | Pendente.
- Compliance | LGPD | Inventário de dados | RoPA | Ausente.
- Estratégia | Foco difuso | Comitê de priorização | Ata mensal | Parcial.

## Compliance
- LGPD — parcial.
- Controles internos — parcial.
- Cyber baseline PME — pendente.
- Governança de IA — não conforme.

## Riscos
- Interrupção operacional por backup não testado.
- Multa ou incidente por privacidade sem inventário de dados.
- Perda de continuidade por bus factor 1.
- Achados sem evidência prejudicam decisão executiva.

## Plano
30 dias: MFA, inventário de dados e backup testado.
60 dias: matriz de controles e owners.
90 dias: scorecard executivo e auditoria de evidências recorrente.
