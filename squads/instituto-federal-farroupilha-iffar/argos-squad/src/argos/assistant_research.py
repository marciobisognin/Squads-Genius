from __future__ import annotations

import json
import re
from dataclasses import asdict
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

import httpx
import yaml

from argos.official_sources import FEDERAL_SOURCE, MUNICIPAL_SOURCE, STATE_SOURCES, OfficialSource


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value[:80] or "pesquisa"


def _http_status(url: str, timeout: float = 10.0) -> dict:
    try:
        r = httpx.get(url, timeout=timeout, follow_redirects=True, headers={"User-Agent": "ARGOS/0.2 Maeve research"})
        return {"ok": r.status_code < 500, "status_code": r.status_code, "final_url": str(r.url), "error": None}
    except Exception as exc:
        return {"ok": False, "status_code": None, "final_url": url, "error": f"{type(exc).__name__}: {exc}"}


def query_querido_diario(assunto: str, municipio_ids: list[str] | None = None, size: int = 10) -> dict:
    base = "https://api.queridodiario.ok.org.br/api/gazettes"
    params: dict[str, str | int] = {"querystring": assunto, "size": size}
    if municipio_ids:
        params["territory_ids"] = ",".join(municipio_ids)
    try:
        r = httpx.get(base, params=params, timeout=20, follow_redirects=True, headers={"User-Agent": "ARGOS/0.2 Maeve research"})
        r.raise_for_status()
        data = r.json()
        gazettes = data.get("gazettes", [])
        return {"ok": True, "endpoint": str(r.url), "total_gazettes": data.get("total_gazettes"), "items": gazettes[:size], "error": None}
    except Exception as exc:
        return {"ok": False, "endpoint": base, "total_gazettes": None, "items": [], "error": f"{type(exc).__name__}: {exc}"}


def build_profile_yaml(assunto: str, ufs: list[str], municipio_ids: list[str] | None) -> dict:
    fontes = ["DOU-INLABS"] + [f"DOE-{uf}" if uf != "DF" else "DODF" for uf in ufs]
    if municipio_ids:
        fontes += [f"QD-{mid}" for mid in municipio_ids]
    else:
        fontes += ["QD"]
    return {
        "perfil": {
            "nome": slugify(assunto),
            "fontes": fontes,
            "secoes": ["DO1", "DO3"],
            "termos": [assunto],
            "termos_ignorados": [],
            "orgaos": [],
            "tipos_ato": [],
            "janela": "DIA",
            "entrega": ["arquivo"],
        }
    }


