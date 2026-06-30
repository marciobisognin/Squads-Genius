"""Testes de indexação — Fase 1 do Gateway."""

import json
import tempfile
from pathlib import Path
from datetime import datetime

from tools.squads_gateway.indexer import (
    create_index,
    load_manifest,
    index_squad,
    _slug_tokens,
)
from tools.squads_gateway.schemas import Index, IndexEntry


def test_slug_tokens():
    """Testa tokenização de texto."""
    text = "Tesouraria Pública & Conformidade 2024"
    tokens = _slug_tokens(text)

    assert len(tokens) > 0
    assert "tesouraria" in tokens
    assert "publica" in tokens
    assert "conformidade" in tokens
    # Deve filtrar stopwords e caracteres especiais
    assert "&" not in " ".join(tokens)


def test_load_manifest():
    """Testa carregamento de squad.yaml."""
    with tempfile.TemporaryDirectory() as tmpdir:
        squad_dir = Path(tmpdir) / "test-squad"
        squad_dir.mkdir()

        # Cria squad.yaml simples
        manifest_path = squad_dir / "squad.yaml"
        manifest_content = """
name: test-squad
display_name: Test Squad
version: 1.0.0
status: operational-prototype
purpose: A test squad
domain: test-domain
language: pt-BR
creator: Test Creator
agents: []
tasks: []
workflows: []
"""
        manifest_path.write_text(manifest_content, encoding="utf-8")

        # Carrega
        data = load_manifest(manifest_path)

        assert data is not None
        assert data["name"] == "test-squad"
        assert data["display_name"] == "Test Squad"


def test_index_squad():
    """Testa indexação de um único squad."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)
        squad_dir = repo_root / "squads" / "test-squad"
        squad_dir.mkdir(parents=True)

        # Cria squad.yaml com agentes e tarefas
        manifest_path = squad_dir / "squad.yaml"
        manifest_content = """
name: squ-test-squad
display_name: Test Squad
version: 1.0.0
status: operational
purpose: Processamento de conteúdo
domain: conteudo
language: pt-BR
creator: Test
agents:
  - id: agent-1
    role: Processador de conteúdo
    file: agents/agent-1.md
tasks:
  - id: task-1
    file: tasks/task-1.yaml
workflows: []
tags:
  - conteudo
  - processamento
"""
        manifest_path.write_text(manifest_content, encoding="utf-8")

        # Indexa
        entry = index_squad(manifest_path, repo_root)

        assert entry is not None
        assert entry.name == "squ-test-squad"
        assert entry.display_name == "Test Squad"
        assert entry.path == "squads/test-squad"
        assert len(entry.agents) == 1
        assert entry.agents[0].id == "agent-1"
        assert len(entry.tasks) == 1
        assert "conteudo" in entry.keywords


def test_create_index():
    """Testa criação de índice completo."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)

        # Cria 2 squads de teste
        for i in range(2):
            squad_dir = repo_root / "squads" / f"test-squad-{i}"
            squad_dir.mkdir(parents=True)

            manifest_path = squad_dir / "squad.yaml"
            manifest_content = f"""
name: test-squad-{i}
display_name: Test Squad {i}
version: 1.0.0
agents: []
tasks: []
workflows: []
"""
            manifest_path.write_text(manifest_content, encoding="utf-8")

        # Cria índice
        index = create_index(repo_root)

        assert isinstance(index, Index)
        assert index.total_count == 2
        assert len(index.squads) == 2
        assert all(isinstance(s, IndexEntry) for s in index.squads)
        assert index.squads[0].name == "test-squad-0"
        assert index.squads[1].name == "test-squad-1"


def test_index_excludes_patterns():
    """Testa exclusão de padrões (backup, media, etc)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)

        # Squad legítimo
        squad_dir = repo_root / "squads" / "real-squad"
        squad_dir.mkdir(parents=True)
        (squad_dir / "squad.yaml").write_text("name: real-squad\n", encoding="utf-8")

        # Squad em pasta excluída
        backup_squad = repo_root / "backup" / "old-squad"
        backup_squad.mkdir(parents=True)
        (backup_squad / "squad.yaml").write_text("name: old-squad\n", encoding="utf-8")

        # Cria índice
        index = create_index(repo_root)

        assert index.total_count == 1
        assert index.squads[0].name == "real-squad"


if __name__ == "__main__":
    test_slug_tokens()
    test_load_manifest()
    test_index_squad()
    test_create_index()
    test_index_excludes_patterns()
    print("✅ Todos os testes de indexação passaram!")
