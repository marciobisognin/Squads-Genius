#!/usr/bin/env python3
"""Contrato de adaptador de host do AETHER OS (aether.host-adapter/v1).

Host é driver: o núcleo consome capacidades declaradas por contrato, com
degradação determinística por capacidade ausente — nunca improviso.
PRD v1.3, §9.4/9.5. Stdlib puro.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ENGINE_ID = "aether-host-adapter@1.0.0"

KNOWN_CAPABILITIES = ("subagent_fork", "prompt_caching", "native_sandbox",
                      "notification_channels", "approval_ui", "streaming")
INVOCATIONS = ("skill", "cli", "api")

# Tabela de degradação determinística (PRD §9.4): ausência tem comportamento
# definido. Mudar uma linha é mudança auditável de software.
DEGRADATION_TABLE = {
    "subagent_fork": "toda derivação vira instanciação limpa; custo maior, semântica idêntica",
    "prompt_caching": "layout de prompt permanece o mesmo; apenas sem reaproveitamento",
    "native_sandbox": "executor usa o sandbox próprio do AETHER",
    "notification_channels": "aprovações e alertas ficam na fila do dashboard/CLI, mesmos prazos",
    "approval_ui": "o gate aponta para 'aether approvals' na CLI",
    "streaming": "resposta entregue ao final do run, sem parcialidades",
}


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def validate(adapter: dict) -> dict:
    issues: list[str] = []
    if adapter.get("schema_version") != "aether.host-adapter/v1":
        issues.append("schema_version deve ser aether.host-adapter/v1")
    for field in ("host", "adapter_version", "invocation", "capabilities"):
        if field not in adapter:
            issues.append(f"campo obrigatório ausente: {field}")
    if adapter.get("invocation") not in INVOCATIONS:
        issues.append(f"invocation inválida: {adapter.get('invocation')}")
    caps = adapter.get("capabilities", {}) or {}
    for name in caps:
        if name not in KNOWN_CAPABILITIES:
            issues.append(f"capacidade desconhecida: {name}")
    for name in ("subagent_fork", "prompt_caching", "native_sandbox",
                 "approval_ui", "streaming"):
        if name in caps and not isinstance(caps[name], bool):
            issues.append(f"capacidade {name} deve ser booleana")
    return {"schema_version": "aether.host-adapter-validation/v1",
            "host": adapter.get("host", ""), "valid": not issues,
            "issues": issues, "validated_by": ENGINE_ID}


def capabilities(adapter: dict) -> dict:
    """Vetor de capacidades + degradação aplicável para cada ausência."""
    caps = adapter.get("capabilities", {}) or {}
    vector, degradations = {}, {}
    for name in KNOWN_CAPABILITIES:
        value = caps.get(name, False if name != "notification_channels" else [])
        present = bool(value)
        vector[name] = value
        if not present:
            degradations[name] = DEGRADATION_TABLE[name]
    return {"schema_version": "aether.host-capabilities/v1",
            "host": adapter.get("host", ""),
            "invocation": adapter.get("invocation", ""),
            "capabilities": vector,
            "degradations": degradations,
            "note": "o núcleo nunca depende de capacidade não declarada",
            "reported_by": ENGINE_ID}


def parity_stub(adapter_a: dict, adapter_b: dict) -> dict:
    """Comparação de vetores para a suíte golden de paridade (NFR-33).

    Paridade plena exige executar os runs de referência em cada host; aqui
    comparamos deterministicamente os vetores declarados e as degradações.
    """
    va, vb = capabilities(adapter_a), capabilities(adapter_b)
    diffs = [{"capability": k, adapter_a.get("host", "a"): va["capabilities"][k],
              adapter_b.get("host", "b"): vb["capabilities"][k]}
             for k in KNOWN_CAPABILITIES
             if va["capabilities"][k] != vb["capabilities"][k]]
    return {"schema_version": "aether.host-parity/v1",
            "hosts": [adapter_a.get("host", ""), adapter_b.get("host", "")],
            "capability_diffs": diffs,
            "verdict": "identical_vectors" if not diffs else "degradation_paths_differ",
            "note": "paridade é verificada, não presumida: rodar suíte golden nos runs de referência",
            "compared_by": ENGINE_ID}


def main() -> int:
    ap = argparse.ArgumentParser(description="Adaptador de Host AETHER")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate"); v.add_argument("--adapter", required=True)
    c = sub.add_parser("capabilities"); c.add_argument("--adapter", required=True)
    p = sub.add_parser("parity"); p.add_argument("--adapter-a", required=True)
    p.add_argument("--adapter-b", required=True)
    args = ap.parse_args()
    if args.cmd == "parity":
        a = json.loads(Path(args.adapter_a).read_text(encoding="utf-8"))
        b = json.loads(Path(args.adapter_b).read_text(encoding="utf-8"))
        print(canonical(parity_stub(a, b)))
        return 0
    adapter = json.loads(Path(args.adapter).read_text(encoding="utf-8"))
    if args.cmd == "validate":
        result = validate(adapter)
        print(canonical(result))
        return 0 if result["valid"] else 1
    print(canonical(capabilities(adapter)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
