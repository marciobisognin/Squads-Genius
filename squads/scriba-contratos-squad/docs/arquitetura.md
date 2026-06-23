# Arquitetura (alinhada ao OMNISCIENT v7.0)

## Componentes
- **Orquestração:** LangGraph `StateGraph` com estado tipado `SCRIBAState` (S0-S11).
- **Roteamento de complexidade:** Cynefin Classifier na entrada (Clear/Complicated/Complex/Chaotic).
- **Handoffs:** SACP — contratos JSON validados por schema entre agentes (rejeita handoff malformado).
- **Gates humanos:** HITL em pontos invariantes — Gate A (instrumento × CCT) e Gate B (homologação final).
- **Self-healing:** Turing loop — BLOQUEIO do Validator devolve ao Calculator/Drafter; `max_iterations` (default 3) antes de escalar ao Gate B.

## Estado (`SCRIBAState`) — campos principais
`input`, `cynefin`, `contract_facts`, `pendencias`, `legal_refs`,
`instrument_decision`, `template_id`, `calc_results`, `draft_clauses`,
`relatorio_validacao`, `hitl_decisions[]`, `iteration_count`, `sacp_log[]`,
`output_paths`.

## Mapeamento PRD → repositório
| PRD (agente) | Squad (agente) | Implementação determinística |
|---|---|---|
| Orchestrator | scriba-orchestrator | (orquestração — LangGraph, futura) |
| Cynefin Classifier | scriba-cynefin-classifier | (LLM heurístico, futuro) |
| Extractor | scriba-extractor | (LLM + parsing, futuro) |
| Normative RAG | scriba-normative-rag | `docs/base_normativa.md` (índice de fontes) |
| Instrument Router | scriba-instrument-router | `scripts/scriba_router.py` ✅ testado |
| Template Selector | scriba-template-selector | (LLM + catálogo de minutas, futuro) |
| Calculator | scriba-calculator | `scripts/scriba_engine.py` ✅ testado |
| Drafter | scriba-drafter | (LLM + template, futuro) |
| Validator | scriba-validator | `scripts/scriba_validator.py` ✅ testado |
| Doc Generator | scriba-doc-generator | (DOCX/MD, futuro) |
| Explainer | scriba-explainer | (LLM + consolidação, futuro) |

## Roadmap por fases (do PRD)
1. **F1 — Router + Engine + Validator + testes-ouro** ✅ entregue (21 testes).
2. **F2 — Extractor + Normative RAG** (normalização de entrada + indexação do compêndio).
3. **F3 — Template Selector** (catálogo de minutas AGU/CNMLC com guarda de vigência).
4. **F4 — Drafter + Doc Generator** (preenchimento de cláusulas + DOCX/MD).
5. **F5 — Orquestração LangGraph completa**, Cynefin, Turing loop, HITL Gates A/B, Explainer.
6. **F6 — Integração** com PCFP Squad (custos de mão de obra) e Farol Contratos.

## Critérios de aceite (v1)
- Reproduz os 3 casos-ouro (reajuste por índice, aditivo de quantitativo, repactuação
  com demonstração analítica) dentro de tolerância de arredondamento.
- Tabela-decisão do Instrument Router (§11 do compêndio) implementada em regras puras.
- Toda cláusula cita seu fundamento legal.
- Alerta crítico de preclusão de repactuação (art. 57, §7º da IN 05/2017) emitido quando aplicável.
- Nenhuma saída "final" sem registro de homologação humana (Gate B).
