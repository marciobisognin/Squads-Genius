"""Ranker determinístico — Fase 2 do Gateway.

Scoring sem LLM, baseado em similaridade léxica de palavras-chave.
Combinação: overlap com agentes (peso 2.0) + overlap com squad (peso 1.0).
"""

import re
from typing import Any


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


def _tokenize(text: str) -> list[str]:
    """Tokeniza texto em palavras significativas."""
    text = (text or "").lower()
    text = re.sub(r"[^0-9a-zà-ÿ\s\-]", " ", text)
    tokens = re.split(r"[\s\-]+", text)
    out: list[str] = []
    for tok in tokens:
        tok = tok.strip()
        if len(tok) >= 3 and tok not in STOPWORDS:
            out.append(tok)
    return out


def rank_squads(query: str, index_data: dict[str, Any], top_n: int = 5) -> list[dict[str, Any]]:
    """Rankeia squads por relevância à query.

    Args:
        query: Descrição da tarefa ou termo de busca
        index_data: Índice JSON (resultado de create_index)
        top_n: Quantos resultados retornar

    Returns:
        Lista de dicts com score, squad, path, matched_keywords, evidence
    """
    query_tokens = set(_tokenize(query))
    if not query_tokens:
        return []

    results: list[dict[str, Any]] = []

    squads = index_data.get("squads", [])
    for squad in squads:
        squad_keywords = set(squad.get("keywords", []))

        # Agentes como sub-pontuação
        agents = squad.get("agents", [])
        for agent in agents:
            agent_id = agent.get("id", "")
            agent_role = agent.get("role", "")
            agent_tokens = set(_tokenize(f"{agent_id} {agent_role}"))

            # Scoring: agente (peso 2.0) + squad (peso 1.0)
            direct_match = query_tokens & agent_tokens
            context_match = (query_tokens & squad_keywords) - direct_match

            base_score = 2.0 * len(direct_match) + 1.0 * len(context_match)

            if base_score > 0:
                matched = sorted(direct_match | context_match)
                evidence = f"Match: {', '.join(matched[:3])}"

                results.append({
                    "score": round(base_score, 2),
                    "squad": squad.get("name", ""),
                    "display_name": squad.get("display_name", ""),
                    "path": squad.get("path", ""),
                    "domain": squad.get("domain", ""),
                    "agent": agent_id if agent_id else None,
                    "agent_role": agent_role,
                    "matched_keywords": matched,
                    "evidence": evidence,
                })

        # Se squad sem agentes, ainda contribui
        if not agents:
            squad_match = query_tokens & squad_keywords
            if squad_match:
                matched = sorted(squad_match)
                evidence = f"Palavras-chave do squad: {', '.join(matched[:3])}"

                results.append({
                    "score": round(1.0 * len(squad_match), 2),
                    "squad": squad.get("name", ""),
                    "display_name": squad.get("display_name", ""),
                    "path": squad.get("path", ""),
                    "domain": squad.get("domain", ""),
                    "agent": None,
                    "agent_role": "",
                    "matched_keywords": matched,
                    "evidence": evidence,
                })

    # Ordena por score desc, depois por squad name
    results.sort(key=lambda x: (-x["score"], x["squad"]))

    # Remove duplicatas (mesmo squad com score diferente — mantém o melhor)
    seen_squads: dict[str, dict[str, Any]] = {}
    for r in results:
        sq_key = r["squad"]
        if sq_key not in seen_squads or r["score"] > seen_squads[sq_key]["score"]:
            seen_squads[sq_key] = r

    final = sorted(seen_squads.values(), key=lambda x: -x["score"])

    return final[:top_n]
