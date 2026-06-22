# maeve-neurocognitive-intelligence-trainer-squad

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.1.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `maeve-neurocognitive-intelligence-trainer-squad`
**Slug no repositório:** `maeve-neurocognitive-intelligence-trainer-squad`
**Versão:** `1.1.0`
**Número na seleção original:** 3

## Visão geral

Maeve Neurocognitive Intelligence Trainer Squad — v1.1 MicroSprint 10–15

## Para que serve

Conduzir ciclos curtos de treino neurocognitivo e metacognitivo, com diagnóstico de gargalos, plano diário de 10–15 minutos, métricas simples e cautela contra promessas pseudocientíficas.

## Estrutura operacional

- **Agentes:** 7
- **Tasks:** 7
- **Workflows:** 1
- **Scripts:** 1
- **Arquivos totais publicados:** 33

## Agentes

- `agents/cognitive-data-analyst.md` — Cognitive Data Analyst
- `agents/ethics-safety-reviewer.md` — Ethics and Safety Reviewer
- `agents/habit-rewiring-engineer.md` — Habit Rewiring Engineer
- `agents/language-abstraction-coach.md` — Language and Abstraction Coach
- `agents/metacognition-coach.md` — Metacognition Coach
- `agents/neuro-learning-architect.md` — Neuro Learning Architect
- `agents/psychometrics-analyst.md` — Psychometrics Analyst

## Tasks principais

- `tasks/01-intake-cognitive-profile.md` — Coletar perfil cognitivo inicial
- `tasks/02-map-gaps-and-domains.md` — Mapear gaps por domínio
- `tasks/03-design-daily-training-loop.md` — Desenhar microtreino diário de 10 a 15 minutos
- `tasks/04-language-and-abstraction-drills.md` — Criar exercícios de linguagem e abstração
- `tasks/05-habit-deconstruction-reconstruction.md` — Reconstruir hábitos cognitivos
- `tasks/06-metrics-and-psychometrics-plan.md` — Criar plano de métricas
- `tasks/07-weekly-review-and-adaptation.md` — Revisão semanal adaptativa

## Workflows

- `workflows/neurocognitive-training-pipeline.yaml`

## Scripts e automação

- `scripts/run_daily_cognitive_trainer.py`

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
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/maeve-neurocognitive-intelligence-trainer-squad/squad.yaml` e `squads/maeve-neurocognitive-intelligence-trainer-squad/workflows/neurocognitive-training-pipeline.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/maeve-neurocognitive-intelligence-trainer-squad/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/maeve-neurocognitive-intelligence-trainer-squad/agents/`)
> e conduza o fluxo definido em `squads/maeve-neurocognitive-intelligence-trainer-squad/`. Siga `squads/maeve-neurocognitive-intelligence-trainer-squad/workflows/neurocognitive-training-pipeline.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/maeve-neurocognitive-intelligence-trainer-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/maeve-neurocognitive-intelligence-trainer-squad/workflows/neurocognitive-training-pipeline.yaml. Conduza o fluxo para o briefing: <...>
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
   @squads/maeve-neurocognitive-intelligence-trainer-squad/squad.yaml @squads/maeve-neurocognitive-intelligence-trainer-squad/workflows/neurocognitive-training-pipeline.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/maeve-neurocognitive-intelligence-trainer-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/maeve-neurocognitive-intelligence-trainer-squad/squad.yaml #file:squads/maeve-neurocognitive-intelligence-trainer-squad/workflows/neurocognitive-training-pipeline.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/maeve-neurocognitive-intelligence-trainer-squad/squad.yaml @squads/maeve-neurocognitive-intelligence-trainer-squad/workflows/neurocognitive-training-pipeline.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/maeve-neurocognitive-intelligence-trainer-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/maeve-neurocognitive-intelligence-trainer-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/maeve-neurocognitive-intelligence-trainer-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/maeve-neurocognitive-intelligence-trainer-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/maeve-neurocognitive-intelligence-trainer-squad/squad.yaml` e `squads/maeve-neurocognitive-intelligence-trainer-squad/workflows/neurocognitive-training-pipeline.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
