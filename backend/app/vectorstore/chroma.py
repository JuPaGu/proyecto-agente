from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

CHROMA_DIR = Path(__file__).resolve().parents[2] / "chroma_data"

db = Chroma(
    collection_name="espacio",
    embedding_function=OllamaEmbeddings(model="bge-m3"),
    persist_directory=str(CHROMA_DIR),
    collection_metadata={"hnsw:space": "cosine"},
)