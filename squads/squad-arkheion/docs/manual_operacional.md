# Manual operacional — ARKHEION

## Pré-requisitos
- Python 3.11+ (núcleo e scripts rodam só com a stdlib).
- Opcional para produção real: `pip install -r requirements.txt` + FFmpeg + Playwright
  (e uma API de text-to-video configurada por variável de ambiente — nunca commitada).

## Fluxo rápido (CLI determinística, sem LLM)

```bash
# 1) Resolver tamanho -> nº de cenas/contadores/funções
python3 arkheion/canon.py

# 2) Montar o andaime do plano a partir do tema + tamanho
python3 scripts/plano_builder.py --tema "infraestrutura de IA" --tamanho 60 \
  --marca "NOUS LAB" --protocolo "ARK-TEC-001"

# 3) Validar specs contra o Cânone (KÁNŌN — gate bloqueante)
python3 scripts/kanon.py --plano examples/plano_sequencial_tecnologia.json --tamanho 60
python3 scripts/kanon.py --card examples/card_interface_tecnologia.json
python3 scripts/kanon.py --footage examples/footage_spec_tecnologia.json

# 4) Plano de animação do HUD (Trilho A)
python3 scripts/hud_plan.py --texto "ACESSO RESTRITO|3 NÍVEIS" --beat 2

# 5) Cadeia de grade FFmpeg canônica (Trilho B)
python3 scripts/grade.py --in footage.mp4 --out cena01_graded.mp4

# 6) Plano de montagem do master (SÝNTHESIS)
python3 scripts/synthesis_plan.py --n 6 --encerramento escuro
```

## Fluxo completo (com agentes LLM)
1. **S0 Intake** — informe tema + tamanho (30/60/90) + marca/protocolo/CTA/encerramento.
2. **Gate 1 (Triagem):** confirme domínio Cynefin e injete ativos (b-roll/logos).
3. **Gate 2 (Roteiro):** aprove/edite os títulos e textos digitados — *antes* de gastar render.
4. Geração paralela de specs → KÁNŌN → render CENA-10 → KÁNŌN por cena → SÝNTHESIS.
5. **Gate 3 (Homologação):** aprove o master ou peça regeneração de cena(s).

## Testes
```bash
python3 -m unittest tests.test_canon tests.test_kanon_rejection -v
```

## Regras de ouro
- O LLM só emite JSON. Cor/fonte/geometria/timing/grade vêm do Cânone — não edite no prompt.
- Nunca commite `.env`, tokens ou chaves. Logos de terceiros só com autorização do usuário.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
