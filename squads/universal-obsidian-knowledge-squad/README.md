# Universal Obsidian Knowledge Squad

**Squad portátil para transformar qualquer vault Obsidian em uma base de
conhecimento pesquisável, citável, auditável e adaptável ao usuário ou ao
agente que o carregar.**

Modo padrão: **read-only**. Citações verificáveis obrigatórias. Núcleo
determinístico (sem LLM na indexação/busca/grafo); LLM só na síntese.

---

## O que ele faz

- Varre e indexa notas Markdown (frontmatter, tags, headings, links, backlinks).
- Busca lexical via **SQLite FTS5** (acento-insensível, pt-BR friendly).
- Responde com **citações verificadas** (`path > heading > trecho`).
- Mapeia grafo de conhecimento, clusters por tag, órfãs e duplicatas.
- Gera digest, relatórios e exporta contexto citável para outro agente.
- Opera via **agente** (Maeve/Hermes/genérico) ou via **CLI**.

## Portabilidade (sem caminho fixo)

Ordem de resolução do vault: `--vault` (CLI) > `config/user.config.yaml` >
`OBSIDIAN_VAULT_PATH` > busca assistida > pergunta ao usuário.

## Uso rápido (CLI)

```bash
# 1. Criar perfil do usuário (sem hardcode de caminho)
python3 scripts/setup_user_profile.py \
  --vault "/caminho/para/o/vault" --language pt-BR --adapter generic --mode read_only

# 2. Indexar o vault
python3 scripts/obsidian_index.py --config config/user.config.yaml

# 3. Buscar
python3 scripts/obsidian_search.py --config config/user.config.yaml --query "tema" --top-k 20

# 4. Consultar com citações verificadas
python3 scripts/obsidian_query.py --config config/user.config.yaml \
  --query "O que minhas notas dizem sobre isto?" --with-citations

# 5. Mapa de conhecimento
python3 scripts/obsidian_graph.py --config config/user.config.yaml \
  --topic "tema" --output examples/outputs/knowledge_map.md

# 6. Auditoria de qualidade
python3 scripts/obsidian_quality_audit.py --config config/user.config.yaml \
  --output examples/outputs/quality_report.json

# Orquestrador único de workflows
python3 scripts/run_squad.py --workflow ask_vault --config config/user.config.yaml --query "..."
```

## Estrutura

- `agents/` — 11 personas (orquestração, indexação, recuperação, citação,
  síntese, grafo, curadoria, auditoria).
- `tasks/` — 10 tasks atômicas. `workflows/` — 8 workflows.
- `scripts/` — núcleo determinístico (Python 3.11+, stdlib; PyYAML opcional).
- `config/` — `default`, `user.config.example` e `adapters/` (generic/maeve/hermes).
- `skills/` — `generic-obsidian-knowledge` (universal) e `maeve-obsidian-adapter` (opcional).
- `schemas/`, `templates/`, `docs/`, `examples/`, `tests/`.

## Determinístico × LLM

Indexação, busca, backlinks, grafo, duplicatas, auditoria e **verificação de
citação** são determinísticos. Apenas a **síntese textual** usa LLM
(`knowledge-synthesizer`). Ver `docs/ARCHITECTURE.md` e `docs/PRD.md` (§11).

## Segurança

Read-only por padrão; escrita só com autorização. Não indexa segredos. Índice
local, nunca versionado. Conteúdo do vault não vai a APIs externas sem
consentimento. Detalhes em `docs/SECURITY.md`.

## Testes

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

## Adaptador Maeve

Opcional e isolado: `runtime.agent_adapter: "maeve"`. Sem caminhos de
dispositivo embutidos (entrega via `MAEVE_DELIVERY_PATH`). Remover o adaptador
não afeta o núcleo. Ver `docs/ADAPTERS.md`.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
