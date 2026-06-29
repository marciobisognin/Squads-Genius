# Análise de Domínio: SKEPTIC Protocol Squad

## 1. Resumo do Domínio
O domínio foca na engenharia de software preventiva e guiada por falhas através do protocolo SKEPTIC. O squad atua na etapa de planejamento e implementação de código, substituindo a abordagem "construir e testar" por "prever falhas, testar falhas e, só então, construir". O sistema requer documentação estrita e orquestração em 5 fases sequenciais rigorosas (Accusation, Defense, Trial, Appeal, Verdict).

## 2. Capacidades Necessárias
1. **Previsão de Falhas (Accusation):** Capacidade de analisar um requisito ou arquitetura e listar exaustivamente modos de falha (severidade, probabilidade, provas) em formato Markdown. Restrição severa: imposição de limite zero na geração de código de implementação nesta capacidade.
2. **Engenharia de Testes Negativos (Defense):** Capacidade de mapear acusações para testes unitários/integração que capturem a vulnerabilidade (Red phase of TDD).
3. **Implementação Guiada por Testes (Trial):** Capacidade de desenvolver soluções e refatorar código unicamente voltado a satisfazer a suíte de testes criada.
4. **Teste de Estresse / Edge Cases (Appeal):** Capacidade de atuar de forma adversarial contra a própria solução recém-criada, gerando novos vetores de falha.
5. **Governança e Geração de Relatórios (Verdict):** Capacidade de auditar o fim do ciclo SKEPTIC, declarar acusações superadas e documentar o `SKEPTIC_REPORT.md`.

## 3. Roles Propostos

| Agent ID | Nome do Agente | Título Sugerido | Arquétipo |
|----------|----------------|-----------------|-----------|
| `failure-predictor` | Failure Predictor | Accusation Specialist | Guardian |
| `test-engineer` | Test Engineer | Defense Specialist | Builder |
| `solution-implementer` | Solution Implementer | Trial Developer | Builder |
| `red-teamer` | Red Teamer | Appeal Challenger | Balancer |
| `skeptic-orchestrator` | Skeptic Orchestrator | Verdict & Protocol Manager | Flow_Master |

## 4. Dependency Graph (ASCII)

```
[Requirement Input / Prompts]
       │
       ▼
+-----------------------------+
| failure-predictor (Fase 1)  | <-- ZERO CODE LIMIT.
| Generates accusations       |
+-----------------------------+
       │
       ▼
+-----------------------------+
| test-engineer (Fase 2)      | <-- Map acc. to failing tests
| Writes tests                |
+-----------------------------+
       │
       ▼
+-----------------------------+
| solution-implementer (Fase 3)| <-- Code implementation
| Makes tests pass            |
+-----------------------------+
       │
       ▼
+-----------------------------+
| red-teamer (Fase 4)         | <-- Adversarial attack testing
| Attempts to break solution  |
+-----------------------------+
       │
       | (If valid edge cases found, return to Phase 1)
       ▼
+-----------------------------+
| skeptic-orchestrator (Fase 5)| <-- Report compilation
| Declares Verdict            |
+-----------------------------+
       │
       ▼
 [SKEPTIC_REPORT.md]
```

## 5. Workflow Patterns Sugeridos
1. **Pipeline Pattern (`skeptic_pipeline_execution`):** A execução primordial em cascata, fase 1 à fase 5.
2. **Evaluator-Optimizer (`red_team_feedback_loop`):** Uma malha entre Fase 4 (Appeal) indicando reprovação de código não robusto de volta para Fase 1 ou 3 para melhorias.

## 6. Contexto do Projeto
- **Arquitetura Base:** O squad será injetado no ecossistema atual do AIOX e adere estritamente as restrições da metodologia descrita.
- **Diferencial Crítico:** A obrigatoriedade de falhas intencionais dos testes antes do trial, e o foco em ceticismo.
