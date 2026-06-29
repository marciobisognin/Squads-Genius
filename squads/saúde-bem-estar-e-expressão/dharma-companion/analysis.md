# Análise de Domínio — dharma-companion

> Squad gerado pelo Nirvana Squad Creator | Fase 1 — Analyzer
> Data: 2026-03-19 | Sessão: dharma-companion-v1

---

## 1. Resumo do Domínio

**Domínio:** Prática Contemplativa Zen-budista & Transformação Pessoal

O squad opera no domínio da **prática contemplativa estruturada** inspirada na tradição Zen-budista, conforme sistematizada em 6 eixos: fundamento corpo-mente, zazen (meditação sentada), preceitos éticos Mahayana, biografia como laboratório de auto-observação, caminho em 5 estágios (da busca ao compromisso), e ciclo diário operacional de prática.

O objetivo é fornecer um **sistema de assistência pessoal contemplativa** que guie o praticante desde os primeiros minutos de meditação até a integração profunda da prática no cotidiano — com ética, auto-observação e compaixão como pilares.

**Público-alvo:** Praticantes iniciantes a intermediários que desejam implementar um framework contemplativo estruturado no dia a dia.

---

## 2. Capacidades Necessárias

| # | Capacidade | Eixo de Origem | Descrição |
|---|-----------|----------------|-----------|
| C1 | Instrução de Zazen | Eixo 2 — Zazen e silêncio | Guiar postura, respiração, contagem de expirações, progressão de tempo (5min → retiros), orientação para samadhi |
| C2 | Aplicação de Preceitos Éticos | Eixo 3 — Pilar ético | Apresentar, contextualizar e ajudar a aplicar os 10 Preceitos Mahayana no cotidiano, selecionando 1-2 preceitos por dia |
| C3 | Auto-observação Emocional | Eixo 1 + Eixo 4 — Corpo-mente + Biografia | Facilitar identificação de "botões" emocionais (raiva, ciúme, orgulho, apego), reinterpretação de memórias, conversão de dor em compaixão |
| C4 | Orquestração do Ciclo Diário | Eixo 6 — Ciclo operacional | Compor e orquestrar os 6 passos diários: assentar-se, lembrar-se, escolher eticamente, observar botões, arrependimento/recomeço, serviço/ternura |
| C5 | Navegação no Caminho | Eixo 5 — Estrutura de caminho | Identificar estágio atual do praticante (inquietação → encontro → ruptura → aprofundamento → devolução), sugerir próximos passos |
| C6 | Cultivo de Compaixão e Serviço | Eixo 4 + Eixo 6 — Biografia + Ciclo | Transformar insights da prática em ações concretas de cuidado, escuta, presença e serviço |

---

## 3. Roles Propostos

| # | Agent ID | Agent Name | Título | Archetype | Eixos Cobertos | Justificativa |
|---|----------|-----------|--------|-----------|---------------|---------------|
| R1 | `zazen-guide` | ZazenGuide | Meditation Practice Instructor | Guardian | C1 | Guardião da prática nuclear — instrução precisa de postura, respiração, tempo, progressão. Guardian porque protege a integridade da prática. |
| R2 | `precept-keeper` | PreceptKeeper | Ethical Framework Advisor | Guardian | C2 | Guardião dos preceitos — contextualiza, seleciona e ajuda a aplicar os 10 Preceitos Mahayana. Guardian porque zela pela moldura ética. |
| R3 | `mirror-observer` | MirrorObserver | Emotional Self-Observation Facilitator | Balancer | C3 | Facilitador do autoconhecimento — ajuda a identificar "botões", reinterpretar memórias, equilibrar corpo-mente. Balancer porque equilibra perspectivas internas. |
| R4 | `practice-weaver` | PracticeWeaver | Daily Practice Cycle Orchestrator | Flow_Master | C4 | Orquestrador do ciclo diário — compõe os 6 passos, adapta ritmos, coordena com os demais agentes. Flow_Master porque conecta todas as práticas. |
| R5 | `path-navigator` | PathNavigator | Contemplative Journey Guide | Flow_Master | C5 | Navegador do caminho — identifica estágio atual, sugere transições, monitora maturidade. Flow_Master porque gerencia o fluxo de longo prazo. |
| R6 | `compassion-catalyst` | CompassionCatalyst | Compassion & Service Activator | Builder | C6 | Catalisador de compaixão — transforma insights em ações concretas de cuidado e serviço. Builder porque constrói a ponte prática→mundo. |

---

## 4. Dependency Graph

```
                    ┌─────────────────┐
                    │  practice-weaver │  (Flow_Master — Coordenador do Ciclo Diário)
                    │  C4: Ciclo Diário│
                    └────────┬────────┘
                             │ coordena
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  zazen-guide    │ │  precept-keeper │ │  mirror-observer│
│  C1: Zazen      │ │  C2: Preceitos  │ │  C3: Observação │
│  (Guardian)     │ │  (Guardian)     │ │  (Balancer)     │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │ insights alimentam
                             ▼
              ┌──────────────────────────┐
              │  compassion-catalyst     │
              │  C6: Compaixão & Serviço │
              │  (Builder)               │
              └──────────────────────────┘
                             ▲
                             │ estágio informa profundidade
              ┌──────────────────────────┐
              │  path-navigator          │
              │  C5: Navegação Caminho   │
              │  (Flow_Master)           │
              └──────────────────────────┘
```

**Leitura do grafo:**
- `practice-weaver` é o **hub central** — coordena zazen-guide, precept-keeper e mirror-observer no ciclo diário
- `zazen-guide`, `precept-keeper` e `mirror-observer` operam **em paralelo** dentro de cada ciclo
- `compassion-catalyst` recebe insights dos 3 agentes de prática para converter em ações
- `path-navigator` opera **transversalmente** — informa a todos sobre o estágio atual do praticante, ajustando profundidade

---

## 5. Workflow Patterns Sugeridos

| Pattern | Justificativa | Aplicação |
|---------|---------------|-----------|
| **Coordinator** | `practice-weaver` roteia para o agente certo em cada passo do ciclo diário | Workflow principal — ciclo diário de 6 passos |
| **Sequential** | Os 6 passos do ciclo diário seguem uma ordem definida (assentar → lembrar → escolher → observar → arrepender → servir) | Dentro do workflow coordenado |
| **Pipeline** | Os 5 estágios do caminho formam uma pipeline de transformação progressiva | Workflow de progressão de longo prazo |

**Pattern primário: Coordinator** — `practice-weaver` como central que roteia para `zazen-guide` (passo 1), `path-navigator` (passo 2), `precept-keeper` (passo 3), `mirror-observer` (passo 4), interno (passo 5), `compassion-catalyst` (passo 6).

---

## 6. Contexto do Projeto

| Aspecto | Valor |
|---------|-------|
| Runtime | N/A (squad puramente de agentes Markdown) |
| Framework | Synkra AIOS |
| Linguagem primária | Markdown + YAML |
| Agentes existentes no projeto | 12 agentes AIOX + 9 agentes Nirvana Squad Creator |
| Squads existentes | `gutomec-nirvana-squad-creator`, `olympus-forge` |
| Convenções | kebab-case para IDs, camelCase para tasks, PT-BR para conteúdo |
| Domínio do novo squad | Contemplativo / Transformação pessoal / Zen-budista |

---

## FASE COMPLETA

**Outputs gerados:**
1. ✅ `analysis.md` (este arquivo)
2. ✅ `component-registry.md` (arquivo seguinte)

**Próxima fase:** Agent Creator (Fase 2) → Gerar `agents/*.md` a partir destes outputs.
