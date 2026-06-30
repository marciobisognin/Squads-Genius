"""Construtor de contratos de ativação — Fase 2 do Gateway.

Gera prompt pronto para copiar/colar e checklist de insumos para ativar um squad.
"""

from .schemas import ActivationContract, ActivationChecklistItem
from typing import Any


def build_activation_contract(squad: dict[str, Any], matched_agents: list[str] = None) -> ActivationContract:
    """Constrói contrato de ativação para um squad.

    Args:
        squad: Dados do squad do índice
        matched_agents: IDs dos agentes relevantes (opcional)

    Returns:
        Contrato de ativação com prompt e checklist
    """
    squad_name = squad.get("name", "unknown-squad")
    squad_path = squad.get("path", "")
    entry_point = squad.get("entry_point", None)

    # Extrai agentes e tarefas
    agents = squad.get("agents", [])
    tasks = squad.get("tasks", [])
    workflows = squad.get("workflows", [])

    # Define agente de entrada
    if not entry_point and agents:
        entry_point = agents[0].get("id", "orchestrator")
    elif not entry_point:
        entry_point = "orchestrator"

    # Cria prompt de ativação
    available_agents_list = "\n".join([f"  - **{a.get('id')}**: {a.get('role', '')}" for a in agents[:10]])
    available_tasks_list = "\n".join([f"  - `{t.get('id')}`" for t in tasks[:10]])

    activation_prompt = f"""# Ativar Squad: {squad_name}

**Caminho:** `{squad_path}`
**Agente de entrada:** `{entry_point}`

## Agentes disponíveis

{available_agents_list or "Nenhum agente definido."}

## Tarefas disponíveis

{available_tasks_list or "Nenhuma tarefa definida."}

## Instruções de ativação

1. **Contexto:** Forneça o contexto completo da demanda
2. **Insumos:** Valide que todos os itens do checklist estão prontos
3. **Entrada:** Cole o prompt abaixo e ajuste conforme necessário:

---

Ativar o squad **{squad_name}** com o agente **{entry_point}**.

**Demanda:** [DESCREVA AQUI]

**Contexto:**
[FORNEÇA CONTEXTO RELEVANTE]

**Insumos:**
[CONFIRME DISPONIBILIDADE DOS INSUMOS]

---

## Próximos passos

- Monitorar execução via logs do squad
- Validar outputs contra critérios de sucesso
- Registrar feedback (sucesso/falha/ajustes) para memória

---

*Gerado pelo Squads Gateway — Fase 2*
"""

    # Cria checklist
    checklist_items = [
        ActivationChecklistItem(
            category="inputs",
            item="Descrição clara da demanda em linguagem natural",
            required=True,
            example="Criar conteúdo para Instagram sobre automação com IA",
        ),
        ActivationChecklistItem(
            category="context",
            item="Contexto organizacional e restrições",
            required=False,
            example="Público-alvo: CXOs, PMEs; tom: executivo",
        ),
        ActivationChecklistItem(
            category="context",
            item="Dados ou referências de entrada",
            required=False,
            example="URLs, arquivos, briefings",
        ),
        ActivationChecklistItem(
            category="credentials",
            item="Credenciais ou permissões necessárias",
            required=False,
            example="API keys, acesso ao banco de dados",
        ),
        ActivationChecklistItem(
            category="criteria",
            item="Critérios de sucesso explícitos",
            required=True,
            example="Top-3 acurácia, tempo < 5 minutos",
        ),
        ActivationChecklistItem(
            category="integration",
            item="Definir como será consumido o output",
            required=False,
            example="Integrar em dashboard, enviar por email, publicar em site",
        ),
    ]

    # Lista agentes e tarefas
    available_agents = [a.get("id", "") for a in agents]
    available_tasks = [t.get("id", "") for t in tasks]

    contract = ActivationContract(
        squad_name=squad_name,
        squad_path=squad_path,
        entry_point_agent=entry_point,
        activation_prompt=activation_prompt,
        checklist=checklist_items,
        available_agents=available_agents,
        available_tasks=available_tasks,
    )

    return contract


def print_activation_contract(contract: ActivationContract) -> None:
    """Imprime contrato de ativação de forma legível."""
    print("\n" + "=" * 80)
    print(f"📋 CONTRATO DE ATIVAÇÃO — {contract.squad_name}")
    print("=" * 80)

    print(f"\n📍 Localização: {contract.squad_path}")
    print(f"🚀 Agente de entrada: {contract.entry_point_agent}")

    print(f"\n👥 Agentes disponíveis ({len(contract.available_agents)}):")
    for agent in contract.available_agents[:5]:
        print(f"   - {agent}")
    if len(contract.available_agents) > 5:
        print(f"   ... e {len(contract.available_agents) - 5} mais")

    print(f"\n✅ Checklist de pré-ativação:")
    current_category = None
    for item in contract.checklist:
        if item.category != current_category:
            print(f"\n   [{item.category.upper()}]")
            current_category = item.category

        req_marker = "🔴 OBRIGATÓRIO" if item.required else "⚪ Opcional"
        print(f"   {req_marker}: {item.item}")
        if item.example:
            print(f"      Exemplo: {item.example}")

    print(f"\n📝 Prompt pronto para copiar:")
    print("-" * 80)
    print(contract.activation_prompt)
    print("-" * 80)
    print()


def export_activation_contract(contract: ActivationContract) -> dict:
    """Exporta contrato como dicionário JSON."""
    return contract.to_dict()
