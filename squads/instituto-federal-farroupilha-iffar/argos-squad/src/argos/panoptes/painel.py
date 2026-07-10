from __future__ import annotations
import html
import json
from pathlib import Path
from argos.engines.mnemon import Mnemon
from argos.official_sources import FEDERAL_SOURCE, MUNICIPAL_SOURCE, STATE_SOURCES
from argos.panoptes.ledger import LivroPanoptes
from argos.panoptes.retificacao import relatorio_retificacoes

# Cartograma em grade (coluna, linha) — posição relativa aproximada das 27 UFs.
UF_GRID = {
    "RR": (2, 0), "AP": (4, 0),
    "AM": (1, 1), "PA": (3, 1), "MA": (5, 1), "CE": (6, 1), "RN": (7, 1),
    "AC": (0, 2), "RO": (2, 2), "TO": (4, 2), "PI": (5, 2), "PB": (7, 2),
    "MT": (2, 3), "GO": (3, 3), "DF": (4, 3), "BA": (5, 3), "PE": (6, 3), "AL": (7, 3),
    "MS": (3, 4), "MG": (4, 4), "ES": (5, 4), "SE": (6, 4),
    "SP": (3, 5), "RJ": (4, 5),
    "PR": (3, 6),
    "SC": (3, 7),
    "RS": (2, 8),
}

STATUS_VISUAL = {
    "api": ("good", "●", "API ativa"),
    "assistido": ("warning", "◐", "Pesquisa assistida"),
    "credencial_requerida": ("serious", "○", "Credencial requerida"),
}

def _e(texto) -> str:
    return html.escape(str(texto if texto is not None else "—"), quote=True)

def _kpi(rotulo: str, valor: str, detalhe: str, tom: str = "") -> str:
    return f'<div class="kpi {tom}"><span class="kpi-label">{_e(rotulo)}</span><span class="kpi-valor">{_e(valor)}</span><span class="kpi-detalhe">{_e(detalhe)}</span></div>'

def _cadeia_html(entradas: list[dict]) -> str:
    if not entradas:
        return '<p class="vazio">Nenhum selo registrado ainda. Rode <code>argos buscar</code> para selar a primeira vigília.</p>'
    blocos = ['<div class="cadeia"><div class="bloco genesis"><span class="bloco-seq">GÊNESIS</span><span class="bloco-hash">ARGOS-PANOPTES</span></div>']
    for ent in entradas:
        blocos.append('<span class="elo" aria-hidden="true">→</span>')
        retif = len(ent.get("retificacoes", []))
        alerta = f'<span class="bloco-alerta">▲ {retif} retificação(ões)</span>' if retif else ""
        blocos.append(
            f'<div class="bloco" title="corpus_hash {_e(ent.get("corpus_hash", ""))}">'
            f'<span class="bloco-seq">SELO #{_e(ent.get("seq"))}</span>'
            f'<span class="bloco-run">{_e(ent.get("run_id"))}</span>'
            f'<span class="bloco-meta">{_e(str(ent.get("selado_em", ""))[:19])} · {_e(ent.get("total_relevantes"))}/{_e(ent.get("total_corpus"))} relevantes</span>'
            f'<span class="bloco-hash">selo {_e(str(ent.get("selo", ""))[:20])}…</span>{alerta}</div>'
        )
    blocos.append("</div>")
    return "".join(blocos)

def _diff_html(linhas: list[str], limite: int = 40) -> str:
    partes = []
    for linha in linhas[:limite]:
        cls = "diff-add" if linha.startswith("+") and not linha.startswith("+++") else "diff-del" if linha.startswith("-") and not linha.startswith("---") else "diff-ctx"
        partes.append(f'<span class="{cls}">{_e(linha)}</span>')
    if len(linhas) > limite:
        partes.append(f'<span class="diff-ctx">… {len(linhas) - limite} linha(s) omitida(s)</span>')
    return "\n".join(partes)

