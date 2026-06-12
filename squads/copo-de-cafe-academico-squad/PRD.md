# PRD - Copo de Cafe Academico Squad v1.0

**Autor:** Marcio Bisognin / Maeve  
**Versao:** 1.0  
**Licenca:** MIT  

---

## 1. Visao Geral

Squad multi-agente para transformar artigos, teses e pesquisas em materiais didaticos: carrosseis, slides, roteiros de podcast e quizzes.

---

## 2. Arquitetura (5 Agentes)

| Agente | Funcao Principal | Entrada | Saida |
| :--- | :--- | :--- | :--- |
| **A1** | **Desmembrador-Artigo** | Decomposicao de artigos em modulos | PDF de artigo | Modulos didaticos |
| **A2** | **Gerador-Carrossel** | Geracao de carrosseis didaticos | Modulo didatico | Carrossel com imagens |
| **A3** | **Criador-Slides** | Criacao de slides de aula | Modulo didatico | Slides em PPTX/PDF |
| **A4** | **Roteirista-Podcast** | Roteirizacao para podcast | Modulo didatico | Roteiro de episodio |
| **A5** | **Gerador-Quiz** | Criacao de quizzes | Modulo didatico | Quiz com gabarito |

---

## 3. Instrucoes de Execucao

### OpenAI Codex
Carregue o PRD.md e os schemas na janela de contexto.

### Claude Code
Use "Projects" para manter PRD, schemas e documentacao em memoria.

---

**Criado por:** Marcio Bisognin / Maeve  
**Repositorio:** [marciobisognin/Squads-Genius](https://github.com/marciobisognin/Squads-Genius)
