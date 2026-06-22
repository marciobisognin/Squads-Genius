# instagram-carrossel-visual-pro

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `instagram-carrossel-visual-pro`
**Slug no repositório:** `instagram-carrossel-visual-pro`
**Versão:** `1.0.0`
**Número na seleção original:** 5

## Visão geral

Squad para criar carrosséis premium de Instagram com PPT e vídeo Manim.

## Para que serve

Produzir carrosséis visuais profissionais com estrutura narrativa, design de slides e apoio de geração/exportação visual para apresentações e redes sociais.

## Estrutura operacional

- **Agentes:** 8
- **Tasks:** 8
- **Workflows:** 2
- **Scripts:** 2
- **Arquivos totais publicados:** 40

## Agentes

- `agents/carousel-copywriter.md` — description: Escreve copy slide a slide para Instagram.
- `agents/carousel-orchestrator.md` — description: Orquestra o pipeline completo do carrossel ao vídeo.
- `agents/carousel-strategist.md` — description: Define objetivo editorial e narrativa do carrossel.
- `agents/instagram-publisher.md` — description: Prepara e publica pacote final no Instagram.
- `agents/manim-video-producer.md` — description: Cria vídeo explicativo em Manim.
- `agents/ppt-producer.md` — description: Monta a versão final em PPT.
- `agents/typography-color-engineer.md` — description: Seleciona tipografia e combinações de cor por tema.
- `agents/visual-director.md` — description: Define direção de arte e composição visual por slide.

## Tasks principais

- `tasks/assemble-publish-package.md` — Task: assemble-publish-package
- `tasks/build-manim-video.md` — Task: build-manim-video
- `tasks/build-ppt-deliverable.md` — Task: build-ppt-deliverable
- `tasks/build-visual-system.md` — Task: build-visual-system
- `tasks/collect-briefing.md` — Task: collect-briefing
- `tasks/design-narrative-arc.md` — Task: design-narrative-arc
- `tasks/produce-slide-assets.md` — Task: produce-slide-assets
- `tasks/write-carousel-copy.md` — Task: write-carousel-copy

## Workflows

- `workflows/carrossel_premium_pipeline.yaml`
- `workflows/rapid_restyle_pipeline.yaml`

## Scripts e automação

- `scripts/build-deliverables.cjs`
- `scripts/validate-package.cjs`

## Como usar

1. Abra o arquivo `squad.yaml` para identificar nome, versão, agentes, tasks e workflows.
2. Leia os arquivos em `agents/` para entender os papéis especializados.
3. Execute as tasks em `tasks/` conforme o fluxo indicado em `workflows/`.
4. Quando houver scripts em `scripts/`, use-os como automações auxiliares; revise dependências antes de executar.
5. Registre saídas, decisões e evidências nos diretórios de documentação ou geração previstos pelo próprio squad.

## Arquivos de referência

- `README.md`
- `squad.yaml`

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
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/instagram-carrossel-visual-pro/squad.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/instagram-carrossel-visual-pro/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/instagram-carrossel-visual-pro/agents/`)
> e conduza o fluxo definido em `squads/instagram-carrossel-visual-pro/`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/instagram-carrossel-visual-pro/squad.yaml e assuma a persona do orquestrador do squad.
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
   @squads/instagram-carrossel-visual-pro/squad.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/instagram-carrossel-visual-pro/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/instagram-carrossel-visual-pro/squad.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/instagram-carrossel-visual-pro/squad.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/instagram-carrossel-visual-pro/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/instagram-carrossel-visual-pro/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/instagram-carrossel-visual-pro/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/instagram-carrossel-visual-pro/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/instagram-carrossel-visual-pro/squad.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
