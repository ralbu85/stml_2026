"""W15 오프라인 테스트 — 통합. 실행: pytest tests/test_week15.py -v"""

import importlib

import pytest

from docqa import tools


class FakeRetriever:
    chunks = ["ReAct의 결합 점수는 34.2다"]

    def query(self, q, k=3):
        return self.chunks


@pytest.fixture(autouse=True)
def clean():
    importlib.reload(tools)  # 가드레일 몽키패치·레지스트리 원복
    yield
    importlib.reload(tools)


def test_agent_answer_wires_everything():
    import app
    script = iter([
        'Thought: 논문을 찾자.\nAction: {"tool": "search_papers", "input": "ReAct 결합"}',
        "Thought: 찾았다.\nFinal Answer: 34.2",
    ])
    ans = app.agent_answer("ReAct 결합 점수는?", FakeRetriever(), llm_fn=lambda m: next(script))
    assert ans == "34.2"
    assert "search_papers" in tools.TOOLS          # W8 등록 확인
    assert getattr(tools.run_tool, "_guarded", False)  # W14 가드레일 확인


def test_baseline_always_retrieves():
    import app
    prompts = []

    def fake_llm(messages):
        prompts.append(messages[-1]["content"])
        return "답"

    app.baseline_answer("아무 질문", FakeRetriever(), llm_fn=fake_llm)
    assert "34.2" in prompts[0]                    # 무조건 검색해 붙였다
