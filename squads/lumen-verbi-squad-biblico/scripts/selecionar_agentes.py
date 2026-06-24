#!/usr/bin/env python3
"""Motor deterministico de selecao e combinacao de agentes (nucleo do MSCA).

Recebe uma consulta em linguagem natural, casa entidades/temas contra o registro
de perfis (BDC) e o mapa semantico, e devolve um ranking de personas biblicas e,
quando pertinente, historiadores complementares. Nao usa LLM: e ranqueamento por
sobreposicao de palavras-chave, totalmente reproduzivel.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent / "data"


def _normalize(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower()


def _tokens(texto: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", _normalize(texto))


def carregar_dados(data_dir: Path = DATA_DIR) -> Dict[str, Any]:
    perfis = json.loads((data_dir / "perfis_agentes.json").read_text(encoding="utf-8"))
    mapa = json.loads((data_dir / "mapa_semantico.json").read_text(encoding="utf-8"))
    return {"perfis": perfis, "mapa": mapa}


def _casa(termo: str, consulta_norm: str, tokens: set[str]) -> bool:
    """Termo de uma palavra casa por palavra inteira; frase casa por substring."""
    termo = termo.strip()
    if " " in termo:
        return termo in consulta_norm
    return termo in tokens


def _pontuar_persona(consulta_norm: str, tokens: set[str], persona: Dict[str, Any], mapa: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    motivos: List[str] = []
    # Conhecimento direto da persona.
    for termo in persona.get("conhecimento", []):
        if _casa(termo, consulta_norm, tokens):
            score += 3
            motivos.append(f"conhecimento:{termo}")
    # Nome citado explicitamente.
    nome_tokens = set(_tokens(persona["nome"]))
    if nome_tokens & tokens:
        score += 5
        motivos.append("nome-citado")
    # Mapa semantico (temas/doutrinas/eventos).
    for categoria in ("temas", "doutrinas", "eventos"):
        for chave, agentes in mapa.get(categoria, {}).items():
            if persona["id"] in agentes and _casa(chave, consulta_norm, tokens):
                score += 2
                motivos.append(f"{categoria}:{chave}")
    return {"id": persona["id"], "nome": persona["nome"], "testamento": persona["testamento"], "score": score, "motivos": sorted(set(motivos))}


def _historiadores_relevantes(consulta_norm: str, tokens: set[str], perfis: Dict[str, Any], mapa: Dict[str, Any]) -> List[Dict[str, Any]]:
    gatilhos = mapa.get("gatilhos_historiador", {})
    selecionados: List[Dict[str, Any]] = []
    por_id = {h["id"]: h for h in perfis.get("historiadores", [])}
    mapeamento = {
        "antigo": "historiador-antigo-testamento",
        "novo": "historiador-novo-testamento",
        "textual": "critico-textual",
    }
    pontos: Dict[str, Dict[str, Any]] = {}

    def _add(hid: str, motivo: str, peso: int) -> None:
        hist = por_id.get(hid)
        if not hist:
            return
        reg = pontos.setdefault(hid, {"id": hist["id"], "nome": hist["nome"], "score": 0, "motivos": []})
        reg["score"] += peso
        reg["motivos"].append(motivo)

    for chave, termos in gatilhos.items():
        for t in termos:
            if _casa(t, consulta_norm, tokens):
                _add(mapeamento[chave], f"gatilho:{t}", 1)

    # Historiadores indicados pelo mapa semantico (evento/tema/doutrina que casou).
    for categoria in ("eventos", "temas", "doutrinas"):
        for chave, agentes in mapa.get(categoria, {}).items():
            if _casa(chave, consulta_norm, tokens):
                for aid in agentes:
                    if aid.startswith("historiador-") or aid == "critico-textual":
                        _add(aid, f"{categoria}:{chave}", 2)

    for reg in pontos.values():
        reg["motivos"] = sorted(set(reg["motivos"]))
    return sorted(pontos.values(), key=lambda x: x["score"], reverse=True)


def selecionar(consulta: str, dados: Dict[str, Any], top_personas: int = 2) -> Dict[str, Any]:
    perfis = dados["perfis"]
    mapa = dados["mapa"]
    consulta_norm = _normalize(consulta)
    tokens = set(_tokens(consulta))

    ranking = [_pontuar_persona(consulta_norm, tokens, p, mapa) for p in perfis.get("personas_biblicas", [])]
    ranking = [r for r in ranking if r["score"] > 0]
    ranking.sort(key=lambda x: x["score"], reverse=True)

    personas_primarias = ranking[:top_personas]
    historiadores = _historiadores_relevantes(consulta_norm, tokens, perfis, mapa)

    multiplas_perspectivas = len(personas_primarias) >= 2 and personas_primarias[0]["score"] - personas_primarias[-1]["score"] <= 3

    return {
        "consulta": consulta,
        "personas_primarias": personas_primarias,
        "historiadores_complementares": historiadores,
        "ranking_completo": ranking,
        "sugere_multiplas_perspectivas": multiplas_perspectivas,
        "fallback": not personas_primarias,
        "nota": "Sem persona pontuada: encaminhar ao curador-bdc para esclarecimento." if not personas_primarias else "",
    }


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Seleciona e combina agentes do Squad Biblico a partir de uma consulta.")
    ap.add_argument("--consulta", required=True, help="Pergunta do usuario em linguagem natural.")
    ap.add_argument("--top", type=int, default=2, help="Numero maximo de personas primarias.")
    ap.add_argument("--data-dir", default=str(DATA_DIR), help="Diretorio com perfis_agentes.json e mapa_semantico.json.")
    return ap.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        dados = carregar_dados(Path(args.data_dir))
    except FileNotFoundError as exc:
        print(json.dumps({"erro": f"dados nao encontrados: {exc}"}, ensure_ascii=False), file=sys.stderr)
        return 2
    resultado = selecionar(args.consulta, dados, top_personas=args.top)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
