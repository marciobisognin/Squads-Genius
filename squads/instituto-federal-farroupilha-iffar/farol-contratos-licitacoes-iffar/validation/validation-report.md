# Validation Report — Farol Contratos & Licitações IFFar v1.3.0

## Checks executados

- `scripts/smoke_test.py` retornou status OK: estrutura de arquivos, `py_compile` de todos os scripts e auditoria offline completa na planilha de exemplo.
- Suíte `pytest tests -q`: **23 testes passando** (regras de auditoria, utilitários compartilhados, detecção de estrutura, pipeline ponta a ponta, saneamento, histórico, base de conhecimento e previsão de quantitativos).
- Comando unificado `scripts/farol_iffar.py analisar` executado ao vivo sobre `examples/dfd_exemplo.xlsx` com `--max-itens 3` e `--ciclo 2026-1` (smoke da API real).
- `scripts/compras_gov.py sugerir-codigo` executado ao vivo: catálogo PDM baixado e cacheado; melhor candidato para "caneta esferográfica azul escrita média" foi o CATMAT 358291 (CANETA ESFEROGRÁFICA, ESCRITA MÉDIA, COR TINTA AZUL).

## Comandos de demonstração

```bash
pip install -r requirements-dev.txt
python scripts/smoke_test.py
python -m pytest tests -q
python examples/gerar_dfd_exemplo.py
python scripts/farol_iffar.py analisar examples/dfd_exemplo.xlsx --paginas 1 --max-itens 3 --ciclo 2026-1 --out output/validacao-v13
```

## Resultados da demonstração (planilha de exemplo, 12 itens fictícios)

Auditoria offline:

- Itens analisados: 12 | Campi detectados: 5
- Achados: 16 | Riscos: `ALTO=3`, `MÉDIO=7`, `BAIXO=0`, `OK=2`
- Tipos: DESCRIÇÃO=7, UNIDADE=5, PREÇO=3 (incl. divergência valor total declarado × calculado), OUTLIER=1
- Valor estimado sob risco: ALTO ≈ R$ 13.119,60; MÉDIO ≈ R$ 12.140,50

Pipeline completo ao vivo (Compras.gov, 3 códigos):

- Itens enriquecidos: 3 | Comparáveis: 2 | Alertas de preço: 0
- Comparações marcadas com baixa equivalência de descrição: 2 (proteção de similaridade funcionando — códigos fictícios não correspondem às descrições externas)
- Cache de respostas da API gravado e reutilizado em `output/.cache`
- Fila de saneamento gerada com 16 achados (status inicial PENDENTE) + painel HTML
- Snapshot do ciclo `2026-1` registrado no histórico com `index.json`

## Outputs validados

- Planilha enriquecida: `output/validacao-v13/dfd_exemplo_AUDITADA_COMPRAS_GOV.xlsx`
- Relatório Compras.gov: `output/validacao-v13/relatorio_compras_gov.md`
- Resumo técnico: `output/validacao-v13/summary_compras_gov.json`
- Mapa comparativo: `output/validacao-v13/mapa_comparativo_compras_gov.html`
- Saneamento: `output/validacao-v13/04_saneamento/saneamento.csv` + `painel_saneamento.html`
- Histórico: `historico/2026-1/summary.json` + `achados_auditoria.csv`

## Limitações conhecidas

- O filtro textual `nomePdm` da API de catálogo não funciona no servidor; o `sugerir-codigo` contorna baixando o catálogo PDM uma única vez para cache local (~41 páginas) e buscando localmente.
- A previsão de quantitativos usa mediana histórica simples; não pondera porte do campus nem sazonalidade.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
