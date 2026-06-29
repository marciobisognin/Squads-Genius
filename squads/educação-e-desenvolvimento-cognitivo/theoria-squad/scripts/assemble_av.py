#!/usr/bin/env python3
"""THEORÍA — HARMONIA: assembly determinístico (mux vídeo+áudio) e manifesto.

Alinha o vídeo (Manim) e o áudio (EChÓ) pelos timestamps da linha do tempo mestra,
monta o comando FFmpeg de mux/encode no formato/aspecto alvo em 1080p e gera o
manifesto de artefatos para auditoria (PRD §9.4 e §13.1 RF7).

Não executa o FFmpeg (isso é feito no ambiente de render); emite o PLANO de mux
determinístico e o manifesto. O mesmo input sempre gera o mesmo plano/manifesto.

Uso:
    python3 scripts/assemble_av.py --timeline timeline.json --formato 9:16 \
        --video media/scene.mp4 --audio media/narracao.wav --out outputs/final.mp4
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from typing import Any, Dict, List

RESOLUCOES = {"16:9": [1920, 1080], "9:16": [1080, 1920], "1:1": [1080, 1080]}


def _hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def build_mux_plan(video: str, audio: str, out: str, formato: str, crf: int = 18) -> Dict[str, Any]:
    if formato not in RESOLUCOES:
        raise ValueError(f"formato inválido: {formato!r}")
    w, h = RESOLUCOES[formato]
    cmd = (
        f"ffmpeg -y -i {video} -i {audio} "
        f"-vf scale={w}:{h}:force_original_aspect_ratio=decrease,"
        f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2 "
        f"-c:v libx264 -pix_fmt yuv420p -crf {crf} -r 60 "
        f"-c:a aac -b:a 192k -shortest {out}"
    )
    return {"formato": formato, "resolucao": [w, h], "comando_ffmpeg": cmd, "saida": out}


def build_manifest(job_id: str, timeline: Dict[str, Any], mux: Dict[str, Any],
                   artefatos: List[str]) -> Dict[str, Any]:
    manifest = {
        "job_id": job_id,
        "duracao_total_s": timeline.get("duracao_total_s"),
        "n_beats": timeline.get("n_beats"),
        "formato": mux["formato"],
        "resolucao": mux["resolucao"],
        "saida_final": mux["saida"],
        "artefatos_intermediarios": artefatos,
        "timeline_hash": _hash(timeline),
        "mux_hash": _hash(mux),
    }
    manifest["manifest_hash"] = _hash(manifest)
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description="HARMONIA — plano de mux + manifesto.")
    ap.add_argument("--timeline", required=True, help="JSON da timeline mestra (CHRONOS).")
    ap.add_argument("--formato", default="16:9", choices=list(RESOLUCOES))
    ap.add_argument("--video", default="media/videos/scene.mp4")
    ap.add_argument("--audio", default="media/audio/narracao.wav")
    ap.add_argument("--out", default="outputs/theoria_final.mp4")
    ap.add_argument("--job-id", default="theoria-job")
    ap.add_argument("--crf", type=int, default=18)
    args = ap.parse_args()

    timeline = json.loads(open(args.timeline, encoding="utf-8").read())
    mux = build_mux_plan(args.video, args.audio, args.out, args.formato, args.crf)
    artefatos = [
        "brief.json", "insight.json", "arco_didatico.json", "roteiro.json",
        "timeline.json", "scene_graphs.json", "scene.py", "qa_report.json",
    ]
    manifest = build_manifest(args.job_id, timeline, mux, artefatos)
    print(json.dumps({"mux": mux, "manifesto": manifest}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
