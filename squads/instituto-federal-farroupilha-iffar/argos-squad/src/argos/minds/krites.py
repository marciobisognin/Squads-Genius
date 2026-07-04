from argos.contracts import ClassificacaoPublicacao, PerfilInteresse, PublicacaoNormalizada
from argos.engines.kanon_lex import score_lexical

def classificar(perfil: PerfilInteresse, publicacoes: list[PublicacaoNormalizada]) -> list[ClassificacaoPublicacao]:
    out = []
    for pub in publicacoes:
        excerto = next((sent.strip() for sent in pub.texto.split('.') if any(t.lower() in sent.lower() for t in perfil.termos)), pub.texto[:220])
        if excerto and not excerto.endswith('.'):
            excerto = excerto[:220]
        out.append(ClassificacaoPublicacao(id_canonico=pub.id_canonico, relevancia=score_lexical(perfil, pub), categoria=pub.tipo_ato or "Ato relevante", justificativa=f"Correspondência lexical determinística com o perfil {perfil.nome}.", excerto_evidencia=excerto))
    return out
