#!/usr/bin/env python3
"""Verificação determinística da suficiência da solicitação de contratação.

Lê a solicitação em JSON (estrutura do templates/solicitacao_contratacao.yaml,
convertida para JSON) e verifica os campos obrigatórios — comuns e específicos
da modalidade — gerando a lista de lacunas e as perguntas pendentes que o
agente intake-requisitos-clarifier apresenta ao usuário.

Uso:
    python3 scripts/intake_suficiencia.py --solicitacao caminho/solicitacao.json

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
from pathlib import Path

CAMPOS_COMUNS = {
    "orgao": "Qual é o órgão/entidade e a unidade requisitante?",
    "esfera": "Qual a esfera: federal, estadual ou municipal?",
    "objeto.descricao": "Descreva o objeto: o que exatamente será contratado?",
    "objeto.natureza": "Qual a natureza do objeto (bem comum, serviço comum, serviço com mão de obra dedicada, obra, serviço de engenharia, TIC)?",
    "objeto.quantitativos": "Quais os quantitativos estimados e a unidade de medida?",
    "justificativa_necessidade": "Qual problema/necessidade justifica a contratação?",
    "prazo_vigencia_pretendida": "Qual a vigência pretendida do contrato?",
}

CAMPOS_POR_MODALIDADE = {
    "pregao": {
        "criterio_julgamento": "Critério de julgamento: menor preço ou maior desconto?",
        "condicoes_especiais.srp": "Haverá registro de preços (SRP)? (sim/não)",
    },
    "concorrencia": {
        "criterio_julgamento": "Critério de julgamento (menor preço, técnica e preço, maior desconto...)?",
        "regime_execucao": "Qual o regime de execução pretendido (art. 46 da Lei 14.133/2021)?",
    },
    "dispensa": {
        "hipotese_legal": "Qual a hipótese de dispensa (inciso do art. 75)? Ex.: baixo valor, emergência.",
        "valor_estimado": "Qual o valor estimado? (necessário para verificar limite de baixo valor)",
    },
    "inexigibilidade": {
        "hipotese_legal": "Qual a hipótese do art. 74 (exclusividade, notória especialização, artista, credenciamento)?",
        "razao_escolha_contratado": "Qual a razão da escolha do contratado e a evidência de inviabilidade de competição?",
    },
    "dialogo_competitivo": {
        "justificativa_dialogo": "Por que as condições do art. 32 estão presentes (inovação, impossibilidade de especificação prévia)?",
    },
    "leilao": {
        "bens_a_alienar": "Quais bens serão alienados e qual a avaliação prévia?",
    },
    "concurso": {
        "premio_remuneracao": "Qual o prêmio ou remuneração prevista para o vencedor?",
    },
    "indefinida": {},
}


def obter(dados: dict, caminho: str):
    atual = dados
    for parte in caminho.split("."):
        if not isinstance(atual, dict) or parte not in atual:
            return None
        atual = atual[parte]
    return atual


def vazio(valor) -> bool:
    return valor is None or (isinstance(valor, str) and not valor.strip()) or (isinstance(valor, (list, dict)) and not valor)


def avaliar(dados: dict) -> dict:
    modalidade = str(dados.get("modalidade_pretendida", "indefinida")).strip().lower() or "indefinida"
    if modalidade not in CAMPOS_POR_MODALIDADE:
        modalidade_chave = "indefinida"
    else:
        modalidade_chave = modalidade

    obrigatorios = dict(CAMPOS_COMUNS)
    obrigatorios.update(CAMPOS_POR_MODALIDADE[modalidade_chave])

    lacunas = []
    presentes = []
    for campo, pergunta in obrigatorios.items():
        if vazio(obter(dados, campo)):
            lacunas.append({"campo": campo, "pergunta": pergunta, "classificacao": "bloqueante"})
        else:
            presentes.append(campo)

    avisos = []
    if modalidade_chave == "indefinida":
        avisos.append("Modalidade não informada: o enquadramento-modalidade-strategist proporá a mais adequada.")
    if vazio(dados.get("valor_estimado")) and modalidade_chave != "dispensa":
        avisos.append("Valor estimado não informado: será construído pela pesquisa de preços (não bloqueante).")

    return {
        "modalidade_avaliada": modalidade_chave,
        "gate_intake_suficiente": "liberado" if not lacunas else "bloqueado",
        "campos_presentes": presentes,
        "lacunas_bloqueantes": lacunas,
        "avisos": avisos,
        "observacao": "Checagem determinística de presença de campos. A avaliação de QUALIDADE do conteúdo é do agente intake-requisitos-clarifier, com revisão humana.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solicitacao", required=True, help="arquivo JSON com a solicitação")
    ap.add_argument("--saida", default=None, help="arquivo JSON de saída (padrão: stdout)")
    args = ap.parse_args()

    caminho = Path(args.solicitacao)
    if not caminho.is_file():
        print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False))
        return 2
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(json.dumps({"erro": f"JSON inválido: {e}"}, ensure_ascii=False))
        return 2

    resultado = avaliar(dados)
    saida = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(saida, encoding="utf-8")
        print(f"resultado gravado em {args.saida}")
    else:
        print(saida)
    return 0 if resultado["gate_intake_suficiente"] == "liberado" else 1


if __name__ == "__main__":
    sys.exit(main())
