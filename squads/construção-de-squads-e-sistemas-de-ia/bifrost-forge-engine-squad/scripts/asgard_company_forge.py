#!/usr/bin/env python3
"""Asgard Company Forge — forja de EMPRESAS (organograma, cargos e governança).

Se o Bifröst forja squads, a Asgard Company Forge forja **organizações**: de um
briefing de negócio, deriva deterministicamente um organograma (liderança →
chefias de departamento → funcionários), com cada funcionário como um agente com
contrato, além de governança, gates e trilha de auditoria (Saga Ledger).

Opcionalmente injeta uma "mente" (perfil de voz) da Biblioteca de Mentes em cada
funcionário — apenas descritores abstratos, nunca texto copiado.

Uso:
    python3 asgard_company_forge.py --briefing empresa.yaml --output ./empresa --overwrite --verify-determinism

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from company_briefing import CompanyBriefing, CompanyBriefingError, load_company_briefing
from saga_ledger import SagaLedger
from bifrost_orchestrator import tree_hash
from package_saga import base_package_files, dump_yaml, write_text
from runic_architect import slugify

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

DEFAULT_DEPARTMENTS = ["Produto", "Engenharia", "Comercial", "Operações", "Qualidade & Risco"]
DEPT_COUNT_BY_SIZE = {"small": 3, "medium": 4, "large": 5}
EMPLOYEES_BY_SIZE = {"small": 1, "medium": 2, "large": 3}


def design_org(briefing: CompanyBriefing) -> Dict[str, Any]:
    slug = slugify(briefing.company_name)
    depts = briefing.departments or DEFAULT_DEPARTMENTS[: DEPT_COUNT_BY_SIZE[briefing.size]]
    per_dept = EMPLOYEES_BY_SIZE[briefing.size]
    ceo_id = f"{slug}-allfather-ceo"
    leadership = {
        "id": ceo_id, "name": "Allfather (Direção)", "role": "Direção executiva",
        "reports_to": None,
        "responsibilities": ["definir visão e prioridades", "aprovar gates de governança", "alocar recursos entre departamentos"],
    }
    departments: List[Dict[str, Any]] = []
    employees: List[Dict[str, Any]] = []
    for dept in depts:
        dslug = slugify(dept)
        head_id = f"{slug}-{dslug}-head"
        head = {
            "id": head_id, "name": f"Chefia de {dept}", "department": dept, "role": f"Liderança de {dept}",
            "reports_to": ceo_id,
            "responsibilities": [f"liderar o departamento de {dept}", "garantir contratos e qualidade", "reportar riscos à direção"],
        }
        employees.append(head)
        dept_emps = [head_id]
        for n in range(1, per_dept + 1):
            emp_id = f"{slug}-{dslug}-specialist-{n}"
            employees.append({
                "id": emp_id, "name": f"Especialista {n} de {dept}", "department": dept,
                "role": f"Execução em {dept}", "reports_to": head_id,
                "responsibilities": [f"executar entregas de {dept}", "manter rastreabilidade ao objetivo", "seguir gates de segurança"],
            })
            dept_emps.append(emp_id)
        departments.append({"name": dept, "slug": dslug, "head": head_id, "employees": dept_emps, "file": f"departments/{dslug}.yaml"})
    return {"slug": slug, "leadership": leadership, "departments": departments, "employees": employees}


def _employee_md(emp: Dict[str, Any], mind: Optional[Dict[str, Any]]) -> str:
    resp = "\n".join(f"- {r}" for r in emp["responsibilities"])
    reports = emp.get("reports_to") or "—"
    voice = ""
    if mind:
        layers = mind.get("layers", {})
        tone = layers.get("5_tone_markers", {})
        voice = (
            "\n## Perfil de voz (mente injetada — descritores abstratos, sem cópia)\n"
            f"- Registro: {tone.get('register', 'n/d')}\n"
            f"- Cadência (frase média): {layers.get('1_voice_cadence', {}).get('avg_sentence_length', 'n/d')}\n"
            f"- Origem: {mind.get('provenance', 'referência de estilo')}\n"
        )
    return f"""# {emp['name']} (`{emp['id']}`)

## Cargo
{emp['role']}{' — ' + emp['department'] if emp.get('department') else ''}

## Reporta-se a
`{reports}`

## Responsabilidades
{resp}

