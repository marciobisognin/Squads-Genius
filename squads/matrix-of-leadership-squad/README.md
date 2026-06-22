# 🔷 Matrix of Leadership Squad

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-premium--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `matrix-of-leadership-squad`
**Versão:** 1.0.0
**Domínio:** Avaliação, desenvolvimento e coaching de liderança executiva
**Licença:** MIT | **Criador:** Marcio Bisognin | **Instagram:** @marciobisognin

---

## Visão Geral

O **Matrix of Leadership Squad** é um sistema multiagente de desenvolvimento de liderança executiva que transforma dados de um líder real — autoavaliação, feedbacks, decisões e desafios — em artefatos de desenvolvimento concretos, executáveis e rastreáveis.

O squad opera como um pipeline integrado de 9 fases com 3 gates de validação humana (HITL), garantindo que nenhum artefato chegue ao líder sem ter sido revisado, validado e aprovado. O resultado final é um conjunto coeso de instrumentos que o líder pode usar imediatamente para crescer, comunicar melhor, decidir com mais clareza e se preparar para o próximo papel.

---

## Artefato de Inspiração

**A Matrix da Liderança** é um cristal sagrado do universo Transformers G1, carregado por Optimus Prime. Ela contém a sabedoria acumulada de todos os líderes Autobots ao longo da história — um repositório vivo de inteligência de liderança que é transmitido de geração em geração.

Este squad é o equivalente digital dessa sabedoria: um sistema que concentra o conhecimento consolidado de décadas de ciência da liderança — Hersey & Blanchard, Greenleaf, Heifetz, Bass, Cynefin, Nonviolent Communication, Radical Candor e Psicologia Positiva — para guiar líderes reais em momentos críticos de sua trajetória.

> *"Until all are one."* — Optimus Prime

---

## Agentes

| Agente | Papel |
|---|---|
| `matrix-orchestrator` | Coordenador central — gerencia o pipeline, aciona gates HITL e consolida artefatos |
| `leadership-archetype-assessor` | Diagnostica o arquétipo de liderança usando SLII, Servant, Adaptativa e Transformacional |
| `feedback-360-synthesizer` | Sintetiza feedbacks de múltiplos stakeholders com análise de padrões e gaps de percepção |
| `decision-intelligence-coach` | Desenvolve a inteligência decisória — Cynefin, OODA, pré-mortem e análise de vieses |
| `executive-presence-director` | Constrói o Playbook de Comunicação, Story Bank e Elevator Pitch executivo |
| `difficult-conversation-simulator` | Conduz role-play de conversas difíceis com feedback estruturado e roteiro para a real |
| `succession-readiness-mapper` | Calcula o Succession Readiness Score e mapeia gaps vs. cargo-alvo |
| `ethical-leadership-guardian` | Audita vieses inconscientes, riscos éticos e liderança inclusiva |

---

## Pipeline de Desenvolvimento

```
INPUT (Perfil do líder)
    │
    ▼
[Fase 1] Intake e Estruturação do Perfil
    │     (matrix-orchestrator)
    ▼
[Fase 2] Diagnóstico de Arquétipo de Liderança
    │     (leadership-archetype-assessor)
    ▼
[Fase 3] Síntese de Feedback 360°
    │     (feedback-360-synthesizer)
    ▼
[GATE 1] ── Validação Humana do Diagnóstico ──► HITL OBRIGATÓRIO
    │
    ▼
[Fase 4] Coaching de Inteligência Decisória
    │     (decision-intelligence-coach)
    ▼
[Fase 5] Desenvolvimento de Presença Executiva
    │     (executive-presence-director)
    ▼
[Fase 6] Simulação de Conversa Difícil
    │     (difficult-conversation-simulator)
    ▼
[Fase 7] Mapeamento de Prontidão para Sucessão
    │     (succession-readiness-mapper)
    ▼
[Fase 8] Revisão Ética e de Liderança Inclusiva
    │     (ethical-leadership-guardian)
    ▼
[GATE 2] ── Aprovação da Revisão Ética ──► HITL OBRIGATÓRIO
    │
    ▼
[Fase 9] Consolidação e Geração do PDI
    │     (matrix-orchestrator)
    ▼
[GATE 3] ── Aprovação do PDI Final ──► HITL OBRIGATÓRIO
    │
    ▼
OUTPUT (Artefatos completos de desenvolvimento)
```

---

## Como Usar

### Uso Mínimo (Diagnóstico Rápido)
Forneça ao `matrix-orchestrator` as informações básicas do líder:

```
Perfil: [Nome], [Cargo], [Nível hierárquico], [Setor], [Tempo na função]
Objetivo: [O que quer desenvolver?]
Desafio atual: [Qual o maior desafio de liderança agora?]
```

O squad iniciará pelo `leadership-archetype-assessor` e produzirá o diagnóstico de arquétipo.

### Uso Completo (Pipeline Integral)
Forneça todos os inputs:

