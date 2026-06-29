#!/usr/bin/env python3
"""Utilidades compartilhadas do Forge of Solus Prime (estrato KÝKLOS).

Carrega briefings YAML/JSON sem depender de bibliotecas externas: usa PyYAML
quando disponível e, caso contrário, um parser determinístico de um subconjunto
de YAML suficiente para o schema de briefing da Disciplina FORJA.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

try:  # PyYAML é opcional — mantém o squad portável (Termux, CI mínimo).
    import yaml  # type: ignore
except Exception:  # pragma: no cover - caminho de fallback
    yaml = None


_INT_RE = re.compile(r"^-?\d+$")
_FLOAT_RE = re.compile(r"^-?\d+\.\d+$")


def _coerce_scalar(token: str) -> Any:
    """Converte um escalar textual em int/float/bool/None/str de forma estável."""
    text = token.strip()
    if (text.startswith('"') and text.endswith('"')) or (
        text.startswith("'") and text.endswith("'")
    ):
        return text[1:-1]
    low = text.lower()
    if low in {"true", "yes"}:
        return True
    if low in {"false", "no"}:
        return False
    if low in {"null", "none", "~", ""}:
        return None
    if _INT_RE.match(text):
        return int(text)
    if _FLOAT_RE.match(text):
        return float(text)
    return text


def _mini_yaml(text: str) -> dict[str, Any]:
    """Parser de subconjunto YAML: mapeamentos de topo, listas e um nível aninhado.

    Cobre exatamente o schema de briefing (escalares, listas ``- item`` e um
    mapeamento aninhado como ``budget_limit``). Determinístico e auditável.
    """
    root: dict[str, Any] = {}
    current_list_key: str | None = None
    current_map_key: str | None = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip() if "#" in raw and not raw.strip().startswith("#") else raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if stripped.startswith("- "):
            if current_list_key is None:
                continue
            root.setdefault(current_list_key, [])
            root[current_list_key].append(_coerce_scalar(stripped[2:]))
            continue
        if ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()
        if indent >= 2 and current_map_key is not None:
            target = root.setdefault(current_map_key, {})
            if isinstance(target, dict):
                target[key] = _coerce_scalar(value)
            continue
        # chave de topo
        current_list_key = None
        current_map_key = None
        if value == "":
            # Pode iniciar uma lista ou um mapeamento aninhado.
            current_list_key = key
            current_map_key = key
            root.setdefault(key, None)
        else:
            root[key] = _coerce_scalar(value)
    # Normaliza chaves que ficaram como None mas sem itens.
    for key, val in list(root.items()):
        if val is None:
            root[key] = None
    return root


def load_briefing(path: str | Path) -> dict[str, Any]:
    """Lê um briefing YAML/JSON e devolve um dicionário Python."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() == ".json":
        return json.loads(text)
    if yaml is not None:
        data = yaml.safe_load(text)
        if isinstance(data, dict):
            return data
    return _mini_yaml(text)


def briefing_keywords(briefing: dict[str, Any]) -> list[str]:
    """Extrai termos de busca determinísticos a partir do briefing."""
    blob_parts: list[str] = []
    for field in ("project_name", "objective", "problem", "target_audience"):
        val = briefing.get(field)
        if isinstance(val, str):
            blob_parts.append(val)
    for field in ("expected_outputs", "integrations", "constraints"):
        val = briefing.get(field)
        if isinstance(val, list):
            blob_parts.extend(str(x) for x in val)
    blob = " ".join(blob_parts).lower()
    tokens = re.findall(r"[a-zà-ú0-9_]{4,}", blob)
    stop = {
        "para", "como", "esse", "essa", "este", "esta", "uma", "uns", "umas",
        "com", "sem", "que", "dos", "das", "por", "mais", "ser", "são", "seu",
        "sua", "the", "and", "for", "with", "from", "into", "user", "será",
    }
    seen: list[str] = []
    for tok in tokens:
        if tok in stop or tok in seen:
            continue
        seen.append(tok)
    return seen[:24]


def write_json(path: str | Path, data: Any) -> Path:
    """Serializa ``data`` como JSON indentado e estável."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False), encoding="utf-8")
    return p


FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."


if __name__ == "__main__":  # pragma: no cover - uso utilitário
    import sys

    if len(sys.argv) > 1:
        print(json.dumps(load_briefing(sys.argv[1]), ensure_ascii=False, indent=2))
    else:
        print("uso: forge_common.py <briefing.yaml|json>")
