# Exemplo — Academia · CRM & Retenção (`crm_churn`)

> Cenário de demonstração do DÉDALO (Família C · decisão por dados).

## Intake
- **Fonte:** processo de cobrança/retenção de uma academia.
- **Dor:** alunos somem sem aviso; cobrança e retenção no escuro.
- **output_mode:** `prd_only`.

## Caminho esperado no pipeline
1. HÓROS classifica como **complicado** (arquétipo conhecido, dados internos).
2. KAIRÓS casa com `crm_churn`; premissas de scoring registradas.
3. Motor Python prioriza; LOGISTÉS calcula LTV/churn/coorte (Python puro).
4. TÉLOS escreve PRD com matriz de rastreabilidade.
5. ELENCHUS audita; NÓMOS sinaliza LGPD (dados de pagamento).

## Saídas
- `output/prd.md`, `output/opportunity_map.yaml`, `output/validation_report.md`.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
