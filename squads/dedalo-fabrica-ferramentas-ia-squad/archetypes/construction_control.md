# Arquétipo D — Controle de Obras (`construction_control`)

> Família D · Operacional de nicho (construtoras).

## Dor canônica
Prazo, orçamento, clima e material descoordenados; estouros descobertos tarde demais.

## Dados necessários
- Cronograma, orçamento, diário de obra, previsão do tempo, estoque de material.

## Agentes sugeridos
- ETL de cronograma (Python), cruzador clima×prazo (Python), alerta de desvio (regras), relator (LLM-JSON).

## Integrações
- Planilhas/ERP de obra, API de clima, fotos de diário (OCR).

## Esqueleto de MVP
- Painel de prazo×orçamento + alerta de risco climático + previsão de falta de material.

## Riscos
- Dados imprecisos do canteiro; automação sobre processo de medição ruim.

## Gancho de monetização
- SaaS de controle de obra por projeto; módulo de previsão.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
