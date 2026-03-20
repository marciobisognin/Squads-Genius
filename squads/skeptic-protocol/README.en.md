# SKEPTIC Protocol

Implementation of the SKEPTIC Protocol (Constructive Skepticism) across 5 rigorous phases for preventive software engineering.

## Installation

1. Move or clone the `skeptic-protocol` folder into your AIOX squads directory.
2. Ensure the AIOX CLI recognizes the package.
3. Invoke the agents using the `/sk` prefix.

## What It Does

This squad applies constructive skepticism by forcing the identification of all possible flaws before the first line of implementation code is written. It replaces the naive "build and test" approach with "predict flaws, prove them with failing tests, and only then implement the solution."

## Pipeline

| Phase | Agent | Role | Model |
|-------|--------|-------|--------|
| 1 | `failure-predictor` | Accusation Specialist | Guardian |
| 2 | `test-engineer` | Defense Specialist | Builder |
| 3 | `solution-implementer` | Trial Developer | Builder |
| 4 | `red-teamer` | Appeal Challenger | Balancer |
| 5 | `skeptic-orchestrator`| Verdict & Protocol Manager | Flow_Master |

## Agents

| Agent | Title | Archetype | Description |
|--------|--------|-----------|-----------|
| `failure-predictor` | Accusation Specialist | Guardian | Exhaustively identifies failure modes without producing code. |
| `test-engineer` | Defense Specialist | Builder | Creates test suites focused on accusations, requiring them to intentionally fail (Red Phase). |
| `solution-implementer` | Trial Developer | Builder | Refactors and implements code solely to pass the test suite. |
| `red-teamer` | Appeal Challenger | Balancer | Acts as an adversary attempting to break the created solution via edge cases. |
| `skeptic-orchestrator` | Verdict & Protocol Manager | Flow_Master | Ensures protocol fluidity and drafts the official SKEPTIC_REPORT.md. |

## Tasks

| Task | Responsible | Atomic Layer | Description |
|------|-------------|-------------|-----------|
| `generateAccusations()` | `FailurePredictor` | Organism | Gathers vulnerabilities detailing severity and probability. |
| `writeFailingTests()` | `TestEngineer` | Organism | Transcribes vulnerabilities into practical negative tests. |
| `implementTrialCode()` | `SolutionImplementer` | Organism | Codes the solution to satisfy Defense constraints. |
| `executeAppeal()` | `RedTeamer` | Molecule | Actively challenges the codebase approved in the Trial phase. |
| `generateVerdictReport()`| `SkepticOrchestrator` | Molecule | Evaluates final statistics and generates documentation. |

## Workflows

| Workflow | Pattern | Agents | Description |
|----------|---------|---------|-----------|
| `skeptic_pipeline_execution` | Pipeline | All 5 | The main, linear execution of the 5 methodology Phases. |
| `red_team_feedback_loop` | Evaluator-Optimizer | `red-teamer`, `failure-predictor`, `solution-implementer` | The adversarial loop triggered if the Appeal breaks the code. |

## Configuration

- config/coding-standards.md
- config/tech-stack.md
- config/source-tree.md

## Usage

### Available Commands

- `*generate-accusations`: Evaluates requirements and creates Markdown accusations.
- `*write-failing-tests`: Builds the initial test suite based on accusations.
- `*implement-trial-code`: Executes the productive coding routine.
- `*execute-appeal`: Performs an internal pentest or strict edge-case review.
- `*generate-verdict-report`: Compiles the final report of the SKEPTIC cycle.

### Examples

```bash
# To start the pipeline from scratch
/sk:failure-predictor
*generate-accusations --objective="Develop MFA login system"
```

## Autor

Marcio Bisognin

[Squads Platform](https://squads.sh/pt)
[Instagram @marciobisognin](https://www.instagram.com/marciobisognin/)

## License

MIT
