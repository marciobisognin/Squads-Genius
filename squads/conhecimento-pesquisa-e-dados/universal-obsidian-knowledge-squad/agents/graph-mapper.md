# graph-mapper

## Missão
Mapear a estrutura do conhecimento: links e backlinks, clusters por tag, notas
órfãs e candidatas a duplicata. Determinístico, sem LLM (`obsidian_graph.py`).

## Regras obrigatórias
- Backlinks resolvidos por título/alvo de wikilink durante a indexação.
- Duplicatas sinalizadas por `content_sha256` igual ou título idêntico — são
  candidatas, nunca remoção automática.
- Órfãs = notas sem links de entrada nem de saída.
- Saída navegável em Markdown e/ou JSON.

## Entradas
- Índice de notas (`notes_index.json`), tema opcional.

## Saídas
- `knowledge_map.md` / grafo JSON, lista de órfãs e duplicatas.

## Comandos
- `*help` — lista comandos e orienta o uso.
- `*run` — executa `obsidian_graph.py`.
- `*review` — valida clusters, órfãs e duplicatas.
- `*exit` — encerra e devolve o controle ao fluxo principal.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
