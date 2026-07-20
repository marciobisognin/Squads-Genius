#!/usr/bin/env python3
"""Generate docs/squads/<id>.html pages and the docs/index.html grid from a JSON data file.

Usage:
    python3 docs/build/generate_site.py docs/build/squads_data.json

Re-run anytime squads_data.json changes. Keeps docs/index.html's hero/footer
intact and only replaces the #squad-grid contents.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
SQUADS_DIR = DOCS / "squads"

REPO_BASE_URL = "https://github.com/marciobisognin/Squads-Genius/tree/main"

# IDs cujo diretório real no repositório difere do id usado no site (ex.:
# versionamento no nome da pasta).
REPO_FOLDER_OVERRIDES = {
    "atlas-visual-reports-squad": "atlas-visual-reports-squad-v1.2.0",
    "argos-squad": "instituto-federal-farroupilha-iffar/argos-squad",
    "trajetoria-evidenciada-squad": "instituto-federal-farroupilha-iffar/trajetoria-evidenciada-squad",
    "scope-sentinel": "cibersegurança/scope-sentinel",
    "trace-mosaic": "cibersegurança/trace-mosaic",
    "breach-compass": "cibersegurança/breach-compass",
}


def resolve_repo_url(sq_id):
    folder = REPO_FOLDER_OVERRIDES.get(sq_id, sq_id)
    if (ROOT / "squads" / folder).is_dir():
        return f"{REPO_BASE_URL}/squads/{folder}"
    if (ROOT / "IFFar-Squads" / "squads" / folder).is_dir():
        return f"{REPO_BASE_URL}/IFFar-Squads/squads/{folder}"
    return None

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — Squads Genius</title>
<link rel="stylesheet" href="../assets/css/style.css">
<style>:root{{--accent:{color};--accent-soft:{color}26;}}</style>
</head>
<body>

<header class="topbar">
  <div class="wrap">
    <div class="brand"><span class="dot"></span> Squads Genius</div>
    <nav><a href="../index.html">← Todos os squads</a></nav>
  </div>
</header>

<div class="wrap squad-hero">
  <a class="back" href="../index.html">← voltar para a galeria</a>
  <h1><span class="badge-lg"><svg><use href="../assets/icons/sprite.svg#icon-{card_icon}"/></svg></span> {name}</h1>
  <p class="tagline">{tagline}</p>{links_html}
</div>

<section class="block">
  <div class="wrap">
    <h2>Agentes</h2>
    <div class="agents">
{agents_html}
    </div>
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <h2>Ferramentas e scripts</h2>
    <div class="tools">
{tools_html}
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <h2>Jornada <small>do briefing à entrega final</small></h2>
    <div class="journey">
      <div class="line"><div class="fill"></div></div>
{steps_html}
    </div>
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <h2>Entrega final</h2>
    <div class="output-box">
      <div class="tool-icon"><svg><use href="../assets/icons/sprite.svg#icon-output"/></svg></div>
      <div><strong>{output_title}</strong><span>{output_desc}</span></div>
    </div>
  </div>
</section>

{repo_link_html}
<footer>Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.</footer>
<script src="../assets/js/main.js"></script>
</body>
</html>
"""

AGENT_CARD = """      <div class="agent-card"><div class="avatar"><svg><use href="../assets/icons/sprite.svg#icon-{icon}"/></svg></div>
        <div><div class="role">{role}</div><h4>{name}</h4><p>{desc}</p></div></div>"""

TOOL_CARD = """      <div class="tool-card"><div class="tool-icon"><svg><use href="../assets/icons/sprite.svg#icon-script"/></svg></div><div><code>{file}</code><span>{desc}</span></div></div>"""

STEP_CARD = """      <div class="step"><div class="num">{n}</div><div class="body"><h4>{title}</h4><p>{desc}</p></div></div>"""

LINK_CHIP = """      <a class="squad-link" href="{url}" target="_blank" rel="noopener">{label}</a>"""

REPO_LINK_SECTION = """<section class="block alt">
  <div class="wrap">
    <div class="output-box">
      <div class="tool-icon"><svg><use href="../assets/icons/sprite.svg#icon-script"/></svg></div>
      <div><strong>Repositório do squad</strong><span><a href="{url}" target="_blank" rel="noopener">Ver {id} no GitHub →</a></span></div>
    </div>
  </div>
</section>"""

CARD_TEMPLATE = """      <a class="squad-card" href="squads/{id}.html" style="--accent-card:{color};--accent-soft-card:{color}26">
        <div class="badge"><svg><use href="assets/icons/sprite.svg#icon-{card_icon}"/></svg></div>
        <h3>{name}</h3>
        <p>{tagline}</p>
        <div class="meta"><span class="tag">{agent_count} agentes</span><span class="tag">{tool_count} scripts</span></div>
        <span class="open">Ver jornada →</span>
      </a>"""

