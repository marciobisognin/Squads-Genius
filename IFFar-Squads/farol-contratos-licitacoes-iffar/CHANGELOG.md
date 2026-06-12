# Changelog — Farol Contratos & Licitações IFFar

## 1.3.0 — 2026-06-12

### Fundação técnica
- `requirements.txt` / `requirements-dev.txt` com dependências declaradas (`openpyxl`, `pytest`).
- Planilha DFD de exemplo com dados fictícios e problemas plantados (`examples/gerar_dfd_exemplo.py` + `examples/dfd_exemplo.xlsx`).
- Suíte de testes automatizados (`tests/`) cobrindo regras de auditoria, detecção de estrutura e pipeline ponta a ponta offline.
- Smoke test ampliado: além de estrutura e compilação, roda auditoria completa na planilha de exemplo.
- CI no GitHub Actions (`.github/workflows/farol-iffar-ci.yml`).
- Módulo compartilhado `scripts/farol_common.py` eliminando duplicação entre scripts.

### Robustez do parser e da análise
- Perfil de mapeamento de colunas configurável via `--perfil perfil.json` para planilhas fora do formato padrão IFFar.
- Detecção de coluna amarela por heurística RGB (não depende mais de 3 códigos exatos).
- Nova coluna **Valor Total Estimado (R$)** (preço × quantidade multicampi) na planilha auditada, com seção de **valor financeiro sob risco** no relatório e ranking dos itens ALTO/MÉDIO de maior valor.
- Novo achado: divergência entre valor total declarado e calculado (preço × quantidade).
- Datas padrão da pesquisa externa agora são relativas (últimos 24 meses) em vez de fixas no código.

### Qualidade do benchmark Compras.gov
- Coluna **Compras.gov Similaridade Descrição** comparando a descrição do DFD com a descrição amostra externa; comparações com baixa equivalência são marcadas e não geram alerta de preço.
- Retry com backoff exponencial em todas as chamadas HTTP.
- Cache local de respostas da API (`--cache`; usado automaticamente pelo enriquecimento).
- `planilha-precos --tipo servico` para itens CATSER.
- Novo comando `compras_gov.py sugerir-codigo --descricao "..."` que sugere códigos CATMAT ranqueados por similaridade.

### Camada 3 — monitoramento recorrente
- `scripts/historico_farol.py`: registra snapshots por ciclo e compara ciclos, apontando achados recorrentes por item/tipo.
- `scripts/painel_saneamento.py`: fila de saneamento com status por achado (PENDENTE → ... → APROVADO) e painel HTML de acompanhamento.
- `scripts/base_conhecimento.py`: base de descrições saneadas/aprovadas, com busca por código/texto e verificação de planilhas contra a base.
- `scripts/previsao_quantitativos.py`: compara quantitativos do ciclo atual com a referência histórica por item/campus e sinaliza desvios.
- `farol_iffar.py analisar` agora gera a fila/painel de saneamento automaticamente e aceita `--ciclo` para registrar a execução no histórico.

### Outros
- Dashboard de auditoria com gráfico SVG de distribuição de risco e valor sob risco por cartão.
- `.gitignore` no repositório (artefatos Python, `output/`, caches).

## 1.2.0
- Comando unificado `farol_iffar.py analisar` (auditoria + Compras.gov + mapa comparativo + busca PNCP por termo).

## 1.1.0
- Integração com a API de Dados Abertos do Compras.gov.br (`compras_gov.py`, `enriquecer_dfd_compras_gov.py`).

## 1.0.0
- Auditoria de planilha DFD multicampi: descrições, unidades, preços, outliers, relatório executivo, CSV de achados e dashboard HTML.
