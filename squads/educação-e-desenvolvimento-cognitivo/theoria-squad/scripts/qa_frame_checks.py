#!/usr/bin/env python3
"""THEORÍA — ÁRGOS: checagens determinísticas de QA por frame (parte não-LLM).

Recebe metadados de frames amostrados (bounding boxes dos mobjects, contraste,
posição de câmera, drift de sync) e emite um QAReport com defeitos tipados e o
estágio responsável por cada conserto (alimenta o loop de Self-Healing).

Não renderiza nem mede pixels aqui (isso é feito pelo Manim/Playwright no ambiente
com render real); este módulo aplica as REGRAS de QA sobre as medições já extraídas,
de forma determinística e auditável.

Entrada (JSON):
    {
      "canvas": [1080, 1920],
      "tolerancia_sync_s": 0.15,
      "frames": [
        {"beat_id": "b1", "t": 1.2,
         "mobjects": [{"id":"vec","bbox":[x0,y0,x1,y1]}, ...],
         "min_contrast_ratio": 6.8,
         "sync_drift_s": 0.05}
      ]
    }
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Tuple

CONTRASTE_MINIMO = 4.5  # WCAG AA para texto normal
MARGEM_SEGURA = 0.04    # 4% de safe zone nas bordas


def _overlap(a: List[float], b: List[float]) -> bool:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    return not (ax1 <= bx0 or bx1 <= ax0 or ay1 <= by0 or by1 <= ay0)


def check_frame(frame: Dict[str, Any], canvas: Tuple[int, int], tol_sync: float) -> List[Dict[str, Any]]:
    w, h = canvas
    mx, my = w * MARGEM_SEGURA, h * MARGEM_SEGURA
    beat_id = frame.get("beat_id")
    defeitos: List[Dict[str, Any]] = []
    mobjects = frame.get("mobjects", [])

    # Off-canvas: bbox fora dos limites com safe zone.
    for mob in mobjects:
        x0, y0, x1, y1 = mob.get("bbox", [0, 0, 0, 0])
        if x0 < mx or y0 < my or x1 > (w - mx) or y1 > (h - my):
            defeitos.append({
                "tipo": "off_canvas", "severidade": "alta", "beat_id": beat_id,
                "detalhe": f"mobject {mob.get('id')} fora da safe zone",
                "estagio_responsavel": "STORYBOARD",
            })

    # Sobreposição: colisão de bounding boxes entre mobjects distintos.
    for i in range(len(mobjects)):
        for j in range(i + 1, len(mobjects)):
            if _overlap(mobjects[i].get("bbox", [0, 0, 0, 0]), mobjects[j].get("bbox", [0, 0, 0, 0])):
                defeitos.append({
                    "tipo": "sobreposicao", "severidade": "media", "beat_id": beat_id,
                    "detalhe": f"{mobjects[i].get('id')} colide com {mobjects[j].get('id')}",
                    "estagio_responsavel": "CINEMATOGRAPHY",
                })

    # Contraste/legibilidade.
    ratio = frame.get("min_contrast_ratio")
    if ratio is not None and float(ratio) < CONTRASTE_MINIMO:
        defeitos.append({
            "tipo": "contraste", "severidade": "media", "beat_id": beat_id,
            "detalhe": f"contraste {ratio} < mínimo {CONTRASTE_MINIMO}",
            "estagio_responsavel": "CINEMATOGRAPHY",
        })

    # Sync drift narração<->animação.
    drift = frame.get("sync_drift_s")
    if drift is not None and abs(float(drift)) > tol_sync:
        defeitos.append({
            "tipo": "sync", "severidade": "alta", "beat_id": beat_id,
            "detalhe": f"drift {drift}s > tolerância {tol_sync}s",
            "estagio_responsavel": "TIMING",
        })

    # Jitter: descontinuidade declarada entre frames.
    if frame.get("jitter"):
        defeitos.append({
            "tipo": "jitter", "severidade": "media", "beat_id": beat_id,
            "detalhe": "descontinuidade de transform entre frames",
            "estagio_responsavel": "SYNTHESIS",
        })
    return defeitos


def run_qa(payload: Dict[str, Any]) -> Dict[str, Any]:
    canvas = tuple(payload.get("canvas", [1920, 1080]))
    tol = float(payload.get("tolerancia_sync_s", 0.15))
    frames = payload.get("frames", [])
    defeitos: List[Dict[str, Any]] = []
    for frame in frames:
        defeitos.extend(check_frame(frame, canvas, tol))
    return {
        "aprovado": not defeitos,
        "frames_amostrados": len(frames),
        "n_defeitos": len(defeitos),
        "defeitos": defeitos,
        "estagios_para_reabrir": sorted({d["estagio_responsavel"] for d in defeitos}),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="ÁRGOS — QA determinístico por frame.")
    ap.add_argument("--frames", help="JSON com canvas/frames. Se ausente, lê stdin.")
    args = ap.parse_args()
    raw = open(args.frames, encoding="utf-8").read() if args.frames else sys.stdin.read()
    report = run_qa(json.loads(raw))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["aprovado"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
