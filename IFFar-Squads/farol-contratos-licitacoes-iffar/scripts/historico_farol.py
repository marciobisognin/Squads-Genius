#!/usr/bin/env python3
"""Histórico de ciclos de auditoria do squad Farol Contratos & Licitações IFFar.

Permite registrar o resultado de cada execução (snapshot por ciclo) e comparar
ciclos para detectar recorrência de erros por item/tipo de achado.

Uso:
    python scripts/historico_farol.py registrar output/farol-iffar --ciclo 2026-1
    python scripts/historico_farol.py comparar --historico historico --out relatorio_historico.md
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def find_first(base: Path, pattern: str) -> Path | None:
    matches = sorted(base.rglob(pattern))
    return matches[0] if matches else None


def load_index(hist_dir: Path) -> Dict[str, Any]:
    index_path = hist_dir / "index.json"
    if index_path.exists():
        return json.loads(index_path.read_text(encoding="utf-8"))
    return {"ciclos": []}


def save_index(hist_dir: Path, index: Dict[str, Any]) -> None:
    (hist_dir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_registrar(args: argparse.Namespace) -> int:
    src = Path(args.resultado)
    hist_dir = Path(args.historico)
    summary_path = find_first(src, "summary_compras_gov.json") or find_first(src, "summary.json")
    achados_path = find_first(src, "achados_auditoria.csv")
    if not summary_path or not achados_path:
        raise SystemExit(f"Não encontrei summary*.json e achados_auditoria.csv em {src}. Rode a auditoria antes de registrar.")
    ciclo_dir = hist_dir / args.ciclo
    ciclo_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(summary_path, ciclo_dir / "summary.json")
    shutil.copy2(achados_path, ciclo_dir / "achados_auditoria.csv")
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    audit = summary.get("auditoria_dfd", summary)
    index = load_index(hist_dir)
    entry = {
        "ciclo": args.ciclo,
        "registrado_em": datetime.now().isoformat(timespec="seconds"),
        "itens_analisados": audit.get("items_analisados"),
        "achados": audit.get("achados"),
        "riscos": audit.get("riscos"),
        "valor_estimado_por_risco": audit.get("valor_estimado_por_risco"),
    }
    index["ciclos"] = [c for c in index["ciclos"] if c.get("ciclo") != args.ciclo] + [entry]
    index["ciclos"].sort(key=lambda c: c["ciclo"])
    save_index(hist_dir, index)
    print(json.dumps({"status": "ok", "ciclo": args.ciclo, "historico": str(ciclo_dir)}, ensure_ascii=False, indent=2))
    return 0


def load_achados(hist_dir: Path, ciclo: str) -> List[Dict[str, str]]:
    path = hist_dir / ciclo / "achados_auditoria.csv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def cmd_comparar(args: argparse.Namespace) -> int:
    hist_dir = Path(args.historico)
    index = load_index(hist_dir)
    ciclos = [c["ciclo"] for c in index["ciclos"]]
    if len(ciclos) < 1:
        raise SystemExit(f"Nenhum ciclo registrado em {hist_dir}. Use o subcomando `registrar` primeiro.")
    # recorrência: pares (código, tipo) que aparecem em mais de um ciclo
    presence: Dict[tuple, List[str]] = defaultdict(list)
    tipo_por_ciclo: Dict[str, Dict[str, int]] = {}
    for ciclo in ciclos:
        achados = load_achados(hist_dir, ciclo)
        tipos: Dict[str, int] = defaultdict(int)
        seen = set()
        for a in achados:
            tipos[a.get("tipo", "?")] += 1
            key = (a.get("codigo", ""), a.get("tipo", ""))
            if key not in seen and a.get("codigo"):
                presence[key].append(ciclo)
                seen.add(key)
        tipo_por_ciclo[ciclo] = dict(tipos)
    recorrentes = sorted(
        [(codigo, tipo, cs) for (codigo, tipo), cs in presence.items() if len(cs) >= 2],
        key=lambda x: -len(x[2]),
    )
    lines = ["# Relatório de Histórico — Farol Contratos & Licitações IFFar", ""]
    lines.append(f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} a partir de {len(ciclos)} ciclo(s): {', '.join(ciclos)}.")
    lines.append("\n## Evolução por ciclo\n")
    lines.append("| Ciclo | Itens | Achados | ALTO | MÉDIO | BAIXO | OK |")
    lines.append("|---|---|---|---|---|---|---|")
    for c in index["ciclos"]:
        riscos = c.get("riscos") or {}
        lines.append(f"| {c['ciclo']} | {c.get('itens_analisados', '—')} | {c.get('achados', '—')} | {riscos.get('ALTO', 0)} | {riscos.get('MÉDIO', 0)} | {riscos.get('BAIXO', 0)} | {riscos.get('OK', 0)} |")
    lines.append("\n## Achados por tipo em cada ciclo\n")
    for ciclo, tipos in tipo_por_ciclo.items():
        resumo = ", ".join(f"{k}: {v}" for k, v in sorted(tipos.items(), key=lambda x: -x[1])) or "sem achados"
        lines.append(f"- **{ciclo}**: {resumo}")
    lines.append("\n## Itens com achados recorrentes (2+ ciclos)\n")
    if recorrentes:
        for codigo, tipo, cs in recorrentes[:40]:
            lines.append(f"- Código {codigo} — {tipo}: presente em {len(cs)} ciclos ({', '.join(cs)}). Priorizar saneamento definitivo e registro na base de conhecimento.")
    else:
        lines.append("- Nenhuma recorrência identificada entre os ciclos registrados.")
    lines.append("\nLicença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.")
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "ciclos": ciclos, "recorrencias": len(recorrentes), "relatorio": str(out_path)}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="historico-farol", description="Registra e compara ciclos de auditoria DFD.")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("registrar", help="registra o resultado de uma auditoria como snapshot de ciclo")
    r.add_argument("resultado", help="diretório de saída de uma execução do squad (ex.: output/farol-iffar)")
    r.add_argument("--ciclo", required=True, help="identificador do ciclo, ex.: 2026-1")
    r.add_argument("--historico", default="historico", help="diretório onde os snapshots são guardados")
    r.set_defaults(func=cmd_registrar)
    c = sub.add_parser("comparar", help="compara os ciclos registrados e aponta recorrências")
    c.add_argument("--historico", default="historico")
    c.add_argument("--out", default="historico/relatorio_historico.md")
    c.set_defaults(func=cmd_comparar)
    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
