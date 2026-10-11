import shutil
import time
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE = Path(__file__).resolve().parent.parent
CORPUS = BASE / "corpus"
CHROMA_DIR = BASE / "chroma_data"

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)


def leer_archivo(path):
    """Separa la cabecera (TÍTULO/FUENTE/LICENCIA) del cuerpo del texto."""
    cabecera, _, cuerpo = path.read_text(encoding="utf-8").partition("\n\n")
    datos = dict(l.split(": ", 1) for l in cabecera.splitlines() if ": " in l)
    return datos.get("TÍTULO", path.stem), datos.get("FUENTE", ""), cuerpo


def main():
    # Reconstrucción completa: borramos la base anterior para no duplicar fragmentos.
    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)

    docs = []
    for path in sorted(CORPUS.glob("*.txt")):
        titulo, fuente, cuerpo = leer_archivo(path)
        for i, trozo in enumerate(splitter.split_text(cuerpo)):
            docs.append(Document(
                page_content=trozo,
                metadata={"titulo": titulo, "fuente": fuente,
                          "archivo": path.name, "chunk": i},
            ))
    print(f"{len(docs)} fragmentos de {len(list(CORPUS.glob('*.txt')))} documentos")

    embeddings = OllamaEmbeddings(model="bge-m3")
    db = Chroma(
        collection_name="espacio",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_metadata={"hnsw:space": "cosine"},
    )

    inicio = time.time()
    lote = 50
    for i in range(0, len(docs), lote):
        db.add_documents(docs[i:i + lote])
        print(f"  {min(i + lote, len(docs))}/{len(docs)}  ({time.time() - inicio:.0f}s)")
    print("Listo.")


if __name__ == "__main__":
    main()