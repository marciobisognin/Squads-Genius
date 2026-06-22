# Maeve Athena Mimir Matrix

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


## O que é este squad

O **Maeve Athena Mimir Matrix** é um squad premium para transformar ideias, produtos, serviços, cursos ou projetos em uma proposta de valor clara, visual e testável.

Ele foi criado para organizar o raciocínio de inovação em torno de quatro perguntas centrais:

- quem é o cliente ou público real;
- quais tarefas, dores e ganhos esse público possui;
- como a solução proposta cria valor;
- quais evidências precisam ser obtidas antes de avançar.

O nome segue a convenção Maeve de squads:

- **Maeve**: orquestração central do squad;
- **Athena**: estratégia, sabedoria prática e clareza;
- **Mimir**: conhecimento profundo, evidência e investigação;
- **Matrix**: transformação e núcleo de decisão, inspirado no universo Transformers.

## Para que serve

Este squad serve para reduzir achismo na criação de produtos, serviços e projetos. Ele ajuda a transformar uma ideia ainda abstrata em uma estrutura objetiva de proposta de valor, com hipóteses, testes e materiais visuais.

Pode ser usado para:

- criar ou revisar um produto;
- estruturar um serviço público ou privado;
- testar uma ideia de curso, consultoria ou mentoria;
- montar um Value Proposition Canvas;
- preparar uma apresentação para gestores, parceiros ou clientes;
- gerar carrosséis, infográficos e materiais visuais para explicar a proposta;
- decidir se uma ideia deve avançar, pivotar, ser redesenhada ou abandonada.

## Estrutura dos agentes

### 1. Maeve Orchestrator

Coordena o fluxo completo do squad. Recebe a ideia ou material inicial, distribui tarefas entre os agentes e consolida a entrega final.

### 2. Customer Profile Cartographer

Mapeia o perfil do cliente ou público-alvo. Organiza:

- tarefas que o cliente tenta realizar;
- dores que impedem o progresso;
- ganhos que o cliente deseja alcançar;
- evidências necessárias para validar esse perfil.

### 3. Value Map Architect

Constrói o mapa de valor da solução. Define:

- produtos ou serviços oferecidos;
- formas de aliviar dores;
- formas de criar ganhos;
- conexões entre oferta e necessidades do cliente.

### 4. Fit Evidence Analyst

Analisa se existe encaixe real entre o perfil do cliente e o mapa de valor. Classifica evidências, identifica lacunas e aponta onde a proposta ainda depende de validação.

### 5. Experiment Sprint Designer

Cria experimentos rápidos para testar hipóteses críticas. Pode propor entrevistas, landing pages, protótipos, smoke tests, pilotos, testes concierge ou pré-venda.

### 6. Visual Canvas Designer

Transforma a proposta de valor em um canvas visual. Define layout, blocos, hierarquia, paleta, legenda e organização visual da informação.

### 7. Infographic & Carousel Producer

Cria materiais visuais de comunicação, como roteiro de carrossel, infográfico textual, sequência didática e narrativa visual para redes sociais, aula ou apresentação.

### 8. Pitch & Story Visualizer

Cria pitch visual, storyboard e narrativa de apresentação. Ajuda a explicar a proposta de valor de forma curta, clara e convincente.

### 9. Ethical & Financial Reviewer

Revisa riscos éticos, promessas exageradas, fragilidade de evidências, riscos financeiros, viabilidade operacional e custo dos experimentos.

## O que o squad entrega no final

Ao final do fluxo, o squad entrega um pacote completo de análise, validação e comunicação da proposta de valor:

- **customer-profile.md**: perfil do cliente com tarefas, dores, ganhos e evidências necessárias;
- **value-map.md**: mapa de valor da solução, com produtos/serviços, aliviadores de dor e criadores de ganho;
- **fit-matrix.md**: matriz de encaixe entre cliente e proposta;
- **hypothesis-backlog.md**: lista priorizada de hipóteses críticas;
- **experiment-sprint.md**: plano de testes rápidos para validar a proposta;
- **visual-canvas-brief.md**: orientação para criação do canvas visual;
- **carousel-outline.md**: roteiro de carrossel ou infográfico explicativo;
- **pitch-storyboard.md**: estrutura de pitch visual e prompts de imagem;
- **executive-decision-report.md**: relatório final com recomendação de decisão.

Em síntese, o **Maeve Athena Mimir Matrix** transforma uma ideia em uma proposta de valor estruturada, testável e comunicável.

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/maeve-athena-mimir-matrix-squad/squad.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/maeve-athena-mimir-matrix-squad/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/maeve-athena-mimir-matrix-squad/agents/`)
> e conduza o fluxo definido em `squads/maeve-athena-mimir-matrix-squad/`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/maeve-athena-mimir-matrix-squad/squad.yaml e assuma a persona do orquestrador do squad.
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
   @squads/maeve-athena-mimir-matrix-squad/squad.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/maeve-athena-mimir-matrix-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/maeve-athena-mimir-matrix-squad/squad.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/maeve-athena-mimir-matrix-squad/squad.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/maeve-athena-mimir-matrix-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/maeve-athena-mimir-matrix-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/maeve-athena-mimir-matrix-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/maeve-athena-mimir-matrix-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/maeve-athena-mimir-matrix-squad/squad.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
