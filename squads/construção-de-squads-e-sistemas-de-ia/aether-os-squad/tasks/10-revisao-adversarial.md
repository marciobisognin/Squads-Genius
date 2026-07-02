# Task 10 — Revisão Adversarial (Contraditório)

**Executor:** ELENCHUS + TEKMÉRION (mentes)
**Fase:** Validação e contraditório (PRD §18.4, §14.2.8, §17.3)

## Objetivo
Submeter toda conclusão de impacto médio, alto ou crítico — e todo artefato
forjado — a uma revisão que **tenta refutá-la** antes da entrega, com cada
objeção obrigada a apresentar evidência.

## Entradas
- Artefato/conclusão alvo + índice de evidências + tier de impacto.

## Saídas
- `aether.adversarial-review/v1` persistida como `AdversarialReview`:
  objeções (com evidência ou marcadas conjectura), severidade,
  `resolution_required`, flags de bajulação.

## Passos
1. ELENCHUS levanta objeções, riscos e hipóteses alternativas.
2. **Cada objeção passa por TEKMÉRION**: evidência apontada ou marca de
   conjectura (simetria anti-ficção compensatória).
3. Objeção com evidência ⇒ correção ou justificativa obrigatória antes de
   `completed`; sem evidência ⇒ ponto de atenção registrado.
4. Correções retornam ao loop de revisão (workflow `loop_revisao_entrega`).

## Critérios de aceite
- Nenhum resultado de impacto médio+ promovido a `completed` sem revisão
  resolvida.
- Zero objeções "órfãs": todas com evidência ou marcadas conjectura.
- Veredito persistido e auditável no dashboard.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
