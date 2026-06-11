# Validation Report — Farol Contratos & Licitações IFFar v1.1.0

## Checks executed

- `scripts/smoke_test.py` returned status OK.
- `scripts/analisar_dfd.py`, `scripts/compras_gov.py` and `scripts/enriquecer_dfd_compras_gov.py` compiled with `py_compile`.
- Demo DFD analysis executed on the provided spreadsheet.
- Compras.gov enrichment executed with `--max-itens 3` as a live API smoke test.
- Output workbook opened successfully with `openpyxl`.
- Enriched columns were confirmed in the workbook.

## Demo summary

Input: `DFD ND 339030.21 - MATERIAIS DE COPA E COZINHA (1).xlsx`

Base DFD audit:

- Items analyzed: 135
- Campi detected: 14
- Findings: 211
- Risk distribution: `ALTO=64`, `MÉDIO=27`, `BAIXO=7`, `OK=37`

Compras.gov live smoke:

- Codes researched: 3
- Items enriched: 3
- Comparable items: 3
- Price alerts: 1

## Validated outputs

- Enriched workbook: `/storage/emulated/0/Download/Material herme/farol-comprasgov-validacao/doc_534d3eaf6437_3 - DFD ND 339030.21 - MATERIAIS DE COPA E COZINHA (1)_AUDITADA_COMPRAS_GOV.xlsx`
- Compras.gov report: `/storage/emulated/0/Download/Material herme/farol-comprasgov-validacao/relatorio_compras_gov.md`
- Technical summary: `/storage/emulated/0/Download/Material herme/farol-comprasgov-validacao/summary_compras_gov.json`

## Confirmed enriched columns

- `Compras.gov Registros`
- `Compras.gov Preço Mínimo`
- `Compras.gov Preço Médio`
- `Compras.gov Preço Mediano`
- `Compras.gov Preço Máximo`
- `Compras.gov Descrição Amostra`
- `Avaliação Preço x Compras.gov`

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
