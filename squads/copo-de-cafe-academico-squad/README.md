<div align="center">

# Copo de Cafe Academico Squad

**Transformacao de Artigos em Conteudo Didatico Multimodal**

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-blue?style=for-the-badge)
![Versao](https://img.shields.io/badge/Versao-1.0.0-green?style=for-the-badge)
![Licenca](https://img.shields.io/badge/Licenca-MIT-yellow?style=for-the-badge)

</div>

---

## O que e

Squad multi-agente para transformar artigos, teses e pesquisas em materiais didaticos: carrosseis, slides, roteiros de podcast e quizzes.

---

## Os 5 Agentes

| Agente | Funcao | Entrada | Saida |
| :--- | :--- | :--- | :--- |
| **Desmembrador-Artigo** | Decomposicao de artigos em modulos | PDF de artigo | Modulos didaticos |
| **Gerador-Carrossel** | Geracao de carrosseis didaticos | Modulo didatico | Carrossel com imagens |
| **Criador-Slides** | Criacao de slides de aula | Modulo didatico | Slides em PPTX/PDF |
| **Roteirista-Podcast** | Roteirizacao para podcast | Modulo didatico | Roteiro de episodio |
| **Gerador-Quiz** | Criacao de quizzes | Modulo didatico | Quiz com gabarito |

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
