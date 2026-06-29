# TURING — A Guilda do Self-Healing

> Homenagem: Alan Turing. · Tier: **Python, não-LLM** · Guilda Turing · envolve todos os nós

## Missão
Self-healing do pipeline: retry com backoff em APIs, reparo de JSON malformado, regeneração de **cena isolada** (sem refazer o vídeo) e escalonamento a HITL após N falhas. Mantém o pipeline resiliente sem comprometer o determinismo.

## Entrada — evento de falha (nó, tipo, payload)
## Saída — decisão de roteamento (JSON)
```json
{ "acao": "retry", "alvo": "tekton", "cena_idx": 4, "tentativa": 2,
  "backoff_s": 4, "escalar_hitl": false }
```

## Política de roteamento de falha (PRD §9)
- **Malformação JSON** → repair + retry (máx 2).
- **Erro de API (vídeo/TTS)** → backoff exponencial (máx 3: 2s, 4s, 8s).
- **Reprovação KÁNŌN persistente (≥2)** → escala a HITL com diagnóstico.
- Circuit breaker por cena: regenerar a CENA-N nunca reprocessa as demais.

## Regras
- Determinístico e idempotente; toda decisão é logada (Langfuse) para auditoria.

## Comandos
- `*help` · `*heal <evento>` · `*status` · `*exit`

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
