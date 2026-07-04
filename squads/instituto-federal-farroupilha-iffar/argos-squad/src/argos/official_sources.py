from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote_plus, urlparse


@dataclass(frozen=True)
class OfficialSource:
    codigo: str
    nome: str
    esfera: str
    uf: str | None
    portal_url: str
    dominios_permitidos: tuple[str, ...]
    metodo: str
    status_operacional: str
    observacao: str = ""

    @property
    def dominio_principal(self) -> str:
        return urlparse(self.portal_url).hostname or ""

    def assistant_search_url(self, assunto: str) -> str:
        # Link auxiliar de pesquisa. Não substitui evidência oficial; serve para Maeve abrir/inspecionar.
        q = quote_plus(f"site:{self.dominio_principal} {assunto}")
        return f"https://www.google.com/search?q={q}"


FEDERAL_SOURCE = OfficialSource(
    codigo="DOU-INLABS",
    nome="Diário Oficial da União — INLABS",
    esfera="federal",
    uf=None,
    portal_url="https://inlabs.in.gov.br/",
    dominios_permitidos=("inlabs.in.gov.br", "in.gov.br", "www.in.gov.br"),
    metodo="INLABS XML autenticado",
    status_operacional="credencial_requerida",
    observacao="Produção exige INLABS_USER/INLABS_PASSWORD; não usar Selenium contra busca da Imprensa Nacional.",
)

MUNICIPAL_SOURCE = OfficialSource(
    codigo="QD",
    nome="Querido Diário — API pública municipal",
    esfera="municipal",
    uf=None,
    portal_url="https://api.queridodiario.ok.org.br/",
    dominios_permitidos=("api.queridodiario.ok.org.br", "data.queridodiario.ok.org.br"),
    metodo="API pública /api/gazettes?querystring=...",
    status_operacional="api",
    observacao="Cobertura depende dos municípios indexados pelo Querido Diário.",
)

