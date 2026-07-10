"""W2 — ReAct 제어 루프 (하네스의 최소 형태).

모델에게 매 턴 아래 형식을 강제하고, 하네스(우리 코드)가 Observation을 채워
다시 모델에게 보내는 while 루프가 에이전트의 뼈대다.

    Thought: <추론>
    Action: {"tool": "<이름>", "input": "<입력>"}     ← 도구가 필요할 때
    ─ 또는 ─
    Thought: <추론>
    Final Answer: <답>                                ← 답을 확정할 때

W2에는 아직 도구가 없다(dispatch가 자리만 지킨다). W3의 tools.py가 그 자리를 채운다.
"""

import json
import re

SYSTEM_PROMPT = """\
당신은 단계적으로 생각하고 행동하는 에이전트다. 매 턴 반드시 아래 두 형식 중 하나로만 답한다.

도구가 필요할 때:
Thought: <지금까지의 추론>
Action: {"tool": "<도구이름>", "input": "<입력>"}

답을 확정할 때:
Thought: <최종 추론>
Final Answer: <답>

Observation: 은 시스템이 채워 준다 — 직접 쓰지 마라. Action 뒤에는 아무것도 쓰지 마라."""


def parse_step(text: str):
    """모델 출력 한 턴을 해석한다.

    Returns:
        ("final", 답변문자열)             — "Final Answer:" 가 있으면 (최우선)
        ("action", 도구이름, 입력문자열)  — "Action:" 뒤 JSON 객체가 파싱되면
        ("neither", 원문)                 — 둘 다 아니거나 JSON이 깨졌으면

    TODO(W2): 8~12줄.
      힌트 1) re.search(r"Final Answer:\\s*(.+)", text, re.S) — 답은 .strip() 해서 반환.
      힌트 2) re.search(r"Action:\\s*(\\{.*?\\})", text, re.S) 로 JSON 부분을 뽑아
              json.loads() → obj["tool"], obj["input"].
      힌트 3) json.JSONDecodeError 가 나면 ("neither", text).
    """
    raise NotImplementedError("TODO(W2): parse_step() 을 구현하세요")


def dispatch(tool: str, tool_input: str) -> str:
    """도구 실행 자리. (제공됨)

    W3부터: tools.py 레지스트리에 등록된 도구가 있으면 실제로 실행한다.
    등록된 게 없으면(W2 상태) 예전 스텁 그대로.
    """
    from . import tools
    if tools.TOOLS:
        return tools.run_tool(tool, tool_input)
    return (
        f"(아직 '{tool}' 도구가 없습니다. "
        "아는 범위에서 추론해 Final Answer를 내세요.)"
    )


def react_loop(question: str, llm_fn=None, max_steps: int = 5, verbose: bool = True) -> str:
    """Thought→Action→Observation 루프를 max_steps까지 돌린다. (제공됨)

    llm_fn: messages(list[dict]) -> str.  None이면 docqa.llm.chat 사용.
            테스트에서는 가짜 함수를 주입한다.
    """
    if llm_fn is None:
        from . import llm
        llm_fn = lambda messages: llm.chat(messages, temperature=0.0)

    from . import tools
    system = SYSTEM_PROMPT
    if tools.TOOLS:  # W3부터: 등록된 도구 목록을 모델에게 알린다 (파이프라인 ①)
        system += "\n\n" + tools.tool_list_prompt()

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"Question: {question}"},
    ]

    for step in range(1, max_steps + 1):
        output = llm_fn(messages)
        if verbose:
            print(f"\n──── step {step} ────\n{output}")

        parsed = parse_step(output)
        if parsed[0] == "final":
            return parsed[1]

        messages.append({"role": "assistant", "content": output})
        if parsed[0] == "action":
            observation = dispatch(parsed[1], parsed[2])
        else:
            observation = "(형식 오류: 'Action: {...}' 또는 'Final Answer: ...' 형식으로 답하세요.)"

        if verbose:
            print(f"Observation: {observation}")
        messages.append({"role": "user", "content": f"Observation: {observation}"})

    return "(최대 스텝 도달 — 답을 확정하지 못했습니다)"
