import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.agents.grafo import buscar, evaluar  # noqa: E402

# "?" = caso dudoso: no sé qué debería pasar, lo revisamos a mano
CASOS = [
    ("¿Qué es un agujero negro?", "responder"),
    ("que es un agujero negro", "responder"),
    ("¿Quién fue el primer hombre en la Luna?", "responder"),
    ("quien fue el primer hombre en la luna", "responder"),
    ("¿Qué es la materia oscura?", "responder"),
    ("que es la materia oscura", "responder"),
    ("¿Qué es el róver Curiosity?", "responder"),
    ("que es el rover curiosity", "responder"),
    ("¿Quién fue Yuri Gagarin?", "responder"),
    ("¿Qué es una supernova?", "responder"),
    ("¿Qué es la Estación Espacial Internacional?", "responder"),
    ("receta de sushi", "rechazar"),
    ("¿Quién ganó el último mundial de fútbol?", "rechazar"),
    ("¿Cuál es la capital de Colombia?", "rechazar"),
    ("¿Cómo se hace una base de datos en SQL?", "rechazar"),
    ("¿Quién es Elon Musk?", "rechazar"),
    ("¿Cómo funciona el cohete Starship de SpaceX?", "?"),
    ("¿Cuándo será el próximo eclipse solar?", "?"),
]

fallas = 0
for pregunta, esperado in CASOS:
    estado = {"pregunta": pregunta}
    estado.update(buscar(estado))
    estado.update(evaluar(estado))
    decision = estado["decision"]
    if esperado == "?":
        marca = "??"
    elif decision == esperado:
        marca = "OK"
    else:
        marca = "FALLA"
        fallas += 1
    print(f"{marca:<5} {estado['mejor_distancia']:.3f}  {decision:<9} (esperado: {esperado:<9}) {pregunta}")

print(f"\nFallas: {fallas}")
