#!/usr/bin/env python3
"""Valida deterministicamente a fidelidade/guardrails de uma resposta gerada.

Checagens (sem LLM):
- presenca de pelo menos uma referencia biblica estruturavel;
- presenca do disclaimer de representacao didatica de IA;
- presenca do footer obrigatorio;
- ausencia de padroes de aspas longas sem referencia (citacao potencialmente inventada).

Retorna um relatorio com aprovado/reprovado e a lista de problemas. Serve de
quality gate antes de a resposta chegar ao usuario.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from parse_referencia_biblica import carregar_livros, extrair  # noqa: E402

FOOTER = "Licenca: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."
DISCLAIMER_TERMOS = ["representacao didatica", "representacao de ia", "nao e a voz real", "simulacao"]

# Aspas com 8+ palavras sem uma referencia logo apos.
_CITACAO_LONGA = re.compile(r"[\"“]([^\"”]{40,})[\"”]")


def _norm(t: str) -> str:
    import unicodedata

    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def validar(resposta: str, data_dir: Path) -> Dict[str, Any]:
    problemas: List[str] = []
    avisos: List[str] = []
    resp_norm = _norm(resposta)

    indice = carregar_livros(data_dir)
    refs = extrair(resposta, indice)
    if not refs:
        problemas.append("nenhuma referencia biblica detectada (livro capitulo[:versiculo]).")

    if not any(term in resp_norm for term in DISCLAIMER_TERMOS):
        problemas.append("disclaimer de representacao didatica de IA ausente.")

    if FOOTER.lower() not in resp_norm and "criado por marcio bisognin" not in resp_norm:
        problemas.append("footer obrigatorio ausente.")

    for m in _CITACAO_LONGA.finditer(resposta):
        trecho = m.group(1)
        janela = resposta[m.end():m.end() + 60]
        if not extrair(janela, indice):
            avisos.append(f"citacao longa sem referencia proxima: '{trecho[:40]}...'")

    aprovado = not problemas
    return {
        "aprovado": aprovado,
        "referencias_detectadas": [r["referencia_normalizada"] for r in refs],
        "problemas": problemas,
        "avisos": avisos,
        "go_no_go": "go" if aprovado else "no-go",
    }


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Valida guardrails/fidelidade de uma resposta do squad.")
    grupo = ap.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--resposta", help="Texto da resposta a validar.")
    grupo.add_argument("--arquivo", help="Arquivo contendo a resposta.")
    ap.add_argument("--data-dir", default=str(SCRIPT_DIR / "data"), help="Diretorio com livros_biblia.json.")
    return ap.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    if args.arquivo:
        resposta = Path(args.arquivo).read_text(encoding="utf-8")
    else:
        resposta = args.resposta
    relatorio = validar(resposta, Path(args.data_dir))
    print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    return 0 if relatorio["aprovado"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
