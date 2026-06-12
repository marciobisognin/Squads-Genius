#!/usr/bin/env python3
"""Comando unificado do squad Farol Contratos & Licitações IFFar."""
from __future__ import annotations

import argparse
import html
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
ENRIQUECER = ROOT / "scripts" / "enriquecer_dfd_compras_gov.py"
PNCP = ROOT / "scripts" / "pncp_busca_termo.py"


def run(cmd: List[str]) -> None:
    print("+", " ".join(str(c) for c in cmd), file=sys.stderr)
    subprocess.run(cmd, check=True)


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def money(v: Any) -> str:
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "—"


def build_mapa(outdir: Path) -> Path:
    summary_path = outdir / "summary_compras_gov.json"
    summary = load_json(summary_path)
    compras_json = Path(summary["compras_gov"]["arquivo_json"])
    rows = json.loads(compras_json.read_text(encoding="utf-8"))
    cards = []
    for row in rows:
        code = html.escape(str(row.get("codigoItemCatalogo", "")))
        desc = html.escape(str(row.get("descricaoAmostra") or "Sem descrição amostra"))
        registros = row.get("registros", 0)
        med = money(row.get("mediana"))
        minimo = money(row.get("min"))
        maximo = money(row.get("max"))
        cards.append(f"""
        <tr>
          <td>{code}</td><td>{registros}</td><td>{minimo}</td><td>{med}</td><td>{maximo}</td><td>{desc}</td>
        </tr>""")
    enrich = summary.get("enriquecimento", {})
    html_doc = f"""<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>Mapa Comparativo Farol IFFar</title>
<style>body{{font-family:Arial,sans-serif;background:#0b1220;color:#eef2ff;margin:0;padding:28px}}h1{{color:#93c5fd}}.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}.card{{background:#172033;border:1px solid #2d3b55;border-radius:14px;padding:16px}}.card b{{display:block;color:#fbbf24;font-size:30px}}table{{width:100%;border-collapse:collapse;margin-top:18px;background:#111827}}th,td{{border:1px solid #334155;padding:8px;vertical-align:top}}th{{background:#1e293b}}small{{color:#94a3b8}}</style></head><body>
<h1>Mapa Comparativo — Farol Contratos & Licitações IFFar + Compras.gov</h1>
<p>Planilha: <code>{html.escape(Path(summary['planilha_original']).name)}</code></p>
<div class='grid'>
<div class='card'>Itens auditados<b>{summary['auditoria_dfd'].get('items_analisados')}</b></div>
<div class='card'>Códigos pesquisados<b>{summary['compras_gov'].get('codigos_pesquisados')}</b></div>
<div class='card'>Itens enriquecidos<b>{enrich.get('itens_enriquecidos')}</b></div>
<div class='card'>Alertas preço<b>{enrich.get('alertas_preco')}</b></div>
</div>
<h2>Resumo de preços externos por código</h2>
<table><tr><th>Código</th><th>Registros</th><th>Mínimo</th><th>Mediana</th><th>Máximo</th><th>Descrição amostra</th></tr>{''.join(cards)}</table>
<p><small>A mediana Compras.gov é evidência de apoio, não decisão automática. Validar equivalência de descrição/unidade antes de usar como referência final.</small></p>
<p><small>Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.</small></p>
</body></html>"""
    path = outdir / "mapa_comparativo_compras_gov.html"
    path.write_text(html_doc, encoding="utf-8")
    return path


def cmd_analisar(args: argparse.Namespace) -> int:
    outdir = Path(args.out)
    cmd = [sys.executable, str(ENRIQUECER), args.planilha, "--inicio", args.inicio, "--fim", args.fim, "--paginas", str(args.paginas), "--out", str(outdir), "--sleep", str(args.sleep)]
    if args.max_itens:
        cmd += ["--max-itens", str(args.max_itens)]
    run(cmd)
    mapa = build_mapa(outdir)
    if args.termo_pncp:
        pncp_out = outdir / "03_pncp_termo"
        run([sys.executable, str(PNCP), args.termo_pncp, "--inicio", args.inicio, "--fim", args.fim, "--modalidade", str(args.modalidade), "--uf", args.uf, "--paginas", str(args.pncp_paginas), "--out", str(pncp_out)])
    summary = load_json(outdir / "summary_compras_gov.json")
    final = {
        "status": "ok",
        "outdir": str(outdir),
        "planilha_enriquecida": summary["enriquecimento"]["saida"],
        "relatorio_compras_gov": summary["relatorio_compras_gov"],
        "mapa_comparativo": str(mapa),
        "summary": str(outdir / "summary_compras_gov.json"),
    }
    print(json.dumps(final, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="farol-iffar", description="Comando unificado do squad Farol Contratos & Licitações IFFar.")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analisar", help="audita DFD, consulta Compras.gov e gera mapa comparativo")
    a.add_argument("planilha")
    a.add_argument("--inicio", default="2024-01-01")
    a.add_argument("--fim", default="2026-12-31")
    a.add_argument("--paginas", type=int, default=2)
    a.add_argument("--sleep", type=float, default=0.15)
    a.add_argument("--max-itens", type=int)
    a.add_argument("--out", default="output/farol-iffar")
    a.add_argument("--termo-pncp", help="termo para busca complementar em contratações PNCP")
    a.add_argument("--modalidade", type=int, default=6)
    a.add_argument("--uf", default="RS")
    a.add_argument("--pncp-paginas", type=int, default=3)
    a.set_defaults(func=cmd_analisar)
    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
