# Dharma Companion

> Sistema contemplativo budista zen de transformación personal: zazen, preceptos éticos, autoobservación y compasión en acción.

## Instalación

```bash
npx squads add dharma-companion
```

## Qué Hace

Dharma Companion es un **squad de asistencia contemplativa** que guía al practicante en la implementación de un framework de práctica budista zen estructurado en 6 ejes:

- **Zazen** — meditación sentada como práctica central
- **Preceptos Mahayana** — marco ético para la vida cotidiana
- **Autoobservación** — identificación de desencadenantes emocionales ("botones")
- **Ciclo diario** — 6 pasos integrados de práctica
- **Camino contemplativo** — 5 etapas de transformación
- **Compasión activa** — conversión de introspecciones en acciones concretas

Desde la inquietud inicial hasta la devolución al mundo, el squad acompaña cada paso con instrucción precisa, reflexión ética y ternura.

## Pipeline — Ciclo Diario de 6 Pasos

| Paso | Agente | Acción | Tiempo Mín. |
|------|--------|--------|-------------|
| 1 | 🧘 ZazenGuide | Asentarse — sesión de zazen | 5 min |
| 2 | 🧭 PathNavigator | Recordar — impermanencia e interdependencia | 1 min |
| 3 | ⚖️ PreceptKeeper | Elegir — 1-2 preceptos para el día | 2 min |
| 4 | 🪞 MirrorObserver | Observar — notar los "botones" a lo largo del día | continuo |
| 5 | 🔄 PracticeWeaver | Arrepentirse — ritual de arrepentimiento y reinicio | 1 min |
| 6 | 💚 CompassionCatalyst | Servir — acción concreta de cuidado y ternura | continuo |

## Agentes

| Icon | Nombre | Archetype | Responsabilidad |
|------|--------|-----------|-----------------|
| 🧘 | ZazenGuide | Guardian | Instrucción de zazen: postura, respiración, progresión |
| ⚖️ | PreceptKeeper | Guardian | Aplicación de los 10 Preceptos Mahayana |
| 🪞 | MirrorObserver | Balancer | Autoobservación emocional, mapa de "botones" |
| 🔄 | PracticeWeaver | Flow_Master | Orquestación del ciclo diario de 6 pasos |
| 🧭 | PathNavigator | Flow_Master | Navegación por las 5 etapas del camino |
| 💚 | CompassionCatalyst | Builder | Conversión de introspecciones en acciones compasivas |

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
Ciclo diario coordinado por PracticeWeaver — desde la meditación matutina hasta el servicio vespertino.
```
[ZazenGuide] → [PathNavigator] → [PreceptKeeper] → [MirrorObserver] → [Arrepentimiento] → [CompassionCatalyst]
```

### contemplative_path_progression
Pipeline de progresión en las 5 etapas contemplativas — desde la búsqueda inicial hasta la devolución al mundo.
```
[PathNavigator] → evalúa etapa → ajusta profundidad → [Todos los agentes se adaptan]
```

## Las 5 Etapas del Camino

| # | Etapa | Descripción |
|---|-------|-------------|
| 1 | 🌊 Inquietud y Búsqueda | Vacío, preguntas existenciales, búsqueda dispersa |
| 2 | 🌱 Encuentro con la Práctica | Contacto con zazen, primeros retiros, transformación |
| 3 | 🔥 Ruptura y Dedicación | Compromiso, cambios de vida, entrenamiento intenso |
| 4 | 🏔️ Profundización | Integración práctica-vida, "misticismo realista" |
| 5 | 🌍 Devolución al Mundo | Enseñar, compartir, compasión a gran escala |

## Configuración

- `config/coding-standards.md` — Convenciones de código y tono
- `config/tech-stack.md` — Tecnologías y tradición
- `config/source-tree.md` — Estructura de directorios

## Uso

### Ciclo diario completo
```
/dc:practice-weaver
*orchestrate-daily-cycle --time-available=30
```

### Agentes individuales
```
/dc:zazen-guide             — Sesión de zazen
/dc:precept-keeper           — Preceptos del día
/dc:mirror-observer          — Observación emocional
/dc:path-navigator           — Evaluación de etapa
/dc:compassion-catalyst      — Acción compasiva
/dc:practice-weaver          — Ciclo diario completo
```

## Autor

Marcio Bisognin
- [Squads Platform](https://squads.sh/pt)
- [Instagram @marciobisognin](https://www.instagram.com/marciobisognin/)

## Licencia

MIT
