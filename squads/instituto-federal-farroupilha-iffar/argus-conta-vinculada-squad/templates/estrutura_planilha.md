# Estrutura da planilha de Conta Vinculada (5 abas)

Gabarito de saída do gerador (`scripts/gerar_planilha_xlsx.py`), alinhado ao dossiê e
aos modelos de IFs (IFSul/UnB).

## Aba 1 — Cadastro/Contrato
órgão · nº do contrato · empresa · CNPJ · **regime tributário** (define o Submódulo 2.2) ·
**SAT/RAT (1/2/3%) e FAP** · banco · agência · conta-vinculada · vigência ·
índice de remuneração (poupança pro rata die).

## Aba 2 — Trabalhadores
nome · CPF · função/cargo (CBO) · data de admissão · data de início no contrato ·
salário-base · adicionais (insalubridade/periculosidade/noturno) · **remuneração total (A)** ·
jornada (40h pós-Decreto 12.174/2024 ou 44h) · benefícios.

## Aba 3 — Provisão mensal (por competência e trabalhador)
competência (MM/AAAA) · Remuneração (A) · **13º (B = A×8,33%)** · **Férias+1/3 (C = A×12,10%)** ·
**Multa FGTS s/ aviso (D = A×4% ou 5%)** · **Incidência 2.2 (E = (total_2.2×21,19%)×A)** ·
Total mensal a depositar (B+C+D+E) · saldo acumulado.

## Aba 4 — Liberações
evento (13º / férias / rescisão / encerramento) · data · trabalhador · avos ·
principal da rubrica · encargos correspondentes · documento comprobatório ·
autorização · ordem bancária · saldo após a liberação.

## Aba 5 — Conferência FGTS/INSS
competência · FGTS devido (8% da remuneração) · FGTS recolhido (extrato/FGTS Digital) ·
divergência · status (regular/irregular) · INSS recolhido (GPS/DARF).

> Cada célula calculada acompanha a memória de cálculo (fórmula + percentual + fundamento legal).

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
