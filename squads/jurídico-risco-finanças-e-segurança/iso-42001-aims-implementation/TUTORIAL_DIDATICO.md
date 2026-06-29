# Tutorial didático — Como usar o ISO 42001 AIMS Implementation Squad

## 1. Ideia em linguagem simples

Imagine que um grande cliente pergunta:

> “Sua empresa usa IA. Mostre onde usa, quais riscos existem, quem é responsável e quais evidências provam controle.”

Este squad ajuda a responder sem improviso.

Ele não “dá certificação”. Ele organiza a casa para que a empresa tenha inventário, riscos, controles, políticas, evidências e um caminho realista para uma auditoria.

## 2. Escolha o modo de trabalho

### Modo A — Gap analysis only
Use quando você quer um diagnóstico rápido.

- Duração típica: 2–4 semanas.
- Entrega: lacunas, riscos e roadmap.
- Melhor para: diretoria, comercial, RFP, primeiro diagnóstico.

### Modo B — Audit readiness sprint
Use quando a empresa já tem materiais, mas precisa organizar evidências.

- Duração típica: 4–6 semanas.
- Entrega: índice de evidências, SoA, auditoria interna simulada.
- Melhor para: preparação antes de auditoria ou cliente exigente.

### Modo C — Full implementation
Use quando a empresa quer implantar o SGIA/AIMS completo.

- Duração típica: 9–12 meses.
- Entrega: sistema de gestão operando com melhoria contínua.
- Melhor para: empresas que pretendem buscar certificação formal.

## 3. Preencha um arquivo de entrada

Use o exemplo:

`examples/saas_b2b_5_llm_products.json`

Ele contém:

- nome da organização;
- contexto comercial;
- sistemas/produtos de IA;
- área responsável;
- dados tratados;
- fornecedor;
- criticidade.

## 4. Rode o gerador

No Termux ou Linux:

```bash
cd ~/squad-factory/workspaces/iso-42001-aims-implementation
python scripts/generate_aims_pack.py --input examples/saas_b2b_5_llm_products.json --output generated/demo --mode gap_analysis_only
```

## 5. Leia os arquivos gerados nesta ordem

1. `00_EXECUTIVE_SUMMARY.md` — visão executiva.
2. `01_AI_INVENTORY.md` — onde a IA é usada.
3. `02_GAP_ANALYSIS.md` — lacunas contra governança esperada.
4. `03_RISK_REGISTER.md` — riscos e controles mínimos.
5. `04_AIIA.md` — avaliação de impacto.
6. `05_SOA.md` — declaração de aplicabilidade.
7. `06_EVIDENCE_INDEX.md` — evidências que precisam existir.
8. `07_ROADMAP.md` — plano 30/60/90 dias e 9–12 meses.
9. `08_CERTIFICATION_READINESS.md` — checagem final de prontidão.

## 6. Como usar em uma empresa real

Peça para cada área responder:

- Onde usamos IA?
- Quais dados entram?
- A IA decide ou apenas sugere?
- Existe revisão humana?
- Quem é o dono do processo?
- Há logs ou evidências?
- O fornecedor é conhecido e avaliado?
- Se o cliente pedir prova amanhã, o que entregamos?

## 7. Como invocar end-to-end

Exemplo de comando conceitual:

```text
Skill("harness", "Gap analysis ISO/IEC 42001 + roadmap SGIA para SaaS B2B com 5 LLM-based products")
```

Roteamento esperado:

- harness BM25
- compliance-citadel
- cc-cco
- cc-ai-governance-head
- iso-42001-aims-implementation
- cross-squads LGPD, segurança e jurídico

## 8. Cuidados importantes

- Não dizer que a empresa é certificada se não houve auditoria formal.
- Não esconder riscos éticos, legais ou operacionais.
- Não tratar ISO 42001 como “documento bonito”; é sistema de gestão.
- Não usar IA crítica sem dono, logs, política, revisão e evidência.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
