# Limitações conhecidas

## Escopo do MVP (v1.0.0)
- **Modo padrão L1 *report-only*:** o squad analisa, recomenda e gera rascunhos;
  **não** altera fonte de verdade, não publica e não faz push.
- **Pesquisa offline:** `JAZZ` usa um catálogo curado local. Conectores de rede
  (`connectors/*.py`) são stubs determinísticos, habilitados apenas após gate HITL.
- **Observabilidade opcional:** sem Langfuse instalado, os spans são sintéticos
  (derivados do grafo), ainda determinísticos e auditáveis.

## Fora do MVP
- Execução L3 *unattended* real em repositórios; publicação automática.
- Integração credenciada com instrumentos externos; MCPs customizados complexos.
- Marketplace público de packs; UI web.

## Dependências
- O núcleo roda só com a **stdlib** do Python 3.11+. Pydantic, PyYAML, LangGraph,
  Langfuse e jsonschema são **opcionais** — cada um tem fallback ou é dispensável
  no modo report-only.

> Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
