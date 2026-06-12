# Exemplos de uso

## 1. Pré-triagem determinística de cláusulas (sem LLM)

```bash
cd squads/themis-contratos-publicos-squad
python3 scripts/checklist_clausulas.py --contrato examples/exemplo_contrato_trecho.txt
```

Saída: relatório JSON com indício de presença/ausência de cada cláusula necessária. O contrato de exemplo deve acusar `nao_localizada` para garantia, matriz de riscos, casos omissos, PNCP, anticorrupção e LGPD — insumos para a análise semântica do agente.

## 2. Validação de limites de termo aditivo (sem LLM)

```bash
# contrato de R$ 480.000 com dois aditivos (R$ 90.000 e R$ 40.000) = 27,08% > 25%
python3 scripts/validar_limites_aditivos.py --valor-inicial 480000 --aditivos 90000 40000 --regime 14133
```

## 3. Análise completa com a equipe de agentes (com LLM)

Em uma sessão do Claude Code (ou runtime AIOS compatível):

1. Leia `squad.yaml` e assuma a persona `agents/themis-orchestrator.md`.
2. Execute o workflow `workflows/analise_completa_contrato.yaml`, fornecendo os documentos do processo.
3. Aprove (ou reprove) cada quality gate quando solicitado.
4. Receba o parecer no formato `templates/parecer_juridico.md` e faça a revisão humana obrigatória.

## 4. Triagem rápida de red flags

Use o workflow `workflows/triagem_rapida_red_flags.yaml` para priorizar uma carteira de contratos antes de decidir quais merecem análise completa.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
