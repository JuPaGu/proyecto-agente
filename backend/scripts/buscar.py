import sys
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

pregunta = " ".join(sys.argv[1:])
for doc, distancia in db.similarity_search_with_score(pregunta, k=4):
    print(f"\n[distancia {distancia:.3f}] {doc.metadata['titulo']} (chunk {doc.metadata['chunk']})")
    print(doc.page_content[:200].replace("\n", " "), "...")
    