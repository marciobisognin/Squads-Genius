# Manual de operação — SCRIBA Contratos Squad

## O que o squad faz
Dado um **tipo de situação contratual** (prorrogação, acréscimo/supressão, reajuste
por índice, repactuação com demonstração analítica, etc.), produz o **instrumento
pronto para assinatura** (minuta inicial · termo aditivo · apostilamento ·
repactuação/reajuste) + memória explicativa, com motor determinístico, citação
obrigatória por cláusula e HITL nos pontos jurídicos críticos.

## Princípio reitor (anti-alucinação)
Todo valor monetário ou decisão de instrumento vem da **engine/router determinísticos
em Python**, nunca do LLM. O LLM extrai, redige e explica; **o número e a decisão de
instrumento são código**.

## Pipeline (workflow `scriba_full_pipeline`)
```
[Input] → Cynefin Classifier → Extractor → Normative RAG
   → Instrument Router → Template Selector [HITL Gate A]
   → Calculator (engine determinística) → Drafter → Validator
        ├─ BLOQUEIO → (Turing loop) → Calculator/Drafter
        └─ OK → [HITL Gate B] → Doc Generator + Explainer → [Output]
```

## Uso rápido (execução determinística, sem LLM)
A partir de `squads/scriba-contratos-squad/`:

```bash
# 1) Rodar a suíte de casos-ouro
python3 tests/test_golden_cases.py

# 2) Pipeline determinístico ponta a ponta (router + engine + validador)
python3 scripts/run_scriba.py --input examples/sample_input_reajuste.json --outdir output
python3 scripts/run_scriba.py --input examples/sample_input_aditivo.json --outdir output
python3 scripts/run_scriba.py --input examples/sample_input_repactuacao.json --outdir output

# 3) Inspecionar o router isoladamente
python3 scripts/scriba_router.py

# 4) Inspecionar a engine isoladamente
python3 scripts/scriba_engine.py
```

## Entrada (estrutura JSON)
Ver `examples/sample_input_*.json`. Campos principais: `contract_facts` (flags
booleanas da situação ativa), e blocos específicos por situação: `reajuste`,
`aditivo`, `repactuacao`, `conta_vinculada`, `prorrogacao`.

## Saídas
- `instrument_decision.json` — instrumento decidido + rationale + legal_refs.
- `calc_results.json` — resultados numéricos da engine, rastreáveis por fórmula/fundamento.
- `relatorio_validacao.json` + `.md` — checagens OK/ALERTA/BLOQUEIO.
- `contrato.docx` / `termo_aditivo.docx` / `apostilamento.docx` — instrumento final (futuro).
- `memoria.md` — memória explicativa (futuro, agente Explainer).

## Gates humanos (invariantes)
1. **HITL Gate A** — confirmação do instrumento decidido e, em repactuação DEMO,
   da classificação de CCT.
2. **HITL Gate B** — homologação humana final da peça redigida, antes da geração
   do pacote definitivo.

## Alerta crítico
**Preclusão de repactuação** (art. 57, §7º da IN 05/2017) — a engine emite alerta
quando a solicitação se aproxima do fim da vigência contratual sem repactuação
exercida.
