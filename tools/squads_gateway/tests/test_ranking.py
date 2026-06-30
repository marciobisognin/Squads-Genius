"""Testes de ranking e roteamento — Fase 2 do Gateway."""

from tools.squads_gateway.ranker import rank_squads, _tokenize


def test_tokenize():
    """Testa tokenização de query."""
    query = "Preciso criar conteúdo para Instagram"
    tokens = _tokenize(query)

    assert "conteudo" in tokens or "criar" in tokens
    assert len(tokens) > 0


def test_rank_squads_simple():
    """Testa roteamento com índice simples."""
    index = {
        "squads": [
            {
                "name": "content-squad",
                "display_name": "Content Squad",
                "path": "squads/content-squad",
                "domain": "conteudo",
                "keywords": ["conteudo", "criacao", "producao", "artigos", "blog"],
                "agents": [
                    {
                        "id": "content-creator",
                        "role": "Especialista em criação de conteúdo",
                        "file": "agents/content-creator.md",
                    }
                ],
            },
            {
                "name": "code-squad",
                "display_name": "Code Squad",
                "path": "squads/code-squad",
                "domain": "desenvolvimento",
                "keywords": ["codigo", "python", "javascript", "desenvolvimento"],
                "agents": [
                    {
                        "id": "dev-lead",
                        "role": "Desenvolvedor sênior",
                        "file": "agents/dev-lead.md",
                    }
                ],
            },
        ]
    }

    # Query sobre conteúdo
    results = rank_squads("Preciso criar conteúdo para instagram", index, top_n=3)

    assert len(results) > 0
    # Content squad deve estar no topo
    assert results[0]["squad"] == "content-squad"
    assert results[0]["score"] > results[-1]["score"]


def test_rank_squads_no_agents():
    """Testa roteamento com squad sem agentes específicos."""
    index = {
        "squads": [
            {
                "name": "tools-squad",
                "display_name": "Tools Squad",
                "path": "squads/tools-squad",
                "domain": "ferramentas",
                "keywords": ["automacao", "integracao", "api", "webhooks"],
                "agents": [],
            }
        ]
    }

    results = rank_squads("Preciso automatizar workflows", index, top_n=5)

    assert len(results) > 0
    assert results[0]["squad"] == "tools-squad"


def test_rank_squads_empty_query():
    """Testa roteamento com query vazia."""
    index = {"squads": []}

    results = rank_squads("", index, top_n=5)

    assert results == []


def test_rank_squads_no_matches():
    """Testa roteamento com query que não bate em nada."""
    index = {
        "squads": [
            {
                "name": "content-squad",
                "path": "squads/content-squad",
                "domain": "conteudo",
                "keywords": ["conteudo", "blog"],
                "agents": [
                    {
                        "id": "writer",
                        "role": "Redator",
                        "file": "agents/writer.md",
                    }
                ],
            }
        ]
    }

    # Query com palavras genéricas (stopwords)
    results = rank_squads("o a e de para", index, top_n=5)

    assert results == []


def test_rank_squads_deduplication():
    """Testa deduplicação de squads (mantém score mais alto)."""
    index = {
        "squads": [
            {
                "name": "multi-agent-squad",
                "path": "squads/multi",
                "domain": "teste",
                "keywords": ["conteudo", "desenvolvimento"],
                "agents": [
                    {
                        "id": "agent-1",
                        "role": "Especialista em conteúdo",
                        "file": "agents/a1.md",
                    },
                    {
                        "id": "agent-2",
                        "role": "Desenvolvedor",
                        "file": "agents/a2.md",
                    },
                ],
            }
        ]
    }

    results = rank_squads("conteudo desenvolvimento", index, top_n=5)

    # Deve ter apenas 1 entrada (squad), com score agregado
    assert len(results) == 1
    assert results[0]["squad"] == "multi-agent-squad"


if __name__ == "__main__":
    test_tokenize()
    test_rank_squads_simple()
    test_rank_squads_no_agents()
    test_rank_squads_empty_query()
    test_rank_squads_no_matches()
    test_rank_squads_deduplication()
    print("✅ Todos os testes de ranking passaram!")
