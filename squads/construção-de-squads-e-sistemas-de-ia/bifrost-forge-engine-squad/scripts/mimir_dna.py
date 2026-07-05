#!/usr/bin/env python3
"""Mímir DNA Distiller — destila um "DNA" de persona/voz em 5 camadas (opcional).

Mímir guarda o poço da sabedoria. Este módulo lê material PÚBLICO fornecido pelo
usuário e devolve um perfil de estilo ABSTRATO em 5 camadas — nunca o conteúdo em
si. É estrutural e determinístico.

Salvaguardas de propriedade intelectual (aplicadas e verificadas):
  * NÃO reproduz trechos: nenhum n-grama verbatim de 4+ palavras é emitido;
  * só estatísticas agregadas + palavras isoladas de alta frequência (não protegíveis);
  * declara explicitamente a origem como "referência de estilo", não cópia.

Uso:
    python3 mimir_dna.py --input material.txt --output dna.yaml

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

_STOP = {
    "de", "da", "do", "das", "dos", "e", "a", "o", "os", "as", "um", "uma", "que", "para", "por",
    "com", "sem", "em", "no", "na", "se", "ao", "the", "of", "and", "for", "to", "in", "is", "it",
    "you", "we", "i", "este", "esta", "isso", "mais", "como", "seu", "sua",
}
_FIRST_PERSON = {"eu", "nós", "meu", "minha", "nosso", "nossa", "i", "we", "my", "our"}
_SECOND_PERSON = {"você", "voce", "vocês", "voces", "teu", "tua", "seu", "sua", "you", "your"}


def _sentences(text: str) -> List[str]:
    return [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]


def _words(text: str) -> List[str]:
    return re.findall(r"[A-Za-zÀ-ÿ0-9]+", text.lower())


def distill(text: str, top_terms: int = 12) -> Dict[str, Any]:
    sents = _sentences(text)
    words = _words(text)
    total = max(1, len(words))
    sent_lens = [len(_words(s)) for s in sents] or [0]
    content = [w for w in words if w not in _STOP and len(w) > 2]
    freq = Counter(content)
    unique = len(set(words))

    layer1_voice = {
        "avg_sentence_length": round(sum(sent_lens) / len(sent_lens), 2),
        "min_sentence_length": min(sent_lens),
        "max_sentence_length": max(sent_lens),
        "sentence_count": len(sents),
    }
    layer2_lexis = {
        "type_token_ratio": round(unique / total, 4),
        "avg_word_length": round(sum(len(w) for w in words) / total, 2),
        "vocabulary_size": unique,
    }
    layer3_rhetoric = {
        "question_ratio": round(text.count("?") / max(1, len(sents)), 4),
        "exclamation_ratio": round(text.count("!") / max(1, len(sents)), 4),
        "comma_density": round(text.count(",") / total, 4),
    }
    layer4_themes = {
        # Palavras isoladas de alta frequência (não protegíveis). Sem frases.
        "top_content_terms": [{"term": t, "count": c} for t, c in freq.most_common(top_terms)],
    }
    layer5_tone = {
        "first_person_ratio": round(sum(1 for w in words if w in _FIRST_PERSON) / total, 4),
        "second_person_ratio": round(sum(1 for w in words if w in _SECOND_PERSON) / total, 4),
        "register": "formal" if layer2_lexis["avg_word_length"] >= 5.2 else "coloquial",
    }
    profile = {
        "dna_version": "1.0",
        "provenance": "Perfil de estilo ABSTRATO derivado de material público como referência; não é cópia de conteúdo.",
        "layers": {
            "1_voice_cadence": layer1_voice,
            "2_lexical_texture": layer2_lexis,
            "3_rhetorical_structure": layer3_rhetoric,
            "4_thematic_vectors": layer4_themes,
            "5_tone_markers": layer5_tone,
        },
        "footer": FOOTER,
    }
    _assert_no_verbatim(text, profile)
    return profile


def _assert_no_verbatim(source: str, profile: Dict[str, Any], n: int = 4) -> None:
    """Garante que nenhum n-grama de n+ palavras da fonte aparece na saída."""
    src_words = _words(source)
    src_ngrams = {" ".join(src_words[i:i + n]) for i in range(len(src_words) - n + 1)}
    emitted = _words(json.dumps(profile, ensure_ascii=False))
    for i in range(len(emitted) - n + 1):
        gram = " ".join(emitted[i:i + n])
        if gram in src_ngrams:
            raise ValueError("Salvaguarda de PI acionada: n-grama verbatim detectado na saída.")


def main() -> int:
    ap = argparse.ArgumentParser(description="Destila DNA de persona/voz (estrutural, com salvaguardas de PI).")
    ap.add_argument("--input", required=True, help="Arquivo de texto público de referência.")
    ap.add_argument("--output", help="Arquivo de saída (YAML se PyYAML disponível, senão JSON).")
    ap.add_argument("--top", type=int, default=12)
    args = ap.parse_args()
    text = Path(args.input).read_text(encoding="utf-8")
    profile = distill(text, top_terms=args.top)
    if args.output:
        out = Path(args.output)
        if out.suffix in {".yaml", ".yml"} and yaml is not None:
            out.write_text(yaml.safe_dump(profile, allow_unicode=True, sort_keys=False), encoding="utf-8")
        else:
            out.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(profile, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
