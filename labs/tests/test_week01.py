"""W1 오프라인 테스트 — API 키 불필요 (가짜 LLM 주입).

실행: pytest tests/test_week01.py -v
"""

from docqa.loop import parse_step, react_loop


# ── parse_step ──────────────────────────────────────────────

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


# ── react_loop ──────────────────────────────────────────────

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
            return 'Action: {"tool": "search", "input": "kt x"}'
        return "Final Answer: ok"

    react_loop("q", llm_fn=fake_llm, verbose=False)
    assert last_user[1].startswith("Observation:")


def test_loop_stops_at_max_steps():
    fake_llm = lambda messages: "Thought: 계속 생각만 한다."  # 영원히 답 없음
    result = react_loop("q", llm_fn=fake_llm, max_steps=3, verbose=False)
    assert "최대 스텝" in result