def run_assisted_research(root: str | Path, assunto: str, municipio_ids: list[str] | None = None, ufs: list[str] | None = None, size: int = 10, check_states: bool = True) -> dict:
    root = Path(root)
    ufs = [uf.upper() for uf in (ufs or sorted(STATE_SOURCES))]
    municipio_ids = municipio_ids or []
    run_id = f"argos-maeve-{date.today().isoformat()}-{slugify(assunto)}"
    out = root / "pesquisas" / run_id
    out.mkdir(parents=True, exist_ok=True)

    profile = build_profile_yaml(assunto, ufs, municipio_ids)
    (out / "perfil.yaml").write_text(yaml.safe_dump(profile, allow_unicode=True, sort_keys=False), encoding="utf-8")

    qd = query_querido_diario(assunto, municipio_ids=municipio_ids or None, size=size)

    state_rows = []
    for uf in ufs:
        source = STATE_SOURCES.get(uf)
        if not source:
            state_rows.append({"uf": uf, "ok": False, "error": "UF não catalogada"})
            continue
        health = _http_status(source.portal_url) if check_states else {"ok": None, "status_code": None, "final_url": source.portal_url, "error": None}
        state_rows.append({
            "uf": uf,
            "codigo": source.codigo,
            "nome": source.nome,
            "portal_url": source.portal_url,
            "assistant_search_url": source.assistant_search_url(assunto),
            "metodo": source.metodo,
            "status_operacional": source.status_operacional,
            "healthcheck": health,
            "producao_granular": False,
            "motivo": "Fonte estadual catalogada para pesquisa assistida; parser granular exige homologação HITL por UF.",
        })

    federal = {
        "source": asdict(FEDERAL_SOURCE),
        "configured": False,
        "lacuna": "Para coleta DOU em produção, configurar INLABS_USER/INLABS_PASSWORD. O ARGOS não usa Selenium contra a busca da Imprensa Nacional.",
    }

    payload = {
        "run_id": run_id,
        "assunto": assunto,
        "created_at": datetime.now().astimezone().isoformat(),
        "federal": federal,
        "municipal_querido_diario": qd,
        "estaduais": state_rows,
        "principio_de_evidencia": "Itens só entram como publicação quando houver texto/URL oficial coletado. Links estaduais assistidos são trilhas de pesquisa, não achados confirmados.",
    }
    (out / "fontes_consultadas.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    md = render_markdown(payload)
    (out / "relatorio_pesquisa.md").write_text(md, encoding="utf-8")
    (out / "links_estaduais.md").write_text(render_state_links(payload), encoding="utf-8")
    return {"run_id": run_id, "output_dir": str(out), "files": [str(out / name) for name in ["perfil.yaml", "fontes_consultadas.json", "relatorio_pesquisa.md", "links_estaduais.md"]]}


def render_markdown(payload: dict) -> str:
    qd = payload["municipal_querido_diario"]
    ok_states = sum(1 for row in payload["estaduais"] if row.get("healthcheck", {}).get("ok"))
    lines = [
        f"# Pesquisa ARGOS/Maeve — {payload['assunto']}",
        "",
        "## Escopo",
        f"- run_id: `{payload['run_id']}`",
        "- Federal: DOU/INLABS",
        "- Municipal: Querido Diário API",
        f"- Estadual: {len(payload['estaduais'])} portais catalogados; {ok_states} responderam ao healthcheck nesta execução",
        "",
        "## Regra de evidência",
        payload["principio_de_evidencia"],
        "",
        "## Federal — DOU",
        f"- Status: {'configurado' if payload['federal']['configured'] else 'pendente de credenciais'}",
        f"- Observação: {payload['federal']['lacuna']}",
        "",
        "## Municipal — Querido Diário",
        f"- Endpoint: {qd.get('endpoint')}",
        f"- OK: {qd.get('ok')}",
        f"- Total informado pela API: {qd.get('total_gazettes')}",
        "",
    ]
    for item in qd.get("items", [])[:10]:
        lines.append(f"- {item.get('date')} · {item.get('territory_id')} · {item.get('url') or item.get('txt_url')}")
    lines += ["", "## Estaduais — portais catalogados"]
    for row in payload["estaduais"]:
        hc = row.get("healthcheck", {})
        status = hc.get("status_code") or "sem resposta"
        lines.append(f"- **{row.get('uf')}** · {row.get('codigo')} · HTTP {status} · {row.get('portal_url')} · [busca assistida]({row.get('assistant_search_url')})")
    lines += ["", "## Próxima ação operacional", "Quando Marcio informar um novo assunto, executar `argos pesquisar --assunto \"...\"` e anexar a pasta gerada em `pesquisas/`."]
    return "\n".join(lines) + "\n"


def render_state_links(payload: dict) -> str:
    lines = [f"# Links estaduais — {payload['assunto']}", ""]
    for row in payload["estaduais"]:
        lines.append(f"## {row.get('uf')} — {row.get('nome')}")
        lines.append(f"- Portal: {row.get('portal_url')}")
        lines.append(f"- Busca assistida: {row.get('assistant_search_url')}")
        lines.append(f"- Status: {row.get('status_operacional')} — {row.get('motivo')}")
        lines.append("")
    return "\n".join(lines)
