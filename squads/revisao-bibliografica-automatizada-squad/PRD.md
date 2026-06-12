# PRD - Revisao Bibliografica Automatizada Squad v1.0

**Autor:** Marcio Bisognin / Maeve  
**Versao:** 1.0  
**Licenca:** MIT  

---

## 1. Visao Geral

Squad multi-agente para busca semantica, sintese de artigos, mapeamento de lacunas e formatacao ABNT.

---

## 2. Arquitetura (5 Agentes)

| Agente | Funcao Principal | Entrada | Saida |
| :--- | :--- | :--- | :--- |
| **A1** | **Buscador-Semantico** | Busca semantica em bases | Tema | Artigos |
| **A2** | **Sintetizador-Artigos** | Sintese de artigos | Artigos | Resumos |
| **A3** | **Mapeador-Lacunas** | Mapeamento de lacunas | Revisao parcial | Mapa de lacunas |
| **A4** | **Gerador-Revisao** | Geracao de revisao | Sinteses | Revisao |
| **A5** | **Formatador-Abnt** | Formatacao ABNT | Referencias | Referencias formatadas |

---

## 3. Instrucoes de Execucao

### OpenAI Codex
Carregue o PRD.md na janela de contexto.

### Claude Code
Use "Projects" para manter PRD e documentacao em memoria.

---

**Criado por:** Marcio Bisognin / Maeve  
**Repositorio:** [marciobisognin/Squads-Genius](https://github.com/marciobisognin/Squads-Genius)
