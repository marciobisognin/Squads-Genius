# HEPHAISTOS — Render Determinístico & Letterização

> Étimo: Ἥφαιστος (*Hḗphaistos*), Hefesto, o ferreiro/forjador dos deuses.
> Cynefin/tier: **Determinístico (Python puro, sem LLM)**
> Trilho: A (render completo) e B (letterização vetorial).

## Missão
**Forjar os pixels finais sem IA.** No Trilho A, renderiza `CarouselSpec+art` em PNG 1080×1350 e
PDF via Jinja2 → HTML/CSS → Playwright (Chromium headless). No Trilho B, **lettera**: sobrepõe
balões e legendas vetoriais nítidas nos `panel_boxes`, usando o **texto exato** do `ComicScript`.
Garante reprodutibilidade: mesma `seed`+`spec`+`tokens` ⇒ mesmo `render_hash` (SHA-256).

## Entradas
- Trilho A: `CarouselSpec + art` + `render/tokens.py`.
- Trilho B: `ComicAssets` (arte) + `ComicScript` (texto) → letterização.

## Saída — `RenderManifest` (JSON)
```json
{
  "carousel_id": "uuid",
  "slides": [
    {"slide_index": 1, "png_path": "outputs/infographic/slide_01.png",
     "width": 1080, "height": 1350, "render_hash": "sha256:..."}
  ],
  "pdf_path": "outputs/infographic/carrossel.pdf",
  "fonts_used": ["Poppins-Bold", "Inter-Regular"],
  "deterministic": true
}
```

## Pipeline Trilho A
`CarouselSpec` → Jinja2 (template = `baoyu.layout`) + tokens CSS (`baoyu.style`) →
Playwright viewport 1080×1350 (`deviceScaleFactor` opc.) → `screenshot()` PNG por slide →
PDF multipágina (Pillow/img2pdf). Ver esqueleto em `scripts/render_engine.py`.

## Pipeline Trilho B (letterização)
`ComicAssets` + `ComicScript` → desenha balões/legendas (SVG/HTML→Playwright) nos `panel_boxes`
→ compõe páginas → PDF. **Determinístico:** roteiro, painéis, posição/conteúdo dos balões,
tipografia e montagem. **Não-determinístico (isolado):** apenas o bitmap da ilustração (ZEUXIS).
O `render_hash` aplica-se à **camada de texto + composição**, não ao bitmap da arte.

## Por que é auditável
- Fontes **embutidas** (sem rede em runtime).
- Nenhuma decisão estética fica a cargo do LLM no momento do desenho.
- `render_hash` registrado em cada manifesto.

## Responsabilidades
- Renderizar todos os slides/páginas e montar o PDF.
- Emitir `OverflowSignal` quando KANON detectar estouro (entra no loop de auto-fit).
- Letterizar Trilho B com texto 100% nítido e correto.

## Não-responsabilidades
- Não decide conteúdo, estilo ou layout (recebe pronto).
- Não gera ilustração (ZEUXIS).

## Comandos
- `*help` · `*run` (render) · `*letter` (letteriza Trilho B) · `*hash` (recalcula render_hash) · `*exit`

## Critérios de qualidade
- Reprodutibilidade pixel-a-pixel (Trilho A): mesma seed+spec ⇒ mesmo hash.
- Texto dos balões (Trilho B) idêntico ao `ComicScript`.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
