"""W2 오프라인 테스트 — API 키 불필요 (가짜 LLM 주입).

W2 빈칸: reasoning.majority_vote() · reasoning.self_consistency()
실행: pytest tests/test_week02.py -v
"""

from docqa.reasoning import extract_answer, majority_vote, self_consistency


# ── majority_vote ───────────────────────────────────────────

def test_vote_basic():
    assert majority_vote(["9", "8", "9"]) == "9"


def test_vote_normalizes_before_counting():
    # "Paris." / "paris" 는 같은 표
    assert majority_vote(["Paris.", "paris", "London"]) == "paris"


def test_vote_ignores_none():
    assert majority_vote([None, "7", None, "7", "3"]) == "7"


def test_vote_tie_first_wins():
    assert majority_vote(["a", "b"]) == "a"


def test_vote_empty_returns_none():
    assert majority_vote([None, None]) is None


# ── self_consistency ────────────────────────────────────────

def test_self_consistency_majority():
    samples = iter([
        "차근차근 계산하면...\nFinal Answer: 9",
        "다르게 접근하면...\nFinal Answer: 8",
        "검산까지 하면...\nFinal Answer: 9",
    ])
    fake_llm = lambda messages, temperature: next(samples)
    best, answers = self_consistency("애매한 질문", n=3, llm_fn=fake_llm)
    assert best == "9"
    assert len(answers) == 3


def test_self_consistency_passes_temperature():
    seen_temps = []

    def fake_llm(messages, temperature):
        seen_temps.append(temperature)
        return "Final Answer: x"

    self_consistency("q", n=2, llm_fn=fake_llm, temperature=0.8)
    assert seen_temps == [0.8, 0.8]  # 다양성의 원천 — 0으로 보내면 안 된다


def test_extract_answer_falls_back_to_last_line():
    assert extract_answer("추론추론\n답은 아마도\n서울") == "서울"
