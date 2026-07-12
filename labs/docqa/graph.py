"""W11 — LangGraph 전환점 🔄: "감싸기(wrap), 버리기 아님".

W2~W10에 직접 짠 부품(파싱·dispatch·도구)을 **그대로 노드의 속으로** 재사용하고,
while 루프가 하던 오케스트레이션(순서·분기·상태)만 LangGraph에 위임한다.

아래 노드 함수 3개는 제공된다 — 전부 우리 loop.py 부품을 부른다.
학생이 채우는 건 **배선(build_graph)** 하나: 우리 while문이 그래프 문법으로
어떻게 번역되는지를 손으로 확인하는 것이 이번 주의 전부다.

    while:  llm → final? → dispatch → 반복
    graph:  agent ─(should_continue)─→ tools ─→ agent … / → END
"""

from __future__ import annotations

from .loop import SYSTEM_PROMPT, dispatch, parse_step

MAX_STEPS = 5


def initial_state(question: str, llm_fn) -> dict:
    """그래프의 상태(state) — while 루프의 지역변수들이 명시적 딕셔너리가 된 것. (제공됨)"""
    from . import tools
    system = SYSTEM_PROMPT + ("\n\n" + tools.tool_list_prompt() if tools.TOOLS else "")
    return {
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": f"Question: {question}"}],
        "answer": None, "pending": None, "steps": 0, "llm_fn": llm_fn,
    }


def agent_node(state: dict) -> dict:
    """LLM 한 턴 — 우리 loop.py의 'llm_fn + parse_step' 부분 그대로. (제공됨)"""
    output = state["llm_fn"](state["messages"])
    parsed = parse_step(output)
    state = {**state, "steps": state["steps"] + 1}
    if parsed[0] == "final":
        return {**state, "answer": parsed[1], "pending": None}
    state["messages"] = state["messages"] + [{"role": "assistant", "content": output}]
    if parsed[0] == "action":
        return {**state, "pending": (parsed[1], parsed[2])}
    return {**state, "pending": ("__format_error__", "")}


def tool_node(state: dict) -> dict:
    """도구 실행 — 우리 dispatch() 그대로. (제공됨)"""
    tool, tool_input = state["pending"]
    if tool == "__format_error__":
        obs = "(형식 오류: 'Action: {...}' 또는 'Final Answer: ...' 형식으로 답하세요.)"
    else:
        obs = dispatch(tool, tool_input)
    return {**state, "pending": None,
            "messages": state["messages"] + [{"role": "user", "content": f"Observation: {obs}"}]}


def should_continue(state: dict) -> str:
    """분기 — while의 종료 조건이 함수가 된 것. (제공됨)"""
    if state["answer"] is not None or state["steps"] >= MAX_STEPS:
        return "end"
    return "tools"


def build_graph():
    """위 세 부품을 LangGraph로 배선한다.

    TODO(W11): 6~9줄.
      from langgraph.graph import StateGraph, END   ← 함수 안에서 import
      1) g = StateGraph(dict)
      2) add_node("agent", agent_node) · add_node("tools", tool_node)
      3) set_entry_point("agent")
      4) add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
      5) add_edge("tools", "agent")
      6) return g.compile()
    """
    try:
        from langgraph.graph import StateGraph, END  # noqa: F401
    except ImportError as e:
        raise ImportError("W11에는 langgraph가 필요합니다: pip install langgraph") from e
    raise NotImplementedError("TODO(W11): build_graph() 를 구현하세요")


def run(question: str, llm_fn=None) -> str:
    """그래프 실행 — react_loop()와 동일 동작이어야 한다(비교가 이번 주 완료 기준). (제공됨)"""
    if llm_fn is None:
        from . import llm
        llm_fn = lambda messages: llm.chat(messages, temperature=0.0)
    app = build_graph()
    final = app.invoke(initial_state(question, llm_fn))
    return final["answer"] or "(최대 스텝 도달 — 답을 확정하지 못했습니다)"
