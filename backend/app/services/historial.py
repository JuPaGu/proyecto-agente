import json
import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "historial.db"


def _conectar():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def iniciar_db():
    with closing(_conectar()) as conn, conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id TEXT NOT NULL,
                pregunta TEXT NOT NULL,
                respuesta TEXT NOT NULL,
                decision TEXT NOT NULL,
                fuentes TEXT NOT NULL,
                creado_en TEXT NOT NULL DEFAULT (datetime('now'))
            )"""
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_mensajes_usuario ON mensajes(usuario_id, id)"
        )


def guardar(usuario_id, pregunta, respuesta, decision, fuentes):
    with closing(_conectar()) as conn, conn:
        conn.execute(
            "INSERT INTO mensajes (usuario_id, pregunta, respuesta, decision, fuentes) "
            "VALUES (?, ?, ?, ?, ?)",
            (usuario_id, pregunta, respuesta, decision, json.dumps(fuentes)),
        )


def listar(usuario_id, limite=50):
    with closing(_conectar()) as conn:
        filas = conn.execute(
            "SELECT id, pregunta, respuesta, decision, fuentes, creado_en "
            "FROM mensajes WHERE usuario_id = ? ORDER BY id DESC LIMIT ?",
            (usuario_id, limite),
        ).fetchall()
    return [{**dict(f), "fuentes": json.loads(f["fuentes"])} for f in filas]