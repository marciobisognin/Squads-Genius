# PRD - Gestor Projetos IFFar Squad v1.0

**Autor:** Marcio Bisognin / Maeve  
**Versao:** 1.0  
**Licenca:** MIT  

---

## 1. Visao Geral

Squad multi-agente para gestao do ciclo de vida de projetos e contratos do IFFar, desde a abertura ate a prestacao de contas.

---

## 2. Arquitetura (5 Agentes)

| Agente | Funcao Principal | Entrada | Saida |
| :--- | :--- | :--- | :--- |
| **A1** | **Abridor-Processo** | Abertura de processo | Demanda | Processo |
| **A2** | **Acompanhador-Medicoes** | Acompanhamento de medicoes | Contrato | Alertas |
| **A3** | **Gerador-Relatorios** | Relatorios de acompanhamento | Dados | Relatorio |
| **A4** | **Encerrador-Contrato** | Encerramento e prestacao | Contrato | Encerramento |
| **A5** | **Relatorio-Gestao** | Relatorio para Reitoria | Projetos | Relatorio consolidado |

---

## 3. Instrucoes de Execucao

### OpenAI Codex
Carregue o PRD.md na janela de contexto.

### Claude Code
Use "Projects" para manter PRD e documentacao em memoria.

---

**Criado por:** Marcio Bisognin / Maeve  
**Repositorio:** [marciobisognin/Squads-Genius](https://github.com/marciobisognin/Squads-Genius)
