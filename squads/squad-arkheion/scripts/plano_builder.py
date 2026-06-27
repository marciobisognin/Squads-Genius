#!/usr/bin/env python3
"""plano_builder — esqueleto determinístico do PlanoSequencial (MŶTHOS-suporte).

A partir do tema + tamanho do vídeo informados pelo usuário, monta o ANDAIME do
plano: nº de cenas, contadores `NN / TT`, funções narrativas, âncoras visuais por
tema e títulos-sugestão por função. MŶTHOS (LLM) preenche `titulo`/`texto_digitado`
finais; este script garante a espinha dorsal canônica (contador == roteiro).

Uso:
    python3 scripts/plano_builder.py --tema tecnologia --tamanho 60
    python3 scripts/plano_builder.py --tema "história da educação" --tamanho 30 --marca ACME --protocolo DOSSIE-001
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arkheion import canon  # noqa: E402

# Títulos-âncora por função narrativa (PRD §2.10). São sugestões; MŶTHOS pode refinar.
TITULOS_SUGESTAO = {
    "pergunta_tensao": ["O PROBLEMA", "O LIMITE"],
    "restricao_contexto": ["ACESSO LIMITADO", "O CONTEXTO"],
    "solucao_metodo": ["O MÉTODO", "A CHAVE"],
    "processo": ["EM MOVIMENTO", "NOS BASTIDORES"],
    "prova_visual": ["DADOS REAIS", "NOVA EVIDÊNCIA"],
    "conclusao_cta": ["EM OPERAÇÃO", "DISPONÍVEL AGORA"],
}


def construir_plano(tema: str, tamanho_s: int = 60, marca: str = "ARKHEION",
                    protocolo: str = "DOSSIE-001") -> Dict[str, Any]:
    pd = canon.resolver_duracao(tamanho_s)
    ancoras = canon.ancoras_para_tema(tema)
    beats = []
    for i, (contador, funcao) in enumerate(zip(pd.contadores, pd.funcoes), start=1):
        beat: Dict[str, Any] = {
            "indice": i,
            "funcao": funcao,
            "contador": contador,
            "titulo": TITULOS_SUGESTAO[funcao][0],
            "texto_digitado": ["<MŶTHOS: 1-4 linhas curtas>"],
            "ancoras_visuais": ancoras[: max(2, len(ancoras) // 2)] or ["documentos"],
        }
        if funcao == "prova_visual":
            beat["dataviz"] = {"tipo": "numero", "rotulo": "<métrica>", "valor": "<valor>"}
        beats.append(beat)
    return {
        "titulo_dossie": f"DOSSIÊ — {tema.upper()}",
        "marca": marca,
        "protocolo": protocolo[:24],
        "tamanho_s": pd.duracao_total_s,
        "n_cenas": pd.n_cenas,
        "beats": beats,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Monta o andaime canônico do PlanoSequencial.")
    ap.add_argument("--tema", required=True, help="assunto/tema do dossiê")
    ap.add_argument("--tamanho", type=int, default=canon.DURACAO_DEFAULT_S, help="tamanho do vídeo em s")
    ap.add_argument("--marca", default="ARKHEION")
    ap.add_argument("--protocolo", default="DOSSIE-001")
    args = ap.parse_args()
    plano = construir_plano(args.tema, args.tamanho, args.marca, args.protocolo)
    print(json.dumps(plano, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
