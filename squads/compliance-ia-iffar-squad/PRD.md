# PRD - Compliance IA IFFar Squad v1.0

**Autor:** Marcio Bisognin / Maeve  
**Versao:** 1.0  
**Licenca:** MIT  

---

## 1. Visao Geral

Squad multi-agente para monitoramento de prazos legais, alertas de vencimentos e geracao de pareceres.

---

## 2. Arquitetura (5 Agentes)

| Agente | Funcao Principal | Entrada | Saida |
| :--- | :--- | :--- | :--- |
| **A1** | **Vigilante-Prazos** | Monitoramento de prazos legais | Calendario | Alertas |
| **A2** | **Auditor-Checklist** | Checklist de conformidade | Documentacao | Status conformidade |
| **A3** | **Gerador-Pareceres** | Geracao de pareceres previos | Caso e normativa | Parecer |
| **A4** | **Dashboard-Riscos** | Dashboard de riscos | Dados de conformidade | Dashboard KPIs |
| **A5** | **Auditor-Externo** | Preparacao para auditorias | Requisitos | Relatorio preparacao |

---

## 3. Instrucoes de Execucao

### OpenAI Codex
Carregue o PRD.md na janela de contexto.

### Claude Code
Use "Projects" para manter PRD e documentacao em memoria.

---

**Criado por:** Marcio Bisognin / Maeve  
**Repositorio:** [marciobisognin/Squads-Genius](https://github.com/marciobisognin/Squads-Genius)
