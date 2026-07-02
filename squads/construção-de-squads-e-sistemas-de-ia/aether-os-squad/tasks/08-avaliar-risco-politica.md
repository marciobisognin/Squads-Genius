# Task 08 — Avaliar Risco e Política

**Executor:** risk_engine (motor) + Policy Engine + THÉMIS (parecer opcional)
**Fase:** Policy gate (PRD §19, §24, §14.2.6)

## Objetivo
Calcular o tier de risco de cada ação por motor determinístico e mapear a
política de aprovação; criar `aether.approval-request/v1` quando exigido.

## Entradas
- Ações do plano (`ActionDescriptor`: fatores de risco) +
  `config/risk_policy.yaml`.

## Saídas
- `aether.risk-assessment/v1` por ação (tier, score Decimal, fatores, regra
  disparada).
- `aether.approval-request/v1` com prazo (`expires_at`), `on_expire`, quórum
  por tier e pacote de contexto (resumo, preview/diff, breakdown de risco,
  estado de orçamento).

## Passos
1. `python3 scripts/risk_engine.py --action <action.json>` — soma ponderada
   (Decimal) + regras de escalonamento rígido (irreversível ⇒ ≥ high;
   pagamento/exclusão/regulatório ⇒ critical; restricted+write ⇒ ≥ high;
   broad creds + open network ⇒ ≥ high).
2. Mapear tier → política (`approval_matrix`): low=auto, medium=supervised,
   high=aprovação antes do efeito, critical=bloqueado por padrão (quórum 2).
3. Caso-limite de governança ⇒ solicitar parecer THÉMIS (não vinculante).
4. Aprovação vencida ⇒ `approval_expired` ⇒ executar `on_expire` declarado.

## Critérios de aceite
- Tier calculado sem nenhuma chamada a modelo.
- Toda aprovação tem prazo, quórum e pacote de contexto — sem fila morta.
- Ação de risco médio+ interrompida em gate quando a política exigir.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
