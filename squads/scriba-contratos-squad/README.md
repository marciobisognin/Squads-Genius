# SCRIBA — Geração Assistida de Instrumentos Contratuais

> **Dado um tipo de contrato, produz o instrumento pronto para assinatura**
> (minuta inicial · termo aditivo · apostilamento · repactuação/reajuste) + memória
> explicativa, para a Administração Pública Federal — com motor de cálculo
> **determinístico**, citação obrigatória por cláusula e HITL nos pontos jurídicos
> críticos.

- **Projeto:** IFFar / CLCFW · **Framework base:** OMNISCIENT v7.0
- **Domínio:** contratos administrativos federais (universidades e institutos federais)
- **Regime:** dual — Lei 14.133/2021 + legado IN SEGES/MPDG 05/2017
- **Versão:** 1.0.0

## Princípio reitor (anti-alucinação)
Todo valor monetário ou decisão de instrumento vem do **router/engine determinísticos
em Python**, nunca do LLM. O LLM extrai, redige e explica; **o número e a decisão de
instrumento são código**.

## Agentes (11)
| Agente | Papel |
|---|---|
| `scriba-orchestrator` | Coordena o StateGraph (S0-S11), HITL Gates, Turing loop, handoff SACP |
| `scriba-cynefin-classifier` | Classifica complexidade do caso (Clear/Complicated/Complex/Chaotic) |
| `scriba-extractor` | Normaliza `contract_facts`; resolve pendências |
| `scriba-normative-rag` | Recupera dispositivos aplicáveis (Lei 14.133, IN 05/2017, AGU, TCU) |
| `scriba-instrument-router` | **Tabela-decisão determinística** (§11 do compêndio) |
| `scriba-template-selector` | Seleciona minuta AGU/CNMLC vigente; guarda de vigência |
| `scriba-calculator` | **Engine determinística** (reajuste, aditivo, repactuação, conta vinculada) |
| `scriba-drafter` | Preenche cláusulas com citação obrigatória de fonte |
| `scriba-validator` | Checklist AGU (art. 92) + riscos TCU; adversarial |
| `scriba-doc-generator` | Gera o instrumento final (DOCX/MD) |
| `scriba-explainer` | Gera a memória explicativa (decisões, fundamentos, cálculo) |

## Workflows (4)
- `scriba_full_pipeline` — pipeline completo S0-S11.
- `scriba_termo_aditivo_prorrogacao` — acréscimo/supressão/prorrogação.
- `scriba_apostilamento_reajuste` — apostilamento por reajuste de índice.
- `scriba_repactuacao_demo` — repactuação com demonstração analítica + alerta de preclusão.

## Scripts determinísticos (Python 3.11+, sem dependências obrigatórias)
A partir de `squads/scriba-contratos-squad/`:

```bash
python3 tests/test_golden_cases.py                                                # 21 casos-ouro
python3 scripts/run_scriba.py --input examples/sample_input_reajuste.json --outdir output
python3 scripts/run_scriba.py --input examples/sample_input_aditivo.json --outdir output
python3 scripts/run_scriba.py --input examples/sample_input_repactuacao.json --outdir output
python3 scripts/scriba_router.py                                                  # inspeciona o router
python3 scripts/scriba_engine.py                                                  # inspeciona a engine
```

## O que a engine acerta (PRD §7)
- **Reajuste** — fator = índice_final/índice_inicial sobre o valor base.
- **Limites de aditivo** — 25% (comum) / 50% (reforma de edifício/equipamento),
  **vedada a compensação entre os dois limites** (art. 125, §1º).
- **Repactuação** — anualidade por componente a partir da `data_base_anterior`,
  com **alerta crítico de preclusão** (art. 57, §7º da IN 05/2017).
- **Conta vinculada/PFG** — provisão mensal sobre o salário-base.
- **Prorrogação** — teto de 60 meses.

## Gates humanos (invariantes)
1. **HITL Gate A** — confirmação do instrumento decidido e, se DEMO, da classificação de CCT.
2. **HITL Gate B** — homologação humana final da peça redigida.

## Status de entrega (roadmap do PRD)
- **F1 — Router + Engine + Validator + testes-ouro:** ✅ entregue e testado (21/21 verde).
- **F2/F3/F4/F5/F6** (Extractor/Normative RAG/Template Selector/Drafter/Doc Generator/
  Explainer LLM, orquestração LangGraph completa, integrações PCFP/Farol Contratos):
  especificados nos agentes/tasks/workflows; implementação futura. Ver `docs/arquitetura.md`.

## Limitações
O catálogo de minutas AGU/CNMLC vigentes e a geração de DOCX não estão embarcados
nesta versão — ver `docs/limitations.md`. Este squad é apoio e **não substitui** o
parecer jurídico da procuradoria/CLCFW responsável.

## Documentação
- `docs/operating_manual.md` — como operar.
- `docs/arquitetura.md` — arquitetura e mapeamento PRD → repositório.
- `docs/base_normativa.md` — fontes normativas e jurisprudência TCU.
- `docs/limitations.md` — premissas, riscos e mitigações.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
