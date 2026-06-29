#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, datetime
from pathlib import Path
FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."
PHASES = [
("01", "intake"), ("02", "context"), ("03", "ai_inventory"), ("04", "classification"),
("05", "gap_mapping"), ("06", "legal_regulatory_mapping"), ("07", "risk_identification"), ("08", "risk_analysis"),
("09", "aiia"), ("10", "controls_design"), ("11", "soa"), ("12", "policy_pack"),
("13", "evidence_collection"), ("14", "internal_audit"), ("15", "management_review"), ("16", "certification_readiness")]

def risk_for(s):
    txt = " ".join(str(s.get(k,"")) for k in ["name","area","decision","data","criticality"]).lower()
    risks=[]
    if "rh" in txt or "currículo" in txt: risks += ["viés discriminatório", "explicabilidade insuficiente", "base legal e transparência"]
    if "contrat" in txt or "juríd" in txt: risks += ["erro jurídico material", "responsabilidade por recomendação", "confidencialidade"]
    if "cliente" in txt or "ticket" in txt: risks += ["alucinação", "vazamento de dados", "resposta inadequada"]
    if "código" in txt or "repo" in txt: risks += ["vazamento de propriedade intelectual", "código inseguro", "dependência de fornecedor"]
    return risks or ["falta de rastreabilidade", "ausência de dono", "controle insuficiente"]

def sev(s):
    c=s.get("criticality","").lower()
    return "alta" if c=="high" else "média" if c=="medium" else "baixa"

def write(out, name, lines):
    Path(out/name).write_text("\n".join(lines).rstrip()+"\n\n"+FOOTER+"\n", encoding="utf-8")

def main():
    ap=argparse.ArgumentParser(description="Gera pacote SGIA/AIMS ISO 42001 a partir de JSON de caso.")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--mode", default=None, choices=[None,"full_implementation","gap_analysis_only","audit_readiness_sprint"])
    args=ap.parse_args()
    data=json.loads(Path(args.input).read_text(encoding="utf-8"))
    out=Path(args.output); out.mkdir(parents=True, exist_ok=True)
    systems=data.get("ai_systems",[]); org=data.get("organization","Organização")
    mode=args.mode or data.get("capability","gap_analysis_only")
    date=datetime.date.today().isoformat()
    write(out,"00_EXECUTIVE_SUMMARY.md", [f"# Sumário Executivo — {org}", f"Data: {date}", f"Modo: {mode}", "", f"Sistemas de IA mapeados: {len(systems)}.", "Objetivo: preparar evidências, riscos e roadmap para SGIA/AIMS alinhado à ISO/IEC 42001.", "", "Decisão crítica: não alegar certificação sem auditoria formal; usar este pacote como prontidão e organização de evidências."])
    inv=[f"# Inventário de IA — {org}"]
    risk=[f"# Registro de Riscos de IA — {org}", "| Sistema | Área | Severidade | Riscos | Controles mínimos |", "|---|---|---|---|---|"]
    gap=[f"# Gap Analysis ISO/IEC 42001 — {org}", "## Lacunas típicas por sistema"]
    aiia=[f"# AIIA — AI Impact Assessment — {org}"]
    soa=[f"# Statement of Applicability — {org}", "| Controle | Aplicável | Justificativa | Evidência |", "|---|---|---|---|"]
    evidence=[f"# Índice de Evidências — {org}", "| Evidência | Sistema | Dono | Status |", "|---|---|---|---|"]
    for i,s in enumerate(systems,1):
        risks=risk_for(s); severity=sev(s)
        inv += ["", f"## {i}. {s.get('name','Sistema sem nome')}", f"- Área: {s.get('area','')}", f"- Decisão apoiada: {s.get('decision','')}", f"- Dados: {s.get('data','')}", f"- Fornecedor: {s.get('vendor','')}", f"- Criticidade: {severity}"]
        risk.append(f"| {s.get('name','')} | {s.get('area','')} | {severity} | {', '.join(risks)} | dono definido; revisão humana; logs; política; avaliação de impacto |")
        gap += ["", f"### {s.get('name','')}", "- Falta confirmar dono formal, finalidade, base documental e evidência de monitoramento.", "- Exigir registro de decisão, controle de fornecedor e revisão periódica."]
        aiia += ["", f"## {s.get('name','')}", f"- Pessoas/grupos afetados: clientes, usuários internos ou candidatos conforme processo.", f"- Riscos principais: {', '.join(risks)}.", "- Mitigação: revisão humana proporcional, logs, documentação, teste de vieses quando aplicável e canal de contestação."]
        evidence.append(f"| Registro de uso, política, logs, AIIA e controles | {s.get('name','')} | dono do processo | pendente/validar |")
    for ctrl in ["Inventário de IA", "Política de uso aceitável", "Gestão de risco de IA", "AIIA", "Gestão de fornecedores", "Monitoramento e melhoria contínua", "Auditoria interna", "Análise crítica da direção"]:
        soa.append(f"| {ctrl} | Sim | Essencial para SGIA/AIMS e defesa contratual | anexar evidência correspondente |")
    roadmap=[f"# Roadmap SGIA/AIMS — {org}", "## 0–30 dias", "- Fechar inventário, donos e política mínima.", "- Bloquear usos críticos sem evidência.", "", "## 31–60 dias", "- Completar risk register, AIIA e SoA.", "- Implementar controles por sistema.", "", "## 61–90 dias", "- Rodar auditoria interna e revisão executiva.", "- Montar pacote RFP/due diligence.", "", "## 9–12 meses", "- Operar ciclo completo de melhoria contínua e decidir certificação formal."]
    readiness=[f"# Certification Readiness Checker — {org}", "## Resultado preliminar", "Pronto para diagnóstico e organização de evidências; não declarar certificação.", "", "## Gates", "- Inventário completo?", "- Riscos classificados?", "- AIIA executada para usos relevantes?", "- SoA aprovado?", "- Evidências indexadas?", "- Auditoria interna realizada?", "- Direção revisou riscos e recursos?"]
    for fname, lines in [("01_AI_INVENTORY.md",inv),("02_GAP_ANALYSIS.md",gap),("03_RISK_REGISTER.md",risk),("04_AIIA.md",aiia),("05_SOA.md",soa),("06_EVIDENCE_INDEX.md",evidence),("07_ROADMAP.md",roadmap),("08_CERTIFICATION_READINESS.md",readiness)]:
        write(out, fname, lines)
    Path(out/"pipeline_16_phases.json").write_text(json.dumps({"organization":org,"mode":mode,"phases":PHASES,"footer":FOOTER}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok":True,"output":str(out),"mode":mode,"files":9,"systems":len(systems),"footer":FOOTER}, ensure_ascii=False))
if __name__ == "__main__": main()
