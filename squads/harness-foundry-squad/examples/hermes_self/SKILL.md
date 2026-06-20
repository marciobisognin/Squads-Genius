# Harness Foundry Squad (skill Hermes)

Harness gerado pelo Harness Foundry Squad a partir de `.`.

## Instalação

```bash
cp -r harness-foundry-squad ~/.hermes/skills/harness-foundry-squad
```

## Comandos disponíveis

- `01_intake_harness_request` (owner: `harness-intake-orchestrator`) — inputs: ['squad_path', 'target_hosts', 'exposure_level'], outputs: ['intake_summary', 'gaps']
- `02_score_squad_fit` (owner: `harness-fit-analyst`) — inputs: ['squad_path'], outputs: ['fit_report']
- `03_build_harnessspec_adapter` (owner: `squad-to-harnessspec-adapter`) — inputs: ['squad_path', 'fit_report'], outputs: ['harnessspec_json', 'gaps']
- `04_generate_hermes_package` (owner: `hermes-package-builder`) — inputs: ['harnessspec_json', 'target_hosts'], outputs: ['cli_config_yaml', 'optional_mcp_json', 'skill_md']
- `05_audit_security_policy` (owner: `security-policy-auditor`) — inputs: ['hermes_package_dir', 'harnessspec_json'], outputs: ['security_audit_report']
- `06_run_harness_doctor` (owner: `harness-doctor-curator`) — inputs: ['hermes_package_dir', 'security_audit_report', 'fit_report'], outputs: ['doctor_report']

## Policy

Default-deny. Exceções: nenhuma.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
