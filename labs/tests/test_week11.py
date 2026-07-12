"""W11 테스트 — graph. 배선(build_graph)은 langgraph 필요 — 없으면 자동 skip.
노드·분기 로직(제공분)은 오프라인 검증. 실행: pytest tests/test_week11.py -v"""

import pytest

from docqa import tools
from docqa.graph import agent_node, initial_state, should_continue, tool_node


@pytest.fixture(autouse=True)
def clean_registry():
    tools.TOOLS.clear()
    yield
    tools.TOOLS.clear()


def test_nodes_reach_answer_without_framework():
    """노드 3개를 손으로 돌려도 while 루프와 같은 동작 — '감싸기'의 증명."""
    script = iter([
        'Thought: 도구.\nAction: {"tool": "x", "input": "y"}',
        "Final Answer: 그래프",
    ])
    state = initial_state("q", llm_fn=lambda m: next(script))
    state = agent_node(state)
    assert should_continue(state) == "tools"
    state = tool_node(state)
    assert state["messages"][-1]["content"].startswith("Observation:")
    state = agent_node(state)
    assert state["answer"] == "그래프"
    assert should_continue(state) == "end"


def test_max_steps_guard():
    state = initial_state("q", llm_fn=lambda m: "Thought: 생각만.")
    for _ in range(10):
        if should_continue(state) == "end":
            break
        state = agent_node(state)
        if state["pending"]:
            state = tool_node(state)
    assert state["steps"] <= 5 or state["answer"] is None


def test_build_graph_matches_react_loop():
    pytest.importorskip("langgraph")               # 없으면 skip (W11 수업에서 설치)
    from docqa.graph import run
    script = iter([
        'Thought: 도구.\nAction: {"tool": "x", "input": "y"}',
        "Final Answer: 동일",
    ])
    assert run("q", llm_fn=lambda m: next(script)) == "동일"
