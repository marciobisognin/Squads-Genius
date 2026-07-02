# Task 13 — Aprender e Memorizar (Autoaprendizado)

**Executor:** memory_engine (motor) + MNÉME (curadoria) + AITÍA (pós-falha)
**Fase:** Avaliação e memória (PRD §14.2.10, §21)

## Objetivo
Fechar o ciclo de aprendizagem: avaliar o run contra os critérios de aceite,
extrair lições candidatas com proveniência e curá-las antes de qualquer
influência sobre decisões futuras.

## Entradas
- Run em estado `completed` ou `partial` (ou `failed` ⇒ análise AITÍA) +
  trilha de eventos, decisões, custos e erros.

## Saídas
- Avaliação pós-run (critérios atendidos, retries, custo, duração).
- Lições em `memory/lessons.jsonl` com `type`
  (`observation|candidate_rule|approved_rule`), `scope`, `evidence[]`,
  `confidence`, `status`, `expires_at` (TTL).
- Parecer de curadoria `aether.lesson-curation/v1` (MNÉME).

## Passos
1. `python3 scripts/memory_engine.py extract --run <run.json>` — lição
   candidata estruturada.
2. MNÉME cura: dedupe contra acervo, conflito com regras vigentes, lastro da
   evidência, escopo e TTL propostos.
3. Falha no run ⇒ AITÍA propõe hipóteses causais; hipótese com evidência gera
   lição candidata.
4. Promoção a `approved_rule` só pelo fluxo humano/política; TTL e revogação
   obrigatórios.

## Critérios de aceite
- Toda lição tem proveniência (run/artefato), escopo e TTL.
- Nenhuma observação não verificada influencia decisão automática.
- Runs aprovados sempre produzem ao menos 1 lição candidata ou descarte
  explícito.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
