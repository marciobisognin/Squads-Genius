#!/usr/bin/env python3
"""Gera a matriz de pacto territorial por campus a partir da matriz central.

Filtra metas por campus, consolida responsabilidades locais, restrições e riscos,
e produz um pacto por campus (CSV) e um documento Markdown pronto para devolutiva.

Uso:
    python3 build_campus_pact.py --input matriz_metas.csv --campus "São Borja" \
        --output-dir output/pactos/
    python3 build_campus_pact.py --input matriz_metas.csv --all --output-dir output/pactos/
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdi_common import derive_risk, norm, read_csv, slugify, write_csv  # noqa: E402


def campi_disponiveis(rows: list[dict]) -> list[str]:
    valores = {str(r.get("campus") or "").strip() for r in rows}
    return sorted(v for v in valores if v)


def filtra(rows: list[dict], campus: str) -> list[dict]:
    alvo = norm(campus)
    return [r for r in rows if norm(r.get("campus")) == alvo]


def to_markdown(campus: str, metas: list[dict]) -> str:
    criticas = [m for m in metas if derive_risk(m) in {"alto", "crítico"}]
    out = [f"# Pacto Territorial — Campus {campus}", ""]
    out.append(f"- Metas pactuadas: **{len(metas)}**")
    out.append(f"- Metas de atenção (risco alto/crítico): **{len(criticas)}**")
    out.append("")
    out.append("## Metas")
    out.append("| Código | Dimensão | Meta | Responsável | Indicador | Status | Risco | Restrição |")
    out.append("|---|---|---|---|---|---|---|---|")
    for m in metas:
        out.append(
            "| {codigo} | {dimensao} | {meta} | {resp} | {ind} | {status} | {risco} | {restr} |".format(
                codigo=m.get("codigo", ""),
                dimensao=m.get("dimensao", ""),
                meta=(m.get("meta", "")[:80]),
                resp=m.get("responsavel_nome", ""),
                ind=(m.get("indicador", "")[:40]),
                status=m.get("status", ""),
                risco=derive_risk(m),
                restr=(m.get("restricao_principal", "")[:40]),
            )
        )
    out.append("")
    out.append("## Compromissos locais")
    out.append("- Responsáveis confirmam metas, indicadores e prazos.")
    out.append("- Restrições de orçamento, infraestrutura, equipe e dados registradas acima.")
    out.append("- Próxima devolutiva no ciclo trimestral de acompanhamento.")
    out.append("")
    out.append("Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.")
    out.append("")
    return "\n".join(out)


def gerar(rows: list[dict], campus: str, out_dir: Path) -> int:
    metas = filtra(rows, campus)
    slug = slugify(campus)
    write_csv(out_dir / f"pacto_{slug}.csv", metas)
    (out_dir / f"pacto_{slug}.md").write_text(to_markdown(campus, metas), encoding="utf-8")
    return len(metas)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Gera pacto territorial por campus.")
    ap.add_argument("--input", required=True, help="Matriz de metas (CSV).")
    ap.add_argument("--campus", default=None, help="Nome do campus.")
    ap.add_argument("--all", action="store_true", help="Gera pacto para todos os campi.")
    ap.add_argument("--output-dir", default="output/pactos")
    args = ap.parse_args(argv)

    rows = read_csv(args.input)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.all:
        alvos = campi_disponiveis(rows)
        if not alvos:
            raise SystemExit("Nenhum campus preenchido na matriz.")
    elif args.campus:
        alvos = [args.campus]
    else:
        raise SystemExit("Informe --campus NOME ou --all.")

    for campus in alvos:
        n = gerar(rows, campus, out_dir)
        print(f"OK: pacto {campus} -> {n} metas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
