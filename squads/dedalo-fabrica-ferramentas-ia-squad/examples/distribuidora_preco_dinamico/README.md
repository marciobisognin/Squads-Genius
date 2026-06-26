# Exemplo — Distribuidora · Preço Dinâmico (`distributor_sales`)

> Cenário de demonstração do DÉDALO (Família D/E · nicho + monetização).

## Intake
- **Fonte:** planilhas de vendas/estoque + descrição da operação.
- **Dor:** ruptura e encalhe simultâneos; preço sem governança.
- **output_mode:** `prd_only`.

## Caminho esperado no pipeline
1. KAIRÓS casa com `distributor_sales`; premissas de scoring registradas.
2. Motor Python prioriza (ver `examples/opportunity_map.json`).
3. DÉMIOURGÓS propõe arquitetura local-first; pricing como módulo monetizável.
4. NÓMOS alerta sobre governança de preço dinâmico.

## Como rodar a priorização determinística
```bash
python3 scripts/score_opportunities.py --input examples/opportunity_map.json
```

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