def _retificacoes_html(dossies: list[dict]) -> str:
    if not dossies:
        return '<p class="vazio">Nenhuma retificação silenciosa detectada. Cada ato monitorado manteve o mesmo conteúdo entre capturas.</p>'
    cartoes = []
    for d in dossies:
        chips = "".join(f'<span class="chip chip-del">− {_e(n)}</span>' for n in d["numeros_removidos"][:8])
        chips += "".join(f'<span class="chip chip-add">+ {_e(n)}</span>' for n in d["numeros_adicionados"][:8])
        numeros = f'<div class="chips"><span class="chips-rotulo">Números alterados:</span>{chips}</div>' if chips else '<div class="chips"><span class="chips-rotulo">Alteração textual sem mudança numérica.</span></div>'
        cartoes.append(
            f'<article class="retif"><header><span class="retif-id">{_e(d["id_canonico"])}</span>'
            f'<span class="retif-meta">{_e(d.get("fonte"))} · detectada em {_e(str(d.get("detectada_em", ""))[:19])}</span></header>'
            f'<div class="retif-hashes"><span title="hash anterior">{_e(d["hash_anterior"][:16])}…</span><span class="seta">→</span><span title="hash novo">{_e(d["hash_novo"][:16])}…</span></div>'
            f'{numeros}<pre class="diff">{_diff_html(d["diff"])}</pre></article>'
        )
    return "".join(cartoes)

def _cartograma_html(ufs_vigiadas: set[str]) -> str:
    celulas = []
    for uf, (col, lin) in sorted(UF_GRID.items()):
        fonte = STATE_SOURCES[uf]
        tom, simbolo, rotulo = STATUS_VISUAL.get(fonte.status_operacional, ("warning", "◐", fonte.status_operacional))
        extra = " vigiada" if uf in ufs_vigiadas else ""
        celulas.append(
            f'<div class="uf {tom}{extra}" style="grid-column:{col + 1};grid-row:{lin + 1}" '
            f'title="{_e(fonte.nome)} — {rotulo} · {_e(fonte.portal_url)}"><span class="uf-sigla">{uf}</span><span class="uf-status">{simbolo}</span></div>'
        )
    return '<div class="mapa">' + "".join(celulas) + "</div>"

def gerar_painel(root: str | Path, output: str | Path | None = None) -> Path:
    root = Path(root)
    runtime = root / ".argos"
    livro = LivroPanoptes(runtime)
    entradas = livro.entradas()
    veredito = livro.verificar()
    mnemon = Mnemon(runtime / "mnemon.sqlite")
    dossies = relatorio_retificacoes(mnemon)

    ultimo = entradas[-1] if entradas else {}
    referencia = str(ultimo.get("selado_em", "livro vazio"))[:19]
    total_vigiadas = mnemon.total_publicacoes()
    ufs_vigiadas = {f.replace("DOE-", "") for ent in entradas for f in ent.get("fontes_consultadas", []) if f.startswith("DOE-")}

    if veredito["integro"] and entradas:
        badge = '<span class="badge badge-good">✔ CADEIA ÍNTEGRA</span>'
        estado_cadeia, tom_cadeia = "íntegra", "good"
    elif not entradas:
        badge = '<span class="badge badge-warning">◐ LIVRO VAZIO</span>'
        estado_cadeia, tom_cadeia = "vazia", "warning"
    else:
        badge = f'<span class="badge badge-critical">✖ VIOLADA NO SELO #{_e(veredito["quebra_seq"])}</span>'
        estado_cadeia, tom_cadeia = f'violada (#{veredito["quebra_seq"]})', "critical"

    kpis = "".join([
        _kpi("Selos no livro", str(veredito["total"]), "runs seladas na cadeia"),
        _kpi("Cadeia de custódia", estado_cadeia, veredito["motivo"], tom_cadeia),
        _kpi("Publicações vigiadas", str(total_vigiadas), "atos com versão e hash no MNÉMON"),
        _kpi("Retificações detectadas", str(len(dossies)), "republicações com conteúdo alterado", "critical" if dossies else "good"),
    ])

    corpo = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ARGOS PANÓPTES — Painel de Vigília</title>
