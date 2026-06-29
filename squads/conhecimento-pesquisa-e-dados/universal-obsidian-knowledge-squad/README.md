# Universal Obsidian Knowledge Squad

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


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

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/universal-obsidian-knowledge-squad/squad.yaml` e `squads/universal-obsidian-knowledge-squad/workflows/setup_user.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `squads/universal-obsidian-knowledge-squad/agents/vault-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `squads/universal-obsidian-knowledge-squad/agents/vault-orchestrator.md`
> e conduza o fluxo definido em `squads/universal-obsidian-knowledge-squad/`. Siga `squads/universal-obsidian-knowledge-squad/workflows/setup_user.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/universal-obsidian-knowledge-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/universal-obsidian-knowledge-squad/workflows/setup_user.yaml. Conduza o fluxo para o briefing: <...>
```
- Use **`@caminho/arquivo`** para dar contexto preciso (autocompleta no prompt).
- Disponível em **CLI, app desktop/web (claude.ai/code) e extensões VS Code / JetBrains**.

</details>

<details>
<summary><b>🟦 Cursor</b></summary>

<br>

1. Abra a pasta do repositório no Cursor.
2. No **Chat / Composer (⌘/Ctrl + I)**, referencie os arquivos com `@`:
   ```text
   @squads/universal-obsidian-knowledge-squad/squad.yaml @squads/universal-obsidian-knowledge-squad/workflows/setup_user.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/universal-obsidian-knowledge-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/universal-obsidian-knowledge-squad/squad.yaml #file:squads/universal-obsidian-knowledge-squad/workflows/setup_user.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/universal-obsidian-knowledge-squad/squad.yaml @squads/universal-obsidian-knowledge-squad/workflows/setup_user.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/universal-obsidian-knowledge-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/universal-obsidian-knowledge-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/universal-obsidian-knowledge-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/universal-obsidian-knowledge-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/universal-obsidian-knowledge-squad/squad.yaml` e `squads/universal-obsidian-knowledge-squad/workflows/setup_user.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
