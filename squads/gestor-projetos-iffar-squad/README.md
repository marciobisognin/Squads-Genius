<div align="center">

# Gestor Projetos IFFar Squad

**Ciclo Completo de Projetos e Contratos no IFFar**

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-blue?style=for-the-badge)
![Versao](https://img.shields.io/badge/Versao-1.0.0-green?style=for-the-badge)
![Licenca](https://img.shields.io/badge/Licenca-MIT-yellow?style=for-the-badge)

</div>

---

## O que e

Squad multi-agente para gestao do ciclo de vida de projetos e contratos do IFFar, desde a abertura ate a prestacao de contas.

---

## Os 5 Agentes

| Agente | Funcao | Entrada | Saida |
| :--- | :--- | :--- | :--- |
| **Abridor-Processo** | Abertura de processo | Demanda | Processo |
| **Acompanhador-Medicoes** | Acompanhamento de medicoes | Contrato | Alertas |
| **Gerador-Relatorios** | Relatorios de acompanhamento | Dados | Relatorio |
| **Encerrador-Contrato** | Encerramento e prestacao | Contrato | Encerramento |
| **Relatorio-Gestao** | Relatorio para Reitoria | Projetos | Relatorio consolidado |

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
