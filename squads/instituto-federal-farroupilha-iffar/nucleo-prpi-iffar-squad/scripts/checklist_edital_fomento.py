#!/usr/bin/env python3
"""Verificação determinística dos campos obrigatórios de um edital de fomento.

Lê os parâmetros de um edital interno de fomento (JSON) e confere a presença
dos campos obrigatórios comuns a qualquer edital e dos campos específicos do
programa (PIBIC, PIBITI, PIBID, extensão).

Uso:
    python3 scripts/checklist_edital_fomento.py --edital caminho/edital.json

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
from pathlib import Path

CAMPOS_OBRIGATORIOS_COMUNS = [
    "programa",
    "objeto",
    "publico_elegivel",
    "cronograma",
    "valor_bolsa",
    "limite_bolsas_por_orientador",
    "documentacao_exigida",
    "criterios_classificacao",
]

CAMPOS_ESPECIFICOS_POR_PROGRAMA = {
    "PIBIC": ["exige_plano_trabalho", "exige_termo_compromisso"],
    "PIBITI": ["exige_plano_trabalho", "exige_termo_compromisso", "area_tecnologica"],
    "PIBID": ["escola_parceira_obrigatoria", "carga_horaria_semanal"],
    "extensao": ["publico_externo_beneficiado", "plano_de_aplicacao"],
}


def verificar(dados: dict) -> dict:
    campos_ausentes_comuns = [c for c in CAMPOS_OBRIGATORIOS_COMUNS if c not in dados or dados[c] in (None, "", [])]

    programa = dados.get("programa")
    campos_especificos = CAMPOS_ESPECIFICOS_POR_PROGRAMA.get(programa, [])
    campos_ausentes_especificos = [c for c in campos_especificos if c not in dados or dados[c] in (None, "", [])]

    campos_ausentes = campos_ausentes_comuns + campos_ausentes_especificos

    return {
        "programa": programa,
        "programa_reconhecido": programa in CAMPOS_ESPECIFICOS_POR_PROGRAMA,
        "campos_ausentes_comuns": campos_ausentes_comuns,
        "campos_ausentes_especificos": campos_ausentes_especificos,
        "gate_edital_aderente_normas": "liberado" if not campos_ausentes else "bloqueado",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--edital", required=True, help="arquivo JSON com os parâmetros do edital")
    ap.add_argument("--saida", default=None, help="arquivo JSON de saída (padrão: stdout)")
    args = ap.parse_args()

    caminho = Path(args.edital)
    if not caminho.is_file():
        print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False))
        return 2
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(json.dumps({"erro": f"JSON inválido: {e}"}, ensure_ascii=False))
        return 2

    resultado = verificar(dados)
    saida = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(saida, encoding="utf-8")
        print(f"resultado gravado em {args.saida}")
    else:
        print(saida)
    return 0 if resultado["gate_edital_aderente_normas"] == "liberado" else 1


if __name__ == "__main__":
    sys.exit(main())
