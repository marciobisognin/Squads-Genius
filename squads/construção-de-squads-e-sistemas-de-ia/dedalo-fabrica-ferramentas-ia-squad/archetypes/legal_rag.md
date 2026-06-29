# Arquétipo D — RAG Jurídico (`legal_rag`)

> Família D · Operacional de nicho (jurídico). **Setor regulado: humano no loop obrigatório.**

## Dor canônica
Pesquisa de jurisprudência e redação de peças lenta e repetitiva; risco de erro material.

## Dados necessários
- Jurisprudência, modelos de peças, normas internas, histórico do escritório.

## Agentes sugeridos
- Recuperador (RAG), redator-assistente (LLM-JSON), revisor humano (gate obrigatório).

## Integrações
- Bases jurídicas, editor de texto, controle de versão de peças.

## Esqueleto de MVP
- Busca de jurisprudência + rascunho de peça com citações + revisão humana.

## Riscos
- Alucinação de citação; responsabilidade profissional; LGPD de dados de clientes.

## Gate obrigatório
- NÓMOS exige `human_in_loop_required=true`; saída é apoio, nunca decisão final.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
