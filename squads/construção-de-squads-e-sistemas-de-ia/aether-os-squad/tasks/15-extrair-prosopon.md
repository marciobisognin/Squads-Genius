# Task 15 — Extrair e Publicar Prósopon (Retratista)

**Executor:** RETRATISTA (mente) + SÝNTHESIS + ELENCHUS + persona_engine (motor)
**Fase:** Perfis de persona (PRD v1.3, §18.9–18.11)

## Objetivo
Produzir um prósopon (`aether.prosopon/v1`) a partir de corpus de obra
pública, com proveniência item a item, e publicá-lo na Galeria sob salvaguardas.

## Entradas
- Corpus público e licenciável aprovado no policy gate + partição reservada
  para validação de fidelidade.

## Saídas
- `aether.prosopon/v1` (5 camadas: principles, mental_models, heuristics,
  methods, voice — cada item com `provenance`).
- Relatório de fidelidade + revisão adversarial + registro na Galeria
  (`persona_engine.py gallery add`, status `experimental`).

## Passos
1. RETRATISTA extrai itens candidatos por camada, cada um com trecho-fonte.
2. SÝNTHESIS consolida com mapa de proveniência por item.
3. ELENCHUS refuta: item sem lastro verificável no corpus é **eliminado**.
4. `python3 scripts/persona_engine.py validate --prosopon <arquivo>` —
   schema, proveniência obrigatória por item, rótulo de disclosure presente.
5. Validação de fidelidade contra a partição reservada (concordância
   estrutural) + check de **zero atribuição factual**.
6. Revisão humana → publicação na Galeria (status `experimental`); promoção a
   `trusted` segue o harness de mentes; troca de perfil de modelo reexige gate.

## Critérios de aceite
- 100% dos itens com proveniência; zero afirmações factuais sobre a pessoa.
- Rótulo "conteúdo sintético inspirado em método publicado" presente e
  verificado automaticamente na egressão.
- Nenhum campo de persona lido por motor determinístico (fronteira dura).
- Despublicação a pedido do titular executável e auditada.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
