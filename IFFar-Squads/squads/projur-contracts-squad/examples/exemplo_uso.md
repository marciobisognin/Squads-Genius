# Exemplo de uso — PROJUR Contracts Squad

Pipeline completo sobre o lote de exemplo (`examples/lote/`).

```bash
cd IFFar-Squads/squads/projur-contracts-squad

# 1. Ingestão (dedup + manifest)
python scripts/ingest.py --input ./examples/lote --output ./saida

# 2. Extração de texto (+ marcação para OCR quando imagem)
python scripts/extract_text.py --manifest ./saida/manifest.json --output ./saida

# 3. Classificação do tipo de instrumento
python scripts/classify_instrument.py --in ./saida/evidencias/textos --output ./saida

# 4. Metadados + partes (CNPJ/CPF)
python scripts/extract_metadata.py --in ./saida/evidencias/textos --classificacao ./saida/classificacao.json --output ./saida
python scripts/normalize_parties.py --in ./saida/metadados.json --output ./saida

# 5. LGPD (detecção/mascaramento de PII)
python scripts/detect_pii.py --in ./saida/evidencias/textos --output ./saida --redact

# 6. Cláusulas + checklist art. 92
python scripts/extract_clauses.py --in ./saida/evidencias/textos --output ./saida
python scripts/check_essential_clauses.py --clausulas ./saida/clausulas.json --output ./saida

# 7. Vínculos + conformidade + ciclo de vida
python scripts/link_instruments.py --metadados ./saida/metadados.json --output ./saida
python scripts/rules_engine.py --regras ./templates/regras.yaml --metadados ./saida/metadados.json --clausulas-essenciais ./saida/clausulas_essenciais.json --partes ./saida/partes.json --output ./saida
python scripts/vigencia_alertas.py --metadados ./saida/metadados.json --hoje 2026-06-17 --output ./saida
python scripts/value_anomaly.py --metadados ./saida/metadados.json --output ./saida

# 8. Matriz + dicionário + indicadores
python scripts/build_matrix.py --metadados ./saida/metadados.json --partes ./saida/partes.json --alertas ./saida/alertas.json --out ./saida/matriz_contratos.csv
python scripts/build_dictionary.py --clausulas ./saida/clausulas.json --out ./saida/dicionario_clausulas.json
python scripts/compute_indicators.py --metadados ./saida/metadados.json --clausulas-essenciais ./saida/clausulas_essenciais.json --alertas ./saida/alertas.json --out ./saida/indicadores.json

# 9. Relatório + checksums + quality + pacote
python scripts/generate_report.py --indicadores ./saida/indicadores.json --alertas ./saida/alertas.json --validacoes ./saida/validacoes.json --out ./saida/relatorio_executivo.md
python scripts/manifest_checksums.py --input ./saida --out ./saida/checksums.json
python scripts/quality_audit.py --input ./saida --out ./saida/quality_report.json
python scripts/package_zip.py --input ./saida --out ./saida/projur_contracts_squad_pacote.zip

# 10. Avaliação de métricas (gold set)
python scripts/gold_eval.py --gold ./examples/gold/gold.json --textos ./saida/evidencias/textos --classificacao ./saida/classificacao.json --out ./saida/gold_eval.json
```

A pasta `./saida/` não é versionada (gerada em execução).

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
