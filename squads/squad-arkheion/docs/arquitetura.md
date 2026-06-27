# Arquitetura — ARKHEION

> Cânone: **A imagem é a prova. O LLM descreve; o código desenha; o silêncio acusa.**

## Visão de alto nível (dual-render em vídeo, herdado de KÊRYX)

```
BRIEFING (tema, marca, CTA, tamanho) ─► HÉGEMŌN (StateGraph)
   │
   ├─ S1 DIAÍRESIS (Cynefin) ── GATE 1 (HITL)
   ├─ S2 MŶTHOS → PlanoSequencial (N beats) ── GATE 2 (HITL: aprova roteiro)
   ├─ fan-out:  S3 SKIÁGRAPHOS ×N (FootageSpec) ∥ S4 TÝPOS ×N (CardInterface) ∥ S5 PHŌNĒ (AudioSpec)
   ├─ S6 KÁNŌN (valida specs) ──(reprova → agente)
   ├─ S7 TÉKTŌN ×N (render CENA-10) ──(falha → TURING)
   ├─ S8 KÁNŌN (valida cenas) ──(reprova → regenera só a cena)
   ├─ S9 SÝNTHESIS (master 2160 + entrega 1080)
   ├─ S10 ELENCHUS (tom) ∥ KÁNŌN (técnica)
   └─ S11 GATE 3 (HITL: homologação) → ENTREGA + Langfuse
```

TURING envolve todos os nós (retry, repair de JSON, backoff, escalonamento a HITL).

## Separação determinístico × probabilístico (invariante TCU)

| Nó | Tipo | Saída |
|---|---|---|
| DIAÍRESIS, MŶTHOS, SKIÁGRAPHOS, TÝPOS, PHŌNĒ, ELENCHUS | LLM | **apenas JSON** |
| KÁNŌN, TÉKTŌN, SÝNTHESIS, TURING, HÉGEMŌN | **Python** | validação/render/montagem/orquestração |

Tudo que define a identidade da marca (cor, geometria, fonte, timing, grão) roda em
código (`arkheion/canon.py`). O LLM nunca desenha — só descreve em JSON o que desenhar.

## A unidade atômica — CENA-10

Cada CENA-10 = Trilho B (footage gradeado) + Trilho A (HUD com alfa) + áudio, em 10s
exatos. Vantagens: paralelizável, regenerável (reprovar a cena 4 não refaz o vídeo),
auditável (KÁNŌN valida cena a cena com checksum).

## Tamanho do vídeo (extensão sobre o PRD)

O usuário informa o **tamanho**; `canon.resolver_duracao()` o converte em nº de
CENA-10, contadores `NN / TT` e a sequência de funções narrativas:

| Tamanho | Cenas | Funções (resumo) |
|---|---|---|
| 30s | 3 | tensão → método → CTA |
| 60s | 6 | tensão → restrição → método → processo → prova → CTA (canônico) |
| 90s | 9 | + processo/prova extras no miolo |

Toda sequência preserva abertura (tensão) e fechamento (CTA), e o beat de prova carrega
`dataviz` obrigatório.

## Contratos SACP

`arkheion/schemas.py` define `Briefing`, `Classificacao`, `Beat`, `PlanoSequencial`,
`FootageSpec`, `CardInterface`, `AudioSpec`, `Cena10`, `DossieMaster`. Usa Pydantic v2
quando disponível; caso contrário degrada para dataclasses com validação equivalente.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
