#!/usr/bin/env python3
"""Renderiza um painel HTML local simples do PDI (sem dependências externas).

Mostra status consolidado, distribuição de risco, recortes por dimensão e por
campus e a lista de metas críticas. Auto-contido (CSS inline), pronto para abrir
no navegador ou servir como base de um BI institucional.

Uso:
    python3 render_dashboard.py --input matriz_metas.csv --output output/dashboard.html
"""
from __future__ import annotations

import argparse
import html
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdi_common import derive_risk, norm, read_csv  # noqa: E402

RISK_COLOR = {"crítico": "#e74c3c", "alto": "#e67e22", "médio": "#f1c40f", "baixo": "#2ecc71"}


def esc(value) -> str:
    return html.escape(str(value or ""))


def _bars(counter: Counter, total: int) -> str:
    out = []
    for label, n in sorted(counter.items(), key=lambda x: -x[1]):
        pct = round(100 * n / total, 1) if total else 0
        out.append(
            f'<div class="row"><span class="lbl">{esc(label)}</span>'
            f'<span class="bar"><i style="width:{pct}%"></i></span>'
            f'<span class="val">{n} ({pct}%)</span></div>'
        )
    return "\n".join(out)


def _risk_chips(counter: Counter) -> str:
    out = []
    for nivel in ("crítico", "alto", "médio", "baixo"):
        out.append(
            f'<span class="chip" style="background:{RISK_COLOR[nivel]}">'
            f'{nivel}: {counter.get(nivel, 0)}</span>'
        )
    return "".join(out)


def build_html(rows: list[dict]) -> str:
    total = len(rows)
    status_c = Counter(norm(r.get("status")) or "SEM STATUS" for r in rows)
    risco_c = Counter(derive_risk(r) for r in rows)
    dim_c = Counter(r.get("dimensao") or "—" for r in rows)
    campus_risk: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        campus_risk[r.get("campus") or "—"][derive_risk(r)] += 1

    criticas = [r for r in rows if derive_risk(r) in {"alto", "crítico"}]

    crit_rows = "\n".join(
        f"<tr><td>{esc(r.get('codigo'))}</td><td>{esc(r.get('dimensao'))}</td>"
        f"<td>{esc(r.get('campus'))}</td><td>{esc(r.get('meta'))[:90]}</td>"
        f"<td><b style='color:{RISK_COLOR[derive_risk(r)]}'>{derive_risk(r)}</b></td>"
        f"<td>{esc(r.get('status'))}</td></tr>"
        for r in criticas
    ) or "<tr><td colspan='6'>Sem metas críticas.</td></tr>"

    campus_rows = "\n".join(
        f"<tr><td>{esc(c)}</td><td>{sum(rc.values())}</td>"
        f"<td style='color:{RISK_COLOR['crítico']}'>{rc.get('crítico',0)}</td>"
        f"<td style='color:{RISK_COLOR['alto']}'>{rc.get('alto',0)}</td>"
        f"<td style='color:{RISK_COLOR['médio']}'>{rc.get('médio',0)}</td>"
        f"<td style='color:{RISK_COLOR['baixo']}'>{rc.get('baixo',0)}</td></tr>"
        for c, rc in sorted(campus_risk.items())
    )

    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Painel PDI Vivo IFFar</title>
<style>
  :root {{ --bg:#0f1724; --card:#16213a; --txt:#e8eefc; --muted:#9fb0d0; --accent:#3aa0ff; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:system-ui,Segoe UI,Roboto,sans-serif; background:var(--bg); color:var(--txt); }}
  header {{ padding:24px 32px; background:linear-gradient(120deg,#11244a,#0f1724); border-bottom:1px solid #24365e; }}
  h1 {{ margin:0; font-size:22px; }} .sub {{ color:var(--muted); font-size:13px; margin-top:4px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; padding:24px 32px; }}
  .card {{ background:var(--card); border:1px solid #24365e; border-radius:14px; padding:18px; }}
  .card h2 {{ font-size:14px; text-transform:uppercase; letter-spacing:.5px; color:var(--muted); margin:0 0 14px; }}
  .kpi {{ font-size:40px; font-weight:700; }}
  .chip {{ display:inline-block; color:#10243f; font-weight:700; padding:4px 10px; border-radius:20px; margin:3px 4px 0 0; font-size:12px; }}
  .row {{ display:flex; align-items:center; gap:10px; margin:6px 0; font-size:13px; }}
  .lbl {{ width:160px; color:var(--muted); }} .val {{ width:90px; text-align:right; color:var(--muted); }}
  .bar {{ flex:1; background:#0d1730; border-radius:8px; height:12px; overflow:hidden; }}
  .bar i {{ display:block; height:100%; background:var(--accent); }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th,td {{ text-align:left; padding:8px 10px; border-bottom:1px solid #24365e; }}
  th {{ color:var(--muted); text-transform:uppercase; font-size:11px; letter-spacing:.5px; }}
  footer {{ padding:18px 32px; color:var(--muted); font-size:12px; }}
</style></head>
<body>
<header>
  <h1>🧭 Painel PDI Vivo IFFar</h1>
  <div class="sub">Gerado em {date.today().isoformat()} · {total} metas acompanhadas · painel local determinístico</div>
</header>
<div class="grid">
  <div class="card"><h2>Metas acompanhadas</h2><div class="kpi">{total}</div></div>
  <div class="card"><h2>Distribuição de risco</h2>{_risk_chips(risco_c)}</div>
  <div class="card"><h2>Status</h2>{_bars(status_c, total)}</div>
  <div class="card"><h2>Metas por dimensão</h2>{_bars(dim_c, total)}</div>
</div>
<div class="grid">
  <div class="card" style="grid-column:1/-1"><h2>Risco por campus</h2>
    <table><thead><tr><th>Campus</th><th>Metas</th><th>Crítico</th><th>Alto</th><th>Médio</th><th>Baixo</th></tr></thead>
    <tbody>{campus_rows}</tbody></table>
  </div>
  <div class="card" style="grid-column:1/-1"><h2>Metas críticas (alto/crítico)</h2>
    <table><thead><tr><th>Código</th><th>Dimensão</th><th>Campus</th><th>Meta</th><th>Risco</th><th>Status</th></tr></thead>
    <tbody>{crit_rows}</tbody></table>
  </div>
</div>
<footer>Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin. · Painel para apoio à decisão; exige revisão humana institucional.</footer>
</body></html>
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Renderiza painel HTML do PDI.")
    ap.add_argument("--input", required=True, help="Matriz de metas (CSV).")
    ap.add_argument("--output", default="output/dashboard.html")
    args = ap.parse_args(argv)

    rows = read_csv(args.input)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_html(rows), encoding="utf-8")
    print(f"OK: painel HTML -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
