# PRD - Mentor IA Educacao Squad v1.0

**Autor:** Marcio Bisognin / Maeve  
**Versao:** 1.0  
**Licenca:** MIT  

---

## 1. Visao Geral

Squad multi-agente para planejamento de aula, geracao de material didatico adaptativo, quiz e feedback personalizado.

---

## 2. Arquitetura (5 Agentes)

| Agente | Funcao Principal | Entrada | Saida |
| :--- | :--- | :--- | :--- |
| **A1** | **Planner-Aula** | Planejamento de aula com IA | Objetivos, conteudo, turma | Plano de aula |
| **A2** | **Gerador-Material** | Geracao de material didatico | Plano de aula | Material adaptativo |
| **A3** | **Avaliador-Quiz** | Criacao e correcao de quiz | Plano de aula | Quiz e feedback |
| **A4** | **Analista-Dificuldades** | Analise de dificuldades | Resultados de quiz | Relatorio |
| **A5** | **Relatorio-Turma** | Relatorio de desempenho | Dados de alunos | Relatorio turma |

---

## 3. Instrucoes de Execucao

### OpenAI Codex
Carregue o PRD.md na janela de contexto.

### Claude Code
Use "Projects" para manter PRD e documentacao em memoria.

---

**Criado por:** Marcio Bisognin / Maeve  
**Repositorio:** [marciobisognin/Squads-Genius](https://github.com/marciobisognin/Squads-Genius)
