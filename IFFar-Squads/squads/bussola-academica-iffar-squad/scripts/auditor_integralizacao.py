#!/usr/bin/env python3
"""Auditoria determinística de integralização curricular.

Cruza o histórico escolar de um aluno com a matriz curricular vigente e
identifica: componentes aprovados, pendentes, pré-requisitos não satisfeitos
e o percentual de carga horária integralizada. Não decide equivalências —
apenas sinaliza quando o aluno cursou um componente fora da matriz vigente,
para validação da coordenação.

Uso:
    python3 scripts/auditor_integralizacao.py \
        --matriz caminho/matriz_curricular.json \
        --historico caminho/historico_aluno.json

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
from pathlib import Path

SITUACOES_APROVADO = {"aprovado", "aproveitamento", "dispensado"}


def carregar_json(caminho: Path) -> dict:
    return json.loads(caminho.read_text(encoding="utf-8"))


def auditar(matriz: dict, historico: dict) -> dict:
    componentes_matriz = {c["id"]: c for c in matriz.get("componentes", [])}
    cursados = {c["id"]: c.get("situacao", "nao_cursado") for c in historico.get("componentes_cursados", [])}

    aprovados = []
    pendentes = []
    pre_requisitos_nao_satisfeitos = []
    fora_da_matriz = []
    carga_horaria_integralizada = 0

    for comp_id, situacao in cursados.items():
        if comp_id not in componentes_matriz:
            fora_da_matriz.append({"id": comp_id, "situacao": situacao})

    for comp_id, comp in componentes_matriz.items():
        situacao = cursados.get(comp_id, "nao_cursado")
        if situacao in SITUACOES_APROVADO:
            aprovados.append(comp_id)
            carga_horaria_integralizada += comp.get("carga_horaria", 0)
        else:
            pendentes.append({"id": comp_id, "nome": comp.get("nome", comp_id), "situacao": situacao})

        if situacao in SITUACOES_APROVADO or situacao == "cursando":
            for pre_req in comp.get("pre_requisitos", []):
                situacao_pre = cursados.get(pre_req, "nao_cursado")
                if situacao_pre not in SITUACOES_APROVADO:
                    pre_requisitos_nao_satisfeitos.append({
                        "componente": comp_id,
                        "pre_requisito_pendente": pre_req,
                        "situacao_pre_requisito": situacao_pre,
                    })

    carga_horaria_total = matriz.get("carga_horaria_total", 0)
    percentual = round((carga_horaria_integralizada / carga_horaria_total) * 100, 2) if carga_horaria_total else 0.0

    return {
        "curso": matriz.get("curso", "não informado"),
        "aluno": historico.get("aluno", "não informado"),
        "matricula": historico.get("matricula", "não informado"),
        "componentes_aprovados": sorted(aprovados),
        "componentes_pendentes": pendentes,
        "pre_requisitos_nao_satisfeitos": pre_requisitos_nao_satisfeitos,
        "componentes_fora_da_matriz_vigente": fora_da_matriz,
        "carga_horaria_integralizada": carga_horaria_integralizada,
        "carga_horaria_total": carga_horaria_total,
        "percentual_integralizacao": percentual,
        "gate_integralizacao_auditada": "sem_pendencia_bloqueante" if not pre_requisitos_nao_satisfeitos else "pendencia_bloqueante",
        "observacao": "Componentes fora da matriz vigente e pré-requisitos pendentes exigem validação humana da coordenação (possível equivalência ou matrícula irregular).",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--matriz", required=True, help="arquivo JSON da matriz curricular vigente")
    ap.add_argument("--historico", required=True, help="arquivo JSON do histórico escolar do aluno")
    ap.add_argument("--saida", default=None, help="arquivo JSON de saída (padrão: stdout)")
    args = ap.parse_args()

    caminho_matriz = Path(args.matriz)
    caminho_historico = Path(args.historico)
    for caminho in (caminho_matriz, caminho_historico):
        if not caminho.is_file():
            print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False))
            return 2

    try:
        matriz = carregar_json(caminho_matriz)
        historico = carregar_json(caminho_historico)
    except json.JSONDecodeError as e:
        print(json.dumps({"erro": f"JSON inválido: {e}"}, ensure_ascii=False))
        return 2

    resultado = auditar(matriz, historico)
    saida = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(saida, encoding="utf-8")
        print(f"resultado gravado em {args.saida}")
    else:
        print(saida)
    return 0 if resultado["gate_integralizacao_auditada"] == "sem_pendencia_bloqueante" else 1


if __name__ == "__main__":
    sys.exit(main())
