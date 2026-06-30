"""Indexador determinístico de squads — Fase 1 do Gateway.

Varre squads/ e IFFar-Squads/, extrai metadados, valida estrutura,
gera índice JSON canônico sem dependências externas (fallback para JSON puro).
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from .schemas import IndexEntry, AgentEntry, TaskEntry, WorkflowEntry, Index

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


STOPWORDS = {
    "a", "o", "e", "de", "do", "da", "das", "dos", "em", "no", "na", "nos", "nas",
    "para", "por", "com", "sem", "que", "um", "uma", "uns", "umas", "ao", "aos",
    "se", "ou", "os", "as", "the", "and", "of", "to", "in", "for", "with", "on",
    "como", "sua", "seu", "suas", "seus", "ele", "ela", "este", "esta", "esse",
    "essa", "isso", "etc", "sobre", "entre", "cada", "quando", "qual", "quais",
    "pelo", "pela", "mais", "menos", "muito", "ja", "já", "ser", "sao", "são",
    "tem", "ter", "fazer", "feito", "via", "partir", "todo", "toda", "todos",
    "todas", "squad", "agente", "agentes", "from", "this", "that", "are", "is",
}


def _slug_tokens(text: str) -> list[str]:
    """Extrai tokens significativos para indexação."""
    text = (text or "").lower()
    text = re.sub(r"[^0-9a-zà-ÿ\s\-]", " ", text)
    tokens = re.split(r"[\s\-]+", text)
    out: list[str] = []
    for tok in tokens:
        tok = tok.strip()
        if len(tok) < 3 or tok in STOPWORDS:
            continue
        out.append(tok)
    return out


def load_manifest(path: Path) -> Optional[dict[str, Any]]:
    """Carrega squad.yaml ou JSON, com fallback para puro JSON."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None

    data: Any = None

    # Tenta YAML primeiro se disponível
    if YAML_AVAILABLE:
        try:
            data = yaml.safe_load(text)
        except Exception:
            data = None

    # Fallback para JSON
    if data is None:
        try:
            data = json.loads(text)
        except Exception:
            return None

    return data if isinstance(data, dict) else None


def extract_agents(manifest: dict[str, Any]) -> list[AgentEntry]:
    """Extrai agentes do squad.yaml."""
    entries: list[AgentEntry] = []
    agents = manifest.get("agents") or []

    if isinstance(agents, list):
        for a in agents:
            if isinstance(a, dict):
                entries.append(AgentEntry(
                    id=str(a.get("id") or a.get("name") or "unknown"),
                    role=str(a.get("role") or a.get("description") or ""),
                    file=a.get("file") or None,
                ))
            elif isinstance(a, str):
                entries.append(AgentEntry(id=a))

    return entries


def extract_tasks(manifest: dict[str, Any]) -> list[TaskEntry]:
    """Extrai tarefas do squad.yaml."""
    entries: list[TaskEntry] = []
    tasks = manifest.get("tasks") or []

    if isinstance(tasks, list):
        for t in tasks:
            if isinstance(t, dict):
                entries.append(TaskEntry(
                    id=str(t.get("id") or t.get("name") or "unknown"),
                    file=t.get("file") or None,
                ))
            elif isinstance(t, str):
                entries.append(TaskEntry(id=t))

    return entries


def extract_workflows(manifest: dict[str, Any]) -> list[WorkflowEntry]:
    """Extrai workflows do squad.yaml."""
    entries: list[WorkflowEntry] = []
    workflows = manifest.get("workflows") or []

    if isinstance(workflows, list):
        for w in workflows:
            if isinstance(w, dict):
                entries.append(WorkflowEntry(
                    id=str(w.get("id") or w.get("name") or "unknown"),
                    file=w.get("file") or None,
                ))
            elif isinstance(w, str):
                entries.append(WorkflowEntry(id=w))

    return entries


