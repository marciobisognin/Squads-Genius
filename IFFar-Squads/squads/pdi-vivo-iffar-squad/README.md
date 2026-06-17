<div align="center">

# 🧭 PDI Vivo IFFar Squad

### Transforma o Plano de Desenvolvimento Institucional do IFFar em um **sistema vivo de gestão**: metas estruturadas, indicadores com fonte, evidências auditáveis, riscos monitorados, pactos por campus, relatórios trimestrais e painel — com engine determinística e humano no loop.

<p>
  <img src="https://img.shields.io/badge/status-premium-00B894?style=for-the-badge" />
  <img src="https://img.shields.io/badge/vers%C3%A3o-1.0.0-6C5CE7?style=for-the-badge" />
  <img src="https://img.shields.io/badge/domain-desenvolvimento%20institucional-0984E3?style=for-the-badge" />
  <img src="https://img.shields.io/badge/institui%C3%A7%C3%A3o-IFFar-00A86B?style=for-the-badge" />
  <img src="https://img.shields.io/badge/agentes%20SME-17-E17055?style=for-the-badge" />
  <img src="https://img.shields.io/badge/testes-pytest%20%2B%20smoke-2ECC71?style=for-the-badge" />
  <img src="https://img.shields.io/badge/license-MIT-6C5CE7?style=for-the-badge" />
</p>

</div>

---

## ✨ Ideia central

O **PDI Vivo IFFar Squad** converte o PDI de documento formal em **rotina operacional verificável**. Cada meta vira um registro estruturado com indicador, fonte, responsável, evidência, prazo e risco. A cada ciclo, o squad recalcula status e risco, gera relatório executivo, painel HTML e pactos por campus — sempre com **revisão humana** antes de publicar.

Ele integra três ciclos: **PDI 2014–2018** (base longitudinal), **PDI 2019–2026** (referência histórica) e **PDI 2027–2034** (ciclo vivo).

## 🎯 Para que serve

<table>
<tr>
<td><b>Estruturar metas</b><br/>Extrai dimensões, objetivos e metas e monta a matriz operacional validável.</td>
<td><b>Vincular evidências</b><br/>Cada indicador com fonte, periodicidade, cálculo e evidência auditável (hash).</td>
<td><b>Monitorar riscos</b><br/>Regra determinística eleva risco por atraso, lacuna de dados ou status crítico.</td>
</tr>
<tr>
<td><b>Pactuar por campus</b><br/>Filtra metas por campus, mapeia restrições e gera pacto territorial.</td>
<td><b>Apoiar decisão</b><br/>Relatório executivo trimestral + painel HTML + ata de decisão corretiva.</td>
<td><b>Comunicar e consultar</b><br/>Linguagem pública, consulta e devolutivas para a comunidade.</td>
</tr>
</table>

## 🤖 17 agentes SME

| Orquestração & documental | Dados & medição | Domínios institucionais | Comunicação & governança |
|---|---|---|---|
| pdi-orchestrator | goal-indicator-extractor | retention-success-monitor | dashboard-report-designer |
| documental-architect | evidence-data-curator | innovation-extension-radar | institutional-diplomacy-consultation |
| campus-territory-analyst | data-bi-integration-engineer | people-staffing-analyst | governance-ethics-lgpd-guardian |
| | risk-budget-dependency-analyst | infrastructure-works-analyst | |
| | budget-loa-ppa-analyst | institutional-assessment-cpa-sinaes-specialist | |
| | | methodology-mec-compliance-reviewer | |

## 🔁 Workflows

- **A** — Ingestão e comparação documental
- **B** — Matriz operacional de metas
- **C** — Pacto por campus
- **D** — Ciclo trimestral de acompanhamento
- **E** — Revisão anual e conferência bienal

## ⚙️ Scripts determinísticos

```bash
# 1) Extrair texto auditável do PDI (PDF/DOCX/MD/TXT) com hash e métricas
python3 scripts/extract_pdi_text.py --input pdi.pdf --label "PDI 2019-2026" --output-dir extracoes/

# 2) Montar a matriz preliminar de metas
python3 scripts/build_goal_matrix.py --input extracoes/pdi.txt --ciclo 2027-2034 --output matriz_metas.csv

# 3) Validar a matriz (lacunas, vocabulário, duplicidade, prazos)
python3 scripts/validate_indicator_matrix.py --input matriz_metas.csv --report output/quality_report.json

# 4) Comparar dois ciclos por incidência de termos de gestão viva
python3 scripts/compare_pdi_cycles.py --anterior extracoes/pdi_2019.txt --novo extracoes/pdi_2027.txt --output-dir output/

# 5) Matriz de riscos a partir da matriz de metas
python3 scripts/risk_matrix.py --input matriz_metas.csv --output-dir output/

# 6) Pacto territorial por campus
python3 scripts/build_campus_pact.py --input matriz_metas.csv --all --output-dir output/pactos/

# 7) Relatório executivo trimestral
python3 scripts/generate_quarterly_report.py --input matriz_metas.csv --trimestre 2026Q2 --output output/relatorio.md

# 8) Painel HTML local
python3 scripts/render_dashboard.py --input matriz_metas.csv --output output/dashboard.html
```

> O núcleo roda apenas com a **biblioteca padrão do Python 3.11+**. `pypdf`/`python-docx` são opcionais (extração de PDF/DOCX); há fallback para DOCX por descompactação.

## 🧪 Testes

```bash
python3 -m pytest tests/ -q        # testes de unidade
python3 scripts/smoke_test.py      # pipeline offline ponta a ponta
```

## 📂 Estrutura

```
pdi-vivo-iffar-squad/
├── README.md · PRD.md · squad.yaml · CHANGELOG.md
├── LICENSE · NOTICE.md · AUTHORS.md · requirements.txt
├── agents/        # 17 agentes SME (YAML)
├── tasks/         # tarefas operacionais
├── workflows/     # 5 workflows (A–E)
├── scripts/       # 10 scripts determinísticos + smoke test
├── schemas/       # goal · indicator · risk · evidence (JSON Schema)
├── templates/     # matriz, dicionário, relatório, ata, pacto
├── examples/      # matriz de exemplo, gerador de PDI sintético e saídas de exemplo
├── docs/          # metodologia · modelo de dados · roadmap
└── tests/         # pytest
```

## 🔒 Governança, ética e LGPD

- Minimização e mascaramento de dado pessoal; retenção configurável.
- Proibição de envio de dados institucionais a modelos externos sem autorização.
- Hash SHA-256 para fontes e evidências.
- Parecer do guardião de governança (com poder de bloqueio) antes de publicar.
- **Humano no loop**: publicação e repactuação sempre exigem revisão institucional.

## 📜 Conformidade
LDB (Lei 9.394/1996) · Lei 11.892/2008 · SINAES (Lei 10.861/2004) · Decreto 9.235/2017 · LGPD (Lei 13.709/2018) · instrumentos do MEC/INEP.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
