import sys
import time
from pathlib import Path
from typing import TypedDict

from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langgraph.graph import END, START, StateGraph

CHROMA_DIR = Path(__file__).resolve().parents[2] / "chroma_data"

# Umbrales provisionales (distancia coseno: menor = más parecido)
UMBRAL_RESPONDER = 0.35
UMBRAL_RECHAZAR = 0.50
K_BUSQUEDA = 4
K_CONTEXTO = 3  # 3 fragmentos de ~1000 caracteres caben holgados en 4096 tokens

MENSAJE_RECHAZO = (
    "No tengo suficiente información en mi base de conocimiento para responder "
    "esa pregunta. Puedes subir documentos relacionados con el tema para ampliarla."
)

db = Chroma(
    collection_name="espacio",
    embedding_function=OllamaEmbeddings(model="bge-m3"),
    persist_directory=str(CHROMA_DIR),
    collection_metadata={"hnsw:space": "cosine"},
)
llm = ChatOllama(model="qwen2.5:3b", temperature=0)


class Estado(TypedDict, total=False):
    pregunta: str
    fragmentos: list[dict]
    mejor_distancia: float
    decision: str
    respuesta: str
    fuentes: list[dict]


def _formatear_contexto(fragmentos):
    return "\n\n".join(f"[{f['titulo']}]\n{f['texto']}" for f in fragmentos[:K_CONTEXTO])


def buscar(estado: Estado) -> Estado:
    resultados = db.similarity_search_with_score(estado["pregunta"], k=K_BUSQUEDA)
    fragmentos = [
        {
            "texto": doc.page_content,
            "titulo": doc.metadata["titulo"],
            "fuente": doc.metadata["fuente"],
            "distancia": dist,
        }
        for doc, dist in resultados
    ]
    return {
        "fragmentos": fragmentos,
        "mejor_distancia": min(f["distancia"] for f in fragmentos),
    }


def evaluar(estado: Estado) -> Estado:
    d = estado["mejor_distancia"]
    if d <= UMBRAL_RESPONDER:
        return {"decision": "responder"}
    if d >= UMBRAL_RECHAZAR:
        return {"decision": "rechazar"}
    # Zona gris: le preguntamos al modelo si el contexto responde la pregunta
    prompt = (
        "Eres un verificador estricto. Lee los fragmentos y la pregunta. "
        "Responde SOLO 'SI' si los fragmentos contienen la información necesaria "
        "para responder la pregunta, o SOLO 'NO' si no la contienen.\n\n"
        f"FRAGMENTOS:\n{_formatear_contexto(estado['fragmentos'])}\n\n"
        f"PREGUNTA: {estado['pregunta']}\n\nRESPUESTA (SI o NO):"
    )
    veredicto = llm.invoke(prompt).content.strip().upper()
    return {"decision": "responder" if veredicto.startswith(("SI", "SÍ")) else "rechazar"}


def generar(estado: Estado) -> Estado:
    prompt = (
        "Eres un asistente sobre astronomía y exploración espacial. Responde la "
        "pregunta usando ÚNICAMENTE la información de los fragmentos. No uses "
        "conocimiento propio. Si los fragmentos no alcanzan para responder, di "
        "exactamente: 'No tengo suficiente información en mi base de conocimiento "
        "para responder esa pregunta.' Repite solo lo que los fragmentos afirman: no conviertas comparaciones en superlativos (por ejemplo, 'tres veces más pesado que X' no significa 'el más pesado'). Responde en español, de forma clara y breve..\n\n"
        f"FRAGMENTOS:\n{_formatear_contexto(estado['fragmentos'])}\n\n"
        f"PREGUNTA: {estado['pregunta']}\n\nRESPUESTA:"
    )
    respuesta = llm.invoke(prompt).content.strip()
    if respuesta.starswith("No tengo suficiente informacion"):
        return {"decision":"rechazar","respuesta":MENSAJE_RECHAZO, "fuentes": []}
    vistos, fuentes = set(), []
    for f in estado["fragmentos"][:K_CONTEXTO]:
        if f["fuente"] not in vistos:
            vistos.add(f["fuente"])
            fuentes.append({"titulo": f["titulo"], "url": f["fuente"]})
    return {"respuesta": respuesta, "fuentes": fuentes}


def rechazar(estado: Estado) -> Estado:
    return {"respuesta": MENSAJE_RECHAZO, "fuentes": []}


def ruta_decision(estado: Estado) -> str:
    return estado["decision"]


def construir_grafo():
    g = StateGraph(Estado)
    g.add_node("buscar", buscar)
    g.add_node("evaluar", evaluar)
    g.add_node("generar", generar)
    g.add_node("rechazar", rechazar)
    g.add_edge(START, "buscar")
    g.add_edge("buscar", "evaluar")
    g.add_conditional_edges(
        "evaluar", ruta_decision, {"responder": "generar", "rechazar": "rechazar"}
    )
    g.add_edge("generar", END)
    g.add_edge("rechazar", END)
    return g.compile()


agente = construir_grafo()


if __name__ == "__main__":
    pregunta = " ".join(sys.argv[1:])
    inicio = time.time()
    r = agente.invoke({"pregunta": pregunta})
    print(f"\nDistancia: {r['mejor_distancia']:.3f} | Decisión: {r['decision']} "
          f"| {time.time() - inicio:.1f}s")
    print(f"\n{r['respuesta']}")
    for f in r["fuentes"]:
        print(f"  - {f['titulo']}: {f['url']}")