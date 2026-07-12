"""W10 오프라인 테스트 — memory. 실행: pytest tests/test_week10.py -v"""

from docqa.memory import Memory


def test_short_term_recent(tmp_path):
    m = Memory(tmp_path / "lt.jsonl")
    for i in range(10):
        m.add_turn("user", f"메시지{i}")
    assert [t["content"] for t in m.recent(3)] == ["메시지7", "메시지8", "메시지9"]


def test_remember_persists_across_sessions(tmp_path):
    p = tmp_path / "lt.jsonl"
    Memory(p).remember("사용자의 연구 주제는 에이전트 평가다")
    m2 = Memory(p)                                  # 새 세션
    assert m2.recall("연구 주제", k=1) != []


def test_recall_returns_relevant_fact(tmp_path):
    p = tmp_path / "lt.jsonl"
    m = Memory(p)
    m.remember("사용자의 연구 주제는 에이전트 평가와 벤치마크다")
    m.remember("사용자는 매운 음식을 좋아한다")
    m.remember("실험 서버 주소는 lab-gpu-01이다")
    top = m.recall("연구 주제가 뭐였지", k=1)
    assert "에이전트 평가" in top[0]


def test_recall_empty_store(tmp_path):
    m = Memory(tmp_path / "none.jsonl")
    assert m.recall("아무거나") == []
