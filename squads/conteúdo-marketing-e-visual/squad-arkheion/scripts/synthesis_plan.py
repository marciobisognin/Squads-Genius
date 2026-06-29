#!/usr/bin/env python3
"""synthesis_plan — plano de montagem do master (SÝNTHESIS, PRD §8.4).

Recebe N CENA-10 já renderizadas/aprovadas por KÁNŌN e emite o plano determinístico
de montagem: ordem de concatenação com corte seco + glitch de 1–2 frames, passe global
de grão/scanline para continuidade, mix de áudio com silêncios estratégicos (silêncio
antes do último beat) e card de encerramento. Emite também os comandos FFmpeg.

Uso:
    python3 scripts/synthesis_plan.py --cenas cena01.mp4 cena02.mp4 ... --encerramento escuro
    python3 scripts/synthesis_plan.py --n 6 --encerramento branco   # plano sintético
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arkheion import canon  # noqa: E402


def plano_montagem(cenas: List[str], encerramento: str = "escuro") -> Dict[str, Any]:
    if encerramento not in canon.ENCERRAMENTOS:
        raise ValueError(f"encerramento inválido: {encerramento}")
    n = len(cenas)
    if not 3 <= n <= 9:
        raise ValueError(f"nº de cenas {n} fora de 3..9")
    dur_total = n * canon.TIMING.cena_s
    # silêncio estratégico antes do último beat (PRD §2.8 / §17.3)
    silencio_offset = (n - 1) * canon.TIMING.cena_s - 0.8
    cortes = [
        {"de": i, "para": i + 1, "tipo": "corte_seco", "glitch_frames": canon.TIMING.glitch_frames[1]}
        for i in range(n - 1)
    ]
    return {
        "n_cenas": n,
        "duracao_total_s": dur_total,
        "fps": canon.TIMING.fps,
        "resolucao_master": list(canon.RES_MASTER),
        "resolucao_entrega": list(canon.RES_ENTREGA),
        "ordem": cenas,
        "cortes": cortes,
        "passe_global": "grao+scanline (continuidade temporal entre cortes)",
        "audio": {
            "bed": "drone_industrial_loop",
            "silencios_s": [round(silencio_offset, 2)],
            "locucao": "opcional (default: ausente — o silêncio é parte da estética)",
        },
        "encerramento": encerramento,
        "comandos": _comandos(cenas, dur_total),
    }


def _comandos(cenas: List[str], dur_total: int) -> Dict[str, str]:
    concat_inputs = " ".join(f"-i {c}" for c in cenas)
    filtro_concat = "".join(f"[{i}:v]" for i in range(len(cenas))) + f"concat=n={len(cenas)}:v=1:a=0[v]"
    grade = canon.GRADE_FFMPEG
    return {
        "concat": f"ffmpeg -y {concat_inputs} -filter_complex \"{filtro_concat}\" -map \"[v]\" master_raw.mp4",
        "passe_global": f"ffmpeg -y -i master_raw.mp4 -vf \"{grade}\" -c:v libx264 -crf 18 master_2160.mp4",
        "entrega": (
            f"ffmpeg -y -i master_2160.mp4 -vf scale={canon.RES_ENTREGA[0]}:{canon.RES_ENTREGA[1]} "
            f"-c:v libx264 -pix_fmt yuv420p -crf 18 entrega_1080.mp4"
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Plano de montagem do master ARKHEION.")
    ap.add_argument("--cenas", nargs="*", help="paths das CENA-10 em ordem")
    ap.add_argument("--n", type=int, help="nº de cenas (gera plano sintético)")
    ap.add_argument("--encerramento", default="escuro", choices=sorted(canon.ENCERRAMENTOS))
    args = ap.parse_args()
    if args.cenas:
        cenas = args.cenas
    elif args.n:
        cenas = [f"cena{i:02d}.mp4" for i in range(1, args.n + 1)]
    else:
        cenas = [f"cena{i:02d}.mp4" for i in range(1, 7)]
    plano = plano_montagem(cenas, args.encerramento)
    print(json.dumps(plano, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
