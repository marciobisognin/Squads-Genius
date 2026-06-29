# Changelog — Farol Contratos & Licitações IFFar

## 3.1.0 — Download das atas assinadas usadas na planilha

- **Novo grupo de agentes "Atas Assinadas"**: `signed-minutes-download-orchestrator`, `minutes-evidence-fetcher`, `minutes-page-locator` e `minutes-index-builder`.
- **Gate humano ao final do pacote de decisão** (`signed_minutes_offer` no workflow `farol-30-procurement-intelligence`): o squad pergunta se o usuário deseja baixar as atas assinadas com os preços usados na planilha entregue.
- **Novo workflow** `baixar-atas-assinadas.yaml`: oferta → confirmação → manifesto → download → localização de página/valor → índice HTML.
- **Novo script determinístico** `scripts/baixar_atas_assinadas.py`: baixa/organiza as atas em pasta por item, calcula `sha256`, localiza em que página o item e o valor aparecem e gera `index.html` + `index.json` (com referência PNCP para pendências). Extração de PDF via `pypdf`/`pdfminer`, com degradação elegante quando não houver biblioteca ou rede.
- **Testes** `tests/test_baixar_atas_assinadas.py` (offline) e atualização de `smoke_test.py` e `requirements.txt` (`pypdf` opcional).

## 3.0.1 — Correções de auditoria de código

- **CI**: corrigido caminho de `paths` e `working-directory` em `farol-iffar-ci.yml`, que apontava para `IFFar-Squads/farol-contratos-licitacoes-iffar` (sem o segmento `squads/`) e por isso nunca disparava nem encontrava o diretório do squad.
- **`farol_common.num()`**: corrigido bug em que valores decimais sem separador de milhar (ex.: `"1234.56"` vindo de célula em texto ou de API) eram interpretados como formato BR e multiplicados por 100 (`123456.0`). Agora o ponto só é tratado como separador de milhar quando há vírgula decimal junto, ou quando há mais de um ponto na string.
- **`farol_30_contracts.extract_attributes()`**: corrigido falso positivo em que os termos de unidade `"m"` e `"l"` casavam por substring com qualquer palavra que contivesse essas letras (ex.: "plástico" gerava `capacidade: ["l"]`). Os padrões agora usam regex com `\b` e exigem dígito colado à abreviação.
- **Heurística de termo restritivo "marca"** (`analisar_dfd.py` e `farol_30_contracts.py`): adicionada exceção para marca citada apenas como referência de padrão de qualidade, com similar/equivalente admitido — uso expressamente permitido pelo art. 41 da Lei nº 14.133/2021. Também corrigido bug em que a exceção textual era aplicada a qualquer termo restritivo, não só a "marca".
- Adicionados testes de regressão para os quatro itens acima (`tests/test_farol_common.py`, `tests/test_analisar_dfd.py`, `tests/test_farol_30_contracts.py`).

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

## 3.0.0 — Farol Public Procurement Intelligence Platform

- Reposiciona o Farol como plataforma institucional de inteligência para contratações públicas.
- Adiciona 12 contratos YAML de agentes especializados.
- Adiciona workflow institucional com estados, retries, timeouts, gates humanos, evidências e falhas.
- Cria base normativa versionada e schemas de achados, evidências e casos.
- Adiciona motor determinístico Farol 3.0 para contratos, especificações, memória de preços e forecasting baseline.
- Adiciona testes automatizados para os novos contratos e motores.
