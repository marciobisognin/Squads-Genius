#!/usr/bin/env python3
"""Engine determinística da Conta-Depósito Vinculada (Anexo XII da IN 05/2017).

Núcleo de cálculo do squad Árgus — Conta Vinculada. NENHUM valor monetário deste
domínio deve ser produzido por LLM: tudo é calculado aqui, em Python puro (apenas
biblioteca padrão), de forma testável e auditável.

Cobre:
- provisão mensal por trabalhador (13º, férias+1/3, multa s/ aviso, incidência 2.2);
- saldo acumulado;
- liberação por evento (13º por avos, férias proporcional+1/3, rescisão, encerramento);
- multa rescisória (40% sem justa causa / 20% acordo) sobre o saldo do extrato FGTS.

Os percentuais são valores de PARTIDA (item 14 do Anexo XII / Submódulo 2.2 do
Anexo VII-D). DEVEM ser conferidos contra a redação vigente e os Cadernos de
Logística da SEGES. A multa sobre aviso é parametrizável (4% atual / 5% literal).

Uso:
    python3 conta_vinculada_core.py --self-test
    python3 conta_vinculada_core.py --provisao --remuneracao 2000 --regime lucro_real_presumido --sat 1 --multa 4
    python3 conta_vinculada_core.py --input exemplo.json

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date
from decimal import ROUND_HALF_UP, Decimal, getcontext
from typing import Any, Dict, List, Optional

getcontext().prec = 28

# ---------------------------------------------------------------------------
# Tabela de percentuais versionada (referência — conferir redação vigente)
# ---------------------------------------------------------------------------
CONFIG: Dict[str, Any] = {
    "versao": "2018.1",
    "vigencia": "Caderno de Logística Conta Vinculada v2.0/2018; item 14 do Anexo XII da IN SEGES/MPDG 05/2017",
    "fontes": [
        "IN SEGES/MPDG 05/2017, Anexo XII, item 14",
        "Anexo VII-D, Submódulo 2.2 (Grupo A)",
        "Lei 13.932/2019, art. 12 (extinção da contribuição social de 10% do FGTS)",
        "Orientação nº 26 do Portal de Compras do Governo Federal (multa 5% -> 4%)",
    ],
    # Provisões mensais sobre a remuneração (campo A)
    "decimo_terceiro": "0.0833",       # 1/12
    "ferias_um_terco": "0.1210",       # 0.09075 (férias) + 0.03025 (1/3)
    "multa_fgts_aviso": {              # multa do FGTS + (ex-)contribuição social sobre aviso prévio
        "atual": "0.04",              # pós Lei 13.932/2019 / Orientação nº 26 (default recomendado)
        "literal": "0.05",            # redação literal do Anexo XII
    },
    # Incidência do Submódulo 2.2 sobre as provisões de 13º e férias+1/3
    # base = 13º a 1/11 (0.0909) + férias+1/3 (0.1210) = 0.2119
    "incidencia_base_coef": "0.2119",
    # Submódulo 2.2 (Grupo A) — total por regime
    "submodulo_2_2": {
        # Lucro Real/Presumido: parte fixa (sem RAT) + RAT*FAP
        # fixa = INSS 20 + Sal-Educação 2,5 + SESC/SESI 1,5 + SENAI/SENAC 1,0 + SEBRAE 0,6 + INCRA 0,2 + FGTS 8 = 33,8%
        "lucro_real_presumido": {
            "fixa": "0.338",
            "rat_por_sat": {"1": "0.01", "2": "0.02", "3": "0.03"},
        },
        # Simples Nacional (Anexos I-III): apenas FGTS 8%
        "simples_nacional": {"total": "0.08"},
    },
    # Multa rescisória sobre o saldo do FGTS (extrato)
    "multa_rescisoria": {"sem_justa_causa": "0.40", "acordo": "0.20"},
}

CENTAVO = Decimal("0.01")


def _d(value: Any) -> Decimal:
    """Converte para Decimal de forma segura."""
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def _money(value: Decimal) -> Decimal:
    """Arredonda para centavos (ROUND_HALF_UP)."""
    return value.quantize(CENTAVO, rounding=ROUND_HALF_UP)


# ---------------------------------------------------------------------------
# Parâmetros do contrato
# ---------------------------------------------------------------------------
@dataclass
class ContratoParams:
    regime: str = "lucro_real_presumido"      # ou "simples_nacional"
    sat: str = "1"                            # "1" | "2" | "3"
    fap: Decimal = field(default_factory=lambda: Decimal("1.0"))
    multa_modo: str = "atual"                 # "atual" (4%) | "literal" (5%)
    jornada: int = 44                         # 40 (Decreto 12.174/2024) ou 44

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContratoParams":
        return cls(
            regime=data.get("regime", "lucro_real_presumido"),
            sat=str(data.get("sat", "1")),
            fap=_d(data.get("fap", "1.0")),
            multa_modo=data.get("multa_modo", "atual"),
            jornada=int(data.get("jornada", 44)),
        )


def total_submodulo_2_2(params: ContratoParams) -> Decimal:
    """Total do Submódulo 2.2 (Grupo A) em decimal, conforme regime/SAT/FAP."""
    sub = CONFIG["submodulo_2_2"]
    if params.regime == "simples_nacional":
        return _d(sub["simples_nacional"]["total"])
    fixa = _d(sub["lucro_real_presumido"]["fixa"])
    rat_map = sub["lucro_real_presumido"]["rat_por_sat"]
    if params.sat not in rat_map:
        raise ValueError(f"SAT inválido: {params.sat!r} (use '1', '2' ou '3')")
    rat = _d(rat_map[params.sat]) * params.fap
    return fixa + rat


def multa_aviso_percent(params: ContratoParams) -> Decimal:
    modo = params.multa_modo
    if modo not in CONFIG["multa_fgts_aviso"]:
        raise ValueError(f"multa_modo inválido: {modo!r} (use 'atual' ou 'literal')")
    return _d(CONFIG["multa_fgts_aviso"][modo])


# ---------------------------------------------------------------------------
# Provisão mensal
# ---------------------------------------------------------------------------
def _rubrica(nome: str, valor: Decimal, percentual: Decimal, formula: str, fundamento: str) -> Dict[str, Any]:
    return {
        "nome": nome,
        "valor": str(_money(valor)),
        "percentual": str(percentual),
        "formula": formula,
        "fundamento": fundamento,
    }


def provisao_mensal(remuneracao: Any, params: ContratoParams) -> Dict[str, Any]:
    """Provisão mensal da conta-vinculada para um trabalhador numa competência.

    Retorna as rubricas B (13º), C (férias+1/3), D (multa s/ aviso),
    E (incidência 2.2) e o total mensal a depositar, com memória de cálculo.
    """
    A = _d(remuneracao)
    p_13 = _d(CONFIG["decimo_terceiro"])
    p_fer = _d(CONFIG["ferias_um_terco"])
    p_multa = multa_aviso_percent(params)
    total_22 = total_submodulo_2_2(params)
    coef_inc = _d(CONFIG["incidencia_base_coef"])
    p_inc = total_22 * coef_inc

    B = A * p_13
    C = A * p_fer
    D = A * p_multa
    E = A * p_inc
    total = _money(B) + _money(C) + _money(D) + _money(E)

    rubricas = [
        _rubrica("13º salário", B, p_13, f"{A} × {p_13}", "Anexo XII, item 14 (1/12)"),
        _rubrica("Férias + 1/3", C, p_fer, f"{A} × {p_fer}", "Anexo XII, item 14 (9,075% + 3,025%)"),
        _rubrica(
            "Multa FGTS s/ aviso prévio", D, p_multa, f"{A} × {p_multa}",
            f"Anexo XII, item 14 ({'4% atual' if params.multa_modo == 'atual' else '5% literal'})",
        ),
        _rubrica(
            "Incidência Submódulo 2.2", E, p_inc,
            f"{A} × ({total_22} × {coef_inc})",
            f"Submódulo 2.2 ({params.regime}, SAT {params.sat}, FAP {params.fap})",
        ),
    ]
    return {
        "remuneracao": str(_money(A)),
        "regime": params.regime,
        "sat": params.sat,
        "fap": str(params.fap),
        "multa_modo": params.multa_modo,
        "total_submodulo_2_2": str(total_22),
        "rubricas": rubricas,
        "total_mensal": str(_money(total)),
        "percentual_total": str((p_13 + p_fer + p_multa + p_inc).quantize(Decimal("0.000001"))),
    }


def saldo_acumulado(totais_mensais: List[Any], liberacoes: Optional[List[Any]] = None) -> str:
    """Saldo = soma das provisões mensais − soma das liberações. Nunca negativo (erro se ficar)."""
    entradas = sum((_d(v) for v in totais_mensais), Decimal("0"))
    saidas = sum((_d(v) for v in (liberacoes or [])), Decimal("0"))
    saldo = _money(entradas - saidas)
    if saldo < 0:
        raise ValueError(f"Saldo negativo ({saldo}): liberações excedem as provisões acumuladas")
    return str(saldo)


# ---------------------------------------------------------------------------
# Avos
# ---------------------------------------------------------------------------
def meses_avos(inicio: str, fim: str) -> int:
    """Conta avos (meses) entre duas datas ISO (YYYY-MM-DD). Mês com ≥ 15 dias = mês cheio.

    Regra do Caderno de Logística: fração igual ou superior a 15 dias conta como mês inteiro.
    Resultado limitado a 12 (um ciclo anual).
    """
    d0 = date.fromisoformat(inicio)
    d1 = date.fromisoformat(fim)
    if d1 < d0:
        raise ValueError("data final anterior à inicial")
    meses = (d1.year - d0.year) * 12 + (d1.month - d0.month)
    # dias residuais no último mês parcial
    if d1.day >= d0.day:
        dias_residuais = d1.day - d0.day
    else:
        meses -= 1
        # aproxima dias do mês anterior (30 dias) — suficiente para a regra dos 15 dias
        dias_residuais = (30 - d0.day) + d1.day
    if dias_residuais >= 15:
        meses += 1
    return max(0, min(12, meses))


# ---------------------------------------------------------------------------
# Liberações
# ---------------------------------------------------------------------------
def liberacao_decimo_terceiro(remuneracao: Any, avos: int, params: ContratoParams) -> Dict[str, Any]:
    A = _d(remuneracao)
    if not 0 <= avos <= 12:
        raise ValueError("avos deve estar entre 0 e 12")
    total_22 = total_submodulo_2_2(params)
    principal = A * Decimal(avos) / Decimal(12)
    encargos = principal * total_22
    total = _money(principal) + _money(encargos)
    return {
        "evento": "13º",
        "avos": avos,
        "principal": str(_money(principal)),
        "encargos": str(_money(encargos)),
        "total": str(_money(total)),
        "formula": f"({A} × {avos}/12) + encargos 2.2 ({total_22})",
        "fundamento": "Anexo XII (liberação por avos); ≥ 15 dias = mês cheio",
    }


def liberacao_ferias(remuneracao: Any, avos: int, params: ContratoParams) -> Dict[str, Any]:
    A = _d(remuneracao)
    if not 0 <= avos <= 12:
        raise ValueError("avos deve estar entre 0 e 12")
    total_22 = total_submodulo_2_2(params)
    base = A * Decimal(avos) / Decimal(12)
    principal = base * (Decimal(1) + Decimal(1) / Decimal(3))  # férias + 1/3
    encargos = principal * total_22
    total = _money(principal) + _money(encargos)
    return {
        "evento": "férias",
        "avos": avos,
        "principal": str(_money(principal)),
        "encargos": str(_money(encargos)),
        "total": str(_money(total)),
        "formula": f"({A} × {avos}/12) × (1 + 1/3) + encargos 2.2 ({total_22})",
        "fundamento": "Anexo XII (férias proporcionais + 1/3 constitucional)",
    }


def multa_rescisoria(saldo_fgts: Any, modo: str = "sem_justa_causa") -> Dict[str, Any]:
    """Multa rescisória sobre o saldo do FGTS do extrato (não estimada)."""
    saldo = _d(saldo_fgts)
    tabela = CONFIG["multa_rescisoria"]
    if modo not in tabela:
        raise ValueError(f"modo de rescisão inválido: {modo!r} (use {list(tabela)})")
    perc = _d(tabela[modo])
    valor = _money(saldo * perc)
    return {
        "evento": "rescisão",
        "modo": modo,
        "saldo_fgts_extrato": str(_money(saldo)),
        "percentual": str(perc),
        "valor": str(valor),
        "formula": f"{_money(saldo)} × {perc}",
        "fundamento": "Multa do FGTS sobre o saldo do extrato (40% sem justa causa / 20% acordo)",
        "observacao": "Dispensa por justa causa NÃO gera liberação de multa.",
    }


# ---------------------------------------------------------------------------
# Execução por arquivo de input
# ---------------------------------------------------------------------------
def processar_input(data: Dict[str, Any]) -> Dict[str, Any]:
    params = ContratoParams.from_dict(data.get("contrato", {}))
    resultado: Dict[str, Any] = {"contrato": data.get("contrato", {}), "trabalhadores": []}
    for trab in data.get("trabalhadores", []):
        rem = trab["remuneracao"]
        competencias = trab.get("competencias", [trab.get("competencia", "")])
        prov = provisao_mensal(rem, params)
        bloco: Dict[str, Any] = {
            "nome": trab.get("nome"),
            "cpf": trab.get("cpf"),
            "provisao_mensal": prov,
            "competencias": competencias,
            "saldo_acumulado": saldo_acumulado([prov["total_mensal"]] * len(competencias)),
        }
        resultado["trabalhadores"].append(bloco)
    return resultado


# ---------------------------------------------------------------------------
# Self-test (golden) — valida contra a memória do dossiê
# ---------------------------------------------------------------------------
def self_test() -> int:
    falhas: List[str] = []

    # incidência 2.2 por SAT (Lucro Real/Presumido, FAP 1.0): 7,39 / 7,60 / 7,82%
    coef = _d(CONFIG["incidencia_base_coef"])
    esperado_inc = {"1": "0.073741", "2": "0.075860", "3": "0.077979"}
    for sat, esp in esperado_inc.items():
        p = ContratoParams(sat=sat)
        inc = (total_submodulo_2_2(p) * coef).quantize(Decimal("0.000001"))
        if inc != Decimal(esp):
            falhas.append(f"incidência 2.2 SAT {sat}: obtido {inc}, esperado {esp}")

    # total 2.2 por SAT
    for sat, esp in {"1": "0.348", "2": "0.358", "3": "0.368"}.items():
        got = total_submodulo_2_2(ContratoParams(sat=sat))
        if got != Decimal(esp):
            falhas.append(f"total 2.2 SAT {sat}: obtido {got}, esperado {esp}")

    # Simples Nacional → só FGTS 8%
    if total_submodulo_2_2(ContratoParams(regime="simples_nacional")) != Decimal("0.08"):
        falhas.append("Simples Nacional deveria ser 0.08")

    # provisão mensal: remuneração 1000, SAT 1, multa 4% → total ~31,82%
    prov = provisao_mensal("1000", ContratoParams(sat="1", multa_modo="atual"))
    # B=83.30 C=121.00 D=40.00 E=73.74 (1000*0.073735=73.735 -> 73.74)
    esp_rubricas = {"13º salário": "83.30", "Férias + 1/3": "121.00",
                    "Multa FGTS s/ aviso prévio": "40.00", "Incidência Submódulo 2.2": "73.74"}
    got_rubricas = {r["nome"]: r["valor"] for r in prov["rubricas"]}
    for nome, esp in esp_rubricas.items():
        if got_rubricas.get(nome) != esp:
            falhas.append(f"rubrica {nome}: obtido {got_rubricas.get(nome)}, esperado {esp}")
    if prov["total_mensal"] != "318.04":
        falhas.append(f"total mensal SAT1/4%: obtido {prov['total_mensal']}, esperado 318.04")

    # multa 5% literal → D=50.00, total 328.04
    prov5 = provisao_mensal("1000", ContratoParams(sat="1", multa_modo="literal"))
    if prov5["total_mensal"] != "328.04":
        falhas.append(f"total mensal SAT1/5%: obtido {prov5['total_mensal']}, esperado 328.04")

    # avos: ≥ 15 dias = mês cheio
    if meses_avos("2026-01-01", "2026-04-20") != 4:
        falhas.append(f"avos 01/01→20/04: obtido {meses_avos('2026-01-01', '2026-04-20')}, esperado 4")
    if meses_avos("2026-01-01", "2026-01-10") != 0:
        falhas.append("avos 01/01→10/01 deveria ser 0 (< 15 dias)")
    if meses_avos("2026-01-01", "2027-06-01") != 12:
        falhas.append("avos deveria ser limitado a 12")

    # multa rescisória 40% sobre saldo 10.000 = 4.000
    if multa_rescisoria("10000", "sem_justa_causa")["valor"] != "4000.00":
        falhas.append("multa rescisória 40% de 10.000 deveria ser 4000.00")
    if multa_rescisoria("10000", "acordo")["valor"] != "2000.00":
        falhas.append("multa rescisória 20% (acordo) de 10.000 deveria ser 2000.00")

    # saldo negativo deve falhar
    try:
        saldo_acumulado(["100.00"], ["200.00"])
        falhas.append("saldo negativo deveria levantar erro")
    except ValueError:
        pass

    if falhas:
        print("SELF-TEST: FALHOU")
        for f in falhas:
            print("  -", f)
        return 1
    print("SELF-TEST: OK (todos os golden checks do dossiê passaram)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Engine determinística da Conta Vinculada.")
    ap.add_argument("--self-test", action="store_true", help="Roda os golden tests do dossiê.")
    ap.add_argument("--provisao", action="store_true", help="Calcula a provisão mensal de um trabalhador.")
    ap.add_argument("--input", help="Arquivo JSON de input (contrato + trabalhadores).")
    ap.add_argument("--remuneracao", help="Remuneração mensal (campo A).")
    ap.add_argument("--regime", default="lucro_real_presumido")
    ap.add_argument("--sat", default="1")
    ap.add_argument("--fap", default="1.0")
    ap.add_argument("--multa", default="4", help="4 (atual) ou 5 (literal).")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    if args.input:
        data = json.loads(open(args.input, encoding="utf-8").read())
        print(json.dumps(processar_input(data), ensure_ascii=False, indent=2))
        return 0

    if args.provisao:
        if not args.remuneracao:
            ap.error("--provisao exige --remuneracao")
        params = ContratoParams(
            regime=args.regime, sat=args.sat, fap=_d(args.fap),
            multa_modo="literal" if str(args.multa) == "5" else "atual",
        )
        print(json.dumps(provisao_mensal(args.remuneracao, params), ensure_ascii=False, indent=2))
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
