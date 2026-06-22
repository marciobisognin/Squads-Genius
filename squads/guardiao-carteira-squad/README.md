<div align="center">

# Guardiao Carteira Squad

**Gestao Inteligente de Investimentos e Criptoativos**

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-blue?style=for-the-badge)
![Versao](https://img.shields.io/badge/Versao-1.0.0-green?style=for-the-badge)
![Licenca](https://img.shields.io/badge/Licenca-MIT-yellow?style=for-the-badge)

</div>

---

## O que e

Squad multi-agente para consolidacao, analise e monitoramento de carteiras de investimento, incluindo acoes, FIIs, criptoativos e renda fixa.

---

## Os 5 Agentes

| Agente | Funcao | Entrada | Saida |
| :--- | :--- | :--- | :--- |
| **Consolidador-Carteira** | Consolidacao de dados de corretoras | Extratos, APIs, CSVs | Carteira unificada |
| **Analista-Risco** | Analise de risco e correlacao | Carteira, dados de mercado | Metricas de risco |
| **Alerta-Rebalanceamento** | Alertas de rebalanceamento | Carteira, alocacao alvo | Alertas e sugestoes |
| **Rastreador-Dividendos** | Rastreamento de dividendos | Carteira, datas | Previsao e historico |
| **Relatorio-Performance** | Relatorio de performance | Dados de performance | Relatorio PDF |

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
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/guardiao-carteira-squad/squad.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/guardiao-carteira-squad/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/guardiao-carteira-squad/agents/`)
> e conduza o fluxo definido em `squads/guardiao-carteira-squad/`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/guardiao-carteira-squad/squad.yaml e assuma a persona do orquestrador do squad.
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
   @squads/guardiao-carteira-squad/squad.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/guardiao-carteira-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/guardiao-carteira-squad/squad.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/guardiao-carteira-squad/squad.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/guardiao-carteira-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/guardiao-carteira-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/guardiao-carteira-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/guardiao-carteira-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/guardiao-carteira-squad/squad.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>


---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
