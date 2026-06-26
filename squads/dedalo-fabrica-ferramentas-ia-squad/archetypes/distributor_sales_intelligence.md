# Arquétipo D — Inteligência de Vendas para Distribuidoras (`distributor_sales`)

> Família D · Operacional de nicho (distribuidoras). Inclui ganchos da Família E (micro-SaaS).

## Dor canônica
Estoque, sazonalidade e preço dinâmico geridos no feeling; ruptura e encalhe simultâneos.

## Dados necessários
- Histórico de vendas, estoque, sazonalidade, preços, margem por SKU.

## Agentes sugeridos
- ETL (Python), previsor de demanda (Python/regras), sugestão de preço (Python), relator (LLM-JSON).

## Integrações
- ERP de distribuição, planilhas, banco local; e-mail para alertas.

## Esqueleto de MVP
- Radar de ruptura/encalhe + sugestão de preço por sazonalidade + margem real por SKU.

## Riscos
- Preço dinâmico sem governança; dado de margem incompleto (data_gaps).

## Gancho de monetização
- Módulo de pricing por assinatura; consultoria de sortimento.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
