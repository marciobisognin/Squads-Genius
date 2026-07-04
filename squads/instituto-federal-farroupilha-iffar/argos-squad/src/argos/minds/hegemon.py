from argos.contracts import PerfilInteresse, RoteamentoIntake

def rotear(perfil: PerfilInteresse, hitl: bool = False) -> RoteamentoIntake:
    if hitl or any(f.startswith("DOE-") for f in perfil.fontes):
        return RoteamentoIntake(perfil=perfil.nome, caminho="hitl", motivo="perfil envolve fonte estadual ou execução com --hitl")
    return RoteamentoIntake(perfil=perfil.nome, caminho="curto", motivo="perfil declarativo validado")
