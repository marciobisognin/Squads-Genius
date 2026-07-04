from __future__ import annotations
from pathlib import Path

from argos.official_sources import all_source_codes, state_by_code
from argos.ophthalmoi.dou_inlabs import DOUInlabsAdapter
from argos.ophthalmoi.estadual_catalog import build_estado_adapter
from argos.ophthalmoi.querido_diario import QueridoDiarioAdapter


def build_adapter(codigo: str, fixture_root: str | Path | None = None):
    code = codigo.upper()
    if code == "DOU-INLABS":
        return DOUInlabsAdapter(fixture_dir=Path(fixture_root) / "dou_inlabs" if fixture_root else None)
    if code == "QD":
        return QueridoDiarioAdapter()
    if code.startswith("QD-"):
        return QueridoDiarioAdapter(municipio_ibge=code.split("-", 1)[1])
    if state_by_code(code):
        return build_estado_adapter(code)
    raise KeyError(f"Fonte não registrada: {codigo}")


def roster():
    return ["DOU-INLABS", "QD-4305207"] + [code for code in all_source_codes() if code.startswith("DOE-") or code == "DODF"]
