#!/usr/bin/env python3
"""KÁNŌN — validador determinístico contra o Cânone (PRD §7 / §11).

Guardião de fidelidade. Valida NUMERICAMENTE specs e configs de render contra
`arkheion/canon.py`: hex exatos, fonte permitida, geometria com tolerância, timing
na faixa, cadeia de grade e duração da cena. Gate bloqueante: divergência → veredito
`aprovado: false` com motivos auditáveis.

Uso:
    python3 scripts/kanon.py --card examples/card_interface_tecnologia.json
    python3 scripts/kanon.py --plano examples/plano_sequencial_tecnologia.json --tamanho 60
    python3 scripts/kanon.py --grade "<cadeia ffmpeg>"
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arkheion import canon  # noqa: E402

CONTADOR_RE = re.compile(r"^(\d{2}) / (\d{2})$")


def validar_hex(valor: str) -> bool:
    return valor.upper() in {h.upper() for h in canon.HEX_PERMITIDOS}


def validar_fonte(fonte: str) -> bool:
    return fonte in canon.FONTES_PERMITIDAS


def _proibidos_em(texto: str) -> List[str]:
    low = texto.lower()
    return [p for p in canon.PROIBIDOS if p.replace("_", " ") in low or p in low]


def validar_card(card: Dict[str, Any], total_cenas: int | None = None) -> List[str]:
    """Valida um CardInterface (dict). Retorna lista de motivos de reprovação."""
    motivos: List[str] = []
    contador = str(card.get("contador", ""))
    m = CONTADOR_RE.match(contador)
    if not m:
        motivos.append(f"contador fora do padrão 'NN / TT': {contador!r}")
    elif total_cenas is not None and int(m.group(2)) != total_cenas:
        motivos.append(f"contador total {m.group(2)} != nº de cenas {total_cenas}")
    titulo = str(card.get("titulo", ""))
    if len(titulo.split()) > canon.TITULO_MAX_PALAVRAS:
        motivos.append(f"título com mais de {canon.TITULO_MAX_PALAVRAS} palavras: {titulo!r}")
    if titulo and titulo != titulo.upper():
        motivos.append(f"título deve ser CAIXA ALTA: {titulo!r}")
    # aceita 'linhas_texto' (CardInterface) ou 'texto_digitado' (Beat)
    linhas = card.get("linhas_texto", card.get("texto_digitado", []))
    if not (1 <= len(linhas) <= 4):
        motivos.append("linhas/texto_digitado deve ter de 1 a 4 itens")
    fonte = card.get("fonte_titulo")
    if fonte is not None and not validar_fonte(fonte):
        motivos.append(f"fonte fora da lista permitida: {fonte!r}")
    for campo in ("titulo", "rodape", "metadados_topo_esq"):
        achados = _proibidos_em(str(card.get(campo, "")))
        if achados:
            motivos.append(f"termo proibido em {campo}: {achados}")
    return motivos


def validar_footage(spec: Dict[str, Any]) -> List[str]:
    """Valida um FootageSpec: plano/movimento válidos e prompt negativo com proibições."""
    motivos: List[str] = []
    if spec.get("plano") not in {"close", "detalhe", "plano_medio", "macro"}:
        motivos.append(f"plano inválido: {spec.get('plano')!r}")
    if spec.get("movimento") not in {"handheld_sutil", "push_lento", "estatico", "pan_lento"}:
        motivos.append(f"movimento inválido: {spec.get('movimento')!r}")
    achados = _proibidos_em(str(spec.get("prompt_positivo", "")))
    if achados:
        motivos.append(f"prompt_positivo contém estética proibida: {achados}")
    dur = spec.get("duracao_s", canon.TIMING.cena_s)
    if dur != canon.TIMING.cena_s:
        motivos.append(f"duração da cena {dur}s != {canon.TIMING.cena_s}s (CENA-10)")
    return motivos


def validar_plano(plano: Dict[str, Any], tamanho_s: int | None = None) -> List[str]:
    """Valida um PlanoSequencial completo contra o Cânone e a duração resolvida."""
    motivos: List[str] = []
    beats = plano.get("beats", [])
    n = len(beats)
    if tamanho_s is not None:
        try:
            pd = canon.resolver_duracao(tamanho_s)
        except ValueError as exc:
            return [str(exc)]
        if n != pd.n_cenas:
            motivos.append(f"nº de beats {n} != {pd.n_cenas} para {tamanho_s}s")
        for beat, contador_esperado, funcao_esperada in zip(beats, pd.contadores, pd.funcoes):
            if beat.get("contador") != contador_esperado:
                motivos.append(
                    f"beat {beat.get('indice')}: contador {beat.get('contador')!r} "
                    f"!= esperado {contador_esperado!r}"
                )
            if beat.get("funcao") != funcao_esperada:
                motivos.append(
                    f"beat {beat.get('indice')}: função {beat.get('funcao')!r} "
                    f"!= esperada {funcao_esperada!r}"
                )
    if not 3 <= n <= 9:
        motivos.append(f"nº de beats {n} fora de 3..9")
    # beat de prova_visual deve carregar dataviz
    for beat in beats:
        if beat.get("funcao") == "prova_visual" and not beat.get("dataviz"):
            motivos.append(f"beat {beat.get('indice')} (prova_visual) sem dataviz")
        motivos += [f"beat {beat.get('indice')}: {m}" for m in validar_card(beat, total_cenas=n)]
    return motivos


def validar_grade(cadeia: str) -> List[str]:
    """Valida a cadeia de grade FFmpeg contra as faixas canônicas (PRD §7)."""
    motivos: List[str] = []

    def _num(pat: str) -> float | None:
        m = re.search(pat, cadeia)
        return float(m.group(1)) if m else None

    contrast = _num(r"contrast=([0-9.]+)")
    sat = _num(r"saturation=([0-9.]+)")
    noise = _num(r"noise=alls=([0-9.]+)")
    lo, hi = canon.GRADE_FAIXAS["contrast"]
    if contrast is None or not lo <= contrast <= hi:
        motivos.append(f"contraste {contrast} fora de {lo}..{hi}")
    lo, hi = canon.GRADE_FAIXAS["saturation"]
    if sat is None or not lo <= sat <= hi:
        motivos.append(f"saturação {sat} fora de {lo}..{hi}")
    lo, hi = canon.GRADE_FAIXAS["noise_alls"]
    if noise is None or not lo <= noise <= hi:
        motivos.append(f"granulação (noise alls) {noise} fora de {lo}..{hi}")
    if "vignette" not in cadeia:
        motivos.append("vinheta ausente na cadeia de grade")
    return motivos


def veredito(motivos: List[str], alvo: str) -> Dict[str, Any]:
    return {
        "alvo": alvo,
        "aprovado": not motivos,
        "motivos": motivos,
        "canone_versao": "1.0.0",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="KÁNŌN — validação determinística do Cânone.")
    ap.add_argument("--card", help="JSON CardInterface a validar")
    ap.add_argument("--footage", help="JSON FootageSpec a validar")
    ap.add_argument("--plano", help="JSON PlanoSequencial a validar")
    ap.add_argument("--grade", help="cadeia FFmpeg a validar (string)")
    ap.add_argument("--tamanho", type=int, default=None, help="tamanho-alvo em s (30/60/90)")
    args = ap.parse_args()

    if args.card:
        data = json.loads(Path(args.card).read_text(encoding="utf-8"))
        res = veredito(validar_card(data), f"card:{args.card}")
    elif args.footage:
        data = json.loads(Path(args.footage).read_text(encoding="utf-8"))
        res = veredito(validar_footage(data), f"footage:{args.footage}")
    elif args.plano:
        data = json.loads(Path(args.plano).read_text(encoding="utf-8"))
        res = veredito(validar_plano(data, args.tamanho), f"plano:{args.plano}")
    elif args.grade:
        res = veredito(validar_grade(args.grade), "grade")
    else:
        res = veredito(validar_grade(canon.GRADE_FFMPEG), "grade_canonica")

    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["aprovado"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
