#!/usr/bin/env python3
"""Utilitários determinísticos compartilhados do PDI Vivo IFFar Squad.

Sem dependências externas obrigatórias (Python 3.11+). Funções puras para
normalização de texto, IO de CSV/JSON, hashing de evidência e cálculo de
status/risco da matriz de metas. Tudo auditável e testável.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import unicodedata
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

# ---------------------------------------------------------------------------
# Vocabulário controlado (espelha schemas/*.schema.json)
# ---------------------------------------------------------------------------
STATUS_VALIDOS = [
    "não iniciada",
    "em planejamento",
    "em execução",
    "parcialmente concluída",
    "concluída",
    "atrasada",
    "suspensa",
    "requer decisão",
    "requer repactuação",
]

NIVEIS_RISCO = ["baixo", "médio", "alto", "crítico"]

PERIODICIDADES = ["mensal", "trimestral", "semestral", "anual", "bienal", "eventual"]

# Campos obrigatórios mínimos da matriz operacional de metas.
CAMPOS_OBRIGATORIOS = [
    "codigo",
    "ciclo",
    "dimensao",
    "meta",
    "indicador",
    "fonte_dados",
    "responsavel_nome",
    "periodicidade",
    "status",
    "risco",
]

# Conjunto completo de colunas recomendadas para a matriz central.
CAMPOS_MATRIZ = [
    "codigo",
    "ciclo",
    "dimensao",
    "objetivo",
    "meta",
    "acao",
    "campus",
    "unidade_responsavel",
    "responsavel_nome",
    "indicador",
    "linha_base",
    "meta_anual",
    "meta_2034",
    "fonte_dados",
    "evidencia_obrigatoria",
    "periodicidade",
    "status",
    "risco",
    "restricao_principal",
    "acao_corretiva",
    "ultima_atualizacao",
    "proxima_revisao",
]


# ---------------------------------------------------------------------------
# Normalização de texto
# ---------------------------------------------------------------------------
def strip_accents(text: str) -> str:
    """Remove acentos preservando o restante dos caracteres."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def norm(text: Any) -> str:
    """Normaliza espaços e caixa: 'Acesso  e   Inclusão ' -> 'ACESSO E INCLUSÃO'."""
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip().upper()


def slugify(text: str) -> str:
    """Converte texto livre em slug técnico ('Acesso e Inclusão' -> 'acesso-e-inclusao')."""
    base = strip_accents(str(text or "")).lower()
    base = re.sub(r"[^a-z0-9]+", "-", base)
    return base.strip("-")


def tokens(text: str) -> set[str]:
    """Tokens significativos (sem acento, sem stopwords curtas) para similaridade."""
    stop = {"de", "da", "do", "das", "dos", "e", "em", "a", "o", "as", "os", "para", "por", "com", "no", "na"}
    raw = re.findall(r"[a-z0-9]+", strip_accents(str(text or "")).lower())
    return {t for t in raw if t not in stop and len(t) > 1}


def similarity(a: str, b: str) -> float:
    """Similaridade de Jaccard entre dois textos (0.0 a 1.0)."""
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    union = len(ta | tb)
    return round(inter / union, 4) if union else 0.0


# ---------------------------------------------------------------------------
# Hashing / evidência auditável
# ---------------------------------------------------------------------------
def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# IO determinístico
# ---------------------------------------------------------------------------
def read_csv(path: str | Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: str | Path, rows: Iterable[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    rows = list(rows)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else CAMPOS_MATRIZ
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: ("" if row.get(k) is None else row.get(k)) for k in fieldnames})


def write_json(path: str | Path, data: Any) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def read_json(path: str | Path) -> Any:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def csv_to_string(rows: list[dict[str, Any]], fieldnames: list[str]) -> str:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: ("" if row.get(k) is None else row.get(k)) for k in fieldnames})
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Regras de status / risco
# ---------------------------------------------------------------------------
def parse_date(value: Any) -> date | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    s = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def is_overdue(proxima_revisao: Any, ref: date | None = None) -> bool:
    """Indica se a próxima revisão já venceu em relação à data de referência."""
    d = parse_date(proxima_revisao)
    if d is None:
        return False
    ref = ref or date.today()
    return d < ref


def derive_risk(meta: dict[str, Any], ref: date | None = None) -> str:
    """Deriva nível de risco a partir de status, atraso e lacunas de evidência.

    Regra determinística e conservadora: na dúvida, eleva o risco para revisão humana.
    """
    status = norm(meta.get("status"))
    declared = str(meta.get("risco") or "").strip().lower()
    overdue = is_overdue(meta.get("proxima_revisao"), ref)
    sem_indicador = not str(meta.get("indicador") or "").strip()
    sem_fonte = not str(meta.get("fonte_dados") or "").strip()
    sem_responsavel = not str(meta.get("responsavel_nome") or "").strip()

    # Status que exigem decisão sobem o risco automaticamente.
    if status in {"SUSPENSA", "REQUER DECISÃO", "REQUER REPACTUAÇÃO"}:
        base = "crítico"
    elif status == "ATRASADA" or overdue:
        base = "alto"
    elif sem_indicador or sem_fonte or sem_responsavel:
        base = "alto"
    elif status in {"NÃO INICIADA", "EM PLANEJAMENTO"}:
        base = "médio"
    else:
        base = "baixo"

    # Mantém o maior risco entre o declarado e o derivado.
    if declared in NIVEIS_RISCO:
        return max((base, declared), key=lambda r: NIVEIS_RISCO.index(r))
    return base


def is_critical(meta: dict[str, Any], ref: date | None = None) -> bool:
    return derive_risk(meta, ref) in {"alto", "crítico"}


FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."
