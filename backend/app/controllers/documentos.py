from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.schemas import DocumentoOut, SubidaOut
from app.security import usuario_actual
from app.services import documentos, ingesta

router = APIRouter(prefix="/documentos", tags=["documentos"])


@router.post("", response_model=SubidaOut, status_code=201)
def subir(archivo: UploadFile = File(...), usuario: dict = Depends(usuario_actual)):
    contenido = archivo.file.read(ingesta.MAX_BYTES + 1)  # nunca leemos más de lo permitido
    try:
        return ingesta.procesar(usuario["id"], archivo.filename or "", contenido)
    except ingesta.ErrorDocumento as e:
        raise HTTPException(status_code=e.codigo, detail=e.mensaje)


@router.get("", response_model=list[DocumentoOut])
def listar(usuario: dict = Depends(usuario_actual)):
    return documentos.listar(usuario["id"])


@router.delete("/{doc_id}", status_code=204)
def borrar(doc_id: str, usuario: dict = Depends(usuario_actual)):
    try:
        ingesta.eliminar(usuario["id"], doc_id)
    except ingesta.ErrorDocumento as e:
        raise HTTPException(status_code=e.codigo, detail=e.mensaje)