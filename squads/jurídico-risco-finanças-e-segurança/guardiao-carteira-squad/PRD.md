# PRD - Guardiao Carteira Squad v1.0

**Autor:** Marcio Bisognin / Maeve  
**Versao:** 1.0  
**Licenca:** MIT  

---

## 1. Visao Geral

Squad multi-agente para consolidacao, analise e monitoramento de carteiras de investimento, incluindo acoes, FIIs, criptoativos e renda fixa.

---

## 2. Arquitetura (5 Agentes)

| Agente | Funcao Principal | Entrada | Saida |
| :--- | :--- | :--- | :--- |
| **A1** | **Consolidador-Carteira** | Consolidacao de dados de corretoras | Extratos, APIs, CSVs | Carteira unificada |
| **A2** | **Analista-Risco** | Analise de risco e correlacao | Carteira, dados de mercado | Metricas de risco |
| **A3** | **Alerta-Rebalanceamento** | Alertas de rebalanceamento | Carteira, alocacao alvo | Alertas e sugestoes |
| **A4** | **Rastreador-Dividendos** | Rastreamento de dividendos | Carteira, datas | Previsao e historico |
| **A5** | **Relatorio-Performance** | Relatorio de performance | Dados de performance | Relatorio PDF |

---

## 3. Instrucoes de Execucao

### OpenAI Codex
Carregue o PRD.md e os schemas na janela de contexto.

### Claude Code
Use "Projects" para manter PRD, schemas e documentacao em memoria.

---

**Criado por:** Marcio Bisognin / Maeve  
**Repositorio:** [marciobisognin/Squads-Genius](https://github.com/marciobisognin/Squads-Genius)
