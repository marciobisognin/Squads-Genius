# KÊRYX — Design system (réplica fiel do padrão)

Fonte única da verdade: `render/tokens.py`. O estilo baoyu modula a **estética**; os tokens
abaixo governam a **identidade** (branding, tipografia, acento) em qualquer estilo.

## Canvas & grid
- Canvas 1080×1350 px (4:5) · margem 72 px · 2 colunas · gutter 64 px.
- Divisória central vertical 1.5 px `#1A1A1A` (~18% opacidade).
- Branding: top-right, 96×96 px, slot configurável (marca do usuário).

## Tipografia
| Papel | Família | Peso | Tamanho | Caso | Cor |
|---|---|---|---|---|---|
| Título | Poppins/Archivo | 800 | 40–46 px | UPPERCASE | `#111111` |
| Header | Poppins/Archivo | 700 | 24–28 px | UPPERCASE | `#111111` |
| Bullet | Inter/Source Sans | 400 | 21–23 px | sentence | `#2B2B2B` |
| Marcador | — | — | 8 px ● | — | `#BDBDBD` |

Fontes embutidas no build (sem rede em runtime → determinismo).

## Cores
`bg #FFFFFF` (off-white `#FAFAF8`) · `ink #111111` · `body #2B2B2B` · `muted #BDBDBD` ·
`accent` por tema (bateria `#3FB950`, calendário `#E5484D`, …).

## Ritmo vertical
title→1º header 40px · entre seções 36px · header→bullets 16px · line-height 1.35 · entre bullets 12px.

## Regras editoriais (o "molho")
- Bullet = imperativo curto (3–7 palavras, máx. 2 linhas).
- Header = comando/substantivo em UPPERCASE.
- 1 gancho de cotidiano por slide; 1 emoji no título; 0 nos bullets; PT-BR sem jargão.

## Biblioteca baoyu (vocabulário adotado, reimplementado — MIT)
- **`baoyu-infographic`**: `layout × estilo` (cada layout = template Jinja2; cada estilo = tokens CSS).
- **`baoyu-comic`**: `arte × tom × layout × preset` (diretrizes de prompt + letterização vetorial).
- Default do Trilho A: `dense-modules × minimalist` (= cards de referência).

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
