import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.agents.grafo import agente  # noqa: E402

# Preguntas NUEVAS: no las usamos para calibrar
PREGUNTAS = [
    "¿Qué diferencia hay entre una estrella de neutrones y una enana blanca?",
    "¿Qué es un púlsar?",
    "¿Cuándo aterrizó el Apolo 11 en la Luna?",
    "¿Qué es el cinturón de Kuiper?",
    "¿Qué es la energía oscura?",
    "¿Qué es el róver Curiosity?",
    "¿Cuántas lunas tiene Júpiter?",
    "¿Cuál es el planeta más grande del sistema solar?",
    "¿Qué es el telescopio Hubble?",
    "¿Cómo se forma una supernova?",
]

for p in PREGUNTAS:
    r = agente.invoke({"pregunta": p})
    print(f"\n{'=' * 70}\n{p}\n[{r['decision']} | distancia {r['mejor_distancia']:.3f}]")
    print(r["respuesta"])
    for f in r["fuentes"]:
        print(f"  - {f['titulo']}")