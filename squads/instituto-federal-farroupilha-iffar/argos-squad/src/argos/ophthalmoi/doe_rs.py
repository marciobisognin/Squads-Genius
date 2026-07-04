from __future__ import annotations
from datetime import date
from argos.contracts import EdicaoRef, PublicacaoNormalizada, StatusFonte

class DOERSAdapter:
    codigo = "DOE-RS"
    dominios_permitidos = ["diariooficial.rs.gov.br"]
    rate_limit_rpm = 20
    def healthcheck(self) -> StatusFonte:
        return StatusFonte(codigo=self.codigo, estado="backlog", mensagem="adapter estadual requer descoberta legítima, fixtures reais e homologação HITL antes de produção")
    def listar_edicoes(self, inicio: date, fim: date) -> list[EdicaoRef]:
        return []
    def obter_publicacoes(self, ref: EdicaoRef) -> list[PublicacaoNormalizada]:
        return []
