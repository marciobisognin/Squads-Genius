from __future__ import annotations
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from argos.contracts import PublicacaoNormalizada

class Mnemon:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.init()
    def init(self) -> None:
        self.conn.executescript('''
        CREATE TABLE IF NOT EXISTS edicoes_processadas(fonte TEXT, secao TEXT, data TEXT, edicao TEXT, hash_zip TEXT, processado_em TEXT, PRIMARY KEY(fonte, secao, data, edicao));
        CREATE TABLE IF NOT EXISTS publicacoes(id_canonico TEXT PRIMARY KEY, hash_conteudo TEXT, primeira_vez_em TEXT, ultima_vez_em TEXT);
        ''')
        self.conn.commit()
    def registrar_publicacao(self, pub: PublicacaoNormalizada) -> str:
        now = datetime.now(timezone.utc).isoformat()
        row = self.conn.execute("SELECT hash_conteudo FROM publicacoes WHERE id_canonico=?", (pub.id_canonico,)).fetchone()
        if row is None:
            self.conn.execute("INSERT INTO publicacoes VALUES (?, ?, ?, ?)", (pub.id_canonico, pub.hash_conteudo, now, now))
            status = "nova"
        elif row[0] != pub.hash_conteudo:
            self.conn.execute("UPDATE publicacoes SET hash_conteudo=?, ultima_vez_em=? WHERE id_canonico=?", (pub.hash_conteudo, now, pub.id_canonico))
            status = "retificacao"
        else:
            self.conn.execute("UPDATE publicacoes SET ultima_vez_em=? WHERE id_canonico=?", (now, pub.id_canonico))
            status = "reprocessada"
        self.conn.commit()
        return status
