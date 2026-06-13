<div align="center">

# Guardiao Carteira Squad

**Gestao Inteligente de Investimentos e Criptoativos**

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-blue?style=for-the-badge)
![Versao](https://img.shields.io/badge/Versao-1.0.0-green?style=for-the-badge)
![Licenca](https://img.shields.io/badge/Licenca-MIT-yellow?style=for-the-badge)

</div>

---

## O que e

Squad multi-agente para consolidacao, analise e monitoramento de carteiras de investimento, incluindo acoes, FIIs, criptoativos e renda fixa.

---

## Os 5 Agentes

| Agente | Funcao | Entrada | Saida |
| :--- | :--- | :--- | :--- |
| **Consolidador-Carteira** | Consolidacao de dados de corretoras | Extratos, APIs, CSVs | Carteira unificada |
| **Analista-Risco** | Analise de risco e correlacao | Carteira, dados de mercado | Metricas de risco |
| **Alerta-Rebalanceamento** | Alertas de rebalanceamento | Carteira, alocacao alvo | Alertas e sugestoes |
| **Rastreador-Dividendos** | Rastreamento de dividendos | Carteira, datas | Previsao e historico |
| **Relatorio-Performance** | Relatorio de performance | Dados de performance | Relatorio PDF |

---

## Stack Tecnico

| Camada | Tecnologia |
| :--- | :--- |
| Orquestracao | LangGraph |
| LLM | Claude (Anthropic) |

---

## Licenca

Este projeto esta sob a licenca **MIT**.

**Criado por:** Marcio Bisognin / Maeve  
**Repositorio:** [marciobisognin/Squads-Genius](https://github.com/marciobisognin/Squads-Genius)
