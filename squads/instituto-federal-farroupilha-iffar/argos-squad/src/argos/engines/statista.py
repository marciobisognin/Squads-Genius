from __future__ import annotations
from collections import Counter
from argos.contracts import ClassificacaoPublicacao, PublicacaoNormalizada

def agregar(publicacoes: list[PublicacaoNormalizada], classificacoes: list[ClassificacaoPublicacao]) -> dict:
    by_id = {p.id_canonico: p for p in publicacoes}
    relevantes = [by_id[c.id_canonico] for c in classificacoes if c.id_canonico in by_id]
    return {
        "total_corpus": len(publicacoes),
        "total_relevantes": len(relevantes),
        "por_fonte": dict(Counter(p.fonte for p in relevantes)),
        "por_orgao": dict(Counter(p.orgao or "não informado" for p in relevantes)),
        "por_tipo_ato": dict(Counter(p.tipo_ato or "não informado" for p in relevantes)),
        "por_categoria": dict(Counter(c.categoria for c in classificacoes)),
    }
