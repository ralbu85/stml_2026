"""W7 — 검색기 📦 (최종 앱의 심장): 청킹 → 임베딩 → 코사인 top-k.

기본 임베딩은 hash_embed(문자 n-gram 해싱) — 오프라인·의존성 0으로 배관을
검증하기 위한 것이다. 의미 검색 품질이 필요하면 embed_fn에 임베딩 API
(OpenAI embeddings, sentence-transformers 등)를 주입하라. 배관은 동일하다.
"""

from __future__ import annotations

import zlib

import numpy as np


def chunk_text(text: str, size: int = 400, overlap: int = 80) -> list[str]:
    """문자 기준 슬라이딩 윈도 청킹. (제공됨 — 크기·오버랩이 현장 노트의 그 다이얼)"""
    chunks = []
    step = max(1, size - overlap)
    for i in range(0, max(1, len(text)), step):
        piece = text[i:i + size].strip()
        if piece:
            chunks.append(piece)
        if i + size >= len(text):
            break
    return chunks


def hash_embed(text: str, dim: int = 256) -> np.ndarray:
    """문자 2·3-gram 해싱 임베딩 (제공됨). 정규화된 dim차원 벡터."""
    v = np.zeros(dim)
    t = text.lower()
    for n in (2, 3):
        for i in range(len(t) - n + 1):
            v[zlib.crc32(t[i:i + n].encode()) % dim] += 1.0
    norm = np.linalg.norm(v)
    return v / norm if norm else v


def cosine_topk(query_vec: np.ndarray, doc_vecs: np.ndarray, k: int = 3) -> list[int]:
    """코사인 유사도 상위 k개의 **인덱스**를 유사도 내림차순으로 반환한다.

    doc_vecs: (N, D) 행렬. 학기 유일의 수식이 이 함수다:
        cos(q, d) = q·d / (|q||d|)

    TODO(W7): 4~6줄.
      힌트: 분모 0 방지엔 아주 작은 수(1e-9)를 더한다. np.argsort(-sims)[:k].
    """
    raise NotImplementedError("TODO(W7): cosine_topk() 를 구현하세요")


class Retriever:
    """문서를 넣고(build) 질문으로 청크를 찾는(query) 검색기."""

    def __init__(self, embed_fn=None):
        self.embed_fn = embed_fn or hash_embed
        self.chunks: list[str] = []
        self.vecs = None

    def add(self, text: str) -> None:
        """문서 하나를 청킹해 담는다. (제공됨)"""
        self.chunks.extend(chunk_text(text))

    def build(self) -> None:
        """담긴 청크 전부를 임베딩한다 — 인덱싱 단계. (제공됨)"""
        self.vecs = np.stack([self.embed_fn(c) for c in self.chunks])

    def query(self, question: str, k: int = 3) -> list[str]:
        """질문과 가장 가까운 청크 k개를 반환한다 — 질의 단계.

        TODO(W7): 2~3줄. 질문을 임베딩 → cosine_topk → 해당 청크 리스트.
        """
        raise NotImplementedError("TODO(W7): Retriever.query() 를 구현하세요")
