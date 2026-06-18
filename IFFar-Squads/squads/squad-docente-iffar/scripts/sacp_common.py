#!/usr/bin/env python3
"""Funções compartilhadas pelos scripts determinísticos do Squad Docente IFFar.

Sem dependências externas — apenas biblioteca padrão do Python 3.11+.
"""
from __future__ import annotations

import csv
import json
from datetime import date, datetime
from pathlib import Path


def read_json(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: str | Path, data) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def read_csv(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: str | Path, rows: list[dict]) -> None:
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_date(value: str) -> date | None:
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except (ValueError, TypeError):
            continue
    return None


def is_dia_letivo(d: date, feriados: set[date], dias_sem_aula: set[int]) -> bool:
    """dias_sem_aula: conjunto de weekday() sem aula (0=segunda ... 6=domingo)."""
    if d.weekday() in dias_sem_aula:
        return False
    if d in feriados:
        return False
    return True


def days_until(target: date, today: date | None = None) -> int:
    today = today or date.today()
    return (target - today).days
