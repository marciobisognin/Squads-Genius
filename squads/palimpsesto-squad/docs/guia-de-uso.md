# Guia de uso — PALIMPSESTO Squad

## Como ativar manualmente

1. Leia `squad.yaml` e assuma a persona de `agents/triador.md`.
2. Envie o objeto de conhecimento histórico-cultural (texto, evento, personalidade, conceito ou lugar) que deseja reconstruir.
3. O Triador classifica e emite `SACP-IN`.
4. Assuma, em sequência, as personas das trilhas ativadas em `SACP-IN.tracks` (`agents/chronos.md`, `agents/terra.md`, etc.) — podem ser executadas em qualquer ordem, pois rodam em paralelo conceitualmente.
5. Assuma `agents/agon.md` para revisar os claims e abrir `tensions[]`.
6. Assuma `agents/elenchus.md` para auditar todos os claims (Camada 1 + ÁGON) e emitir `VerifiedClaim[]`.
7. Se `SACP-IN.sensitivity_flag` não for nulo, pause para revisão humana (ver `tasks/05-hitl-gate-sensibilidade.md`) antes de continuar.
8. Assuma `agents/tecelao.md` para montar o `Dossier`.
9. Assuma `agents/aedo.md` para narrar, seguida de `agents/ponte.md` para fechar.
10. Entregue a resposta seguindo a estrutura de `templates/formato-entrega.md`.

## Como validar os contratos

```bash
cd squads/palimpsesto-squad
python3 scripts/validate_contracts.py
```

Valida os exemplos de `examples/fixtures/` contra os schemas de `templates/`.

## Referências

- PRD original completo: `references/PRD_PALIMPSESTO.md`.
- Exemplo trabalhado (Mt 5,5): `examples/exemplo-mt-5-5.md`.
