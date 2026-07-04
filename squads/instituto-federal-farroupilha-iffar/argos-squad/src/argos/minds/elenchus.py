from argos.contracts import ClassificacaoPublicacao, PublicacaoNormalizada, VereditoAuditoria
from argos.engines.tekmerion import auditar

def revisar(publicacoes: list[PublicacaoNormalizada], classificacoes: list[ClassificacaoPublicacao], verificar_urls: bool = False) -> VereditoAuditoria:
    ok, motivos = auditar({p.id_canonico: p for p in publicacoes}, classificacoes, verificar_urls=verificar_urls)
    return VereditoAuditoria(aprovado=ok, itens_reprovados=list(motivos), motivos=motivos)
