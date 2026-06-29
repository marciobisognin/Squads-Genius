# Farol PCFP Squad — Planilha de Custos e Formação de Preços

> **Do edital à Planilha de Custos e Formação de Preços (XLSX com fórmulas vivas)**, para
> serviços contínuos com **dedicação exclusiva de mão de obra** na Administração Pública
> Federal — com cálculo **determinístico**, memória rastreável por rubrica e validação
> contra a IN 05/2017, a IN 98/2022 e a jurisprudência do TCU.

- **Projeto:** Farol Contratos · **Framework base:** OMNISCIENT v7.0
- **Domínio:** licitações e contratos federais (universidades e institutos federais)
- **Regime:** dual — IN 05/2017 (8.666) + Lei 14.133/2021 (IN 98/2022)
- **Versão:** 1.0.0

## Princípio reitor (anti-alucinação)
Todo número final vem de uma **engine determinística em Python**, nunca do LLM.
O LLM extrai, classifica, mapeia CBO/CCT e redige a memória — **a matemática é código**.

## Agentes (8)
| Agente | Papel |
|---|---|
| `pcfp-orchestrator` | Orquestra o StateGraph, roteamento Cynefin, Turing loop, handoff SACP |
| `pcfp-extractor` | Extrai postos/jornada/adicionais do edital/TR/CCT (campo ausente → null + HITL) |
| `pcfp-classifier` | Mapeia CBO/CCT/regime; **HITL Gate 1** |
| `pcfp-rules-engine` | Resolve o RuleSet (alíquotas, desoneração, tributos, CV/PFG) com fundamento |
| `pcfp-calculator` | **Engine determinística** dos Módulos 1–6 (Python puro) |
| `pcfp-validator` | Checagens + jurisprudência TCU (OK/ALERTA/BLOQUEIO) |
| `pcfp-xlsx-generator` | XLSX com **fórmulas vivas** (fallback CSV) |
| `pcfp-hitl-homologacao` | **Gate final humano** (invariante) |

## Workflows (3)
- `pcfp_full_pipeline` — elaboração nova (edital/resumo → planilha homologada).
- `pcfp_analise_proposta` — análise de exequibilidade de proposta de licitante.
- `pcfp_repactuacao_reajuste` — repactuação (mão de obra) e/ou reajuste (insumos), com diff.

## Scripts determinísticos (Python 3.11+, sem dependências obrigatórias)
A partir de `squads/farol-pcfp-squad/`:

```bash
python3 tests/test_golden_cases.py                                   # 11 casos-ouro
python3 scripts/run_pcfp.py --input examples/sample_input.json --outdir output
python3 scripts/pcfp_rules.py                                        # inspeciona o RuleSet
python3 scripts/xlsx_generator.py --salario 1600 --qtd 10 --meses 12 --saida planilha.xlsx
```

## A ordem de incidência (o que a engine acerta)
- Submódulo **2.2 incide sobre Módulo 1 + Submódulo 2.1** (IN 07/2018).
- A **rescisão (Módulo 3)** recebe a incidência do 2.2.
- **Vale-transporte por custo efetivo** (descontados até 6% do salário) — sem piso arbitrário.
- **Tributos por gross-up** sobre o faturamento; **IRPJ/CSLL não entram** (jurisprudência TCU).

## Gates humanos (invariantes)
1. **HITL Gate 1** — confirmação de CBO/CCT (impacta todo o cálculo).
2. **HITL Homologação** — nenhuma planilha é final sem homologação humana registrada.

## Status de entrega (roadmap do PRD)
- **F1 — Engine + testes-ouro:** ✅ entregue e testado (11/11 verde).
- **F4 — XLSX (fórmulas vivas):** ✅ esqueleto entregue (requer `openpyxl` no destino).
- **F2/F3/F5/F6** (Extractor/Classifier LLM, dual-regime completo, LangGraph, integrações):
  especificados nos agentes/workflows; implementação futura. Ver `docs/arquitetura.md`.

## Limitações
Os percentuais default do `RuleSet` são **ilustrativos** (modelo público, regime não
desonerado) e **devem ser confirmados** contra a CCT vigente, os custos mínimos da
IN 176/2024 e o enquadramento tributário, sob homologação humana. Ver `docs/limitations.md`.
Este squad é apoio e **não substitui** o parecer técnico/jurídico do servidor.

## Documentação
- `docs/operating_manual.md` — como operar.
- `docs/arquitetura.md` — arquitetura e mapeamento PRD → repositório.
- `docs/base_normativa.md` — fontes para o RAG e jurisprudência TCU.
- `docs/limitations.md` — premissas, riscos e mitigações.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
