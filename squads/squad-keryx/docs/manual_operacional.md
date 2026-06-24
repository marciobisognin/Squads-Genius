# KÊRYX — Manual operacional

## Ativação
- Comando: **`/keryx <pedido>`** — ex.: `/keryx gerar carrossel, 5 slides`.
- Ativação manual: leia `squad.yaml`, assuma a persona do **HEGEMON** (`agents/hegemon.md`) e
  siga o workflow `workflows/full_keryx_pipeline.yaml`.

## Input mínimo
Apenas `n_slides` é obrigatório. Tudo o mais tem default ou é sorteado por KLEROS.

```
n_slides            (obrigatório)   ex.: 5
output_format       infographic | comic | auto   (default: auto)
mode                single_theme | combined | random_mix   (default: auto via Cynefin)
domains             ["tecnologia","produtividade","gestao_vida","livros"]
seed                inteiro (reprodutibilidade)
tom                 default | mais_direto | mais_didatico
branding            slot de logo/ícone do canto (default: marca do usuário)
```

## Scripts determinísticos (Python 3.11+, stdlib)
Executar a partir de `squads/squad-keryx/`:

```bash
# Curadoria reprodutível (KLEROS)
python3 scripts/kleros_curation.py --n-slides 5 --seed 42 --mode single_theme

# Tokens do design system (fonte única da verdade)
python3 render/tokens.py

# Validar um CarouselSpec contra as regras editoriais
python3 scripts/validate_carousel_spec.py --spec examples/exemplo_carousel_spec.json

# Render Trilho A (requer jinja2 + playwright + pillow; degrada para manifesto/hash sem eles)
python3 -c "import json,sys; sys.path.insert(0,'render'); import engine; \
print(json.dumps(engine.render_carousel(json.load(open('examples/exemplo_carousel_spec.json')), {}, 42), ensure_ascii=False))"
```

## Trilhos
- **A — Infográfico:** TAXIS → LACONICUS → APELLES → HEPHAISTOS (render) → KANON → MOMUS → HITL.
- **B — Quadrinho:** RHAPSODOS → MOMUS → **HITL #1** → EIDOLON → ZEUXIS → **HITL #2** →
  HEPHAISTOS (letteriza) → KANON → **HITL final**.

## Gates obrigatórios
1. `briefing_cynefin` (HEGEMON) — classe e roteamento.
2. `qa_visual_kanon` — overflow = 0, aderência ≥95%.
3. `qa_factual_momus` — sem flags críticas.
4. `hitl_roteiro_comic` e `hitl_arte_comic` — só Trilho B.
5. `hitl_entrega` — homologação humana final (não-negociável).

## Self-healing (Turing loop)
Falhas recuperáveis (overflow, bullet longo, flag factual) geram `fix_request` tipado que
reentra no agente responsável, com `max_retries` por nó e circuit breaker → escala ao HITL.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
