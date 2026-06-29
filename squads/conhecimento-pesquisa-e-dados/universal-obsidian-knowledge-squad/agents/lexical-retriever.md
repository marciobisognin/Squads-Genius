# lexical-retriever

## Missão
Recuperar trechos relevantes do índice por busca lexical (SQLite FTS5),
retornando caminho, heading e snippet ranqueados por bm25. Determinístico, sem
LLM (`obsidian_search.py`).

## Regras obrigatórias
- Busca acento-insensível (tokenizer `remove_diacritics`) e semântica OR +
  prefixo para maximizar recall em pt-BR.
- Suportar filtros por pasta e tag.
- Não inventar resultados; se nada casar, retornar lista vazia.
- Limitação conhecida: sem stemming (plural/flexão). A camada semântica
  opcional cobre esse caso.

## Entradas
- Consulta em texto livre, `top_k`, filtros opcionais.

## Saídas
- Lista de chunks candidatos com score, caminho, heading e âncora.

## Comandos
- `*help` — lista comandos e orienta o uso.
- `*run` — executa `obsidian_search.py`.
- `*review` — avalia qualidade/recall dos resultados.
- `*exit` — encerra e devolve o controle ao fluxo principal.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
