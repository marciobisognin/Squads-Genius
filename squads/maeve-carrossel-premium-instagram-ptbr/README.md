# Maeve Carrossel Premium Instagram PT-BR

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.1.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `Maeve Carrossel Premium Instagram PT-BR`
**Slug no repositório:** `maeve-carrossel-premium-instagram-ptbr`
**Versão:** `1.1.0`
**Número na seleção original:** 4

## Visão geral

Squad Nirvana/AIOS para transformar uma solicitação do usuário em carrossel premium para Instagram, com copy em pt-BR, tipografia elegante, elementos infográficos, estrutura visual pixel/ASCII, geração de HTML por slide, conversão para PNG, legenda e hashtags na mesma pasta final, além de vídeo vertical com voz Francisca.

## Para que serve

Criar carrosséis premium em português para Instagram, combinando roteiro didático, direção visual, geração de slides, exportação e preparação de entregáveis.

## Estrutura operacional

- **Agentes:** 6
- **Tasks:** 8
- **Workflows:** 1
- **Scripts:** 3
- **Arquivos totais publicados:** 582

## Agentes

- `agents/briefing-strategist.md` — Briefing Strategist
- `agents/copywriter-ptbr.md` — Copywriter PT-BR
- `agents/html-renderer.md` — HTML Renderer
- `agents/qa-publisher.md` — QA Publisher
- `agents/video-director-francisca.md` — Video Director Francisca
- `agents/visual-director.md` — Visual Director

## Tasks principais

- `tasks/01-interpretar-solicitacao.md` — Interpretar Solicitacao
- `tasks/02-planejar-narrativa.md` — Planejar Narrativa
- `tasks/03-criar-copy-slides.md` — Criar Copy Slides
- `tasks/04-definir-direcao-visual.md` — Definir Direcao Visual
- `tasks/05-gerar-html-e-png.md` — Gerar Html E Png
- `tasks/06-criar-legenda-hashtags.md` — Criar Legenda Hashtags
- `tasks/07-validar-entrega.md` — Validar Entrega
- `tasks/08-criar-video-francisca-manim.md` — Criar Video Francisca Manim

## Workflows

- `workflows/carrossel-premium-pipeline.yaml`

## Scripts e automação

- `scripts/generate_feller_capture_recapture_project.py`
- `scripts/generate_francisca_video.py`
- `scripts/generate_premium_carousel.py`

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
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/maeve-carrossel-premium-instagram-ptbr/squad.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/maeve-carrossel-premium-instagram-ptbr/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/maeve-carrossel-premium-instagram-ptbr/agents/`)
> e conduza o fluxo definido em `squads/maeve-carrossel-premium-instagram-ptbr/`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/maeve-carrossel-premium-instagram-ptbr/squad.yaml e assuma a persona do orquestrador do squad.
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
   @squads/maeve-carrossel-premium-instagram-ptbr/squad.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/maeve-carrossel-premium-instagram-ptbr/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/maeve-carrossel-premium-instagram-ptbr/squad.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/maeve-carrossel-premium-instagram-ptbr/squad.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/maeve-carrossel-premium-instagram-ptbr/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/maeve-carrossel-premium-instagram-ptbr/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/maeve-carrossel-premium-instagram-ptbr/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/maeve-carrossel-premium-instagram-ptbr/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/maeve-carrossel-premium-instagram-ptbr/squad.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
