#!/usr/bin/env python3
"""Núcleo determinístico do Universal Obsidian Knowledge Squad.

Funções compartilhadas: carregamento de config, resolução do vault,
parsing de Markdown (frontmatter, tags, headings, wikilinks), chunking,
IDs estáveis e armazenamento do índice (SQLite FTS5 + JSON).

Sem dependências externas obrigatórias. PyYAML é usado quando disponível;
caso contrário, config e frontmatter podem ser fornecidos em JSON.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import sqlite3
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

try:  # PyYAML é opcional
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

INDEX_DIRNAME = ".obsidian_knowledge_index"
SECRET_PATTERNS = [
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"gho_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"BEGIN (?:RSA |EC )?PRIVATE[ ]KEY"),
    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*\S+"),
]
WIKILINK_RE = re.compile(r"\[\[([^\]\|]+)(?:\|[^\]]+)?\]\]")
TAG_RE = re.compile(r"(?:^|\s)#([A-Za-z0-9_\-/]+)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


# --------------------------------------------------------------------------- #
# Config e resolução do vault
# --------------------------------------------------------------------------- #
def load_config(path: Optional[str]) -> Dict[str, Any]:
    """Carrega config YAML ou JSON. Retorna {} se não houver arquivo."""
    if not path:
        return {}
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Config não encontrada: {path}")
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() == ".json":
        return json.loads(text)
    if yaml is not None:
        return yaml.safe_load(text) or {}
    raise RuntimeError(
        "PyYAML não instalado e config não é JSON. "
        "Instale pyyaml ou forneça config .json."
    )


def resolve_vault_path(config: Dict[str, Any], cli_vault: Optional[str]) -> Path:
    """Ordem de resolução (PRD §4): CLI > config > env > erro pedindo caminho."""
    candidate = (
        cli_vault
        or (config.get("vault") or {}).get("path")
        or os.environ.get("OBSIDIAN_VAULT_PATH")
    )
    if not candidate:
        raise ValueError(
            "Caminho do vault não definido. Use --vault, config.vault.path "
            "ou a variável de ambiente OBSIDIAN_VAULT_PATH."
        )
    p = Path(os.path.expanduser(str(candidate)))
    if not p.is_dir():
        raise NotADirectoryError(f"Vault não é um diretório válido: {p}")
    return p


def index_dir_for(vault: Path, config: Dict[str, Any]) -> Path:
    runtime = config.get("runtime") or {}
    custom = runtime.get("index_dir")
    if custom:
        return Path(os.path.expanduser(str(custom)))
    return vault / INDEX_DIRNAME


# --------------------------------------------------------------------------- #
# Modelo de dados
# --------------------------------------------------------------------------- #
@dataclass
class Chunk:
    chunk_id: str
    note_id: str
    path: str
    heading: str
    text: str
    anchor_quote: str
    start_line: int
    end_line: int
    tags: List[str] = field(default_factory=list)


@dataclass
class Note:
    note_id: str
    current_path: str
    previous_paths: List[str]
    title: str
    frontmatter: Dict[str, Any]
    tags: List[str]
    headings: List[str]
    links_out: List[str]
    links_in: List[str]
    modified_at: str
    content_sha256: str
    word_count: int
    language: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# --------------------------------------------------------------------------- #
# Parsing de Markdown
# --------------------------------------------------------------------------- #
def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_frontmatter(text: str) -> Dict[str, Any]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    if yaml is not None:
        try:
            data = yaml.safe_load(block)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    # Fallback mínimo: pares chave: valor de primeiro nível.
    out: Dict[str, Any] = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text, count=1)


def extract_tags(text: str, frontmatter: Dict[str, Any]) -> List[str]:
    tags = set()
    fm_tags = frontmatter.get("tags")
    if isinstance(fm_tags, str):
        tags.update(t.strip() for t in fm_tags.split(",") if t.strip())
    elif isinstance(fm_tags, list):
        tags.update(str(t).strip() for t in fm_tags if str(t).strip())
    for m in TAG_RE.finditer(text):
        tags.add(m.group(1))
    return sorted(tags)


def extract_headings(body: str) -> List[str]:
    return [m.group(2).strip() for line in body.splitlines()
            for m in [HEADING_RE.match(line)] if m]


def extract_wikilinks(body: str) -> List[str]:
    seen: List[str] = []
    for m in WIKILINK_RE.finditer(body):
        target = m.group(1).strip()
        if target and target not in seen:
            seen.append(target)
    return seen


def detect_language(frontmatter: Dict[str, Any], default: str) -> str:
    lang = frontmatter.get("language") or frontmatter.get("lang")
    return str(lang) if lang else default


def chunk_by_headings(note_id: str, path: str, body: str,
                      tags: List[str]) -> List[Chunk]:
    """Divide o corpo em chunks delimitados por headings Markdown."""
    lines = body.splitlines()
    chunks: List[Chunk] = []
    current_heading = "(início)"
    buf: List[str] = []
    start = 1

    def flush(end_line: int) -> None:
        text = "\n".join(buf).strip()
        if text:
            anchor = " ".join(text.split())[:120]
            cid = _sha256(f"{path}|{current_heading}|{start}|{text[:64]}")[:24]
            chunks.append(Chunk(
                chunk_id=f"sha256:{cid}", note_id=note_id, path=path,
                heading=current_heading, text=text, anchor_quote=anchor,
                start_line=start, end_line=end_line, tags=list(tags),
            ))

    for i, line in enumerate(lines, start=1):
        m = HEADING_RE.match(line)
        if m:
            flush(i - 1)
            current_heading = m.group(2).strip()
            buf = []
            start = i + 1
        else:
            buf.append(line)
    flush(len(lines))
    return chunks


def title_from(path: Path, frontmatter: Dict[str, Any], body: str) -> str:
    if frontmatter.get("title"):
        return str(frontmatter["title"])
    for line in body.splitlines():
        m = HEADING_RE.match(line)
        if m:
            return m.group(2).strip()
    return path.stem


# --------------------------------------------------------------------------- #
# Varredura do vault
# --------------------------------------------------------------------------- #
def iter_markdown_files(vault: Path, include: List[str],
                        exclude: List[str]) -> Iterable[Path]:
    include = include or ["**/*.md"]
    matched: List[Path] = []
    for pattern in include:
        matched.extend(vault.glob(pattern))
    seen = set()
    for path in sorted(matched):
        if not path.is_file():
            continue
        rel = path.relative_to(vault).as_posix()
        if any(fnmatch.fnmatch(rel, ex) or rel.startswith(ex.rstrip("*/"))
               for ex in (exclude or [])):
            continue
        if path in seen:
            continue
        seen.add(path)
        yield path


# --------------------------------------------------------------------------- #
# Índice (SQLite FTS5 + JSON)
# --------------------------------------------------------------------------- #
SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    note_id TEXT PRIMARY KEY,
    current_path TEXT,
    previous_paths TEXT,
    title TEXT,
    frontmatter TEXT,
    tags TEXT,
    headings TEXT,
    links_out TEXT,
    links_in TEXT,
    modified_at TEXT,
    content_sha256 TEXT,
    word_count INTEGER,
    language TEXT
);
CREATE TABLE IF NOT EXISTS registry (
    content_sha256 TEXT PRIMARY KEY,
    note_id TEXT
);
CREATE TABLE IF NOT EXISTS path_registry (
    path TEXT PRIMARY KEY,
    note_id TEXT
);
CREATE VIRTUAL TABLE IF NOT EXISTS chunks USING fts5(
    chunk_id UNINDEXED, note_id UNINDEXED, path UNINDEXED,
    heading, text, anchor_quote UNINDEXED,
    start_line UNINDEXED, end_line UNINDEXED, tags,
    tokenize = "unicode61 remove_diacritics 2"
);
"""


