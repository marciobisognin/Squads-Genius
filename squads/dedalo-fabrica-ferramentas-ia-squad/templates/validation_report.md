# Relatório de Validação — `validation_report.md`

> Template do NÓMOS (QA/segurança/LGPD) + veredito do ELENCHUS (red-team).

## Red-team (ELENCHUS)
- **Veredito:** aprovado | aprovado_com_ressalvas | **bloqueado**
- **Ataques:** `<alvo>` — `<crítica>` — severidade (baixa/media/alta/fatal)
- **Requisitos alucinados:** `<lista — sem evidência>`
- **Kill shot:** `<o argumento que derruba o plano, se houver>`
- **Correções exigidas:** `<lista>`

## Qualidade (NÓMOS)
- Checks: `<lista>`

## LGPD
- Base legal: `<...>` · Minimização: `<...>` · Anonimização/Consentimento: `<...>`

## Segurança
- Flags: `<segredos? credenciais? permissões?>` — **zero segredos expostos**

## Setor regulado
- `human_in_loop_required`: true/false (saúde/jurídico/financeiro ⇒ true)
- Disclaimer: `<alerta, não parecer jurídico>`

## Go / No-Go
- `go | conditional_go | no_go` — condições: `<...>`

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
