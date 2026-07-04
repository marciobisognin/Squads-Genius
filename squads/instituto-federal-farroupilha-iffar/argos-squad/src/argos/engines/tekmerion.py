from __future__ import annotations
import httpx
from argos.contracts import ClassificacaoPublicacao, PublicacaoNormalizada

def excerto_literal(pub: PublicacaoNormalizada, excerto: str) -> bool:
    return bool(excerto) and excerto in pub.texto

def url_verificavel(url: str, timeout: float = 8.0) -> bool:
    try:
        r = httpx.head(url, follow_redirects=True, timeout=timeout)
        if r.status_code < 400:
            return True
        r = httpx.get(url, follow_redirects=True, timeout=timeout)
        return r.status_code < 400
    except Exception:
        return False

def auditar(publicacoes: dict[str, PublicacaoNormalizada], classificacoes: list[ClassificacaoPublicacao], verificar_urls: bool = False) -> tuple[bool, dict[str, str]]:
    motivos = {}
    for cls in classificacoes:
        pub = publicacoes.get(cls.id_canonico)
        if not pub:
            motivos[cls.id_canonico] = "publicação ausente do corpus fixado"
        elif not excerto_literal(pub, cls.excerto_evidencia):
            motivos[cls.id_canonico] = "excerto_evidencia não existe literalmente no texto-fonte"
        elif verificar_urls and not url_verificavel(str(pub.url_original)):
            motivos[cls.id_canonico] = "url_original não respondeu no gate TEKMÉRION"
    return not motivos, motivos