1. **Perfil completo** — cargo, nível, setor, contexto organizacional
2. **Autoavaliação** — como o líder se avalia em competências-chave
3. **Feedbacks 360°** — respostas de pares, liderados e superiores (mín. 5)
4. **Decisões recentes** — 2–3 situações de decisão difícil vivenciadas
5. **Cargo-alvo** — próxima posição de carreira almejada
6. **Conversa difícil pendente** — situação que o líder está evitando enfrentar

### Ativação por Agente Individual
Cada agente pode ser ativado de forma independente:

```
→ Apenas diagnóstico de arquétipo: ativar leadership-archetype-assessor
→ Apenas síntese de 360°: ativar feedback-360-synthesizer
→ Apenas simulação de conversa: ativar difficult-conversation-simulator
→ Apenas score de sucessão: ativar succession-readiness-mapper
```

---

## Outputs Esperados

| Artefato | Descrição |
|---|---|
| **Relatório DNA de Liderança** | Arquétipo, forças, pontos cegos, padrões e mapa de competências |
| **PDI — Plano de Desenvolvimento Individual** | Metas trimestrais, marcos, métricas e responsáveis por 12 meses |
| **Executive Communication Playbook** | Scripts, frameworks narrativos, Story Bank e Elevator Pitch |
| **Succession Readiness Score** | Score 0–100, zona de prontidão, gap analysis e plano de aceleração |
| **Relatório de Síntese 360°** | Padrões, gaps de percepção e citações anônimas por tema |
| **Roteiro de Conversa Difícil** | Preparação, abertura, corpo e fechamento para a conversa real |
| **Relatório de Revisão Ética** | Vieses detectados, alertas de risco e recomendações de liderança inclusiva |

---

## Frameworks de Liderança Utilizados

- **SLII (Hersey & Blanchard):** Liderança Situacional — D1-D4 × S1-S4
- **Servant Leadership (Greenleaf):** 8 dimensões do líder servo
- **Liderança Adaptativa (Heifetz):** trabalho técnico vs. trabalho adaptativo
- **Liderança Transformacional (Bass):** 4 I's — influência, motivação, estimulação, consideração
- **Competing Values Framework (Quinn):** 8 papéis em dois eixos
- **Cynefin (Snowden):** 5 domínios de complexidade e modos decisórios
- **OODA Loop (Boyd):** decisão em ambientes voláteis
- **Radical Candor (Scott):** cuidar + desafiar simultaneamente
- **NVC (Rosenberg):** comunicação não violenta
- **Conversas Cruciais (Patterson et al.):** segurança psicológica e coragem
- **Psychological Safety (Edmondson):** 4 estágios de segurança da equipe
- **Inclusive Leadership (Bourke):** 6 traços do líder inclusivo

---

## Segurança e Ética

- Feedbacks de stakeholders são sempre anonimizados antes de qualquer análise
- Nenhum dado de liderança é publicado sem consentimento explícito
- Situações que configurem assédio ou discriminação são sinalizadas e encaminhadas aos canais formais
- O squad não substitui processos de RH, judiciais ou psicológicos formais

---

## Estrutura de Arquivos

```
matrix-of-leadership-squad/
├── squad.yaml
├── README.md
├── agents/
│   ├── matrix-orchestrator.md
│   ├── leadership-archetype-assessor.md
│   ├── feedback-360-synthesizer.md
│   ├── decision-intelligence-coach.md
│   ├── executive-presence-director.md
│   ├── difficult-conversation-simulator.md
│   ├── succession-readiness-mapper.md
│   └── ethical-leadership-guardian.md
├── workflows/
│   ├── leadership-development-pipeline.yaml
│   └── quality-gates.yaml
└── tasks/
    ├── leadership-assessment.md
    └── executive-coaching.md
```

---

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/matrix-of-leadership-squad/squad.yaml` e `squads/matrix-of-leadership-squad/workflows/leadership-development-pipeline.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `squads/matrix-of-leadership-squad/agents/matrix-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `squads/matrix-of-leadership-squad/agents/matrix-orchestrator.md`
> e conduza o fluxo definido em `squads/matrix-of-leadership-squad/`. Siga `squads/matrix-of-leadership-squad/workflows/leadership-development-pipeline.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/matrix-of-leadership-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/matrix-of-leadership-squad/workflows/leadership-development-pipeline.yaml. Conduza o fluxo para o briefing: <...>
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
   @squads/matrix-of-leadership-squad/squad.yaml @squads/matrix-of-leadership-squad/workflows/leadership-development-pipeline.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/matrix-of-leadership-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/matrix-of-leadership-squad/squad.yaml #file:squads/matrix-of-leadership-squad/workflows/leadership-development-pipeline.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/matrix-of-leadership-squad/squad.yaml @squads/matrix-of-leadership-squad/workflows/leadership-development-pipeline.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/matrix-of-leadership-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/matrix-of-leadership-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/matrix-of-leadership-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/matrix-of-leadership-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/matrix-of-leadership-squad/squad.yaml` e `squads/matrix-of-leadership-squad/workflows/leadership-development-pipeline.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
