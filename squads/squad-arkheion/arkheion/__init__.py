"""ARKHEION — pipeline de dossiês visuais em vídeo (estética "arquivo confidencial").

A identidade da marca vive em código determinístico (`canon.py`), não em prompts.
O LLM apenas descreve em JSON (`schemas.py`); o código desenha e o validador (KÁNŌN)
reprova numericamente qualquer artefato fora do Cânone.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""

from . import canon  # noqa: F401

__all__ = ["canon"]
__version__ = "1.0.0"

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
