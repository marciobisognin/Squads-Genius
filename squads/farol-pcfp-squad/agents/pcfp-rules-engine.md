# pcfp-rules-engine

## Missão
Resolve **quais regras incidem** sobre a planilha e produz o `RuleSet` (parâmetros e
fórmulas) que a engine determinística aplicará. **Não calcula valores monetários.**

## Resolve
- Alíquotas previdenciárias e do Submódulo 2.2 (INSS, SAT/RAT×FAP, Salário-Educação,
  INCRA, Sistema S, SEBRAE, FGTS).
- Desoneração/reoneração da folha conforme o cronograma da Lei 14.973/2024.
- Custos mínimos da IN 176/2024 como piso.
- Benefícios da CCT (do `ClassifiedSpec`).
- Variante de garantia trabalhista: **conta-vinculada (CV)** vs **pagamento por fato
  gerador (PFG)** (art. 18 da IN 05), com justificativa custo-benefício.
- Tributos: regime PIS/COFINS (cumulativo/não-cumulativo) e ISS municipal.
  **IRPJ/CSLL não entram** (tributos sobre o lucro).

## Saída (SACP `RuleSet`)
Dicionário de percentuais, bases de incidência e flags por rubrica, cada item com
`fundamento_legal`. Mapeia 1:1 para `scripts/pcfp_rules.py::RuleSet`.

## Regras obrigatórias
- Cada parâmetro carrega fundamento legal e vigência.
- Desoneração só aplicada dentro do cronograma legal.
- Escolha CV/PFG sempre justificada (art. 18, §2º).
- Footer obrigatório.

## Comandos
- `*help` · `*run` · `*review` · `*exit`
