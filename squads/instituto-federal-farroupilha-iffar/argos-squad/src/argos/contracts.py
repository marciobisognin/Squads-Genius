from __future__ import annotations
from datetime import date
from typing import Literal, Protocol
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class PublicacaoNormalizada(StrictModel):
    id_canonico: str
    fonte: str
    esfera: Literal["federal", "estadual", "municipal"]
    uf: str | None = None
    data_publicacao: date
    edicao: str
    secao: str | None = None
    orgao: str | None = None
    tipo_ato: str | None = None
    identifica: str | None = None
    ementa: str | None = None
    texto: str
    url_original: HttpUrl
    pagina: str | None = None
    hash_conteudo: str

class PerfilInteresse(StrictModel):
    nome: str
    fontes: list[str]
    termos: list[str] = Field(min_length=1)
    termos_ignorados: list[str] = []
    orgaos: list[str] = []
    tipos_ato: list[str] = []
    secoes: list[str] = []
    janela: Literal["DIA", "SEMANA", "MES"] = "DIA"
    entrega: list[Literal["arquivo", "email", "webhook"]] = ["arquivo"]

class ClassificacaoPublicacao(StrictModel):
    id_canonico: str
    relevancia: int = Field(ge=0, le=100)
    categoria: str
    justificativa: str = Field(max_length=280)
    excerto_evidencia: str

class SintesePublicacao(StrictModel):
    id_canonico: str
    resumo: str = Field(max_length=400)

class VereditoAuditoria(StrictModel):
    aprovado: bool
    itens_reprovados: list[str] = []
    motivos: dict[str, str] = {}

class RoteamentoIntake(StrictModel):
    perfil: str
    caminho: Literal["curto", "desambiguacao", "hitl"]
    motivo: str

class RelatorioComposto(StrictModel):
    run_id: str
    markdown_path: str
    html_path: str
    json_path: str
    corpus_hash: str
    perfil_hash: str

class EdicaoRef(StrictModel):
    fonte: str
    data: date
    secao: str | None = None
    edicao: str
    url: HttpUrl | None = None
    fixture_path: str | None = None

class StatusFonte(StrictModel):
    codigo: str
    estado: Literal["ok", "degradado", "indisponivel", "backlog", "suspensa", "observacao"]
    mensagem: str
    ultima_edicao: date | None = None
    latencia_ms: int | None = None

class AdapterDiario(Protocol):
    codigo: str
    dominios_permitidos: list[str]
    rate_limit_rpm: int
    def listar_edicoes(self, inicio: date, fim: date) -> list[EdicaoRef]: ...
    def obter_publicacoes(self, ref: EdicaoRef) -> list[PublicacaoNormalizada]: ...
    def healthcheck(self) -> StatusFonte: ...
