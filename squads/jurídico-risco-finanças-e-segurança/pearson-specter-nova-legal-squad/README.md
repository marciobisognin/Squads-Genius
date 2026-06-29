# pearson-specter-nova-legal-squad

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-Proprietary-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `pearson-specter-nova-legal-squad`
**Slug no repositório:** `pearson-specter-nova-legal-squad`
**Versão:** `1.0.0`
**Número na seleção original:** 14

## Visão geral

Squad legal inteligente para orquestrar pipeline adversarial de argumentação e estratégia jurídica usando LLMs especializados em direito brasileiro e common law.

## Para que serve

Organizar análise jurídica/estratégica inspirada em uma firma de alta performance, com agentes para triagem, argumentação, auditoria e estruturação de peças ou pareceres.

## Estrutura operacional

- **Agentes:** 6
- **Tasks:** 7
- **Workflows:** 1
- **Scripts:** 0
- **Arquivos totais publicados:** 20

## Agentes

- `agents/donna.md` — title: Analista de Jurimetria e Legal Ops
- `agents/harvey.md` — title: Especialista em M&A e Litígio Estratégico
- `agents/jessica.md` — title: Especialista em Governança, Antitruste e Relações Governamentais
- `agents/legal-orchestrator.md` — title: Orquestrador do Pipeline Jurídico
- `agents/louis.md` — title: Especialista Tributário e Financeiro
- `agents/mike.md` — title: Pesquisador Constitucional e Penal

## Tasks principais

- `tasks/compile-case-report.md` — task: compileCaseReport()
- `tasks/craft-strategy.md` — task: craftStrategy()
- `tasks/deep-research.md` — responsavel_type: Agente
- `tasks/define-case.md` — responsavel: "Legal Orchestrator
- `tasks/financial-audit.md` — task: financialAudit()
- `tasks/intake-oracle.md` — responsavel_type: Agente
- `tasks/macro-alignment.md` — task: macroAlignment()

## Workflows

- `workflows/litigation-pipeline-loop.yaml`

## Como usar

1. Abra o arquivo `squad.yaml` para identificar nome, versão, agentes, tasks e workflows.
2. Leia os arquivos em `agents/` para entender os papéis especializados.
3. Execute as tasks em `tasks/` conforme o fluxo indicado em `workflows/`.
4. Quando houver scripts em `scripts/`, use-os como automações auxiliares; revise dependências antes de executar.
5. Registre saídas, decisões e evidências nos diretórios de documentação ou geração previstos pelo próprio squad.

## Arquivos de referência

- `README.md`
- `squad.yaml`
- `config/coding-standards.md`
- `config/source-tree.md`
- `config/tech-stack.md`

## Propriedade intelectual e licença

- Licença padrão adotada para novos squads de Marcio: MIT.
- Criado por: Marcio Bisognin.
- Instagram: [@marciobisognin](https://instagram.com/marciobisognin).
- Observação: squads legados foram publicados preservando sua estrutura original; quando não houver arquivo de licença interno, considere a política do repositório e a documentação de cada pasta.

---

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/pearson-specter-nova-legal-squad/squad.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/pearson-specter-nova-legal-squad/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/pearson-specter-nova-legal-squad/agents/`)
> e conduza o fluxo definido em `squads/pearson-specter-nova-legal-squad/`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/pearson-specter-nova-legal-squad/squad.yaml e assuma a persona do orquestrador do squad.
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
   @squads/pearson-specter-nova-legal-squad/squad.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/pearson-specter-nova-legal-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/pearson-specter-nova-legal-squad/squad.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/pearson-specter-nova-legal-squad/squad.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/pearson-specter-nova-legal-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/pearson-specter-nova-legal-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/pearson-specter-nova-legal-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/pearson-specter-nova-legal-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/pearson-specter-nova-legal-squad/squad.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
