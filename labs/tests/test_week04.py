"""W4 오프라인 테스트 — API 키 불필요.

W4 빈칸: tools.run_tool() · tools.calculator()
실행: pytest tests/test_week04.py -v
"""

import pytest

from docqa import tools
from docqa.loop import react_loop


@pytest.fixture(autouse=True)
def clean_registry():
    """전역 레지스트리를 테스트마다 비운다."""
    tools.TOOLS.clear()
    yield
    tools.TOOLS.clear()


# ── run_tool: 에러도 Observation이다 ────────────────────────

def test_run_tool_calls_registered_fn():
    tools.register("echo", "그대로 돌려준다", lambda x: f"echo: {x}")
    assert tools.run_tool("echo", "hi") == "echo: hi"


def test_run_tool_unknown_lists_available():
    tools.register("calculator", "계산", lambda x: x)
    obs = tools.run_tool("calculater", "1+1")  # 모델이 낸 오타
    assert "calculater" in obs and "calculator" in obs  # 가용 목록을 알려줘야 모델이 고친다


def test_run_tool_wraps_exceptions():
    def boom(x):
        raise RuntimeError("연결 실패")
    tools.register("flaky", "가끔 죽는 도구", boom)
    obs = tools.run_tool("flaky", "x")       # 예외가 밖으로 나오면 루프가 죽는다
    assert "오류" in obs and "연결 실패" in obs


def test_run_tool_truncates_long_output():
    tools.register("dump", "장문 출력", lambda x: "x" * 10_000)
    obs = tools.run_tool("dump", "")
    assert len(obs) <= tools.OBS_MAX_CHARS + 20
    assert "잘림" in obs


# ── calculator ──────────────────────────────────────────────

def test_calculator_precedence():
    assert tools.calculator("2+3*4") == "14"


def test_calculator_float():
    assert tools.calculator("400/1400").startswith("0.2857")


def test_calculator_integer_valued_division():
    assert tools.calculator("10/2") == "5"  # 5.0이 아니라 5


def test_calculator_rejects_code_via_run_tool():
    tools.register_defaults()
    obs = tools.run_tool("calculator", "__import__('os').system('ls')")
    assert "오류" in obs  # 실행되지 않고 관찰로 돌아온다


# ── 루프 통합: 계산기를 실제로 호출해 답한다 ────────────────

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
    assert "calculator" in captured["system"]  # 파이프라인 ①: 도구를 모델에게 알렸다
