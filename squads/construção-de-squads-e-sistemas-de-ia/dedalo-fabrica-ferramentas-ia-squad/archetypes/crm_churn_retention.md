# Arquétipo C — CRM / Churn / Retenção (`crm_churn`)

> Família C · Decisão por dados (aplicada a retenção).

## Dor canônica
Clientes saem sem aviso; cobrança e retenção operadas no escuro, sem LTV/coorte.

## Dados necessários
- Base de clientes, pagamentos, uso, tickets, datas de entrada/saída.

## Agentes sugeridos
- ETL (Python), calculador de LTV/churn/coorte (Python puro), alerta de anomalia (regras).

## Integrações
- ERP/CRM, gateway de pagamento, planilhas, banco local.

## Esqueleto de MVP
- Painel de churn + alerta de cliente em risco + coorte de retenção.

## Riscos
- Dados sensíveis (LGPD); métrica enganosa sem definição clara.

## Gancho de monetização
- Módulo de retenção por assinatura; consultoria de dados aplicada.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
