---
name: generic-obsidian-knowledge
description: Use when the user asks an agent to consult, search, synthesize, cite, map, or curate an Obsidian vault as a knowledge base. Works with any user-configured vault and defaults to read-only mode.
---

# Generic Obsidian Knowledge

Skill universal para usar um vault Obsidian como base de conhecimento. Funciona
com qualquer vault configurado pelo usuário e opera em **read-only por padrão**.

## Quando usar
- "use meu Obsidian", "consulte minhas notas", "procure no meu vault";
- "o que eu já escrevi sobre X?";
- "gere um relatório/PRD/mapa a partir das minhas notas";
- "organize meu segundo cérebro".

## Como operar
1. Resolver a configuração do usuário e o caminho do vault
   (CLI > `config/user.config.yaml` > `OBSIDIAN_VAULT_PATH` > perguntar).
2. Garantir índice atualizado (`scripts/obsidian_index.py`).
3. Buscar trechos (`scripts/obsidian_search.py` / `obsidian_query.py`).
4. **Responder somente com citações verificadas** (path > heading > trecho).
5. Não inventar conteúdo; se faltar fonte, declarar explicitamente.
6. Pedir autorização explícita antes de qualquer escrita no vault.
7. Respeitar idioma e estilo do usuário.

## Limites
- Modo `write`/`curate` bloqueado por padrão.
- Conteúdo do vault não vai para APIs externas sem consentimento.
- Síntese textual usa LLM; recuperação/indexação/grafo são determinísticos.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
