from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from app import config

CHROMA_DIR = Path(__file__).resolve().parents[2] / "chroma_data"

db = Chroma(
    collection_name="espacio",
    embedding_function=OllamaEmbeddings(model="bge-m3", base_url=config.OLLAMA_BASE_URL),
    persist_directory=str(CHROMA_DIR),
    collection_metadata={"hnsw:space": "cosine"},
)