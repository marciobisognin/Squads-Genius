"""Router Orquestrado — Fase 3 do Gateway.

Pipeline de orquestração: Intake → Normalize → Rank → Validate → Handoff → HITL
Implementado com máquina de estados simples (sem dependência de LangGraph).
"""

from enum import Enum
from typing import Any, Optional, Callable
from datetime import datetime

from .schemas import RouteRequest, RouteDecision, MatchedEntry
from .ranker import rank_squads
from .audit_logger import AuditLogger
from .memory_store import MemoryStore
from .hitl_gate import HITLGate, SafeMode


class RouterState(Enum):
    """Estados do pipeline de roteamento."""

    INTAKE = "intake"
    NORMALIZE = "normalize"
    RANK = "rank"
    VALIDATE = "validate"
    HANDOFF = "handoff"
    HITL = "hitl"
    COMPLETE = "complete"
    FAILED = "failed"


class OrchestrationRouter:
    """Router que orquestra o pipeline de roteamento de squads."""

    def __init__(
        self,
        index_data: dict[str, Any],
        audit_logger: Optional[AuditLogger] = None,
        memory_store: Optional[MemoryStore] = None,
        hitl_gate: Optional[HITLGate] = None,
    ):
        """Inicializa router.

        Args:
            index_data: Dados do índice de squads
            audit_logger: Logger de auditoria (optional)
            memory_store: Loja de memória (optional)
            hitl_gate: Gate de HITL (optional)
        """
        self.index_data = index_data
        self.audit_logger = audit_logger or AuditLogger()
        self.memory_store = memory_store or MemoryStore()
        self.hitl_gate = hitl_gate or HITLGate()

    def route(
        self,
        task_description: str,
        context: Optional[str] = None,
        preferred_domain: Optional[str] = None,
        require_hitl_approval: bool = False,
    ) -> RouteDecision:
        """Executa pipeline completo de roteamento.

        Args:
            task_description: Descrição da tarefa
            context: Contexto adicional (optional)
            preferred_domain: Domínio preferido (optional)
            require_hitl_approval: Requer aprovação HITL (default: False)

        Returns:
            Decisão estruturada de roteamento
        """
        state = {
            "current_state": RouterState.INTAKE,
            "task": task_description,
            "context": context,
            "preferred_domain": preferred_domain,
            "error": None,
        }

        print(f"\n🚀 Iniciando pipeline de roteamento...")
        print(f"   Task: {task_description[:60]}...")

        # 1. INTAKE: Valida entrada
        state = self._state_intake(state)
        if state["current_state"] == RouterState.FAILED:
            return self._create_failure_decision(state)

        # 2. NORMALIZE: Normaliza intenção
        state = self._state_normalize(state)

        # 3. RANK: Rankeia squads
        state = self._state_rank(state)
        if state["current_state"] == RouterState.FAILED:
            return self._create_failure_decision(state)

        # 4. VALIDATE: Valida resultado
        state = self._state_validate(state)

        # 5. HANDOFF: Prepara entrega
        state = self._state_handoff(state)

        # 6. HITL: Gate de aprovação (se necessário)
        if require_hitl_approval:
            state = self._state_hitl(state)
            if state["current_state"] == RouterState.FAILED:
                return self._create_failure_decision(state)

        state["current_state"] = RouterState.COMPLETE

        # Constrói resposta final
        decision = self._build_decision(state)

        print(f"\n✅ Pipeline concluído com sucesso!")
        print(f"   Top match: {decision.top_match.squad if decision.top_match else 'N/A'}")

        return decision

    def _state_intake(self, state: dict) -> dict:
        """Valida entrada."""
        print(f"\n📥 [INTAKE] Validando entrada...")

        task = state.get("task", "").strip()

        if not task or len(task) < 5:
            state["error"] = "Tarefa muito curta ou vazia"
            state["current_state"] = RouterState.FAILED
            print(f"❌ Entrada inválida: {state['error']}")
            return state

        state["current_state"] = RouterState.NORMALIZE
        print(f"✅ Entrada válida")

        return state

    def _state_normalize(self, state: dict) -> dict:
        """Normaliza intenção (sem LLM por enquanto)."""
        print(f"\n🔤 [NORMALIZE] Normalizando intenção...")

        # Aqui seria usado LLM em produção para embeddings
        # Por enquanto, mantemos a tarefa como está
        state["normalized_task"] = state.get("task", "")

        print(f"✅ Tarefa normalizada")
        return state

    def _state_rank(self, state: dict) -> dict:
        """Rankeia squads."""
        print(f"\n📊 [RANK] Ranqueando squads...")

        task = state.get("normalized_task", state.get("task", ""))
        ranked = rank_squads(task, self.index_data, top_n=5)

        if not ranked:
            state["error"] = "Nenhum squad encontrado"
            state["current_state"] = RouterState.FAILED
            print(f"❌ Roteamento falhou: {state['error']}")
            return state

        # Aplica boost de memória
        boost = self.memory_store.get_concept_boost(task)
        if boost > 1.0:
            print(f"🧠 Boost de memória: +{(boost-1)*100:.0f}%")
            ranked[0]["score"] *= boost

        state["ranked"] = ranked
        state["current_state"] = RouterState.VALIDATE

        print(f"✅ {len(ranked)} squads ranqueados")

        return state

    def _state_validate(self, state: dict) -> dict:
        """Valida resultado."""
        print(f"\n✓ [VALIDATE] Validando resultado...")

        ranked = state.get("ranked", [])

        if not ranked or ranked[0]["score"] < 1.0:
            print(f"⚠️  Score baixo (< 1.0). Pode indicar gap.")

        state["current_state"] = RouterState.HANDOFF
        print(f"✅ Validação concluída")

        return state

    def _state_handoff(self, state: dict) -> dict:
        """Prepara entrega."""
        print(f"\n📦 [HANDOFF] Preparando entrega...")

        ranked = state.get("ranked", [])
        top = ranked[0] if ranked else None

        # Log de auditoria
        self.audit_logger.log_route_event(
            task=state.get("task", ""),
            top_match=top["squad"] if top else None,
            score=top["score"] if top else 0,
            matched_keywords=top.get("matched_keywords", []) if top else [],
        )

        state["current_state"] = RouterState.HITL if state.get("require_hitl") else RouterState.COMPLETE
        print(f"✅ Handoff preparado")

        return state

    def _state_hitl(self, state: dict) -> dict:
        """Gate de aprovação HITL."""
        print(f"\n🔐 [HITL] Verificando gate de aprovação...")

        ranked = state.get("ranked", [])
        top = ranked[0] if ranked else None

        if not top:
            state["error"] = "Sem resultado para aprovar"
            state["current_state"] = RouterState.FAILED
            return state

        # Pede aprovação
        with SafeMode(
            self.hitl_gate,
            "activate_squad",
            f"Ativar squad {top['squad']}",
            {
                "squad": top["squad"],
                "score": top["score"],
                "agent": top.get("agent"),
            },
        ) as approved:
            if not approved:
                state["error"] = "Usuário rejeitou ativação"
                state["current_state"] = RouterState.FAILED
                print(f"❌ Ativação rejeitada pelo usuário")
                return state

        state["current_state"] = RouterState.COMPLETE
        print(f"✅ HITL gate aprovado")

        return state

    def _build_decision(self, state: dict) -> RouteDecision:
        """Constrói decisão de roteamento."""
        ranked = state.get("ranked", [])

        top_match = None
        if ranked:
            top = ranked[0]
            top_match = MatchedEntry(
                squad=top["squad"],
                path=top["path"],
                score=top["score"],
                agent=top.get("agent"),
                role=top.get("agent_role", ""),
                matched_keywords=top.get("matched_keywords", []),
                evidence=top.get("evidence", ""),
            )

        decision = RouteDecision(
            task_description=state.get("task", ""),
            recommendations=[
                MatchedEntry(
                    squad=r["squad"],
                    path=r["path"],
                    score=r["score"],
                    agent=r.get("agent"),
                    role=r.get("agent_role", ""),
                    matched_keywords=r.get("matched_keywords", []),
                    evidence=r.get("evidence", ""),
                )
                for r in ranked[:3]
            ],
            top_match=top_match,
            routing_index_version=self.index_data.get("version", "1.0.0"),
        )

        return decision

    @staticmethod
    def _create_failure_decision(state: dict) -> RouteDecision:
        """Cria decisão de falha."""
        from .schemas import GapAnalysis

        decision = RouteDecision(
            task_description=state.get("task", ""),
            gap_analysis=GapAnalysis(
                reason=state.get("error", "Erro desconhecido"),
                suggested_squad_name="novo-squad",
            ),
        )
        return decision
