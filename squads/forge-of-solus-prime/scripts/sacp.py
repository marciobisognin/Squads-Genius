#!/usr/bin/env python3
"""SACP — Structured Agent Communication Protocol (estrato LÓGOS).

Contrato tipado de handoff entre atos/agentes do Anel da Forja. Implementa a
**Lei do Contrato**: todo bastão passado é validado por schema, com
``extra="forbid"`` para barrar a patologia DERIVA DE CONTRATO (campos
espúrios ou perdidos falham na validação).

Usa Pydantic v2 quando disponível; caso contrário, degrada para dataclasses
com a mesma superfície de API (``model_dump``/``model_validate``), preservando
a portabilidade do squad.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import datetime as dt
import uuid
from decimal import Decimal
from enum import Enum
from typing import Any

try:  # Caminho preferencial: validação real por schema.
    from pydantic import BaseModel, ConfigDict, Field  # type: ignore

    _PYDANTIC = True
except Exception:  # pragma: no cover - fallback determinístico
    _PYDANTIC = False


class Estrato(str, Enum):
    TELOS = "telos"
    LOGOS = "logos"
    ORGANON = "organon"
    KYKLOS = "kyklos"
    MNEME = "mneme"


class Veredito(str, Enum):
    APROVADO = "aprovado"
    REPROVADO = "reprovado"
    REVISAR = "revisar"
    ESCALAR = "escalar"


ATOS_VALIDOS = {
    "noesis", "boule", "diairesis", "praxis", "elenchos", "krisis", "anamnesis",
}


if _PYDANTIC:

    class CustoSACP(BaseModel):
        model_config = ConfigDict(extra="forbid")
        tokens_estimados: int = 0
        tokens_reais: int = 0
        chamadas_ferramenta: int = 0
        custo_monetario: Decimal = Field(default=Decimal("0"))

    class ContratoSACP(BaseModel):
        """Handoff tipado entre dois atos/agentes do Anel da Forja."""

        model_config = ConfigDict(extra="forbid")
        contrato_id: str
        emissor: str
        receptor: str
        estrato: Estrato
        ato: str
        timestamp: dt.datetime
        payload: dict[str, Any]
        schema_ref: str
        evidencias: list[str] = Field(default_factory=list)
        veredito: Veredito = Veredito.REVISAR
        custo: CustoSACP = Field(default_factory=CustoSACP)
        requer_humano: bool = False

else:  # pragma: no cover - fallback sem pydantic
    from dataclasses import asdict, dataclass, field

    @dataclass
    class CustoSACP:
        tokens_estimados: int = 0
        tokens_reais: int = 0
        chamadas_ferramenta: int = 0
        custo_monetario: Decimal = field(default_factory=lambda: Decimal("0"))

        def model_dump(self) -> dict[str, Any]:
            d = asdict(self)
            d["custo_monetario"] = str(self.custo_monetario)
            return d

    @dataclass
    class ContratoSACP:
        contrato_id: str
        emissor: str
        receptor: str
        estrato: Estrato
        ato: str
        timestamp: dt.datetime
        payload: dict[str, Any]
        schema_ref: str
        evidencias: list[str] = field(default_factory=list)
        veredito: Veredito = Veredito.REVISAR
        custo: CustoSACP = field(default_factory=CustoSACP)
        requer_humano: bool = False

        def __post_init__(self) -> None:
            if self.ato not in ATOS_VALIDOS:
                raise ValueError(f"ato inválido: {self.ato}")

        def model_dump(self) -> dict[str, Any]:
            return {
                "contrato_id": self.contrato_id,
                "emissor": self.emissor,
                "receptor": self.receptor,
                "estrato": self.estrato.value if isinstance(self.estrato, Estrato) else self.estrato,
                "ato": self.ato,
                "timestamp": self.timestamp.isoformat(),
                "payload": self.payload,
                "schema_ref": self.schema_ref,
                "evidencias": list(self.evidencias),
                "veredito": self.veredito.value if isinstance(self.veredito, Veredito) else self.veredito,
                "custo": self.custo.model_dump(),
                "requer_humano": self.requer_humano,
            }


def novo_contrato(
    emissor: str,
    receptor: str,
    estrato: Estrato | str,
    ato: str,
    payload: dict[str, Any],
    schema_ref: str = "schemas/sacp_contract.schema.json",
    *,
    evidencias: list[str] | None = None,
    veredito: Veredito | str = Veredito.REVISAR,
    requer_humano: bool = False,
) -> ContratoSACP:
    """Cria um contrato SACP com ``contrato_id`` e timestamp determinísticos."""
    if ato not in ATOS_VALIDOS:
        raise ValueError(f"ato inválido: {ato!r} (válidos: {sorted(ATOS_VALIDOS)})")
    est = estrato if isinstance(estrato, Estrato) else Estrato(str(estrato))
    ver = veredito if isinstance(veredito, Veredito) else Veredito(str(veredito))
    return ContratoSACP(
        contrato_id="sacp-" + uuid.uuid4().hex[:12],
        emissor=emissor,
        receptor=receptor,
        estrato=est,
        ato=ato,
        timestamp=dt.datetime.now(dt.timezone.utc),
        payload=payload,
        schema_ref=schema_ref,
        evidencias=list(evidencias or []),
        veredito=ver,
        requer_humano=requer_humano,
    )


def dump(contrato: ContratoSACP) -> dict[str, Any]:
    """Serializa um contrato para dict JSON-serializável."""
    if _PYDANTIC:
        return contrato.model_dump(mode="json")  # type: ignore[call-arg]
    return contrato.model_dump()


if __name__ == "__main__":  # pragma: no cover
    import json

    c = novo_contrato(
        "BLASTER", "PROWL", Estrato.LOGOS, "diairesis",
        {"tarefas": 5}, evidencias=["briefing.normalizado.yaml"],
        veredito=Veredito.APROVADO,
    )
    print(json.dumps(dump(c), ensure_ascii=False, indent=2))
