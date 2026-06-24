#!/usr/bin/env python3
"""Extrai e normaliza referencias biblicas de um texto livre.

Reconhece padroes como "Joao 3:16", "Mateus 5:1-12", "Sl 23", "1 Corintios 13".
Saida estruturada (livro canonico, capitulo, versiculos, testamento) para
recuperacao precisa na BDC. Deterministico, sem dependencias externas.
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


def _norm(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower().strip()


def carregar_livros(data_dir: Path = DATA_DIR) -> Dict[str, Dict[str, str]]:
    dados = json.loads((data_dir / "livros_biblia.json").read_text(encoding="utf-8"))
    indice: Dict[str, Dict[str, str]] = {}
    for livro in dados["livros"]:
        chaves = [_norm(livro["nome"])] + [_norm(a) for a in livro.get("abrev", [])]
        for chave in chaves:
            indice[chave] = {"nome": livro["nome"], "testamento": livro["testamento"]}
    return indice


_REF = re.compile(
    r"((?:[1-3]\s*)?[A-Za-zÀ-ÿ]+(?:\s+(?:dos\s+)?[A-Za-zÀ-ÿ]+)*)"  # nome do livro (pode ter prefixo numerico)
    r"\s+(\d{1,3})"                                                   # capitulo
    r"(?::(\d{1,3})(?:\s*-\s*(\d{1,3}))?)?"                           # versiculo(s) opcionais
)


def extrair(texto: str, indice: Dict[str, Dict[str, str]]) -> List[Dict[str, Any]]:
    achados: List[Dict[str, Any]] = []
    for m in _REF.finditer(texto):
        bruto_livro, cap, v_ini, v_fim = m.groups()
        chave = _norm(bruto_livro)
        info = indice.get(chave)
        if info is None:
            # tenta casar pela ultima/duas ultimas palavras (ex.: "no livro de Joao 3")
            partes = chave.split()
            for n in (3, 2, 1):
                cand = " ".join(partes[-n:])
                if cand in indice:
                    info = indice[cand]
                    break
        if info is None:
            continue
        ref = {
            "livro": info["nome"],
            "testamento": info["testamento"],
            "capitulo": int(cap),
            "versiculo_inicial": int(v_ini) if v_ini else None,
            "versiculo_final": int(v_fim) if v_fim else (int(v_ini) if v_ini else None),
            "referencia_normalizada": _formatar(info["nome"], cap, v_ini, v_fim),
        }
        achados.append(ref)
    return achados


def _formatar(livro: str, cap: str, v_ini: str | None, v_fim: str | None) -> str:
    if not v_ini:
        return f"{livro} {cap}"
    if v_fim and v_fim != v_ini:
        return f"{livro} {cap}:{v_ini}-{v_fim}"
    return f"{livro} {cap}:{v_ini}"


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Extrai referencias biblicas estruturadas de um texto.")
    ap.add_argument("--texto", required=True, help="Texto livre contendo referencias biblicas.")
    ap.add_argument("--data-dir", default=str(DATA_DIR), help="Diretorio com livros_biblia.json.")
    return ap.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        indice = carregar_livros(Path(args.data_dir))
    except FileNotFoundError as exc:
        print(json.dumps({"erro": f"dados nao encontrados: {exc}"}, ensure_ascii=False), file=sys.stderr)
        return 2
    refs = extrair(args.texto, indice)
    print(json.dumps({"texto": args.texto, "referencias": refs, "total": len(refs)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
