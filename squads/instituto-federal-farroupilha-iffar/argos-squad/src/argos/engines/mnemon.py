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
        CREATE TABLE IF NOT EXISTS versoes(id_canonico TEXT, hash_conteudo TEXT, texto TEXT, fonte TEXT, url_original TEXT, capturado_em TEXT, PRIMARY KEY(id_canonico, hash_conteudo));
        CREATE TABLE IF NOT EXISTS retificacoes(id_canonico TEXT, hash_anterior TEXT, hash_novo TEXT, detectada_em TEXT, PRIMARY KEY(id_canonico, hash_anterior, hash_novo));
        ''')
        self.conn.commit()
    def registrar_publicacao(self, pub: PublicacaoNormalizada, agora: str | None = None) -> str:
        now = agora or datetime.now(timezone.utc).isoformat()
        row = self.conn.execute("SELECT hash_conteudo FROM publicacoes WHERE id_canonico=?", (pub.id_canonico,)).fetchone()
        if row is None:
            self.conn.execute("INSERT INTO publicacoes VALUES (?, ?, ?, ?)", (pub.id_canonico, pub.hash_conteudo, now, now))
            status = "nova"
        elif row[0] != pub.hash_conteudo:
            self.conn.execute("UPDATE publicacoes SET hash_conteudo=?, ultima_vez_em=? WHERE id_canonico=?", (pub.hash_conteudo, now, pub.id_canonico))
            self.conn.execute("INSERT OR IGNORE INTO retificacoes VALUES (?, ?, ?, ?)", (pub.id_canonico, row[0], pub.hash_conteudo, now))
            status = "retificacao"
        else:
            self.conn.execute("UPDATE publicacoes SET ultima_vez_em=? WHERE id_canonico=?", (now, pub.id_canonico))
            status = "reprocessada"
        self.conn.execute("INSERT OR IGNORE INTO versoes VALUES (?, ?, ?, ?, ?, ?)", (pub.id_canonico, pub.hash_conteudo, pub.texto, pub.fonte, str(pub.url_original), now))
        self.conn.commit()
        return status
    def texto_versao(self, id_canonico: str, hash_conteudo: str) -> str | None:
        row = self.conn.execute("SELECT texto FROM versoes WHERE id_canonico=? AND hash_conteudo=?", (id_canonico, hash_conteudo)).fetchone()
        return row[0] if row else None
    def listar_retificacoes(self) -> list[dict]:
        rows = self.conn.execute("SELECT r.id_canonico, r.hash_anterior, r.hash_novo, r.detectada_em, v.fonte, v.url_original FROM retificacoes r LEFT JOIN versoes v ON v.id_canonico = r.id_canonico AND v.hash_conteudo = r.hash_novo ORDER BY r.detectada_em, r.id_canonico").fetchall()
        return [{"id_canonico": r[0], "hash_anterior": r[1], "hash_novo": r[2], "detectada_em": r[3], "fonte": r[4], "url_original": r[5]} for r in rows]
    def total_publicacoes(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM publicacoes").fetchone()[0]
