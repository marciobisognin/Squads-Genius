# Component Registry: SKEPTIC Protocol Squad

Este documento é a FONTE ÚNICA DE VERDADE para todos os nomes (agentes, tasks, workflows) do squad SKEPTIC Protocol. Qualquer geração subsequente (Agent Creator, Task Creator, Workflow Creator) DEVE usar estritamente os nomes exatos definidos aqui.

## 1. Agentes (Agents)

| Agent ID (kebab-case) | Agent Name | Título / Role |
|-------------------------|------------|---------------|
| `failure-predictor` | FailurePredictor | Accusation Specialist |
| `test-engineer` | TestEngineer | Defense Specialist |
| `solution-implementer` | SolutionImplementer | Trial Developer |
| `red-teamer` | RedTeamer | Appeal Challenger |
| `skeptic-orchestrator` | SkepticOrchestrator | Verdict & Protocol Manager |

## 2. Tarefas (Tasks)

| Task Identifier | Responsável (Agent ID) | Função Primária |
|-----------------|------------------------|-----------------|
| `generateAccusations()` | `failure-predictor` | Identifica modos de falha (severidade, probabilidade) baseado em requisitos, sem emitir código de implementação. |
| `writeFailingTests()` | `test-engineer` | Constrói testes (unitários/integração) focados em comprovar, através de bugs/falhas, a validade das acusações. |
| `implementTrialCode()`| `solution-implementer` | Desenvolve o respectivo código fonte do software com objetivo único de reparar as falhas e aprovar os testes. |
| `executeAppeal()` | `red-teamer` | Varre a solução desenvolvida tentando explorar edge cases não coberto pelos testes iniciais. |
| `generateVerdictReport()`| `skeptic-orchestrator` | Analisa os logs do ciclo, mapeia cobertura, define o veredito do desenvolvimento e gera SKEPTIC_REPORT.md. |

## 3. Workflows

| Workflow Name | Formato | Padrão Recomendado | Agentes Envolvidos |
|---------------|---------|--------------------|--------------------|
| `skeptic_pipeline_execution` | snake_case | Pipeline | `failure-predictor` → `test-engineer` → `solution-implementer` → `red-teamer` → `skeptic-orchestrator` |
| `red_team_feedback_loop` | snake_case | Evaluator-Optimizer | `red-teamer`, `failure-predictor`, `solution-implementer` |

## 4. Convenções do Squad
- **Prefixo CLI:** `sk` (ex: `/sk:failure-predictor`)
- **Idiomas:** Descrições textuais em PT-BR ou EN-US. Artefatos de código, testes, variáveis de ambiente ou IDs sempre em Inglês.
