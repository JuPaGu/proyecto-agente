from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import config
from app.controllers import documentos as documentos_ctrl
from app.controllers import historial as historial_ctrl
from app.controllers import preguntas
from app.security import usuario_actual
from app.services import documentos, historial


@asynccontextmanager
async def lifespan(app: FastAPI):
    historial.iniciar_db()
    documentos.iniciar_db()
    yield


app = FastAPI(
    title="Agente del Espacio",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if config.ENABLE_DOCS else None,
    redoc_url=None,
    openapi_url="/openapi.json" if config.ENABLE_DOCS else None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(preguntas.router)
app.include_router(historial_ctrl.router)
app.include_router(documentos_ctrl.router)


@app.get("/salud")
def salud(usuario: dict = Depends(usuario_actual)):
    return {"estado": "ok"}