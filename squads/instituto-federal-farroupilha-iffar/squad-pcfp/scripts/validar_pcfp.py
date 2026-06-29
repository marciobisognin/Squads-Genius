#!/usr/bin/env python3
"""Checklist determinístico de conformidade sobre a CostSheet (apoio do A6).

Verificações automatizáveis do PRD:
- Reserva técnica sem indicação de custos → CRÍTICO (Acórdãos TCU 1442/2010 e 593/2010).
- Rubricas de conta vinculada (Anexo XII da IN 05/2017) presentes e flagadas.
- Rubricas não renováveis (IN 07/2018) sinalizadas para a prorrogação.
- Percentuais discricionários fora de faixas de alerta (custos indiretos, lucro).
- Benefícios obrigatórios mínimos presentes (IN 176/2024 / IN 147/2026 — checagem de presença).

Saída: ComplianceReport JSON com findings {severidade, rubrica, descricao, fundamento, recomendacao}.
A avaliação jurídica de mérito é do agente A6 + revisão humana.

Uso:
    python3 scripts/validar_pcfp.py --costsheet costsheet.json [--ci-max 0.10 --lucro-max 0.15]

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
from pathlib import Path

CONTA_VINCULADA_ESPERADAS = {"decimo_terceiro", "ferias_e_terco", "multa_fgts"}
BENEFICIOS_MINIMOS_PRESENCA = ["vale_transporte", "auxilio_alimentacao"]  # presença típica — IN 176/2024 (conferir caso)


def finding(severidade, rubrica, descricao, fundamento, recomendacao):
    return {"severidade": severidade, "rubrica": rubrica, "descricao": descricao,
            "fundamento": fundamento, "recomendacao": recomendacao}


def validar(cs: dict, ci_max: float, lucro_max: float) -> dict:
    findings = []
    rubricas = cs.get("rubricas", [])
    nomes = {r["nome"] for r in rubricas}
    por_nome = {r["nome"]: r for r in rubricas}

    # 1. Reserva técnica
    for r in rubricas:
        if "reserva" in r["nome"].lower() and "tecnica" in r["nome"].lower().replace("é", "e"):
            findings.append(finding(
                "critico", r["nome"],
                "Rubrica de reserva técnica detectada. Reserva técnica sem indicação prévia e detalhada dos custos que a compõem é vedada.",
                "Acórdãos TCU 1442/2010 e 593/2010",
                "Excluir a rubrica ou detalhar analiticamente os custos que a justificam."))

    # 2. Conta vinculada
    faltando_cv = CONTA_VINCULADA_ESPERADAS - {r["nome"] for r in rubricas if r.get("conta_vinculada")}
    if faltando_cv:
        findings.append(finding(
            "alerta", ", ".join(sorted(faltando_cv)),
            "Rubricas tipicamente sujeitas à conta-depósito vinculada não estão flagadas como tal.",
            "Anexo XII da IN SEGES 05/2017",
            "Conferir o destaque das provisões retidas (13º, férias+1/3, multa FGTS) conforme o instrumento do órgão."))

    # 3. Não renováveis
    nao_renovaveis = [r["nome"] for r in rubricas if not r.get("renovavel", True)]
    if nao_renovaveis:
        findings.append(finding(
            "info", ", ".join(nao_renovaveis),
            "Rubricas marcadas como não renováveis: devem ser excluídas/zeradas na prorrogação.",
            "IN SEGES 07/2018 (alterações ao Anexo VII-D)",
            "Sinalizar no instrumento de prorrogação e na repactuação (A7)."))
    else:
        findings.append(finding(
            "alerta", None,
            "Nenhuma rubrica marcada como não renovável — atípico em PCFP de mão de obra.",
            "IN SEGES 07/2018",
            "Conferir aviso prévio trabalhado e demais parcelas não renováveis do caso."))

    # 4. Percentuais discricionários
    dh = cs.get("parametros", {}).get("decisoes_humanas", {})
    try:
        ci = float(dh.get("custos_indiretos_pct", 0))
        lucro = float(dh.get("lucro_pct", 0))
        if ci > ci_max:
            findings.append(finding("alerta", "custos_indiretos",
                                    f"Custos indiretos de {ci:.2%} acima da faixa de alerta ({ci_max:.0%}).",
                                    "Cadernos Técnicos SEGES (faixas de referência — conferir)",
                                    "Justificar formalmente o percentual ou ajustar."))
        if lucro > lucro_max:
            findings.append(finding("alerta", "lucro",
                                    f"Lucro de {lucro:.2%} acima da faixa de alerta ({lucro_max:.0%}).",
                                    "Cadernos Técnicos SEGES (faixas de referência — conferir)",
                                    "Justificar formalmente o percentual ou ajustar."))
        if not dh.get("responsavel"):
            findings.append(finding("critico", None,
                                    "Decisões humanas sem responsável registrado.",
                                    "PRD Squad PCFP — princípio HITL; IN Conjunta MP/CGU 01/2016 (controles internos)",
                                    "Registrar o responsável pela validação antes de instruir o processo."))
    except (TypeError, ValueError):
        findings.append(finding("critico", None, "Percentuais discricionários ilegíveis no input.",
                                "PRD — schema-first", "Corrigir o input da engine."))

    # 5. Benefícios mínimos (presença)
    beneficios_presentes = {r["nome"] for r in rubricas if r["modulo"] == "2.3"}
    for b in BENEFICIOS_MINIMOS_PRESENCA:
        if b not in beneficios_presentes:
            findings.append(finding(
                "alerta", b,
                f"Benefício tipicamente obrigatório '{b}' não localizado no Submódulo 2.3.",
                "IN SEGES/MGI 176/2024 (custos mínimos relevantes); reembolso-creche: IN 147/2026",
                "Conferir CCTProfile e a exigibilidade no caso; justificar a ausência se inaplicável."))

    criticos = sum(1 for f in findings if f["severidade"] == "critico")
    alertas = sum(1 for f in findings if f["severidade"] == "alerta")
    return {
        "schema": "ComplianceReport v1 (PRD Squad PCFP)",
        "resultado": "vermelho" if criticos else ("amarelo" if alertas else "verde"),
        "criticos": criticos, "alertas": alertas,
        "findings": findings,
        "observacao": "Checagem determinística parcial. O checklist completo do caso é montado pelo A3 e executado pelo A6, com revisão humana obrigatória.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--costsheet", required=True)
    ap.add_argument("--ci-max", type=float, default=0.10)
    ap.add_argument("--lucro-max", type=float, default=0.15)
    ap.add_argument("--saida", default=None)
    args = ap.parse_args()
    caminho = Path(args.costsheet)
    if not caminho.is_file():
        print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False)); return 2
    rel = validar(json.loads(caminho.read_text(encoding="utf-8")), args.ci_max, args.lucro_max)
    texto = json.dumps(rel, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(texto, encoding="utf-8"); print(f"ComplianceReport gravado em {args.saida}")
    else:
        print(texto)
    return 0 if rel["resultado"] != "vermelho" else 1


if __name__ == "__main__":
    sys.exit(main())
