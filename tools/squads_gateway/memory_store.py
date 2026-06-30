"""Memory Store — Fase 3 do Gateway.

Sistema de memória que aprende com feedback (sucesso/falha).
Ajusta pesos determinísticos e mantém histórico de aprendizagem.
"""

import json
from pathlib import Path
from typing import Any, Optional
from datetime import datetime


class MemoryStore:
    """Loja de memória com feedback e ajuste de pesos."""

    def __init__(self, memory_path: Path = None):
        """Inicializa memória.

        Args:
            memory_path: Caminho do arquivo de memória (default: gateway_memory.json)
        """
        self.memory_path = memory_path or Path("gateway_memory.json")
        self.memory = self._load_memory()

    def _load_memory(self) -> dict[str, Any]:
        """Carrega memória do disco."""
        if self.memory_path.exists():
            try:
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass

        # Memória padrão
        return {
            "version": "1.0.0",
            "created_at": datetime.utcnow().isoformat(),
            "last_updated_at": datetime.utcnow().isoformat(),
            "concept_weights": {},  # Conceitos que aparecem em boas respostas
            "squad_preferences": {},  # Preferências por squad baseado em feedback
            "feedback_history": [],  # Histórico de feedbacks
            "learning_events": [],  # Eventos de aprendizagem
        }

    def save_memory(self) -> None:
        """Salva memória no disco."""
        self.memory["last_updated_at"] = datetime.utcnow().isoformat()
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.memory_path, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    def record_feedback(
        self,
        task_description: str,
        selected_squad: str,
        feedback: str,  # success | failure | neutral
        notes: str = "",
    ) -> None:
        """Registra feedback sobre uma decisão de roteamento.

        Args:
            task_description: Descrição da tarefa original
            selected_squad: Squad que foi selecionado
            feedback: success | failure | neutral
            notes: Notas adicionais
        """
        # Registra no histórico
        feedback_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "task": task_description,
            "squad": selected_squad,
            "feedback": feedback,
            "notes": notes,
        }
        self.memory["feedback_history"].append(feedback_entry)

        # Se sucesso, aprende com os conceitos
        if feedback == "success":
            self._learn_from_success(task_description, selected_squad)
        elif feedback == "failure":
            self._learn_from_failure(task_description, selected_squad)

        self.save_memory()

    def _learn_from_success(self, task_description: str, squad_name: str) -> None:
        """Aprende com uma decisão bem-sucedida."""
        # Extrai palavras-chave da tarefa como conceitos
        concepts = self._extract_concepts(task_description)

        # Aumenta peso dos conceitos
        for concept in concepts:
            if concept not in self.memory["concept_weights"]:
                self.memory["concept_weights"][concept] = 0.0
            self.memory["concept_weights"][concept] += 1.0

        # Aumenta preferência por squad
        if squad_name not in self.memory["squad_preferences"]:
            self.memory["squad_preferences"][squad_name] = {"successes": 0, "failures": 0}
        self.memory["squad_preferences"][squad_name]["successes"] += 1

        # Registra evento de aprendizagem
        self.memory["learning_events"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "type": "positive_reinforcement",
            "squad": squad_name,
            "concepts_learned": concepts,
        })

    def _learn_from_failure(self, task_description: str, squad_name: str) -> None:
        """Aprende com uma decisão malsucedida."""
        # Diminui preferência por squad
        if squad_name not in self.memory["squad_preferences"]:
            self.memory["squad_preferences"][squad_name] = {"successes": 0, "failures": 0}
        self.memory["squad_preferences"][squad_name]["failures"] += 1

        # Registra evento de aprendizagem
        self.memory["learning_events"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "type": "negative_reinforcement",
            "squad": squad_name,
            "reason": "failed_attempt",
        })

    @staticmethod
    def _extract_concepts(text: str) -> list[str]:
        """Extrai conceitos (palavras-chave) de um texto."""
        import re

        # Remove pontuação e converte para lowercase
        text = text.lower()
        text = re.sub(r"[^0-9a-zà-ÿ\s\-]", " ", text)

        # Split em palavras
        words = re.split(r"[\s\-]+", text)

        # Filtra: apenas palavras com 3+ caracteres, não stopwords
        stopwords = {
            "a", "o", "e", "de", "do", "da", "das", "dos", "em", "no", "na",
            "para", "por", "com", "sem", "que", "um", "uma", "ao", "se", "ou",
            "the", "and", "of", "to", "in", "for", "with", "on", "is", "are",
        }

        concepts = []
        for word in words:
            word = word.strip()
            if len(word) >= 3 and word not in stopwords:
                concepts.append(word)

        return concepts

    def get_concept_boost(self, task_description: str) -> float:
        """Retorna boost de score baseado em conceitos aprendidos.

        Args:
            task_description: Descrição da tarefa

        Returns:
            Boost multiplicador (ex: 1.2 = +20%)
        """
        concepts = self._extract_concepts(task_description)
        total_weight = sum(self.memory["concept_weights"].get(c, 0) for c in concepts)

        # Normaliza: para cada conceito, ganha 0.1x
        boost = 1.0 + (total_weight * 0.1)

        # Capa em 1.5x (não deixa explodir)
        return min(boost, 1.5)

    def get_squad_confidence(self, squad_name: str) -> float:
        """Retorna confiança no squad baseada em feedback histórico.

        Args:
            squad_name: Nome do squad

        Returns:
            Score de confiança (0-1)
        """
        prefs = self.memory["squad_preferences"].get(squad_name)
        if not prefs:
            return 0.5  # Neutro se sem histórico

        successes = prefs.get("successes", 0)
        failures = prefs.get("failures", 0)
        total = successes + failures

        if total == 0:
            return 0.5

        # Score = successes / total
        return successes / total

    def print_memory_stats(self) -> None:
        """Imprime estatísticas da memória."""
        print("\n" + "=" * 70)
        print("🧠 MEMORY STORE STATISTICS")
        print("=" * 70)

        print(f"\n📚 Conceitos aprendidos: {len(self.memory['concept_weights'])}")
        if self.memory["concept_weights"]:
            top_concepts = sorted(
                self.memory["concept_weights"].items(),
                key=lambda x: x[1],
                reverse=True,
            )[:5]
            print("   Top conceitos:")
            for concept, weight in top_concepts:
                print(f"     - {concept}: {weight:.1f}")

        print(f"\n🎯 Squad preferences: {len(self.memory['squad_preferences'])}")
        if self.memory["squad_preferences"]:
            for squad, prefs in sorted(self.memory["squad_preferences"].items())[:5]:
                successes = prefs.get("successes", 0)
                failures = prefs.get("failures", 0)
                total = successes + failures
                if total > 0:
                    rate = successes / total * 100
                    print(f"   {squad}: {successes}✅ {failures}❌ ({rate:.0f}%)")

        print(f"\n📝 Feedback history: {len(self.memory['feedback_history'])} entradas")
        print(f"📊 Learning events: {len(self.memory['learning_events'])} eventos")

        print("\n" + "=" * 70 + "\n")

    def export_learning_report(self, output_path: Path = None) -> dict[str, Any]:
        """Exporta relatório de aprendizagem.

        Args:
            output_path: Caminho para salvar (opcional)

        Returns:
            Dicionário com o relatório
        """
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "total_feedback_entries": len(self.memory["feedback_history"]),
            "total_learning_events": len(self.memory["learning_events"]),
            "concepts_learned": len(self.memory["concept_weights"]),
            "squad_success_rates": {},
            "top_concepts": [],
        }

        # Calcula taxa de sucesso por squad
        for squad, prefs in self.memory["squad_preferences"].items():
            successes = prefs.get("successes", 0)
            total = successes + prefs.get("failures", 0)
            if total > 0:
                report["squad_success_rates"][squad] = {
                    "successes": successes,
                    "failures": prefs.get("failures", 0),
                    "success_rate": successes / total,
                }

        # Top conceitos
        if self.memory["concept_weights"]:
            top = sorted(
                self.memory["concept_weights"].items(),
                key=lambda x: x[1],
                reverse=True,
            )[:10]
            report["top_concepts"] = [{"concept": c, "weight": w} for c, w in top]

        # Salva se caminho fornecido
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

        return report
