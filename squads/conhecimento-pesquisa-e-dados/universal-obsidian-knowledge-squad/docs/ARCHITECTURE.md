# Arquitetura

Três camadas (PRD §1):

1. **Núcleo universal (determinístico)** — `scripts/obsidian_core.py` e scripts
   de indexação, busca, grafo e auditoria. Sem LLM.
2. **Perfil do usuário** — `config/user.config.yaml`: vault, idioma, estilo,
   modo e adaptador. Resolução sem hardcode (CLI > config > env > perguntar).
3. **Adaptador do agente** — `config/adapters/*.yaml`: generic, maeve, hermes.
   Maeve é opcional e isolado.

## Fluxo de dados
notas .md → parsing (frontmatter/tags/headings/wikilinks) → chunking por
heading → SQLite FTS5 + índices JSON → busca lexical → verificação de citação →
(LLM) síntese.

## Determinístico × LLM (controle de custo)
Indexação, busca, backlinks, grafo, duplicatas, auditoria e verificação de
citação são determinísticos. Somente a **síntese textual** e a redação de
justificativas usam LLM (PRD §11).

## Índice local
`.obsidian_knowledge_index/` no vault (ou `runtime.index_dir`). Nunca
versionado. IDs estáveis com `previous_paths` para sobreviver a renames.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
