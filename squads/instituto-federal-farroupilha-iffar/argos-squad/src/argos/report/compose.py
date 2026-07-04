from __future__ import annotations
import json
from pathlib import Path
from argos.contracts import ClassificacaoPublicacao, PublicacaoNormalizada, RelatorioComposto, SintesePublicacao

def compose_report(run: dict, publicacoes: list[PublicacaoNormalizada], classificacoes: list[ClassificacaoPublicacao], sinteses: list[SintesePublicacao], estatisticas: dict, out_dir: str | Path) -> RelatorioComposto:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    run_id = run["run_id"]
    by_id = {p.id_canonico: p for p in publicacoes}
    syn = {s.id_canonico: s for s in sinteses}
    lines = [f"# Relatório ARGOS — {run['perfil_nome']}", "", "## Cabeçalho de auditoria", f"- run_id: `{run_id}`", f"- corpus_hash: `{run['corpus_hash']}`", f"- perfil_hash: `{run['perfil_hash']}`", f"- janela: `{run['inicio']}` a `{run['fim']}`", f"- fontes consultadas: {', '.join(run['fontes_consultadas']) or 'nenhuma'}", f"- fontes com falha/lacuna: {', '.join(run['fontes_lacuna']) or 'nenhuma'}", "", "## Sumário executivo", f"Foram avaliadas {estatisticas['total_corpus']} publicações normalizadas; {estatisticas['total_relevantes']} passaram pelo filtro de interesse e pelo gate de evidência literal.", "", "## Achados por categoria"]
    for cls in sorted(classificacoes, key=lambda c: (-c.relevancia, c.categoria)):
        pub = by_id[cls.id_canonico]
        resumo = syn[cls.id_canonico].resumo if cls.id_canonico in syn else pub.texto[:350]
        lines += [f"### {cls.categoria} — relevância {cls.relevancia}/100", f"- **Ato:** {pub.identifica or pub.ementa or pub.tipo_ato or 'Sem título'}", f"- **Órgão:** {pub.orgao or 'não informado'}", f"- **Fonte/Edição/Data:** {pub.fonte} · {pub.edicao} · {pub.data_publicacao.isoformat()}", f"- **Resumo:** {resumo}", f"- **Excerto-evidência literal:** > {cls.excerto_evidencia}", f"- **Link:** {pub.url_original}", ""]
    lines += ["## Estatísticas", "```json", json.dumps(estatisticas, ensure_ascii=False, indent=2, sort_keys=True), "```", "", "## Apêndice de lacunas"]
    lines += [f"- {x}" for x in run["lacunas"]] if run["lacunas"] else ["- Nenhuma lacuna declarada nesta execução."]
    md = "\n".join(lines) + "\n"
    md_path = out / f"{run_id}.md"
    html_path = out / f"{run_id}.html"
    json_path = out / f"{run_id}.json"
    md_path.write_text(md, encoding="utf-8")
    html = "<html><head><meta charset='utf-8'><title>ARGOS</title><style>body{font-family:sans-serif;max-width:980px;margin:40px auto;line-height:1.5}code,pre{background:#f4f4f4}</style></head><body><pre>" + md.replace('&','&amp;').replace('<','&lt;') + "</pre></body></html>"
    html_path.write_text(html, encoding="utf-8")
    json_path.write_text(json.dumps({"run": run, "estatisticas": estatisticas, "publicacoes": [p.model_dump(mode='json') for p in publicacoes], "classificacoes": [c.model_dump(mode='json') for c in classificacoes], "sinteses": [s.model_dump(mode='json') for s in sinteses]}, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return RelatorioComposto(run_id=run_id, markdown_path=str(md_path), html_path=str(html_path), json_path=str(json_path), corpus_hash=run['corpus_hash'], perfil_hash=run['perfil_hash'])
