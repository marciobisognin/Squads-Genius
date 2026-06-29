# Policy default-deny do Harness Foundry Squad

Todo harness gerado por este squad nasce com a policy mais restritiva possível. Qualquer permissão adicional precisa ser pedida explicitamente e registrada.

## Regras base

1. Nenhum comando de shell irrestrito (`shell: "*"`) é gerado por padrão.
2. Acesso a filesystem é restrito ao diretório do próprio harness e a uma pasta `output/` explícita.
3. Acesso à rede só é declarado quando o squad de origem já depende de uma API externa (ex.: Compras.gov.br) — e mesmo assim, com domínio específico, nunca wildcard.
4. Nenhuma credencial é gerada, sugerida ou armazenada em qualquer arquivo do harness.
5. Exceções à policy exigem: motivo, agente responsável e confirmação humana registrada em `security_audit.json`.

## Verificação automática

```bash
python3 scripts/harness_doctor.py --hermes-dir output/<squad>/hermes
```

Um harness com `status: BLOCKED` nunca deve ser instalado ou publicado.
