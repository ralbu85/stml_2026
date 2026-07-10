"""W2 오프라인 테스트 — API 키 불필요 (가짜 LLM 주입).

W2 빈칸: loop.parse_step() · reasoning.majority_vote() · reasoning.self_consistency()
실행: pytest tests/test_week02.py -v
"""

from docqa.loop import parse_step, react_loop
from docqa.reasoning import extract_answer, majority_vote, self_consistency


# ── loop: parse_step ────────────────────────────────────────

def test_parse_final_answer():
    out = "Thought: 계산이 끝났다.\nFinal Answer: 42"
    assert parse_step(out) == ("final", "42")


def test_parse_action_json():
    out = 'Thought: 계산기가 필요하다.\nAction: {"tool": "calculator", "input": "400/1400"}'
    assert parse_step(out) == ("action", "calculator", "400/1400")


def test_parse_neither_on_free_text():
    kind, _ = parse_step("음... 잘 모르겠는데요.")
    assert kind == "neither"


def test_parse_broken_json_is_neither():
    kind, _ = parse_step('Action: {"tool": calculator}')  # 따옴표 없는 JSON
    assert kind == "neither"


# ── loop: react_loop ────────────────────────────────────────

def test_loop_reaches_final_answer():
    script = iter([
        'Thought: 도구를 써 보자.\nAction: {"tool": "calculator", "input": "1+1"}',
        "Thought: 도구가 없으니 직접 답한다.\nFinal Answer: 2",
    ])
    fake_llm = lambda messages: next(script)
    assert react_loop("1+1은?", llm_fn=fake_llm, verbose=False) == "2"


def test_loop_feeds_observation_back():
    """행동 다음 턴의 user 메시지가 Observation: 으로 시작해야 한다."""
    last_user = []

    def fake_llm(messages):
        last_user.append(messages[-1]["content"])
        if len(last_user) == 1:
            return 'Action: {"tool": "search", "input": "ktx"}'
        return "Final Answer: ok"

    react_loop("q", llm_fn=fake_llm, verbose=False)
    assert last_user[1].startswith("Observation:")


def test_loop_stops_at_max_steps():
    fake_llm = lambda messages: "Thought: 계속 생각만 한다."  # 영원히 답 없음
    result = react_loop("q", llm_fn=fake_llm, max_steps=3, verbose=False)
    assert "최대 스텝" in result


# ── reasoning: majority_vote ────────────────────────────────

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


# ── reasoning: self_consistency ─────────────────────────────

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
