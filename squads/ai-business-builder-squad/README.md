# ai-business-builder-squad

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `ai-business-builder-squad`
**Slug no repositório:** `ai-business-builder-squad`
**Versão:** `1.0.0`
**Número na seleção original:** 15

## Visão geral

A comprehensive squad for end-to-end business construction, from ideation to strategic mentorship using open-source AI tools.

## Para que serve

Estruturar negócios baseados em IA, da tese de oportunidade ao desenho de oferta, produto, funil, operação e validação comercial.

## Estrutura operacional

- **Agentes:** 8
- **Tasks:** 6
- **Workflows:** 2
- **Scripts:** 1
- **Arquivos totais publicados:** 34

## Agentes

- `agents/brand-architect.md` — title: Brand Identity & Visual Strategist
- `agents/business-strategist.md` — title: Business Strategy & Ideation Lead
- `agents/content-strategist.md` — title: Content Strategy & Social Media Architect
- `agents/copywriter-ai.md` — title: High-Conversion Copy & Storytelling Specialist
- `agents/funnel-engineer.md` — title: Marketing Funnel Architect
- `agents/market-analyst.md` — title: Market Viability Specialist
- `agents/product-architect.md` — title: Product Design & Conception Specialist
- `agents/strategic-mentor.md` — title: Strategic Business Mentor

## Tasks principais

- `tasks/brand-identity-creation.md` — task: brandIdentityCreation()
- `tasks/ideation-and-validation.md` — task: ideationAndValidation()
- `tasks/marketing-funnel-design.md` — task: marketingFunnelDesign()
- `tasks/product-conception-framework.md` — task: productConceptionFramework()
- `tasks/social-media-automation.md` — task: socialMediaAutomation()
- `tasks/strategic-growth-mentorship.md` — task: strategicGrowthMentorship()

## Workflows

- `workflows/business-launch-pipeline.yaml`
- `workflows/content-to-conversion-flow.yaml`

## Scripts e automação

- `scripts/squad-tools.cjs`

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
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/ai-business-builder-squad/squad.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/ai-business-builder-squad/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/ai-business-builder-squad/agents/`)
> e conduza o fluxo definido em `squads/ai-business-builder-squad/`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/ai-business-builder-squad/squad.yaml e assuma a persona do orquestrador do squad.
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
   @squads/ai-business-builder-squad/squad.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/ai-business-builder-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/ai-business-builder-squad/squad.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/ai-business-builder-squad/squad.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/ai-business-builder-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/ai-business-builder-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/ai-business-builder-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/ai-business-builder-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/ai-business-builder-squad/squad.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
