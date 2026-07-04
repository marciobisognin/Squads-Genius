from argos.contracts import PublicacaoNormalizada, SintesePublicacao

def sintetizar(publicacoes: list[PublicacaoNormalizada]) -> list[SintesePublicacao]:
    out = []
    for pub in publicacoes:
        resumo = (pub.ementa or pub.texto).replace("\n", " ")
        if len(resumo) > 390:
            resumo = resumo[:387].rstrip() + "..."
        out.append(SintesePublicacao(id_canonico=pub.id_canonico, resumo=resumo))
    return out
