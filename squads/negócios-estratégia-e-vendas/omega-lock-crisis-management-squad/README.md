# 🔐 Omega Lock — Crisis Management Squad

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-premium--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


> *"O Omega Lock é o único artefato capaz de restaurar Cybertron — ou destruí-la. Neste squad, representa o poder de reverter o irreversível e reconstruir a partir da catástrofe."*

---

## Visão Geral

O **Omega Lock Crisis Management Squad** é um sistema multiagente de gestão de crises corporativas que cobre o ciclo completo: detecção precoce, classificação, resposta coordenada, continuidade operacional, comunicação multi-stakeholder, interface jurídica, recuperação de reputação e análise pós-mortem.

O squad foi projetado para organizações que precisam responder a crises com velocidade, clareza e controle — sem improvisar. Cada agente é um especialista em seu domínio, orquestrado por um comando central que impõe HITL (humano no loop) obrigatório nas crises de maior severidade.

---

## Artefato de Inspiração

**Omega Lock — Transformers Prime**

O Omega Lock é um dispositivo de poder absoluto capaz de restaurar planetas inteiros ou destruí-los completamente. Aparece como o ponto culminante da série Transformers Prime, representando a decisão mais crítica: usar o poder para construir ou deixar que seja usado para destruir.

No contexto deste squad, o Omega Lock simboliza:
- **O poder de reverter o irreversível**: restaurar reputação, operações e confiança após uma crise
- **A responsabilidade do poder**: decisões durante crises têm consequências que não podem ser desfeitas sem custo
- **A importância do humano no loop**: o Omega Lock jamais deveria ser usado sem deliberação — assim como decisões críticas de crise

---

## Agentes

| Agente | Papel | HITL |
|--------|-------|------|
| `omega-lock-orchestrator` | Coordenador central — ativa, monitora e consolida | Sim (nível 3+) |
| `crisis-early-warning-sentinel` | Detecta sinais precoces de crise em 5 domínios | Não |
| `crisis-classifier` | Tipifica e atribui nível de severidade (1-5) | Sim (nível 3+) |
| `stakeholder-comm-architect` | Arquiteta comunicação diferenciada por stakeholder | Sim (externos) |
| `media-response-strategist` | Estratégia de mídia e coaching de porta-voz | Sim |
| `legal-risk-interface` | Revisa comunicados e mapeia riscos jurídicos | Sim |
| `operational-continuity-planner` | BCP e rotas alternativas de operação | Não |
| `reputation-recovery-designer` | Estratégia de recuperação reputacional pós-crise | Não |
| `post-mortem-analyst` | Causa-raiz e lições aprendidas (5 Porquês, Fishbone) | Sim |

---

## Escala de Severidade

| Nível | Nome | HITL | Perfil |
|-------|------|------|--------|
| 1 | Incidente Isolado | Não | Impacto interno, reversível, sem visibilidade externa |
| 2 | Alerta Elevado | Não | Potencial de escalada, stakeholders internos afetados |
| 3 | Crise Declarada | **Obrigatório** | Impacto externo confirmado, reputação em risco |
| 4 | Crise Grave | **Obrigatório** | Cobertura midiática, múltiplos stakeholders, impacto financeiro |
| 5 | Crise Existencial | **Obrigatório** | Risco de insolvência, ação penal ou colapso reputacional |

---

## Pipeline Principal

```
[Sinal de Crise]
      ↓
[crisis-early-warning-sentinel] → Boletim de Alerta
      ↓
[crisis-classifier] → Nível 1-2 (automático) | Nível 3-5 (HITL)
      ↓
[omega-lock-orchestrator] → Abertura do Ciclo + Decision Log
      ↓
┌─────────────────────────────────────────────────┐
│  PARALELO — Quatro Frentes Simultâneas          │
│  ├── stakeholder-comm-architect (Kit de Comms)  │
│  ├── legal-risk-interface (Riscos Jurídicos)    │
│  ├── operational-continuity-planner (BCP)       │
│  └── media-response-strategist (Mídia + PR)     │
└─────────────────────────────────────────────────┘
      ↓
[legal-risk-interface] → Revisão de Comunicados (HITL)
      ↓
[omega-lock-orchestrator] → Crisis Response Playbook (HITL)
      ↓
[crisis-early-warning-sentinel] → Monitoramento de Contenção
      ↓
[reputation-recovery-designer] → Recuperação Reputacional
      ↓
[post-mortem-analyst] → Pós-Mortem + Plano de Ação (HITL)
      ↓
[omega-lock-orchestrator] → Encerramento do Ciclo
```

---

## Como Usar

### Ativação em Modo de Crise

