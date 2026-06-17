#!/usr/bin/env python3
"""Smoke test do PDI Vivo IFFar Squad.

Verifica estrutura de arquivos, compilação dos scripts e executa o pipeline
offline sobre a matriz de exemplo: extração sintética -> matriz -> validação ->
riscos -> pacto por campus -> relatório trimestral -> painel HTML.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

REQUIRED = [
    "squad.yaml",
    "README.md",
    "PRD.md",
    "LICENSE",
    "NOTICE.md",
    "AUTHORS.md",
    "CHANGELOG.md",
    "requirements.txt",
    "scripts/pdi_common.py",
    "scripts/extract_pdi_text.py",
    "scripts/build_goal_matrix.py",
    "scripts/validate_indicator_matrix.py",
    "scripts/compare_pdi_cycles.py",
    "scripts/build_campus_pact.py",
    "scripts/risk_matrix.py",
    "scripts/generate_quarterly_report.py",
    "scripts/render_dashboard.py",
    "schemas/goal.schema.json",
    "schemas/indicator.schema.json",
    "schemas/risk.schema.json",
    "schemas/evidence.schema.json",
    "examples/matriz_metas_exemplo.csv",
    "examples/gerar_exemplo.py",
]


def run(cmd: list[str], cwd: Path) -> None:
    print("  $", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def main() -> int:
    print("== 1. Arquivos obrigatórios ==")
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing:
        raise SystemExit("Arquivos ausentes: " + ", ".join(missing))
    print(f"  OK ({len(REQUIRED)} arquivos)")

    print("== 2. Compilação dos scripts ==")
    import py_compile

    for py in sorted(SCRIPTS.glob("*.py")):
        py_compile.compile(str(py), doraise=True)
    print("  OK")

    print("== 3. Validação de JSON Schemas ==")
    for sch in sorted((ROOT / "schemas").glob("*.json")):
        json.loads(sch.read_text(encoding="utf-8"))
    print("  OK")

    print("== 4. Pipeline offline ==")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        matriz = ROOT / "examples" / "matriz_metas_exemplo.csv"

        # 4a. Extração sintética + matriz preliminar
        synth = tmp / "pdi_sintetico.txt"
        run([sys.executable, str(ROOT / "examples" / "gerar_exemplo.py"), "--output", str(synth)], ROOT)
        run([sys.executable, str(SCRIPTS / "build_goal_matrix.py"),
             "--input", str(synth), "--output", str(tmp / "matriz_preliminar.csv"),
             "--json", str(tmp / "matriz_preliminar.json")], ROOT)
        prelim = json.loads((tmp / "matriz_preliminar.json").read_text(encoding="utf-8"))
        assert len(prelim) >= 5, f"esperava >=5 metas extraídas, obtive {len(prelim)}"

        # 4b. Validação (matriz de exemplo deve gerar achados, mas rodar sem erro)
        run([sys.executable, str(SCRIPTS / "validate_indicator_matrix.py"),
             "--input", str(matriz), "--report", str(tmp / "quality_report.json")], ROOT)
        report = json.loads((tmp / "quality_report.json").read_text(encoding="utf-8"))
        assert report["total_metas"] == 10, report["total_metas"]

        # 4c. Riscos
        run([sys.executable, str(SCRIPTS / "risk_matrix.py"),
             "--input", str(matriz), "--output-dir", str(tmp)], ROOT)
        assert (tmp / "matriz_riscos.csv").exists()

        # 4d. Comparativo de ciclos (usa o mesmo texto sintético duas vezes)
        run([sys.executable, str(SCRIPTS / "compare_pdi_cycles.py"),
             "--anterior", str(synth), "--novo", str(synth), "--output-dir", str(tmp)], ROOT)
        assert (tmp / "comparativo_ciclos.md").exists()

        # 4e. Pacto por campus (todos)
        run([sys.executable, str(SCRIPTS / "build_campus_pact.py"),
             "--input", str(matriz), "--all", "--output-dir", str(tmp / "pactos")], ROOT)
        assert list((tmp / "pactos").glob("pacto_*.md")), "nenhum pacto gerado"

        # 4f. Relatório trimestral
        run([sys.executable, str(SCRIPTS / "generate_quarterly_report.py"),
             "--input", str(matriz), "--output", str(tmp / "relatorio.md")], ROOT)
        assert (tmp / "relatorio.md").stat().st_size > 200

        # 4g. Painel HTML
        run([sys.executable, str(SCRIPTS / "render_dashboard.py"),
             "--input", str(matriz), "--output", str(tmp / "dashboard.html")], ROOT)
        html = (tmp / "dashboard.html").read_text(encoding="utf-8")
        assert "Painel PDI Vivo IFFar" in html

    print("  OK")
    print("\nSMOKE TEST: PASSOU ✅")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
