#!/usr/bin/env python3
"""Sága Mind-Keeper — Biblioteca de Mentes injetáveis.

Sága, deusa nórdica associada à memória e à narrativa, bebe diariamente com Odin.
Esta biblioteca guarda "mentes" (perfis de voz/persona em 5 camadas destilados pelo
Mímir DNA) e permite **injetá-las** em agentes de squads ou funcionários de empresas.

Salvaguardas de PI (herdadas do Mímir DNA e reaplicadas na injeção):
  * perfis são apenas estatísticas/descritores ABSTRATOS;
  * nenhum n-grama verbatim de 4+ palavras da fonte é emitido;
  * a injeção adiciona somente descritores de estilo — nunca texto.

Uso:
    python3 mind_clone_library.py --library ./dna --add "Voz Institucional" --input material.txt
    python3 mind_clone_library.py --library ./dna --list
    python3 mind_clone_library.py --library ./dna --inject "Voz Institucional" --agent-name "Delivery Builder"

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

from mimir_dna import distill, _assert_no_verbatim
from runic_architect import slugify

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."


def distill_profile(text: str, name: str, top_terms: int = 12) -> Dict[str, Any]:
    profile = distill(text, top_terms=top_terms)
    profile["id"] = slugify(name)
    profile["name"] = name
    return profile


def save_profile(profile: Dict[str, Any], path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.suffix in {".yaml", ".yml"} and yaml is not None:
        p.write_text(yaml.safe_dump(profile, allow_unicode=True, sort_keys=False), encoding="utf-8")
    else:
        p.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_profile(path: str | Path) -> Dict[str, Any]:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix in {".yaml", ".yml"} and yaml is not None:
        return yaml.safe_load(text)
    return json.loads(text)


def inject(profile: Dict[str, Any], agent: Dict[str, Any]) -> Dict[str, Any]:
    """Anexa um perfil de voz ABSTRATO a um agente/funcionário (sem texto da fonte)."""
    layers = profile.get("layers", {})
    descriptors = {
        "mind_id": profile.get("id"),
        "register": layers.get("5_tone_markers", {}).get("register"),
        "avg_sentence_length": layers.get("1_voice_cadence", {}).get("avg_sentence_length"),
        "type_token_ratio": layers.get("2_lexical_texture", {}).get("type_token_ratio"),
        "first_person_ratio": layers.get("5_tone_markers", {}).get("first_person_ratio"),
        "second_person_ratio": layers.get("5_tone_markers", {}).get("second_person_ratio"),
        "provenance": profile.get("provenance", "referência de estilo abstrata"),
    }
    enriched = dict(agent)
    enriched["voice_profile"] = descriptors
    return enriched


class MindCloneLibrary:
    """Repositório em disco de perfis de mente (YAML)."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        return self.root / f"{slugify(name)}.yaml"

    def add(self, name: str, text_path: str | Path, top_terms: int = 12) -> Dict[str, Any]:
        text = Path(text_path).read_text(encoding="utf-8")
        profile = distill_profile(text, name, top_terms=top_terms)
        # Salvaguarda extra: reprova qualquer vazamento verbatim antes de salvar.
        _assert_no_verbatim(text, profile)
        save_profile(profile, self._path(name))
        return profile

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        p = self._path(name)
        return load_profile(p) if p.exists() else None

    def list(self) -> List[Dict[str, str]]:
        out: List[Dict[str, str]] = []
        for p in sorted(self.root.glob("*.yaml")):
            prof = load_profile(p)
            out.append({"id": prof.get("id", p.stem), "name": prof.get("name", p.stem)})
        return out

    def inject_into(self, name: str, agent: Dict[str, Any]) -> Dict[str, Any]:
        profile = self.get(name)
        if profile is None:
            raise KeyError(f"mente não encontrada: {name}")
        return inject(profile, agent)


def main() -> int:
    ap = argparse.ArgumentParser(description="Biblioteca de Mentes injetáveis (Sága Mind-Keeper).")
    ap.add_argument("--library", required=True, help="Diretório da biblioteca de mentes.")
    ap.add_argument("--add", help="Nome da mente a adicionar.")
    ap.add_argument("--input", help="Arquivo de texto público de referência (com --add).")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--get", help="Nome da mente a exibir.")
    ap.add_argument("--inject", help="Nome da mente a injetar.")
    ap.add_argument("--agent-name", default="Agente", help="Nome do agente alvo da injeção (demo).")
    ap.add_argument("--top", type=int, default=12)
    args = ap.parse_args()
    lib = MindCloneLibrary(args.library)
    if args.add:
        if not args.input:
            ap.error("--add requer --input")
        prof = lib.add(args.add, args.input, top_terms=args.top)
        print(json.dumps({"added": prof["id"], "name": prof["name"]}, ensure_ascii=False, indent=2))
        return 0
    if args.list:
        print(json.dumps(lib.list(), ensure_ascii=False, indent=2))
        return 0
    if args.get:
        print(json.dumps(lib.get(args.get) or {}, ensure_ascii=False, indent=2))
        return 0
    if args.inject:
        enriched = lib.inject_into(args.inject, {"name": args.agent_name})
        print(json.dumps(enriched, ensure_ascii=False, indent=2))
        return 0
    ap.error("informe uma ação: --add, --list, --get ou --inject")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
