#!/usr/bin/env python3
"""Extração de texto de TXT/MD/PDF/DOCX (nativo), com degradação graciosa.

Para TXT/MD lê direto. Para DOCX lê via zipfile (document.xml). Para PDF tenta
um extrator leve de texto entre parênteses; se não houver camada de texto,
marca o item para OCR de fallback (ocr_fallback / ocr-especialista).

Uso: python scripts/extract_text.py --manifest ./saida/manifest.json --output ./saida
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path

from projur_common import read_json, sha256_text, write_json


def from_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def from_docx(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", errors="ignore")
        xml = re.sub(r"</w:p>", "\n", xml)
        return re.sub(r"<[^>]+>", "", xml)
    except Exception:
        return ""


def from_pdf(path: Path) -> str:
    """Extrator leve: junta strings de texto não-comprimido. Best-effort."""
    data = path.read_bytes()
    chunks = re.findall(rb"\(((?:[^()\\]|\\.)*)\)", data)
    txt = " ".join(c.decode("latin-1", errors="ignore") for c in chunks)
    return re.sub(r"\s+", " ", txt).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    manifest = read_json(args.manifest, {"itens": []})
    out = Path(args.output) if args.output else Path(args.manifest).parent
    textos_dir = out / "evidencias" / "textos"
    textos_dir.mkdir(parents=True, exist_ok=True)

    resultados = []
    for item in manifest.get("itens", []):
        p = Path(item["arquivo"])
        fmt = item.get("formato", "")
        if fmt in ("txt", "md"):
            texto = from_txt(p)
        elif fmt in ("docx", "doc"):
            texto = from_docx(p)
        elif fmt == "pdf":
            texto = from_pdf(p)
        else:
            texto = ""
        precisa_ocr = len(texto.strip()) < 40
        (textos_dir / f"{item['id']}.txt").write_text(texto, encoding="utf-8")
        resultados.append({
            "id": item["id"],
            "caracteres": len(texto),
            "precisa_ocr": precisa_ocr,
            "checksum_texto": sha256_text(texto),
        })

    write_json(out / "extracao.json", {"itens": resultados})
    pend = sum(1 for r in resultados if r["precisa_ocr"])
    print(f"Texto extraído de {len(resultados)} itens; {pend} item(ns) marcados para OCR.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
