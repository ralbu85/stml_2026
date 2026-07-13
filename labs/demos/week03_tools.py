"""W3 데모 — function calling 단발 왕복: 스키마 → 호출 의도 → 파싱 → 실행 → 재주입.

실행: python demos/week03_tools.py "1400의 29%는 얼마야?"
✅ W3 완료 기준: 모델이 낸 호출 의도(JSON)를 파싱·실행해 결과가 최종 답에 반영된다.

관전 포인트:
1. 모델은 도구를 실행하지 않는다 — 호출 의도(JSON)를 출력할 뿐이고, 실행은 우리 코드다.
2. 반복(루프)이 없다 — 왕복 한 번뿐. 이 왕복을 while로 감는 것이 W4다.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from docqa import llm, tools

CALL_PROMPT = """\
아래 도구 중 하나가 필요하면 {{"tool": "<이름>", "input": "<입력>"}} 형식의 JSON 한 줄만 출력하라.
도구가 필요 없으면 답을 바로 출력하라.

{tool_list}

Question: {question}"""


def extract_call(text: str):
    """모델 출력에서 도구 호출 JSON을 찾는다. 없으면 None → 직접 답으로 간주."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
        return obj["tool"], obj["input"]
    except (json.JSONDecodeError, KeyError):
        return None


if __name__ == "__main__":
    tools.register_defaults()
    question = sys.argv[1] if len(sys.argv) > 1 else "1400의 29%는 얼마야?"

    # ① 스키마 제공 + ② 호출 의도 출력
    prompt = CALL_PROMPT.format(tool_list=tools.tool_list_prompt(), question=question)
    output = llm.ask(prompt, temperature=0.0)
    print(f"모델 출력:\n{output}\n")

    # ③ 파싱 → ④ 실행 → ⑤ 결과 재주입
    call = extract_call(output)
    if call is None:
        print("도구 호출 없음 — 모델이 직접 답했다.")
    else:
        name, tool_input = call
        observation = tools.run_tool(name, tool_input)
        print(f"실행 결과(Observation): {observation}\n")
        final = llm.ask(
            f"Question: {question}\n도구 '{name}' 실행 결과: {observation}\n이 결과로 최종 답을 한 문장으로.",
            temperature=0.0,
        )
        print(f"최종 답: {final}")
