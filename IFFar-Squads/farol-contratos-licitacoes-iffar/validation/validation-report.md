# Validation Report — Farol Contratos & Licitações IFFar v1.2.0

## Checks executed

- `scripts/smoke_test.py` returned status OK.
- `scripts/analisar_dfd.py`, `scripts/compras_gov.py`, `scripts/enriquecer_dfd_compras_gov.py`, `scripts/farol_iffar.py` and `scripts/pncp_busca_termo.py` compiled with `py_compile`.
- Unified command `scripts/farol_iffar.py analisar` executed on the provided DFD spreadsheet.
- Compras.gov enrichment executed with `--max-itens 3` as a live API smoke test.
- PNCP term search executed with `--termo-pncp "copa cozinha"` as a live API smoke test.
- Output workbook opened successfully in the prior v1.1 validation and v1.2 output file was generated.
- Comparative HTML map was generated.

## Demo command

```bash
python scripts/farol_iffar.py analisar "DFD ND 339030.21 - MATERIAIS DE COPA E COZINHA (1).xlsx" \
  --inicio 2026-01-01 \
  --fim 2026-12-31 \
  --paginas 1 \
  --max-itens 3 \
  --termo-pncp "copa cozinha" \
  --pncp-paginas 1 \
  --out "/storage/emulated/0/Download/Material herme/farol-iffar-camada2-validacao"
```

## Demo summary

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

PNCP term live smoke:

- Term: `copa cozinha`
- Rows consulted: 10
- Matches in the sample page: 0
- Output JSON/CSV generated successfully.

## Validated outputs

- Enriched workbook: `/storage/emulated/0/Download/Material herme/farol-iffar-camada2-validacao/doc_534d3eaf6437_3 - DFD ND 339030.21 - MATERIAIS DE COPA E COZINHA (1)_AUDITADA_COMPRAS_GOV.xlsx`
- Compras.gov report: `/storage/emulated/0/Download/Material herme/farol-iffar-camada2-validacao/relatorio_compras_gov.md`
- Technical summary: `/storage/emulated/0/Download/Material herme/farol-iffar-camada2-validacao/summary_compras_gov.json`
- Comparative map: `/storage/emulated/0/Download/Material herme/farol-iffar-camada2-validacao/mapa_comparativo_compras_gov.html`
- PNCP term output: `/storage/emulated/0/Download/Material herme/farol-iffar-camada2-validacao/03_pncp_termo/pncp_busca_termo.json`

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
