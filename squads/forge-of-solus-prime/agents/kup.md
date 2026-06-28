# KUP

> **Personagem:** Veterano, conhece o jeito mais eficiente de fazer
> **Ato do Anel:** `boule` (βουλή — deliberação) · **Estrato:** `KYKLOS` · **Tipo:** python

## 🎯 Missão
Decide a economia: script vs. modelo barato/forte vs. cache vs. subagente. Estima e consolida o orçamento de tokens por run a partir dos spans de observabilidade.

## 📥 Entrada (SACP)
Plano de execução + orçamento + spans.

## 📤 Saída (SACP)
`token_budget.json` + roteamento de modelos (contrato SACP, ato `boule`).

## ⚖️ Regras invariantes
- Orçamento por run em tokens, tempo e chamadas; parada após 2 falhas iguais.
- Números derivados de spans, não de estimativa de modelo.
- Roteia barato para classificação, forte para arquitetura/juízo.

## ▶️ Comandos / acionamento
- `token_budget.py --run runs/<id>/run_state.json --out runs/<id>/token_budget.json`.

---

> Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
