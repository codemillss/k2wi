"""Chroma 벡터스토어 – 최초 1회만 임베딩을 생성하고,
이후에는 디스크‑캐시와 프로세스 전역 LRU 캐시를 재사용한다."""
import json
from functools import lru_cache
from typing import List
from pathlib import Path

from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma

from .config import CHROMA_DIR, DATA_JSONL, EMBEDDINGS


@lru_cache(maxsize=1)
def load_chroma() -> Chroma:
    """Return a *singleton* Chroma instance.

    Workflow:
    1. **이미 존재하는** `CHROMA_DIR` 이 있으면 → 그대로 로드 (임베딩 계산 X)
    2. 디렉터리가 없으면 → JSONL → 임베딩 생성 → `persist()` → 반환
    3. 이후 동일 프로세스 내 호출은 LRU 캐시로 즉시 반환 (RAM 복사 X)
    """
    # ── 1. 디스크에 벡터 스토어가 있으면 바로 로드 ──────────────────────────
    if CHROMA_DIR.exists():
        return Chroma(persist_directory=str(CHROMA_DIR), embedding_function=EMBEDDINGS)

    # ── 2. 최초 1회: 문서 → 임베딩 → Chroma 생성 & 저장 ─────────────────────
    docs: List[Document] = []
    with DATA_JSONL.open("r", encoding="utf-8") as f:
        for line in f:
            j = json.loads(line)
            docs.append(Document(page_content=j["text"]))

    db = Chroma.from_documents(docs, EMBEDDINGS, persist_directory=str(CHROMA_DIR))
    db.persist()  # 디스크 저장 (다음 실행부턴 바로 로드)
    return db