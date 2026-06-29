# Dharma Companion

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


> Sistema contemplativo Zen-budista de transformação pessoal — zazen, preceitos éticos, auto-observação e compaixão em ação.

## Instalação

```bash
npx squads add dharma-companion
```

## O que Faz

O Dharma Companion é um **squad de assistência contemplativa** que guia o praticante na implementação de um framework de prática Zen-budista estruturado em 6 eixos:

- **Zazen** — meditação sentada como prática nuclear
- **Preceitos Mahayana** — moldura ética para a vida cotidiana
- **Auto-observação** — identificação de gatilhos emocionais ("botões")
- **Ciclo diário** — 6 passos integrados de prática
- **Caminho contemplativo** — 5 estágios de transformação
- **Compaixão ativa** — conversão de insights em ações concretas

Da inquietação inicial à devolução ao mundo, o squad acompanha cada passo com instrução precisa, reflexão ética e ternura.

## Pipeline — Ciclo Diário de 6 Passos

| Passo | Agente | Ação | Tempo Mín. |
|-------|--------|------|------------|
| 1 | 🧘 ZazenGuide | Assentar-se — sessão de zazen | 5 min |
| 2 | 🧭 PathNavigator | Lembrar-se — impermanência e interdependência | 1 min |
| 3 | ⚖️ PreceptKeeper | Escolher — 1-2 preceitos para o dia | 2 min |
| 4 | 🪞 MirrorObserver | Observar — notar os "botões" ao longo do dia | contínuo |
| 5 | 🔄 PracticeWeaver | Arrepender-se — ritual de arrependimento e recomeço | 1 min |
| 6 | 💚 CompassionCatalyst | Servir — ação concreta de cuidado e ternura | contínuo |

## Agentes

| Icon | Nome | Archetype | Responsabilidade |
|------|------|-----------|------------------|
| 🧘 | ZazenGuide | Guardian | Instrução de zazen: postura, respiração, progressão |
| ⚖️ | PreceptKeeper | Guardian | Aplicação dos 10 Preceitos Mahayana |
| 🪞 | MirrorObserver | Balancer | Auto-observação emocional, mapa de "botões" |
| 🔄 | PracticeWeaver | Flow_Master | Orquestração do ciclo diário de 6 passos |
| 🧭 | PathNavigator | Flow_Master | Navegação nos 5 estágios do caminho |
| 💚 | CompassionCatalyst | Builder | Conversão de insights em ações de compaixão |

## Tasks

| Task | Responsável | Atomic Layer |
|------|-------------|-------------|
| `guideMeditation()` | ZazenGuide | Organism |
| `applyPrecepts()` | PreceptKeeper | Organism |
| `observeEmotions()` | MirrorObserver | Organism |
| `orchestrateDailyCycle()` | PracticeWeaver | Organism |
| `assessStage()` | PathNavigator | Molecule |
| `activateCompassion()` | CompassionCatalyst | Molecule |
| `performRepentance()` | PracticeWeaver | Atom |
| `trackProgress()` | PathNavigator | Molecule |

## Workflows

### daily_practice_cycle
Ciclo diário coordenado pelo PracticeWeaver — da meditação matinal ao serviço vespertino.
```
[ZazenGuide] → [PathNavigator] → [PreceptKeeper] → [MirrorObserver] → [Arrependimento] → [CompassionCatalyst]
```

### contemplative_path_progression
Pipeline de progressão nos 5 estágios contemplativos — da busca inicial à devolução ao mundo.
```
[PathNavigator] → avalia estágio → ajusta profundidade → [Todos os agentes adaptam]
```

## Os 5 Estágios do Caminho

| # | Estágio | Descrição |
|---|---------|-----------|
| 1 | 🌊 Inquietação e Busca | Vazio, perguntas existenciais, busca dispersa |
| 2 | 🌱 Encontro com a Prática | Contato com zazen, primeiros retiros, transformação |
| 3 | 🔥 Ruptura e Dedicação | Compromisso, mudanças de vida, treino intenso |
| 4 | 🏔️ Aprofundamento | Integração prática-vida, "misticismo realista" |
| 5 | 🌍 Devolução ao Mundo | Ensinar, compartilhar, compaixão em larga escala |

## Configuração

- `config/coding-standards.md` — Convenções de código e tom
- `config/tech-stack.md` — Tecnologias e tradição
- `config/source-tree.md` — Estrutura de diretórios

## Uso

### Ciclo diário completo
```
/dc:practice-weaver
*orchestrate-daily-cycle --time-available=30
```

### Agentes individuais
```
/dc:zazen-guide             — Sessão de zazen
/dc:precept-keeper           — Preceitos do dia
/dc:mirror-observer          — Observação emocional
/dc:path-navigator           — Avaliação de estágio
/dc:compassion-catalyst      — Ação compassiva
/dc:practice-weaver          — Ciclo diário completo
```

## Autor

Marcio Bisognin
- [Squads Platform](https://squads.sh/pt)
- [Instagram @marciobisognin](https://www.instagram.com/marciobisognin/)

## Licença

MIT

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/dharma-companion/squad.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/dharma-companion/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/dharma-companion/agents/`)
> e conduza o fluxo definido em `squads/dharma-companion/`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/dharma-companion/squad.yaml e assuma a persona do orquestrador do squad.
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
   @squads/dharma-companion/squad.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/dharma-companion/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/dharma-companion/squad.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/dharma-companion/squad.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/dharma-companion/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/dharma-companion/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/dharma-companion/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/dharma-companion/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/dharma-companion/squad.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>


---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
