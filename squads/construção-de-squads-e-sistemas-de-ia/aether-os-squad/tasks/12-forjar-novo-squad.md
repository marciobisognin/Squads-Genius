# Task 12 — Forjar Novo Squad (capability_gap)

**Executor:** HÉPHAISTOS (mente) + forge_bridge (motor) + ELENCHUS (revisão)
**Fase:** Forja dinâmica (PRD §20)

## Objetivo
Quando o Motor de Seleção emite `capability_gap`, criar sob governança um novo
squad candidato capaz de executar a tarefa órfã — nunca improvisar uma seleção
inadequada.

## Entradas
- `aether.selection-decision/v1` com `capability_gap: true` + tarefa órfã +
  domínio e restrições.

## Saídas
- `capability-spec.md`, `briefing_<nome>.yaml` (schema do briefing_parser do
  Maeve Genius Forge), scaffold de squad candidato em workspace isolado,
  `validation-report.json`, `adversarial-review.json`, `promotion-request.json`.

## Passos
1. HÉPHAISTOS especifica a capacidade faltante (contratos, permissões, riscos).
2. `python3 scripts/forge_bridge.py --gap <gap.json> --workspace <dir>` gera
   briefing + scaffold mínimo validável (squad.yaml, agents/, tasks/,
   workflows/, scripts/, examples/, docs/, LICENSE, NOTICE.md, AUTHORS.md).
3. Quando o construtor oficial (Maeve Genius Forge) estiver disponível,
   delegar a construção completa a ele.
4. Validar: `validate_squad.py --root <candidato>` até `go`.
5. ELENCHUS revisa o candidato (escalonamento de capacidade, permissões
   excessivas, injeção embutida).
6. Registrar como `experimental`; promoção a `trusted` exige telemetria de uso
   e aprovação conforme política. Publicação é efeito de alto risco.

## Critérios de aceite
- Scaffold candidato passa em validação estrutural (`go`).
- Revisão adversarial persistida antes de qualquer promoção.
- Nada foi escrito no repositório produtivo sem gate.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
