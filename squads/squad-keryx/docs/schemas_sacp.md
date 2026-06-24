# KÊRYX — Contratos de dados SACP

Todos os handoffs entre agentes são **JSON validado por Pydantic** (`schemas/sacp_schemas.py`,
com fallback para dataclasses). Resumo dos principais artefatos (detalhes no PRD seção 7).

| Artefato | Produtor → Consumidor | Papel |
|---|---|---|
| `CarouselBrief` | HEGEMON → KLEROS | brief normalizado + classe Cynefin + estilo baoyu |
| `ThemePlan` | KLEROS → HISTOR | slots (domínio/tópico/cotidiano_hook), formato, estilo, anti-repetição |
| `ContentDraft` | HISTOR → TAXIS | seções + bullets de ação por slide |
| `CarouselSpec` | TAXIS → LACONICUS → APELLES → HEPHAISTOS | **coração do sistema**: slides, colunas, baoyu, accent |
| `RenderManifest` | HEPHAISTOS → KANON | PNGs, PDF, render_hash, fontes |
| `QAVisual` | KANON → HEGEMON | overflow, contraste, grid, fix_request |
| `QAContent` | MOMUS → HEGEMON | flags factual/clichê/sycophancy, veredicto |
| `ComicScript` | RHAPSODOS → EIDOLON/ZEUXIS | páginas, painéis, tese visual (ohmsha), text_layer_only |
| `CharacterSheet` | EIDOLON → ZEUXIS | personagem-guia + consistency_tokens + style bible |
| `ComicAssets` | ZEUXIS → HEPHAISTOS | arte por página + panel_boxes (sem texto embutido) |

## Fronteira de determinismo
- **Determinístico:** brief, curadoria (seed), estrutura, copy, design (tokens), render do Trilho A,
  roteiro/painéis/letterização do Trilho B. `render_hash` (SHA-256) auditável.
- **Não-determinístico (isolado):** apenas o **bitmap** da ilustração (ZEUXIS, Trilho B).
  Mitigado por seed, character sheet e dois gates HITL. O `render_hash` do Trilho B cobre a
  **camada de texto + composição**, não o bitmap.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