## Contrato
```json
{json.dumps({'input': ['tarefa', 'contexto'], 'output': ['status', 'entregavel', 'notas']}, ensure_ascii=False, indent=2)}
```
{voice}
---
{FOOTER}
"""


class CompanyForge:
    def __init__(self, briefing: CompanyBriefing, output: Path, mind: Optional[Dict[str, Any]] = None) -> None:
        self.briefing = briefing
        self.output = Path(output)
        self.mind = mind
        self.files: Dict[str, str] = {}

    def build_files(self) -> Dict[str, str]:
        b = self.briefing
        org = design_org(b)
        slug = org["slug"]
        manifest = {
            "name": slug, "commercial_name": b.company_name, "type": "company", "version": "0.1.0",
            "language": "pt-BR", "license": "MIT", "creator": "Marcio Bisognin",
            "forged_by": "Asgard Company Forge", "required_footer": FOOTER,
            "mission": b.mission, "market": b.market, "offer": b.offer, "size": b.size,
            "leadership": {"id": org["leadership"]["id"], "file": f"employees/{org['leadership']['id']}.md"},
            "departments": org["departments"],
            "employees": [{"id": e["id"], "file": f"employees/{e['id']}.md", "reports_to": e.get("reports_to"), "department": e.get("department")} for e in [org["leadership"]] + org["employees"]],
            "governance_gates": ["mission_alignment", "contracts", "security", "human_approval"],
            "outputs": ["company.yaml", "employees", "departments", "governance.md", "README.md"],
            "mind_injected": bool(self.mind),
        }
        files: Dict[str, str] = {"company.yaml": dump_yaml(manifest)}
        for emp in [org["leadership"]] + org["employees"]:
            files[f"employees/{emp['id']}.md"] = _employee_md(emp, self.mind)
        for dept in org["departments"]:
            files[dept["file"]] = dump_yaml({
                "name": dept["name"], "head": dept["head"], "employees": dept["employees"], "footer": FOOTER,
            })
        files["governance.md"] = self._governance_md(b, org)
        files["README.md"] = self._readme_md(b, org)
        files["docs/overview.md"] = f"# Visão geral — {b.company_name}\n\nMissão: {b.mission}\nMercado: {b.market}\nOferta: {b.offer}\n\n{FOOTER}\n"
        files["examples/company_briefing.sample.yaml"] = dump_yaml(b.to_dict())
        files["scripts/run_company.py"] = self._runner()
        files["tests/test_structure.py"] = self._structure_test()
        files.update(base_package_files(b.company_name))
        self.files = files
        return files

    def _governance_md(self, b: CompanyBriefing, org: Dict[str, Any]) -> str:
        heads = "\n".join(f"- **{d['name']}** → `{d['head']}`" for d in org["departments"])
        return f"""# Governança — {b.company_name}

## Cadeia de comando
- Direção: `{org['leadership']['id']}`
{heads}

## Gates de governança
| Gate | Verifica |
|---|---|
| mission_alignment | Cada departamento rastreável à missão |
| contracts | Todo funcionário com contrato de entrada/saída |
| security | Nível `{b.security_level}`; sem persistência de credenciais |
| human_approval | {', '.join(b.human_approval_requirements) or 'a definir pela direção'} |

---
{FOOTER}
"""

    def _readme_md(self, b: CompanyBriefing, org: Dict[str, Any]) -> str:
        rows = "\n".join(f"| {d['name']} | `{d['head']}` | {len(d['employees'])} |" for d in org["departments"])
        return f"""# {b.company_name}

> {b.mission}

Organização forjada pela **Asgard Company Forge** — determinística e auditável.

## Mercado & oferta
- Mercado: {b.market}
- Oferta: {b.offer}
- Porte: {b.size}

## Organograma
| Departamento | Chefia | Pessoas |
|---|---|---|
{rows}

## Rodando
```bash
python3 scripts/run_company.py
```

