# PERCEPTOR

> **Personagem:** Cientista, examina, mede e analisa
> **Ato do Anel:** `praxis` (πρᾶξις — ação) · **Estrato:** `ORGANON` · **Tipo:** python

## 🎯 Missão
Avalia fit, licença, maturidade, risco, instalação e interoperabilidade das candidatas com um motor determinístico em `Decimal`. O score é Python puro, auditável e reproduzível.

## 📥 Entrada (SACP)
`tool_candidates.json` do JAZZ.

## 📤 Saída (SACP)
`tool_evaluation.json` com `fit_score` e decisão (incorporate/adapt/reject/watch).

## ⚖️ Regras invariantes
- Lei da Fronteira Determinística: nenhum número nasce de LLM.
- Risco alto nunca incorpora automaticamente.
- Pesos canônicos versionados (somam 1.00).

## ▶️ Comandos / acionamento
- `evaluate_tool.py --candidates <cand.json> --out runs/<id>/tool_evaluation.json`.

---

> Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
