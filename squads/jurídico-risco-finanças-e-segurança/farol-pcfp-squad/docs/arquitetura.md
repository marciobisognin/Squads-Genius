# Arquitetura (alinhada ao OMNISCIENT v7.0)

## Componentes
- **Orquestração:** LangGraph `StateGraph` com estado tipado `PCFPState`.
- **Roteamento de complexidade:** Cynefin Classifier na entrada (Clear/Complicated/Complex).
- **Handoffs:** SACP — contratos JSON validados por schema entre agentes (rejeita handoff malformado).
- **Gates humanos:** HITL em pontos invariantes (CCT, custos mínimos, CV/PFG, homologação final).
- **Observabilidade:** Langfuse (traces por agente, custo de tokens, latência, taxa de bloqueio).
- **Self-healing:** Turing loop — BLOQUEIO devolve ao Calculator/Rules; `max_iterations` antes de escalar.

## Estado (`PCFPState`) — campos principais
`input`, `cynefin_band`, `extracted_spec`, `classified_spec`, `rule_set`, `calc_result`,
`validation_report`, `xlsx_path`, `hitl_decisions[]`, `iteration_count`, `sacp_log[]`,
`langfuse_trace_id`.

## Mapeamento PRD → repositório
| PRD (agente) | Squad (agente) | Implementação determinística |
|---|---|---|
| Orchestrator | pcfp-orchestrator | (orquestração — LangGraph, futura) |
| Extractor | pcfp-extractor | (LLM + parsing, futura) |
| Classifier | pcfp-classifier | (LLM + RAG, futura) |
| Rules Engine | pcfp-rules-engine | `scripts/pcfp_rules.py` (RuleSet) |
| Calculator | pcfp-calculator | `scripts/pcfp_engine.py` ✅ testado |
| Validator | pcfp-validator | `scripts/pcfp_validator.py` ✅ testado |
| XLSX Generator | pcfp-xlsx-generator | `scripts/xlsx_generator.py` ✅ (fallback CSV) |
| HITL Homologação | pcfp-hitl-homologacao | gate humano (registro de decisão) |

## Roadmap por fases (do PRD)
1. **F1 — Engine + testes-ouro** ✅ entregue (Calculator + Validator + 11 testes).
2. **F2 — Extractor + Classifier** (edital→spec, CBO/CCT, HITL #1).
3. **F3 — Rules Engine dual-regime** (IN05 ⇄ Lei14133/IN98) + variantes CV/PFG.
4. **F4 — XLSX Generator** com fórmulas vivas ✅ esqueleto entregue (requer openpyxl no destino).
5. **F5 — Orquestração LangGraph completa**, Cynefin, Turing loop, Langfuse, HITL final.
6. **F6 — Integração** SIPAC/Notion (Farol Contratos) e múltiplos postos/CCTs.

## Critérios de aceite (v1)
- Reproduz os 3 casos-ouro (limpeza, vigilância, apoio) dentro de tolerância de arredondamento.
- 0 ocorrências de IRPJ/CSLL; incidências do 2.2 corretas em 100% dos testes.
- Toda rubrica cita seu fundamento legal.
- Nenhuma saída "final" sem registro de homologação humana.
