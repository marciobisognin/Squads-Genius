# scriba-calculator

## Missão
Engine determinística (**Python puro, sem LLM**). Implementa os cálculos do
PRD §7: reajuste por índice, limites de aditivo (25%/50%), repactuação por
componente (com alerta de preclusão) e provisão de conta vinculada/PFG. É o
coração anti-alucinação do squad — **nenhum valor monetário sai da geração
livre do LLM.**

## Implementação
- Código: `scripts/scriba_engine.py`.
- `calcular_reajuste` — fator = índice_final/índice_inicial sobre `valor_base`.
- `avaliar_limites_aditivo` — 25% (acréscimo/supressão comum) e 50%
  (reforma de edifício/equipamento), **vedada a compensação entre os dois
  limites** (art. 125, §1º).
- `avaliar_repactuacao` — anualidade por componente a partir da
  `data_base_anterior`; alerta de **preclusão** quando a solicitação ultrapassa
  `dias_alerta_preclusao` antes do fim da vigência (art. 57, §7º da IN 05/2017).
- `calcular_provisao_mensal` — conta vinculada × PFG sobre `salario_base`.
- `avaliar_prorrogacao` — teto de 60 meses (`meses_ja_executados +
  meses_prorrogacao`).

## Saída
Estrutura numérica por cálculo; cada resultado carrega `{valor, formula,
fundamento, flags}` — rastreável célula a célula.

## Testes obrigatórios
Suíte de casos-ouro em `tests/test_golden_cases.py` (reajuste por IPCA,
aditivo com acréscimo dentro do limite, repactuação com alerta de preclusão).
Rodar com `python3 tests/test_golden_cases.py`.

## Regras obrigatórias
- Nenhum valor monetário é produzido por LLM.
- Determinismo: mesma entrada → mesma saída.
- Toda saída é rastreável (valor + fórmula + fundamento).
- Footer obrigatório na entrega documental.

## Comandos
- `*help` · `*run` · `*review` · `*exit`
