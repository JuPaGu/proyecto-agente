from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

CHROMA_DIR = Path(__file__).resolve().parent.parent / "chroma_data"

db = Chroma(
    collection_name="espacio",
    embedding_function=OllamaEmbeddings(model="bge-m3"),
    persist_directory=str(CHROMA_DIR),
    collection_metadata={"hnsw:space": "cosine"},
)

PREGUNTAS = {
    "EN CORPUS": [
        "¿Qué es un agujero negro?",
        "¿Quién fue el primer hombre en la Luna?",
        "¿Cuántos planetas tiene el sistema solar?",
        "¿Qué es la materia oscura?",
        "¿Para qué sirve el telescopio James Webb?",
        "¿Qué fue el programa Apolo?",
        "¿Qué es la paradoja de Fermi?",
        "¿Qué pasó con la sonda Voyager 1?",
    ],
    "FUERA DE TEMA": [
        "receta de sushi",
        "¿Quién ganó el último mundial de fútbol?",
        "¿Cómo se hace una base de datos en SQL?",
        "¿Cuál es la capital de Colombia?",
    ],
    "ESPACIO PERO NO EN CORPUS": [
        "¿Qué es el róver Curiosity?",
        "¿Quién es Elon Musk?",
        "¿Cómo funciona el cohete Starship de SpaceX?",
        "¿Cuándo será el próximo eclipse solar?",
    ],
}

for grupo, preguntas in PREGUNTAS.items():
    print(f"\n=== {grupo} ===")
    for p in preguntas:
        doc, dist = db.similarity_search_with_score(p, k=1)[0]
        print(f"{dist:.3f}  {p}  ->  {doc.metadata['titulo']}")
        