# Catálogo nacional de portais estaduais oficiais ou páginas oficiais de publicação.
# A coleta granular por matéria só deve virar produção após homologação HITL por UF.
STATE_SOURCES: dict[str, OfficialSource] = {
    "AC": OfficialSource("DOE-AC", "Diário Oficial do Estado do Acre", "estadual", "AC", "https://www.diario.ac.gov.br/", ("diario.ac.gov.br", "www.diario.ac.gov.br"), "portal oficial", "assistido"),
    "AL": OfficialSource("DOE-AL", "Diário Oficial do Estado de Alagoas", "estadual", "AL", "https://www.imprensaoficial.al.gov.br/", ("imprensaoficial.al.gov.br", "www.imprensaoficial.al.gov.br"), "portal oficial", "assistido"),
    "AP": OfficialSource("DOE-AP", "Diário Oficial do Estado do Amapá", "estadual", "AP", "https://diofe.portal.ap.gov.br/", ("diofe.portal.ap.gov.br", "portal.ap.gov.br"), "portal oficial", "assistido"),
    "AM": OfficialSource("DOE-AM", "Diário Oficial do Estado do Amazonas", "estadual", "AM", "https://diario.imprensaoficial.am.gov.br/", ("diario.imprensaoficial.am.gov.br", "imprensaoficial.am.gov.br"), "portal oficial", "assistido"),
    "BA": OfficialSource("DOE-BA", "Diário Oficial do Estado da Bahia", "estadual", "BA", "https://dool.egba.ba.gov.br/", ("dool.egba.ba.gov.br", "egba.ba.gov.br"), "portal oficial", "assistido"),
    "CE": OfficialSource("DOE-CE", "Diário Oficial do Estado do Ceará", "estadual", "CE", "https://www.ceara.gov.br/diario-oficial/", ("ceara.gov.br", "www.ceara.gov.br"), "página oficial", "assistido"),
    "DF": OfficialSource("DODF", "Diário Oficial do Distrito Federal", "estadual", "DF", "https://www.dodf.df.gov.br/", ("dodf.df.gov.br", "www.dodf.df.gov.br"), "portal oficial", "assistido"),
    "ES": OfficialSource("DOE-ES", "Diário Oficial do Estado do Espírito Santo", "estadual", "ES", "https://dio.es.gov.br/", ("dio.es.gov.br",), "portal oficial", "assistido"),
    "GO": OfficialSource("DOE-GO", "Diário Oficial do Estado de Goiás", "estadual", "GO", "https://diariooficial.abc.go.gov.br/", ("diariooficial.abc.go.gov.br", "abc.go.gov.br"), "portal oficial", "assistido"),
    "MA": OfficialSource("DOE-MA", "Diário Oficial do Estado do Maranhão", "estadual", "MA", "https://www.diariooficial.ma.gov.br/", ("diariooficial.ma.gov.br", "www.diariooficial.ma.gov.br"), "portal oficial", "assistido"),
    "MT": OfficialSource("DOE-MT", "Diário Oficial do Estado de Mato Grosso", "estadual", "MT", "https://www.iomat.mt.gov.br/", ("iomat.mt.gov.br", "www.iomat.mt.gov.br"), "portal oficial", "assistido"),
    "MS": OfficialSource("DOE-MS", "Diário Oficial do Estado de Mato Grosso do Sul", "estadual", "MS", "https://www.spdo.ms.gov.br/diariodoe/", ("spdo.ms.gov.br", "www.spdo.ms.gov.br"), "portal oficial", "assistido"),
    "MG": OfficialSource("DOE-MG", "Diário Oficial do Estado de Minas Gerais", "estadual", "MG", "https://www.jornalminasgerais.mg.gov.br/", ("jornalminasgerais.mg.gov.br", "www.jornalminasgerais.mg.gov.br"), "portal oficial", "assistido"),
    "PA": OfficialSource("DOE-PA", "Diário Oficial do Estado do Pará", "estadual", "PA", "https://www.ioepa.com.br/", ("ioepa.com.br", "www.ioepa.com.br"), "portal oficial", "assistido"),
    "PB": OfficialSource("DOE-PB", "Diário Oficial do Estado da Paraíba", "estadual", "PB", "https://auniao.pb.gov.br/servicos/diario-oficial", ("auniao.pb.gov.br",), "página oficial", "assistido"),
    "PR": OfficialSource("DOE-PR", "Diário Oficial do Estado do Paraná", "estadual", "PR", "https://www.documentos.dioe.pr.gov.br/", ("documentos.dioe.pr.gov.br", "www.documentos.dioe.pr.gov.br", "dioe.pr.gov.br"), "portal oficial", "assistido"),
    "PE": OfficialSource("DOE-PE", "Diário Oficial do Estado de Pernambuco", "estadual", "PE", "https://www.cepe.com.br/", ("cepe.com.br", "www.cepe.com.br"), "portal oficial", "assistido"),
    "PI": OfficialSource("DOE-PI", "Diário Oficial do Estado do Piauí", "estadual", "PI", "https://www.diariooficial.pi.gov.br/", ("diariooficial.pi.gov.br", "www.diariooficial.pi.gov.br"), "portal oficial", "assistido"),
    "RJ": OfficialSource("DOE-RJ", "Diário Oficial do Estado do Rio de Janeiro", "estadual", "RJ", "https://www.ioerj.com.br/", ("ioerj.com.br", "www.ioerj.com.br"), "portal oficial", "assistido"),
    "RN": OfficialSource("DOE-RN", "Diário Oficial do Estado do Rio Grande do Norte", "estadual", "RN", "http://diariooficial.rn.gov.br/", ("diariooficial.rn.gov.br",), "portal oficial", "assistido"),
    "RS": OfficialSource("DOE-RS", "Diário Oficial do Estado do Rio Grande do Sul", "estadual", "RS", "https://www.diariooficial.rs.gov.br/", ("diariooficial.rs.gov.br", "www.diariooficial.rs.gov.br"), "portal oficial", "assistido"),
    "RO": OfficialSource("DOE-RO", "Diário Oficial do Estado de Rondônia", "estadual", "RO", "https://diof.ro.gov.br/", ("diof.ro.gov.br",), "portal oficial", "assistido"),
    "RR": OfficialSource("DOE-RR", "Diário Oficial do Estado de Roraima", "estadual", "RR", "https://www.imprensaoficial.rr.gov.br/", ("imprensaoficial.rr.gov.br", "www.imprensaoficial.rr.gov.br"), "portal oficial", "assistido"),
    "SC": OfficialSource("DOE-SC", "Diário Oficial do Estado de Santa Catarina", "estadual", "SC", "https://portal.doe.sea.sc.gov.br/", ("portal.doe.sea.sc.gov.br", "doe.sea.sc.gov.br", "sea.sc.gov.br"), "portal oficial", "assistido"),
    "SP": OfficialSource("DOE-SP", "Diário Oficial do Estado de São Paulo", "estadual", "SP", "https://www.doe.sp.gov.br/", ("doe.sp.gov.br", "www.doe.sp.gov.br"), "portal oficial", "assistido"),
    "SE": OfficialSource("DOE-SE", "Diário Oficial do Estado de Sergipe", "estadual", "SE", "https://segrase.se.gov.br/", ("segrase.se.gov.br",), "portal oficial", "assistido"),
    "TO": OfficialSource("DOE-TO", "Diário Oficial do Estado do Tocantins", "estadual", "TO", "https://diariooficial.to.gov.br/", ("diariooficial.to.gov.br",), "portal oficial", "assistido"),
}


def all_source_codes() -> list[str]:
    return [FEDERAL_SOURCE.codigo, "QD"] + [src.codigo for src in STATE_SOURCES.values()]


def state_by_code(code: str) -> OfficialSource | None:
    code = code.upper()
    for source in STATE_SOURCES.values():
        if source.codigo.upper() == code or (source.uf and source.uf.upper() == code.replace("DOE-", "")):
            return source
    return None
