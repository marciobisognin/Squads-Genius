#!/usr/bin/env python3
"""Engine determinística de regras de conformidade.

Carrega templates/regras.yaml (ou .json) e aplica condições simples sobre os
metadados/cláusulas de cada instrumento. Nenhum juízo de mérito: produz
apontamentos classificados, com fundamento e necessidade de revisão humana.

Uso: python scripts/rules_engine.py --regras ./templates/regras.yaml \
        --metadados ./saida/metadados.json --clausulas-essenciais ./saida/clausulas_essenciais.json \
        --partes ./saida/partes.json --output ./saida
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from projur_common import read_json, write_json

try:
    import yaml
except Exception:  # degradação graciosa
    yaml = None


def load_rules(path: str) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    if p.suffix in (".yaml", ".yml") and yaml is not None:
        return yaml.safe_load(p.read_text(encoding="utf-8")).get("regras", [])
    if p.suffix == ".json" or yaml is None:
        alt = p.with_suffix(".json")
        if alt.exists():
            return read_json(alt, {}).get("regras", [])
    return []


def avaliar(regra: dict, ctx: dict) -> bool:
    """Avalia a condição da regra. Condições suportadas (campo 'condicao')."""
    cond = regra.get("condicao", "")
    md = ctx["metadados"]
    ess = ctx["essenciais"]
    partes = ctx["partes"]
    if cond == "sem_clausulas_essenciais":
        return bool(ess and ess.get("essenciais_ausentes"))
    if cond == "sem_base_legal":
        return not md.get("base_legal")
    if cond == "valor_ausente":
        return md.get("valor") in (None, 0)
    if cond == "documento_parte_invalido":
        return any(not p.get("valido", True) for p in partes.get("partes", []))
    if cond == "convenio_sem_plano_trabalho":
        return md.get("tipo") in ("convenio", "termo_execucao_descentralizada") and "plano de trabalho" not in (md.get("objeto") or "").lower()
    if cond == "sem_vigencia":
        return not md.get("vigencia_fim")
    if cond == "pdi_sem_pi":
        return "pd&i" in (md.get("objeto") or "").lower() or "pesquisa" in (md.get("objeto") or "").lower()
    if cond == "sempre":
        return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--regras", required=True)
    ap.add_argument("--metadados", required=True)
    ap.add_argument("--clausulas-essenciais", default=None)
    ap.add_argument("--partes", default=None)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    out = Path(args.output) if args.output else Path(args.metadados).parent
    regras = load_rules(args.regras)
    metadados = read_json(args.metadados, {"itens": []}).get("itens", [])
    ess = {i["instrumento_id"]: i for i in read_json(args.clausulas_essenciais, {"itens": []}).get("itens", [])} if args.clausulas_essenciais else {}
    partes = {i["id"]: i for i in read_json(args.partes, {"itens": []}).get("itens", [])} if args.partes else {}

    validacoes = []
    for md in metadados:
        ctx = {"metadados": md, "essenciais": ess.get(md["id"], {}), "partes": partes.get(md["id"], {})}
        for regra in regras:
            if avaliar(regra, ctx):
                validacoes.append({
                    "instrumento_id": md["id"],
                    "regra_id": regra["id"],
                    "resultado": "violada",
                    "classificacao": "suspeita" if regra.get("severidade") in ("media", "baixa") else "depende_justificativa",
                    "fundamento": regra.get("base_legal", "verificar na fonte oficial"),
                    "confianca": regra.get("confianca", 0.6),
                    "revisao_humana": True,
                })

    write_json(out / "validacoes.json", {"total": len(validacoes), "itens": validacoes})
    print(f"Engine de regras: {len(validacoes)} apontamento(s) sobre {len(regras)} regra(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
