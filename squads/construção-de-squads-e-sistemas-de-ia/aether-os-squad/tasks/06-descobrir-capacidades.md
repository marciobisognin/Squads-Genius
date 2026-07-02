# Task 06 — Descobrir e Indexar Capacidades

**Executor:** registry_indexer (motor determinístico)
**Fase:** Descoberta e Registry (PRD §10, §11)

## Objetivo
Varrer as fontes autorizadas (roots locais, repositórios Git em cache, pacotes
aprovados), interpretar cada `squad.yaml` e converter para o **manifesto
canônico interno** (`aether.squad/v1`), indexando capacidades no Registry.

## Entradas
- Roots configurados de squads (ex.: `squads/` deste repositório).

## Saídas
- `registry.json`: squads com id, versão, capabilities, componentes, estado de
  confiança (`discovered → parsed → validated → trusted | quarantined`),
  integridade (sha256 do manifesto) e timestamp de indexação.

## Passos
1. `python3 scripts/registry_indexer.py discover --root <dir>` — scanner puro,
   **sem executar nenhum script** dos squads descobertos (PRD §10.2).
2. Parsing por adaptador `squad-yaml`; falha de parse ⇒ `quarantined` com
   motivo estruturado.
3. Validação estrutural: referências de agents/tasks/workflows existem.
4. Extração de capacidades e tags para busca; indexação incremental
   (reprocessar somente o que mudou — NFR-03).

## Critérios de aceite
- Nenhum script de squad recém-descoberto foi executado.
- Todo squad indexado tem estado de confiança explícito e hash de manifesto.
- Busca por capability/tag responde a partir do índice local.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
