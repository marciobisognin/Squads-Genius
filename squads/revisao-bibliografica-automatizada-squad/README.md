<div align="center">

# Revisao Bibliografica Automatizada Squad

**Producao Academica em Larga Escala com IA**

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-blue?style=for-the-badge)
![Versao](https://img.shields.io/badge/Versao-1.0.0-green?style=for-the-badge)
![Licenca](https://img.shields.io/badge/Licenca-MIT-yellow?style=for-the-badge)

</div>

---

## O que e

Squad multi-agente para busca semantica, sintese de artigos, mapeamento de lacunas e formatacao ABNT.

---

## Os 5 Agentes

| Agente | Funcao | Entrada | Saida |
| :--- | :--- | :--- | :--- |
| **Buscador-Semantico** | Busca semantica em bases | Tema | Artigos |
| **Sintetizador-Artigos** | Sintese de artigos | Artigos | Resumos |
| **Mapeador-Lacunas** | Mapeamento de lacunas | Revisao parcial | Mapa de lacunas |
| **Gerador-Revisao** | Geracao de revisao | Sinteses | Revisao |
| **Formatador-Abnt** | Formatacao ABNT | Referencias | Referencias formatadas |

---

## Stack Tecnico

| Camada | Tecnologia |
| :--- | :--- |
| Orquestracao | LangGraph |
| LLM | Claude (Anthropic) |

---

## Licenca

Este projeto esta sob a licenca **MIT**.

**Criado por:** Marcio Bisognin / Maeve  
**Repositorio:** [marciobisognin/Squads-Genius](https://github.com/marciobisognin/Squads-Genius)

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/revisao-bibliografica-automatizada-squad/squad.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/revisao-bibliografica-automatizada-squad/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/revisao-bibliografica-automatizada-squad/agents/`)
> e conduza o fluxo definido em `squads/revisao-bibliografica-automatizada-squad/`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/revisao-bibliografica-automatizada-squad/squad.yaml e assuma a persona do orquestrador do squad.
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
   @squads/revisao-bibliografica-automatizada-squad/squad.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/revisao-bibliografica-automatizada-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/revisao-bibliografica-automatizada-squad/squad.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/revisao-bibliografica-automatizada-squad/squad.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/revisao-bibliografica-automatizada-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/revisao-bibliografica-automatizada-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/revisao-bibliografica-automatizada-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/revisao-bibliografica-automatizada-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/revisao-bibliografica-automatizada-squad/squad.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>


---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
