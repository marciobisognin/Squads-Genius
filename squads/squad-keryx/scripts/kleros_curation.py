#!/usr/bin/env python3
"""KÊRYX — KLEROS: curadoria aleatória determinística.

Sorteia domínio(s)/tópico(s) com pesos + anti-repetição usando RNG COM SEED
(reprodutível). Sorteia também formato (infographic/comic) quando 'auto' e propõe
o par de estilo baoyu por heurística. Sem dependências externas (stdlib).

Uso:
    python3 scripts/kleros_curation.py --n-slides 5 --seed 42 --mode single_theme
    python3 scripts/kleros_curation.py --n-slides 4 --seed 7 --output-format comic
"""
from __future__ import annotations

import argparse
import json
import random
from typing import Dict, List, Optional

# Banco mínimo de domínios -> tópicos (PRD seção 5). Cada tópico carrega um cotidiano_hook.
BANCO: Dict[str, Dict[str, str]] = {
    "tecnologia": {
        "atalhos_automacao": "as tarefas repetitivas que comem seu dia",
        "seguranca_digital": "o medo de ter a conta invadida",
        "ia_pratica": "usar IA para trabalhar menos",
        "higiene_digital": "o celular que rouba sua atenção",
    },
    "produtividade": {
        "evitar_burnout": "a pilha de pendências que rouba sua energia",
        "tecnica_pomodoro": "a dificuldade de manter o foco",
        "regra_2_minutos": "os pequenos pendentes que se acumulam",
        "eat_the_frog": "adiar a tarefa mais difícil do dia",
    },
    "gestao_vida": {
        "financas_pessoais": "o dinheiro que some no fim do mês",
        "rotina_casa": "a casa sempre bagunçada",
        "compras_inteligentes": "gastar demais no mercado",
        "alimentacao": "comer mal na correria",
    },
    "livros": {
        "estoicismo_pratico": "reagir no impulso e se arrepender",
        "tres_corpos_explicado": "entender o caos com um exemplo do dia a dia",
        "licoes_marco_aurelio": "manter a calma sob pressão",
        "pense_como_fisico": "tomar decisões com modelos mentais",
    },
}

SUBDOMINIOS_LIVROS = ["literatura", "ficcao_cientifica", "filosofia", "matematica", "fisica"]

# Heurística domínio -> estilo baoyu (PRD seção 8.6).
ESTILO_INFOGRAFICO = {
    "tecnologia": {"layout": "dense-modules", "style": "technical-schematic"},
    "produtividade": {"layout": "dense-modules", "style": "minimalist"},
    "gestao_vida": {"layout": "bento-grid", "style": "craft-handmade"},
    "livros": {"layout": "timeline", "style": "morandi-journal"},
}
ESTILO_COMIC = {
    "tecnologia": {"art": "ligne-claire", "tone": "neutral", "layout": "standard", "preset": None},
    "produtividade": {"art": "ligne-claire", "tone": "warm", "layout": "standard", "preset": "ohmsha"},
    "gestao_vida": {"art": "chalk", "tone": "warm", "layout": "standard", "preset": None},
    "livros": {"art": "ink-brush", "tone": "dramatic", "layout": "standard", "preset": None},
}


def _candidatos(domains: List[str], excluidos: List[str]) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for dom in domains:
        for topico, hook in BANCO.get(dom, {}).items():
            if topico not in excluidos:
                out.append({"dominio": dom, "topico": topico, "cotidiano_hook": hook})
    return out


def sugerir_estilo(dominio: str, fmt: str) -> Dict[str, object]:
    if fmt == "comic":
        return ESTILO_COMIC.get(dominio, ESTILO_COMIC["produtividade"])
    return ESTILO_INFOGRAFICO.get(dominio, ESTILO_INFOGRAFICO["produtividade"])


def curar(
    n_slides: int,
    seed: int,
    domains: Optional[List[str]] = None,
    mode: str = "single_theme",
    output_format: str = "auto",
    excluidos: Optional[List[str]] = None,
    format_weights: Optional[List[float]] = None,
) -> Dict[str, object]:
    rng = random.Random(seed)
    domains = domains or list(BANCO.keys())
    excluidos = excluidos or []
    fw = format_weights or [0.7, 0.3]

    fmt = output_format
    if fmt == "auto":
        fmt = rng.choices(["infographic", "comic"], weights=fw, k=1)[0]

    cand = _candidatos(domains, excluidos)
    if not cand:
        cand = _candidatos(domains, [])  # afrouxa anti-repetição se esvaziar

    slots: List[Dict[str, object]] = []
    if mode == "single_theme":
        base = rng.choice(cand)
        dom = base["dominio"]
        pool = [c for c in cand if c["dominio"] == dom] or cand
        escolhidos = [rng.choice(pool) for _ in range(n_slides)]
    elif mode == "combined":
        escolhidos = [rng.choice(cand) for _ in range(n_slides)]
    else:  # random_mix
        escolhidos = [rng.choice(cand) for _ in range(n_slides)]

    for i, c in enumerate(escolhidos, 1):
        slot = {"slide_index": i, **c}
        if c["dominio"] == "livros":
            slot["subdominio"] = rng.choice(SUBDOMINIOS_LIVROS)
        slots.append(slot)

    dom_estilo = slots[0]["dominio"] if slots else "produtividade"
    estilo = sugerir_estilo(str(dom_estilo), fmt)

    return {
        "output_format": fmt,
        "baoyu_style": {fmt if fmt == "comic" else "infographic": estilo},
        "slots": slots,
        "anti_repeticao": {"janela": 30, "topicos_excluidos": excluidos, "estilos_excluidos": []},
        "seed": seed,
        "mode": mode,
    }


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="KLEROS — curadoria aleatória determinística.")
    ap.add_argument("--n-slides", type=int, required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--mode", choices=["single_theme", "combined", "random_mix"], default="single_theme")
    ap.add_argument("--output-format", choices=["infographic", "comic", "auto"], default="auto")
    ap.add_argument("--domains", nargs="*", default=None)
    ap.add_argument("--exclude", nargs="*", default=None, help="tópicos a excluir (anti-repetição).")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    plan = curar(
        n_slides=args.n_slides,
        seed=args.seed,
        domains=args.domains,
        mode=args.mode,
        output_format=args.output_format,
        excluidos=args.exclude,
    )
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
