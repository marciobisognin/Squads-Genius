"""Testes de acurácia de roteamento — Fase 2 do Gateway.

Valida que o roteamento atinge ≥90% de acerto no Top-3.
"""

import json
from pathlib import Path

from tools.squads_gateway.ranker import rank_squads
from .fixtures_routing import all_fixtures, get_fixture_by_id


def load_test_index() -> dict:
    """Carrega o índice de teste (gerado ou local)."""
    # Tenta carregar squads_index.json da raiz
    index_path = Path(__file__).parent.parent.parent.parent / "squads_index.json"

    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Fallback: retorna índice vazio para testes rápidos
    return {"squads": [], "version": "1.0.0"}


def test_routing_top3_accuracy():
    """Valida que ≥90% das fixtures acertam Top-3."""
    index = load_test_index()
    fixtures = all_fixtures()

    results = {
        "total_fixtures": len(fixtures),
        "correct_top3": 0,
        "failed_fixtures": [],
        "accuracies_by_category": {},
    }

    for fixture in fixtures:
        # Rankeia
        ranked = rank_squads(fixture.task_description, index, top_n=3)

        # Extrai nomes dos squads ranqueados
        ranked_squads = {r["squad"] for r in ranked}

        # Verifica se algum do Top-3 esperado está nos resultados
        match = any(expected in ranked_squads for expected in fixture.expected_top_squads)

        if match:
            results["correct_top3"] += 1
        else:
            results["failed_fixtures"].append({
                "fixture_id": fixture.id,
                "task": fixture.task_description,
                "expected": fixture.expected_top_squads,
                "got": list(ranked_squads),
            })

        # Agrupa por categoria
        if fixture.category not in results["accuracies_by_category"]:
            results["accuracies_by_category"][fixture.category] = {"total": 0, "correct": 0}

        results["accuracies_by_category"][fixture.category]["total"] += 1
        if match:
            results["accuracies_by_category"][fixture.category]["correct"] += 1

    # Calcula acurácia
    accuracy = results["correct_top3"] / results["total_fixtures"] * 100

    # Mostra resultados
    print(f"\n{'='*70}")
    print(f"🎯 ROUTING ACCURACY TEST RESULTS")
    print(f"{'='*70}")
    print(f"\n📊 Overall:")
    print(f"   Total fixtures: {results['total_fixtures']}")
    print(f"   Correct Top-3: {results['correct_top3']}")
    print(f"   Accuracy: {accuracy:.1f}%")
    print(f"   Target: ≥90%")
    print(f"   Status: {'✅ PASS' if accuracy >= 90 else '❌ FAIL'}")

    print(f"\n📈 By Category:")
    for category in sorted(results["accuracies_by_category"].keys()):
        cat_data = results["accuracies_by_category"][category]
        cat_accuracy = cat_data["correct"] / cat_data["total"] * 100
        print(f"   {category:20s}: {cat_data['correct']:2d}/{cat_data['total']:2d} ({cat_accuracy:5.1f}%)")

    if results["failed_fixtures"]:
        print(f"\n❌ Failed Fixtures ({len(results['failed_fixtures'])}):")
        for failed in results["failed_fixtures"][:5]:  # Mostra apenas primeiros 5
            print(f"\n   [{failed['fixture_id']}] {failed['task'][:60]}...")
            print(f"     Expected: {', '.join(failed['expected'][:2])}")
            print(f"     Got:      {', '.join(failed['got'][:2]) if failed['got'] else '(nenhum)'}")

    print(f"\n{'='*70}\n")

    # Assertion
    assert accuracy >= 90, f"Acurácia {accuracy:.1f}% < 90% (alvo)"

    return results


def generate_accuracy_report(output_path: Path = None) -> dict:
    """Gera relatório JSON de acurácia."""
    if output_path is None:
        output_path = Path(__file__).parent.parent.parent.parent / "routing_accuracy_report.json"

    results = {}
    try:
        results = test_routing_top3_accuracy()
    except AssertionError as e:
        results["error"] = str(e)

    # Salva relatório
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"📄 Relatório salvo: {output_path}")

    return results


if __name__ == "__main__":
    import sys

    try:
        results = test_routing_top3_accuracy()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Teste falhou: {e}")
        sys.exit(1)
