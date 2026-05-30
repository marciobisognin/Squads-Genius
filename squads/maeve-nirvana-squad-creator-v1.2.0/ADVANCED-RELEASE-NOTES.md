# Advanced Release Notes — v1.2.0 (Maeve)

## Novidades
- Gates automáticos por fase no comando `state advance` (padrão: `--auto-gate=true`).
- Novo comando de relatório final:
  - `report final <session> --target=... --marketplace=...`
- Geração de `FINAL-PUBLISH-REPORT.md` padronizado por sessão.

## Compatibilidade
- Node.js >= 18
- AIOS minVersion 2.1.0


## v1.3.0

- Reescrito `bin/nirvana-squad-create.cjs` com parser robusto para `--output caminho` e `--output=caminho`.
- Adicionado `--mode=scaffold|full` para alternar entre scaffold mínimo e squad completo validável.
- Adicionados `--target=aios|maeve` e `--profile=marcio|generic`.
- Novos squads com `--profile=marcio` recebem `LICENSE`, `NOTICE.md`, `AUTHORS.md`, `.ip/ownership.json` e `.ip/response-footer.md`.
- `--release` passa a bloquear manifesto vazio em modo `full`.
- `--smoke-test` executa o teste local do squad recém-gerado.
- Cada geração escreve `validation/generation-report.md`.


## v1.4.0

- Integração do Nirvana README Architect como `Architect Gate` premium no workflow de geração.
- Novo script `scripts/premium-architect-gate.cjs` para auditar e reconstruir squads abaixo do padrão premium.
- Geração `--mode=full` agora roda o gate automaticamente, salvo quando `--no-premium-gate` é informado.
- O gate valida manifesto, agentes, tasks, README, IP/licença, smoke test e score de documentação.
- O gate gera `validation/premium-architect-report.md` e a geração final registra o resultado em `validation/generation-report.md`.
- O smoke test dos squads full agora exige a presença do relatório premium.
