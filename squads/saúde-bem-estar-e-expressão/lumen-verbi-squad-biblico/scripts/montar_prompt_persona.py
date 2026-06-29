#!/usr/bin/env python3
"""Monta deterministicamente o prompt de sistema de uma persona/historiador.

A partir do registro de perfis (BDC), do contexto recuperado e da consulta,
gera o bloco de instrucao que o LLM da persona devera seguir, ja embutindo os
guardrails do guardiao-teologico. Nenhum texto e inventado aqui: tudo vem do
perfil cadastrado. Isso garante coerencia e reproducao.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

DATA_DIR = Path(__file__).resolve().parent / "data"

GUARDRAILS = [
    "Voce e uma representacao DIDATICA de IA desta figura, nao a voz real dela.",
    "Nunca invente citacoes; toda citacao deve trazer a referencia (livro capitulo:versiculo).",
    "Separe claramente: texto biblico, consenso historico-academico e interpretacao teologica.",
    "Mantenha neutralidade denominacional e sinalize quando a interpretacao for controversa.",
    "Permaneca no escopo de conhecimento do perfil; fora dele, recomende outro agente.",
]


def carregar_perfis(data_dir: Path = DATA_DIR) -> Dict[str, Any]:
    return json.loads((data_dir / "perfis_agentes.json").read_text(encoding="utf-8"))


def buscar_perfil(perfis: Dict[str, Any], agente_id: str) -> Optional[Dict[str, Any]]:
    for grupo in ("personas_biblicas", "historiadores"):
        for item in perfis.get(grupo, []):
            if item["id"] == agente_id:
                return {"grupo": grupo, **item}
    return None


def montar(perfil: Dict[str, Any], consulta: str, contexto: Optional[List[str]] = None) -> str:
    contexto = contexto or []
    linhas: List[str] = []
    linhas.append(f"# Persona ativa: {perfil['nome']} ({perfil['id']})")
    if perfil["grupo"] == "personas_biblicas":
        linhas.append(f"Papel: {perfil.get('papel_principal', '')}")
        linhas.append(f"Testamento: {perfil.get('testamento', '')}")
        linhas.append(f"Personalidade: {', '.join(perfil.get('personalidade', []))}")
        linhas.append(f"Estilo de comunicacao: {perfil.get('estilo_comunicacao', '')}")
        linhas.append(f"Perspectiva teologica: {perfil.get('perspectiva_teologica', '')}")
        linhas.append(f"Passagens-chave: {', '.join(perfil.get('passagens_chave', []))}")
    else:
        linhas.append(f"Especializacao: {perfil.get('especializacao', '')}")
        linhas.append(f"Abordagem: {perfil.get('abordagem', '')}")
        linhas.append(f"Estilo de comunicacao: {perfil.get('estilo_comunicacao', '')}")
        linhas.append(f"Periodos: {', '.join(perfil.get('periodos', []))}")
    linhas.append("")
    linhas.append("## Guardrails obrigatorios")
    linhas.extend(f"- {g}" for g in GUARDRAILS)
    linhas.append("")
    if contexto:
        linhas.append("## Contexto recuperado da BDC")
        linhas.extend(f"- {c}" for c in contexto)
        linhas.append("")
    linhas.append("## Consulta do usuario")
    linhas.append(consulta)
    linhas.append("")
    linhas.append("Responda no estilo do perfil acima, citando referencias e respeitando os guardrails.")
    linhas.append("Encerre com: Licenca: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.")
    return "\n".join(linhas)


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Monta o prompt de sistema de uma persona/historiador.")
    ap.add_argument("--agente", required=True, help="ID do agente (ex.: persona-jesus).")
    ap.add_argument("--consulta", required=True, help="Pergunta do usuario.")
    ap.add_argument("--contexto", nargs="*", default=[], help="Trechos de contexto recuperados da BDC.")
    ap.add_argument("--data-dir", default=str(DATA_DIR), help="Diretorio com perfis_agentes.json.")
    return ap.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        perfis = carregar_perfis(Path(args.data_dir))
    except FileNotFoundError as exc:
        print(f"dados nao encontrados: {exc}", file=sys.stderr)
        return 2
    perfil = buscar_perfil(perfis, args.agente)
    if perfil is None:
        print(f"agente desconhecido: {args.agente}", file=sys.stderr)
        return 1
    print(montar(perfil, args.consulta, args.contexto))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
