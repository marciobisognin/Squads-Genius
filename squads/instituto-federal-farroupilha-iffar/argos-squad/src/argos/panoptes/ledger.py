from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

GENESIS = hashlib.sha256(b"ARGOS-PANOPTES-GENESIS").hexdigest()

def _canonico(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)

def _selo(entrada: dict) -> str:
    corpo = {k: v for k, v in entrada.items() if k != "selo"}
    return hashlib.sha256(_canonico(corpo).encode()).hexdigest()

class LivroPanoptes:
    """Livro-razão append-only: cada run do ARGOS vira uma entrada selada e encadeada.

    O selo de cada entrada cobre o selo da anterior, então qualquer alteração
    retroativa quebra a cadeia inteira — verificável offline, sem servidor.
    """
    def __init__(self, runtime_dir: str | Path):
        self.path = Path(runtime_dir) / "panoptes" / "livro.jsonl"
    def entradas(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
    def selar(self, registro: dict, selado_em: str | None = None) -> dict:
        entradas = self.entradas()
        entrada = {
            "seq": len(entradas) + 1,
            "selado_em": selado_em or datetime.now(timezone.utc).isoformat(),
            "anterior": entradas[-1]["selo"] if entradas else GENESIS,
            **registro,
        }
        entrada["selo"] = _selo(entrada)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(_canonico(entrada) + "\n")
        return entrada
    def verificar(self) -> dict:
        entradas = self.entradas()
        anterior = GENESIS
        for entrada in entradas:
            if entrada.get("anterior") != anterior:
                return {"integro": False, "total": len(entradas), "quebra_seq": entrada.get("seq"), "motivo": "elo 'anterior' não corresponde ao selo da entrada precedente"}
            if entrada.get("selo") != _selo(entrada):
                return {"integro": False, "total": len(entradas), "quebra_seq": entrada.get("seq"), "motivo": "selo não confere com o conteúdo da entrada (registro adulterado)"}
            anterior = entrada["selo"]
        return {"integro": True, "total": len(entradas), "quebra_seq": None, "motivo": "cadeia íntegra do gênesis ao último selo"}
