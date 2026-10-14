import sqlite3
from contextlib import closing

from app.services.historial import DB_PATH


def _conectar():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def iniciar_db():
    with closing(_conectar()) as conn, conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS documentos (
                id TEXT PRIMARY KEY,
                usuario_id TEXT NOT NULL,
                nombre TEXT NOT NULL,
                sha256 TEXT NOT NULL UNIQUE,
                n_fragmentos INTEGER NOT NULL,
                creado_en TEXT NOT NULL DEFAULT (datetime('now'))
            )"""
        )


def existe_huella(huella):
    with closing(_conectar()) as conn:
        return conn.execute(
            "SELECT 1 FROM documentos WHERE sha256 = ?", (huella,)
        ).fetchone() is not None


def crear(doc_id, usuario_id, nombre, huella, n_fragmentos):
    with closing(_conectar()) as conn, conn:
        conn.execute(
            "INSERT INTO documentos (id, usuario_id, nombre, sha256, n_fragmentos) "
            "VALUES (?, ?, ?, ?, ?)",
            (doc_id, usuario_id, nombre, huella, n_fragmentos),
        )


def listar(usuario_id):
    with closing(_conectar()) as conn:
        filas = conn.execute(
            "SELECT id, nombre, n_fragmentos, creado_en, usuario_id "
            "FROM documentos ORDER BY creado_en DESC"
        ).fetchall()
    return [
        {"id": f["id"], "nombre": f["nombre"], "n_fragmentos": f["n_fragmentos"],
         "creado_en": f["creado_en"], "propio": f["usuario_id"] == usuario_id}
        for f in filas
    ]


def obtener(doc_id):
    with closing(_conectar()) as conn:
        fila = conn.execute("SELECT * FROM documentos WHERE id = ?", (doc_id,)).fetchone()
    return dict(fila) if fila else None


def borrar(doc_id):
    with closing(_conectar()) as conn, conn:
        conn.execute("DELETE FROM documentos WHERE id = ?", (doc_id,))