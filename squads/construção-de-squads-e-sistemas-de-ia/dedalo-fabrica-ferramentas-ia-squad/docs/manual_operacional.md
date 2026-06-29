# Manual Operacional — DÉDALO (Fábrica de Ferramentas IA)

## Ativação
- Slash: `/dedalo <vídeo | briefing | dor | processo>`.
- Manual: leia `squad.yaml`, assuma `agents/orchestrator.md` (HEGEMÓN) e siga
  `workflows/full_dedalo_pipeline.yaml` (S0–S14 + Turing transversal).

## Invariante-mestre
O **LLM emite SOMENTE JSON estruturado**. **Todo número — scoring, priorização, métricas —
roda em Python** (`engine/`). Verificável por inspeção de código.

## Fluxo (estados)
`S0 intake → S1 Cynefin (HITL#1) → S2 fontes → S3 oportunidades → S4 scoring (Python) →
S5 processo → S6 conhecimento → S7 dados → S8 PRD → S9 arquitetura → S10 red-team →
S11 QA/LGPD → S12 aprovação MVP (HITL#2) → S13 protótipo → S14 entrega (HITL#3)`.

## Gates HITL
| Gate | Quando | Decisão |
|---|---|---|
| HITL#1 | pós-Cynefin | confirma domínio + escopo de intake |
| HITL#2 | pré-construção | aprova PRD + escopo do MVP |
| HITL#3 | pré-export | homologação final go/no-go |

## Scripts determinísticos
```bash
python3 scripts/extract_sources.py --sources <fonte ...>          # esboço de SourcePackage
python3 scripts/score_opportunities.py --input examples/opportunity_map.json   # ranking (Python puro)
python3 scripts/build_prd.py --input <tool_prd.json> --output output/prd.md     # PRD + matriz
python3 scripts/validate_delivery.py --root output                 # go/no-go de entrega
python3 engine/scoring.py                                          # demo de priorização
```

## Regras de ouro
- Separar observado, inferido, hipótese, recomendação e risco.
- Nenhuma feature/oportunidade órfã (rastreabilidade radical).
- Fonte inacessível: marcar, nunca inventar.
- Saúde/jurídico/financeiro: humano no loop obrigatório.
- Nunca expor segredos/credenciais.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
