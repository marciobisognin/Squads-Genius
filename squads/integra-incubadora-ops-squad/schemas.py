# schemas.py - pydantic models for squad data structures

from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

class StartupProfile(BaseModel):
    """Dados básicos da startup submetida ao processo de triagem."""
    nome: str
    cnpj: Optional[str]
    area_atuacao: str
    cnpj_natureza_juridica: Optional[str]
    fase: Literal["captacao", "triagem", "avaliacao", "incubacao", "graduacao", "egresso"]
    score_admissao: float
    status: Literal["aprovada", "pre-incubacao", "rejeitada", "em_avaliacao"]
    data_submissao: datetime
    responsavel: str
    candidato: Optional[dict] = Field(default=None, description="Informacoes adicionais do Candidato (formacao, apoio, etc.)")
    startup: Optional[dict] = Field(default=None, description="Informacoes adicionais da Startup (prototipo, modelo, etc.)")
    class Config:
        title = "StartupProfile"

# Exemplo de uso simples validação no script.  Mais schemas podem ser adicionados
# conforme necessidade (TRLReport, LeanCanvas, MentorshipPlan, etc.)
