from __future__ import annotations
from datetime import date
import hashlib, httpx
from argos.contracts import EdicaoRef, PublicacaoNormalizada, StatusFonte
from argos.ophthalmoi.base import RateLimiter, assert_egress_allowed

class QueridoDiarioAdapter:
    codigo = "QD"
    dominios_permitidos = ["api.queridodiario.ok.org.br"]
    rate_limit_rpm = 30
    def __init__(self, municipio_ibge: str | None = None, timeout: float = 15.0):
        self.municipio_ibge = municipio_ibge
        self.timeout = timeout
        self.rate = RateLimiter(self.rate_limit_rpm)
    @property
    def codigo_fonte(self) -> str:
        return f"QD-{self.municipio_ibge}" if self.municipio_ibge else "QD"
    def healthcheck(self) -> StatusFonte:
        return StatusFonte(codigo=self.codigo_fonte, estado="ok", mensagem="adapter pronto; coleta online sob demanda com rate limit conservador")
    def listar_edicoes(self, inicio: date, fim: date) -> list[EdicaoRef]:
        return [EdicaoRef(fonte=self.codigo_fonte, data=inicio, edicao=f"{inicio.isoformat()}..{fim.isoformat()}", url="https://api.queridodiario.ok.org.br/")]
    def obter_publicacoes(self, ref: EdicaoRef) -> list[PublicacaoNormalizada]:
        if not self.municipio_ibge:
            return []
        base = "https://api.queridodiario.ok.org.br/api/gazettes"
        assert_egress_allowed(base, self.dominios_permitidos)
        self.rate.wait()
        try:
            r = httpx.get(base, params={"territory_ids": self.municipio_ibge, "published_since": ref.data.isoformat(), "published_until": ref.data.isoformat(), "size": 100}, timeout=self.timeout, headers={"User-Agent": "ARGOS/0.1 contato: Marcio Bisognin"})
            r.raise_for_status()
            rows = r.json().get("gazettes", [])
        except Exception:
            return []
        pubs = []
        for i, item in enumerate(rows):
            content = item.get("excerpt") or item.get("territory_name") or "Diário municipal coletado pelo Querido Diário."
            url = item.get("url") or item.get("txt_url") or "https://api.queridodiario.ok.org.br/"
            canon = hashlib.sha256(f"QD|{self.municipio_ibge}|{item.get('date')}|{i}|{url}".encode()).hexdigest()
            pubs.append(PublicacaoNormalizada(id_canonico=canon, fonte=self.codigo_fonte, esfera="municipal", uf=None, data_publicacao=ref.data, edicao=str(item.get("edition") or ref.edicao), secao=None, orgao=item.get("territory_name"), tipo_ato=None, identifica=item.get("scraped_at"), ementa=None, texto=content, url_original=url, pagina=None, hash_conteudo=hashlib.sha256(content.encode()).hexdigest()))
        return pubs
