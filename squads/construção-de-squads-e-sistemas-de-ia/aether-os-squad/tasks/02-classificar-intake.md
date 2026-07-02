# Task 02 — Classificar Intake

**Executor:** KRITÉS (mente) + Cortex (roteamento)
**Fase:** Classificação (PRD §13, §14.2.2)

## Objetivo
Classificar a intenção em regime de complexidade (Cynefin) e decidir se o gate
humano de classificação é obrigatório antes do planejamento.

## Entradas
- `AetherIntentEnvelope` + contexto recuperado.

## Saídas
- `aether.intake-classification/v1` persistida como `IntakeClassification`.
- Estado do run: `classified` ou `awaiting_classification`.

## Passos
1. KRITÉS propõe regime, domínio, classe de dado, risco estimado e confiança.
2. Cortex verifica gatilhos de gate: regime complexo/caótico/indefinido;
   confiança < limiar; dado `restricted`; efeito irreversível no enunciado;
   ambiguidade entre objetivos incompatíveis.
3. Se gate exigido: acionar Task 03 (MAIEUTIKÉ) e aguardar confirmação humana.
4. Registrar a decisão do gate como evento auditável.

## Critérios de aceite
- Classificação valida no schema e é imutável após persistência.
- Nenhum run avança de `received` a `planned` sem classificação.
- Decisão humana (quando houver) registrada com identidade e timestamp.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
