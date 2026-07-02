# Task 11 — Sintetizar e Entregar

**Executor:** SÝNTHESIS (mente) + Cortex (resposta ao Hermes)
**Fase:** Entrega (PRD §14.2.9, §18.7)

## Objetivo
Consolidar as entregas parciais em síntese final com **mapa de proveniência por
afirmação** e devolver ao Hermes a resposta estruturada do run.

## Entradas
- Handoffs SACP das tarefas terminais + artefatos validados + revisão
  adversarial resolvida.

## Saídas
- `aether.synthesis/v1` (síntese + evidências + limitações + próximos passos).
- Resposta ao Hermes: `run_id`, `status`, `summary`, `artifacts[]` (sha256),
  `approval_request`, `next_actions[]`, `audit_ref`.

## Passos
1. SÝNTHESIS compõe apenas o que as tarefas produziram; cada afirmação aponta
   evidência.
2. TEKMÉRION valida o lastro da síntese.
3. Cortex monta a resposta estruturada e emite `run.completed` (ou `partial`
   com limitações explícitas).
4. Chain-of-thought privado do modelo **não** é persistido nem exibido
   (princípio 8).

## Critérios de aceite
- 100% das afirmações da síntese com evidência ou marcadas não verificadas.
- Limitações e incertezas propagadas, não suavizadas.
- Artefatos entregues com hash e vínculo ao run.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
