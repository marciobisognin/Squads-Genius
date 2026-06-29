#!/usr/bin/env python3
"""THEORÍA — CHRONOS: cálculo determinístico de tempo (sem LLM).

A duração do vídeo é DERIVADA do conteúdo (tempo necessário para explicar tudo),
limitada pela banda informada no brief. Nada de números mágicos: tudo rastreável.

Fórmula (PRD §9.2):
    dur_narracao_s = palavras / (taxa_fala_ppm / 60)
    pausa_absorcao = f(funcao_didatica)
    run_time_anim  = max(dur_narracao_s, soma(run_time primitivas)) + pausa_absorcao
    duracao_total  = Σ run_time_anim   (validada contra banda_duracao_s)

Uso:
    python3 scripts/chronos_timing.py --beats caminho/beats.json
    cat beats.json | python3 scripts/chronos_timing.py
    python3 scripts/chronos_timing.py --beats beats.json --reconcile durations_tts.json
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Tuple

# Configuráveis (PRD §9.2). pt-BR narração didática.
TAXA_FALA_PPM = 150
PAUSA_ABSORCAO_S: Dict[str, float] = {
    "gancho": 0.5,
    "intuicao": 0.8,
    "formalizacao": 1.0,
    "recompensa": 1.5,
}
TOLERANCIA_SYNC_S = 0.200  # 200 ms/beat (default do loop S5<->S9)


def duracao_narracao(palavras: int, taxa_ppm: int = TAXA_FALA_PPM) -> float:
    """Segundos de narração para um número de palavras."""
    if palavras <= 0:
        return 0.0
    return round(palavras / (taxa_ppm / 60.0), 3)


def run_time_beat(beat: Dict[str, Any]) -> Dict[str, float]:
    """Calcula durações de um beat de forma determinística."""
    palavras = int(beat.get("palavras") or len(str(beat.get("narracao", "")).split()))
    funcao = str(beat.get("funcao_didatica", "intuicao"))
    soma_primitivas = float(sum(p.get("run_time_s", 0.0) for p in beat.get("primitivas", [])))

    dur_narr = duracao_narracao(palavras)
    pausa = PAUSA_ABSORCAO_S.get(funcao, 0.8)
    run_time_anim = round(max(dur_narr, soma_primitivas) + pausa, 3)
    return {
        "palavras": palavras,
        "duracao_narracao_s": dur_narr,
        "pausa_absorcao_s": pausa,
        "run_time_anim_s": run_time_anim,
    }


def build_timeline(
    beats: List[Dict[str, Any]],
    banda_duracao_s: Optional[Tuple[int, int]] = None,
) -> Dict[str, Any]:
    """Produz a linha do tempo mestra a partir dos beats."""
    timeline: List[Dict[str, Any]] = []
    t = 0.0
    for beat in beats:
        calc = run_time_beat(beat)
        inicio = round(t, 3)
        t += calc["run_time_anim_s"]
        timeline.append({
            "id": beat.get("id"),
            "funcao_didatica": beat.get("funcao_didatica"),
            **calc,
            "inicio_s": inicio,
            "fim_s": round(t, 3),
        })
    total = round(t, 3)
    dentro_da_banda = True
    aviso = None
    if banda_duracao_s:
        lo, hi = banda_duracao_s
        if total < lo:
            dentro_da_banda = False
            aviso = f"duração {total}s abaixo da banda mínima {lo}s — considere aprofundar conteúdo"
        elif total > hi:
            dentro_da_banda = False
            aviso = f"duração {total}s acima da banda máxima {hi}s — considere enxugar beats"
    return {
        "duracao_total_s": total,
        "n_beats": len(beats),
        "dentro_da_banda": dentro_da_banda,
        "aviso": aviso,
        "timeline": timeline,
    }


def reconcile(
    timeline: Dict[str, Any],
    duracoes_tts_s: Dict[str, float],
    tolerancia_s: float = TOLERANCIA_SYNC_S,
) -> Dict[str, Any]:
    """Loop S5<->S9: confronta o tempo planejado com a duração real do TTS (EChÓ).

    Para cada beat, se |Δ| > tolerância, reajusta run_time_anim para acomodar a
    narração real, preservando a pausa de absorção. Retorna a timeline reconciliada
    e a lista de beats que precisaram de ajuste.
    """
    ajustes: List[Dict[str, Any]] = []
    nova: List[Dict[str, Any]] = []
    t = 0.0
    for item in timeline["timeline"]:
        bid = item["id"]
        real = duracoes_tts_s.get(str(bid))
        novo = dict(item)
        if real is not None:
            delta = round(real - item["duracao_narracao_s"], 3)
            if abs(delta) > tolerancia_s:
                novo["duracao_narracao_s"] = round(real, 3)
                base = max(real, item["run_time_anim_s"] - item["pausa_absorcao_s"])
                novo["run_time_anim_s"] = round(base + item["pausa_absorcao_s"], 3)
                ajustes.append({"id": bid, "delta_s": delta, "novo_run_time_anim_s": novo["run_time_anim_s"]})
        novo["inicio_s"] = round(t, 3)
        t += novo["run_time_anim_s"]
        novo["fim_s"] = round(t, 3)
        nova.append(novo)
    return {
        "duracao_total_s": round(t, 3),
        "n_beats": len(nova),
        "ajustes": ajustes,
        "convergiu": not ajustes,
        "timeline": nova,
    }


def _load(path: Optional[str]) -> Any:
    raw = open(path, encoding="utf-8").read() if path else sys.stdin.read()
    return json.loads(raw)


def main() -> int:
    ap = argparse.ArgumentParser(description="CHRONOS — timeline determinística.")
    ap.add_argument("--beats", help="JSON com lista de beats (ou {beats:[...], banda_duracao_s:[lo,hi]}).")
    ap.add_argument("--reconcile", help="JSON {beat_id: duracao_real_s} do TTS (EChÓ).")
    args = ap.parse_args()

    data = _load(args.beats)
    if isinstance(data, dict):
        beats = data.get("beats", [])
        banda = tuple(data.get("banda_duracao_s", ())) or None
    else:
        beats, banda = data, None

    timeline = build_timeline(beats, banda)
    if args.reconcile:
        tts = _load(args.reconcile)
        out = reconcile(timeline, {str(k): float(v) for k, v in tts.items()})
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if out["convergiu"] else 1

    print(json.dumps(timeline, ensure_ascii=False, indent=2))
    return 0 if timeline["dentro_da_banda"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
