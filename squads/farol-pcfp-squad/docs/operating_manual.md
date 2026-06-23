# Manual de operação — Farol PCFP Squad

## O que o squad faz
Dado um **edital** (ou um **resumo do objeto**), produz a **Planilha de Custos e Formação
de Preços** completa (XLSX com fórmulas vivas), por posto/categoria, com memória de
cálculo, base normativa por rubrica e relatório de validação contra a IN 05/2017, a
IN 98/2022 e a jurisprudência do TCU.

## Princípio reitor (anti-alucinação)
Todo número final vem da **engine determinística em Python**, nunca do LLM. O LLM
extrai, classifica, mapeia CBO/CCT e redige a memória; **a matemática é código**.

## Pipeline (workflow `pcfp_full_pipeline`)
```
[Input] → Cynefin Classifier → Orchestrator
   → Extractor → Classifier(CBO/CCT/Regime) [HITL #1] → Rules Engine
   → Calculator (engine determinística) → Validator
        ├─ BLOQUEIO → (Turing loop) → Rules/Calculator
        └─ OK → XLSX Generator → HITL Homologação → [Output]
```

## Uso rápido (execução determinística, sem LLM)
A partir de `squads/farol-pcfp-squad/`:

```bash
# 1) Rodar a suíte de casos-ouro
python3 tests/test_golden_cases.py

# 2) Pipeline determinístico ponta a ponta (engine + validador)
python3 scripts/run_pcfp.py --input examples/sample_input.json --outdir output

# 3) Inspecionar o RuleSet default
python3 scripts/pcfp_rules.py

# 4) Gerar a planilha (XLSX com fórmulas vivas; CSV se openpyxl ausente)
python3 scripts/xlsx_generator.py --salario 1600 --qtd 10 --meses 12 --saida planilha.xlsx
```

## Entrada (`PCFPInput`)
Ver `examples/sample_input.json`. Campos principais: `fonte`, `arquivos`,
`resumo_objeto`, `parametros` (regime, municipio_uf, garantia_trabalhista,
data_base_proposta, meses_execucao, desoneracao_folha, piso_cct, custo_minimo_in176).

## Saídas (`PCFPOutput`)
- `planilha.xlsx` (ou `.csv` no fallback) — abas Discriminação, postos, Quadro-Resumo,
  Memória, Base Normativa, com fórmulas vivas.
- `relatorio_validacao.json` + `.md` — checagens OK/ALERTA/BLOQUEIO.
- `memoria_calculo.md` — cada rubrica com valor, fórmula e fundamento.
- `handoff_SACP.json` — rastro dos contratos entre agentes.

## Gates humanos (invariantes)
1. **HITL Gate 1** — confirmação de CBO/CCT (impacta todo o cálculo).
2. **HITL Homologação** — nenhuma planilha é final sem homologação humana registrada.

## Variantes de garantia trabalhista
- **Conta-Depósito Vinculada (CV)** — provisões bloqueadas.
- **Pagamento pelo Fato Gerador (PFG)** — paga-se no fato gerador.
A escolha é justificada por custo-benefício (art. 18, §2º da IN 05).