```
1. Descreva o evento ou sinal detectado:
   "Detectei o seguinte sinal de crise: [descrição]. 
    Contexto organizacional: [setor, porte, stakeholders].
    Acionar pipeline do Omega Lock."

2. O orchestrator assumirá o controle, ativará os agentes e solicitará 
   validação humana quando necessário.
```

### Ativação de Agente Específico

```
# Apenas classificar uma situação:
[crisis-classifier]: Classifique a seguinte situação: [briefing]

# Apenas criar o kit de comunicação:
[stakeholder-comm-architect]: Crie o kit de comunicação para a seguinte crise: [briefing]

# Apenas revisar um comunicado:
[legal-risk-interface]: Revise o seguinte comunicado antes de publicação: [texto]

# Apenas conduzir o pós-mortem:
[post-mortem-analyst]: Conduza o pós-mortem da seguinte crise: [documentação]
```

### Comandos Globais

- `*status`: exibe o estado atual do pipeline de crise
- `*escalate`: força escalada de nível e aciona HITL imediato
- `*compile-playbook`: consolida todos os outputs em um documento único
- `*help`: lista todos os comandos disponíveis

---

## Outputs Esperados

| Entregável | Descrição | Agente Responsável |
|-----------|-----------|-------------------|
| Crisis Response Playbook | Documento mestre com toda a estratégia de resposta | omega-lock-orchestrator |
| Kit de Comunicação Multi-Stakeholder | Mensagens por grupo (conselho, mídia, clientes, reguladores, colaboradores) | stakeholder-comm-architect |
| Statement Inicial + Key Messages | Primeira declaração pública + mensagens centrais | media-response-strategist |
| Mapa de Riscos Jurídicos | Exposições por área do direito + obrigações legais | legal-risk-interface |
| BCP — Plano de Continuidade | Processos críticos, RTO/RPO, rotas alternativas | operational-continuity-planner |
| Roadmap de Recuperação Reputacional | Estratégia pós-contenção em 4 fases (12 meses) | reputation-recovery-designer |
| Relatório de Pós-Mortem | Causa-raiz, lições aprendidas, plano de ação preventiva | post-mortem-analyst |

---

## Regras de Ouro

1. **Nenhum comunicado externo sem revisão jurídica** — sem exceções
2. **HITL obrigatório em Nível 3+** — o orchestrator bloqueia o pipeline até aprovação humana
3. **Fatos, não especulações** — só declare o que é comprovável
4. **Velocidade com precisão** — responder rápido é vital, mas informação incorreta agrava a crise
5. **Documentar tudo** — cada decisão deve ter justificativa, responsável e timestamp

---

## Estrutura de Arquivos

```
omega-lock-crisis-management-squad/
├── squad.yaml
├── README.md
├── agents/
│   ├── omega-lock-orchestrator.md
│   ├── crisis-early-warning-sentinel.md
│   ├── crisis-classifier.md
│   ├── stakeholder-comm-architect.md
│   ├── media-response-strategist.md
│   ├── legal-risk-interface.md
│   ├── operational-continuity-planner.md
│   ├── reputation-recovery-designer.md
│   └── post-mortem-analyst.md
├── workflows/
│   ├── crisis-management-pipeline.yaml
│   └── quality-gates.yaml
└── tasks/
    ├── crisis-response.md
    └── business-continuity.md
```

---

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/omega-lock-crisis-management-squad/squad.yaml` e `squads/omega-lock-crisis-management-squad/workflows/crisis-management-pipeline.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `squads/omega-lock-crisis-management-squad/agents/omega-lock-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `squads/omega-lock-crisis-management-squad/agents/omega-lock-orchestrator.md`
> e conduza o fluxo definido em `squads/omega-lock-crisis-management-squad/`. Siga `squads/omega-lock-crisis-management-squad/workflows/crisis-management-pipeline.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/omega-lock-crisis-management-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/omega-lock-crisis-management-squad/workflows/crisis-management-pipeline.yaml. Conduza o fluxo para o briefing: <...>
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
   @squads/omega-lock-crisis-management-squad/squad.yaml @squads/omega-lock-crisis-management-squad/workflows/crisis-management-pipeline.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/omega-lock-crisis-management-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/omega-lock-crisis-management-squad/squad.yaml #file:squads/omega-lock-crisis-management-squad/workflows/crisis-management-pipeline.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/omega-lock-crisis-management-squad/squad.yaml @squads/omega-lock-crisis-management-squad/workflows/crisis-management-pipeline.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/omega-lock-crisis-management-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/omega-lock-crisis-management-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/omega-lock-crisis-management-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/omega-lock-crisis-management-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/omega-lock-crisis-management-squad/squad.yaml` e `squads/omega-lock-crisis-management-squad/workflows/crisis-management-pipeline.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
