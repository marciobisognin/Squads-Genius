# OrbisVisum — Squad de Mapeamento Visual e Solução Multiagente

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


## O que é este squad

O **OrbisVisum** é um squad criado para analisar imagens complexas — como prints, infográficos, carrosséis, telas de sistemas, páginas de documentos, quadros visuais e materiais com muitos elementos — e transformar essas imagens em uma estrutura compreensível, organizada e acionável.

Ele não apenas descreve a imagem. O objetivo é mapear os elementos visuais e textuais, entender a solicitação do usuário e conduzir o problema por uma cadeia de agentes até chegar a uma solução, relatório, blueprint ou artefato final.

## Para que serve

O squad serve para situações em que uma imagem contém informação demais para uma simples descrição. Ele ajuda a:

- identificar todos os elementos visíveis da imagem;
- organizar textos, títulos, categorias, códigos, cores, layouts e relações espaciais;
- separar observação visual de interpretação;
- transformar imagens em diagnóstico, estrutura, taxonomia ou plano de ação;
- encaminhar a solicitação por agentes especializados;
- construir uma resposta final, solução operacional ou material derivado das imagens.

## Estrutura dos agentes

O OrbisVisum opera com 8 agentes principais:

1. **briefing-intake**
   Interpreta a solicitação inicial do usuário, identifica objetivo, contexto, restrições, tipo de entrega esperada e critérios de sucesso.

2. **visual-cartographer**
   Mapeia os elementos visuais das imagens: títulos, blocos, objetos, ícones, cores, hierarquia, composição, páginas, agrupamentos e relações espaciais.

3. **ocr-semantics**
   Extrai textos, siglas, termos, categorias e conceitos presentes na imagem, transformando conteúdo visual em dados estruturados.

4. **problem-framer**
   Converte o mapa visual em uma formulação de problema: o que precisa ser resolvido, construído, explicado, organizado ou validado.

5. **solution-architect**
   Define a arquitetura da solução: sequência de execução, componentes, dependências, formato de saída e critérios de validação.

6. **builder-executor**
   Constrói o entregável final, que pode ser relatório, blueprint, checklist, roteiro, prompt, base de conhecimento, estrutura de squad ou outro artefato solicitado.

7. **quality-sentinel**
   Valida se todos os elementos relevantes foram considerados e se existe rastreabilidade entre imagem, observação, interpretação e solução final.

8. **publication-bridge**
   Organiza a entrega ao usuário, prepara o resumo final, orienta próximos passos e consolida o material para publicação, envio ou reutilização.

## O que o squad entrega no final

Ao final do fluxo, o OrbisVisum entrega um conjunto estruturado de saídas, incluindo:

- inventário das imagens analisadas;
- mapa dos elementos visuais e textuais;
- extração semântica dos conceitos encontrados;
- enquadramento do problema ou objetivo do usuário;
- blueprint da solução;
- artefato final construído conforme a solicitação;
- relatório de validação;
- nota de entrega com síntese e próximos passos.

Na prática, o squad transforma imagens em entendimento, entendimento em decisão e decisão em um entregável utilizável.

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/orbisvisum-elementos-visuais-squad/squad.yaml` e `squads/orbisvisum-elementos-visuais-squad/workflows/orbisvisum-pipeline.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/orbisvisum-elementos-visuais-squad/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/orbisvisum-elementos-visuais-squad/agents/`)
> e conduza o fluxo definido em `squads/orbisvisum-elementos-visuais-squad/`. Siga `squads/orbisvisum-elementos-visuais-squad/workflows/orbisvisum-pipeline.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/orbisvisum-elementos-visuais-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/orbisvisum-elementos-visuais-squad/workflows/orbisvisum-pipeline.yaml. Conduza o fluxo para o briefing: <...>
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
   @squads/orbisvisum-elementos-visuais-squad/squad.yaml @squads/orbisvisum-elementos-visuais-squad/workflows/orbisvisum-pipeline.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/orbisvisum-elementos-visuais-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/orbisvisum-elementos-visuais-squad/squad.yaml #file:squads/orbisvisum-elementos-visuais-squad/workflows/orbisvisum-pipeline.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/orbisvisum-elementos-visuais-squad/squad.yaml @squads/orbisvisum-elementos-visuais-squad/workflows/orbisvisum-pipeline.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/orbisvisum-elementos-visuais-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/orbisvisum-elementos-visuais-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/orbisvisum-elementos-visuais-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/orbisvisum-elementos-visuais-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/orbisvisum-elementos-visuais-squad/squad.yaml` e `squads/orbisvisum-elementos-visuais-squad/workflows/orbisvisum-pipeline.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