def open_index(index_dir: Path) -> sqlite3.Connection:
    index_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(index_dir / "vault.sqlite"))
    conn.executescript(SCHEMA)
    return conn


def stable_note_id(conn: sqlite3.Connection, frontmatter: Dict[str, Any],
                   path: str, content_sha: str) -> tuple[str, List[str]]:
    """ID estável + previous_paths (PRD §14).

    Prioridade: id do frontmatter > id já associado ao path >
    id já associado ao conteúdo (rename) > novo id determinístico.
    """
    if frontmatter.get("id"):
        return str(frontmatter["id"]), []
    row = conn.execute(
        "SELECT note_id FROM path_registry WHERE path=?", (path,)).fetchone()
    if row:
        return row[0], []
    row = conn.execute(
        "SELECT note_id FROM registry WHERE content_sha256=?",
        (content_sha,)).fetchone()
    if row:
        old = conn.execute(
            "SELECT current_path, previous_paths FROM notes WHERE note_id=?",
            (row[0],)).fetchone()
        prev = []
        if old:
            prev = json.loads(old[1] or "[]")
            if old[0] and old[0] != path and old[0] not in prev:
                prev.append(old[0])
        return row[0], prev
    return f"uoks:{_sha256(path)[:24]}", []


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def dump_json_indexes(index_dir: Path, notes: List[Note],
                      chunks: List[Chunk]) -> None:
    """Espelha o índice em JSON para inspeção/portabilidade (PRD §14)."""
    def w(name: str, data: Any) -> None:
        (index_dir / name).write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    w("notes_index.json", [n.to_dict() for n in notes])
    w("chunks_index.json", [asdict(c) for c in chunks])
    tags: Dict[str, List[str]] = {}
    for n in notes:
        for t in n.tags:
            tags.setdefault(t, []).append(n.current_path)
    w("tags_index.json", tags)
    backlinks = {n.current_path: n.links_in for n in notes}
    w("backlinks_index.json", backlinks)
    headings = {n.current_path: n.headings for n in notes}
    w("headings_index.json", headings)
    w("last_scan.json", {
        "scanned_at": now_iso(),
        "note_count": len(notes),
        "chunk_count": len(chunks),
    })


def scan_secrets(text: str) -> List[str]:
    return [p.pattern for p in SECRET_PATTERNS if p.search(text)]
