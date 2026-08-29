"""제공 라이브러리 agent_lib 오프라인 테스트 — 배관이 올바른지 검증.

학생 빈칸(노트북의 프롬프트·흐름)은 여기서 검증하지 않는다. 이 테스트는
'제공 코드가 정확하다'만 보장한다. 실행: pytest tests/test_agent_lib.py -v
"""

import docqa.agent_lib as A


# ── 답 추출·정규화·채점 ─────────────────────────────────────

def test_extract_final_answer():
    assert A.extract_answer("풀이...\nFinal Answer: 9") == "9"


def test_extract_falls_back_to_last_line():
    assert A.extract_answer("추론\n답은 아마도\n서울") == "서울"


def test_normalize():
    assert A.normalize("  Paris. ") == "paris"


def test_contains_answer():
    assert A.contains_answer("계산하면 Final Answer: 160 이다", "160")
    assert not A.contains_answer("모르겠다", "160")


def test_majority_vote_basic():
    assert A.majority_vote(["9", "8", "9"]) == "9"


def test_majority_vote_ignores_none_and_normalizes():
    assert A.majority_vote([None, "Paris.", "paris", None]) == "paris"


def test_majority_vote_empty():
    assert A.majority_vote([None, None]) is None


# ── chat/ask (가짜 클라이언트 주입) ─────────────────────────

class _FakeMsg:
    def __init__(self, c): self.message = type("M", (), {"content": c})


class _FakeClient:
    """마지막으로 받은 messages를 기록하고 고정 답을 돌려주는 가짜 클라이언트."""
    def __init__(self): self.seen = None
    @property
    def chat(self): return self
    @property
    def completions(self): return self
    def create(self, model, messages, temperature=0.0, **kw):
        self.seen = messages
        return type("R", (), {"choices": [_FakeMsg("Final Answer: 42")]})


def test_chat_and_ask_wire_messages(monkeypatch):
    fake = _FakeClient()
    monkeypatch.setattr(A, "_client", fake)
    out = A.ask("질문", system="지침")
    assert out == "Final Answer: 42"
    assert fake.seen[0] == {"role": "system", "content": "지침"}
    assert fake.seen[1] == {"role": "user", "content": "질문"}


# ── accuracy (가짜 answer_fn) ───────────────────────────────

def test_accuracy_scores():
    evalset = [{"question": "q1", "answer": "9"}, {"question": "q2", "answer": "5"}]
    # 첫 문항만 맞히는 함수
    fn = lambda q: "Final Answer: 9" if q == "q1" else "Final Answer: 0"
    assert A.accuracy(fn, evalset, verbose=False) == 0.5


def test_load_evalset():
    items = A.load_evalset("reasoning_evalset.jsonl")
    assert len(items) >= 5
    assert all("question" in it and "answer" in it for it in items)
