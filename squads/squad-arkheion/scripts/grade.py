#!/usr/bin/env python3
"""grade — cadeia de color grading FFmpeg determinística (TÉKTŌN, PRD §2.6 / §8.2).

Emite a linha de comando FFmpeg que impõe o look canônico sobre qualquer footage,
independentemente da variância do gerador de vídeo. A marca é code-enforced: o mesmo
filtro produz sempre o mesmo look. Inclui o overlay de scanlines (geq) como passe
separado, conforme o Cânone.

Uso:
    python3 scripts/grade.py --in footage.mp4 --out cena_graded.mp4
    python3 scripts/grade.py --chain          # imprime só a cadeia de filtros
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arkheion import canon  # noqa: E402

# Scanlines sutis via geq (overlay separado, PRD §2.6/§8.2): linhas pares levemente
# escurecidas — efeito CRT discreto.
SCANLINES_GEQ = "geq=lum='lum(X,Y)*(0.96+0.04*mod(Y,2))':cb='cb(X,Y)':cr='cr(X,Y)'"


def build_filtro() -> str:
    """Cadeia completa: grade canônica + scanlines."""
    return f"{canon.GRADE_FFMPEG},{SCANLINES_GEQ}"


def build_cmd(entrada: str, saida: str, fps: int = None) -> str:
    fps = fps or canon.TIMING.fps
    return (
        f"ffmpeg -y -i {entrada} "
        f"-vf \"{build_filtro()}\" "
        f"-r {fps} -c:v libx264 -pix_fmt yuv420p -crf 18 -an {saida}"
    )


def descrever() -> Dict[str, str]:
    return {
        "grade": canon.GRADE_FFMPEG,
        "scanlines": SCANLINES_GEQ,
        "cadeia_completa": build_filtro(),
        "fps": str(canon.TIMING.fps),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Cadeia de grade FFmpeg canônica.")
    ap.add_argument("--in", dest="entrada", help="footage de entrada")
    ap.add_argument("--out", dest="saida", help="vídeo graded de saída")
    ap.add_argument("--chain", action="store_true", help="imprime apenas a cadeia de filtros")
    args = ap.parse_args()
    if args.chain:
        print(build_filtro())
    elif args.entrada and args.saida:
        print(build_cmd(args.entrada, args.saida))
    else:
        print(json.dumps(descrever(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
