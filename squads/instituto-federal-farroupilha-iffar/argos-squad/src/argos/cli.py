from __future__ import annotations
import argparse, json
from datetime import date
from pathlib import Path
from argos.assistant_research import run_assisted_research
from argos.engines.mnemon import Mnemon
from argos.graph import ArgosPipeline, load_profile
from argos.ophthalmoi.registry import build_adapter, roster
from argos.panoptes.ledger import LivroPanoptes
from argos.panoptes.painel import gerar_painel
from argos.panoptes.retificacao import relatorio_retificacoes

def project_root() -> Path:
    p = Path.cwd()
    return p if (p / "perfis").exists() and (p / "src" / "argos").exists() else Path(__file__).resolve().parents[2]

def profile_path(root: Path, name: str) -> Path:
    path = Path(name)
    if path.exists():
        return path
    candidate = root / "perfis" / (name if name.endswith(".yaml") else f"{name}.yaml")
    if not candidate.exists():
        raise SystemExit(f"Perfil não encontrado: {name}")
    return candidate

def cmd_fontes(args) -> int:
    root = project_root()
    if args.sub == "listar":
        for codigo in roster():
            status = build_adapter(codigo, fixture_root=root / "tests" / "fixtures" if args.fixture else None).healthcheck()
            print(f"{codigo}\t{status.estado}\t{status.mensagem}")
        return 0
    status = build_adapter(args.codigo, fixture_root=root / "tests" / "fixtures" if args.fixture else None).healthcheck()
    ficha = root / "docs" / "homologacao" / f"FICHA-{args.codigo}.md"
    print(json.dumps({"codigo": args.codigo, "gate_tecnico": status.model_dump(mode='json'), "ficha": str(ficha), "homologacao_humana_obrigatoria": args.codigo.startswith('DOE-')}, ensure_ascii=False, indent=2))
    return 0

def cmd_perfil(args) -> int:
    print(load_profile(profile_path(project_root(), args.nome)).model_dump_json(indent=2))
    return 0

def cmd_buscar(args) -> int:
    root = project_root()
    composed = ArgosPipeline(root).run(profile_path(root, args.perfil), date.fromisoformat(args.data), output_dir=args.output_dir, fixture=args.fixture, hitl=args.hitl, verificar_urls=args.verify_urls)
    print(composed.model_dump_json(indent=2))
    return 0

def cmd_relatorio(args) -> int:
    latest = project_root() / ".argos" / "latest_run.json"
    if not latest.exists():
        raise SystemExit("Nenhum relatório encontrado")
    data = json.loads(latest.read_text(encoding="utf-8"))
    print(data["markdown_path"] if args.sub == "abrir" else json.dumps(data, ensure_ascii=False, indent=2))
    return 0

def cmd_dlq(args) -> int:
    dlq = project_root() / ".argos" / "dlq"
    if args.sub == "listar":
        for item in sorted(dlq.glob("*.json")) if dlq.exists() else []:
            print(item)
        return 0
    print("Reprocessamento DLQ exige revisão humana do payload SACP.")
    return 1

def cmd_panoptes(args) -> int:
    livro = LivroPanoptes(project_root() / ".argos")
    if args.sub == "verificar":
        veredito = livro.verificar()
        print(json.dumps(veredito, ensure_ascii=False, indent=2))
        return 0 if veredito["integro"] else 1
    if args.sub == "livro":
        for ent in livro.entradas():
            print(f"#{ent['seq']}\t{ent['selado_em'][:19]}\t{ent['run_id']}\tselo {ent['selo'][:16]}…\tretificações: {len(ent.get('retificacoes', []))}")
        return 0
    print(gerar_painel(project_root(), args.output))
    return 0

def cmd_retificacoes(args) -> int:
    mnemon = Mnemon(project_root() / ".argos" / "mnemon.sqlite")
    dossies = relatorio_retificacoes(mnemon)
    if args.sub == "diff":
        dossies = [d for d in dossies if d["id_canonico"] == args.id]
        if not dossies:
            raise SystemExit(f"Nenhuma retificação registrada para: {args.id}")
    print(json.dumps(dossies, ensure_ascii=False, indent=2))
    return 0

def cmd_pesquisar(args) -> int:
    root = project_root()
    municipio_ids = [x.strip() for x in (args.municipio or "").split(",") if x.strip()]
    ufs = [x.strip().upper() for x in (args.ufs or "").split(",") if x.strip()]
    result = run_assisted_research(root, args.assunto, municipio_ids=municipio_ids, ufs=ufs or None, size=args.size, check_states=not args.no_check_states)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="argos")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_fontes = sub.add_parser("fontes"); s = p_fontes.add_subparsers(dest="sub", required=True)
    p = s.add_parser("listar"); p.add_argument("--fixture", action="store_true")
    p = s.add_parser("homologar"); p.add_argument("codigo"); p.add_argument("--fixture", action="store_true")
    p_fontes.set_defaults(func=cmd_fontes)
    p_perfil = sub.add_parser("perfil"); s = p_perfil.add_subparsers(dest="sub", required=True); p = s.add_parser("validar"); p.add_argument("nome"); p_perfil.set_defaults(func=cmd_perfil)
    p_buscar = sub.add_parser("buscar"); p_buscar.add_argument("--perfil", required=True); p_buscar.add_argument("--data", required=True); p_buscar.add_argument("--hitl", action="store_true"); p_buscar.add_argument("--fixture", action="store_true"); p_buscar.add_argument("--verify-urls", action="store_true"); p_buscar.add_argument("--output-dir"); p_buscar.set_defaults(func=cmd_buscar)
    p_rel = sub.add_parser("relatorio"); s = p_rel.add_subparsers(dest="sub", required=True); s.add_parser("abrir"); s.add_parser("ultimo"); p_rel.set_defaults(func=cmd_relatorio)
    p_dlq = sub.add_parser("dlq"); s = p_dlq.add_subparsers(dest="sub", required=True); s.add_parser("listar"); p = s.add_parser("reprocessar"); p.add_argument("id"); p_dlq.set_defaults(func=cmd_dlq)
    p_pesq = sub.add_parser("pesquisar"); p_pesq.add_argument("--assunto", required=True); p_pesq.add_argument("--municipio", help="IDs IBGE separados por vírgula, ex.: 4305207"); p_pesq.add_argument("--ufs", help="UFs separadas por vírgula; omita para todas"); p_pesq.add_argument("--size", type=int, default=10); p_pesq.add_argument("--no-check-states", action="store_true"); p_pesq.set_defaults(func=cmd_pesquisar)
    p_pan = sub.add_parser("panoptes"); s = p_pan.add_subparsers(dest="sub", required=True); s.add_parser("verificar"); s.add_parser("livro"); p = s.add_parser("painel"); p.add_argument("--output"); p_pan.set_defaults(func=cmd_panoptes)
    p_ret = sub.add_parser("retificacoes"); s = p_ret.add_subparsers(dest="sub", required=True); s.add_parser("listar"); p = s.add_parser("diff"); p.add_argument("id"); p_ret.set_defaults(func=cmd_retificacoes)
    p_replay = sub.add_parser("replay"); p_replay.add_argument("run_id"); p_replay.set_defaults(func=lambda args: (print("Replay determinístico exige corpus_hash/perfil_hash armazenados em .argos/runs; use o JSON do relatório."), 0)[1])
    args = parser.parse_args(argv)
    return args.func(args)
if __name__ == "__main__":
    raise SystemExit(main())
