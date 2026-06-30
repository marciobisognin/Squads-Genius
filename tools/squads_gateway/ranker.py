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
        if len(tok) >= 2 and tok not in STOPWORDS:  # Reduzido de 3 para 2 chars
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
        # Combina todos os campos de busca do squad (em ordem de relevância)
        squad_name_tokens = set(_tokenize(squad.get("name", "")))
        squad_display_tokens = set(_tokenize(squad.get("display_name", "")))
        squad_keywords = set(squad.get("keywords", []))
        squad_purpose_tokens = set(_tokenize(squad.get("purpose", "")))
        squad_path_tokens = set(_tokenize(squad.get("path", "")))

        # Agentes como sub-pontuação
        agents = squad.get("agents", [])

        if agents:
            # Com agentes: prioriza match em agentes, depois squad
            for agent in agents:
                agent_id = agent.get("id", "")
                agent_role = agent.get("role", "")
                agent_tokens = set(_tokenize(f"{agent_id} {agent_role}"))

                # Scoring estruturado:
                direct_match = query_tokens & agent_tokens  # Match em agente
                name_match = (query_tokens & squad_name_tokens) - direct_match  # Match em nome
                display_match = (query_tokens & squad_display_tokens) - direct_match - name_match
                keyword_match = (query_tokens & squad_keywords) - direct_match - name_match - display_match
                other_match = (query_tokens & (squad_purpose_tokens | squad_path_tokens)) - direct_match - name_match - display_match - keyword_match

                # Pesos: agent (4.0) > nome (3.5) > display (3.0) > keywords (1.5) > outros (0.5)
                base_score = (
                    4.0 * len(direct_match) +
                    3.5 * len(name_match) +
                    3.0 * len(display_match) +
                    1.5 * len(keyword_match) +
                    0.5 * len(other_match)
                )

                if base_score > 0:
                    matched = sorted(direct_match | name_match | display_match | keyword_match | other_match)
                    evidence = f"Agent: {agent_id} | Match: {', '.join(matched[:3])}"

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
        else:
            # Sem agentes: prioriza match em nome do squad
            name_match = query_tokens & squad_name_tokens
            display_match = (query_tokens & squad_display_tokens) - name_match
            keyword_match = (query_tokens & squad_keywords) - name_match - display_match
            other_match = (query_tokens & (squad_purpose_tokens | squad_path_tokens)) - name_match - display_match - keyword_match

            # Pesos aumentados para squads sem agentes (para balancear)
            base_score = (
                4.0 * len(name_match) +
                3.0 * len(display_match) +
                1.5 * len(keyword_match) +
                0.5 * len(other_match)
            )

            if base_score > 0:
                matched = sorted(name_match | display_match | keyword_match | other_match)
                evidence = f"Squad: {squad.get('name', '')} | Match: {', '.join(matched[:3])}"

                results.append({
                    "score": round(base_score, 2),
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
