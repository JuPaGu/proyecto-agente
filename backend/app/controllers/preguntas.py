import logging

from fastapi import APIRouter, Depends, HTTPException

from app.security import usuario_actual

from app.agents.grafo import agente
from app.schemas import PreguntaIn, RespuestaOut

logger = logging.getLogger(__name__)
router = APIRouter(tags=["agente"])


@router.post("/preguntar", response_model=RespuestaOut)
def preguntar(datos: PreguntaIn, usuario: dict = Depends(usuario_actual)):
    try:
        r = agente.invoke({"pregunta": datos.pregunta, "usuario_id": usuario["id"]})
    except Exception:
        logger.exception("Falló el agente")
        raise HTTPException(
            status_code=503, detail="El agente no está disponible en este momento."
        )
    return RespuestaOut(
        respuesta=r["respuesta"],
        decision=r["decision"],
        distancia=r["mejor_distancia"],
        fuentes=r["fuentes"],
    )