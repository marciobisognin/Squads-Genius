#!/usr/bin/env python3
"""Painel de saneamento do squad Farol Contratos & Licitações IFFar.

Transforma os achados da auditoria em uma fila de saneamento com status por
achado (PENDENTE → EM_ANALISE → CONFIRMADO_CAMPUS → CORRIGIDO → APROVADO ou
DESCARTADO) e gera um painel HTML de acompanhamento.

Uso:
    python scripts/painel_saneamento.py gerar output/auditoria/achados_auditoria.csv --out output/saneamento
    python scripts/painel_saneamento.py atualizar output/saneamento/saneamento.csv --id 5 --status CORRIGIDO --obs "Descrição revisada"
    python scripts/painel_saneamento.py painel output/saneamento/saneamento.csv --out output/saneamento/painel_saneamento.html
"""
from __future__ import annotations

import argparse
import csv
import html
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

STATUSES = ["PENDENTE", "EM_ANALISE", "CONFIRMADO_CAMPUS", "CORRIGIDO", "APROVADO", "DESCARTADO"]
FIELDS = ["id", "linha", "item", "codigo", "risco", "tipo", "achado", "valor_estimado", "status", "responsavel", "observacao", "atualizado_em"]
STATUS_COLORS = {
    "PENDENTE": "#ef4444", "EM_ANALISE": "#f59e0b", "CONFIRMADO_CAMPUS": "#38bdf8",
    "CORRIGIDO": "#a3e635", "APROVADO": "#34d399", "DESCARTADO": "#94a3b8",
}


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def cmd_gerar(args: argparse.Namespace) -> int:
    achados = read_rows(Path(args.achados))
    outdir = Path(args.out)
    rows = []
    for i, a in enumerate(achados, start=1):
        rows.append({
            "id": str(i),
            "linha": a.get("linha", ""),
            "item": a.get("item", ""),
            "codigo": a.get("codigo", ""),
            "risco": a.get("risco", ""),
            "tipo": a.get("tipo", ""),
            "achado": a.get("achado", ""),
            "valor_estimado": a.get("valor_estimado", ""),
            "status": "PENDENTE",
            "responsavel": "",
            "observacao": "",
            "atualizado_em": datetime.now().isoformat(timespec="seconds"),
        })
    path = outdir / "saneamento.csv"
    write_rows(path, rows)
    print(json.dumps({"status": "ok", "achados": len(rows), "saneamento": str(path)}, ensure_ascii=False, indent=2))
    return 0


def cmd_atualizar(args: argparse.Namespace) -> int:
    if args.status not in STATUSES:
        raise SystemExit(f"Status inválido: {args.status}. Use um de: {', '.join(STATUSES)}")
    path = Path(args.saneamento)
    rows = read_rows(path)
    updated = 0
    for row in rows:
        if (args.id and row.get("id") == str(args.id)) or (args.codigo and row.get("codigo") == str(args.codigo)):
            row["status"] = args.status
            if args.responsavel:
                row["responsavel"] = args.responsavel
            if args.obs:
                row["observacao"] = args.obs
            row["atualizado_em"] = datetime.now().isoformat(timespec="seconds")
            updated += 1
    if not updated:
        raise SystemExit("Nenhum achado encontrado com o id/código informado.")
    write_rows(path, rows)
    print(json.dumps({"status": "ok", "atualizados": updated, "novo_status": args.status}, ensure_ascii=False, indent=2))
    return 0


def cmd_painel(args: argparse.Namespace) -> int:
    rows = read_rows(Path(args.saneamento))
    counts = {s: 0 for s in STATUSES}
    for r in rows:
        counts[r.get("status", "PENDENTE")] = counts.get(r.get("status", "PENDENTE"), 0) + 1
    resolvidos = counts["APROVADO"] + counts["CORRIGIDO"] + counts["DESCARTADO"]
    progresso = (resolvidos / len(rows) * 100) if rows else 0.0
    cards = "".join(
        f'<div class="card" style="border-top:4px solid {STATUS_COLORS[s]}"><b>{s.replace("_", " ")}</b><span>{counts[s]}</span></div>'
        for s in STATUSES
    )
    body_rows = "".join(
        f'<tr><td>{html.escape(r.get("id", ""))}</td><td>{html.escape(r.get("codigo", ""))}</td>'
        f'<td>{html.escape(r.get("risco", ""))}</td><td>{html.escape(r.get("tipo", ""))}</td>'
        f'<td>{html.escape(r.get("achado", ""))}</td>'
        f'<td style="color:{STATUS_COLORS.get(r.get("status", "PENDENTE"), "#fff")}">{html.escape(r.get("status", ""))}</td>'
        f'<td>{html.escape(r.get("responsavel", ""))}</td><td>{html.escape(r.get("observacao", ""))}</td></tr>'
        for r in rows
    )
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Painel de Saneamento — Farol IFFar</title>
<style>body{{font-family:Arial,sans-serif;background:#0f172a;color:#e5e7eb;margin:0;padding:28px}}h1{{color:#93c5fd}}
.grid{{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}}.card{{background:#1e293b;border:1px solid #334155;border-radius:14px;padding:14px}}
.card span{{display:block;font-size:30px;color:#fbbf24}}.bar{{background:#1e293b;border-radius:10px;height:22px;margin:18px 0;overflow:hidden}}
.bar div{{background:#34d399;height:100%;text-align:right;padding-right:8px;color:#052e16;font-weight:bold}}
table{{width:100%;border-collapse:collapse;background:#111827;margin-top:18px}}td,th{{border:1px solid #374151;padding:8px;vertical-align:top}}th{{background:#1f2937}}.muted{{color:#94a3b8}}</style></head><body>
<h1>Painel de Saneamento — Farol Contratos & Licitações IFFar</h1>
<p class="muted">Achados em acompanhamento: {len(rows)} | Resolvidos (corrigido/aprovado/descartado): {resolvidos}</p>
<div class="bar"><div style="width:{progresso:.0f}%">{progresso:.0f}%</div></div>
<div class="grid">{cards}</div>
<table><tr><th>ID</th><th>Código</th><th>Risco</th><th>Tipo</th><th>Achado</th><th>Status</th><th>Responsável</th><th>Observação</th></tr>{body_rows}</table>
<p class="muted">Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.</p></body></html>"""
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(doc, encoding="utf-8")
    print(json.dumps({"status": "ok", "achados": len(rows), "progresso_pct": round(progresso, 1), "painel": str(out_path)}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="painel-saneamento", description="Fila e painel de saneamento dos achados de auditoria.")
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gerar", help="cria a fila de saneamento a partir do CSV de achados")
    g.add_argument("achados", help="caminho do achados_auditoria.csv")
    g.add_argument("--out", default="output/saneamento")
    g.set_defaults(func=cmd_gerar)
    a = sub.add_parser("atualizar", help="atualiza o status de um achado")
    a.add_argument("saneamento", help="caminho do saneamento.csv")
    a.add_argument("--id", help="id do achado na fila")
    a.add_argument("--codigo", help="atualiza todos os achados de um código de item")
    a.add_argument("--status", required=True, help="novo status: " + ", ".join(STATUSES))
    a.add_argument("--responsavel")
    a.add_argument("--obs")
    a.set_defaults(func=cmd_atualizar)
    pa = sub.add_parser("painel", help="gera painel HTML de acompanhamento")
    pa.add_argument("saneamento", help="caminho do saneamento.csv")
    pa.add_argument("--out", default="output/saneamento/painel_saneamento.html")
    pa.set_defaults(func=cmd_painel)
    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
