"""W3 오프라인 테스트 — API 키 불필요.

W3 빈칸: tools.run_tool() · tools.calculator()
실행: pytest tests/test_week03.py -v
(루프와의 결합 테스트는 W4 — tests/test_week04.py)
"""

import pytest

from docqa import tools


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
    obs = tools.run_tool("flaky", "x")       # 예외가 밖으로 나오면 호출자가 죽는다
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


# ── 단발 왕복: 모델 출력(JSON) → 파싱 → 실행 → 관찰 ─────────

def test_single_roundtrip_from_model_output():
    """W3 완료 기준 — 호출 의도(JSON)를 파싱·실행해 관찰 문자열을 얻는다."""
    import json

    tools.register_defaults()
    model_output = '{"tool": "calculator", "input": "1400*0.29"}'  # 모델이 낸 호출 의도
    call = json.loads(model_output)
    obs = tools.run_tool(call["tool"], call["input"])
    assert obs == "406"


def test_tool_list_prompt_mentions_all_tools():
    tools.register_defaults()
    prompt = tools.tool_list_prompt()
    assert "calculator" in prompt and "text_search" in prompt  # 파이프라인 ①: 스키마 제공
