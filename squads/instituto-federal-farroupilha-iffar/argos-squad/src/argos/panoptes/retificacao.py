from __future__ import annotations
import difflib, re
from argos.engines.mnemon import Mnemon

_NUMERO = re.compile(r"\d(?:[\d.,/-]*\d)?")

def extrair_numeros(texto: str) -> list[str]:
    return _NUMERO.findall(texto or "")

def diff_textos(antigo: str, novo: str) -> dict:
    diff = [l.rstrip("\n") for l in difflib.unified_diff((antigo or "").splitlines(), (novo or "").splitlines(), fromfile="versao_anterior", tofile="versao_nova", lineterm="")]
    antes, depois = set(extrair_numeros(antigo)), set(extrair_numeros(novo))
    return {
        "diff": diff,
        "numeros_removidos": sorted(antes - depois),
        "numeros_adicionados": sorted(depois - antes),
    }

def relatorio_retificacoes(mnemon: Mnemon) -> list[dict]:
    """Cada retificação vira um dossiê: o que mudou, linha a linha, e quais números foram alterados.

    Números que somem/aparecem entre versões (valores, prazos, CNPJs) são o sinal
    de maior risco em republicações silenciosas de atos oficiais.
    """
    dossies = []
    for ret in mnemon.listar_retificacoes():
        antigo = mnemon.texto_versao(ret["id_canonico"], ret["hash_anterior"])
        novo = mnemon.texto_versao(ret["id_canonico"], ret["hash_novo"])
        analise = diff_textos(antigo or "", novo or "") if (antigo is not None or novo is not None) else {"diff": [], "numeros_removidos": [], "numeros_adicionados": []}
        dossies.append({**ret, **analise, "versao_anterior_disponivel": antigo is not None, "versao_nova_disponivel": novo is not None})
    return dossies
