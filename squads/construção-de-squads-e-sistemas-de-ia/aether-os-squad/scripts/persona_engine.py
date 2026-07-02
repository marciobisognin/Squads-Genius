#!/usr/bin/env python3
"""Motor de Personas do AETHER OS (aether.prosopon/v1) — PRD v1.3, §18.9-18.11.

Valida prósopa (proveniência item a item obrigatória), verifica rotulagem na
egressão, bloqueia personificação e governa a Galeria. Persona é máscara, não
juízo: nenhum campo de persona é lido por motor de decisão — este motor só
valida contratos e salvaguardas. Stdlib puro.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ENGINE_ID = "aether-persona-engine@1.0.0"

REQUIRED_LAYERS = ("principles", "mental_models", "heuristics", "methods", "voice")
LIFECYCLE = {"draft": {"experimental"}, "experimental": {"trusted", "deprecated"},
             "trusted": {"deprecated", "experimental"}, "deprecated": set()}
DISCLOSURE = "conteúdo sintético inspirado em método publicado"

# Antipersonificação: assinar, datar ou apresentar-se como a pessoa.
IMPERSONATION_PATTERNS = [
    re.compile(r"(?i)assinado(?:\s+por)?\s*[:,]"),
    re.compile(r"(?i)atenciosamente,\s*\n"),
    re.compile(r"(?i)\beu,\s+[A-ZÀ-Ü][a-zà-ü]+(\s+[A-ZÀ-Ü][a-zà-ü]+)+,"),
    re.compile(r"(?i)como (?:autor|autora) (?:da obra|do método), (?:eu|afirmo)"),
    re.compile(r"(?i)(?:endosso|recomendo) pessoalmente"),
]
# Atribuição factual sobre a pessoa (proibida nas camadas).
FACTUAL_PATTERNS = [
    re.compile(r"(?i)\b(?:nasceu|morreu|casou|foi preso|declarou em \d{4})\b"),
    re.compile(r"(?i)\bopina atualmente\b"),
]


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def validate(prosopon: dict) -> dict:
    """Valida contrato, proveniência por item e salvaguardas estruturais."""
    issues: list[str] = []
    if prosopon.get("schema_version") != "aether.prosopon/v1":
        issues.append("schema_version deve ser aether.prosopon/v1")
    for field in ("id", "version", "subject_reference", "layers", "labels"):
        if field not in prosopon:
            issues.append(f"campo obrigatório ausente: {field}")
    layers = prosopon.get("layers", {}) or {}
    for layer in REQUIRED_LAYERS:
        if layer not in layers:
            issues.append(f"camada ausente: {layer}")
    for layer in ("principles", "mental_models", "heuristics", "methods"):
        for i, item in enumerate(layers.get(layer, []) or []):
            if not isinstance(item, dict):
                issues.append(f"{layer}[{i}] deve ser objeto")
                continue
            if not item.get("provenance"):
                issues.append(f"{layer}[{i}] sem proveniência — obrigatória item a item")
            claim = str(item.get("claim", item.get("name", "")))
            if not claim:
                issues.append(f"{layer}[{i}] sem claim")
            for pattern in FACTUAL_PATTERNS:
                if pattern.search(claim):
                    issues.append(f"{layer}[{i}] contém atribuição factual "
                                  f"sobre a pessoa — proibido (zero atribuição)")
            if layer == "heuristics" and not item.get("when"):
                issues.append(f"heuristics[{i}] sem condição de uso (when)")
    disclosure = (prosopon.get("labels", {}) or {}).get("disclosure", "")
    if DISCLOSURE not in disclosure:
        issues.append(f"labels.disclosure deve conter: '{DISCLOSURE}'")
    if prosopon.get("lifecycle", "draft") not in LIFECYCLE:
        issues.append(f"lifecycle inválido: {prosopon.get('lifecycle')}")
    return {"schema_version": "aether.prosopon-validation/v1",
            "prosopon": prosopon.get("id", ""), "valid": not issues,
            "issues": issues, "validated_by": ENGINE_ID}


def label_check(text: str, persona_id: str) -> dict:
    """Verificação de egressão: rótulo obrigatório + antipersonificação."""
    issues: list[dict] = []
    if DISCLOSURE not in text:
        issues.append({"class": "policy_denied",
                       "detail": "rótulo de disclosure ausente no artefato"})
    for pattern in IMPERSONATION_PATTERNS:
        if pattern.search(text):
            issues.append({"class": "policy_denied",
                           "detail": f"padrão de personificação: {pattern.pattern}",
                           "security_event": True})
    return {"schema_version": "aether.persona-egress-check/v1",
            "persona": persona_id, "verdict": "pass" if not issues else "blocked",
            "issues": issues, "checked_by": ENGINE_ID}


def gallery_add(store: Path, prosopon: dict) -> dict:
    validation = validate(prosopon)
    if not validation["valid"]:
        return {"action": "rejected", "issues": validation["issues"]}
    entries = gallery_load(store)
    key = f"{prosopon['id']}@{prosopon['version']}"
    if any(f"{e['id']}@{e['version']}" == key for e in entries):
        return {"action": "duplicate", "prosopon": key}
    record = {"id": prosopon["id"], "version": prosopon["version"],
              "lifecycle": prosopon.get("lifecycle", "experimental"),
              "subject_reference": prosopon.get("subject_reference", ""),
              "status": "published"}
    entries.append(record)
    gallery_save(store, entries)
    return {"action": "published", "prosopon": key,
            "lifecycle": record["lifecycle"]}


def gallery_retire(store: Path, persona_id: str, reason: str) -> dict:
    """Despublicação auditada (pedido do titular ou depreciação)."""
    entries = gallery_load(store)
    hit = False
    for entry in entries:
        if entry["id"] == persona_id and entry["status"] == "published":
            entry["status"] = "retired"
            entry["lifecycle"] = "deprecated"
            entry["retire_reason"] = reason
            hit = True
    gallery_save(store, entries)
    return {"action": "retired" if hit else "not_found",
            "prosopon": persona_id, "reason": reason,
            "note": "despublicação auditada; trilha preservada"}


def gallery_load(store: Path) -> list[dict]:
    if not store.exists():
        return []
    return [json.loads(line) for line in
            store.read_text(encoding="utf-8").splitlines() if line.strip()]


def gallery_save(store: Path, entries: list[dict]) -> None:
    store.parent.mkdir(parents=True, exist_ok=True)
    store.write_text("".join(canonical(e) + "\n" for e in entries),
                     encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Motor de Personas AETHER")
    ap.add_argument("--gallery", default="personas/gallery.jsonl")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate"); v.add_argument("--prosopon", required=True)
    l = sub.add_parser("label-check"); l.add_argument("--artifact", required=True)
    l.add_argument("--persona", required=True)
    g = sub.add_parser("gallery-add"); g.add_argument("--prosopon", required=True)
    r = sub.add_parser("gallery-retire"); r.add_argument("--persona", required=True)
    r.add_argument("--reason", required=True)
    sub.add_parser("gallery-list")
    args = ap.parse_args()
    store = Path(args.gallery)
    if args.cmd == "validate":
        result = validate(json.loads(Path(args.prosopon).read_text(encoding="utf-8")))
        print(canonical(result))
        return 0 if result["valid"] else 1
    if args.cmd == "label-check":
        text = Path(args.artifact).read_text(encoding="utf-8", errors="ignore")
        result = label_check(text, args.persona)
        print(canonical(result))
        return 0 if result["verdict"] == "pass" else 10  # 10 = egressão bloqueada
    if args.cmd == "gallery-add":
        result = gallery_add(store, json.loads(Path(args.prosopon).read_text(encoding="utf-8")))
        print(canonical(result))
        return 0 if result["action"] == "published" else 1
    if args.cmd == "gallery-retire":
        print(canonical(gallery_retire(store, args.persona, args.reason)))
        return 0
    print(canonical(gallery_load(store)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
