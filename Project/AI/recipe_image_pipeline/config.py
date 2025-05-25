from pathlib import Path
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama

# LLM models
LLM_STAGE0 = Ollama(model="gemma3:12b")  # Stage‑0
LLM_STAGE2 = Ollama(model="gemma3:12b")   # Stage‑2 (swap to 4b if 필요)

# RAG / Chroma paths
DATA_JSONL = Path("./data/rag_korean_cooking.jsonl")
CHROMA_DIR = Path("./chroma_bge")

# Embedding model
EMBEDDINGS = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": True},
)