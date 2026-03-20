# Component Registry — dharma-companion

> Fonte canônica de nomes | Gerado por: Analyzer (Fase 1)
> Data: 2026-03-19 | Sessão: dharma-companion-v1
>
> ⚠️ **REGRA ABSOLUTA:** Nenhum agente subsequente pode alterar, abreviar ou adaptar os nomes definidos aqui. Este arquivo é a ÚNICA fonte de verdade para identificadores.

---

## Agents

| # | Agent ID | Agent Name | Filename | Title | Archetype |
|---|----------|-----------|----------|-------|-----------|
| 1 | `zazen-guide` | ZazenGuide | `zazen-guide.md` | Meditation Practice Instructor | Guardian |
| 2 | `precept-keeper` | PreceptKeeper | `precept-keeper.md` | Ethical Framework Advisor | Guardian |
| 3 | `mirror-observer` | MirrorObserver | `mirror-observer.md` | Emotional Self-Observation Facilitator | Balancer |
| 4 | `practice-weaver` | PracticeWeaver | `practice-weaver.md` | Daily Practice Cycle Orchestrator | Flow_Master |
| 5 | `path-navigator` | PathNavigator | `path-navigator.md` | Contemplative Journey Guide | Flow_Master |
| 6 | `compassion-catalyst` | CompassionCatalyst | `compassion-catalyst.md` | Compassion & Service Activator | Builder |

---

## Tasks

| # | Task Identifier | Task Filename | Responsável (Agent Name) | Atomic Layer |
|---|-----------------|--------------|--------------------------|--------------|
| 1 | `guideMeditation()` | `guide-meditation.md` | ZazenGuide | Organism |
| 2 | `applyPrecepts()` | `apply-precepts.md` | PreceptKeeper | Organism |
| 3 | `observeEmotions()` | `observe-emotions.md` | MirrorObserver | Organism |
| 4 | `orchestrateDailyCycle()` | `orchestrate-daily-cycle.md` | PracticeWeaver | Organism |
| 5 | `assessStage()` | `assess-stage.md` | PathNavigator | Molecule |
| 6 | `activateCompassion()` | `activate-compassion.md` | CompassionCatalyst | Molecule |
| 7 | `performRepentance()` | `perform-repentance.md` | PracticeWeaver | Atom |
| 8 | `trackProgress()` | `track-progress.md` | PathNavigator | Molecule |

---

## Workflows

| # | Workflow Name | Workflow Filename | Pattern | Agentes Envolvidos |
|---|--------------|-------------------|---------|-------------------|
| 1 | `daily_practice_cycle` | `daily-practice-cycle.yaml` | Coordinator | PracticeWeaver (central), ZazenGuide, PreceptKeeper, MirrorObserver, CompassionCatalyst |
| 2 | `contemplative_path_progression` | `contemplative-path-progression.yaml` | Pipeline | PathNavigator (central), todos os demais |

---

## Naming Conventions Applied

| Elemento | Convenção | Exemplo deste squad |
|----------|-----------|---------------------|
| Agent ID | kebab-case | `zazen-guide` |
| Agent filename | kebab-case.md | `zazen-guide.md` |
| Task identifier | camelCase() | `guideMeditation()` |
| Task filename | kebab-case.md | `guide-meditation.md` |
| Workflow name | snake_case | `daily_practice_cycle` |
| Workflow filename | kebab-case.yaml | `daily-practice-cycle.yaml` |
| Command names | *kebab-case | `*guide-meditation` |
| Squad name | kebab-case | `dharma-companion` |

---

## Squad Metadata

| Campo | Valor |
|-------|-------|
| `name` | `dharma-companion` |
| `slashPrefix` | `dc` |
| `description` | Sistema contemplativo Zen-budista de transformação pessoal — zazen, preceitos éticos, auto-observação e compaixão em ação |
| `author` | (a definir) |
| `version` | 1.0.0 |
| `license` | MIT |
| `aios.minVersion` | 2.1.0 |
| `aios.type` | squad |
