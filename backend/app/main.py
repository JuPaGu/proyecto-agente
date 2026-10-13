from fastapi import FastAPI

from app.controllers import preguntas

app = FastAPI(title="Agente del Espacio", version="0.1.0")
app.include_router(preguntas.router)


@app.get("/salud")
def salud():
    return {"estado": "ok"}