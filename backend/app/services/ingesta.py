import hashlib
import io
import logging
import uuid
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from app.services import documentos
from app.vectorstore.chroma import db

logger = logging.getLogger(__name__)

EXTENSIONES = {".pdf", ".txt", ".md"}
MAX_BYTES = 5 * 1024 * 1024
MAX_FRAGMENTOS = 300
MIN_CHARS = 200  # mismo criterio que la ingesta del corpus

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)


class ErrorDocumento(Exception):
    def __init__(self, mensaje, codigo=422):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo


def extraer_texto(extension, contenido):
    if extension == ".pdf":
        try:
            lector = PdfReader(io.BytesIO(contenido))
            return "\n\n".join((p.extract_text() or "") for p in lector.pages)
        except Exception:
            raise ErrorDocumento("No se pudo leer el PDF (¿está dañado o protegido?).")
    try:
        return contenido.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ErrorDocumento("El archivo de texto debe estar codificado en UTF-8.")


def procesar(usuario_id, nombre_original, contenido):
    nombre = Path(nombre_original).name[:120] or "documento"
    extension = Path(nombre).suffix.lower()
    if extension not in EXTENSIONES:
        raise ErrorDocumento("Formato no permitido. Usa PDF, TXT o MD.", 415)
    if not contenido:
        raise ErrorDocumento("El archivo está vacío.")
    if len(contenido) > MAX_BYTES:
        raise ErrorDocumento("El archivo supera los 5 MB.", 413)

    huella = hashlib.sha256(contenido).hexdigest()
    if documentos.existe_huella(huella):
        raise ErrorDocumento("Este documento ya fue cargado.", 409)

    texto = extraer_texto(extension, contenido)
    trozos = [t for t in splitter.split_text(texto) if len(t.strip()) >= MIN_CHARS]
    if not trozos:
        raise ErrorDocumento("No se encontró texto suficiente (¿es un PDF escaneado?).")
    if len(trozos) > MAX_FRAGMENTOS:
        raise ErrorDocumento(
            f"El documento es demasiado largo ({len(trozos)} fragmentos; máximo {MAX_FRAGMENTOS}).",
            413,
        )

    doc_id = uuid.uuid4().hex
    docs = [
        Document(
            page_content=t,
            metadata={"titulo": nombre, "fuente": f"Documento subido: {nombre}",
                      "doc_id": doc_id, "chunk": i},
        )
        for i, t in enumerate(trozos)
    ]
    ids = [f"{doc_id}:{i}" for i in range(len(docs))]
    try:
        for i in range(0, len(docs), 50):
            db.add_documents(docs[i:i + 50], ids=ids[i:i + 50])
    except Exception:
        logger.exception("Falló la ingesta de %s", nombre)
        db.delete(ids=ids)  # no dejar fragmentos huérfanos
        raise ErrorDocumento("No se pudo procesar el documento. Intenta de nuevo.", 503)

    documentos.crear(doc_id, usuario_id, nombre, huella, len(docs))
    return {"id": doc_id, "nombre": nombre, "fragmentos": len(docs)}


def eliminar(usuario_id, doc_id):
    doc = documentos.obtener(doc_id)
    if doc is None or doc["usuario_id"] != usuario_id:
        raise ErrorDocumento("Documento no encontrado.", 404)
    db.delete(ids=[f"{doc_id}:{i}" for i in range(doc["n_fragmentos"])])
    documentos.borrar(doc_id)
    