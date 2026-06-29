"""HITL Gate — Fase 3 do Gateway.

Gate de "Humano No Loop" que requer aprovação para ações críticas.
Bloqueia ações de publicação, credenciais ou mudanças sem aprovação.
"""

from enum import Enum
from typing import Optional, Callable


class ActionLevel(Enum):
    """Níveis de ação para HITL gate."""

    SAFE = "safe"  # Sem restrição (leitura, busca, relatório)
    REVIEW = "review"  # Requer review (ativar squad, modificar config)
    CRITICAL = "critical"  # Requer aprovação explícita (publicar, credenciais)


class HITLGate:
    """Gate de controle humano para ações críticas."""

    def __init__(self, approval_callback: Optional[Callable[[str], bool]] = None):
        """Inicializa gate.

        Args:
            approval_callback: Função para pedir aprovação (default: input())
        """
        self.approval_callback = approval_callback or self._default_approval

    @staticmethod
    def _default_approval(prompt: str) -> bool:
        """Pede aprovação interativa ao usuário."""
        response = input(f"\n{prompt}\n\n[y/n]: ").strip().lower()
        return response in ("y", "yes", "s", "sim")

    def check_action(
        self,
        action: str,
        level: ActionLevel,
        description: str = "",
        details: Optional[dict] = None,
    ) -> bool:
        """Verifica se uma ação é permitida.

        Args:
            action: Nome da ação (ex: 'activate_squad', 'publish_index')
            level: Nível de restrição (SAFE, REVIEW, CRITICAL)
            description: Descrição legível da ação
            details: Detalhes adicionais para mostrar ao usuário

        Returns:
            True se permitido, False se negado
        """
        if level == ActionLevel.SAFE:
            return True

        # Constrói prompt de aprovação
        prompt = self._build_approval_prompt(action, description, details, level)

        # Pede aprovação
        approved = self.approval_callback(prompt)

        if approved:
            print(f"✅ Ação '{action}' aprovada.")
        else:
            print(f"❌ Ação '{action}' rejeitada pelo usuário.")

        return approved

    @staticmethod
    def _build_approval_prompt(
        action: str,
        description: str,
        details: Optional[dict],
        level: ActionLevel,
    ) -> str:
        """Constrói prompt de aprovação legível."""
        level_icon = "🔍" if level == ActionLevel.REVIEW else "🚨"
        level_text = "REVISÃO" if level == ActionLevel.REVIEW else "APROVAÇÃO CRÍTICA"

        prompt = f"{level_icon} {level_text} REQUERIDA\n"
        prompt += f"\n📋 Ação: {action}"

        if description:
            prompt += f"\n📝 Descrição: {description}"

        if details:
            prompt += "\n\n📊 Detalhes:"
            for key, value in details.items():
                if isinstance(value, (list, dict)):
                    value = f"{type(value).__name__} com {len(value)} itens"
                prompt += f"\n  • {key}: {value}"

        prompt += "\n\n⚠️  Tem certeza que quer continuar?"

        return prompt

    @staticmethod
    def classify_action(action: str) -> ActionLevel:
        """Classifica o nível de restrição de uma ação.

        Args:
            action: Nome da ação

        Returns:
            Nível de restrição
        """
        # Ações críticas
        critical_actions = {
            "publish_index",
            "export_credentials",
            "reset_memory",
            "delete_logs",
            "update_weights",
        }

        # Ações de review
        review_actions = {
            "activate_squad",
            "generate_contract",
            "record_feedback",
            "create_squad",
        }

        action_lower = action.lower()

        if any(c in action_lower for c in critical_actions):
            return ActionLevel.CRITICAL

        if any(r in action_lower for r in review_actions):
            return ActionLevel.REVIEW

        return ActionLevel.SAFE


class SafeMode:
    """Context manager para modo seguro que requer aprovação."""

    def __init__(
        self,
        gate: HITLGate,
        action: str,
        description: str = "",
        details: Optional[dict] = None,
    ):
        """Inicializa modo seguro.

        Args:
            gate: Instância do HITLGate
            action: Nome da ação
            description: Descrição legível
            details: Detalhes adicionais
        """
        self.gate = gate
        self.action = action
        self.description = description
        self.details = details
        self.approved = False

    def __enter__(self) -> bool:
        """Entra no modo seguro e pede aprovação."""
        level = self.gate.classify_action(self.action)
        self.approved = self.gate.check_action(
            self.action, level, self.description, self.details
        )
        return self.approved

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sai do modo seguro."""
        if exc_type:
            print(f"❌ Erro durante execução: {exc_val}")
            return False
        return True


# Exemplo de uso
if __name__ == "__main__":
    gate = HITLGate()

    # Ação segura (sem aprovação necessária)
    print("\n1. Testando ação SAFE:")
    if gate.check_action("search_squad", ActionLevel.SAFE, "Buscar um squad"):
        print("   ✅ Pode prosseguir")

    # Ação de review (pede aprovação)
    print("\n2. Testando ação REVIEW:")
    if gate.check_action(
        "activate_squad",
        ActionLevel.REVIEW,
        "Ativar squad instagram-carrossel",
        {"squad": "instagram-carrossel-visual-pro", "agents": 5},
    ):
        print("   ✅ Pode prosseguir")

    # Usando context manager
    print("\n3. Usando SafeMode context manager:")
    with SafeMode(
        gate,
        "publish_index",
        "Publicar índice para produção",
        {"squads": 86, "destination": "docs/"},
    ) as approved:
        if approved:
            print("   ✅ Publicando...")
        else:
            print("   ❌ Publicação cancelada")