<style>
  :root {{
    --pagina:#0d0d0d; --superficie:#1a1a19; --borda:rgba(255,255,255,.10); --grade:#2c2c2a;
    --ink:#ffffff; --ink-2:#c3c2b7; --ink-3:#898781;
    --azul:#3987e5; --good:#0ca30c; --warning:#fab219; --serious:#ec835a; --critical:#d03b3b;
  }}
  * {{ box-sizing:border-box; margin:0; }}
  body {{ background:var(--pagina); color:var(--ink-2); font:15px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; padding:32px 20px 60px; }}
  main {{ max-width:1080px; margin:0 auto; display:grid; gap:28px; }}
  h1 {{ color:var(--ink); font-size:26px; letter-spacing:.5px; }}
  h1 .olho {{ color:var(--azul); }}
  h2 {{ color:var(--ink); font-size:17px; margin-bottom:4px; border-left:3px solid var(--azul); padding-left:10px; }}
  .sub {{ color:var(--ink-3); font-size:13px; }}
  .mono, .bloco-hash, .retif-hashes, .diff {{ font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }}
  header.topo {{ display:flex; flex-wrap:wrap; align-items:baseline; gap:14px; border-bottom:1px solid var(--grade); padding-bottom:18px; }}
  .badge {{ font-size:12px; font-weight:700; letter-spacing:.8px; padding:5px 12px; border-radius:999px; border:1px solid; }}
  .badge-good {{ color:var(--good); border-color:var(--good); }}
  .badge-warning {{ color:var(--warning); border-color:var(--warning); }}
  .badge-critical {{ color:var(--critical); border-color:var(--critical); }}
  section {{ background:var(--superficie); border:1px solid var(--borda); border-radius:14px; padding:22px; }}
  .kpis {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:12px; background:none; border:none; padding:0; }}
  .kpi {{ background:var(--superficie); border:1px solid var(--borda); border-radius:14px; padding:16px 18px; display:grid; gap:2px; }}
  .kpi-label {{ font-size:12px; text-transform:uppercase; letter-spacing:.8px; color:var(--ink-3); }}
  .kpi-valor {{ font-size:30px; font-weight:700; color:var(--ink); }}
  .kpi.good .kpi-valor {{ color:var(--good); }}
  .kpi.warning .kpi-valor {{ color:var(--warning); }}
  .kpi.critical .kpi-valor {{ color:var(--critical); }}
  .kpi-detalhe {{ font-size:12px; color:var(--ink-3); }}
  .cadeia {{ display:flex; align-items:center; gap:10px; overflow-x:auto; padding:8px 2px 14px; }}
  .bloco {{ min-width:200px; background:var(--pagina); border:1px solid var(--grade); border-radius:10px; padding:12px 14px; display:grid; gap:3px; flex-shrink:0; }}
  .bloco:hover {{ border-color:var(--azul); }}
  .bloco.genesis {{ min-width:130px; border-style:dashed; color:var(--ink-3); }}
  .bloco-seq {{ font-size:11px; font-weight:700; letter-spacing:.8px; color:var(--azul); }}
  .bloco-run {{ font-size:13px; color:var(--ink); }}
  .bloco-meta {{ font-size:11px; color:var(--ink-3); }}
  .bloco-hash {{ font-size:11px; color:var(--ink-3); }}
  .bloco-alerta {{ font-size:11px; color:var(--critical); font-weight:700; }}
  .elo {{ color:var(--grade); font-size:18px; flex-shrink:0; }}
  .retif {{ border:1px solid var(--grade); border-left:3px solid var(--critical); border-radius:10px; padding:14px 16px; margin-top:12px; display:grid; gap:8px; background:var(--pagina); }}
  .retif header {{ display:flex; flex-wrap:wrap; gap:10px; justify-content:space-between; border:none; padding:0; }}
  .retif-id {{ color:var(--ink); font-weight:600; }}
  .retif-meta {{ font-size:12px; color:var(--ink-3); }}
  .retif-hashes {{ font-size:12px; color:var(--ink-3); display:flex; gap:8px; align-items:center; }}
  .seta {{ color:var(--serious); }}
  .chips {{ display:flex; flex-wrap:wrap; gap:6px; align-items:center; }}
  .chips-rotulo {{ font-size:12px; color:var(--ink-3); }}
  .chip {{ font-size:12px; font-weight:600; padding:2px 10px; border-radius:999px; border:1px solid; }}
  .chip-del {{ color:var(--critical); border-color:var(--critical); }}
  .chip-add {{ color:var(--good); border-color:var(--good); }}
  .diff {{ font-size:12px; background:#111110; border:1px solid var(--grade); border-radius:8px; padding:12px; overflow-x:auto; display:grid; }}
  .diff-add {{ color:var(--good); }}
  .diff-del {{ color:var(--critical); }}
  .diff-ctx {{ color:var(--ink-3); }}
  .mapa {{ display:grid; grid-template-columns:repeat(8,minmax(44px,64px)); grid-auto-rows:44px; gap:6px; justify-content:center; padding:10px 0; }}
  .uf {{ border:1px solid var(--grade); border-radius:8px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:0; cursor:default; }}
  .uf:hover {{ border-color:var(--ink-2); }}
  .uf-sigla {{ font-size:12px; font-weight:700; color:var(--ink); }}
  .uf-status {{ font-size:10px; line-height:1; }}
  .uf.good {{ background:rgba(12,163,12,.12); }} .uf.good .uf-status {{ color:var(--good); }}
  .uf.warning {{ background:rgba(250,178,25,.10); }} .uf.warning .uf-status {{ color:var(--warning); }}
  .uf.serious {{ background:rgba(236,131,90,.10); }} .uf.serious .uf-status {{ color:var(--serious); }}
  .uf.vigiada {{ border-color:var(--azul); box-shadow:0 0 0 1px var(--azul); }}
  .legenda {{ display:flex; flex-wrap:wrap; gap:16px; font-size:12px; color:var(--ink-3); justify-content:center; margin-top:8px; }}
  .legenda b {{ font-weight:400; }}
  .fontes-fixas {{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:14px; }}
  .fonte-chip {{ font-size:12px; border:1px solid var(--grade); border-radius:999px; padding:4px 12px; color:var(--ink-2); }}
  .fonte-chip b {{ color:var(--ink); font-weight:600; }}
  .vazio {{ color:var(--ink-3); font-size:14px; padding:8px 0; }}
  code {{ background:#111110; border:1px solid var(--grade); border-radius:4px; padding:1px 6px; font-size:12px; }}
  footer {{ color:var(--ink-3); font-size:12px; text-align:center; border-top:1px solid var(--grade); padding-top:18px; }}
</style>
</head>
<body>
<main>
  <header class="topo">
    <h1><span class="olho">👁</span> ARGOS · PANÓPTES</h1>
    {badge}
    <span class="sub">Livro de Vigília — cadeia de custódia dos runs · referência {_e(referencia)}</span>
  </header>

  <div class="kpis">{kpis}</div>

  <section>
    <h2>Cadeia de custódia</h2>
    <p class="sub">Cada run é selada com SHA-256 sobre o selo anterior. Verifique offline: <code>argos panoptes verificar</code></p>
    {_cadeia_html(entradas)}
  </section>

  <section>
    <h2>Radar de retificações silenciosas</h2>
    <p class="sub">Mesmo ato oficial, conteúdo diferente entre capturas — diff literal e números alterados, sem interpretação de LLM.</p>
    {_retificacoes_html(dossies)}
  </section>

  <section>
    <h2>Cobertura de fontes oficiais — 27 UFs + federal + municipal</h2>
    <div class="fontes-fixas">
      <span class="fonte-chip">○ <b>DOU / INLABS</b> — federal · credencial requerida</span>
      <span class="fonte-chip">● <b>Querido Diário</b> — municipal · API ativa</span>
    </div>
    {_cartograma_html(ufs_vigiadas)}
    <div class="legenda">
      <span><b style="color:var(--good)">●</b> API ativa</span>
      <span><b style="color:var(--warning)">◐</b> Pesquisa assistida (homologação HITL pendente)</span>
      <span><b style="color:var(--serious)">○</b> Credencial requerida</span>
      <span><b style="color:var(--azul)">▢</b> UF consultada em runs seladas</span>
    </div>
  </section>

  <footer>Squad ARGOS · módulo PANÓPTES — painel estático gerado deterministicamente, sem rede e sem dependências.<br>
  Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.</footer>
</main>
</body>
</html>
"""
    destino = Path(output) if output else runtime / "panoptes" / "painel.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(corpo, encoding="utf-8")
    return destino
