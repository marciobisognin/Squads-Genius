<div align="center">

# Revisao Bibliografica Automatizada Squad

**Producao Academica em Larga Escala com IA**

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-blue?style=for-the-badge)
![Versao](https://img.shields.io/badge/Versao-1.0.0-green?style=for-the-badge)
![Licenca](https://img.shields.io/badge/Licenca-MIT-yellow?style=for-the-badge)

</div>

---

## O que e

Squad multi-agente para busca semantica, sintese de artigos, mapeamento de lacunas e formatacao ABNT.

---

## Os 5 Agentes

| Agente | Funcao | Entrada | Saida |
| :--- | :--- | :--- | :--- |
| **Buscador-Semantico** | Busca semantica em bases | Tema | Artigos |
| **Sintetizador-Artigos** | Sintese de artigos | Artigos | Resumos |
| **Mapeador-Lacunas** | Mapeamento de lacunas | Revisao parcial | Mapa de lacunas |
| **Gerador-Revisao** | Geracao de revisao | Sinteses | Revisao |
| **Formatador-Abnt** | Formatacao ABNT | Referencias | Referencias formatadas |

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
