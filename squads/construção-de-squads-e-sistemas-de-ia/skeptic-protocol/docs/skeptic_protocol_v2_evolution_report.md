# Relatório de evolução — SKEPTIC Protocol v2.0

## Escopo executado

O SKEPTIC Protocol foi evoluído de um protocolo de testes adversariais de software para uma plataforma defensiva de red teaming de agentes e squads multiagentes.

A implementação permite testar qualquer squad por caminho e exportar resultados em JSON, Markdown e HTML, com biblioteca de ataques canários, cenários reproduzíveis, severidade, probabilidade, impacto, evidências, recomendações, regressão de segurança e CI.

## Componentes adicionados

- `scripts/skeptic_agent_redteam.py` — runner determinístico de red teaming de squads por caminho.
- `data/agent_redteam_attack_library.json` — biblioteca de 16 cenários canários cobrindo as 14 classes solicitadas.
- `tests/test_skeptic_agent_redteam.py` — testes automatizados do runner, biblioteca, exports, cenários e regressão.
- `tests/test_security_regression_self.py` — regressão de segurança gerada para o próprio SKEPTIC.
- `docs/agent-red-team-platform.md` — documentação técnica da plataforma.
- `tasks/run-agent-red-team.md` — task AIOS/OpenSquad para execução do red team.
- `workflows/agent-squad-red-team-platform.yaml` — workflow com gates, timeouts, retries e falhas.
- `.github/workflows/skeptic-agent-redteam.yml` — integração CI.

## Componentes atualizados

- `README.md` — agora descreve funcionalidades efetivamente implementadas.
- `squad.yaml` — versão 2.0.0, novas capacidades, scripts, data, docs e workflow.
- `agents/red-teamer.md` — papel expandido para red teaming de agentes e multiagentes.
- `agents/skeptic-orchestrator.md` — veredito com evidência, go/no-go e integridade de ações.

## Vulnerabilidades cobertas

- Prompt injection direta.
- Prompt injection indireta em documentos.
- Prompt injection indireta em páginas web.
- Prompt injection indireta em e-mails, resultados de busca e ferramentas MCP.
- Exfiltração de contexto, memória, credenciais, instruções internas e dados de outro usuário.
- Escalada de privilégio.
- Uso de ferramenta não autorizada.
- Confused deputy.
- Alucinação de ações executadas.
- Citações inexistentes ou incompatíveis.
- Loop infinito entre agentes.
- Amplificação de erro entre agentes.
- Aprovação humana simulada ou ignorada.
- Consumo excessivo de tokens e ferramentas.
- Persistência indevida de dados.
- Manipulação do agente avaliador.

## Evidências de validação

Comandos executados:

```bash
python -m py_compile scripts/skeptic_agent_redteam.py
python -m pytest -q
python scripts/skeptic_agent_redteam.py --squad . --output redteam-output/self --formats json,markdown,html --write-scenarios --fail-on vulnerable
python scripts/skeptic_agent_redteam.py --squad ../maeve-genius-forge-squad --output redteam-output/maeve-genius-forge --formats json,markdown,html --write-scenarios --fail-on none
```

Resultados observados:

- `python -m pytest -q`: `5 passed`.
- Scan do próprio SKEPTIC: `total_attacks: 16`, `pass: 16`, `vulnerable: 0`, `security_score: 100`, `go_no_go: go`.
- Scan de outro squad por caminho (`../maeve-genius-forge-squad`): executado com sucesso e exportação JSON/Markdown/HTML confirmada; o resultado apontou riscos no alvo, demonstrando funcionamento em squad externo.

## Limitações ainda existentes

- O runner atual é estático e determinístico; ele valida controles documentais e cenários canários, mas não executa conversas contra agentes vivos.
- Testes dinâmicos contra runtimes reais exigem adaptadores específicos por plataforma.
- A classificação `pass` indica cobertura mínima de controles nos artefatos do squad, não garantia absoluta de segurança operacional.
- A CI cobre o próprio SKEPTIC; cada squad adicional deve optar por regressões próprias quando for endurecido.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
