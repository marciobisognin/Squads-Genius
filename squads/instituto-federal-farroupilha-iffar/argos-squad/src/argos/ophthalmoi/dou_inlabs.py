from __future__ import annotations
import hashlib, html, os, re, zipfile
from datetime import date, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET
from argos.contracts import EdicaoRef, PublicacaoNormalizada, StatusFonte
from argos.ophthalmoi.base import RateLimiter, assert_egress_allowed

def _parse_date(value: str | None) -> date:
    if not value:
        raise ValueError("pubDate ausente")
    value = value.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y%m%d"):
        try:
            return datetime.strptime(value[:10] if fmt == "%Y-%m-%d" else value, fmt).date()
        except ValueError:
            pass
    return date.fromisoformat(value[:10])

def _norm_space(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(text or "")).strip()

def _node_text(article: ET.Element, tag: str) -> str | None:
    node = article.find(f".//{tag}")
    return None if node is None else _norm_space(" ".join(node.itertext()))

def _sanitize_body(article: ET.Element) -> str:
    parts = [_node_text(article, tag) for tag in ("Titulo", "SubTitulo", "Identifica", "Ementa", "Texto")]
    parts = [p for p in parts if p]
    if not parts:
        parts = [_norm_space(" ".join(article.itertext()))]
    return "\n".join(parts).strip()

def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-") or "materia"

class DOUInlabsAdapter:
    codigo = "DOU-INLABS"
    dominios_permitidos = ["inlabs.in.gov.br", "in.gov.br", "www.in.gov.br"]
    rate_limit_rpm = 20
    def __init__(self, fixture_dir: str | Path | None = None):
        self.fixture_dir = Path(fixture_dir) if fixture_dir else None
        self.rate = RateLimiter(self.rate_limit_rpm)
    def healthcheck(self) -> StatusFonte:
        if self.fixture_dir and self.fixture_dir.exists():
            return StatusFonte(codigo=self.codigo, estado="ok", mensagem="modo fixture ativo")
        if not (os.getenv("INLABS_USER") and os.getenv("INLABS_PASSWORD")):
            return StatusFonte(codigo=self.codigo, estado="indisponivel", mensagem="credenciais INLABS ausentes: defina INLABS_USER/INLABS_PASSWORD")
        return StatusFonte(codigo=self.codigo, estado="degradado", mensagem="credenciais presentes; download real deve ser habilitado conforme endpoint INLABS vigente")
    def listar_edicoes(self, inicio: date, fim: date) -> list[EdicaoRef]:
        if self.fixture_dir and self.fixture_dir.exists():
            refs = []
            for xml in sorted(self.fixture_dir.glob("*.xml")):
                art = ET.parse(xml).getroot()
                refs.append(EdicaoRef(fonte=self.codigo, data=_parse_date(art.attrib.get("pubDate")), secao=art.attrib.get("pubName"), edicao=art.attrib.get("editionNumber") or "fixture", fixture_path=str(xml), url=art.attrib.get("urlPage") or "https://www.in.gov.br/"))
            return [r for r in refs if inicio <= r.data <= fim]
        return []
    def obter_publicacoes(self, ref: EdicaoRef) -> list[PublicacaoNormalizada]:
        return [parse_article(Path(ref.fixture_path).read_text(encoding="utf-8"))] if ref.fixture_path else []
    def parse_zip(self, zip_path: str | Path) -> list[PublicacaoNormalizada]:
        out = []
        with zipfile.ZipFile(zip_path) as zf, TemporaryDirectory() as tmp:
            for name in sorted(n for n in zf.namelist() if n.lower().endswith(".xml")):
                target = Path(tmp) / Path(name).name
                target.write_bytes(zf.read(name))
                out.append(parse_article(target.read_text(encoding="utf-8")))
        return out

def parse_article(xml_text: str) -> PublicacaoNormalizada:
    article = ET.fromstring(xml_text)
    attrs = article.attrib
    secao = attrs.get("pubName") or "DOU"
    edicao = attrs.get("editionNumber") or "s/e"
    article_id = attrs.get("id") or attrs.get("name") or hashlib.sha256(xml_text.encode()).hexdigest()[:16]
    texto = _sanitize_body(article)
    identifica = _node_text(article, "Identifica")
    ementa = _node_text(article, "Ementa")
    orgao = _norm_space((attrs.get("artCategory") or "").replace("/", " / ")) or None
    tipo = _norm_space(attrs.get("artType") or "") or None
    canon = hashlib.sha256(f"DOU-INLABS|{secao}|{edicao}|{article_id}".encode()).hexdigest()
    htxt = hashlib.sha256(texto.encode("utf-8")).hexdigest()
    url = attrs.get("urlPage") or attrs.get("url") or attrs.get("artUrl") or "https://www.in.gov.br/web/dou/-/" + _slug(identifica or article_id)
    assert_egress_allowed(url, DOUInlabsAdapter.dominios_permitidos)
    return PublicacaoNormalizada(id_canonico=canon, fonte="DOU-INLABS", esfera="federal", uf=None, data_publicacao=_parse_date(attrs.get("pubDate")), edicao=str(edicao), secao=secao, orgao=orgao, tipo_ato=tipo, identifica=identifica, ementa=ementa, texto=texto, url_original=url, pagina=attrs.get("numberPage") or attrs.get("pdfPage"), hash_conteudo=htxt)
