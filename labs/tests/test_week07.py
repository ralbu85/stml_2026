"""W7 오프라인 테스트 — retriever. 실행: pytest tests/test_week07.py -v"""

import numpy as np

from docqa.retriever import Retriever, chunk_text, cosine_topk


def test_chunk_overlap():
    chunks = chunk_text("a" * 1000, size=400, overlap=80)
    assert len(chunks) >= 3
    assert all(len(c) <= 400 for c in chunks)


def test_cosine_topk_orders_by_similarity():
    q = np.array([1.0, 0.0])
    docs = np.array([[0.0, 1.0],    # 직교 (유사도 0)
                     [1.0, 0.0],    # 동일 방향 (유사도 1)
                     [1.0, 1.0]])   # 45도
    assert cosine_topk(q, docs, k=2) == [1, 2]


def test_cosine_topk_ignores_magnitude():
    q = np.array([1.0, 0.0])
    docs = np.array([[100.0, 0.0], [0.9, 0.1]])
    assert cosine_topk(q, docs, k=1) == [0]  # 길이가 아니라 방향


def test_retriever_finds_relevant_chunk():
    r = Retriever()  # 기본 hash_embed — 오프라인
    r.add("ReAct는 추론과 행동을 교차시키는 프롬프트 기법이다. " * 5)
    r.add("김치찌개 레시피: 돼지고기와 묵은지를 볶는다. " * 5)
    r.build()
    top = r.query("ReAct 프롬프트 기법", k=1)
    assert "ReAct" in top[0]
