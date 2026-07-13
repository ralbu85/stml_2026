"""W4 오프라인 테스트 — API 키 불필요 (가짜 LLM 주입).

W4 빈칸: loop.parse_step()
실행: pytest tests/test_week04.py -v
후반 테스트는 W3의 tools.py(run_tool·calculator)가 완성되어 있어야 통과한다.
"""

import pytest

from docqa import tools
from docqa.loop import parse_step, react_loop


@pytest.fixture(autouse=True)
def clean_registry():
    """전역 레지스트리를 테스트마다 비운다."""
    tools.TOOLS.clear()
    yield
    tools.TOOLS.clear()


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
        "Thought: 등록된 도구가 없으니 직접 답한다.\nFinal Answer: 2",
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


# ── 루프 × 도구 결합: 첫 완전한 에이전트 ────────────────────

def test_loop_calls_calculator_end_to_end():
    tools.register_defaults()
    seen_observations = []

    def fake_llm(messages):
        last = messages[-1]["content"]
        if last.startswith("Observation:"):
            seen_observations.append(last)
            return f"Thought: 관찰을 읽었다.\nFinal Answer: {last.split(':', 1)[1].strip()}"
        return 'Thought: 계산기를 쓰자.\nAction: {"tool": "calculator", "input": "12*34"}'

    answer = react_loop("12 곱하기 34는?", llm_fn=fake_llm, verbose=False)
    assert answer == "408"                       # ✅ W4 완료 기준
    assert "408" in seen_observations[0]         # 관찰로 진짜 결과가 들어왔다


def test_loop_system_prompt_lists_tools():
    tools.register_defaults()
    captured = {}

    def fake_llm(messages):
        captured["system"] = messages[0]["content"]
        return "Final Answer: ok"

    react_loop("q", llm_fn=fake_llm, verbose=False)
    assert "calculator" in captured["system"]  # W3 파이프라인 ①: 도구를 모델에게 알렸다
