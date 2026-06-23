# pcfp-calculator

## Missão
Engine determinística (**Python puro, sem LLM**). Implementa os Módulos 1–6 e os
quadros-resumo com a **ordem de incidência correta**. É o coração anti-alucinação do squad.

## Implementação
- Código: `scripts/pcfp_engine.py` (+ `scripts/pcfp_rules.py`).
- Ordem de incidência (a engine erra se inverter):
  - Submódulo 2.2 incide sobre **Módulo 1 + Submódulo 2.1** (IN 07/2018).
  - A provisão de rescisão (Módulo 3) recebe a incidência do Submódulo 2.2.
  - Vale-transporte por **custo efetivo** (descontados até 6% do salário) — sem piso arbitrário.
  - Tributos do Módulo 6 por **gross-up** sobre o faturamento; **sem IRPJ/CSLL**.

## Saída
Estrutura numérica completa por posto + global; cada célula carrega
`{valor, formula, fundamento, flags}`.

## Testes obrigatórios
Suíte de casos-ouro em `tests/test_golden_cases.py` (limpeza diurno 44h, vigilância
12×36 noturno, apoio administrativo) — verifica invariantes de incidência, vedações,
custo efetivo do VT e gross-up. Rodar com `python3 tests/test_golden_cases.py`.

## Regras obrigatórias
- Nenhum valor monetário é produzido por LLM.
- Toda rubrica é rastreável (valor + fórmula + fundamento).
- Determinismo: mesma entrada → mesma saída.
- Footer obrigatório na entrega documental.

## Comandos
- `*help` · `*run` · `*review` · `*exit`
