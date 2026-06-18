# PRD — Squad Docente IFFar

Sistema multiagente para automação do trabalho docente e organização de aulas
e materiais didáticos no IFFar.

## 01 — Visão & Problema

No IFFar, o ciclo docente orbita o PPC, o Regulamento Didático-Pedagógico
(RDP), o Plano de Ensino, o Diário de Classe e as normativas da PROEN
(incluindo a Res. CONSUP 52/2019 sobre flexibilizações/AEE). Boa parte do
esforço é repetitivo e propenso a desalinhamento com o curso.

A proposta é um squad de agentes que assiste o docente do planejamento à
avaliação, sempre validando contra a norma vigente e sempre deixando a
decisão e o lançamento oficial sob responsabilidade humana.

## 02 — Objetivos & KPIs (metas-alvo, a calibrar com baseline real)

| KPI | Meta |
|---|---|
| Tempo para elaborar um Plano de Ensino | −60% |
| Materiais com aderência verificada ao PPC | 100% |
| Tempo de preparação do conselho de classe | −50% |
| Lançamento oficial sem homologação humana | 0 (invariante) |

## 03 — Usuários

- **Docente** — planeja o semestre, produz material e avalia.
- **Coordenação de Curso / NDE** — homologa planos e zela pela aderência ao PPC.
- **Equipe pedagógica / TAE** — apoia inclusão (NAPNE/CAI) e prazos.
- **PROEN** — visão institucional de padronização e conformidade.

## 04 — Escopo

**No escopo:**
- Elaboração assistida de Plano de Ensino alinhado ao PPC e ao calendário.
- Geração de materiais didáticos (sequências, slides, apostilas, listas).
- Ponte com produção de animações Manim para conceitos visuais.
- Construção de avaliações, rubricas e banco de itens.
- Adaptação de materiais para AEE conforme normativa.
- Consolidação de dados para conselho de classe (sem decisão).
- Alertas de prazo e checklist de conformidade.

**Fora do escopo:**
- Lançamento oficial de notas, frequência ou diário.
- Qualquer decisão pedagógica final.
- Substituição de sistemas acadêmicos institucionais.
- Tratamento de dado sensível de estudante fora de ambiente controlado.

## 05 — O Squad

Ver `README.md` para a tabela completa dos 9 agentes (A0–A7 + Gate Humano) e
`agents/*.yaml` para a especificação de cada um.

## 06 — Pipeline

Pedido do docente → A0 classifica e roteia → A1 valida contra PPC/RDP →
A2·A3·A4·A5 produzem → A6·A7 consolidam e checam → Gate Humano homologa →
saída oficial. Ver `workflows/pipeline-completo-docente.yaml`.

## 07 — Requisitos

**Funcionais:** classificação de intenção, RAG normativo com fonte, plano de
ensino estruturado, materiais exportáveis, roteiros Manim, avaliações e
rubricas, adaptação AEE, dossiê de conselho (somente leitura), alertas de
prazo, homologação humana obrigatória.

**Não-funcionais:** handoffs em JSON validado por schema, rastreabilidade de
fonte normativa, observabilidade ponta a ponta, isolamento de dado sensível
(LGPD), trilha de auditoria de homologação, operação multi-campus, degradação
segura (sinaliza em vez de inventar).

## 08 — Arquitetura & Stack (referência de implementação full-stack)

| Camada | Tecnologia |
|---|---|
| Orquestração | LangGraph — grafo de agentes, estado e handoffs |
| Schema | Pydantic — contratos SACP em JSON validado |
| Recuperação | RAG — embeddings + vector DB (pgvector ou Pinecone) |
| Modelo | LLM via API; modelo local para etapas com dado sensível |
| Backend | FastAPI — serviços, filas e gate de homologação |
| Frontend | React — painel do docente, fila HITL, mapa do squad |
| Observabilidade | Langfuse / LangSmith — traces, custo, qualidade |

> Este squad entrega a camada de agentes, schemas, scripts determinísticos e
> documentação. A referência de stack acima orienta uma futura implementação
> em produto; os scripts em `scripts/` já funcionam isoladamente com Python
> padrão.

## 09 — Dados & RAG

A base de recuperação ingere PPC, RDP, ementas, resoluções CONSUP/CEPE, guias
da PROEN e o calendário acadêmico. Toda saída que invoca norma traz
rastreabilidade da fonte — e, na ausência de fonte, o agente sinaliza em vez
de inventar.

```
// fronteira de dados
público  → PPC · RDP · resoluções · calendário        (Fases 0–2)
sensível → frequência · notas · perfil AEE             (Fase 3, ambiente controlado)
```

## 10 — LGPD & Governança

- Dado de estudante só entra na Fase 3, em ambiente controlado.
- Gate Humano (HG) obrigatório antes de qualquer oficialização.
- Trilha de auditoria de toda homologação.

## 11 — Roadmap

Ver `docs/roadmap.md`.

## 12 — Riscos

| Risco | Mitigação |
|---|---|
| Alucinação normativa | Toda norma vem do RAG com citação; degradação segura sem fonte |
| Exposição de dado de estudante (LGPD) | Dado sensível só na Fase 3, em ambiente controlado |
| Automatizar decisão que é humana | Gate HITL obrigatório; agentes preparam, nunca oficializam |
| Baixa adoção docente | MVP focado na dor real, sem fricção e sem dado sensível |
| Desalinhamento com o PPC | Guardião Curricular valida toda saída antes da homologação |

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
