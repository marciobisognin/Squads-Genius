#!/usr/bin/env python3
"""THEORÍA — Render config: RenderJob → comandos Manim/FFmpeg determinísticos.

Traduz o formato escolhido em resolução 1080p + FPS e monta a linha de comando do
Manim CLI e do encode FFmpeg. Tudo parametrizado por RenderJob — reproduzível
(PRD §9.3).

Uso:
    python3 scripts/render_config.py --formato 9:16 --scene-file outputs/scene.py --class EulerIdentity
    python3 scripts/render_config.py --job render_job.json
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, Tuple

RESOLUCOES: Dict[str, Tuple[int, int]] = {
    "16:9": (1920, 1080),
    "9:16": (1080, 1920),
    "1:1": (1080, 1080),
}


def resolucao_para_formato(formato: str) -> Tuple[int, int]:
    if formato not in RESOLUCOES:
        raise ValueError(f"formato inválido: {formato!r} (use {sorted(RESOLUCOES)})")
    return RESOLUCOES[formato]


def build_manim_cmd(scene_file: str, class_name: str, formato: str, fps: int = 60, preview: bool = False) -> str:
    """Linha de comando do Manim CLI. preview=True usa baixa qualidade para QA barato."""
    w, h = resolucao_para_formato(formato)
    qualidade = "-ql" if preview else "-qh"
    res = f"{w},{h}" if not preview else f"{w // 2},{h // 2}"
    fps_eff = 30 if preview else fps
    return f"manim {qualidade} --resolution {res} --fps {fps_eff} {scene_file} {class_name}"


def build_ffmpeg_cmd(video_in: str, audio_in: str, video_out: str, crf: int = 18) -> str:
    """Encode final H.264 yuv420p (compatível com web/social)."""
    return (
        f"ffmpeg -y -i {video_in} -i {audio_in} "
        f"-c:v libx264 -pix_fmt yuv420p -crf {crf} "
        f"-c:a aac -b:a 192k -shortest {video_out}"
    )


def build_job(formato: str, scene_file: str, class_name: str, seed: int = 42,
              manim_lock: str = "0.18.1", crf: int = 18, fps: int = 60) -> Dict[str, Any]:
    w, h = resolucao_para_formato(formato)
    return {
        "formato": formato,
        "resolucao": [w, h],
        "fps": fps,
        "qualidade": "-qh",
        "seed": seed,
        "manim_version_lock": manim_lock,
        "crf": crf,
        "comandos": {
            "preview_qa": build_manim_cmd(scene_file, class_name, formato, fps, preview=True),
            "render_full": build_manim_cmd(scene_file, class_name, formato, fps, preview=False),
            "encode": build_ffmpeg_cmd("media/videos/scene.mp4", "media/audio/narracao.wav",
                                       f"outputs/theoria_{formato.replace(':', 'x')}.mp4", crf),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera comandos de render determinísticos.")
    ap.add_argument("--job", help="JSON RenderJob completo (sobrescreve flags).")
    ap.add_argument("--formato", default="16:9", choices=list(RESOLUCOES))
    ap.add_argument("--scene-file", default="outputs/theoria_scene.py")
    ap.add_argument("--class", dest="class_name", default="TheoriaScene")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--crf", type=int, default=18)
    args = ap.parse_args()

    if args.job:
        cfg = json.loads(open(args.job, encoding="utf-8").read())
        job = build_job(
            cfg.get("formato", "16:9"),
            cfg.get("scene_file", args.scene_file),
            cfg.get("class_name", args.class_name),
            int(cfg.get("seed", 42)),
            cfg.get("manim_version_lock", "0.18.1"),
            int(cfg.get("crf", 18)),
            int(cfg.get("fps", 60)),
        )
    else:
        job = build_job(args.formato, args.scene_file, args.class_name, args.seed, crf=args.crf)

    print(json.dumps(job, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
