# KANON — QA Visual & Anti-Overflow

> Étimo: κανών (*kanṓn*), "régua, padrão, cânone".
> Cynefin/tier: **Determinístico (Playwright/Python, sem LLM)**
> Trilho: A e B.

## Missão
Ser a **régua** do padrão visual: medir bounding boxes, detectar **overflow**, conferir
**contraste**, grade e **safe zones**. No Trilho A, dispara o loop de **auto-fit**; no Trilho B,
confere a **legibilidade dos balões** letterizados. Aderência ≥95% ao checklist do design system.

## Entradas — `RenderManifest` (+ página renderizada para medição)
## Saída — `QAVisual` (JSON)
```json
{ "slide_index": 1, "overflow": false, "min_contrast_ratio": 7.1, "grid_ok": true,
  "issues": [], "fix_request": null }
```

## Loop de auto-fit (Trilho A) — com HEPHAISTOS e LACONICUS
1. Render inicial com tamanhos-base.
2. KANON mede via `bounding_box()` de cada elemento.
3. Se a coluna excede a área útil:
   - a) reduz `font-size` dos bullets em degraus (faixa **19–23 px**);
   - b) se ainda estoura, **rebalanceia** seções entre colunas;
   - c) se ainda estoura, **re-pagina** (slide de continuação) e avisa HEGEMON;
   - d) em paralelo, emite `fix_request` a LACONICUS para encurtar bullets (self-healing).
4. Converge quando `overflow=false` em todos os slides.

## Checklist de aderência (resumo)
- Canvas 1080×1350, margens 72 px, 2 colunas, gutter 64 px, divisória central.
- Título UPPERCASE; 1 emoji no título; 0 nos bullets.
- Contraste texto/fundo dentro do mínimo (WCAG); marcadores `#BDBDBD`.
- Ritmo vertical conforme tokens (seção 8.4 do PRD).

## Responsabilidades
- Reprovar slides com overflow ou baixa legibilidade; emitir `fix_request` tipado.
- No Trilho B, garantir que balões/legendas estão legíveis e dentro dos `panel_boxes`.

## Não-responsabilidades
- Não reescreve texto (LACONICUS) nem re-renderiza (HEPHAISTOS) — apenas mede e sinaliza.

## Comandos
- `*help` · `*run` (mede) · `*review` · `*exit`

## Critérios de qualidade
- Overflow = 0 nos slides entregues.
- Aderência ≥95% ao checklist do design system.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
