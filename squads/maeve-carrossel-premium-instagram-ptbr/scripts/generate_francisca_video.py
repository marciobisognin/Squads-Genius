#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera vídeo vertical premium para Instagram com narração Francisca.

Preferência: Manim, quando importável e funcional.
Fallback confiável: Pillow + ffmpeg, adequado ao Termux/Android.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 24
VOICE = "pt-BR-FranciscaNeural"


def run(cmd, cwd=None, check=True, timeout=None):
    try:
        p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        class TimeoutResult:
            returncode = 124
            stdout = f"TIMEOUT após {timeout}s: {' '.join(map(str, cmd))}\n{exc.stdout or ''}"
        p = TimeoutResult()
    if check and p.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(map(str, cmd))}\n{p.stdout}")
    return p


def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


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
        if draw.textbbox((0, 0), test, font=fnt)[2] <= width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, width, gap=12, max_lines=None, align="left"):
    x, y = xy
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        tx = x
        if align == "center":
            bbox = draw.textbbox((0,0), line, font=fnt)
            tx = x + (width - (bbox[2]-bbox[0]))/2
        draw.text((tx, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def read_text(path: Path, default=""):
    return path.read_text(encoding="utf-8") if path.exists() else default


def extract_slides(project: Path):
    manifest_path = project / "manifest.json"
    slides = []
    if manifest_path.exists():
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            for item in data.get("slides", []):
                slides.append(str(item.get("title") or f"Slide {item.get('num','')}").strip())
        except Exception:
            pass
    if not slides:
        roteiro = read_text(project / "roteiro.md")
        for line in roteiro.splitlines():
            if line.startswith("**") and line.endswith("**"):
                slides.append(line.strip("* "))
    return slides[:8] or ["Ideia central", "Visual premium", "Resumo prático", "Ação final"]


def make_plan_and_narration(project: Path, video_dir: Path, duration: int):
    slides = extract_slides(project)
    legenda = read_text(project / "legenda.txt")
    topic = slides[0] if slides else "Carrossel premium"
    plan = f"""# Plano audiovisual — vídeo Francisca

- Formato: vertical 9:16, 1080x1920.
- Idioma: português brasileiro.
- Voz: {VOICE}.
- Estilo: lúdico premium para Instagram, com cards arredondados, pixel blocks, estrelas, setas e microinfográficos.
- Duração alvo: {duration}s.
- Tema base: {topic}.

## Sequência
1. Abertura com título grande e moldura lúdica.
2. Apresentação de 3 a 5 ideias do roteiro em cards animados.
3. Microinfográfico com barra de progresso visual.
4. Fechamento com CTA claro.

## Observação técnica
O script tenta usar Manim quando disponível. Em Termux, se Manim/Pango falhar, o fallback Pillow + ffmpeg gera o vídeo sem interromper a entrega.
"""
    compact = "; ".join(slides[:5])
    narration = f"""Olá! Eu sou a Francisca. Neste vídeo, vamos transformar {topic} em uma explicação simples, visual e prática. Observe os blocos principais: {compact}. A ideia é usar um design claro, com texto grande, elementos lúdicos e uma sequência fácil de acompanhar. Salve este conteúdo para revisar depois e compartilhe com alguém que também precisa dessa explicação."""
    video_dir.mkdir(parents=True, exist_ok=True)
    (video_dir / "plan.md").write_text(plan, encoding="utf-8")
    (video_dir / "narracao.txt").write_text(narration, encoding="utf-8")
    return slides, narration


def manim_available():
    try:
        import manim  # noqa
        return True, "manim importável"
    except Exception as e:
        return False, str(e).strip()[:300]


def write_manim_source(project: Path, video_dir: Path, slides):
    title = slides[0].replace('"', '\\"')
    bullets = slides[1:5] or slides
    bullet_code = repr(bullets)
    source = f'''from manim import *

WCONF = config
WCONF.pixel_width = 1080
WCONF.pixel_height = 1920
WCONF.frame_width = 9
WCONF.frame_height = 16

BG = "#0B1020"
CREAM = "#F7EEDC"
GOLD = "#D8B35A"
CYAN = "#62D6FF"
PINK = "#E85D9E"
MONO = "DejaVu Sans Mono"

class FranciscaInstagramVideo(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text("{title}", font=MONO, color=CREAM, font_size=48, weight=BOLD).to_edge(UP, buff=1.0)
        frame = RoundedRectangle(width=7.8, height=13.8, corner_radius=.25, color=GOLD).set_stroke(width=3)
        self.play(Create(frame), Write(title), run_time=1.4)
        self.wait(.5)
        bullets = {bullet_code}
        cards = VGroup()
        colors = [GOLD, CYAN, PINK, CREAM]
        for i, b in enumerate(bullets[:4]):
            card = RoundedRectangle(width=7.3, height=1.45, corner_radius=.22, color=colors[i%4], fill_opacity=.12)
            txt = Text(b[:52], font=MONO, color=CREAM, font_size=25).move_to(card.get_center())
            group = VGroup(card, txt)
            cards.add(group)
        cards.arrange(DOWN, buff=.35).move_to(ORIGIN).shift(DOWN*.1)
        for c in cards:
            self.play(FadeIn(c, shift=UP*.25), run_time=.8)
            self.wait(.25)
        bar = Rectangle(width=6.8, height=.16, color=CYAN, fill_opacity=1).to_edge(DOWN, buff=2.2)
        label = Text("premium • lúdico • visível", font=MONO, color=GOLD, font_size=28).next_to(bar, UP, buff=.35)
        self.play(GrowFromEdge(bar, LEFT), Write(label), run_time=1.2)
        self.wait(1.0)
        cta = Text("Salve e compartilhe", font=MONO, color=PINK, font_size=44, weight=BOLD).to_edge(DOWN, buff=.9)
        self.play(Write(cta), run_time=1.0)
        self.wait(2)
'''
    path = video_dir / "manim_scene.py"
    path.write_text(source, encoding="utf-8")
    return path


def render_with_manim(project: Path, video_dir: Path, slides):
    ok, reason = manim_available()
    if not ok or not have("manim"):
        return None, f"Manim indisponível: {reason}"
    src = write_manim_source(project, video_dir, slides)
    p = run(["manim", "-ql", str(src), "FranciscaInstagramVideo"], cwd=video_dir, check=False, timeout=45)
    if p.returncode != 0:
        return None, "Falha Manim: " + p.stdout[-800:]
    candidates = list((video_dir / "media").rglob("FranciscaInstagramVideo.mp4"))
    if not candidates:
        return None, "Manim renderizou, mas MP4 não foi encontrado"
    out = video_dir / "video_base.mp4"
    shutil.copy2(candidates[0], out)
    return out, "manim"


def gradient():
    # Otimizado para Termux: cria gradiente pequeno e amplia, evitando loop pixel-a-pixel em 1080x1920.
    sw, sh = 108, 192
    img = Image.new("RGB", (sw, sh), "#0B1020")
    px = img.load()
    for y in range(sh):
        for x in range(sw):
            t = x/sw*.25 + y/sh*.75
            px[x,y] = (int(11+38*t), int(16+24*t), int(32+70*t))
    return img.resize((W, H), Image.Resampling.BICUBIC)


def draw_frame(slides, frame_i, total_frames):
    t = frame_i / max(1, total_frames-1)
    img = gradient()
    d = ImageDraw.Draw(img, "RGBA")
    cream=(247,238,220,255); gold=(216,179,90,255); cyan=(98,214,255,255); pink=(232,93,158,255)
    titlef=font(70, True); bodyf=font(40, False); smallf=font(30, True); monof=font(28, True)
    # playful floating elements
    for k in range(18):
        x = int((80 + k*67 + math.sin(t*6+k)*45) % (W-120)) + 40
        y = int((120 + k*91 - t*240) % (H-240)) + 80
        col = [gold, cyan, pink][k%3]
        if k%3 == 0:
            d.rounded_rectangle((x,y,x+28,y+28), radius=6, fill=col)
        elif k%3 == 1:
            d.ellipse((x,y,x+30,y+30), fill=col)
        else:
            d.polygon([(x+15,y),(x+30,y+30),(x,y+30)], fill=col)
    d.rounded_rectangle((54,54,W-54,H-54), radius=42, outline=(216,179,90,210), width=4)
    d.text((74,80), "▣ ▣ ▣  vídeo premium • Francisca  ▣ ▣ ▣", font=monof, fill=(247,238,220,190))
    # select phase
    phase = min(len(slides)-1, int(t * max(1,len(slides))))
    title = slides[phase]
    y = 245
    y = draw_wrapped(d, (86,y), title, titlef, cream, 900, gap=8, max_lines=3)
    y += 42
    body = "Uma explicação em português, com visual lúdico, texto grande e elementos infográficos para Instagram."
    draw_wrapped(d, (92,y), body, bodyf, (242,222,192,255), 850, gap=14, max_lines=3)
    # central infographic card
    card_y = 1040
    d.rounded_rectangle((86, card_y, W-86, card_y+430), radius=44, fill=(255,255,255,22), outline=(255,255,255,72), width=2)
    d.text((128, card_y+42), "MICROINFOGRÁFICO", font=smallf, fill=gold)
    labels=["clareza", "ritmo", "visual", "ação"]
    for i,lab in enumerate(labels):
        yy=card_y+115+i*67
        d.text((128, yy-5), lab, font=font(30, True), fill=cream)
        maxw=560
        fillw=int(maxw*(0.35+0.6*((math.sin(t*math.pi*2+i)+1)/2)))
        d.rounded_rectangle((330, yy, 330+maxw, yy+28), radius=14, outline=(247,238,220,120), width=2)
        d.rounded_rectangle((330, yy, 330+fillw, yy+28), radius=14, fill=[gold,cyan,pink,cream][i])
    # CTA/pagination
    d.text((92,H-265), "+----+  ->  +----+  ->  +----+", font=monof, fill=(247,238,220,210))
    d.text((92,H-220), "|IDEA|      |VISUAL|     |AÇÃO|", font=monof, fill=(247,238,220,210))
    progress = int(t*100)
    d.text((W-220,H-150), f"{progress:02d}%", font=font(48, True), fill=gold)
    d.text((92,H-150), "Salve e compartilhe", font=font(44, True), fill=pink)
    return img.convert("RGB")


def render_fallback(video_dir: Path, slides, duration):
    if not have("ffmpeg"):
        raise SystemExit("ffmpeg não encontrado; não é possível gerar MP4")
    frames = video_dir / "frames"
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir(parents=True)
    total = max(1, int(duration * FPS))
    for i in range(total):
        draw_frame(slides, i, total).save(frames / f"frame_{i:04d}.png", quality=94)
    out = video_dir / "video_base.mp4"
    run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames/"frame_%04d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)])
    return out, "fallback_pillow_ffmpeg"


def generate_tts(video_dir: Path, narration: str, skip=False):
    if skip:
        return None, "TTS pulado por opção de smoke test"
    if not have("edge-tts"):
        return None, "edge-tts não encontrado"
    audio = video_dir / "narracao_francisca.mp3"
    p = run(["edge-tts", "--voice", VOICE, "--write-media", str(audio), "--text", narration], check=False, timeout=90)
    if p.returncode != 0 or not audio.exists() or audio.stat().st_size < 1000:
        if audio.exists() and audio.stat().st_size < 1000:
            try:
                audio.unlink()
            except Exception:
                pass
        return None, "Falha edge-tts: " + p.stdout[-500:]
    return audio, VOICE


def mux(video_dir: Path, video: Path, audio: Path|None):
    final = video_dir / "final_francisca.mp4"
    if audio and audio.exists():
        run(["ffmpeg", "-y", "-i", str(video), "-i", str(audio), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(final)])
    else:
        shutil.copy2(video, final)
    preview = video_dir / "preview.png"
    run(["ffmpeg", "-y", "-i", str(final), "-vf", "select=eq(n\\,24)", "-frames:v", "1", "-update", "1", str(preview)], check=False)
    return final, preview


def probe(path: Path):
    if not have("ffprobe"):
        return {}
    p = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,duration", "-of", "json", str(path)], check=False)
    try:
        return json.loads(p.stdout).get("streams", [{}])[0]
    except Exception:
        return {}


def main():
    ap = argparse.ArgumentParser(description="Gera vídeo vertical com voz Francisca para Instagram")
    ap.add_argument("--project", required=True, help="Pasta final do carrossel")
    ap.add_argument("--duration", type=int, default=18, help="Duração alvo em segundos")
    ap.add_argument("--skip-tts", action="store_true", help="Não gerar TTS; útil para smoke test offline")
    ap.add_argument("--force-fallback", action="store_true", help="Pula Manim e usa fallback Pillow + ffmpeg")
    args = ap.parse_args()
    project = Path(args.project)
    if not project.exists():
        raise SystemExit(f"Pasta do projeto não encontrada: {project}")
    video_dir = project / "video"
    slides, narration = make_plan_and_narration(project, video_dir, args.duration)
    if args.force_fallback:
        video, mode = None, "Manim pulado por --force-fallback"
        manim_note = mode
    else:
        video, mode = render_with_manim(project, video_dir, slides)
        manim_note = mode
    if video is None:
        manim_note = mode
        video, mode = render_fallback(video_dir, slides, args.duration)
    audio, tts_note = generate_tts(video_dir, narration, skip=args.skip_tts)
    final, preview = mux(video_dir, video, audio)
    info = {
        "ok": True,
        "generated_at": datetime.now().isoformat(),
        "language": "pt-BR",
        "voice_requested": VOICE,
        "tts_status": tts_note,
        "render_mode": mode,
        "manim_status": manim_note,
        "format": "vertical 9:16 Instagram",
        "final": str(final),
        "preview": str(preview),
        "probe": probe(final),
    }
    (video_dir / "video_manifest.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(info, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
