# Pesquisa externa, monitoramento e predição

Estado das extensões planejadas para o squad (atualizado na v1.3.0):

1. **Pesquisa externa de preços** — ✅ implementada. Integração com a API de Dados Abertos do Compras.gov.br (`scripts/compras_gov.py`, `scripts/enriquecer_dfd_compras_gov.py`), com cache local, retry e validação de equivalência de descrição por similaridade.
2. **Séries históricas** — ✅ implementada. `scripts/historico_farol.py` registra snapshots por ciclo e compara ciclos, apontando recorrência de achados por item/tipo. O comando unificado aceita `--ciclo` para registrar automaticamente.
3. **Modelo preditivo simples** — ✅ implementada (primeira versão). `scripts/previsao_quantitativos.py` usa a mediana histórica por item/campus como referência e sinaliza desvios do ciclo atual (≥2x ou ≤0,5x). Evoluções possíveis: ponderar por porte do campus, tendência linear e sazonalidade.
4. **Painel de monitoramento** — ✅ implementada. `scripts/painel_saneamento.py` gera fila de saneamento com status por achado (PENDENTE → EM_ANALISE → CONFIRMADO_CAMPUS → CORRIGIDO → APROVADO/DESCARTADO) e painel HTML com progresso.
5. **Base de conhecimento de itens saneados** — ✅ implementada. `scripts/base_conhecimento.py` mantém descrições aprovadas em JSON, com busca por código/texto e verificação de novas planilhas contra a base.

Próximas evoluções sugeridas:

- Cruzar valor financeiro sob risco com o painel de saneamento para priorização automática da fila.
- Ponderar a previsão de quantitativos por número de matrículas/porte do campus.
- Exportar o histórico para um painel BI institucional (CSV consolidado por ciclo).
