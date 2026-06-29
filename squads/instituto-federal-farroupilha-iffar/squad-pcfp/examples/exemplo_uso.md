# Exemplos de uso

## 1. Engine determinística — PCFP de limpeza 44h (sem LLM)

```bash
cd IFFar-Squads/squads/squad-pcfp
python3 scripts/pcfp_core.py --input examples/exemplo_input_limpeza44h.json --saida /tmp/costsheet.json
```

Saída: CostSheet com ~22 rubricas (módulos 1–6), cada uma com valor, fórmula, fundamento e flags `renovavel`/`conta_vinculada`, mais totais por módulo e preço por posto. Valores do exemplo são fictícios.

## 2. Checklist de conformidade (sem LLM)

```bash
python3 scripts/validar_pcfp.py --costsheet /tmp/costsheet.json
```

Saída: ComplianceReport verde/amarelo/vermelho com findings fundamentados (reserva técnica → TCU 1442/2010; conta vinculada → Anexo XII; não renováveis → IN 07/2018; faixas de CI/lucro).

## 3. Diff de proposta de licitante (sem LLM)

```bash
python3 scripts/diff_proposta.py --referencia /tmp/costsheet.json --proposta proposta_normalizada.json
```

Saída: diff célula a célula com classificação por limiar (padrão: amarelo ≥ 10%, vermelho ≥ 25%) e comparação do total por posto.

## 4. Fluxo completo com a equipe de agentes (com LLM)

Em uma sessão do Claude Code (ou runtime AIOS compatível):

1. Leia `squad.yaml` e assuma a persona `agents/a1-orquestrador-maestro.md`.
2. Descreva a demanda ("elaborar PCFP para...", "analisar esta proposta...", "repactuar o contrato...") e anexe TR/ETP/proposta/CCT.
3. O A2 extrai o ServiceProfile e pergunta o que faltar; o A4 apresenta o enquadramento sindical para sua **aprovação (HITL Gate 1)**.
4. Informe as decisões humanas: custos indiretos, lucro, regime tributário (a engine não tem default silencioso).
5. A engine calcula, o A6 audita (loop de correção se vermelho) e o A8 gera planilha, relatório e checklist assinável para sua **aprovação final (HITL Gate 2)**.

## 5. Repactuação

Use o workflow `repactuacao_reajuste` entregando o contrato vigente, a CostSheet original e a nova CCT — o A7 produz o diff analítico rubrica a rubrica com alerta de preclusão antes de qualquer minuta.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