def index_squad(manifest_path: Path, repo_root: Path) -> Optional[IndexEntry]:
    """Indexa um único squad.yaml."""
    squad_dir = manifest_path.parent
    manifest = load_manifest(manifest_path)

    if not manifest:
        return None

    name = str(manifest.get("name") or squad_dir.name)

    try:
        # Caminho relativo da raiz do repo
        rel_path = squad_dir.relative_to(repo_root).as_posix()

        # Extrai estrutura
        agents = extract_agents(manifest)
        tasks = extract_tasks(manifest)
        workflows = extract_workflows(manifest)

        # Extrai palavras-chave
        text_to_index = " ".join([
            manifest.get("name", ""),
            manifest.get("display_name", ""),
            manifest.get("purpose", ""),
            manifest.get("domain", ""),
            " ".join(manifest.get("tags", [])),
        ])
        keywords = _slug_tokens(text_to_index)

        entry = IndexEntry(
            name=name,
            path=rel_path,
            display_name=str(manifest.get("display_name") or name),
            version=str(manifest.get("version") or "1.0.0"),
            status=str(manifest.get("status") or "operational-prototype"),
            purpose=str(manifest.get("purpose") or ""),
            domain=str(manifest.get("domain") or ""),
            language=str(manifest.get("language") or "pt-BR"),
            creator=str(manifest.get("creator") or ""),
            license=str(manifest.get("license") or "MIT"),
            agents=agents,
            tasks=tasks,
            workflows=workflows,
            keywords=keywords,
            tags=manifest.get("tags") or [],
        )
        return entry
    except Exception as e:
        print(f"⚠️  Erro ao indexar {manifest_path}: {e}", flush=True)
        return None


def scan_directory(repo_root: Path, exclude_patterns: Optional[list[str]] = None) -> list[Path]:
    """Encontra todos os squad.yaml, evitando padrões."""
    exclude_patterns = exclude_patterns or [".backup", "media", "docs"]
    manifests: list[Path] = []

    for manifest_path in sorted(repo_root.rglob("squad.yaml")):
        # Verifica se está em pasta excluída
        if any(exc in manifest_path.parts for exc in exclude_patterns):
            continue
        manifests.append(manifest_path)

    return manifests


def create_index(repo_root: Path) -> Index:
    """Cria índice completo varrendo repo_root."""
    manifests = scan_directory(repo_root)
    entries: list[IndexEntry] = []

    for manifest_path in manifests:
        entry = index_squad(manifest_path, repo_root)
        if entry:
            entries.append(entry)

    # Ordena por nome
    entries.sort(key=lambda e: e.name)

    index = Index(
        squads=entries,
        total_count=len(entries),
        metadata={
            "repo_root": str(repo_root),
            "manifest_count": len(manifests),
            "indexed_squads": len(entries),
        }
    )

    return index


def save_index(index: Index, output_path: Path) -> None:
    """Salva índice em JSON estruturado."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    json_data = index.to_dict()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)


def generate_audit_report(index: Index, output_path: Path) -> None:
    """Gera relatório de auditoria com cobertura e gaps."""
    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "total_squads_indexed": index.total_count,
        "coverage": {
            "squads_with_agents": sum(1 for s in index.squads if s.agents),
            "squads_with_tasks": sum(1 for s in index.squads if s.tasks),
            "squads_with_workflows": sum(1 for s in index.squads if s.workflows),
        },
        "by_domain": {},
        "by_status": {},
        "broken_links": [],
    }

    # Agrupa por domínio e status
    for squad in index.squads:
        domain = squad.domain or "undefined"
        status = squad.status or "unknown"

        if domain not in report["by_domain"]:
            report["by_domain"][domain] = 0
        report["by_domain"][domain] += 1

        if status not in report["by_status"]:
            report["by_status"][status] = 0
        report["by_status"][status] += 1

        # Verifica links quebrados
        for agent in squad.agents:
            if agent.file:
                agent_path = Path(squad.path) / agent.file
                if not agent_path.exists():
                    report["broken_links"].append({
                        "type": "agent",
                        "squad": squad.name,
                        "expected_path": str(agent_path),
                    })

        for task in squad.tasks:
            if task.file:
                task_path = Path(squad.path) / task.file
                if not task_path.exists():
                    report["broken_links"].append({
                        "type": "task",
                        "squad": squad.name,
                        "expected_path": str(task_path),
                    })

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
