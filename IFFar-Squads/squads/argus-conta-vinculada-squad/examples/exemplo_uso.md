# Exemplo de uso — Árgus Conta Vinculada

Contrato fictício de limpeza (IFFar, jornada 40h, Lucro Real/Presumido, SAT 1, multa 4%).

## 1. Provisão mensal (engine determinística)

```bash
python3 scripts/conta_vinculada_core.py --input examples/exemplo_contrato_limpeza.json
```

Saída (resumo): para remuneração R$ 1.620,00 → total mensal a depositar **R$ 515,23**
(≈ 31,80%), decomposto em 13º (R$ 134,95), férias+1/3 (R$ 196,02), multa 4% (R$ 64,80)
e incidência do Submódulo 2.2 (R$ 119,46). Cada rubrica vem com fórmula e fundamento.

Cálculo avulso (sem arquivo):

```bash
python3 scripts/conta_vinculada_core.py --provisao --remuneracao 1620 --regime lucro_real_presumido --sat 1 --multa 4
```

Trocar para Simples Nacional (incidência 2.2 cai para só FGTS 8%) ou multa literal 5%:

```bash
python3 scripts/conta_vinculada_core.py --provisao --remuneracao 1620 --regime simples_nacional --multa 4
python3 scripts/conta_vinculada_core.py --provisao --remuneracao 1620 --sat 2 --multa 5
```

## 2. Conferência e regras de liberação (fail-closed)

```bash
python3 scripts/validar_conta_vinculada.py --input examples/exemplo_conferencia.json
```

Bloqueia a liberação quando: CPF inválido, FGTS recolhido < devido (8%), justa causa,
rescisão > 1 ano sem homologação sindical, documentação incompleta ou saldo insuficiente.

## 3. Geração da planilha .xlsx

```bash
python3 scripts/conta_vinculada_core.py --input examples/exemplo_contrato_limpeza.json > /tmp/consolidado.json
python3 scripts/gerar_planilha_xlsx.py --input /tmp/consolidado.json --output examples/exemplo_planilha_conta_vinculada.xlsx --csv
```

Gera `exemplo_planilha_conta_vinculada.xlsx` com as 5 abas (Cadastro, Trabalhadores,
Provisão mensal, Liberações, Conferência FGTS). O `--csv` adiciona um fallback por aba.

## 4. Testes

```bash
python3 scripts/conta_vinculada_core.py --self-test
python3 scripts/validar_conta_vinculada.py --self-test
python3 scripts/gerar_planilha_xlsx.py --self-test
```

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