# Ordem de exibição das categorias na galeria. IFFar fica como bloco
# institucional dedicado ao final. Categorias fora desta lista entram depois,
# em ordem alfabética.
CATEGORY_ORDER = [
    "Construção de Squads & Sistemas de IA",
    "Negócios, Estratégia & Vendas",
    "Conhecimento, Pesquisa & Dados",
    "Conteúdo, Marketing & Visual",
    "Educação & Desenvolvimento Cognitivo",
    "Cibersegurança",
    "Jurídico, Risco, Finanças & Segurança",
    "Saúde, Bem-estar & Expressão",
    "Instituto Federal Farroupilha (IFFar)",
]


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "cat"

VALID_ICONS = {
    "orchestrator", "researcher", "writer", "auditor", "designer", "validator",
    "analyst", "strategist", "reviewer", "communicator", "scientist", "architect",
    "builder", "guardian", "router", "planner", "composer", "factory", "failsafe",
    "generic", "script", "workflow", "input", "output",
}


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def safe_icon(icon):
    return icon if icon in VALID_ICONS else "generic"


def render_squad_page(sq):
    agents_html = "\n".join(
        AGENT_CARD.format(icon=safe_icon(a.get("icon")), role=esc(a.get("role")), name=esc(a.get("name")), desc=esc(a.get("desc")))
        for a in sq.get("agents", [])
    )
    tools = sq.get("tools", [])
    if tools:
        tools_html = "\n".join(TOOL_CARD.format(file=esc(t.get("file")), desc=esc(t.get("desc"))) for t in tools)
    else:
        tools_html = '      <div class="tool-card"><div class="tool-icon"><svg><use href="../assets/icons/sprite.svg#icon-workflow"/></svg></div><div><code>—</code><span>Squad sem scripts determinísticos dedicados.</span></div></div>'
    steps_html = "\n".join(
        STEP_CARD.format(n=i + 1, title=esc(s.get("title")), desc=esc(s.get("desc")))
        for i, s in enumerate(sq.get("steps", []))
    )
    links = sq.get("links", [])
    if links:
        chips = "\n".join(LINK_CHIP.format(url=esc(l.get("url")), label=esc(l.get("label"))) for l in links)
        links_html = f'\n  <div class="squad-links">\n{chips}\n  </div>'
    else:
        links_html = ""
    out = sq.get("output", {})
    repo_url = resolve_repo_url(sq["id"])
    repo_link_html = REPO_LINK_SECTION.format(url=esc(repo_url), id=esc(sq["id"])) if repo_url else ""
    html = PAGE_TEMPLATE.format(
        name=esc(sq["name"]),
        color=sq.get("color", "#7c5cff"),
        card_icon=safe_icon(sq.get("card_icon")),
        tagline=esc(sq.get("tagline")),
        links_html=links_html,
        agents_html=agents_html,
        tools_html=tools_html,
        steps_html=steps_html,
        output_title=esc(out.get("title")),
        output_desc=esc(out.get("desc")),
        repo_link_html=repo_link_html,
    )
    (SQUADS_DIR / f"{sq['id']}.html").write_text(html, encoding="utf-8")


def _card(sq):
    return CARD_TEMPLATE.format(
        id=sq["id"],
        color=sq.get("color", "#7c5cff"),
        card_icon=safe_icon(sq.get("card_icon")),
        name=esc(sq["name"]),
        tagline=esc(sq.get("tagline")),
        agent_count=len(sq.get("agents", [])),
        tool_count=len(sq.get("tools", [])),
    )


def render_index_grid(squads):
    # Agrupa por categoria, respeitando CATEGORY_ORDER e mantendo a ordem
    # original dos squads dentro de cada categoria.
    groups = {}
    for sq in squads:
        groups.setdefault(sq.get("category", "Outros"), []).append(sq)
    ordered = [c for c in CATEGORY_ORDER if c in groups]
    ordered += sorted(c for c in groups if c not in CATEGORY_ORDER)

    nav = "\n".join(
        f'      <a href="#cat-{slugify(c)}">{esc(c)} <span>{len(groups[c])}</span></a>'
        for c in ordered
    )
    sections = []
    for c in ordered:
        cards = "\n\n".join(_card(sq) for sq in groups[c])
        sections.append(
            f'    <section class="cat-section" id="cat-{slugify(c)}">\n'
            f'      <h2 class="cat-title">{esc(c)} <span class="cat-count">{len(groups[c])}</span></h2>\n'
            f'      <div class="grid">\n\n{cards}\n\n      </div>\n'
            f'    </section>'
        )
    body = f'    <nav class="cat-nav">\n{nav}\n    </nav>\n\n' + "\n\n".join(sections)

    index_path = DOCS / "index.html"
    text = index_path.read_text(encoding="utf-8")
    new_text = re.sub(
        r'(<div id="squad-grid">\n).*?(\n  </div>\n</main>)',
        lambda m: m.group(1) + "\n" + body + "\n" + m.group(2),
        text,
        flags=re.DOTALL,
    )
    index_path.write_text(new_text, encoding="utf-8")


def main():
    data_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("squads_data.json")
    all_squads = json.loads(data_path.read_text(encoding="utf-8"))
    SQUADS_DIR.mkdir(parents=True, exist_ok=True)
    for sq in all_squads:
        render_squad_page(sq)
    render_index_grid(all_squads)
    print(f"Generated {len(all_squads)} squad pages + updated index grid.")


if __name__ == "__main__":
    main()
