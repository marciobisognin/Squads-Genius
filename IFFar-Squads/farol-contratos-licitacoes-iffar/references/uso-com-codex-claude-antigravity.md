# Uso do Farol com Codex, Claude Code e Google Antigravity

Este guia descreve como pedir para um agente de codificação operar o squad Farol Contratos & Licitações IFFar com a integração Compras.gov.

## Pré-requisitos

No ambiente do agente, confirme:

```bash
python --version
python -m py_compile scripts/analisar_dfd.py scripts/compras_gov.py scripts/enriquecer_dfd_compras_gov.py
python scripts/smoke_test.py
```

Para ler planilhas `.xlsx`, o ambiente precisa de `openpyxl`.

## Uso direto no terminal

```bash
python scripts/enriquecer_dfd_compras_gov.py "CAMINHO/DFD.xlsx" \
  --inicio 2024-01-01 \
  --fim 2026-12-31 \
  --paginas 2 \
  --out output/farol-compras-gov
```

Para teste rápido:

```bash
python scripts/enriquecer_dfd_compras_gov.py "CAMINHO/DFD.xlsx" \
  --inicio 2026-01-01 \
  --fim 2026-12-31 \
  --paginas 1 \
  --max-itens 5 \
  --out output/teste-compras-gov
```

## Prompt para OpenAI Codex CLI

Use este prompt dentro do repositório/pasta do squad:

```text
Você está no squad Farol Contratos & Licitações IFFar.
Tarefa: executar a auditoria da planilha DFD informada e enriquecer com dados oficiais do Compras.gov.

Regras:
1. Não altere os arquivos originais da planilha.
2. Execute primeiro `python scripts/smoke_test.py`.
3. Execute `python scripts/enriquecer_dfd_compras_gov.py "<CAMINHO_DA_PLANILHA>" --inicio <AAAA-MM-DD> --fim <AAAA-MM-DD> --paginas 2 --out output/farol-compras-gov`.
4. Verifique se foram gerados: planilha enriquecida XLSX, `relatorio_compras_gov.md`, CSV/JSON do Compras.gov e `summary_compras_gov.json`.
5. Leia o relatório e entregue um resumo executivo com: cobertura, itens sem preço externo, alertas de preço e recomendações.
```

## Prompt para Claude Code

```text
Trabalhe como executor do squad Farol Contratos & Licitações IFFar.

Objetivo: analisar a planilha DFD anexada e usar `scripts/enriquecer_dfd_compras_gov.py` para cruzar a auditoria interna com preços praticados no Compras.gov.

Procedimento obrigatório:
- Inspecione README.md, squad.yaml e references/compras-gov-integracao.md.
- Rode `python scripts/smoke_test.py`.
- Rode `python scripts/enriquecer_dfd_compras_gov.py "<CAMINHO_DA_PLANILHA>" --inicio 2024-01-01 --fim 2026-12-31 --paginas 2 --out output/farol-compras-gov`.
- Não invente dados; use apenas os arquivos gerados e a saída real do terminal.
- Ao final, informe os caminhos dos artefatos e uma síntese de decisão para a equipe de licitações.
```

## Prompt para Google Antigravity

```text
Abra a pasta do squad Farol Contratos & Licitações IFFar como workspace.

Missão: executar uma análise de licitações/contratos com integração Compras.gov.

Passos:
1. Leia README.md e references/compras-gov-integracao.md.
2. Use o terminal integrado para rodar `python scripts/smoke_test.py`.
3. Rode a auditoria enriquecida:
   python scripts/enriquecer_dfd_compras_gov.py "<CAMINHO_DA_PLANILHA>" --inicio 2024-01-01 --fim 2026-12-31 --paginas 2 --out output/farol-compras-gov
4. Abra/inspecione `summary_compras_gov.json` e `relatorio_compras_gov.md`.
5. Entregue uma resposta para gestor público com: achados críticos, comparação de preços, itens que exigem pesquisa complementar e próximos passos.
```

## Como interpretar os artefatos

- `*_AUDITADA_COMPRAS_GOV.xlsx`: planilha principal para trabalho da equipe.
- `relatorio_compras_gov.md`: explicação executiva da cobertura externa e alertas.
- `summary_compras_gov.json`: arquivo ideal para agentes automatizados consumirem.
- `resumo_precos_por_codigo.csv`: base simples para Excel/LibreOffice.

## Boa prática institucional

Sempre tratar a mediana Compras.gov como **evidência de apoio**, não como decisão automática. Se a especificação do item ou unidade de fornecimento não for equivalente, a comparação de preços deve ser qualificada ou descartada.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
