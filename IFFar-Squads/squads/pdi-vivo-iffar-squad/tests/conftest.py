import sys
from pathlib import Path

# Permite importar os módulos de scripts/ diretamente nos testes.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
