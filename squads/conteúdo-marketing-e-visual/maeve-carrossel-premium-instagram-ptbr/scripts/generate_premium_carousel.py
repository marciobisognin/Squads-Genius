#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gerador operacional do squad Maeve Carrossel Premium Instagram PT-BR.

Entrada: briefing YAML simples.
Saída: HTML + PNG por slide, roteiro.md, legenda.txt, hashtags.txt e manifest.json.
"""
from __future__ import annotations

import argparse
import json
import re
import textwrap
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception as exc:  # pragma: no cover
    raise SystemExit("Pillow é necessário para gerar PNG: pip install pillow") from exc

W, H = 1080, 1350


def parse_simple_yaml(path: Path) -> dict:
    data = {}
    if not path.exists():
        raise SystemExit(f"Briefing não encontrado: {path}")
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip().strip('"').strip("'")
        if v.isdigit():
            v = int(v)
        data[k.strip()] = v
    return data


def slugify(text: str) -> str:
    text = text.lower()
    repl = {"á":"a","à":"a","ã":"a","â":"a","é":"e","ê":"e","í":"i","ó":"o","ô":"o","õ":"o","ú":"u","ç":"c"}
    for a,b in repl.items():
        text = text.replace(a,b)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "carrossel"


def font(size: int, bold: bool=False):
    candidates = [
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf" if bold else "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/system/fonts/Roboto-Bold.ttf" if bold else "/system/fonts/Roboto-Regular.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textbbox((0,0), test, font=fnt)[2] <= width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, width, line_gap=10, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def gradient_bg():
    img = Image.new("RGB", (W, H), "#0B1020")
    px = img.load()
    for y in range(H):
        for x in range(W):
            t = (x/W*0.35 + y/H*0.65)
            r = int(11 + 35*t)
            g = int(16 + 20*t)
            b = int(32 + 55*t)
            px[x,y] = (r,g,b)
    return img


def slide_plan(brief: dict) -> list[dict]:
    tema = brief.get("tema", "Tema solicitado pelo usuário")
    objetivo = brief.get("objetivo", "explicar com clareza")
    publico = brief.get("publico", "público geral")
    cta = brief.get("cta", "Salve este carrossel para consultar depois.")
    n = int(brief.get("slides", 8) or 8)
    n = max(5, min(n, 14))
    base = [
        ("O guia visual", f"{tema}: uma explicação premium, simples e prática para {publico}."),
        ("Por que isso importa?", f"A ideia central é transformar {tema} em passos claros, sem ruído e sem complicação."),
        ("Mapa rápido", "Veja o caminho: contexto → conceito → exemplo → aplicação → ação."),
        ("A lógica por trás", f"{objetivo.capitalize()}: cada bloco visual resolve uma dúvida de cada vez."),
        ("Exemplo prático", "Use o modelo: observe, pergunte, compare, registre e revise."),
        ("O erro comum", "Não confunda aparência bonita com compreensão. O visual precisa explicar."),
        ("Checklist final", "Clareza, ritmo, contraste, hierarquia e uma ação concreta ao final."),
        ("Agora é com você", cta),
    ]
    if n > 8:
        extras = [
            ("Camada 1", "Defina o problema antes de escolher a ferramenta."),
            ("Camada 2", "Converta conceitos abstratos em formas, fluxos e comparações."),
            ("Camada 3", "Use dados, setas e ícones apenas quando ajudarem a decidir."),
            ("Aplicação real", "Transforme a explicação em uma próxima ação mensurável."),
            ("Resumo premium", "Menos enfeite, mais direção visual e significado."),
            ("Próximo passo", "Reutilize o método em novos temas e refine com feedback."),
        ]
        base = base[:6] + extras[:n-8] + base[6:]
    return [{"num": i+1, "title": t, "body": b} for i,(t,b) in enumerate(base[:n])]


def html_for_slide(slide, total, brief):
    ascii_bar = "▣ ▣ ▣  ::  ║ premium grid ║  ::  ▣ ▣ ▣"
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Slide {slide['num']:02d}</title>
<style>
  :root {{ --bg:#0B1020; --ink:#F7EEDC; --gold:#D8B35A; --cyan:#62D6FF; --pink:#E85D9E; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); font-family: Inter, Manrope, Arial, sans-serif; }}
  .slide {{ width:1080px; height:1350px; padding:74px; color:var(--ink);
    background: radial-gradient(circle at 18% 12%, rgba(216,179,90,.26), transparent 28%),
                radial-gradient(circle at 86% 78%, rgba(232,93,158,.20), transparent 30%),
                linear-gradient(145deg,#0B1020,#111B35 58%,#21152D);
    position:relative; overflow:hidden; }}
  .pixel {{ position:absolute; inset:38px; border:2px solid rgba(216,179,90,.42); box-shadow:0 0 0 8px rgba(255,255,255,.025); }}
  .ascii {{ color:rgba(247,238,220,.55); letter-spacing:3px; font: 700 22px monospace; }}
  .eyebrow {{ color:var(--gold); font-weight:800; letter-spacing:4px; text-transform:uppercase; margin-top:58px; }}
  h1 {{ font-size:86px; line-height:.94; max-width:860px; margin:36px 0 26px; letter-spacing:-3px; }}
  .body {{ font-size:38px; line-height:1.22; max-width:820px; color:#F2DEC0; }}
  .card {{ position:absolute; left:74px; right:74px; bottom:145px; border:1px solid rgba(255,255,255,.16);
    border-radius:34px; padding:30px; background:rgba(255,255,255,.065); backdrop-filter:blur(8px); }}
  .metric {{ display:flex; gap:18px; align-items:center; font-size:28px; }}
  .bar {{ height:18px; flex:1; border-radius:30px; background:linear-gradient(90deg,var(--gold),var(--cyan),var(--pink)); }}
  .page {{ position:absolute; right:74px; bottom:72px; color:var(--gold); font-weight:800; font-size:28px; }}
</style>
</head>
<body><main class="slide">
<div class="pixel"></div>
<div class="ascii">{ascii_bar}</div>
<div class="eyebrow">{brief.get('tema','carrossel premium')}</div>
<h1>{slide['title']}</h1>
<p class="body">{slide['body']}</p>
<section class="card"><div class="metric"><span>INFOGRÁFICO</span><div class="bar"></div><span>PIXEL + ASCII</span></div></section>
<div class="page">{slide['num']:02d}/{total:02d}</div>
</main></body></html>'''


def draw_slide(slide, total, brief, out_png):
    img = gradient_bg()
    draw = ImageDraw.Draw(img)
    cream = "#F7EEDC"; gold = "#D8B35A"; cyan = "#62D6FF"; pink = "#E85D9E"; muted = "#F2DEC0"
    # ornamental/pixel frame
    draw.rounded_rectangle((38,38,W-38,H-38), radius=30, outline=(216,179,90), width=3)
    for x in range(72, W-72, 42):
        color = gold if (x//42)%2 else cyan
        draw.rectangle((x, 58, x+16, 74), fill=color)
        draw.rectangle((x, H-74, x+16, H-58), fill=color)
    for y in range(130, H-130, 52):
        draw.rectangle((55, y, 70, y+15), fill=pink if (y//52)%2 else gold)
        draw.rectangle((W-70, y, W-55, y+15), fill=cyan if (y//52)%2 else gold)

    mono = font(24, True); small = font(25, True); titlef = font(86, True); bodyf = font(39, False); labelf = font(28, True)
    ascii_bar = "▣ ▣ ▣  ::  ║ premium grid ║  ::  ▣ ▣ ▣"
    draw.text((74,78), ascii_bar, font=mono, fill=(247,238,220))
    draw.text((74,170), str(brief.get('tema','carrossel premium')).upper()[:52], font=small, fill=gold)
    y = draw_wrapped(draw, (74,245), slide['title'], titlef, cream, 860, line_gap=4, max_lines=3)
    y += 22
    draw_wrapped(draw, (78,y), slide['body'], bodyf, muted, 820, line_gap=12, max_lines=4)

    # infographic card
    card = (74, H-365, W-74, H-145)
    draw.rounded_rectangle(card, radius=34, fill=(28,35,62), outline=(255,255,255), width=2)
    draw.text((112, H-326), "INFOGRÁFICO VISUAL", font=labelf, fill=gold)
    # bars
    bx, by = 112, H-270
    labels = ["clareza", "ritmo", "visual"]
    widths = [560, 690, 620]
    colors = [gold, cyan, pink]
    for i,(lab,wid,col) in enumerate(zip(labels,widths,colors)):
        yy = by+i*50
        draw.text((bx, yy-8), lab, font=font(24, True), fill=cream)
        draw.rounded_rectangle((bx+150, yy, bx+150+wid, yy+22), radius=11, fill=col)
        draw.rounded_rectangle((bx+150, yy, bx+780, yy+22), radius=11, outline=(247,238,220), width=1)
    # ASCII mini diagram
    draw.text((650, H-326), "+----+  ->  +----+", font=mono, fill=cream)
    draw.text((650, H-288), "|IDEA|      |AÇÃO|", font=mono, fill=cream)
    draw.text((650, H-250), "+----+  ->  +----+", font=mono, fill=cream)
    draw.text((W-170, H-98), f"{slide['num']:02d}/{total:02d}", font=font(30, True), fill=gold)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_png, quality=95)


def main():
    ap = argparse.ArgumentParser(description="Gera carrossel premium Instagram em pt-BR")
    ap.add_argument("--brief", required=True, help="Arquivo YAML de briefing")
    ap.add_argument("--output", required=True, help="Pasta final de saída")
    args = ap.parse_args()
    brief = parse_simple_yaml(Path(args.brief))
    out = Path(args.output)
    slides_dir = out / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)
    slides = slide_plan(brief)
    total = len(slides)

    roteiro = [f"# Roteiro — {brief.get('tema','Carrossel premium')}\n"]
    manifest = {"generated_at": datetime.now().isoformat(), "language":"pt-BR", "size":"1080x1350", "slides": []}
    for s in slides:
        html = html_for_slide(s, total, brief)
        html_path = slides_dir / f"slide-{s['num']:02d}.html"
        png_path = slides_dir / f"slide-{s['num']:02d}.png"
        html_path.write_text(html, encoding="utf-8")
        draw_slide(s, total, brief, png_path)
        roteiro.append(f"## Slide {s['num']:02d}\n\n**{s['title']}**\n\n{s['body']}\n")
        manifest["slides"].append({"num":s['num'], "html":str(html_path.name), "png":str(png_path.name), "title":s['title']})

    (out / "roteiro.md").write_text("\n".join(roteiro), encoding="utf-8")
    legenda = f"""{brief.get('tema','Este tema')} pode ficar muito mais claro quando vira mapa visual.\n\nNeste carrossel, a ideia foi organizar o conteúdo em blocos simples, com hierarquia, ritmo e exemplos visuais para facilitar a compreensão.\n\n{brief.get('cta','Salve para consultar depois e compartilhe com alguém que precisa ver isso.')}\n"""
    (out / "legenda.txt").write_text(legenda, encoding="utf-8")
    tags_base = ["#carrossel", "#instagram", "#designpremium", "#infografico", "#conteudodigital", "#ptbr", "#visualdesign", "#educacaodigital", "#criacaodeconteudo"]
    tema_tags = ["#" + slugify(x) for x in str(brief.get('tema','')).split()[:4] if len(x) > 3]
    (out / "hashtags.txt").write_text(" ".join(tags_base + tema_tags) + "\n", encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "output": str(out), "slides": total}, ensure_ascii=False))

if __name__ == "__main__":
    main()
