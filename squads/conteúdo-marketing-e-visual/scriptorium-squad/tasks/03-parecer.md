# Task 03 — Parecer (G3)

**Owner:** `G3` (Parecer) · acesso a dados: `somente-verificado`
**Estágio:** 3

## Objetivo
Revisão por pares simulada multi-perspectiva com sprint contract cego e decisão editorial.

## Passos
1. `analista-de-dominio`: detectar área e configurar painel (fase cega).
2. Fechar o `ContratoDeParecer` **antes** de ler o manuscrito (`fase_cega: true`).
3. `parecerista-metodologico`, `parecerista-de-dominio`, `parecerista-interdisciplinar`: pareceres pontuados (1–5).
4. `contraditor-editorial`: ataque adversarial pontuado (limiar de concessão).
5. `sintetizador-editorial`: protocolo mecânico de 3 passos → decisão.
6. `editor-chefe`: decisão editorial + roteiro de revisão.

## Gates
- 🤖 Limiar de concessão; sprint contract cego.
- 🧑 Humano revê a decisão.

## Critério de aceite
- `ContratoDeParecer` com `fase_cega: true` e `decisao` preenchida.
- Condição de falha crítica (alegação não-sustentada) impede Aceitar.
