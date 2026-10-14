from fastapi import APIRouter, Depends, Query

from app.schemas import MensajeOut
from app.security import usuario_actual
from app.services import historial

router = APIRouter(tags=["historial"])


@router.get("/historial", response_model=list[MensajeOut])
def listar_historial(
    limite: int = Query(50, ge=1, le=200),
    usuario: dict = Depends(usuario_actual),
):
    return historial.listar(usuario["id"], limite)