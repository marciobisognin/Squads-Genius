# Maeve Genius Forge Squad

**Nome técnico:** `maeve-genius-forge-squad`
**Nome comercial:** Maeve Genius Forge — Sistema de Criação de Ativos com IA

Maeve Genius Forge é uma fábrica operacional para transformar briefing livre em sistema completo de IA: pesquisa, estratégia, design system, agentes, workflows, scripts, documentação, monetização e pacote publicável.

## Diferencial

O squad supera pipelines genéricos porque combina quatro camadas:

1. **Inteligência e pesquisa rastreável:** separa fatos, inferências, hipóteses, recomendações e fontes.
2. **Design original:** analisa referências sem copiar marca, gerando tokens, componentes e regras de aplicação.
3. **Automação determinística:** converte tarefas repetitivas em scripts Python locais para reduzir custo de tokens.
4. **Publicação e monetização:** entrega README, quality gates, ZIP, estratégia comercial e IP nativa.

## Agentes

- `forge-orchestrator` — Coordena o pipeline completo, decide ordem de execução, consolida outputs e aciona quality gates.
- `briefing-intelligence-analyst` — Extrai requisitos, lacunas, hipóteses e critérios de sucesso do briefing inicial.
- `deep-research-strategist` — Executa pesquisa profunda, organiza fontes, contexto, riscos e oportunidades com rastreabilidade.
- `business-model-architect` — Transforma pesquisa em proposta de valor, oferta, modelo comercial, precificação e monetização.
- `design-system-forger` — Cria design system original, tokens, componentes e guidelines visuais sem copiar marcas de terceiros.
- `workflow-engineer` — Mapeia processos, cria workflows, gates, rollback e trilhas humano-no-loop.
- `agent-architect` — Desenha agentes, papéis, comandos, responsabilidades, dependências e contratos de saída.
- `script-factory-engineer` — Identifica tarefas determinísticas e gera scripts portáveis, testáveis e de baixo custo.
- `quality-audit-sentinel` — Valida qualidade, segurança, autoria, rastreabilidade, executabilidade e completude.
- `github-release-publisher` — Empacota, cria README, prepara commit e publica no GitHub quando autorizado.

## Workflows

- `full_forge_pipeline.yaml` — pipeline completo de 15 fases.
- `design_system_only.yaml` — criação de identidade original e tokens.
- `script_automation_sprint.yaml` — identificação, criação e teste de scripts determinísticos.
- `github_release_pipeline.yaml` — validação, empacotamento, scan e publicação autorizada.

## Uso rápido

```bash
python scripts/validate_squad.py --root .
python scripts/forge_squad.py --briefing examples/example_consultoria_ia.yaml --output output/demo-consultoria
python scripts/estimate_costs.py --root output/demo-consultoria --manual-hours 12 --hourly-rate 150
python scripts/package_squad.py --root . --output ../../exports/maeve-genius-forge-squad-v1.0.0.zip
```

## Quality gates

- Clareza de briefing.
- Pesquisa com fontes e riscos.
- Design original e exportável.
- Arquitetura de squad não redundante.
- Scripts executáveis e testáveis.
- Publicação sem segredos, com licença/autoria.

## Segurança e propriedade intelectual

- Não publicar `.env`, tokens, chaves privadas ou credenciais.
- Usar referências apenas como insumo analítico.
- Encerrar respostas finais com o footer obrigatório.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
