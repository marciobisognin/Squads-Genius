# Dharma Companion

> Zen Buddhist contemplative system for personal transformation — zazen, ethical precepts, self-observation, and compassion in action.

## Installation

```bash
npx squads add dharma-companion
```

## What It Does

Dharma Companion is a **contemplative assistance squad** that guides the practitioner in implementing a Zen Buddhist practice framework structured around 6 axes:

- **Zazen** — seated meditation as the core practice
- **Mahayana Precepts** — ethical framework for daily life
- **Self-observation** — identifying emotional triggers ("buttons")
- **Daily cycle** — 6 integrated practice steps
- **Contemplative path** — 5 stages of transformation
- **Active compassion** — converting insights into concrete actions

From initial restlessness to giving back to the world, the squad accompanies every step with precise instruction, ethical reflection, and tenderness.

## Pipeline — 6-Step Daily Cycle

| Step | Agent | Action | Min. Time |
|------|-------|--------|-----------|
| 1 | 🧘 ZazenGuide | Settle down — zazen session | 5 min |
| 2 | 🧭 PathNavigator | Remember — impermanence and interdependence | 1 min |
| 3 | ⚖️ PreceptKeeper | Choose — 1-2 precepts for the day | 2 min |
| 4 | 🪞 MirrorObserver | Observe — notice the "buttons" throughout the day | continuous |
| 5 | 🔄 PracticeWeaver | Repent — repentance and renewal ritual | 1 min |
| 6 | 💚 CompassionCatalyst | Serve — concrete action of care and tenderness | continuous |

## Agents

| Icon | Name | Archetype | Responsibility |
|------|------|-----------|----------------|
| 🧘 | ZazenGuide | Guardian | Zazen instruction: posture, breathing, progression |
| ⚖️ | PreceptKeeper | Guardian | Application of the 10 Mahayana Precepts |
| 🪞 | MirrorObserver | Balancer | Emotional self-observation, "buttons" map |
| 🔄 | PracticeWeaver | Flow_Master | Orchestration of the 6-step daily cycle |
| 🧭 | PathNavigator | Flow_Master | Navigation through the 5 stages of the path |
| 💚 | CompassionCatalyst | Builder | Conversion of insights into compassionate actions |

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
Daily cycle coordinated by PracticeWeaver — from morning meditation to evening service.
```
[ZazenGuide] → [PathNavigator] → [PreceptKeeper] → [MirrorObserver] → [Repentance] → [CompassionCatalyst]
```

### contemplative_path_progression
Progression pipeline through the 5 contemplative stages — from initial search to giving back to the world.
```
[PathNavigator] → assesses stage → adjusts depth → [All agents adapt]
```

## The 5 Stages of the Path

| # | Stage | Description |
|---|-------|-------------|
| 1 | 🌊 Restlessness and Search | Emptiness, existential questions, scattered search |
| 2 | 🌱 Encountering the Practice | Contact with zazen, first retreats, transformation |
| 3 | 🔥 Rupture and Dedication | Commitment, life changes, intense training |
| 4 | 🏔️ Deepening | Practice-life integration, "realistic mysticism" |
| 5 | 🌍 Giving Back to the World | Teaching, sharing, large-scale compassion |

## Configuration

- `config/coding-standards.md` — Code conventions and tone
- `config/tech-stack.md` — Technologies and tradition
- `config/source-tree.md` — Directory structure

## Usage

### Complete daily cycle
```
/dc:practice-weaver
*orchestrate-daily-cycle --time-available=30
```

### Individual agents
```
/dc:zazen-guide             — Zazen session
/dc:precept-keeper           — Precepts of the day
/dc:mirror-observer          — Emotional observation
/dc:path-navigator           — Stage assessment
/dc:compassion-catalyst      — Compassionate action
/dc:practice-weaver          — Complete daily cycle
```

## Author

Marcio Bisognin
- [Squads Platform](https://squads.sh/pt)
- [Instagram @marciobisognin](https://www.instagram.com/marciobisognin/)

## License

MIT
