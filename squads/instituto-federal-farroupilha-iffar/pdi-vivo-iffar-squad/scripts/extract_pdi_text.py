#!/usr/bin/env python3
"""Extrai texto auditável de PDF/DOCX/Markdown/TXT do PDI.

Salva o texto limpo, métricas (caracteres, linhas, incidência de termos-chave) e
o hash SHA-256 da fonte original — base auditável para todo o pipeline.

Uso:
    python3 extract_pdi_text.py --input pdi.pdf --output-dir extracoes/
    python3 extract_pdi_text.py --input pdi.docx --label "PDI 2019-2026"

Dependências opcionais: pypdf/PyPDF2 (PDF) e python-docx (DOCX). Markdown e TXT
são lidos sem dependências. DOCX também é lido via descompactação zip como fallback.
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdi_common import sha256_file, slugify, write_json  # noqa: E402

# Termos típicos de "gestão viva" — usados no relatório comparativo do estudo.
TERMOS_GESTAO_VIVA = [
    "monitoramento",
    "indicadores",
    "riscos",
    "evidências",
    "dashboard",
    "painel",
    "dados",
    "territorial",
    "permanência",
    "êxito",
    "orçamento",
    "metas",
]


def _read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _read_docx(path: Path) -> str:
    """Lê DOCX. Tenta python-docx; faz fallback para descompactação XML pura."""
    try:
        import docx  # type: ignore

        document = docx.Document(str(path))
        return "\n".join(p.text for p in document.paragraphs)
    except Exception:
        with zipfile.ZipFile(path) as zf:
            xml = zf.read("word/document.xml").decode("utf-8", errors="ignore")
        xml = re.sub(r"</w:p>", "\n", xml)
        xml = re.sub(r"<[^>]+>", "", xml)
        import html

        return html.unescape(xml)


def _read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        try:
            from PyPDF2 import PdfReader  # type: ignore
        except Exception as exc:  # pragma: no cover - ambiente sem libs de PDF
            raise SystemExit(
                "Para extrair PDF instale pypdf: pip install pypdf"
            ) from exc
    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".markdown"}:
        return _read_txt(path)
    if suffix == ".docx":
        return _read_docx(path)
    if suffix == ".pdf":
        return _read_pdf(path)
    raise SystemExit(f"Formato não suportado: {suffix}")


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def metrics(text: str) -> dict:
    lower = text.lower()
    return {
        "caracteres": len(text),
        "linhas": text.count("\n") + 1 if text else 0,
        "palavras": len(text.split()),
        "incidencia_termos": {t: lower.count(t.lower()) for t in TERMOS_GESTAO_VIVA},
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Extrai texto auditável do PDI.")
    ap.add_argument("--input", required=True, help="Arquivo PDF/DOCX/MD/TXT.")
    ap.add_argument("--output-dir", default="extracoes", help="Pasta de saída.")
    ap.add_argument("--label", default=None, help="Rótulo legível da fonte.")
    args = ap.parse_args(argv)

    src = Path(args.input)
    if not src.is_file():
        raise SystemExit(f"Arquivo não encontrado: {src}")

    label = args.label or src.stem
    slug = slugify(label)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    text = clean_text(extract_text(src))
    txt_path = out_dir / f"{slug}.txt"
    txt_path.write_text(text, encoding="utf-8")

    report = {
        "fonte": str(src),
        "label": label,
        "slug": slug,
        "sha256_fonte": sha256_file(src),
        "arquivo_extraido": str(txt_path),
        "metricas": metrics(text),
    }
    write_json(out_dir / f"{slug}.metrics.json", report)

    print(f"OK: {txt_path} ({report['metricas']['caracteres']} caracteres, "
          f"{report['metricas']['linhas']} linhas)")
    print(f"     hash fonte: {report['sha256_fonte'][:16]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
