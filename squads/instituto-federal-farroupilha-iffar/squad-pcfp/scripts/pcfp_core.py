#!/usr/bin/env python3
"""pcfp-core — engine determinística da PCFP (fundação F0 do roadmap do PRD).

Preenche os módulos 1-6 do Anexo VII-D da IN SEGES 05/2017 a partir de um
input JSON, produzindo a CostSheet: cada rubrica com {modulo, nome, valor,
formula, fundamento, renovavel, conta_vinculada}. Aritmética em Decimal.

PRINCÍPIOS (PRD Squad PCFP v1.0):
- Nenhum valor é "gerado" por LLM: este código é a única fonte de números.
- Percentuais de encargos ficam na tabela CONFIG_REFERENCIA, versionada —
  são VALORES DE REFERÊNCIA que DEVEM ser conferidos contra a redação
  vigente das normas e os Cadernos Técnicos SEGES antes do uso oficial.
- Percentuais discricionários (custos indiretos, lucro) e regime tributário
  são DECISÕES HUMANAS: vêm no input, sem default silencioso.

Uso:
    python3 scripts/pcfp_core.py --input examples/exemplo_input_limpeza44h.json [--saida costsheet.json]

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

D = Decimal
CENT = D("0.01")

# Percentuais de REFERÊNCIA (conferir Caderno Técnico/redação vigente — ver docs/base_normativa.md)
CONFIG_REFERENCIA = {
    "submodulo_2_1": {
        "decimo_terceiro": ("0.0833", "13º salário — 1/12 avos", "CF/88 art. 7º, VIII; Anexo VII-D Submódulo 2.1"),
        "ferias_e_terco": ("0.1111", "férias (1/12) + 1/3 constitucional", "CF/88 art. 7º, XVII; Anexo VII-D Submódulo 2.1"),
    },
    "submodulo_2_2": {
        "inss_patronal": ("0.20", "contribuição previdenciária patronal", "Lei 8.212/1991, art. 22, I — conferir reoneração Lei 14.973/2024"),
        "fgts": ("0.08", "FGTS", "Lei 8.036/1990, art. 15"),
        "rat_fap": ("0.03", "RAT ajustado pelo FAP (informar o do CNAE/empresa)", "Lei 8.212/1991, art. 22, II — RAT×FAP do caso"),
        "terceiros": ("0.058", "salário-educação + Sistema S + INCRA", "conferir alíquotas de terceiros do FPAS do caso"),
    },
    "modulo_3": {
        "aviso_previo_indenizado": ("0.0042", "provisão de aviso prévio indenizado", "Anexo VII-D Módulo 3 — referência Caderno Técnico"),
        "aviso_previo_trabalhado": ("0.0194", "provisão de aviso prévio trabalhado", "Anexo VII-D Módulo 3 — referência Caderno Técnico"),
        "multa_fgts": ("0.04", "multa do FGTS sobre remuneração (40% x 8% + projeção)", "Lei 8.036/1990, art. 18, §1º — referência simplificada"),
    },
    "modulo_4": {
        "ferias_substituto": ("0.0833", "cobertura de férias do titular", "Anexo VII-D Módulo 4 — habilitado por cobertura ininterrupta"),
        "ausencias_legais": ("0.0166", "ausências legais e enfermidade (referência)", "CLT art. 473; Caderno Técnico — conferir"),
        "afastamento_maternidade": ("0.0008", "afastamento maternidade (referência)", "Caderno Técnico — conferir"),
    },
}

NAO_RENOVAVEIS = {"aviso_previo_trabalhado"}  # IN 07/2018 — conferir demais rubricas do caso
CONTA_VINCULADA = {"decimo_terceiro", "ferias_e_terco", "multa_fgts"}  # Anexo XII IN 05/2017


def dec(v) -> Decimal:
    return D(str(v))


def money(v: Decimal) -> Decimal:
    return v.quantize(CENT, rounding=ROUND_HALF_UP)


def rubrica(modulo, nome, valor, formula, fundamento, renovavel=True, conta_vinculada=False):
    return {
        "modulo": modulo,
        "nome": nome,
        "valor": float(money(valor)),
        "formula": formula,
        "fundamento": fundamento,
        "renovavel": renovavel,
        "conta_vinculada": conta_vinculada,
    }


def calcular(inp: dict) -> dict:
    erros = []
    for campo in ("salario_base", "decisoes_humanas"):
        if campo not in inp:
            erros.append(f"campo obrigatório ausente: {campo}")
    dh = inp.get("decisoes_humanas", {})
    for campo in ("custos_indiretos_pct", "lucro_pct", "regime_tributario", "responsavel"):
        if campo not in dh:
            erros.append(f"decisão humana obrigatória ausente: decisoes_humanas.{campo} (sem default silencioso)")
    if erros:
        return {"erro": erros}

    rubricas = []
    salario = dec(inp["salario_base"])

    # ---- Módulo 1 — Composição da Remuneração ----
    rubricas.append(rubrica("1", "salario_base", salario, "piso da CCT", ["CCTProfile — cláusula do piso (HITL Gate 1)"]))
    m1 = salario
    for ad in inp.get("adicionais", []):
        nome, base = ad["nome"], ad.get("base", "salario_base")
        if "percentual" in ad:
            pct = dec(ad["percentual"])
            base_valor = salario if base == "salario_base" else dec(ad["base_valor"])
            valor = base_valor * pct
            formula = f"{pct} * {base} ({base_valor})"
        else:
            valor = dec(ad["valor"])
            formula = "valor direto da CCT/laudo"
        rubricas.append(rubrica("1", nome, valor, formula, ad.get("fundamento", ["CCT/laudo — informar cláusula"])))
        m1 += valor

    # ---- Submódulo 2.1 — 13º e férias ----
    s21 = D(0)
    for chave, (pct, desc, fund) in CONFIG_REFERENCIA["submodulo_2_1"].items():
        valor = m1 * D(pct)
        rubricas.append(rubrica("2.1", chave, valor, f"{pct} * M1 ({money(m1)})", [desc, fund, "percentual de referência — conferir"],
                                conta_vinculada=chave in CONTA_VINCULADA))
        s21 += valor

    # ---- Submódulo 2.2 — encargos sobre M1 + 2.1 ----
    base_22 = m1 + s21
    s22 = D(0)
    overrides = inp.get("percentuais_overrides", {}).get("submodulo_2_2", {})
    for chave, (pct_ref, desc, fund) in CONFIG_REFERENCIA["submodulo_2_2"].items():
        pct = dec(overrides.get(chave, pct_ref))
        origem = "override do caso" if chave in overrides else "referência — conferir"
        valor = base_22 * pct
        rubricas.append(rubrica("2.2", chave, valor, f"{pct} * (M1 + S2.1) ({money(base_22)})", [desc, fund, origem]))
        s22 += valor

    # ---- Submódulo 2.3 — benefícios CCT (com desconto/coparticipação) ----
    s23 = D(0)
    for b in inp.get("beneficios", []):
        bruto = dec(b["valor_mensal"])
        desconto = dec(b.get("desconto_empregado", 0))
        valor = bruto - desconto
        rubricas.append(rubrica("2.3", b["nome"], valor, f"{bruto} - desconto {desconto}",
                                [b.get("fundamento", "CCT — informar cláusula"), "coparticipação descontada"]))
        s23 += valor

    # ---- Módulo 3 — Provisão para rescisão ----
    m3 = D(0)
    for chave, (pct, desc, fund) in CONFIG_REFERENCIA["modulo_3"].items():
        valor = m1 * D(pct)
        rubricas.append(rubrica("3", chave, valor, f"{pct} * M1 ({money(m1)})", [desc, fund, "percentual de referência — conferir"],
                                renovavel=chave not in NAO_RENOVAVEIS, conta_vinculada=chave in CONTA_VINCULADA))
        m3 += valor

    # ---- Módulo 4 — Reposição do profissional ausente ----
    m4 = D(0)
    if inp.get("cobertura_ininterrupta", False):
        base_m4 = m1 + s21 + s22
        for chave, (pct, desc, fund) in CONFIG_REFERENCIA["modulo_4"].items():
            valor = base_m4 * D(pct)
            rubricas.append(rubrica("4", chave, valor, f"{pct} * (M1 + M2.1 + M2.2) ({money(base_m4)})",
                                    [desc, fund, "percentual de referência — conferir"]))
            m4 += valor
    else:
        rubricas.append(rubrica("4", "nao_aplicavel", D(0), "cobertura_ininterrupta = false",
                                ["Módulo 4 habilitado apenas com cobertura ininterrupta (ServiceProfile)"]))

    # ---- Módulo 5 — Insumos diversos ----
    m5 = D(0)
    for ins in inp.get("insumos", []):
        valor = dec(ins["valor_mensal"])
        rubricas.append(rubrica("5", ins["nome"], valor, "valor mensal informado",
                                [ins.get("fundamento", "TR/ETP — memória de cálculo do órgão")]))
        m5 += valor

    # ---- Módulo 6 — CIT&L (decisões humanas + gross-up de tributos) ----
    subtotal = m1 + s21 + s22 + s23 + m3 + m4 + m5
    ci_pct, lucro_pct = dec(dh["custos_indiretos_pct"]), dec(dh["lucro_pct"])
    ci = subtotal * ci_pct
    lucro = (subtotal + ci) * lucro_pct
    base_tributavel = subtotal + ci + lucro
    trib = dh.get("tributos", {})
    soma_t = sum(dec(v) for v in trib.values())
    if soma_t >= 1:
        return {"erro": ["soma das alíquotas de tributos >= 100% — verificar input"]}
    preco_posto = base_tributavel / (D(1) - soma_t)
    tributos_valor = preco_posto - base_tributavel

    rubricas.append(rubrica("6", "custos_indiretos", ci, f"{ci_pct} * subtotal ({money(subtotal)})",
                            [f"DECISÃO HUMANA registrada — responsável: {dh['responsavel']}"]))
    rubricas.append(rubrica("6", "lucro", lucro, f"{lucro_pct} * (subtotal + CI)",
                            [f"DECISÃO HUMANA registrada — responsável: {dh['responsavel']}"]))
    for tnome, tpct in trib.items():
        rubricas.append(rubrica("6", f"tributo_{tnome}", preco_posto * dec(tpct),
                                f"{tpct} * preço (gross-up: base/(1-{soma_t}))",
                                [f"regime: {dh['regime_tributario']}", "alíquota do caso — conferir transição CBS/IBS (LC 214/2025)"]))

    qtd = int(inp.get("qtd_postos", 1))
    total_mensal = preco_posto * qtd
    return {
        "schema": "CostSheet v1 (PRD Squad PCFP)",
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "engine": "pcfp_core.py (fundação F0 — golden tests dos Cadernos Técnicos pendentes, ver roadmap)",
        "aviso": "Percentuais de referência DEVEM ser conferidos contra a redação vigente e os Cadernos Técnicos SEGES. Automação não é parecer jurídico.",
        "parametros": {"salario_base": float(salario), "qtd_postos": qtd, "cobertura_ininterrupta": bool(inp.get("cobertura_ininterrupta", False)),
                       "decisoes_humanas": dh},
        "totais": {
            "modulo_1": float(money(m1)), "submodulo_2_1": float(money(s21)), "submodulo_2_2": float(money(s22)),
            "submodulo_2_3": float(money(s23)), "modulo_3": float(money(m3)), "modulo_4": float(money(m4)),
            "modulo_5": float(money(m5)), "custos_indiretos": float(money(ci)), "lucro": float(money(lucro)),
            "tributos": float(money(tributos_valor)), "preco_por_posto_mensal": float(money(preco_posto)),
            "total_mensal_contrato": float(money(total_mensal)),
        },
        "rubricas": rubricas,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="JSON com ServiceProfile+CCTProfile consolidados e decisões humanas")
    ap.add_argument("--saida", default=None)
    args = ap.parse_args()
    caminho = Path(args.input)
    if not caminho.is_file():
        print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False)); return 2
    resultado = calcular(json.loads(caminho.read_text(encoding="utf-8")))
    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(texto, encoding="utf-8"); print(f"CostSheet gravada em {args.saida}")
    else:
        print(texto)
    return 0 if "erro" not in resultado else 1


if __name__ == "__main__":
    sys.exit(main())
