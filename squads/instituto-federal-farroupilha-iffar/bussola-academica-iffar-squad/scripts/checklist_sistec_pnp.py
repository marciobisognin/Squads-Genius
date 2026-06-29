#!/usr/bin/env python3
"""Checklist determinístico de consistência para envio a SISTEC/Plataforma Nilo Peçanha.

Lê um registro acadêmico em JSON e verifica a presença e a coerência mínima
dos campos exigidos para o envio oficial, sinalizando divergências para
correção pela secretaria acadêmica antes do envio real (este script NÃO
envia dados a nenhum sistema externo).

Uso:
    python3 scripts/checklist_sistec_pnp.py --registro caminho/registro.json

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
from pathlib import Path

CAMPOS_OBRIGATORIOS = {
    "aluno.nome": "Nome completo do aluno.",
    "aluno.matricula": "Número de matrícula do aluno.",
    "curso": "Nome do curso conforme catálogo/matriz vigente.",
    "situacao_matricula": "Situação atual: matriculado, concluinte, evadido, trancado ou transferido.",
    "data_inicio": "Data de início do vínculo com o curso.",
    "carga_horaria_cursada": "Carga horária cursada até o momento.",
}

SITUACOES_VALIDAS = {"matriculado", "concluinte", "evadido", "trancado", "transferido"}


def obter(dados: dict, caminho: str):
    atual = dados
    for parte in caminho.split("."):
        if not isinstance(atual, dict) or parte not in atual:
            return None
        atual = atual[parte]
    return atual


def vazio(valor) -> bool:
    return valor is None or (isinstance(valor, str) and not valor.strip())


def checar(registro: dict) -> dict:
    divergencias = []
    campos_presentes = []

    for campo, descricao in CAMPOS_OBRIGATORIOS.items():
        if vazio(obter(registro, campo)):
            divergencias.append({"campo": campo, "tipo": "ausente", "descricao": descricao})
        else:
            campos_presentes.append(campo)

    situacao = (registro.get("situacao_matricula") or "").strip().lower()
    if situacao and situacao not in SITUACOES_VALIDAS:
        divergencias.append({
            "campo": "situacao_matricula",
            "tipo": "valor_invalido",
            "valor_local": situacao,
            "valor_esperado": sorted(SITUACOES_VALIDAS),
        })

    if situacao == "concluinte" and vazio(registro.get("data_conclusao")):
        divergencias.append({
            "campo": "data_conclusao",
            "tipo": "ausente",
            "descricao": "Situação 'concluinte' exige data de conclusão.",
        })

    carga_cursada = registro.get("carga_horaria_cursada")
    carga_matriz = registro.get("carga_horaria_matriz_referencia")
    if situacao == "concluinte" and carga_cursada is not None and carga_matriz is not None:
        if carga_cursada < carga_matriz:
            divergencias.append({
                "campo": "carga_horaria_cursada",
                "tipo": "divergencia",
                "valor_local": carga_cursada,
                "valor_esperado": f">= {carga_matriz} (carga horária total da matriz de referência)",
            })

    return {
        "campos_presentes": campos_presentes,
        "divergencias": divergencias,
        "gate_dados_consistentes_sistec_pnp": "consistente" if not divergencias else "divergencia_a_corrigir",
        "observacao": "Checagem determinística de presença e coerência mínima. Nenhum envio é realizado por este script; o responsável pela secretaria acadêmica faz o envio após corrigir as divergências.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--registro", required=True, help="arquivo JSON com o registro acadêmico")
    ap.add_argument("--saida", default=None, help="arquivo JSON de saída (padrão: stdout)")
    args = ap.parse_args()

    caminho = Path(args.registro)
    if not caminho.is_file():
        print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False))
        return 2
    try:
        registro = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(json.dumps({"erro": f"JSON inválido: {e}"}, ensure_ascii=False))
        return 2

    resultado = checar(registro)
    saida = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(saida, encoding="utf-8")
        print(f"resultado gravado em {args.saida}")
    else:
        print(saida)
    return 0 if resultado["gate_dados_consistentes_sistec_pnp"] == "consistente" else 1


if __name__ == "__main__":
    sys.exit(main())
