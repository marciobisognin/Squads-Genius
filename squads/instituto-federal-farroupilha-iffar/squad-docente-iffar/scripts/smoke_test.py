#!/usr/bin/env python3
"""Smoke test offline do pipeline determinístico do Squad Docente IFFar.

Executa cronograma → validação de plano → checagem de prazos com dados
sintéticos em um diretório temporário, sem chamadas externas.

Uso:
    python3 smoke_test.py
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        topicos_path = tmp / "topicos.json"
        topicos_path.write_text(json.dumps(["Introdução", "Conceito A", "Conceito B", "Revisão"]), encoding="utf-8")

        cronograma_path = tmp / "cronograma.json"
        run([
            sys.executable, str(SCRIPTS_DIR / "build_cronograma.py"),
            "--topicos", str(topicos_path),
            "--inicio", "2026-08-03",
            "--fim", "2026-08-31",
            "--output", str(cronograma_path),
        ])

        cronograma = json.loads(cronograma_path.read_text(encoding="utf-8"))
        plano = {
            "componente_id": "COMP-001",
            "curso_id": "CURSO-001",
            "ementa": "Ementa de exemplo",
            "objetivos": ["Objetivo 1"],
            "metodologia": "Aulas expositivas e práticas",
            "conteudo_programatico": ["Introdução", "Conceito A", "Conceito B", "Revisão"],
            "avaliacao": "Prova e trabalho",
            "referencias": ["Referência 1"],
            "cronograma": cronograma["cronograma"],
            "veredito_curricular": "conforme",
            "status_homologacao": "em_revisao",
        }
        plano_path = tmp / "plano.json"
        plano_path.write_text(json.dumps(plano, ensure_ascii=False), encoding="utf-8")

        report_path = tmp / "quality_report.json"
        run([
            sys.executable, str(SCRIPTS_DIR / "validate_plano_ensino.py"),
            "--input", str(plano_path),
            "--report", str(report_path),
        ])

        agenda_path = tmp / "agenda.json"
        agenda_path.write_text(json.dumps([
            {"descricao": "Entrega do Plano de Ensino", "data_limite": "2026-07-01", "dispositivo_rdp": "Art. 12"},
        ]), encoding="utf-8")
        alertas_path = tmp / "alertas.json"
        run([
            sys.executable, str(SCRIPTS_DIR / "check_prazos.py"),
            "--agenda", str(agenda_path),
            "--hoje", "2026-06-18",
            "--output", str(alertas_path),
        ])

        print("\nSmoke test concluído com sucesso. Pipeline offline íntegro.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
