#!/usr/bin/env python3
"""Baixa as atas de registro de preços assinadas usadas na planilha entregue.

A partir de um manifesto que liga cada item da planilha às atas cujo preço foi
adotado, este script:

1. cria uma pasta por item (``atas/<codigo>-<slug>/``);
2. baixa (ou copia) os arquivos das atas assinadas para a pasta do item;
3. localiza, dentro de cada arquivo, em que página o item e o seu valor aparecem;
4. gera um ``index.html`` que aponta para a pasta de cada item, lista os arquivos
   e indica a página e o valor encontrados, além de um ``index.json`` com hashes
   para integridade de evidência.

Determinístico, sem dependências obrigatórias externas. O download usa apenas a
biblioteca padrão; a extração de texto de PDF usa ``pypdf``/``pdfminer`` quando
disponível e degrada com elegância quando não há rede ou biblioteca de PDF.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

USER_AGENT = "farol-atas-assinadas/1.0 (+farol-contratos-licitacoes-iffar)"
PNCP_API = "https://pncp.gov.br/api/pncp/v1"
PNCP_APP = "https://pncp.gov.br/app"

# numeroControlePncp: CNPJ(14)-tipo(1)-sequencial/ano  (ex.: 00394452000103-1-000123/2024)
_CONTROLE_RX = re.compile(r"(\d{14})-(\d+)-(\d+)/(\d{4})")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(text: str, max_len: int = 50) -> str:
    norm = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode("ascii")
    norm = re.sub(r"[^a-zA-Z0-9]+", "-", norm).strip("-").lower()
    return (norm[:max_len].strip("-")) or "item"


def item_folder_name(item: Dict[str, Any]) -> str:
    codigo = str(item.get("codigo") or item.get("codigoItemCatalogo") or "").strip()
    slug = slugify(item.get("descricao") or item.get("descricaoAmostra") or "item")
    return f"{codigo}-{slug}".strip("-") if codigo else slug


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_controle_pncp(numero: str) -> Optional[Dict[str, str]]:
    if not numero:
        return None
    m = _CONTROLE_RX.search(str(numero))
    if not m:
        return None
    cnpj, tipo, sequencial, ano = m.groups()
    return {"cnpj": cnpj, "tipo": tipo, "sequencial": str(int(sequencial)), "ano": ano}


def pncp_referencia(numero: str) -> Optional[str]:
    """URL pública (app PNCP) para consulta humana da ata pelo número de controle."""
    parts = parse_controle_pncp(numero)
    if not parts:
        return None
    return f"{PNCP_APP}/atas/{parts['cnpj']}/{parts['ano']}/{parts['sequencial']}"


def candidate_urls(ata: Dict[str, Any]) -> List[str]:
    """Retorna URLs candidatas para baixar o(s) arquivo(s) da ata, em ordem de prioridade."""
    urls: List[str] = []
    for key in ("url_documento", "url", "arquivo_url", "link"):
        v = ata.get(key)
        if isinstance(v, str) and v.startswith("http"):
            urls.append(v)
        elif isinstance(v, list):
            urls.extend([u for u in v if isinstance(u, str) and u.startswith("http")])
    parts = parse_controle_pncp(ata.get("numeroControlePncpAta") or ata.get("numeroControlePNCP") or "")
    if parts:
        # Endpoint de arquivos da contratação no PNCP (a listagem é resolvida em runtime).
        urls.append(
            f"{PNCP_API}/orgaos/{parts['cnpj']}/compras/{parts['ano']}/{parts['sequencial']}/arquivos"
        )
    return urls


def http_get(url: str, timeout: int = 90, retries: int = 2, backoff: float = 1.5) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    last_err: Optional[Exception] = None
    import time

    for attempt in range(retries + 1):
        try:
            with urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except (HTTPError, URLError, TimeoutError, OSError) as ex:  # pragma: no cover - rede
            last_err = ex
            if attempt < retries:
                time.sleep(backoff * (2 ** attempt))
                continue
    raise RuntimeError(f"falha ao baixar {url}: {last_err}")


def _safe_filename(url: str, fallback: str) -> str:
    name = url.rstrip("/").split("/")[-1].split("?")[0]
    if not name or "." not in name:
        name = fallback
    return slugify(Path(name).stem, 60) + (Path(name).suffix or ".pdf")


def baixar_arquivos_ata(ata: Dict[str, Any], destino: Path, *, download: bool = True) -> List[Dict[str, Any]]:
    """Baixa/copia os arquivos de uma ata para ``destino`` e retorna metadados por arquivo."""
    resultados: List[Dict[str, Any]] = []
    rotulo = str(ata.get("numeroAtaRegistroPreco") or ata.get("numeroControlePncpAta") or "ata")

    # 1) Arquivo local já fornecido (modo offline / evidência já coletada).
    local = ata.get("arquivo_local")
    if local:
        src = Path(local)
        if src.is_file():
            dest = destino / _safe_filename(str(src.name), slugify(rotulo) + ".pdf")
            shutil.copy2(src, dest)
            resultados.append({"arquivo": dest.name, "origem": str(src), "status": "copiado", "sha256": sha256_file(dest)})
            return resultados
        resultados.append({"arquivo": None, "origem": str(src), "status": "pendente", "motivo": "arquivo_local inexistente"})
        return resultados

    # 2) Download por URL/numero de controle PNCP.
    urls = candidate_urls(ata)
    if not urls:
        resultados.append({"arquivo": None, "status": "pendente", "motivo": "sem url_documento, arquivo_local ou numeroControlePncpAta"})
        return resultados
    if not download:
        resultados.append({"arquivo": None, "status": "pendente", "motivo": "download desabilitado (--no-download)", "urls": urls, "referencia_pncp": pncp_referencia(ata.get("numeroControlePncpAta", ""))})
        return resultados

    baixou = False
    for url in urls:
        try:
            data = http_get(url)
        except Exception as ex:  # pragma: no cover - rede
            resultados.append({"arquivo": None, "url": url, "status": "erro", "motivo": str(ex)})
            continue
        if not data.startswith(b"%PDF"):
            # Provável listagem JSON de arquivos do PNCP; registra para resolução humana.
            resultados.append({"arquivo": None, "url": url, "status": "pendente", "motivo": "resposta não-PDF (provável índice de arquivos); informar url_documento direta"})
            continue
        dest = destino / _safe_filename(url, slugify(rotulo) + ".pdf")
        dest.write_bytes(data)
        resultados.append({"arquivo": dest.name, "url": url, "status": "baixado", "sha256": sha256_file(dest)})
        baixou = True
        break
    if not baixou and all(r.get("status") != "baixado" for r in resultados):
        resultados.append({"status": "pendente", "motivo": "nenhuma URL retornou PDF", "referencia_pncp": pncp_referencia(ata.get("numeroControlePncpAta", ""))})
    return resultados


# ---------------------------------------------------------------------------
# Localização do item e do valor dentro do arquivo
# ---------------------------------------------------------------------------

def _extrair_paginas(arquivo: Path) -> List[str]:
    """Retorna o texto por página. ``.txt`` vira uma única página (útil em testes)."""
    if arquivo.suffix.lower() == ".txt":
        return [arquivo.read_text(encoding="utf-8", errors="replace")]
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(arquivo))
        return [(p.extract_text() or "") for p in reader.pages]
    except Exception:
        pass
    try:  # pragma: no cover - dependência opcional
        from pdfminer.high_level import extract_text  # type: ignore

        texto = extract_text(str(arquivo)) or ""
        return texto.split("\f") if "\f" in texto else [texto]
    except Exception:
        return []


def _valor_variantes(valor: Any) -> List[str]:
    out: List[str] = []
    try:
        v = float(str(valor).replace(".", "").replace(",", ".")) if isinstance(valor, str) and "," in valor else float(valor)
    except (TypeError, ValueError):
        return out
    out.append(f"{v:.2f}".replace(".", ","))   # 12,50
    out.append(f"{v:.2f}")                       # 12.50
    if v == int(v):
        out.append(str(int(v)))
    return list(dict.fromkeys(out))


def localizar_item(arquivo: Path, item: Dict[str, Any], valor: Any) -> List[Dict[str, Any]]:
    paginas = _extrair_paginas(arquivo)
    if not paginas:
        return [{"status": "parser_indisponivel", "motivo": "instale pypdf/pdfminer.six para localizar páginas em PDF"}]
    codigo = str(item.get("codigo") or item.get("codigoItemCatalogo") or "").strip()
    descricao = str(item.get("descricao") or item.get("descricaoAmostra") or "")
    tokens = [t for t in re.findall(r"[a-zA-ZÀ-ÿ0-9]{4,}", descricao.lower())]
    valores = _valor_variantes(valor)
    achados: List[Dict[str, Any]] = []
    for i, texto in enumerate(paginas, start=1):
        low = texto.lower()
        cod_ok = bool(codigo) and codigo.lower() in low
        val_ok = any(v in texto for v in valores)
        n_tok = sum(1 for t in set(tokens) if t in low)
        desc_ok = bool(tokens) and n_tok >= max(2, round(0.4 * len(set(tokens))))
        if cod_ok or val_ok or desc_ok:
            idx = -1
            for needle in ([codigo] if cod_ok else []) + (valores if val_ok else []):
                idx = low.find(needle.lower())
                if idx >= 0:
                    break
            trecho = " ".join(texto[max(0, idx - 60): idx + 80].split()) if idx >= 0 else ""
            achados.append({
                "pagina": i,
                "codigo_encontrado": cod_ok,
                "valor_encontrado": val_ok,
                "descricao_compativel": desc_ok,
                "score": round((cod_ok + val_ok + (n_tok / len(set(tokens)) if tokens else 0)) / 3, 3),
                "trecho": trecho,
            })
    if not achados:
        return [{"status": "nao_localizado", "motivo": "item/valor não encontrado no texto extraído"}]
    achados.sort(key=lambda a: -a.get("score", 0))
    return achados


# ---------------------------------------------------------------------------
# Índice HTML
# ---------------------------------------------------------------------------

def _money(v: Any) -> str:
    try:
        return "R$ " + f"{float(v):.2f}".replace(".", ",")
    except (TypeError, ValueError):
        return html.escape(str(v or ""))


def gerar_index_html(resultado: Dict[str, Any], outdir: Path) -> Path:
    itens = resultado.get("itens", [])
    linhas: List[str] = []
    for it in itens:
        pasta = it["pasta"]
        cabec = (
            f'<h2 id="{html.escape(pasta)}">{html.escape(str(it.get("codigo","")))} — '
            f'{html.escape(str(it.get("descricao","")))}</h2>'
            f'<p class="meta">Valor usado na planilha: <b>{_money(it.get("valor_usado"))}</b> · '
            f'Pasta: <a href="{html.escape(pasta)}/">{html.escape(pasta)}/</a></p>'
        )
        linhas.append(f'<section class="item">{cabec}')
        arquivos = it.get("arquivos", [])
        if not arquivos:
            linhas.append('<p class="pendente">Nenhum arquivo de ata baixado para este item.</p>')
        for arq in arquivos:
            nome = arq.get("arquivo")
            if nome:
                link = f'<a href="{html.escape(pasta)}/{html.escape(nome)}">{html.escape(nome)}</a>'
            else:
                ref = arq.get("referencia_pncp")
                link = (f'<a href="{html.escape(ref)}">consultar no PNCP</a>' if ref else "—")
            status = html.escape(str(arq.get("status", "")))
            ata_rotulo = html.escape(str(arq.get("ata", "")))
            linhas.append(f'<h3 class="arq">📄 {link} <span class="badge">{status}</span> <span class="ata">{ata_rotulo}</span></h3>')
            locs = arq.get("localizacoes", [])
            rows = []
            for loc in locs:
                if loc.get("pagina"):
                    flags = ", ".join(f for f, on in [("código", loc.get("codigo_encontrado")), ("valor", loc.get("valor_encontrado")), ("descrição", loc.get("descricao_compativel"))] if on)
                    rows.append(
                        f'<tr><td>{loc["pagina"]}</td><td>{html.escape(flags)}</td>'
                        f'<td>{_money(it.get("valor_usado")) if loc.get("valor_encontrado") else "—"}</td>'
                        f'<td class="trecho">{html.escape(loc.get("trecho",""))}</td></tr>'
                    )
                else:
                    rows.append(f'<tr><td colspan="4" class="pendente">{html.escape(loc.get("status",""))}: {html.escape(loc.get("motivo",""))}</td></tr>')
            if rows:
                linhas.append('<table><thead><tr><th>Página</th><th>Encontrado</th><th>Valor</th><th>Trecho</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>")
        linhas.append("</section>")

    toc = "".join(
        f'<li><a href="#{html.escape(it["pasta"])}">{html.escape(str(it.get("codigo","")))} — {html.escape(str(it.get("descricao",""))[:60])}</a></li>'
        for it in itens
    )
    doc = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atas assinadas — índice por item</title>
<style>
  body{{font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;margin:0;background:#0f1226;color:#e8eaf2}}
  header{{background:linear-gradient(135deg,#6C5CE7,#0984E3);padding:28px 22px;color:#fff}}
  header h1{{margin:0 0 6px;font-size:1.5rem}}
  main{{max-width:1040px;margin:0 auto;padding:20px}}
  nav{{background:#161a36;border-radius:12px;padding:14px 18px;margin-bottom:18px}}
  nav ul{{margin:6px 0 0;padding-left:18px}} nav a{{color:#9ecbff;text-decoration:none}}
  section.item{{background:#161a36;border-radius:12px;padding:16px 18px;margin:14px 0;border:1px solid #262c52}}
  h2{{margin:0 0 4px;font-size:1.15rem;color:#fff}} .meta{{color:#aab0d6;margin:0 0 10px}}
  h3.arq{{font-size:1rem;margin:14px 0 6px}}
  a{{color:#9ecbff}} .badge{{background:#2ECC71;color:#06210f;border-radius:6px;padding:1px 8px;font-size:.72rem;text-transform:uppercase}}
  .badge:empty{{display:none}} .ata{{color:#aab0d6;font-size:.82rem}}
  table{{width:100%;border-collapse:collapse;margin:6px 0 4px;font-size:.88rem}}
  th,td{{border:1px solid #2a305a;padding:6px 8px;text-align:left;vertical-align:top}}
  th{{background:#1d2347;color:#cdd3f5}} td.trecho{{color:#aab0d6}} .pendente{{color:#F39C12}}
  footer{{max-width:1040px;margin:0 auto;padding:18px;color:#8a90b8;font-size:.85rem}}
</style></head>
<body>
<header><h1>🧭 Atas de registro de preços assinadas — índice por item</h1>
<div>Caso: {html.escape(str(resultado.get("case_id","—")))} · Gerado em {html.escape(resultado.get("gerado_em",""))} · {len(itens)} item(ns)</div></header>
<main>
<nav><b>Itens</b><ul>{toc}</ul></nav>
{''.join(linhas)}
</main>
<footer>Evidência para conferência humana. Confirme página e valor no documento assinado antes de instruir o processo.<br>
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.</footer>
</body></html>"""
    out = outdir / "index.html"
    out.write_text(doc, encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Orquestração
# ---------------------------------------------------------------------------

def baixar(manifest: Dict[str, Any], outdir: Path, *, download: bool = True) -> Dict[str, Any]:
    atas_dir = outdir
    atas_dir.mkdir(parents=True, exist_ok=True)
    resultado: Dict[str, Any] = {
        "case_id": manifest.get("case_id"),
        "gerado_em": now_iso(),
        "fonte_manifesto": manifest.get("origem"),
        "itens": [],
    }
    for item in manifest.get("itens", []):
        pasta_nome = item_folder_name(item)
        pasta = atas_dir / pasta_nome
        pasta.mkdir(parents=True, exist_ok=True)
        item_res: Dict[str, Any] = {
            "codigo": item.get("codigo") or item.get("codigoItemCatalogo"),
            "descricao": item.get("descricao") or item.get("descricaoAmostra"),
            "valor_usado": item.get("valor_usado", item.get("mediana")),
            "pasta": pasta_nome,
            "arquivos": [],
        }
        for ata in item.get("atas", []) or []:
            arquivos = baixar_arquivos_ata(ata, pasta, download=download)
            rotulo = str(ata.get("numeroAtaRegistroPreco") or ata.get("numeroControlePncpAta") or "ata")
            for meta in arquivos:
                meta["ata"] = rotulo
                nome = meta.get("arquivo")
                if nome and meta.get("status") in ("baixado", "copiado"):
                    meta["localizacoes"] = localizar_item(pasta / nome, item, ata.get("valorUnitario", item_res["valor_usado"]))
                else:
                    if not meta.get("referencia_pncp"):
                        meta["referencia_pncp"] = pncp_referencia(ata.get("numeroControlePncpAta", ""))
                item_res["arquivos"].append(meta)
        resultado["itens"].append(item_res)

    index_html = gerar_index_html(resultado, atas_dir)
    index_json = atas_dir / "index.json"
    index_json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    resultado["index_html"] = str(index_html)
    resultado["index_json"] = str(index_json)
    return resultado


def montar_manifesto(resumo: List[Dict[str, Any]], case_id: Optional[str], origem: Optional[str]) -> Dict[str, Any]:
    """Cria um manifesto-esqueleto a partir do resumo de preços por código.

    As atas devem ser preenchidas pelo agente de pesquisa de preços com o número
    de controle PNCP / URL do documento assinado efetivamente adotado por item.
    """
    itens = []
    for rec in resumo:
        itens.append({
            "codigo": rec.get("codigoItemCatalogo") or rec.get("codigo"),
            "descricao": rec.get("descricaoAmostra") or rec.get("descricao"),
            "valor_usado": rec.get("mediana", rec.get("valor_usado")),
            "atas": [],  # preencher: numeroAtaRegistroPreco, numeroControlePncpAta, url_documento, valorUnitario
        })
    return {"case_id": case_id, "gerado_em": now_iso(), "origem": origem, "itens": itens}


def _load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Baixa atas assinadas usadas na planilha e gera índice HTML por item.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("baixar", help="baixa as atas do manifesto e gera o índice HTML por item")
    b.add_argument("--manifest", required=True, help="JSON ligando itens às atas usadas")
    b.add_argument("--out", default="output/atas-assinadas", help="pasta de saída (cria subpasta por item)")
    b.add_argument("--no-download", action="store_true", help="não acessa a rede; usa apenas arquivo_local e registra pendências")

    m = sub.add_parser("montar-manifesto", help="gera um manifesto-esqueleto a partir do resumo de preços por código")
    m.add_argument("--resumo", required=True, help="resumo_precos_por_codigo.json")
    m.add_argument("--out", required=True, help="caminho do manifesto a gerar")
    m.add_argument("--case-id")

    args = parser.parse_args(argv)
    if args.cmd == "baixar":
        manifest = _load_json(args.manifest)
        result = baixar(manifest, Path(args.out), download=not args.no_download)
        print(json.dumps({
            "case_id": result.get("case_id"),
            "itens": len(result.get("itens", [])),
            "index_html": result["index_html"],
            "index_json": result["index_json"],
        }, ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "montar-manifesto":
        resumo = _load_json(args.resumo)
        manifest = montar_manifesto(resumo, args.case_id, args.resumo)
        Path(args.out).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"manifesto": args.out, "itens": len(manifest["itens"])}, ensure_ascii=False, indent=2))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
