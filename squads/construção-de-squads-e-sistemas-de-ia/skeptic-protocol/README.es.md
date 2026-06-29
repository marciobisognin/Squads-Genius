# SKEPTIC Protocol

Implementación del SKEPTIC Protocol (Escepticismo Constructivo) en 5 fases rigurosas para la ingeniería de software preventiva.

## Instalación

1. Mueva o clone la carpeta `skeptic-protocol` dentro de su directorio de squads de AIOX.
2. Asegúrese de que la CLI de AIOX reconozca el paquete.
3. Invoque a los agentes utilizando el prefijo `/sk`.

## Qué Hace

Este squad aplica el escepticismo constructivo, forzando la identificación de todas las fallas posibles antes de que se escriba la primera línea de código de implementación. El sistema sustituye el enfoque ingenuo de "construir y probar" por el de "prever fallas, demostrarlas con pruebas que fallan y, solo entonces, implementar la solución".

## Pipeline

| Fase | Agente | Rol | Modelo |
|------|--------|-------|--------|
| 1 | `failure-predictor` | Accusation Specialist | Guardian |
| 2 | `test-engineer` | Defense Specialist | Builder |
| 3 | `solution-implementer` | Trial Developer | Builder |
| 4 | `red-teamer` | Appeal Challenger | Balancer |
| 5 | `skeptic-orchestrator`| Verdict & Protocol Manager | Flow_Master |

## Agentes

| Agente | Título | Archetype | Descripción |
|--------|--------|-----------|-----------|
| `failure-predictor` | Accusation Specialist | Guardian | Identifica exahustivamente los modos de fallo sin producir código. |
| `test-engineer` | Defense Specialist | Builder | Crea suites de pruebas enfocadas en las acusaciones, exigiendo que fallen (Red Phase). |
| `solution-implementer` | Trial Developer | Builder | Refactoriza e implementa código únicamente para hacer pasar las pruebas. |
| `red-teamer` | Appeal Challenger | Balancer | Actúa como adversario intentando romper la solución creada mediante casos extremos. |
| `skeptic-orchestrator` | Verdict & Protocol Manager | Flow_Master | Garantiza la fluidez del protocolo y redacta el SKEPTIC_REPORT.md oficial. |

## Tasks

| Task | Responsable | Atomic Layer | Descripción |
|------|-------------|-------------|-----------|
| `generateAccusations()` | `FailurePredictor` | Organism | Recopila vulnerabilidades detallando severidad y probabilidad. |
| `writeFailingTests()` | `TestEngineer` | Organism | Transcribe vulnerabilidades a pruebas prácticas negativas. |
| `implementTrialCode()` | `SolutionImplementer` | Organism | Codifica la solución para satisfacer las restricciones defensivas. |
| `executeAppeal()` | `RedTeamer` | Molecule | Desafía activamente al código aprobado en la fase Trial. |
| `generateVerdictReport()`| `SkepticOrchestrator` | Molecule | Evalúa las estadísticas finales y genera la documentación. |

## Workflows

| Workflow | Pattern | Agentes | Descripción |
|----------|---------|---------|-----------|
| `skeptic_pipeline_execution` | Pipeline | Los 5 | La ejecución principal y lineal de las 5 Fases de la metodología. |
| `red_team_feedback_loop` | Evaluator-Optimizer | `red-teamer`, `failure-predictor`, `solution-implementer` | El ciclo adversarial disparado si la apelación rompe el código. |

## Configuración

- config/coding-standards.md
- config/tech-stack.md
- config/source-tree.md

## Uso

### Comandos Disponibles

- `*generate-accusations`: Evalúa requisitos y crea acusaciones en Markdown.
- `*write-failing-tests`: Construye la suite de pruebas inicial basada en las acusaciones.
- `*implement-trial-code`: Ejecuta la rutina de código productiva.
- `*execute-appeal`: Realiza un *pentest* interno o una revisión de casos extremos.
- `*generate-verdict-report`: Compila el informe final del ciclo SKEPTIC.

### Ejemplos

```bash
# Para iniciar el pipeline desde cero
/sk:failure-predictor
*generate-accusations --objective="Desarrollar sistema de login con MFA"
```

## Autor

Marcio Bisognin

[Squads Platform](https://squads.sh/pt)
[Instagram @marciobisognin](https://www.instagram.com/marciobisognin/)

## Licencia

MIT
