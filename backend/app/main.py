from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.controllers import documentos as documentos_ctrl
from app.controllers import historial as historial_ctrl
from app.controllers import preguntas
from app.services import documentos, historial


@asynccontextmanager
async def lifespan(app: FastAPI):
    historial.iniciar_db()
    documentos.iniciar_db()
    yield


app = FastAPI(title="Agente del Espacio", version="0.1.0", lifespan=lifespan)
app.include_router(preguntas.router)
app.include_router(historial_ctrl.router)
app.include_router(documentos_ctrl.router)


@app.get("/salud")
def salud():
    return {"estado": "ok"}