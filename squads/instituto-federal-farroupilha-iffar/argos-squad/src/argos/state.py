from typing import TypedDict
class ArgosState(TypedDict, total=False):
    run_id: str
    perfil_nome: str
    corpus_hash: str
    perfil_hash: str
    fontes_consultadas: list[str]
    fontes_lacuna: list[str]
    lacunas: list[str]
