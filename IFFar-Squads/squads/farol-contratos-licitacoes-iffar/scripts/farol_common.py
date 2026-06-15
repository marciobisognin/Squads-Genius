#!/usr/bin/env python3
"""Módulo compartilhado do squad Farol Contratos & Licitações IFFar.

Concentra utilitários usados pelos demais scripts: normalização de texto e
números, datas relativas, cliente HTTP com retry/backoff e cache local,
estatística de preços e similaridade de descrições.
"""
from __future__ import annotations

import hashlib
import json
import re
import statistics
import time
import unicodedata
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

COMPRAS_BASE_URL = "https://dadosabertos.compras.gov.br"
USER_AGENT = "farol-contratos-licitacoes-iffar/1.3 (+compras-gov-cli)"

STOPWORDS = {
    "DE", "DA", "DO", "DAS", "DOS", "E", "EM", "COM", "PARA", "POR",
    "TIPO", "ITEM", "UNIDADE", "APROXIMADAMENTE", "MINIMO", "MINIMA",
}


def norm(s: Any) -> str:
    return re.sub(r"\s+", " ", str(s or "").strip()).upper()


def num(v: Any) -> Optional[float]:
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).replace(".", "").replace(",", "."))
    except Exception:
        return None


def date_range_default(days: int = 730) -> Tuple[str, str]:
    """Período padrão relativo: últimos `days` dias até hoje."""
    end = date.today()
    start = end - timedelta(days=days)
    return start.isoformat(), end.isoformat()


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def tokens(s: Any) -> Set[str]:
    text = strip_accents(norm(s))
    return {t for t in re.findall(r"[A-Z0-9]+", text) if len(t) >= 3 and t not in STOPWORDS}


def similarity(a: Any, b: Any) -> float:
    """Similaridade Jaccard entre tokens de duas descrições (0 a 1)."""
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def price_stats(prices: List[float]) -> Dict[str, float]:
    stats: Dict[str, float] = {}
    if prices:
        stats.update({
            "min": min(prices),
            "max": max(prices),
            "media": sum(prices) / len(prices),
            "mediana": statistics.median(prices),
        })
        if len(prices) >= 4:
            q = statistics.quantiles(prices, n=4, method="inclusive")
            stats.update({"q1": q[0], "q3": q[2]})
    return stats


def _cache_key(path: str, params: Dict[str, Any]) -> str:
    raw = path + "?" + urlencode(sorted((k, str(v)) for k, v in params.items()))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def fetch_json(path: str, params: Dict[str, Any], *, base_url: str = COMPRAS_BASE_URL,
               timeout: int = 60, retries: int = 3, backoff: float = 1.5,
               cache_dir: str | Path | None = None) -> Any:
    """GET JSON com retry exponencial e cache local opcional por URL."""
    cache_file = None
    if cache_dir:
        cache_file = Path(cache_dir) / (_cache_key(path, params) + ".json")
        if cache_file.exists():
            try:
                return json.loads(cache_file.read_text(encoding="utf-8"))
            except Exception:
                pass
    url = base_url + path + "?" + urlencode(params)
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urlopen(req, timeout=timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8", errors="replace"))
            if cache_file:
                cache_file.parent.mkdir(parents=True, exist_ok=True)
                cache_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            return payload
        except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            last_exc = exc
            if attempt < retries:
                time.sleep(backoff * (2 ** attempt))
    assert last_exc is not None
    raise last_exc


def compras_fetch_material_precos(codigo_item: Any, inicio: str, fim: str, paginas: int = 1,
                                  tamanho_pagina: int = 10, sleep: float = 0.05,
                                  cache_dir: str | Path | None = None) -> Dict[str, Any]:
    """Consulta preços praticados no módulo Pesquisa de Preços do Compras.gov.br."""
    rows: List[Dict[str, Any]] = []
    try:
        codigo = int(float(codigo_item))
    except Exception:
        return {"erro": "codigo_invalido", "registros": 0, "precos": [], "rows": []}
    for page in range(1, max(1, int(paginas)) + 1):
        params = {
            "codigoItemCatalogo": codigo,
            "dataCompraInicio": inicio,
            "dataCompraFim": fim,
            "pagina": page,
            "tamanhoPagina": max(10, int(tamanho_pagina)),
        }
        try:
            payload = fetch_json("/modulo-pesquisa-preco/1_consultarMaterial", params, cache_dir=cache_dir)
        except Exception as exc:
            return {"erro": str(exc)[:180], "registros": len(rows), "precos": [], "rows": rows}
        batch = payload.get("resultado") or []
        rows.extend(batch)
        total_pages = int(payload.get("totalPaginas") or 0)
        if not batch or (total_pages and page >= total_pages):
            break
        if sleep:
            time.sleep(sleep)
    prices = [p for p in (num(r.get("precoUnitario")) for r in rows) if p and p > 0]
    stats: Dict[str, Any] = {"registros": len(rows), "precos": prices, "rows": rows}
    stats.update(price_stats(prices))
    return stats
