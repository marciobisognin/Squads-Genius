from __future__ import annotations
from argos.contracts import PerfilInteresse, PublicacaoNormalizada

def _haystack(pub: PublicacaoNormalizada) -> str:
    return "\n".join(str(x or "") for x in [pub.orgao, pub.tipo_ato, pub.identifica, pub.ementa, pub.texto]).lower()

def filtrar_publicacoes(perfil: PerfilInteresse, publicacoes: list[PublicacaoNormalizada]) -> list[PublicacaoNormalizada]:
    termos = [t.lower() for t in perfil.termos]
    ignorados = [t.lower() for t in perfil.termos_ignorados]
    orgaos = [o.lower() for o in perfil.orgaos]
    tipos = [t.lower() for t in perfil.tipos_ato]
    secoes = [s.upper() for s in perfil.secoes]
    out = []
    for pub in publicacoes:
        hay = _haystack(pub)
        if secoes and (pub.secao or "").upper() not in secoes:
            continue
        if tipos and not any(t in (pub.tipo_ato or "").lower() for t in tipos):
            continue
        if orgaos and not any(o in hay for o in orgaos):
            continue
        if not any(t in hay for t in termos):
            continue
        if any(t in hay for t in ignorados):
            continue
        out.append(pub)
    return out

def score_lexical(perfil: PerfilInteresse, pub: PublicacaoNormalizada) -> int:
    hay = _haystack(pub)
    hits = sum(1 for t in perfil.termos if t.lower() in hay)
    org_hit = 1 if any(o.lower() in hay for o in perfil.orgaos) else 0
    tipo_hit = 1 if any(t.lower() in (pub.tipo_ato or "").lower() for t in perfil.tipos_ato) else 0
    return min(100, 35 + hits * 20 + org_hit * 15 + tipo_hit * 10)
