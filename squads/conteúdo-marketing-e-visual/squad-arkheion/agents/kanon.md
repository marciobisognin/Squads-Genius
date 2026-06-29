# KÁNŌN — A Régua

> Étimo: κανών (*kanṓn*), "régua/cânone". · Tier: **Python, não-LLM** · Guilda de Validação · **Gate bloqueante** · Implementação: `scripts/kanon.py`

## Missão
Guardião de fidelidade. Validar **numericamente** cada spec e render contra `arkheion/canon.py`: hex exatos, fonte permitida, geometria com tolerância, timing na faixa, cadeia de grade e duração da cena. Divergência → **reprovação bloqueante** com motivo auditável.

## Entrada — `CardInterface` | `FootageSpec` | `PlanoSequencial` | cadeia de grade | `Cena10`
## Saída — veredito (JSON)
```json
{ "alvo": "card:...", "aprovado": false,
  "motivos": ["título deve ser CAIXA ALTA: 'o problema'"],
  "canone_versao": "1.0.0" }
```

## O que valida (determinístico)
- **Hex** ∈ `PALETA_CINE ∪ PALETA_UI`; **fonte** ∈ `FONTES_PERMITIDAS`.
- **Título:** CAIXA ALTA, ≤4 palavras, ≤28 chars.
- **Contador:** padrão `NN / TT` e `TT` == nº de cenas resolvido.
- **Plano sequencial:** contador e função de cada beat coerentes com o tamanho; `prova_visual` exige `dataviz`.
- **Grade FFmpeg:** contraste 1.30–1.50, saturação 0.10–0.12, granulação 16–20, vinheta presente.
- **Footage:** plano/movimento válidos, prompt sem estética proibida, duração == 10s.
- **Proibidos:** neon, saturado, 3D, holograma, tiktok, dourado, gamer, branco digital puro.

## Comandos
- `*help` · `*validate <artefato.json>` · `*grade <cadeia>` · `*exit`

## Critério
- Falso-positivo zero no exemplo canônico; **qualquer** artefato sintético fora do padrão deve falhar (ver `tests/test_kanon_rejection.py`).

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
