#!/usr/bin/env python3
"""hud_plan — plano de animação do HUD frame-a-frame (TÉKTŌN Trilho A, PRD §8.1).

Calcula deterministicamente, para uma CENA-10, o cronograma de frames: fade do preto,
entrada do título, glitch RGB, digitação a 20–30 cps, piscar do cursor e (no beat de
prova) crescimento da barra/contagem numérica. Não renderiza pixels — emite o plano
que o renderizador (HTML/CSS + Playwright) consome frame a frame.

Uso:
    python3 scripts/hud_plan.py --texto "ACESSO RESTRITO|3 NÍVEIS DE SIGILO" --beat 2
    python3 scripts/hud_plan.py --texto "98% DE FALHAS" --beat 5 --dataviz
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arkheion import canon  # noqa: E402


def _s_para_frame(segundos: float) -> int:
    return round(segundos * canon.TIMING.fps)


def plano_hud(linhas: List[str], beat: int, dataviz: bool = False,
              cps: int = canon.VELOCIDADE_DIGITACAO_CPS) -> Dict[str, Any]:
    t = canon.TIMING
    total_frames = t.frames_por_cena
    titulo_entrada_f = _s_para_frame(sum(t.titulo_entrada_s) / 2)  # ponto médio da faixa
    glitch_f = t.glitch_frames[1]  # 2 frames (limite superior canônico)
    cursor_periodo_f = _s_para_frame(sum(t.cursor_blink_s) / 2)

    eventos: List[Dict[str, Any]] = [
        {"frame": 0, "evento": "fade_do_preto", "dur_frames": titulo_entrada_f},
        {"frame": 0, "evento": "glitch_rgb_titulo", "dur_frames": glitch_f},
        {"frame": titulo_entrada_f, "evento": "titulo_visivel"},
    ]

    # Digitação: revela substring por frame a `cps`. frames por caractere = fps/cps.
    frames_por_char = max(1, round(t.fps / cps))
    cursor_frame = titulo_entrada_f + glitch_f
    for linha in linhas:
        for ch_idx in range(1, len(linha) + 1):
            eventos.append({
                "frame": cursor_frame,
                "evento": "digita",
                "conteudo": linha[:ch_idx],
            })
            cursor_frame += frames_por_char
        eventos.append({"frame": cursor_frame, "evento": "quebra_linha"})

    if dataviz or beat in (5,):
        eventos.append({
            "frame": cursor_frame,
            "evento": "dataviz_anima",
            "modo": "barra_esquerda_para_direita+contagem_rapida",
            "dur_frames": total_frames - cursor_frame,
        })

    return {
        "beat": beat,
        "fps": t.fps,
        "total_frames": total_frames,
        "cps": cps,
        "frames_por_char": frames_por_char,
        "cursor_blink_frames": cursor_periodo_f,
        "geometria_base": canon.GEOMETRIA.base,
        "tokens_ui": canon.PALETA_UI,
        "fonte_default": canon.FONTE_TITULO_DEFAULT,
        "eventos": eventos,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Plano determinístico de frames do HUD.")
    ap.add_argument("--texto", required=True, help="linhas separadas por '|'")
    ap.add_argument("--beat", type=int, default=1)
    ap.add_argument("--dataviz", action="store_true")
    ap.add_argument("--cps", type=int, default=canon.VELOCIDADE_DIGITACAO_CPS)
    args = ap.parse_args()
    linhas = [l for l in args.texto.split("|") if l]
    plano = plano_hud(linhas, args.beat, args.dataviz, args.cps)
    # imprime resumo + nº de eventos (evita poluir o terminal com 240 frames)
    resumo = {k: v for k, v in plano.items() if k != "eventos"}
    resumo["n_eventos"] = len(plano["eventos"])
    print(json.dumps(resumo, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
