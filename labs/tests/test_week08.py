"""W8 오프라인 테스트 — 검색을 도구로. 실행: pytest tests/test_week08.py -v"""

import pytest

from docqa import tools


class FakeRetriever:
    def query(self, q, k=3):
        return [f"청크1({q})", "청크2", "청크3"][:k]


@pytest.fixture(autouse=True)
def clean_registry():
    tools.TOOLS.clear()
    yield
    tools.TOOLS.clear()


def test_search_tool_registered():
    tools.register_search(FakeRetriever())
    assert "search_papers" in tools.TOOLS


def test_search_tool_returns_joined_chunks():
    tools.register_search(FakeRetriever())
    obs = tools.run_tool("search_papers", "ReAct 결과")
    assert "청크1(ReAct 결과)" in obs and "---" in obs


def test_description_says_when_not_to_use():
    """도구 정의가 곧 프롬프트 — '안 쓰나'까지 적었는지 (W4 체크리스트)."""
    tools.register_search(FakeRetriever())
    desc = tools.TOOLS["search_papers"]["description"]
    assert any(w in desc for w in ["안 쓰", "사용 금지", "쓰지 마"])


def test_loop_system_prompt_includes_search(monkeypatch):
    from docqa.loop import react_loop
    tools.register_search(FakeRetriever())
    captured = {}

    def fake_llm(messages):
        captured["system"] = messages[0]["content"]
        return "Final Answer: ok"

    react_loop("q", llm_fn=fake_llm, verbose=False)
    assert "search_papers" in captured["system"]
