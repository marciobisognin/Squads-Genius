from __future__ import annotations

from datetime import date

import httpx

from argos.contracts import EdicaoRef, PublicacaoNormalizada, StatusFonte
from argos.official_sources import OfficialSource, state_by_code


class EstadoCatalogAdapter:
    """Adapter estadual catalogado.

    Este adapter não inventa publicações. Enquanto a UF não tiver parser homologado,
    ele oferece healthcheck, allowlist e referência oficial para o modo Maeve assistido.
    """

    rate_limit_rpm = 12

    def __init__(self, source: OfficialSource):
        self.source = source
        self.codigo = source.codigo
        self.dominios_permitidos = list(source.dominios_permitidos)

    def healthcheck(self) -> StatusFonte:
        try:
            r = httpx.get(self.source.portal_url, timeout=12, follow_redirects=True, headers={"User-Agent": "ARGOS/0.2 contato: Marcio Bisognin"})
            estado = "observacao" if r.status_code < 500 else "degradado"
            return StatusFonte(codigo=self.codigo, estado=estado, mensagem=f"portal catalogado respondeu HTTP {r.status_code}; coleta granular exige homologação HITL")
        except Exception as exc:
            return StatusFonte(codigo=self.codigo, estado="degradado", mensagem=f"portal catalogado, mas healthcheck falhou: {type(exc).__name__}: {exc}")

    def listar_edicoes(self, inicio: date, fim: date) -> list[EdicaoRef]:
        return [EdicaoRef(fonte=self.codigo, data=inicio, edicao=f"assistido:{inicio.isoformat()}..{fim.isoformat()}", url=self.source.portal_url)]

    def obter_publicacoes(self, ref: EdicaoRef) -> list[PublicacaoNormalizada]:
        # Não há extração granular homologada por padrão; o modo assistido registra links e lacunas.
        return []


def build_estado_adapter(codigo: str) -> EstadoCatalogAdapter:
    source = state_by_code(codigo)
    if not source:
        raise KeyError(f"Fonte estadual não catalogada: {codigo}")
    return EstadoCatalogAdapter(source)
