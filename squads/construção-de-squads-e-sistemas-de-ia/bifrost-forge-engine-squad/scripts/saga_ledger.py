#!/usr/bin/env python3
"""Saga Ledger — trilha de auditoria encadeada por hash (JSONL + SHA256).

Cada evento da forja vira uma "saga": uma linha JSON com hash do próprio conteúdo
encadeado ao hash do evento anterior. Adulterar qualquer linha quebra a cadeia,
o que permite verificar integridade determinística de ponta a ponta.

Uso como biblioteca:
    ledger = SagaLedger(path, deterministic=True)
    ledger.record("intake", "phase_start", {"briefing": "x"})
    ok, issues = SagaLedger.verify(path)

Uso como CLI:
    python3 saga_ledger.py --verify <ledger.jsonl>

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

GENESIS = "0" * 64
FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."


def _canonical(payload: Any) -> str:
    """Serialização canônica e estável para hashing reprodutível."""
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _hash_entry(prev_hash: str, body: Dict[str, Any]) -> str:
    material = prev_hash + "|" + _canonical(body)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


class SagaLedger:
    """Escritor append-only de eventos com cadeia de hash SHA256."""

    def __init__(self, path: str | Path, deterministic: bool = False) -> None:
        self.path = Path(path)
        self.deterministic = deterministic
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._seq = 0
        self._last_hash = GENESIS
        if self.path.exists():
            entries = self.read(self.path)
            if entries:
                self._seq = entries[-1]["seq"]
                self._last_hash = entries[-1]["entry_hash"]

    def _timestamp(self) -> str:
        if self.deterministic:
            # Relógio lógico: mantém a reprodutibilidade bit-a-bit da trilha.
            return f"T{self._seq + 1:06d}"
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def record(self, phase: str, event: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._seq += 1
        body = {
            "seq": self._seq,
            "ts": self._timestamp(),
            "phase": phase,
            "event": event,
            "payload": payload or {},
            "prev_hash": self._last_hash,
        }
        body["entry_hash"] = _hash_entry(self._last_hash, body)
        self._last_hash = body["entry_hash"]
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(_canonical(body) + "\n")
        return body

    @property
    def head(self) -> str:
        return self._last_hash

    @staticmethod
    def read(path: str | Path) -> List[Dict[str, Any]]:
        p = Path(path)
        if not p.exists():
            return []
        entries: List[Dict[str, Any]] = []
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                entries.append(json.loads(line))
        return entries

    @staticmethod
    def verify(path: str | Path) -> Tuple[bool, List[str]]:
        entries = SagaLedger.read(path)
        issues: List[str] = []
        prev = GENESIS
        for idx, entry in enumerate(entries, start=1):
            if entry.get("seq") != idx:
                issues.append(f"sequência quebrada na linha {idx}: seq={entry.get('seq')}")
            if entry.get("prev_hash") != prev:
                issues.append(f"encadeamento quebrado na linha {idx}")
            body = {k: entry[k] for k in ("seq", "ts", "phase", "event", "payload", "prev_hash")}
            expected = _hash_entry(prev, body)
            if entry.get("entry_hash") != expected:
                issues.append(f"hash adulterado na linha {idx}")
            prev = entry.get("entry_hash", "")
        return (not issues), issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Verifica a integridade de um Saga Ledger.")
    ap.add_argument("--verify", required=True, help="Caminho do ledger .jsonl a verificar.")
    args = ap.parse_args()
    ok, issues = SagaLedger.verify(args.verify)
    print(json.dumps({"ledger": args.verify, "integridade": "ok" if ok else "quebrada", "issues": issues}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
