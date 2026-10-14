from pydantic import BaseModel, Field


class PreguntaIn(BaseModel):
    pregunta: str = Field(min_length=3, max_length=500)


class Fuente(BaseModel):
    titulo: str
    url: str


class RespuestaOut(BaseModel):
    respuesta: str
    decision: str
    distancia: float
    fuentes: list[Fuente]

class MensajeOut(BaseModel):
    id: int
    pregunta: str
    respuesta: str
    decision: str
    fuentes: list[Fuente]
    creado_en: str