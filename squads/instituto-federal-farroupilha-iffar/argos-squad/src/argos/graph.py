from __future__ import annotations
import hashlib, json
from datetime import date, timedelta
from pathlib import Path
from uuid import uuid4
import yaml
from argos.contracts import PerfilInteresse
from argos.engines.kanon_lex import filtrar_publicacoes
from argos.engines.mnemon import Mnemon
from argos.engines.statista import agregar
from argos.minds.elenchus import revisar
from argos.minds.hegemon import rotear
from argos.minds.krites import classificar
from argos.minds.laconicus import sintetizar
from argos.ophthalmoi.registry import build_adapter
from argos.report.compose import compose_report

def _hash_obj(obj) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()

def load_profile(path: str | Path) -> PerfilInteresse:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return PerfilInteresse.model_validate(data.get("perfil", data))

def janela_datas(data_ref: date, janela: str) -> tuple[date, date]:
    if janela == "SEMANA":
        return data_ref - timedelta(days=6), data_ref
    if janela == "MES":
        return data_ref - timedelta(days=29), data_ref
    return data_ref, data_ref

class ArgosPipeline:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.runtime = self.root / ".argos"
        self.mnemon = Mnemon(self.runtime / "mnemon.sqlite")
    def run(self, profile_path: str | Path, data_ref: date, output_dir: str | Path | None = None, fixture: bool = False, hitl: bool = False, verificar_urls: bool = False):
        perfil = load_profile(profile_path)
        inicio, fim = janela_datas(data_ref, perfil.janela)
        fixture_root = self.root / "tests" / "fixtures" if fixture else None
        roteamento = rotear(perfil, hitl=hitl)
        publicacoes = []
        fontes_consultadas = []
        fontes_lacuna = []
        lacunas = []
        for fonte in perfil.fontes:
            try:
                adapter = build_adapter(fonte, fixture_root=fixture_root)
                status = adapter.healthcheck()
                if status.estado not in {"ok", "observacao"}:
                    fontes_lacuna.append(fonte)
                    lacunas.append(f"{fonte}: {status.estado} — {status.mensagem}")
                    continue
                fontes_consultadas.append(fonte)
                for ref in adapter.listar_edicoes(inicio, fim):
                    for pub in adapter.obter_publicacoes(ref):
                        self.mnemon.registrar_publicacao(pub)
                        publicacoes.append(pub)
            except Exception as exc:
                fontes_lacuna.append(fonte)
                lacunas.append(f"{fonte}: falha controlada — {exc}")
        corpus_hash = _hash_obj([p.model_dump(mode='json') for p in publicacoes])
        perfil_hash = _hash_obj(perfil.model_dump(mode='json'))
        candidatos = filtrar_publicacoes(perfil, publicacoes)
        classificacoes = classificar(perfil, candidatos)
        sinteses = sintetizar(candidatos)
        veredito = revisar(candidatos, classificacoes, verificar_urls=verificar_urls)
        if not veredito.aprovado:
            dlq = self.runtime / "dlq"
            dlq.mkdir(parents=True, exist_ok=True)
            (dlq / f"{uuid4().hex}.json").write_text(veredito.model_dump_json(indent=2), encoding="utf-8")
            classificacoes = [c for c in classificacoes if c.id_canonico not in veredito.itens_reprovados]
            sinteses = [s for s in sinteses if s.id_canonico not in veredito.itens_reprovados]
            lacunas.append(f"Gate 2 reprovou {len(veredito.itens_reprovados)} item(ns); payload enviado à DLQ.")
        estatisticas = agregar(candidatos, classificacoes)
        run_id = f"argos-{data_ref.isoformat()}-{uuid4().hex[:8]}"
        run = {"run_id": run_id, "perfil_nome": perfil.nome, "roteamento": roteamento.model_dump(mode='json'), "corpus_hash": corpus_hash, "perfil_hash": perfil_hash, "inicio": inicio.isoformat(), "fim": fim.isoformat(), "fontes_consultadas": fontes_consultadas, "fontes_lacuna": fontes_lacuna, "lacunas": lacunas}
        composed = compose_report(run, candidatos, classificacoes, sinteses, estatisticas, Path(output_dir) if output_dir else self.runtime / "runs")
        latest = self.runtime / "latest_run.json"
        latest.parent.mkdir(parents=True, exist_ok=True)
        latest.write_text(composed.model_dump_json(indent=2), encoding="utf-8")
        return composed
