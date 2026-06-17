#!/usr/bin/env python3
"""Constrói a matriz operacional preliminar de metas a partir do texto do PDI.

Heurística determinística: identifica dimensões/eixos, objetivos, metas e ações por
padrões de numeração e palavras-chave, e produz uma matriz com os campos do modelo
mínimo de dados. Os campos não inferíveis ficam vazios para preenchimento humano —
o script nunca inventa indicador, fonte, responsável ou prazo.

Uso:
    python3 build_goal_matrix.py --input extracoes/pdi.txt --ciclo 2027-2034 \
        --output matriz_metas.csv --json matriz_metas.json
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdi_common import CAMPOS_MATRIZ, norm, write_csv, write_json  # noqa: E402

# Padrões de detecção (conservadores).
RE_DIMENSAO = re.compile(
    r"^\s*(?:dimens[ãa]o|eixo|pol[íi]tica|cap[íi]tulo)\b[\s:–-]*(.+)$", re.IGNORECASE
)
RE_OBJETIVO = re.compile(r"^\s*objetivo\b[\s:0-9.–-]*(.+)$", re.IGNORECASE)
RE_META = re.compile(r"^\s*(?:meta|m)\s*[:.\-]?\s*([0-9]+[.0-9]*)\s*[)\.:–-]?\s*(.+)$", re.IGNORECASE)
RE_ACAO = re.compile(r"^\s*(?:a[çc][ãa]o|estrat[ée]gia)\b[\s:0-9.–-]*(.+)$", re.IGNORECASE)
RE_META_GENERICA = re.compile(r"\bmeta\b", re.IGNORECASE)


def parse_lines(text: str) -> list[dict]:
    """Percorre as linhas mantendo o contexto de dimensão/objetivo corrente."""
    dimensao = ""
    objetivo = ""
    metas: list[dict] = []
    seq = 0

    for raw in text.splitlines():
        line = raw.strip()
        if not line or len(line) < 4:
            continue

        m_dim = RE_DIMENSAO.match(line)
        if m_dim and len(m_dim.group(1)) > 3:
            dimensao = m_dim.group(1).strip(" .:–-")
            continue

        m_obj = RE_OBJETIVO.match(line)
        if m_obj and len(m_obj.group(1)) > 3:
            objetivo = m_obj.group(1).strip(" .:–-")
            continue

        m_meta = RE_META.match(line)
        if m_meta and len(m_meta.group(2)) > 5:
            seq += 1
            metas.append(_row(seq, dimensao, objetivo, m_meta.group(2).strip(), m_meta.group(1)))
            continue

        # Linha que menciona "meta" textualmente mas não casa o padrão numerado.
        if RE_META_GENERICA.search(line) and len(line) > 25 and not RE_ACAO.match(line):
            seq += 1
            metas.append(_row(seq, dimensao, objetivo, line, ""))

    return metas


def _row(seq: int, dimensao: str, objetivo: str, meta: str, num: str) -> dict:
    codigo = f"M-{seq:03d}" if not num else f"M-{num}"
    row = {campo: "" for campo in CAMPOS_MATRIZ}
    row.update(
        {
            "codigo": codigo,
            "dimensao": dimensao,
            "objetivo": objetivo,
            "meta": re.sub(r"\s+", " ", meta).strip(),
            "status": "não iniciada",
        }
    )
    return row


def dedupe(rows: list[dict]) -> list[dict]:
    seen: set[str] = set()
    unique: list[dict] = []
    for row in rows:
        key = norm(row["meta"])[:120]
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Gera matriz preliminar de metas do PDI.")
    ap.add_argument("--input", required=True, help="Arquivo de texto extraído (.txt).")
    ap.add_argument("--ciclo", default="2027-2034", help="Ciclo do PDI (ex.: 2027-2034).")
    ap.add_argument("--output", default="matriz_metas.csv", help="CSV de saída.")
    ap.add_argument("--json", default=None, help="JSON de saída opcional.")
    args = ap.parse_args(argv)

    text = Path(args.input).read_text(encoding="utf-8", errors="ignore")
    rows = dedupe(parse_lines(text))
    for row in rows:
        row["ciclo"] = args.ciclo

    write_csv(args.output, rows, CAMPOS_MATRIZ)
    if args.json:
        write_json(args.json, rows)

    print(f"OK: {len(rows)} metas preliminares -> {args.output}")
    print("AVISO: indicadores, fontes, responsáveis e prazos exigem preenchimento humano.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
