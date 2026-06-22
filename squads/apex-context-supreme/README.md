# apex-context-supreme

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.1.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


Squad supremo de Context Engineering, Enriquecimento e Otimização de Janela de Contexto. Transforma projetos desorganizados em bases de conhecimento de alta performance para agentes IA, garantindo máxima densidade semântica com o mínimo de tokens.

Totalmente compatível com Claude, Gemini, Codex e Antigravity.

## Instalação

```bash
npx squads add olympus-forge/apex-context-supreme
```

## O que Faz

O **APEX-CONTEXT SUPREME** automatiza a criação de regras de contexto (`CLAUDE.md`, `GEMINI.md`, etc.) através de um pipeline de 4 fases:

- **Arquitetura Técnica**: Escaneamento recursivo e mapeamento de tech stack.
- **Enriquecimento Semântico**: Injeção de sabedoria técnica densa e instruções acionáveis.
- **Escultura de Tokens**: Remoção de redundâncias cross-platform e poda de ruído.
- **Validação de Qualidade**: Compliance com padrões AIOS e integridade de links.

## Pipeline

| Fase | Agente | Papel | Modelo |
|------|--------|-------|--------|
| 1 | 🏛️ Maven | Arquiteta de Blueprint | Sonnet |
| 2 | ✨ Spark | Alquimista de Contexto | Opus |
| 3 | ✂️ Trim | Escultor de Tokens | Sonnet |
| 4 | ⚖️ Vigil | Guardiã da Qualidade | Flash |

## Agentes

| Ícone | Agente | Título | Archetype | Descrição |
|-------|--------|--------|-----------|-----------|
| 🚀 | apex-orquestrista | Context Orchestration Specialist | Flow_Master | Mente central e orquestrador do pipeline |
| 🏛️ | maven-arquiteta | Technical Blueprint Architect | Builder | Escaneia projeto e define blueprint técnico |
| ✨ | spark-alquimista | Context Enrichment Specialist | Builder | Gera regras semânticas densas |
| ✂️ | trim-escultor | Context Window Optimizer | Balancer | Otimiza densidade e remove redundâncias |
| ⚖️ | vigil-validadora | Quality Assurance Specialist | Guardian | Valida integridade e compliance AIOS |

## Tasks

| Task | Responsável | Atomic Layer | Descrição |
|------|-------------|--------------|-----------|
| `arquitetarContexto()` | maven-arquiteta | Molecule | Gera blueprint.yaml e inventory.json |
| `enriquecerContexto()` | spark-alquimista | Organism | Cria arquivos de regras (.md) enriquecidos |
| `otimizarContexto()` | trim-escultor | Molecule | Reduz ruído e otimiza tokens |
| `validarContexto()` | vigil-validadora | Molecule | Executa quality gate e compliance check |

## Workflows

| Workflow | Pattern | Agentes | Descrição |
|----------|---------|---------|-----------|
| `apex_context_pipeline` | Sequential Pipeline | Maven → Spark → Trim → Vigil | Fluxo end-to-end de 4 fases |

## Configuração

- `config/coding-standards.md` — Convenções de naming e docs
- `config/tech-stack.md` — Sw e frameworks suportados
- `config/source-tree.md` — Estrutura organizacional do squad

## Uso

### Comandos Principais

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `*iniciar-pipeline` | Inicia o fluxo completo | `/apex:iniciar-pipeline` |
| `*status-apex` | Mostra saúde do contexto | `/apex:status-apex` |
| `*set-platform` | Define foco de otimização | `/apex:set-platform --name=gemini` |

## Autor

Marcio Bisognin

## Licença

MIT

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/apex-context-supreme/squad.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/apex-context-supreme/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/apex-context-supreme/agents/`)
> e conduza o fluxo definido em `squads/apex-context-supreme/`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/apex-context-supreme/squad.yaml e assuma a persona do orquestrador do squad.
  Conduza o fluxo para o briefing: <...>
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
   @squads/apex-context-supreme/squad.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/apex-context-supreme/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/apex-context-supreme/squad.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/apex-context-supreme/squad.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/apex-context-supreme/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/apex-context-supreme/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/apex-context-supreme/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/apex-context-supreme/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/apex-context-supreme/squad.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>


---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