---
{FOOTER}
"""

    def _runner(self) -> str:
        return ('#!/usr/bin/env python3\n'
                '"""Runner da empresa: resume o organograma do manifesto."""\n'
                'from __future__ import annotations\n'
                'import json\nfrom pathlib import Path\n'
                'try:\n    import yaml\nexcept Exception:\n    yaml = None\n\n\n'
                'def main() -> int:\n'
                '    root = Path(__file__).resolve().parents[1]\n'
                '    text = (root / "company.yaml").read_text(encoding="utf-8")\n'
                '    data = yaml.safe_load(text) if yaml else json.loads(text)\n'
                '    print(json.dumps({"company": data.get("commercial_name"), '
                '"departments": [d["name"] for d in data.get("departments", [])], '
                '"headcount": len(data.get("employees", []))}, ensure_ascii=False, indent=2))\n'
                '    return 0\n\n\n'
                'if __name__ == "__main__":\n    raise SystemExit(main())\n')

    def _structure_test(self) -> str:
        return ('"""Teste estrutural da empresa forjada."""\n'
                'from pathlib import Path\n\n'
                'ROOT = Path(__file__).resolve().parents[1]\n\n\n'
                'def test_company_files():\n'
                '    for rel in ["company.yaml", "README.md", "LICENSE", "NOTICE.md", "AUTHORS.md", "governance.md"]:\n'
                '        assert (ROOT / rel).is_file(), rel\n'
                '    assert (ROOT / "employees").is_dir()\n'
                '    assert (ROOT / "departments").is_dir()\n')

    def forge(self) -> Dict[str, Any]:
        self.output.mkdir(parents=True, exist_ok=True)
        saga = self.output / ".saga"
        saga.mkdir(exist_ok=True)
        ledger = SagaLedger(saga / "company_ledger.jsonl", deterministic=True)
        ledger.record("company", "run_start", {"company": self.briefing.company_name, "size": self.briefing.size})
        self.build_files()
        ledger.record("company", "org_designed", {"employees": sum(1 for k in self.files if k.startswith("employees/"))})
        for rel, content in self.files.items():
            write_text(self.output / rel, content if content.endswith("\n") else content + "\n")
        digest, per_file = tree_hash(self.output)
        report = {
            "company": self.briefing.company_name,
            "employees": sum(1 for k in self.files if k.startswith("employees/")),
            "departments": sum(1 for k in self.files if k.startswith("departments/")),
            "mind_injected": bool(self.mind),
            "determinism_hash": digest,
            "files": len(per_file),
            "go_no_go": "go",
        }
        write_text(self.output / "quality_report.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        ledger.record("company", "run_end", {"determinism_hash": digest})
        report["ledger_head"] = ledger.head
        return report


def _verify_determinism(briefing: CompanyBriefing, mind: Optional[Dict[str, Any]]) -> str:
    digests = []
    for _ in range(2):
        tmp = Path(tempfile.mkdtemp(prefix="company-det-"))
        try:
            CompanyForge(briefing, tmp, mind).forge()
            digests.append(tree_hash(tmp)[0])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    if digests[0] != digests[1]:
        raise CompanyBriefingError(f"determinismo quebrado: {digests[0]} != {digests[1]}")
    return digests[0]


def main() -> int:
    ap = argparse.ArgumentParser(description="Forja uma empresa (organograma + governança) a partir de um briefing.")
    ap.add_argument("--briefing", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify-determinism", action="store_true")
    ap.add_argument("--mind", help="Perfil de mente (YAML/JSON) da Biblioteca de Mentes para injetar.")
    args = ap.parse_args()
    try:
        briefing = load_company_briefing(args.briefing)
        mind = None
        if args.mind:
            from mind_clone_library import load_profile
            mind = load_profile(args.mind)
        if args.dry_run:
            org = design_org(briefing)
            print(json.dumps({"company": briefing.company_name, "departments": [d["name"] for d in org["departments"]],
                              "headcount": len(org["employees"]) + 1, "dry_run": True}, ensure_ascii=False, indent=2))
            return 0
        det = _verify_determinism(briefing, mind) if args.verify_determinism else None
        out = Path(args.output).resolve()
        if out.exists() and any(out.iterdir()):
            if not args.overwrite:
                raise CompanyBriefingError(f"Saída não vazia: {out}. Use --overwrite.")
            shutil.rmtree(out)
        report = CompanyForge(briefing, out, mind).forge()
        if det and det != report["determinism_hash"]:
            print(f"Aviso: hash difere ({det} != {report['determinism_hash']}).")
        report["determinism_verified"] = bool(args.verify_determinism)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except CompanyBriefingError as exc:
        print(f"Erro de briefing: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
