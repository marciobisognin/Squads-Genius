#!/usr/bin/env python3
"""Funções compartilhadas do PROJUR Contracts Squad.

Determinístico, Python 3.11+, somente biblioteca padrão.
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------- IO
def read_json(path: str | Path, default: Any = None) -> Any:
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(path: str | Path, data: Any) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return p


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ------------------------------------------------------------------------- TEXTO
def strip_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_text(text: str) -> str:
    """Normaliza para comparação/similaridade: minúsculas, sem acento, espaços colapsados."""
    text = strip_accents(text).lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def similarity(a: str, b: str) -> float:
    """Similaridade 0..1 entre dois textos (difflib sobre texto normalizado)."""
    from difflib import SequenceMatcher
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()


# ------------------------------------------------------------------- VALOR / DATA
def parse_money_br(raw: str) -> float | None:
    """Converte 'R$ 1.234.567,89' -> 1234567.89."""
    if raw is None:
        return None
    m = re.search(r"(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2}|\d+(?:\.\d+)?)", raw)
    if not m:
        return None
    s = m.group(1)
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def parse_date_br(raw: str) -> str | None:
    """Extrai data dd/mm/aaaa e retorna ISO aaaa-mm-dd."""
    if raw is None:
        return None
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})", raw)
    if not m:
        return None
    d, mo, y = m.groups()
    return f"{y}-{mo}-{d}"


# ----------------------------------------------------------------- CNPJ / CPF
def _digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")


def valid_cpf(raw: str) -> bool:
    cpf = _digits(raw)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in (9, 10):
        s = sum(int(cpf[n]) * ((i + 1) - n) for n in range(i))
        dv = (s * 10) % 11 % 10
        if dv != int(cpf[i]):
            return False
    return True


def valid_cnpj(raw: str) -> bool:
    cnpj = _digits(raw)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1
    for pesos, pos in ((pesos1, 12), (pesos2, 13)):
        s = sum(int(cnpj[n]) * pesos[n] for n in range(pos))
        dv = 11 - (s % 11)
        dv = 0 if dv >= 10 else dv
        if dv != int(cnpj[pos]):
            return False
    return True


def classify_document(raw: str) -> tuple[str, bool]:
    """Retorna (tipo_documento, valido) para um CNPJ/CPF."""
    d = _digits(raw)
    if len(d) == 14:
        return "CNPJ", valid_cnpj(d)
    if len(d) == 11:
        return "CPF", valid_cpf(d)
    return "desconhecido", False
